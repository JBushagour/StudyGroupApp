from google.appengine.ext import ndb


class Membership(ndb.Model):
    email = ndb.StringProperty(required=True)
    groupname = ndb.StringProperty(required=True)
