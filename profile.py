import webapp2
import socialdata
import helpers


class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not helpers.get_user_email():
            self.redirect('/')
        else:
            values = helpers.get_template_parameters()
            profile = socialdata.get_user_profile(helpers.get_user_email())
            if profile:
                values['name'] = profile.name
                values['school'] = profile.school
                values['courses'] = profile.courses
            helpers.render_template(self, 'profile-edit.html', values)


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = helpers.get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get("name")
            school = self.request.get("school")
            values = helpers.get_template_parameters()
            name.strip()
            name.replace(" ", "&")
            if len(name) > 60:
                error_text += "Your name can't be more than 60 letters\n"
            for i in name:
                if i == '?':
                    error_text += "Your name can't have ' ? '\n"
                elif i == '\\':
                    error_text += "Your name can't have ' \\ '\n"
                elif i == '/':
                    error_text += "Your name can't have ' / '\n"
                elif i == '.':
                    error_text += "Your name can't have ' . '\n"
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
            helpers.render_template(self, 'profile-edit.html', values)


class ProfileViewHandler(webapp2.RequestHandler):
    def get(self, profilename):
        profile = socialdata.get_profile_by_name(profilename)
        values = helpers.get_template_parameters()
        values['name'] = 'Unknown'
        values['courses'] = "courses does not exist"
        values['school'] = "school does not exist"
        if profile:
            values['name'] = profile.name
            values['courses'] = profile.courses
            values['school'] = profile.school
        helpers.render_template(self, 'profile-view.html', values)
