import os
import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
from UserProfile_model import UserProfile
from group_model import Group
from membership_model import Membership


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


class DeleteAllHandler(webapp2.RequestHandler): #Handles /pwtasfytn
    def get(self):
        p = UserProfile.query().fetch()
        for profile in p:
            profile.key.delete()
        g = Group.query().fetch()
        for group in g:
            group.key.delete()
        m = Membership.query().fetch()
        for membership in m:
            membership.key.delete()
