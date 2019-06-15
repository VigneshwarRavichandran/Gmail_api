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

  def store(self, message_id, sender, date, subject):
    cur = self.db_connect()
    if cur:
      cur.execute("INSERT INTO mail(sender, date, subject, message_id) VALUES('{0}', '{1}', '{2}', '{3}')".format(sender, date, subject[0:2000], message_id))
      self.conn.commit()
    else:  
      raise ConnectionError()

  def contain_any(self, sender, date, subject):
    cur = self.db_connect()
    if cur:
      cur.execute("SELECT message_id FROM mail WHERE date >= '{0}' or sender = '{1}' or subject LIKE '%{2}%'".format(date, sender, subject))
      return(cur.fetchall())
    raise ConnectionError()

  def contain_all(self, sender, date, subject):
    cur = self.db_connect()
    if cur:
      cur.execute("SELECT message_id FROM mail WHERE date >= '{0}' and sender = '{1}' and subject LIKE '%{2}%'".format(date, sender, subject))
      return(cur.fetchall())
    raise ConnectionError()

  def close(self):
    self.conn.close()
    