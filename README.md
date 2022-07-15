# stock_project
Reason - This project is for code review at stack builders



About the APP

The APP will manage your stock holdings and eventually can be implemented as Dividend Tracker for stocks

I used Django & Django rest framework to show my coding style. 
I also utilized test cases for Stock app, however I will add test cases for portfolio app later.

Also we can utilized celery to send email to the user or to run cron job.

This project is currently in development phase, so settings.py file isn't modified yet to deployment standerdeds.

Steps for getting started
1. Install dependency in your virutualenv
   - pip install -r requirement.txt

2. Do Migration and Migrate
  - python manage.py makemigrations
  - python manage.py migrate

3. Create superuser
  - python manage.py createsuperuser

4. Explore the api and send me feedback!
