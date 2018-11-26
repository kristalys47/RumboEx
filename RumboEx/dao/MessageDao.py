from RumboEx.config.dbconfig import pg_config
import psycopg2


class MessageDAO:
    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    # GET Methods

    def get_chats_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = 'select UC.chat_id, u.name as receipient_name, u.lastname as reciepient_lastname ' \
                'from "user" as u inner join ' \
                '(select U1.chat_id, U2.user_id from user_chat as U1 inner join user_chat as U2 on U1.chat_id=U2.chat_id ' \
                'and U1.user_id = %s and not U1.user_id = U2.user_id) as UC ' \
                'on UC.user_id = u.id;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_messages_by_chat_id(self, chat_id):
        cursor = self.conn.cursor()
        query = 'select * from message where chat_id = %s order by date desc, m_id desc;'
        cursor.execute(query, (chat_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result
