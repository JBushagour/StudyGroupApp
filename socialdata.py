from UserProfile_model import UserProfile


def save_profile(name, email, courses, school, groups): # Saves profile
    p = get_user_profile(email) #gets the user profile
    if p: #if it exists we update it
        p.name = name
        p.courses = courses
        p.school = school
        if groups != "NOCHANGE": #don't change groups if it has "NOCHANGE"
            p.groups = groups
    else: #if it doens't we create it
        if groups == "NOCHANGE": #if we create with a "mochange", then we must add an empty bracket
            groups = []
        p = UserProfile(email=email, name=name, courses=courses, school=school, groups=groups)
    p.put()


def get_user_profile(email):  # gets user profile from email
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_profile_by_name(name): # gets user profile from name
    q = UserProfile.query(UserProfile.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_profile_groups(email):  # gets the groups in a profile
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile.groups