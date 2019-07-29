from google.appengine.ext import ndb


class UserProfile(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    courses = ndb.StringProperty(repeated=True)
    school = ndb.StringProperty(required=True)
    groups = ndb.StringProperty(repeated=True)


class Group(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    course = ndb.StringProperty(required=True)
    member_limit = ndb.IntegerProperty()
    members = ndb.StringProperty(repeated=True)
    group_admin = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
