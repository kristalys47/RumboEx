import sendgrid
from sendgrid.helpers.mail import *
from RumboEx.config.sendgridcred import SENDGRID_API_KEY


class EmailHandler:

    def __init__(self):
        self.apikey = SENDGRID_API_KEY

    # Methods to send an email through sendgrid

    # An email is sent every time a user receives a new message

    def send_mail_after_message(self, m_id):
        from RumboEx.handler.MessageHandler import MessageHandler
        from RumboEx.dao.MessageDao import MessageDAO
        msg = MessageDAO().get_message_by_message_id(m_id)
        msg = MessageHandler().mapToLongMessageDict(msg)
        sg = sendgrid.SendGridAPIClient(apikey=self.apikey)
        from_email = Email(msg['sent_by_email'])
        # from_email = Email('irixa.vales@upr.edu')
        to_email = Email(msg['sent_to_email'])
        # to_email = Email('irixa.vales@upr.edu')
        subject = "My Study Coach: New message from %s" % (msg['sent_by_name'] + ' ' + msg['sent_by_lastname'])
        content = Content("text/plain", msg['text'])
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    # An email is sent after a successful registration

    def send_mail_after_register(self, user_id):
        from RumboEx.handler.UserHandler import UserHandler
        from RumboEx.dao.UserDao import UserDAO
        usr = UserDAO().getUser(user_id)
        usr = UserHandler().mapToUserDict(usr)
        sg = sendgrid.SendGridAPIClient(apikey=self.apikey)
        to_email = Email(usr['email'])
        subject = 'My Study Coach: New account'
        content = Content("text/plain",
                          "A new account was created for %s %s.\n\n\tusername: %s\n\tpassword: %s\n\nGo to mystudycoach.uprm.edu to use My Study Coach!" %
                          (usr['name'], usr['lastname'], usr['username'], usr['password']))
        mail = Mail(None, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response)
