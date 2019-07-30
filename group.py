import webapp2
import group_data
import socialdata
import helpers


class GroupCreateHandler(webapp2.RequestHandler):
    def get(self):
        if not helpers.get_user_email():
            self.redirect('/')
        else:
            values = helpers.get_template_parameters()
            profile = socialdata.get_user_profile(helpers.get_user_email())
            if profile:
                values['groups'] = profile.groups
            helpers.render_template(self, 'group-create.html', values)


class GroupEditHandler(webapp2.RequestHandler):
    def get(self):
        if not helpers.get_user_email():
            self.redirect('/')
        else:
            values = helpers.get_template_parameters()
            group = group_data.get_group_by_admin(helpers.get_user_email())
            if group:
                values['name'] = group.name
                values['course'] = group.course
                values['description'] = group.description
                if group.member_limit:
                    values['member_limit'] = group.member_limit
                else:
                    values['member_limit'] = 5
            helpers.render_template(self, 'group-edit.html', values)


class GroupSaveHandler(webapp2.RequestHandler):
    def post(self):
        profile = socialdata.get_user_profile(helpers.get_user_email())
        if not profile:
            print("Fcgwogwouaougwuogwaguowagouawguoawguogouwagouwaougwaugoaw")
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get("name")
            course = self.request.get("course")
            description = self.request.get("description")
            member_limit = self.request.get("member_limit")
            members = []
            members.append(helpers.get_user_email())
            group_admin = helpers.get_user_email()
            school = profile.school
            groups = socialdata.get_profile_groups(helpers.get_user_email())
            groups.append(name)
            socialdata.save_profile(profile.name, profile.email, profile.courses, profile.school, groups)
            values = helpers.get_template_parameters()
            name.strip()
            name.replace(" ", "&")
            if len(name) > 20:
                error_text += "Your name can't be more than 20 letters\n"
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
            values['course'] = course
            values['description'] = description
            values['member_limit'] = member_limit
            if error_text:
                values['errormsg'] = error_text
            else:
                group_data.save_group(name, description, course, int(member_limit), members, group_admin, school)
                values['successmsg'] = "Everything worked out fine."
            helpers.render_template(self, 'group-edit.html', values)


class GroupViewHandler(webapp2.RequestHandler):
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
