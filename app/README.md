# `app` Folder #

These are the main files and folders for PageSage.


## Folders ##

### `static\` ###
* The folder for static files called by the program (JavaScript, CSS, images, etc)
	* `bootstrap\`
	* `css\`
	* `img\`
	* `js\`

### `templates\` ###
	* `authn\`
	* `bookclub\`
	* `errors\`
	* `landing\`
	* `user\`

## Files ##

### `errors.py` ###
* Holds error rerouters for simple page errors
	* 404 : standard "Page Not Found" reroute
	* 401 : "Login Required" reroute
* Codes after return statements ensure code is returned with the page

### `forms.py` ###
* Uses `Flask-WTF` for convenience
* `SearchForm()`
	* For searching for books
	* Allows for form persistence for JavaScript search function to work
	* Allows for easy rerouting to search page

### `models.py` ###
* Holds models/loose schema for the database
* Uses `Flask-Login` and `Flask-Dance` for mixins for OAuth
* Uses Flask-SQLAlchemy for easy DB tie-in with closing on SQL calls
* `User()`
	* Uses email and first name for repeated login
	* Repr is for debugging
* `OAuth()`
	* Stores OAuth2 token details
* `load_user()`
	* Loads a specific user queried by the app's `login_manager` (from `Flask-Login`)

### `routes.py` ###
* Holds standard routes for the app
* All `user` and `bookclub` routes
	* Require login
	* Use `form.validate_on_submit()` to allow rerouting to the search page
	* Have `GET` and `POST` methods for submitting and receiving information
* `login()`
	* Lets user choose login page or automatically reroutes to the user page if already logged in
* `google_login()`
	* Reroutes the user to their user page if they are already logged in
	* If the user isn't authorized, reroute to the Google OAuth2 login
	* Attempts to get user information from login
	* If user (email account) already exists in database, login with information from database (create new user if not)
	* Catch token errors and try login again
	* Loads the landing page after everything passes
* `logout()`
	* Uses `Flask-Login` to logout the current user and return them to the landing page
