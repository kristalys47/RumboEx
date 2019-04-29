from flask import jsonify
from RumboEx.handler.emails import EmailHandler
from RumboEx.dao.MessageDao import MessageDAO


class MessageHandler:

    # GET Methods

    def get_chats_by_user_id(self, user_id):
        dao = MessageDAO()
        chats = dao.get_chats_by_user_id(user_id)
        if not chats:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for c in chats:
            chat = self.mapToChatDict(c)
            chat['messages'] = []
            messages = dao.get_messages_by_chat_id(chat['chat_id'])
            if messages:
                for m in messages:
                    chat['messages'].append(self.mapToMessageDict(m))
            mapped_result.append(chat)
        return jsonify(Chats=mapped_result)

    # Post Methods

    def insert_message(self, form):
        if len(form) is not 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            sent_by = form['sent_by']
            sent_to = form['sent_to']
            date = form['date']
            text = form['text']
            seen = form['seen']
            if sent_by and sent_to and date and text:
                dao = MessageDAO()
                m_id = dao.insert_message(sent_by, sent_to, date, text, seen)
                # result = self.mapToTaskDict(task_id)
                # todo: fix this method
                # EmailHandler().send_mail_after_message(m_id)
                return jsonify({'msg_id': m_id}), 200
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    # Method to send an email through sendgrid
    # An email is sent every time a user receives a new message

    # def send_mail(self, m_id):
    #     dao = MessageDAO()
    #     msg = dao.get_message_by_message_id(m_id)
    #     msg = self.mapToLongMessageDict(msg)
    #     sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    #     # from_email = Email(msg['sent_by_email'])
    #     from_email = Email('irixa.vales@upr.edu')
    #     # to_email = Email(msg['sent_to_email'])
    #     to_email = Email('irixa.vales@upr.edu')
    #     subject = "My Study Coach: New message from %s" % (msg['sent_by_name'] + ' ' + msg['sent_by_lastname'])
    #     content = Content("text/plain", msg['text'])
    #     mail = Mail(from_email, subject, to_email, content)
    #     response = sg.client.mail.send.post(request_body=mail.get())
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)

    # Map to Dictionaries

    def mapToChatDict(self, row):
        return {
            'chat_id': row[0],
            'contact': {
                'user_id': row[1],
                'username': row[2],
                'name': row[3],
                'lastname': row[4],
                'email': row[5]
            }
        }

    def mapToMessageDict(self, row):
        return {
            'm_id': row[0],
            'sent_by': row[1],
            'sent_to': row[2],
            'date': row[3],
            'text': row[4],
            'seen': row[5]
        }

    def mapToLongMessageDict(self, row):
        return {
            'm_id': row[0], 'date': row[1], 'text': row[2], 'seen': row[3],
            'sent_by_id': row[4], 'sent_by_username': row[5], 'sent_by_name': row[6], 'sent_by_lastname': row[7], 'sent_by_email': row[8],
            'sent_to_id': row[9], 'sent_to_username': row[10], 'sent_to_name': row[11], 'sent_to_lastname': row[12], 'sent_to_email': row[13],
        }
