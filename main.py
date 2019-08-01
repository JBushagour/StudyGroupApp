import socialdata
import webapp2
import profile
import helpers
import group


class MainHandler(webapp2.RequestHandler): #handles the main page
    def get(self):
        values = helpers.get_template_parameters()
        if helpers.get_user_email(): #checks to see if signed in
            profile = socialdata.get_user_profile(helpers.get_user_email())
            if profile: #if the profile exists, we can click on profile-view
                values['name'] = profile.name
        helpers.render_template(self, 'mainpage.html', values)  # shows page


app = webapp2.WSGIApplication([
    ('/p/(.*)', profile.ProfileViewHandler),
    ('/g/join/(.*)', group.GroupJoinHandler),
    ('/g/delete/(.*)', group.GroupDeleteHandler),
    ('/g/leave/(.*)', group.GroupLeaveHandler),
    ('/g/(.*)', group.GroupViewHandler),
    ("/profile-edit", profile.ProfileEditHandler),
    ("/profile-save", profile.ProfileSaveHandler),
    ("/group-create", group.GroupCreateHandler),
    ("/group-edit", group.GroupEditHandler),
    ("/group-save", group.GroupSaveHandler),
    ("/group-list", group.GroupListHandler),
    ("/pwtasfytn", helpers.DeleteAllHandler),
    ('.*', MainHandler)
])
