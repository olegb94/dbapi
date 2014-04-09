import MySQLdb

class Database(object):
	number = None
	connections = []
	availiable = []

	def __init__(self, number):
		self.number = number
		for i in range(number):
			self.connections.append(self.connect())
			self.availiable.append(True)

	def get_connection(self):
		while(True):
			for i in range(self.number):
				if self.availiable[i]:
					self.availiable[i] = False
					return i

	def return_connection(self, i):
		self.availiable[i] = True

	def connect(self):
		conn = MySQLdb.connect(
			host = "localhost",
			user = "login",
			passwd = "password",
			db = "api_db",
		)
		conn.set_character_set('utf8')
		return conn

	def get_cursor(self, connection):
		c = connection.cursor(MySQLdb.cursors.DictCursor)
		c.execute('SET NAMES utf8;')
		c.execute('SET CHARACTER SET utf8;')
		c.execute('SET character_set_connection=utf8;')
		return c

	def query(self, sql, param=[]):
		i = self.get_connection()
		connection = self.connections[i]
		try:
			connection.ping()
		except:
			connection = self.connect()
		finally:
			cursor = self.get_cursor(connection)
			connection.commit()
			cursor.execute(sql, param)
			res = cursor.fetchall()
			cursor.close()
			self.return_connection(i)
		return res

	def query_one(self, sql, param=[]):
		i = self.get_connection()
		connection = self.connections[i]
		try:
			connection.ping()
		except:
			connection = self.connect()
		finally:
			cursor = self.get_cursor(connection)
			connection.commit()
			cursor.execute(sql, param)
			res = cursor.fetchone()
			cursor.close()
			self.return_connection(i)
		return res

	def update(self, sql, param=[]):
		i = self.get_connection()
		connection = self.connections[i]
		try:
			connection.ping()
		except:
			connection = self.connect()
		finally:
			cursor = self.get_cursor(connection)
			cursor.execute(sql, param)
			connection.commit()
			cursor.close()
			self.return_connection(i)

	def update_get_id(self, sql, param=[]):
		i = self.get_connection()
		connection = self.connections[i]
		try:
			connection.ping()
		except:
			connection = self.connect()
		finally:
			cursor = self.get_cursor(connection)
			cursor.execute(sql, param)
			cursor.execute("SELECT last_insert_id();")
			connection.commit()
			res =  cursor.fetchone()['last_insert_id()']
			cursor.close()
			self.return_connection(i)
		return res