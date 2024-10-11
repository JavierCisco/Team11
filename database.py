import psycopg2
from psycopg2 import sql


################################################################################################################################################
# Establishing connection with database in VMachine
################################################################################################################################################

# define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
}

# declaring the vars here so that i can  keep them in the global scope
conn = None
cursor = None
	
# try block to make sure that it connects succesfully before proceeding
try:
    # connect to postgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()
except Exception as error:
    print(f'Error connecting to PostgreSQL database: {error}')
################################################################################################################################################



################################################################################################################################################
# Functions that perform queries using try-catch blocks to prevent errors from happening and protecting memory.
################################################################################################################################################

# executing queries functions
def view_database():
	try:
		cursor.execute("SELECT * FROM players;")
		rows = cursor.fetchall()
		for row in rows:
			print(row)
	except Exception as error:
		print(f'Error viewing the Database: {error}')

def insert_player(id, name):
	try:
		cursor.execute('''INSERT INTO players VALUES(%s, %s);''', (id, name))
		conn.commit()
	except Exception as error:
		print(f'Error inserting a player: {error}')

def remove_player(playerID):
	try:
		cursor.execute('''DELETE FROM players WHERE id = %s;''', [playerID])
		conn.commit()
	except Exception as error:
		print(f'Error removing a player: {error}')
################################################################################################################################################



################################################################################################################################################
# Function that closes the cursor and the connection
################################################################################################################################################

# cursor would close before being accessed in main, this fixed the bug, i call this in main function 'end_game()'
#	so it will for sure execute, as long as the game closes, so will this block execute
def bye_data():
	print('freeing up memory')
	if cursor:
		cursor.close()
	if conn:
		conn.close()
