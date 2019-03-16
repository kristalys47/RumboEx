from flask import jsonify
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
                return jsonify({'msg_id': m_id}), 200
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

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
