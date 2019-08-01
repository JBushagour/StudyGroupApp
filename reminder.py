import webapp2
import socialdata
import helpers
from UserProfile_model import UserProfile
import mail

class RequestReminderHandler(webapp2.RequestHandler):
    def get(self):
        from_address= "admin@studigroup.appspot.com"
        email = helpers.get_user_email()
        subject = "Reminder"
        body = "You have a study group meeting at " 
        mail.send_mail(from_address, email, body, subject)
