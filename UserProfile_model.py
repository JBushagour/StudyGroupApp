from google.appengine.ext import ndb


class UserProfile(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    courses = ndb.StringProperty(repeated=True)
    school = ndb.StringProperty(required=True)
