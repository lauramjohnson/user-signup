import webapp2
import cgi


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

        self.response.write("Welcome " + ui_username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/created',NewUserHandler)

], debug=True)
