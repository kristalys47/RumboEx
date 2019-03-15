from flask import jsonify
from RumboEx.dao.MessageDao import MessageDAO


class MessageHandler:

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
