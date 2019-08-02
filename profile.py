import webapp2
import socialdata
import helpers
import membership_data


class ProfileEditHandler(webapp2.RequestHandler): #Handles /profile-edit
    def get(self):
        if not helpers.get_user_email(): # if they don't have an email, we kick em
            self.redirect('/')
        else:
            values = helpers.get_template_parameters()
            profile = socialdata.get_user_profile(helpers.get_user_email())
            if profile:  # if they do have a profile, we populate it with default values
                values['name'] = profile.name
                values['school'] = profile.school
                values['courses'] = profile.courses
            helpers.render_template(self, 'profile-edit.html', values)  # shows the profile-edit page


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = helpers.get_user_email()
        if not email:  # if they don't have an email, we kick em
            self.redirect('/')
        else:
            error_text = ''  # intialize an empty error text
            name = self.request.get("name")  # gets values from form
            school = self.request.get("school") 
            values = helpers.get_template_parameters()
            name.strip()
            name.replace(" ", "&")
            # Restricts the name choices for the user
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
            coursesList = []  # code for showing repeated courses
            coursenum = 0
            course = self.request.get("classes0")
            while course:
                coursesList.append(course)
                coursenum += 1
                course = self.request.get("classes" + str(coursenum))
            values['courses'] = coursesList
            values['school'] = school
            if error_text:
                values['errormsg'] = error_text
            else:
                socialdata.save_profile(name, email, coursesList, school)  # save profile if everything is fine
                values['successmsg'] = "Success!"
            helpers.render_template(self, 'profile-edit.html', values) #show page


class ProfileViewHandler(webapp2.RequestHandler):  #handles profile-view
    def get(self, profilename):
        profile = socialdata.get_profile_by_name(profilename) #gets the profile
        values = helpers.get_template_parameters()
        values['name'] = 'Unknown' #if the profile doens't exist we popoulate the spaces with defaults
        values['courses'] = ["courses does not exist"]
        values['school'] = "school does not exist"
        values["groups"] = ["Groups do not exist"]
        if profile:  # if we have a profile, populate the spaces with correct info
            values['name'] = profile.name
            values['courses'] = profile.courses
            values['school'] = profile.school
            values["groups"] = membership_data.get_groups_from_member(profile.email)
        helpers.render_template(self, 'profile-view.html', values) #show page
