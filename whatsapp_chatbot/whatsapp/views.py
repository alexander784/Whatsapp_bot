import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from .utils.whatsapp_api import WhatsAppAPI
from .models import User, Message, Booking


def get_booking_response(message_text, sender):
    """Handle booking conversation with menu-driven flow."""
    message_text = message_text.lower().strip()
    user, _ = User.objects.get_or_create(phone_number=sender)

    menu_options = [
        "1. Make a Booking",
        "2. Check Bookings",
        "3. Cancel Booking",
        "4. Help"
    ]
    menu_text = (
    "📋 Booking Bot Menu\n" 
    "Welcome! Please choose an option:\n"
    "1️⃣  Make a Booking\n"
    "2️⃣  Check Bookings\n"
    "3️⃣  Cancel Booking\n"
    "4️⃣  Help\n\n"
    "_Reply with the number or keyword (e.g., '1' or 'make')._"
)

    # Handle greetings
    if message_text in ["hey", "hi", "hello"]:
        user.state = 'menu'
        user.temp_data = {}
        user.save()
        return menu_text

    # Handle conversation based on state
    if user.state == 'menu':
        option = None
        if message_text in ["1", "make"]:
            option = "make"
        elif message_text in ["2", "check"]:
            option = "check"
        elif message_text in ["3", "cancel"]:
            option = "cancel"
        elif message_text in ["4", "help"]:
            option = "help"
        else:
            return "Booking Bot: Invalid option. Reply with a number (1-4) or keyword (make, check, cancel, help)."

        if option == "make":
            user.state = 'booking_date'
            user.save()
            return "Booking Bot: Please enter the booking date (YYYY-MM-DD), e.g., 2025-06-01."
        elif option == "check":
            bookings = Booking.objects.filter(user=user)
            user.state = 'initial'
            user.save()
            if bookings:
                response = "Booking Bot: Your bookings:\n" + "\n".join(
                    [f"- {b.date}: {b.details}" for b in bookings]
                )
            else:
                response = "Booking Bot: No bookings found."
            return response + "\nSay 'hey' to see the menu again."
        elif option == "cancel":
            bookings = Booking.objects.filter(user=user)
            if not bookings:
                user.state = 'initial'
                user.save()
                return "Booking Bot: No bookings to cancel. Say 'hey' to see the menu."
            user.state = 'cancel_select'
            user.save()
            return "Booking Bot: Your bookings:\n" + "\n".join(
                [f"{i+1}. {b.date}: {b.details}" for i, b in enumerate(bookings)]
            ) + "\nReply with the number to cancel, or 'back' to return."
        elif option == "help":
            user.state = 'initial'
            user.save()
            return "Booking Bot: I can help with:\n- Make a Booking: Create a new booking\n- Check Bookings: View your bookings\n- Cancel Booking: Remove a booking\n- Help: Show this message\nSay 'hey' to start."

    elif user.state == 'booking_date':
        try:
            booking_date = datetime.strptime(message_text, "%Y-%m-%d").date()
            user.temp_data = {'date': message_text}
            user.state = 'booking_details'
            user.save()
            return "Booking Bot: What are you booking? (e.g., Hotel Room, Flight, Appointment)"
        except ValueError:
            return "Booking Bot: Invalid date format. Please use YYYY-MM-DD, e.g., 2025-06-01."

    elif user.state == 'booking_details':
        details = message_text or "General Booking"
        booking_date = datetime.strptime(user.temp_data.get('date'), "%Y-%m-%d").date()
        Booking.objects.create(user=user, date=booking_date, details=details)
        user.state = 'initial'
        user.temp_data = {}
        user.save()
        suggestion = "Booking Bot: Your booking for {} on {} is confirmed!\nWould you like to make another booking? Reply 'yes' or 'no'.".format(details, booking_date)
        return suggestion

    elif user.state == 'cancel_select':
        if message_text == 'back':
            user.state = 'menu'
            user.save()
            return menu_text
        try:
            index = int(message_text) - 1
            bookings = Booking.objects.filter(user=user)
            if 0 <= index < len(bookings):
                booking = bookings[index]
                booking.delete()
                user.state = 'initial'
                user.save()
                return "Booking Bot: Booking for {} on {} cancelled. Say 'hey' to see the menu.".format(booking.details, booking.date)
            return "Booking Bot: Invalid number. Reply with a number from the list or 'back'."
        except ValueError:
            return "Booking Bot: Please reply with a number or 'back'."

    if user.state == 'initial' and message_text in ['yes', 'no']:
        if message_text == 'yes':
            user.state = 'menu'
            user.save()
            return menu_text
        return "Booking Bot: Thanks for using Booking Bot! Say 'hey' to start again."

    return "Booking Bot: Say 'hey', 'hi', or 'hello' to see the menu!"

@csrf_exempt
def webhook(request):
    if request.method == "GET":
        return JsonResponse({"status": "success"}, status=200)
    
    elif request.method == "POST":
        try:
            whatsapp_api = WhatsAppAPI()
            sender, message_text = whatsapp_api.process_incoming_message(request.POST)
            
            if sender and message_text:
                user, created = User.objects.get_or_create(phone_number=sender)
                Message.objects.create(user=user, text=message_text, is_sent=False,status='sent')
                
                response_text = get_booking_response(message_text, sender)
                whatsapp_api.send_message(sender, response_text)
                Message.objects.create(user=user, text=response_text, is_sent=True,status='delivered')
                
                return JsonResponse({"status": "success"}, status=200)
            
            return JsonResponse({"status": "no_message"}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return JsonResponse({"status": "invalid"}, status=400)

def web_chat(request):
    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:
            whatsapp_api = WhatsAppAPI()
            sender = "+254796097131"
            user, _ = User.objects.get_or_create(phone_number=sender)
            Message.objects.create(user=user, text=message_text, is_sent=False)
            response_text = get_booking_response(message_text, sender)
            whatsapp_api.send_message(sender, response_text)
            Message.objects.create(user=user, text=response_text, is_sent=True)
        return redirect('web_chat')
    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'whats_app/web_chat.html', {'messages': messages})

def get_messages(request):
    messages = Message.objects.all().order_by('timestamp')
    data = [{
        'phone_number': message.user.phone_number,
        'text': message.text,
        'is_sent': message.is_sent,
        'timestamp': message.timestamp.strftime('%H:%M, %d %b %Y'),
        'status': message.status
    } for message in messages]
    return JsonResponse({'messages': data})
