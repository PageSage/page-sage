import os
import tempfile
from flask import url_for

import unittest

from app import app


class BasicRouteTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["LOGIN_DISABLED"] = True
        
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    #########################
    ## Landing Page Routes ##
    #########################

    def test_landing_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_welcome_page(self):
        response = self.app.get('/welcome', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_terms_page(self):
        response = self.app.get('/terms', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_tos_page(self):
        response = self.app.get('/tos', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_terms_of_service(self):
        response = self.app.get('/terms-of-service', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_privacy(self):
        response = self.app.get('/privacy', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

  
    ##################
    ## AuthN Routes ##
    ##################

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_google_login(self):
        response = self.app.get('/google-login')
        self.assertEqual(response.status_code, 302)

    def test_facebook_login(self):
        response = self.app.get('/facebook-login')
        self.assertEqual(response.status_code, 302)

    #################
    ## User Routes ##
    #################

    def test_user_page(self):
        response = self.app.get('/user')
        self.assertEqual(response.status_code, 401)

    def test_profile_page(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 401)

    def test_user_book(self):
        response = self.app.get('/user/book')
        self.assertEqual(response.status_code, 401)

    def test_my_shelf(self):
        response = self.app.get('/my-shelf')
        self.assertEqual(response.status_code, 401)

    def test_user_search(self):
        response = self.app.get('/user/search')
        self.assertEqual(response.status_code, 401)

    def test_user_settings(self):
        response = self.app.get('user/settings')
        self.assertEqual(response.status_code, 401)


    #####################
    ## Bookclub Routes ##
    #####################

    def test_bookclub(self):
        response = self.app.get('/bookclub')
        self.assertEqual(response.status_code, 401)

    def test_club(self):
        response = self.app.get('/club')
        self.assertEqual(response.status_code, 401)

    def test_forums(self):
        response = self.app.get('/bookclub/forums')
        self.assertEqual(response.status_code, 401)

    def test_forum(self):
        response = self.app.get('/bookclub/forum')
        self.assertEqual(response.status_code, 401)

    def test_bookclub_shelf(self):
        response = self.app.get('/bookclub/shelf')
        self.assertEqual(response.status_code, 401)

    def test_bookclub_bookshelf(self):
        response = self.app.get('/bookclub/bookshelf')
        self.assertEqual(response.status_code, 401)

    def test_bookclub_suggestions(self):
        response = self.app.get('/bookclub/suggestions')
        self.assertEqual(response.status_code, 401)

    def test_bookclub_book(self):
        response = self.app.get('/bookclub/book')
        self.assertEqual(response.status_code, 401)

    def test_bookclub_settings(self):
        response = self.app.get('/bookclub/settings')
        self.assertEqual(response.status_code, 401)

    def test_bookclub_search(self):
        response = self.app.get('/bookclub/search')
        self.assertEqual(response.status_code, 401)


    #################
    ## Error Pages ##
    #################

    ## This test does not work currently--why 
    def test_404_page(self):
        response = self.app.get('/anything_should_go_here')
        self.assertEqual(response.status_code, 404)

    def test_401_page_user(self):
        response = self.app.get('/user')
        self.assertEqual(response.status_code, 401)

    def test_401_page_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
