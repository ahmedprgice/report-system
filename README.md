# Campus Security

# To run the project
***Prerequisite***
1. Download and Install ngrok `https://ngrok.com/download`
2. Create a free account and login to access you token
3. Open ngrok and add token to your computer `ngrok config add-authtoken <YOUR TOKEN>`
4. Start an ngrok server for your local machine `ngrok http http://localhost:8000`
5. Copy the ngrok link and replace the BASE_URL `app/views.py LINE 20`
6. Add your ngrok url to CSRF Trusted Origins in `cmp/settings.py Line 30`
7. Create a virtual environment in your project folder `python -m venv .venv`
8. Activate environment `.venv/Scripts/activate`
9. run `pip install -r requirements.txt` 
10. run `python manage.py makemigrations`
11. run `python manage.py migrate`
12. run `python manage.py runserver`
13. Open the ngrok url from any device

# Default Admin Login
email='admin@example.com', 
username='admin', 
password='admin'

*** you can update default admin login in app/migrations/0002_generate_adminuser.py Line 6 ***
*** NOTE: You need to do this before you do step 10***
