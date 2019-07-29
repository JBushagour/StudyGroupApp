import os
import socialdata
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values


class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        if get_user_email():
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
        render_template(self, 'mainpage.html', values)


class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
                values['school'] = profile.school
                values['courses'] = profile.courses
            render_template(self, 'profile-edit.html', values)


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get("name")
            courses = self.request.get("courses")
            school = self.request.get("school")
            values = get_template_parameters()
            name.strip()
            name.replace(" ","&")
            values['name'] = name
            coursesList = []
            coursenum = 0
            course = self.request.get("classes0")
            while course:
                coursesList.append(course)
                coursenum += 1
                course = self.request.get("classes" + str(coursenum))
            values['courses'] = coursesList
            values['school'] = school
            groups = ["hello", "heirhooh"]
            if error_text:
                values['errormsg'] = error_text
            else:
                socialdata.save_profile(name, email, coursesList, school, groups)
                values['successmsg'] = "Everything worked out fine."
            render_template(self, 'profile-edit.html', values)


class ProfileViewHandler(webapp2.RequestHandler):
    def get(self, profilename):
        profile = socialdata.get_profile_by_name(profilename)
        values = get_template_parameters()
        values['name'] = 'Unknown'
        values['courses'] = "courses does not exist"
        values['school'] = "school does not exist"
        if profile:
            values['name'] = profile.name
            values['courses'] = profile.courses
            values['school'] = profile.school
        render_template(self, 'profile-view.html', values)


app = webapp2.WSGIApplication([
    ('/p/(.*)', ProfileViewHandler),
    ("/profile-edit", ProfileEditHandler),
    ("/profile-save", ProfileSaveHandler),
    ('.*', MainHandler)
])