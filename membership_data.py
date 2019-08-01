from membership_model import Membership
from group_model import Group

def save_membership(email, groupname): # Saves profile
    m = Membership(email=email, groupname=groupname)
    m.put()


def get_groups_from_member(email):
    groups = Membership.query(Membership.email == email).fetch()
    groupnames = []
    for group in groups:
        groupnames.append(group.groupname)
    return groupnames


def get_members_from_group(groupname):
    members = Membership.query(Membership.groupname == groupname).fetch()
    memberemails = []
    for member in members:
        memberemails.append(member.email)
    return memberemails


def delete_membership(email, groupname):
    m = Membership.query(Membership.groupname == groupname).fetch()
    for membership in m:
        if membership.email == email:
            membership.key.delete()

def delete_all_membership( groupname):
    m = Membership.query(Membership.groupname == groupname).fetch()
    for membership in m:
        membership.key.delete()
    g = Group.query(Group.name == groupname).fetch(1)
    for group in g:
        group.key.delete()
