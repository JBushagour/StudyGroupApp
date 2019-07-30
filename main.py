import socialdata
import webapp2
import profile
import helpers


class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = helpers.get_template_parameters()
        if helpers.get_user_email():
            profile = socialdata.get_user_profile(helpers.get_user_email())
            if profile:
                values['name'] = profile.name
        helpers.render_template(self, 'mainpage.html', values)


app = webapp2.WSGIApplication([
    ('/p/(.*)', profile.ProfileViewHandler),
    ("/profile-edit", profile.ProfileEditHandler),
    ("/profile-save", profile.ProfileSaveHandler),
    ('.*', MainHandler)
])
