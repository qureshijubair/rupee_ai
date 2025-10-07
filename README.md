# ₹upee AI
Rupee AI is an LLM based chatbot application for financial Assistance to citizens of India.

NOTE: This is a management project undertaken for partial fulfillment of degree in Data Science and AI in MBA from IIT Mandi, Himachal Pradesh, India

This web application utilizes "Django REST Framework" (a Django based framework) for Backend development and "SvelteKit framework" (a SvelteJS Web framework) for Frontend Web development. Read all instructions carefully before working.

### General Instructions

Current Path: user@username working_directory %

```
# Create the project directory
mkdir finance-management-project
cd finance-management-project

# Select project folder as current working directory
cd finance-management-project

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv rupee-ai-env

# Activate virtual environment
source rupee-ai-env/bin/activate  # On Windows use `rupee-ai-env\Scripts\activate`

# To deactivate the currently activated environment, type command
deactivate
```

As Industry practice GitHub clone repository outside of the virtual environment folder to maintain a clean project structure and avoids mixing codebase with the virtual environment configurations.

```
# Install the Git repository adjacent to virtual environment folder (outside of `rupee-ai-env`)
git clone https://github.com/rohankvashisht/rupee-ai.git

# Select this project folder (cloned repo) as current working directory
cd rupee-ai
```

###  Directory Structure overview

Local Folders and Navigation: working_directory (Your Local Path) -> finance-management-project (Local Folder) -> rupee-ai-env (Virtual Environment) , rupee-ai (Cloned GitHub Repository)

Project folder Constitution: rupee-ai (GitHub Repo) -> backend, frontend, README.md, .gitignore

### Backend Instructions

Documentation: [Installation](https://www.django-rest-framework.org/#installation) , [Quickstart](https://www.django-rest-framework.org/#quickstart)

Current Path: (rupee-ai-env) user@username rupee-ai %

```
# Select `backend` folder as current working directory
cd backend

# Observe the `django_rest_project` project folder which contains Django REST Framework files and folders code

# Install Django, Django REST framework, etc. into the selected virtual environment using `requirements.txt` file
pip install -r requirements.txt

# Select `django_rest_project` folder as current working directory
cd django_rest_project

# Observe that the folder contains existing Django applications with names like: chatbot, ..

# Go back to previous directory
cd ..

# Working in Django shell
python manage.py shell

# Quit out of the Django shell
quit()

# For migrations
python manage.py makemigrations

# For migrations for our `chatbot` model
python manage.py makemigrations chatbot

# For syncing database: SQLite
python manage.py migrate

# For syncing database for our `chatbot` model
python manage.py migrate chatbot

# Testing API on Django's development server
python manage.py runserver

# Development server starts at http://127.0.0.1:8000/ by default
# Quit the server with CONTROL-C
```

### Frontend Instructions

Documentation: [Introduction](https://kit.svelte.dev/docs/introduction) , [Tutorial](https://learn.svelte.dev/tutorial/welcome-to-svelte)

Current Path: (rupee-ai-env) user@username rupee-ai %

```
# Select `frontend` folder as current working directory
cd frontend

# Select `sveltekit-app` project folder as current working directory
cd sveltekit-app

# Install node install dependencies with `npm install` (or `pnpm install` or `yarn`) into the selected virtual environment
npm install
```

To update Node.js itself, I recommend you use [nvm](https://github.com/creationix/nvm), the [Node Version Manager](https://github.com/creationix/nvm).
Refer this [StackOverflow Question](https://stackoverflow.com/questions/6237295/how-can-i-update-node-js-and-npm-to-their-latest-versions)

```
# `nvm` allows you to quickly install and use different versions of node via the command line.

nvm use 16
# Now using node v16.9.1 (npm v7.21.1)
node -v
v16.9.1

nvm install 12
# Now using node v12.22.6 (npm v6.14.5)
node -v
v12.22.6
```

```
# Start the server in localhost with preassigned port
npm run dev

# Or start the server and open the app in a new browser tab
npm run dev -- --open

# Create a production version of your app
npm run build

# Preview the production build
npm run preview
```