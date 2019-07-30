from group_model import Group


def save_group(name, description, courses, member_limit, members, group_admin, school):
    p = get_group_by_name(name)
    if p:
        p.name = name
        p.description = description
        p.courses = courses
        p.member_limit = member_limit
        p.members = members
        p.group_admin = group_admin
        p.school = school
    else:
        p = Group(
            name=name, description=description, courses=courses,
            member_limit=member_limit, members=members, group_admin=group_admin,
            school=school
            )
    p.put()


def get_group_by_name(name):
    q = Group.query(Group.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None
