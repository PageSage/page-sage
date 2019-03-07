# `pip` Requirements Folder #

This folder is for the various `pip` package requirements needed for deployment, testing, and development.


## `common.txt` ##
* Requirements file to be used for deployment and be head to head with `../requirements.txt`
* Contents:
	* `Flask` : the framework that runs the app
	* `Flask-WTF` : a form handler for the website
	* `Flask-SQLAlchemy` : the database mapper
	* `Flask-Dance` : the OAuth2 handler for logins; most actively developed and modern
	* `Flask-Login` : the AuthN handler for Flask
	* `Flask-Migrate` : the alembic wrapper for easy DB migrations
	* `sqlalchemy_utils` : a necessary component for flask-migrate

## `dev.txt` ##
* Requirements file to be used for components that are in development and not ready for deployment
* Also uses all of the dependencies from `common.txt`

## `test.txt` ##
* Requirements file to be used for components that are only needed for testing
* Also uses all of the dependencies from `common.txt`
