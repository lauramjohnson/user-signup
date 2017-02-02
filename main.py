import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>UserSignup</title>
    <style type="text/css">
        *{
            font-family:Verdana;
        }
        body{
            background-color:mistyrose;
        }
        table{
            border:1px solid salmon;
            background-color:lightgray;
        }
        .column1{
            width:150px;
            color:teal;
        }
        .column3{
            color:red;

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
        error_username = self.request.get("error_username")
        error_password = self.request.get("error_password")
        error_mismatch_password = self.request.get("error_mismatch_password")
        error_email = self.request.get("error_email")

        ui_username = self.request.get("username")
        ui_email = self.request.get("email")

        if ui_username != '':
            insert_username = "value=" + ui_username
        else:
            insert_username = ""

        if ui_email != '':
            insert_email = "value=" + ui_email
        else:
            insert_email = ""

        newuser_form = """
        <table>
        <form action= "/welcome" method="post">
        <tr>
            <td class="column1">
                <label>Username
            </td>
            <td class="column2">
                <input type="text" name="username" """ + cgi.escape(insert_username) + """>
            </td>
            <td class="column3">
                """ + error_username + """
            </td>
        </tr></label>

        <tr>
            <td class="column1">
                <label>Password
            </td>
            <td class="column2">
                <input type="password" name="password">
            </td>
            <td class="column3">
                """ + error_password + """
            </td>
        </tr></label>

        <tr>
            <td class="column1">
                <label>Verify Password
            </td>
            <td class="column2">
                <input type="password" name="ver_password">
            </td>
            <td class="column3">
                """ + error_mismatch_password + """
            </td>
        </tr></label>

        <tr>
            <td class="column1">
                <label>Email (optional)
            </td>
            <td class="column2">
                <input type="text" name="email" """+ cgi.escape(insert_email) +""">
            </td>
            <td class="column3">
                """ + error_email + """
            </td>
        </tr></label>

        </table>
        <br>
        <input type="submit" value="Create User"/>

        </form>
        """


        self.response.write(page_header + newuser_form + page_footer)

class NewUserHandler(webapp2.RequestHandler):
    def post(self):
        ori_username = self.request.get("username")
        ori_email = self.request.get("email")
        ui_username = cgi.escape(ori_username)
        ui_password = cgi.escape(self.request.get("password"))
        ui_verpassword = cgi.escape(self.request.get("ver_password"))
        ui_email = cgi.escape(ori_email)



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
            error_string = "/?"
            if error_username != '':
                error_string += "error_username=" + error_username + "&"
            if error_password != '':
                error_string += "error_password=" + error_password + "&"
            if error_mismatch_password != '':
                error_string += "error_mismatch_password=" + error_mismatch_password + "&"
            if error_email != '':
                error_string += "error_email=" + error_email + "&"
            error_string += "username=" + ori_username + "&email=" + ori_email

            self.redirect(error_string)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',NewUserHandler)

], debug=True)
