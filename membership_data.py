from membership_model import Membership

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
