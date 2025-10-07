# Back-End Application

This is a Python based backend application for assistance to users of Rupee AI.

NOTE: This is a internal project under Rupee AI Labs, School of Management, IIT Mandi, Himachal Pradesh, India.

This backend application utilizes "Django REST Framework" (a Django based framework) for Backend development in Python. Read all instructions carefully before working.

### Authors

Rohan: [Github](https://github.com/rohankvashisht/)

### General Instructions

Current Path: user@username working_directory $

```
# Create the project directory
mkdir project-hr-bot

# Select project folder as current working directory
cd project-hr-bot

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv rest-backend-env

# Activate virtual environment
source rest-backend-env/bin/activate  # On Windows use `rest-backend-env\Scripts\activate`

# To deactivate the currently activated environment, type command
deactivate
```

As Industry practice GitHub clone repository outside of the virtual environment folder to maintain a clean project structure and avoids mixing codebase with the virtual environment configurations.

```
# Install the Git repository adjacent to virtual environment folder (outside of `rest-backend-env`)
git clone https://gitlab.com/<path-to-repo>/rest-backend.git

# Select this project folder (cloned repo) as current working directory
cd rest-backend
```

###  Directory Structure overview

Local Folders and Navigation: working_directory (Your Local Path) -> project-hr-bot (Local Folder) -> rest-backend-env (Virtual Environment) , rest-backend (Cloned GitLab Repository)

Project folder Constitution: rest-backend (GitLab Repo) -> `backend`, README.md, .gitignore

### Package Dependency Management

This Django REST application runs on Python v3.12.4.
To effectively solve dependency conflicts, pipreqs and pip-tools are used, refer this [StackOverflow Answer](https://stackoverflow.com/questions/31684375/automatically-create-file-requirements-txt/69081814#69081814).

```
# Navigate to the `backend` folder
cd ./path/to/backend/

# Install pipreqs
pip3 install pipreqs

# Install pip-tools
pip3 install pip-tools

# Use the following to build a deterministic requirements.txt
pipreqs . --savepath=requirements.in

# Generate .txt file from .in
pip-compile requirements.in

# Go back to previous directory
cd ..
```

### Backend Instructions

Documentation: [Installation](https://www.django-rest-framework.org/#installation), [Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/), [Tutorial](https://www.django-rest-framework.org/tutorial/1-serialization/)

Current Path: (rest-backend-env) user@username rest-backend $

```
# Select `backend` folder as current working directory (if not already)
cd backend

# Observe the `django_rest_project` project folder which contains Django REST Framework files and folders code

# Install Django, Django REST framework, etc. into the selected virtual environment using `requirements.txt` file
pip install -r requirements.txt

```

Backend (`backend`) folder Constitution: requirements.in, requirements.txt, `django_rest_project`

Note: Create and keep your `.env` file here in `backend` folder of your cloned repository. 

```
# Select `django_rest_project` folder as current working directory
cd django_rest_project

# Observe that the folder contains existing Django applications with names like: `django_rest_project`, `chatbot`, ..
```

Django REST (`django_rest_project`) folder Constitution: manage.py, `static`, `django_rest_project`, `chatbot`

Note: Refer to this StackOverflow Post for files and folder structure: [StackOverflow Answer](https://stackoverflow.com/questions/48624307/must-a-django-rest-framework-app-really-be-a-subfolder-of-the-projects-root-app)

```
# Working in Django shell
python manage.py shell

# Quit out of the Django shell
quit()

# For migrations
python manage.py makemigrations

# For migrations for our `chatbot` app
python manage.py makemigrations chatbot

# For syncing database: SQLite
python manage.py migrate

# For syncing database for our `chatbot` model
python manage.py migrate chatbot

# Testing API on Django's development server
python manage.py runserver <CUSTOM_IP_ADDRESS>:<CUSTOM_PORT_NUMBER>

# Development server starts at http://127.0.0.1:8000/ by default
# Quit the server with CONTROL-C in Windows or CMD + C for Mac
```
#### Configure env file

`.env` file here in kept in `backend` folder of your cloned repository, which is just outside of the Django REST (`django_rest_project`) folder.

Critical Parameters that should be mentioned in `.env` file are:

- DEBUG = 'True' or 'False'
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_API_TYPE
- AZURE_OPENAI_API_VERSION
- AZURE_OPENAI_DEFAULT_DEPLOYMENT_NAME
- AZURE_OPENAI_DEPLOYMENT_VERSION
- AZURE_OPENAI_MODEL_NAME
- DB Credentials

#### Configure Static Content

Websites generally need to serve additional files such as images, JavaScript, or CSS. 

In Django, these files are refered as "static files". Django provides `django.contrib.staticfiles` to help you manage them.

To understand how to configure and manage, refer this [link](https://docs.djangoproject.com/en/5.0/howto/static-files/).

```
# Run the collectstatic management command
# if `static` folder is not present in `django_rest_framework` folder
python manage.py collectstatic
```