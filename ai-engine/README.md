# AI Engine (Rupee AI)

Rupee AI is an LLM based chatbot application for assistance to users of India. 
AI Engine serves requests from `frontend` services asynchronously.

This backend application utilizes "FastAPI Framework" (a Python based Asynchronous framework) for Backend development in Python. Read all instructions carefully before working.

### Last Updated on

21 November, 2024 11:07 P.M. IST

### Authors

- [Rohan](https://github.com/rohankvashisht/)

### General Instructions

Current Path: user@username working_directory $

```
# Create the project directory
mkdir project-<PROJECT_NAME>

# Select project folder as current working directory
cd project-<PROJECT_NAME>

# Create directory for FastAPI services
mkdir ai-engine

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv ai-engine-env

# Activate virtual environment
source ai-engine-env/bin/activate  # On Windows use `ai-engine-env\Scripts\activate`

# To deactivate the currently activated environment, type command
deactivate
```

As Industry practice GitHub clone repository outside of the virtual environment folder to maintain a clean project structure and avoids mixing codebase with the virtual environment configurations.

```
# Install the Git repository adjacent to virtual environment folder (outside of `ai-engine-env`)
git clone https://github.com/<path-to-repo>/ai-engine.git

# Select this project folder (cloned repo) as current working directory
cd ai-engine
```

###  Directory Structure overview

Local Folders and Navigation: working_directory (Your Local Path) -> project-<PROJECT_NAME> (Local Folder) -> ai-engine-env (Virtual Environment) , ai-engine (Cloned GitHub Repository)

Project folder Constitution: ai-engine (GitHub Repo) -> `core`, `files`, `apis`, main.py, README.md, requirements.txt, .gitignore

### Package Dependency Management

This FastAPI application runs on Python v3.12.4.
To effectively solve dependency conflicts, we have used `requirements.txt`

```
# Generate requirements file
pip freeze > requirements.txt
```

### Backend Instructions

Documentation: [Installation](https://fastapi.tiangolo.com/#installation), [Dependencies](https://fastapi.tiangolo.com/#dependencies), [Learn](https://fastapi.tiangolo.com/learn/), [References](https://fastapi.tiangolo.com/reference/)

Current Path: (ai-engine-env) user@username ai-engine $

```
# Install FastAPI framework, Langchain etc. into the selected virtual environment using `requirements.txt` file
pip install -r requirements.txt

```

Note: Create and keep your `.env` file here in `ai-engine` folder of your cloned repository. 

```
# Select `core` folder as current working directory
ls core/

# Observe that the folder contains python files for FastAPI applications with names like: `utils.py`, `llm.py`, ..
```

#### Configure env file

`.env` file is kept in `ai-engine` folder of your cloned repository

Critical Parameters that should be mentioned in `.env` file are:

- DEBUG = 'True' or 'False'
- HOST = Your Server\'s IP Address
- PORT = Port number to which this app is exposed
- OPENAI_API_KEY = For LLM based content generation
- TAVILY_API_KEY = For web based search results

#### Deployment

```
# FastAPI depends on Pydantic and Starlette, use "standard" package to start with
pip install "fastapi[standard]"

# Testing FastAPI on Uvicorn development server
fastapi dev ./main.py --host <CUSTOM_HOST> --port <CUSTOM_PORT>

# Development server starts at http://127.0.0.1:8000/ by default
# Quit the server with CONTROL-C in Windows or CMD + C for Mac

# Run a FastAPI ASGI production server (Uvicorn) manually
fastapi run ./main.py --host <CUSTOM_HOST> --port <CUSTOM_PORT>

# You can also start a Uvicorn server
# Installing additional dependencies
pip install "uvicorn[standard]"

# Run a Uvicorn server manually
uvicorn main:app --host <CUSTOM_HOST> --port <CUSTOM_PORT>
```
