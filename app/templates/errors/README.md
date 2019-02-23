# Error Pages #

The files here are for HTML/Jinja2 templates relating to error pages.


## `401.html` ##
* This file acts as a landing page for the 401 error which occurs when a user tries to login to a page requiring a login
	* Allows rerouting to `choose-login.html` and the welcome page

## `404.html` ##
* This file acts as a ladning page for the 404 error which occurs when a user tries to navigate to a page that does not exist
	* Allows rerouting to the welcome page
