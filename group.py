import webapp2
import group_data
import socialdata
import helpers


class GroupCreateHandler(webapp2.RequestHandler): #Handles /group-create
    def get(self):
        profile = socialdata.get_user_profile(helpers.get_user_email())
        if not profile: #if the user does not have a profile, go to home
            self.redirect('/')
        else: #otherwise, allow them to create group
            values = helpers.get_template_parameters()
            values['name'] = profile.name
            values['groups'] = profile.groups 
            helpers.render_template(self, 'group-create.html', values) #show group creation page


class GroupEditHandler(webapp2.RequestHandler): #Handles /group-edit
    def get(self):
        if not helpers.get_user_email(): #at this point, they should have an email. If they don't, kick 'em
            self.redirect('/')
        else:
            values = helpers.get_template_parameters()
            helpers.render_template(self, 'group-edit.html', values) #the page is rendered


class GroupSaveHandler(webapp2.RequestHandler):  #Handles /group-save
    def post(self):
        profile = socialdata.get_user_profile(helpers.get_user_email()) #we get a profile
        if not profile: #if the profile doesn't exist, we kick them out
            self.redirect('/')
        else:
            error_text = '' #initializes an empty error
            group_name = self.request.get("group_name")
            course = self.request.get("course")
            description = self.request.get("description")
            member_limit = self.request.get("member_limit") #lines 35 - 42 set default values in group
            members = []
            members.append(helpers.get_user_email())
            group_admin = helpers.get_user_email()
            school = profile.school
            groups = socialdata.get_profile_groups(helpers.get_user_email()) #we get a list of the users previous groups
            groups.append(group_name) #we add this group on to it
            socialdata.save_profile(profile.name, profile.email, profile.courses, profile.school, groups) #save the profile with the change to the groups
            values = helpers.get_template_parameters()
            group_name.strip() #lines 47- 59 are name nonos
            group_name.replace(" ", "&")
            if len(group_name) > 20:
                error_text += "Your name can't be more than 20 letters\n"
            for i in group_name:
                if i == '?':
                    error_text += "Your name can't have ' ? '\n"
                elif i == '\\':
                    error_text += "Your name can't have ' \\ '\n"
                elif i == '/':
                    error_text += "Your name can't have ' / '\n"
                elif i == '.':
                    error_text += "Your name can't have ' . '\n"
            values['group_name'] = group_name #set template values
            values['course'] = course
            values['description'] = description
            values['member_limit'] = member_limit
            values['name'] = profile.name
            if error_text: #print error text if there's a problem
                values['errormsg'] = error_text
            else:
                group_data.save_group(group_name, description, course, int(member_limit), members, group_admin, school) #print success message if no problem saving
                values['successmsg'] = "Everything worked out fine."
            helpers.render_template(self, 'group-edit.html', values) #go back to edit render


class GroupViewHandler(webapp2.RequestHandler):  #Handles /group-view, CURRENTLY NONFUNCTIONAL
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