import webapp2
import group_data
import socialdata
import helpers
import membership_data


class GroupCreateHandler(webapp2.RequestHandler): #Handles /group-create
    def get(self):
        profile = socialdata.get_user_profile(helpers.get_user_email())
        if not profile: #if the user does not have a profile, go to home
            self.redirect('/')
        else: #otherwise, allow them to create group
            values = helpers.get_template_parameters()
            values['name'] = profile.name
            groups = group_data.get_admin_groups(profile.email)
            groupNames = []
            for group in groups:
                groupNames.append(group.name)
            values["groups"] = groupNames
            helpers.render_template(self, 'group-create.html', values) #show group creation page


class GroupEditHandler(webapp2.RequestHandler): #Handles /group-edit
    def get(self):
        profile = socialdata.get_user_profile(helpers.get_user_email())
        if not profile: #at this point, they should have a profile. If they don't, kick 'em
            self.redirect('/')
        else:
            values = helpers.get_template_parameters()
            values['courses'] = profile.courses
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
            member_limit = self.request.get("quantity") #lines 35 - 42 set default values in group
            group_admin = helpers.get_user_email()
            school = profile.school
            values = helpers.get_template_parameters()
            group_name.strip() #lines 49- 57 are name nonos
            group_name.replace(" ", "&")
            if (len(group_name) < 1) or (len(course) < 1) or (len(description) < 1) or (len(member_limit) < 1):
                error_text += "Make sure all fields are filled"
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
            values['courses'] = profile.courses
            values['description'] = description
            values['member_limit'] = member_limit
            values['name'] = profile.name
            if group_data.get_group_by_name(group_name):
                error_text += "This group name is already taken"
            if error_text: #print error text if there's a problem
                values['errormsg'] = error_text
            else:
                membership_data.save_membership(helpers.get_user_email(), group_name)
                group_data.save_group(group_name, description, course, int(member_limit), group_admin, school) #print success message if no problem saving
                values['successmsg'] = "Everything worked out fine."
            helpers.render_template(self, 'group-edit.html', values) #go back to edit render


class GroupViewHandler(webapp2.RequestHandler):  #Handles /group-view, CURRENTLY NONFUNCTIONAL
    def get(self, groupname):
        group = group_data.get_group_by_name(groupname)
        values = helpers.get_template_parameters()
        values['groupname'] = 'Unknown'
        values['course'] = "no course"
        values['school'] = "no school"
        values['description'] = "no description"
        values['admin'] = "unknown admin"
        values["members"] = "unkown members"
        profile = socialdata.get_user_profile(helpers.get_user_email())
        values['name'] = profile.name
        if group:
            values['groupname'] = group.name
            values['course'] = group.course
            values['school'] = group.school
            values['description'] = group.description
            values['admin'] = group.group_admin
            values["members"] = membership_data.get_members_from_group(groupname)
            helpers.render_template(self, 'group-view.html', values)


class GroupListHandler(webapp2.RequestHandler): #Handles /group-list
    def get(self):
        profile = socialdata.get_user_profile(helpers.get_user_email())
        if not profile: #if the user does not have a profile, go to home
            self.redirect('/')
        else: #otherwise, allow them to create group
            errorText = ''
            values = helpers.get_template_parameters()
            groups = group_data.get_groups_by_courses(profile.courses)
            listOfGroupNames = []
            for group in groups:
                membersList = membership_data.get_members_from_group(group.name)
                if ((group.member_limit) - len(membersList) + 1) < 1:
                    errorText += "The member limit has been reached"
                elif profile.email in membersList:
                    errorText += "You are already in this group"
                else:
                    listOfGroupNames.append(group.name)
            values['name'] = profile.name
            values['groups'] = listOfGroupNames
            helpers.render_template(self, 'group-list.html', values) #show group creation page


class GroupJoinHandler(webapp2.RequestHandler): #Handles /group-join
    def get(self, groupname):
        profile = socialdata.get_user_profile(helpers.get_user_email())
        if not profile: #if the user does not have a profile, go to home
            self.redirect('/')
        else: #otherwise, allow them to create group
            errorText = ""
            values = helpers.get_template_parameters()
            groups = group_data.get_groups_by_courses(profile.courses)
            listOfGroupNames = []
            membersList = membership_data.get_members_from_group(groupname)
            for group in groups:
                if ((group.member_limit) - len(membersList) + 1) < 1:
                    errorText += "The member limit has been reached"
                elif profile.email in membersList:
                    errorText += "You are already in this group"
                else:
                    listOfGroupNames.append(group.name)
            values['name'] = profile.name
            values['groups'] = listOfGroupNames
            if errorText:
                values['errormsg'] = errorText
            else:
                membership_data.save_membership(helpers.get_user_email(), groupname)
                values['successmsg'] = "Everything worked out fine."
                self.redirect("/group-list")
            helpers.render_template(self, 'group-list.html', values) #show group creation page
