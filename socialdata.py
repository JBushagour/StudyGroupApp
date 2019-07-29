from socialmodels import UserProfile


def save_profile(name, email, courses, school):
    p = get_user_profile(email)
    if p:
        p.name = name
        p.courses = courses
        p.school = school
    else:
        p = UserProfile(email=email, name=name, courses=courses, school=school)
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
