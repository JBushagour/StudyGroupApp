import os
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
    