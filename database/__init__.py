import MySQLdb

class EmailDb:
  def __init__(self):
    self.host = 'localhost'
    self.user = 'root'
    self.passwd = '1998'
    self.db = 'gmail_ruler'
    self.conn = None

  def db_connect(self):
    try:
      self.conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db, use_unicode=True, charset="utf8")
      self.conn.names="utf8"
      cur = self.conn.cursor()
      return cur
    except:
      return None

  def store(self, sender, date, subject, message, message_id):
    cur = self.db_connect()
    if cur:
      sender = sender.split('<')
      sender = sender[len(sender)-1]
      email_id = sender[0:len(sender)-1]
      cur.execute("INSERT INTO mail(sender, date, subject, message, message_id) VALUES('{0}', '{1}', '{2}', '{3}', '{4}')".format(email_id, date[0:1000], subject[0:2000], message[0:6000], message_id))
      self.conn.commit()
    else:  
      raise ConnectionError()

  def get_content(self, email_id):
    cur = self.db_connect()
    if cur:
      result = cur.execute("SELECT date,subject FROM mail WHERE sender = '{0}'".format(email_id))
      if result == 0:
        return {
          "message" : "No such sender in your INBOX"
        }
      return(cur.fetchall())
    raise ConnectionError()

  def get_all_subject(self):
    cur = self.db_connect()
    if cur:
      cur.execute("SELECT subject FROM mail")
      return(cur.fetchall())
    raise ConnectionError()

  def get_email(self, subject):
    cur = self.db_connect()
    if cur:
      result = cur.execute("SELECT sender FROM mail WHERE subject = '{0}'".format(subject))
      return(cur.fetchone())
    raise ConnectionError()

  def get_all_content(self):
    cur = self.db_connect()
    if cur:
      result = cur.execute("SELECT sender,date,subject FROM mail")
      return(cur.fetchall())
    raise ConnectionError()

  def close(self):
    self.conn.close()
    