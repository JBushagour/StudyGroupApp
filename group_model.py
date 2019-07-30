from google.appengine.ext import ndb


class Group(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    course = ndb.StringProperty(required=True)
    member_limit = ndb.IntegerProperty()
    members = ndb.StringProperty(repeated=True)
    group_admin = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
