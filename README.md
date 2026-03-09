
# CarEase - Car Service Management Application

## Project Overview
CarEase is designed to help users manage their car services efficiently. It allows users to book appointments, track service progress, and make payments using M-Pesa. The application is built using Flask, a lightweight WSGI web application framework in Python.

## current Features
- View different services offered
- Book appointments for services 
- responsive web interface

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

# Project Structure

```
project/
├── static/
│   ├── css
│   ├── js
│   
├── templates/
│   ├── 404.html
│   └── index.html
│   └── about.html
│   └── contact.html
│   └── progress.html
│   └── services.html
│   └── tracking.html
├── app.py
├── carease.db
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
