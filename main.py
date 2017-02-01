import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>UserSignup</title>
    <style type="text/css">
        label{
            color:teal;
        }
    </style>
</head>
<body>
    <h1>
        User Signup
    </h1>
"""

page_footer = """
</body>
</html>
"""
class MainHandler(webapp2.RequestHandler):
    def get(self):
        newuser_form = """
        <form action= "/created" method="post">
        <label>
            Username
            <input type="text" name="username"/>
        </label>
        <br>
        <label>
            Password
            <input type="password" name="password"/>
        </label>
        <br>
        <label>
            Verify Password
            <input type="password" name="ver_password"/>
        </label>
        <br>
        <label>
            Email (optional)
            <input type="text" name="email"/>
        </label>
        <br>
        <input type="submit" value="Create User"/>

        </form>
        """


        self.response.write(page_header + newuser_form + page_footer)

class NewUserHandler(webapp2.RequestHandler):
    def post(self):
        ui_username = self.request.get("username")
        ui_password = self.request.get("password")
        ui_verpassword = self.request.get("ver_password")
        ui_email = self.request.get("email")

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        def valid_username(username):
            return USER_RE.match(username)

        def valid_password(password):
            return PASSWORD_RE.match(password)

        def valid_email(email):
            return EMAIL_RE.match(email)

        error_count = 0


        error_username = ''
        error_password = ''
        error_mismatch_password = ''
        error_email = ''

        if not ui_username:
            error_username ="You must enter a username"
            error_count += 1
        elif not valid_username(ui_username):
            error_count += 1
            error_username = "That is not a valid username"

        if not ui_password:
            error_password = "You must enter a password"
            error_count += 1
        elif not valid_password(ui_password):
            error_count += 1
            error_password = "You must enter a valid password"

        if ui_password != ui_verpassword:
            error_count += 1
            error_mismatch_password = "Your passwords must match"

        if ui_email and not valid_email(ui_email):
            error_count += 1
            error_email = "Your email address is invalid"

        if error_count == 0:
            self.response.write("Welcome " + ui_username)
        else:
            self.response.write(error_username + "<br>" +error_password + "<br>"+error_mismatch_password + "<br>"+error_email)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/created',NewUserHandler)

], debug=True)
