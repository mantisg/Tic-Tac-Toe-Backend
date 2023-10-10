from flask import Flask, jsonify
from flask_mysqldb import MySQL

##App init and configuration

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'MantisG'
app.config['MYSQL_PASSWORD'] = 'S0lshe@rt1028!'
app.config['MYSQL_DB'] = 'Tic_Tac_Toe_db'

mysql = MySQL(app)

##TEST

DEFAULT_HISTORY = [[None]*9]

@app.route('/core')
def core_game():
	return jsonify({
	        "players": ["X", "O"],
	        "history": DEFAULT_HISTORY.copy(),
    })

##GET all data from each table

@app.route('/board', methods=['GET'])
def get_board():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM board''')
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

@app.route('/users', methods=['GET'])
def get_users():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM user_profile''')
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

@app.route('/games', methods=['GET'])
def get_games():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM games''')
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

@app.route('/pg', methods=['GET'])
def get_pg():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM profile_game''')
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

@app.route('/moves', methods=['GET'])
def get_moves():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM moves''')
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

##GET data from tables by id

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM user_profile WHERE p_id = %s''', (id,))
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

@app.route('/games/<int:id>', methods=['GET'])
def get_game_by_id(id):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM games WHERE g_id = %s''', (id,))
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

@app.route('/moves/<int:id>', methods=['GET'])
def get_move_by_id(id):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM moves WHERE m_id = %s''', (id))
	data = cur.fetchall()
	cur.close()
	return jsonify(data)

##POST, adding new data to tables

@app.route('/users', methods=['POST'])
def add_user():
	cur = mysql.connection.cursor()
	profileid = None
	username = request.json['username']
	fname = request.json['fname']
	lname = request.json['lname']
	cur.execute('''INSERT INTO user_profile (p_id, username, fname, lname) VALUES (%s)''', (profileid, username, fname, lname))
	mysql.connection.commit()
	cur.close()
	return jsonify({'message': 'Data added successfully'})

@app.route('/games', methods=['POST'])
def add_game():
	cur = mysql.connection.cursor()
	gameid = None
	title = request.json['title']
	cur.execute('''INSERT INTO games (g_id, title) VALUES (%s)''', (gameid, title))
	mysql.connection.commit()
	cur.close()
	return jsonify({'message': 'Data added successfully'})

@app.route('/moves', methods=['POST'])
def add_move():
	cur = mysql.connection.cursor()
	moveid = None
	profileid = request.json['p_id']
	gameid = request.json['g_id']
	value = request.json['value']
	boardid = request.json['b_id']
	cur.execute('''INSERT INTO moves (m_id, p_id, g_id, value, b_id) VALUES (%s)''', (moveid, profileid, gameid, value, boardid))
	mysql.connection.commit()
	cur.close()
	return jsonify({'message': 'Data added successfully'})

##PUT, update and change objects in tables

@app.route('/moves/<int:id>', methods=['PUT'])
def update_move(id):
	cur = mysql.connection.cursor()
	moveid = request.json['m_id']
	profileid = request.json['p_id']
	gameid = request.json['g_id']
	value = request.json['value']
	boardid = request.json['b_id']
	cur.execute('''UPDATE moves SET m_id = %s, p_id = %s, g_id = %s, value = %s, b_id = %s WHERE m_id = %s''', (moveid, profileid, gameid, value, boardid))
	mysql.connection.commit()
	cur.close()
	return ({'message': 'Data updated successfully'})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
	cur = mysql.connection.cursor()
	profileid = request.json['p_id']
	username = request.json['username']
	fname = request.json['fname']
	lname = request.json['lname']
	cur.execute('''UPDATE user_profile SET p_id = %s, username = %s, fname = %s, lname = %s WHERE p_id = %s''', (profileid, username, fname, lname))
	mysql.connection.commit()
	cur.close()
	return ({'message': 'user_profile updated successfully'})

@app.route('/games/<int:id>', methods=['PUT'])
def update_games(id):
	cur = mysql.connection.cursor()
	gameid = request.json['g_id']
	title = request.json['title']
	cur.execute('''UPDATE games SET g_id = %s, title = %s WHERE g_id = %s''', (gameid, title))
	mysql.connection.commit()
	cur.close()
	return ({'message': 'games updated successfully'})

##DELETE, deleting objects from tables

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
	cur = mysql.connection.cursor()
	cur.execute('''DELETE FROM user_profile WHERE p_id = %s''', (id,))
	mysql.connection.commit()
	cur.close()
	return({'message': 'User deleted successfully'})

@app.route('/games/<int:id>', methods=['GET'])
def delete_game(id):
	cur = mysql.connection.cursor()
	cur.execute('''DELETE FROM games WHERE g_id = %s''', (id,))
	mysql.connection.commit()
	cur.close()
	return ({'message': 'Game deleted successfully'})

##GO OVER DELETE MOVE LOGIC

if __name__ == '__main__':
	app.run(debug=True)