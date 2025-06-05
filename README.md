## WhatApp Booking Bot

A sleek, user-friendly WhatsApp chatbot built with Django to streamline booking management. Create, check, or cancel bookings effortlessly through an intuitive menu-driven conversation flow.

## Features
* Interactive Menu: Users can make, check, or cancel bookings with simple commands (1, make, etc.).
* Persistent State Management: Tracks user interactions using a Django model for seamless conversation flow.
* Real-Time Web Chat: A responsive web interface mirrors WhatsApp-style messaging with sent/received indicators and message status
* WhatsApp API Integration: Processes incoming messages and sends responses via a custom WhatsApp API wrapper.
* Twilio Integration: Leverages Twilio's WhatsApp API for reliable messaging.


## Tech stack
* Backend: Django, Python
* UI: HTML, Tailwind CSS, JavaScript
* Database: PostgreSQL
* API: Twilio WhatsApp API via custom wrapper

## Setup
1. Clone the repo:
   ```bash
    git clone https://github.com/alexander784/Whatsapp_bot.git
    cd Whatsapp
2. Install dependecies:
   ```bash
   pip install -r requirements.txt
3. Apply migrations:
   ```bash
   python3 manage.py migrate

4. Configure Twilio credentials: 
    Create  .env file and store the  (Account SID, Auth Token, and WhatsApp number)
 5. Run server:
    ```bash
    Python3 manage.py runserver


## Usage
* Whatsapp: Text "hey","hi", to Twilion Whatsapp number to start.
* Open you fav web browser http://localhost:8000/web_chat for a WhatsApp-style interface.
* Follow instructions after sending greetings.

## Project Structure
* views.py: Manages webhook and web chat logic.
* models.py: Defines User, Message, and Booking models.
* utils/whatsapp_api.py: Handles Twilio WhatsApp API integration.
* templates/whats_app/web_chat.html: Renders the web chat UI.


## Contribution
Contributions are always welcome! Open an issue for discussion or submit a pull request.

## License
MIT License

Feel free to reach out: **ga.nyaga7@gmail.com**




