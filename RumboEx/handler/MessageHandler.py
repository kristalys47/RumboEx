from flask import jsonify
from RumboEx.dao.MessageDao import MessageDAO


class MessageHandler():

    def get_chats_by_user_id(self, user_id):
        dao = MessageDAO()
        chats = dao.get_chats_by_user_id(user_id)
        if not chats:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for c in chats:
            chat = {'chat_id': c[0], 'receipient': "%s %s" % (c[1], c[2])}
            chat['messages'] = []
            messages = dao.get_messages_by_chat_id(c[0])
            if messages:
                for m in messages:
                    chat['messages'].append(self.mapToMessageDict(m))
            mapped_result.append(chat)
        return jsonify(mapped_result)

    def mapToMessageDict(self, row):
        return {
            'm_id': row[0],
            'chat_id': row[1],
            'sent_by': row[2],
            'sent_to': row[3],
            'date': row[4],
            'text': row[5]
        }
