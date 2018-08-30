from db.dbsetup import open_connection

QUERIES = [
  """
  CREATE TABLE IF NOT EXISTS users(
          user_id SERIAL PRIMARY KEY NOT NULL,
          username VARCHAR NOT NULL,
          email VARCHAR NOT NULL,
          password VARCHAR NOT NULL,
          role INT NOT NULL,
          orders VARCHAR[] NOT NULL default '{}'
          )
  """,

  """
  CREATE TABLE IF NOT EXISTS orders(
          order_id SERIAL PRIMARY KEY NOT NULL,
          question_desc VARCHAR NOT NULL,
          user_id INT REFERENCES users(user_id))""",

"""
  CREATE TABLE IF NOT EXISTS menu(
          entry_id SERIAL PRIMARY KEY NOT NULL,
          item VARCHAR NOT NULL,
          cost INT NOT NULL)"""
]


def create_db():
    """ Create the db"""
    conn = open_connection()
    cur = conn.cursor()

    for query in QUERIES:
        cur.execute(query)
