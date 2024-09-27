import psycopg2
from psycopg2 import sql

# define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    # commented out, so imma leave em that way
    # 'password': 'student',
    # 'host': 'localhost',
    # 'port': '5432'
}

try:
    # connect to postgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # version stuff
    cursor.execute("select version();")
    version = cursor.fetchone()
    print(f'Connected to - {version}')

    # executing queries
    cursor.execute('select * from players;')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as error:
    print(f'Error connecting to PostgreSQL database: {error}')

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()