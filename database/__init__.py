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
      cur = self.conn.cursor()
      return cur
    except:
      return None

  def store(self, sender, date, subject, message):
    cur = self.db_connect()
    if cur:
      sender = sender.split('<')
      sender = sender[len(sender)-1]
      email_id = sender[0:len(sender)-1]
      cur.execute("INSERT INTO email_details(sender, date, subject, message) VALUES('{0}', '{1}', '{2}', '{3}')".format(email_id, date[0:1000], subject[0:2000], message[0:6000]))
      self.conn.commit()
    else:  
      raise ConnectionError()

  def email_exist(self, email_id):
    cur = self.db_connect()
    if cur:
      result = cur.execute("SELECT * FROM email_details WHERE sender = '{0}'".format(email_id))
      if result == 0:
        return False
      return True
    raise ConnectionError()

  def get_details(self, email_id):
    cur = self.db_connect()
    if cur:
      cur.execute("SELECT * FROM email_details WHERE sender = '{0}'".format(email_id))
      return(cur.fetchall())
    raise ConnectionError() 

  def close(self):
    self.conn.close()
    