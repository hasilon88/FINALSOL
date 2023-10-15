import mysql.connector

# 127.0.0.1
# 3306

# # Function to create a database connection
# def createConnection():
#     db_config = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': '0396',
#         'database': 'messages',
#         'port': 3306
#     }
#     return mysql.connector.connect(**db_config)

# # Used cursor throughout the whole code to prevent SQL injections

# # CRUD Operations for user table:

# createConnection()

# def addUser(conn, name, email, password, privateKey, publicKey):
#     cursor = conn.cursor()
#     query = """
#     INSERT INTO user (name, email, password, private_key, public_key)
#     VALUES (%s, %s, %s, %s, %s)
#     """
#     cursor.execute(query, (name, email, password, privateKey, publicKey))
#     conn.commit()
#     cursor.close()

# def getUserByAttribute(conn, attribute, attributeValue):
#     cursor = conn.cursor(dictionary=True)
#     query = f"SELECT * FROM user WHERE {attribute} = %s"
#     cursor.execute(query, (attributeValue,))
#     user = cursor.fetchone()
#     cursor.close()
#     return user if user else {}

# def updateUser(conn, userId, name=None, email=None, password=None, privateKey=None, publicKey=None):
#     cursor = conn.cursor()
#     fields = []
#     values = []
#     if name:
#         fields.append("name = %s")
#         values.append(name)
#     if email:
#         fields.append("email = %s")
#         values.append(email)
#     if password:
#         fields.append("password = %s")
#         values.append(password)
#     if privateKey:
#         fields.append("private_key = %s")
#         values.append(privateKey)
#     if publicKey:
#         fields.append("public_key = %s")
#         values.append(publicKey)
    
#     values.append(userId)
#     query = f"UPDATE user SET {', '.join(fields)} WHERE id = %s"
#     cursor.execute(query, tuple(values))
#     conn.commit()
#     cursor.close()

# def deleteUser(conn, userId):
#     cursor = conn.cursor()
#     query = "DELETE FROM user WHERE id = %s"
#     cursor.execute(query, (userId,))
#     conn.commit()
#     cursor.close()

# # Get all user ids from user table

# def get_all_user_ids(conn):
#     cursor = conn.cursor()

#     cursor.execute("SELECT id FROM user")
#     results = cursor.fetchall()

#     if not results:
#         return ["no user ids found"]

#     user_ids = [row[0] for row in results]
#     return user_ids

# # CRUD Operations for message table:

# def addMessage(conn, senderId, receiverId, content):
#     cursor = conn.cursor()
#     query = """
#     INSERT INTO message (sender_id, receiver_id, content)
#     VALUES (%s, %s, %s)
#     """
#     cursor.execute(query, (senderId, receiverId, content))
#     conn.commit()
#     cursor.close()

# def getMessageById(conn, messageId):
#     cursor = conn.cursor(dictionary=True)
#     query = "SELECT * FROM message WHERE id = %s"
#     cursor.execute(query, (messageId,))
#     message = cursor.fetchone()
#     cursor.close()
#     return message if message else {}

# def updateMessageContent(conn, messageId, newContent):
#     cursor = conn.cursor()
#     query = """
#     UPDATE message
#     SET content = %s
#     WHERE id = %s
#     """
#     cursor.execute(query, (newContent, messageId))
#     conn.commit()
#     cursor.close()

# def deleteMessage(conn, messageId):
#     cursor = conn.cursor()
#     query = "DELETE FROM message WHERE id = %s"
#     cursor.execute(query, (messageId,))
#     conn.commit()
#     cursor.close()

# # Get all sent and received messages

# def getMessagesByReceiverId(conn, receiverId):
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT message.id, message.content, message.datetime, user.name as sender_name
#     FROM message
#     JOIN user ON message.sender_id = user.id
#     WHERE message.receiver_id = %s
#     """
#     cursor.execute(query, (receiverId,))
#     messages = cursor.fetchall()
#     cursor.close()
#     return messages

# def getSentMessagesBySenderId(conn, senderId):
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT message.id, message.content, message.datetime, user.name as receiver_name
#     FROM message
#     JOIN user ON message.receiver_id = user.id
#     WHERE message.sender_id = %s
#     """
#     cursor.execute(query, (senderId,))
#     messages = cursor.fetchall()
#     cursor.close()
#     return messages

import mariadb

# Function to create a database connection
def createConnection():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '0396',
        'database': 'messages',
        'port': 3306
    }
    return mariadb.connect(**db_config)
# Used cursor throughout the whole code to prevent SQL injections

# CRUD Operations for user table:

def addUser(conn, name, email, password, privateKey, publicKey):
    cursor = conn.cursor()
    query = """
    INSERT INTO user (name, email, password, private_key, public_key)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, email, password, privateKey, publicKey))
    conn.commit()
    cursor.close()

def getUserByAttribute(conn, attribute, attributeValue):
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM user WHERE {attribute} = %s"
    cursor.execute(query, (attributeValue,))
    user = cursor.fetchone()
    cursor.close()
    return user if user else {}

def updateUser(conn, userId, name=None, email=None, password=None, privateKey=None, publicKey=None):
    cursor = conn.cursor()
    fields = []
    values = []
    if name:
        fields.append("name = %s")
        values.append(name)
    if email:
        fields.append("email = %s")
        values.append(email)
    if password:
        fields.append("password = %s")
        values.append(password)
    if privateKey:
        fields.append("private_key = %s")
        values.append(privateKey)
    if publicKey:
        fields.append("public_key = %s")
        values.append(publicKey)
    
    values.append(userId)
    query = f"UPDATE user SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, tuple(values))
    conn.commit()
    cursor.close()

def deleteUser(conn, userId):
    cursor = conn.cursor()
    query = "DELETE FROM user WHERE id = %s"
    cursor.execute(query, (userId,))
    conn.commit()
    cursor.close()

# Get all user ids from user table
def get_all_user_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user")
    results = cursor.fetchall()
    if not results:
        return ["no user ids found"]
    user_ids = [row[0] for row in results]
    return user_ids

# CRUD Operations for message table:
def addMessage(conn, senderId, receiverId, content):
    cursor = conn.cursor()
    query = """
    INSERT INTO message (sender_id, receiver_id, content)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (senderId, receiverId, content))
    conn.commit()
    cursor.close()

def getMessageById(conn, messageId):
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM message WHERE id = %s"
    cursor.execute(query, (messageId,))
    message = cursor.fetchone()
    cursor.close()
    return message if message else {}

def updateMessageContent(conn, messageId, newContent):
    cursor = conn.cursor()
    query = """
    UPDATE message
    SET content = %s
    WHERE id = %s
    """
    cursor.execute(query, (newContent, messageId))
    conn.commit()
    cursor.close()

def deleteMessage(conn, messageId):
    cursor = conn.cursor()
    query = "DELETE FROM message WHERE id = %s"
    cursor.execute(query, (messageId,))
    conn.commit()
    cursor.close()

# Get all sent and received messages
def getMessagesByReceiverId(conn, receiverId):
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT message.id, message.content, message.datetime, user.name as sender_name
    FROM message
    JOIN user ON message.sender_id = user.id
    WHERE message.receiver_id = %s
    """
    cursor.execute(query, (receiverId,))
    messages = cursor.fetchall()
    cursor.close()
    return messages

def getSentMessagesBySenderId(conn, senderId):
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT message.id, message.content, message.datetime, user.name as receiver_name
    FROM message
    JOIN user ON message.receiver_id = user.id
    WHERE message.sender_id = %s
    """
    cursor.execute(query, (senderId,))
    messages = cursor.fetchall()
    cursor.close()
    return messages
