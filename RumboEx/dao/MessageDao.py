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
        query = 'select UC.chat_id, u.id, u.username, u.name, u.lastname, u.email ' \
                'from "user" as u inner join ' \
                '(select U1.chat_id, U2.user_id ' \
                'from user_chat as U1 ' \
                'inner join user_chat as U2 on U1.chat_id=U2.chat_id ' \
                'and U1.user_id = %s and not U1.user_id = U2.user_id) as UC ' \
                'on UC.user_id = u.id ' \
                'inner join ' \
                '(select max(date) as date, chat_id from message group by chat_id) as M on M.chat_id=UC.chat_id ' \
                'order by M.date desc;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_messages_by_chat_id(self, chat_id):
        cursor = self.conn.cursor()
        query = 'select m_id, sent_by, sent_to, date, text, seen from message where chat_id = %s order by date, m_id;'
        cursor.execute(query, (chat_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_message_by_message_id(self, m_id):
        cursor = self.conn.cursor()
        query = 'select m_id, date, text, seen, ' \
                'sent_by as sent_by_id, S.username as sent_by_username, S.name as sent_by_name, S.lastname as sent_by_lastname, S.email as sent_by_email, ' \
                'sent_to as sent_to_id, R.username as sent_to_username, R.name as sent_to_name, R.lastname as sent_to_lastname, R.email as sent_to_email ' \
                'from message ' \
                'inner join "user" as S on S.id=sent_by ' \
                'inner join "user" as R on R.id=sent_to ' \
                'where m_id=%s;'
        cursor.execute(query, (m_id,))
        return cursor.fetchone()

    # POST Methods

    def insert_message(self, sent_by, sent_to, date, text, seen):
        cursor = self.conn.cursor()
        query = 'select chat_id ' \
                'from user_chat as C1 inner join user_chat as C2 using(chat_id) ' \
                'where C1.user_id=%s and C2.user_id=%s and not C1.user_id=C2.user_id;'
        cursor.execute(query, (sent_by, sent_to,))
        chat_id = cursor.fetchone()[0]
        if not chat_id:
            chat_id = self.insert_chat(sent_by, sent_to)
        query2 = 'insert into message (chat_id, sent_by, sent_to, date, text, seen) ' \
                 'values (%s,%s,%s,%s,%s,%s) returning m_id;'
        cursor.execute(query2, (chat_id, sent_by, sent_to, date, text, seen,))
        m_id = cursor.fetchone()[0]
        self.conn.commit()
        return m_id

    def insert_chat(self, user1, user2):
        cursor = self.conn.cursor()
        query = 'insert into chat default values returning chat_id;'
        cursor.execute(query,)
        chat_id = cursor.fetchone()[0]
        query1 = 'insert into user_chat(chat_id, user_id) values (%s, %s);'
        cursor.execute(query1, (chat_id, user1,))
        cursor.execute(query1, (chat_id, user2,))
        self.conn.commit()
        return chat_id