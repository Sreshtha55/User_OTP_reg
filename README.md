Below are the steps followed by me to setup this project

1. Install python3 and pip. Below are the steps:

    sudo apt update
    sudo apt install python3-pip
    sudo pip3 install --upgrade pip
    sudo apt install python3



2. Install virtualenv by below command

    sudo apt install python3-virtualenv

3. Install Git by below commands

    sudo apt-get update
    sudo apt-get install git

4. Install docker by below commands

    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


5. Configure your Git username and email using followimg commnds

    git config --global user.name "Sresht"
    git config --global user.email "eparis@atlassian.com"

6. Create a folder and initialize git in it by below command

    git init

7. Create .gitignore file by below command and add all those contents in it that are not required to be tracked by git

    touch .gitignore

8. Create and then activate the virtualenv by below commands

    virtualenv env
    source env/bin/activate

9. Install django by below commnd

    pip install django

10. Create the django project in the current directory by below command

    django-admin startproject proj .

11. Create the basic django app in the django project by below command

    python manage.py startapp app

12. To consider the app in your project you need to specify your app name in INSTALLED_APPS list as follows in settings.py:

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
    ]

13. Add below in settings.py file to use local smtp-server

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp-server'
    EMAIL_PORT = 1025

14. Create requirements.txt file by below command

    pip freeze > requirements.txt

15. Created templates folder inside app folder and added home.html file

16. Created one model class Profile with 3 fields as user,email_otp,is_verified inside models.py. The field user has OnetoOne relationship with the default User model class

17. Run makemigrations and migrate command using below command so that all tables gets created in the default database sqlite

    python manage.py makemigrations 
    python manage.py migrate

18. Register this newly created model class in admins.py file using below command

    admin.site.register(Profile)

19. Created superuser using below commands

    python manage.py createsuperuser

20. Created below 4 functions

    home() -> This is main view function which runs first.

    genegenerateOTP() -> This is the function which generates random 4-digit OTP.

    send_otp() -> This is the function which sends email to user with the OTP and URL to get their email verify so that user can login inside website.

    verify() -> This is another view function which runs when user click the URL mentioned in the email. Once the user clicks the URL , is_verified field is updated to True so that user can login in the website later.


21. Created urls.py file inside app folder and added urlpatterns for the two view functions home() and verify().

22. Included the newly created path in urls.py of app inside the main project directory(proj) urls.py file using below line

    path('',include("app.urls"))

23. Created two files named Dockerfile and docker-compose.yml for docker configuration. There are two containers one for the django app and another for the smptp server. Django is exposed to 8000 port where smtp server container is exposed to two ports of localmachine which is 8025 and 1025 .

24. Run the docker container to test the code running or not by using below command

    sudo docker compose up -d

25. Once the docker conatiner is running then use below URLs in browser

    http://127.0.0.1:8000/ -> for django application.

    http://127.0.0.1:8025/ -> For SMTP Web UI.

26. If code is fine then add and commit the code in the local repository using below commands

    git add .
    git commit -m "Any message"

27. Create one Github repository and add the local repository to this Github remote repository using below commands

    git remote add origin <REMOTE_URL>

28. Push the code to remote Github repository using below commands

    git push origin master
