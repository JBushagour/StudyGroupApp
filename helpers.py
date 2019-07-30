import os
from google.appengine.api import users
from google.appengine.ext.webapp import template


def render_template(handler, file_name, template_values):  # this is code written by a mythical man and we musn't touch it
    path = os.path.join(os.path.dirname(__file__), 'templates/' + file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():  # gets user's current email
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None


def get_template_parameters():  # get's login or logout url
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values
