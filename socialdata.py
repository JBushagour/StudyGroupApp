from socialmodels import UserProfile
from socialmodels import Group


def save_profile(name, email, courses, school, groups):
    p = get_user_profile(email)
    if p:
        p.name = name
        p.courses = courses
        p.school = school
        p.groups = groups
    else:
        p = UserProfile(email=email, name=name, courses=courses, school=school, groups=groups)
    p.put()


def get_user_profile(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_profile_by_name(name):
    q = UserProfile.query(UserProfile.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


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
