from UserProfile_model import UserProfile


def save_profile(name, email, courses, school): # Saves profile
    p = get_user_profile(email) #gets the user profile
    if p: #if it exists we update it
        p.name = name
        p.courses = courses
        p.school = school
    else: #if it doens't we create it
        p = UserProfile(email=email, name=name, courses=courses, school=school)
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
    