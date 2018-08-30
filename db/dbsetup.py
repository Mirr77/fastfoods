import psycopg2


def connect_db():
  '''Connect to main app database'''

  db_details = "dbname='fastfoods' user='postgres' host='localhost' password='password'"
  try:
      return psycopg2.connect(db_details)

  except:
      print ("Unable to establish connection to database")


def open_connection():
    """ Open connection to execute queries """
    conn = connect_db()
    return conn


