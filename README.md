
# CarEase - Car Service Management Application

## Project Overview
CarEase is designed to help users manage their car services efficiently. It allows users to book appointments, track service progress, and make payments using M-Pesa. The application is built using Flask, a lightweight WSGI web application framework in Python.

Data gathering Google Docs link:
https://docs.google.com/forms/d/e/1FAIpQLSeXR9nBmfDFY7w0Meq_6i_pH_08KBlFlhqub2hYKlVpuSw_NA/viewform?usp=header

## Features
- View different services offered
- Book appointments for services 
- View and manage appointments
- Pay for services using M-Pesa 
- Service progress tracking
- Email notifications

## Technologies Used
- **Backend**: Flask (Python), Blueprint architecture, Flask-SocketIO, flask-cors
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, Leaflet.js maps, Socket.IO client
- **Payment Integration**: M-Pesa (via Daraja API)
- **Email Notifications**: SMTP2Go
- **Version Control**: Github
- **Deployment**: Ngrok for local development and testing of the Daraja API integration

## Requirements
- Python 3.x
- Flask
- SQLite
- ngrok for daraja api integration


# Project Structure

```
project/
├── api/
│   ├── __init__.py
│   ├── appointments.py
│   ├── booking.py
│   ├── contact.py
│   ├── daraja.py
│   ├── tracking.py
│   ├── users.py
│   └── util.py
├── db/
│   ├── __init__.py
│   ├── util/
│   │   ├── create.py
│   │   ├── drop.py
│   │   ├── insert.py
│   └── carease.db
│   └── initialize.py
├── misc/
│   ├── __init__.py
│   ├── helpers.py
│   └── constants.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│   └── lib/
│   └── scss/
├── templates/
│   ├── 404.html
│   └── index.html
│   └── about.html
│   └── contact.html
│   └── progress.html
│   └── services.html
│   └── tracking.html
├── views/
│   ├── __init__.py
│   ├── index.py
│   └── about.py
│   └── contact.py
│   └── progress.py
│   └── services.py
│   └── tracking.py
├── app.py
├── requirements.txt
├── README.md
```
## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/24-nyalim/CarEase.git
    cd CarEase
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Initialize the database:
    ```bash
    python db/initialize.py
    ```
6. Run the application:
    ```bash
    python app.py
    ```
7. Access the application in your web browser at `http://localhost:[PORT]`, where `[PORT]` is the port number specified in `app.py`.

## Environment Variables
Create a `.env` file in the project root with:

```env
SMTP2GO_API_KEY=api-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SMTP2GO_SENDER=verified-sender@yourdomain.com
MPESA_CONSUMER_KEY=...
MPESA_CONSUMER_SECRET=...
MPESA_PASSKEY=...
CALLBACK_URL=...
```

Notes:
- `SMTP2GO_SENDER` must be a sender identity verified inside your SMTP2GO account.
- If you rotate SMTP2GO credentials, only replace `SMTP2GO_API_KEY` and keep the same variable name.
