from group_model import Group


def save_group(name, description, course, member_limit, group_admin, school): #this function saves the group
    p = get_group_by_name(name)
    if p: #if it exists, we update the group
        p.name = name
        p.description = description
        p.course = course
        p.member_limit = member_limit
        p.group_admin = group_admin
        p.school = school
    else: #otherwise we create a new group 
        p = Group(
            name=name, description=description, course=course,
            member_limit=member_limit, group_admin=group_admin,
            school=school
            )
    p.put()


def get_group_by_name(name): # simple function to return group object given name
    q = Group.query(Group.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_group_by_admin(email): # simple function to return group object given admin email
    q = Group.query(Group.group_admin == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_groups_by_courses(courseList): # simple function to return group object given admin email
    listOfGroups = []
    for course in courseList:
        results = Group.query(Group.course == course).fetch()
        for group in results:
            listOfGroups.append(group)
    return listOfGroups
