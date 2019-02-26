[![Build Status](https://travis-ci.com/PageSage/page-sage.svg?branch=master)](https://travis-ci.com/PageSage/page-sage)  [![codecov](https://codecov.io/gh/PageSage/page-sage/branch/master/graph/badge.svg)](https://codecov.io/gh/PageSage/page-sage)  [![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=PageSage_page-sage&metric=alert_status)](https://sonarcloud.io/dashboard?id=PageSage_page-sage)


# Page Sage #
"To help book clubs select books that will be generally well received by the entire group."


## How to Run ##
*Basic Requirements to run this app:*
* *python3.6*
* *GoogleAPI keys (more below)*
* *A Bash style terminal is recommended*


1. Set up a virtual environment with:
	* `python3 -m venv venv`
	* `source ./venv/bin/activate`
	* This is not entirely necessary, but it keeps the environment and your machine cleaner
2. Clone our project and enter the directory:
	* `git clone https://github.com/PageSage/page-sage`
	* `cd page-sage`
3. Set up your Google Cloud Console:
	* Navigate to [Google Cloud Console](https://console.cloud.google.com)
	* Set up a new application
	* Under API Services & Credentials, click "Create Credentials" and "OAuth client ID"
	* Choose webapp
	* Your "Authorized JavaScript origins" should be: `http://localhost:5000`
	* Your "Authorized redirect URIs" should be: `http://localhost:5000/google-login/google/authorized`
	* *Please remember to never publish your Client ID or any active API keys on a public platform*
4. Set up the database:
	* `flask init db`
	* `flask migrate -m "Your migration message here"`
	* `flask upgrade` <-- This command may fail occasionally

### Choose one of the following methods to run the app: ###

### Run with Python ###
5. Set your environment variables:
	* `export GOOGLE_SECRET=<your_google_key>`
	* `export GOOGLE_CLIENT_ID=<your_client_id>`
	* `export SECRET_KEY=<your_secret_key>`
	* It is advised to use a randomized, (at least) 64-bit secret key for this
6. Install the dependencies:
	* `pip install --upgrade pip && pip install -r requirements.txt`
7. Run the app:
	* `python3 page-sage.py`
	* Close the app with `Ctrl + C`


### Run with Docker ###
5. Ensure you have a docker client installed and running
6. Set your environment variables in `Dockerfile`:
	* `ENV GOOGLE_SECRET=<your_google_key>`
	* `ENV GOOGLE_CLIENT_ID=<your_client_id>`
	* `ENV SECRET_KEY=<your_secret_key>`
	* It is advised to use a randomized, (at least) 64-bit secret key for this
7. Run the app:
	* `./build_and_run.sh`


### Run on Deployment-level Server (with Docker) ###
5. Ensure you have a docker client installed and running
6. Switch `Dockerfile` to the `Dockerfile_deploy` file contents
	* `./switch_to_deploy`
7. Set your environment variables in `Dockerfile`:
	* `ENV GOOGLE_SECRET=<your_google_key>`
	* `ENV GOOGLE_CLIENT_ID=<your_client_id>`
	* `ENV SECRET_KEY=<your_secret_key>`
	* It is advised to use a randomized, (at least) 64-bit secret key for this
8. Run the app:
	* `./build_and_run.sh`


*If you would like to work as a developer on this project, please open an issue and let us know there*



## Folder Information ##

Documentation for the contents of the main folder.

### `requirements/` ###
* Folder of pip dependencies for testing, development, and deployment

### `app/` ###
* Main application folder for Flask components

### `Dockerfile` ###
* Our development and test-level Dockerfile
* Uses `python:3.6-alpine` for lightweight usage
	* The Alpine distributions tend to be the most light-weight and fastest overall

### `Dockerfile_deploy` ###
* Our deployment level Dockerfile
* Uses `tiangolo/meinheld-gunicorn-flask:python3.6-alpine3.8` for server speed
* Module and Variable are the same for this app's case but need to be set for the dockerfile

### `./build_and_run.sh` ###
* Shell script to help automate the Dockerfile building and image running
* Opens port 5000 by default
* Adds the whole folder contents

### `config.py` ###
* Configuration file for Flask
* Gets environmental variables for the secret key (to help prevent CSRF attacks) and the database (SQLite still, in our case)

### `page-sage.py` ###
* Basic app runner file
* Opens up at `0.0.0.0` so the port can be found by the Dockerfile to be exposed externally

### `requirements.txt` ###
* The deployment requirements folder

### `./switch_to_deploy.sh` ###
* Shell script to rotate `Dockerfile_deploy` into `Dockerfile` and the previous `Dockerfile` to `Dockerfile_Develop`
* For testing with the deployment level server

### `./switch_to_develop.sh`
* Shell script to rotate `Dockerfile_develop` into `Dockerfile` and the previous `Dockerfile` to `Dockerfile_Develop`
* For reverting from testing with the deployment level server

### `test_page-sage.py` ###
* Test file for app
* Most tests rely on no login being present
* Naming from convention for `pytest` test runner

### `test_page-sage_login_required.py` ###
* Test file for app
* Tests depend on login being present and required
* Cannot disable login functionality with app or test with OAuth2 as exclusive login currently
	* Only tests for 401 errors




*Want more documentation? Let us know!*
