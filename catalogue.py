import database
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(new_username, new_password):
    new_hash = generate_password_hash(new_password)
    sql = "INSERT INTO Users (name, password_hash) VALUES (?, ?)"
    database.execute(sql, [new_username, new_hash])

def check_password(given_username, given_password):
    sql = "SELECT password_hash, id FROM Users WHERE name = ?"
    query_result = database.query(sql, [given_username])
    if len(query_result) == 1:
        correct_hash = query_result[0]["password_hash"]
        if check_password_hash(correct_hash, given_password):
            return query_result[0]["id"]
    return None

def get_all_works():
    sql = """SELECT 
        W.id, W.title, W.user_id, U.name AS user_name
    FROM 
        Works W, Users U
    WHERE
        W.user_id = U.id
        """    
    return database.query(sql)

def get_work(work_id):
    sql = """SELECT 
        W.id, W.title, W.user_id, U.name AS user_name
    FROM 
        Works W, Users U
    WHERE
        W.user_id = U.id AND W.id = ?
        """
    return database.query(sql, [work_id])[0]

def create_work(new_work_title, creator_user_id):
    sql = "INSERT INTO Works (title, user_id) VALUES (?, ?)"
    database.execute(sql, [new_work_title, creator_user_id])

def delete_work(work_id):
    sql = "DELETE FROM Works WHERE id = ?"
    database.execute(sql, [work_id])

def edit_work(work_id, column_name, new_value):
    if column_name == "title":
        sql = "UPDATE Works SET title = ? WHERE id = ?"
        database.execute(sql, [new_value, work_id])

def search(search_term):
    sql = """SELECT 
    		W.id, W.title, W.user_id, U.name AS user_name 	
	FROM 
		Works W, Users U 
    WHERE 
    		W.title LIKE ? OR user_name LIKE ?"""
    return database.query(sql, ["%" +search_term +"%", "%" +search_term +"%"])

def create_collection(new_collection_title, creator_user_id):
    sql = "INSERT INTO Collections (user_id, title) VALUES (?, ?)"
    database.execute(sql, [creator_user_id, new_collection_title])

def add_work_to_collection(work_id, collection_title, adder_user_id):
    sql1 = "SELECT id FROM Collections WHERE title = ?"
    query_result_1 = database.query(sql1, [collection_title])
    if len(query_result_1) == 0:
        create_collection(collection_title, adder_user_id)
        query_result_1 = database.query(sql1, [collection_title])
    new_collection_id = query_result_1[0][0]
    sql2 = """INSERT INTO WorksInCollection (work_id, collection_id)
    VALUES (?, ?)"""
    database.execute(sql2, [work_id, new_collection_id])
    return

def get_collections_that_include(work_id):
    sql = """SELECT
        C.title, C.user_id, U.name AS user_name
    FROM
        Collections C, Works W, WorksInCollection WC, Users U
    WHERE
        C.id = WC.collection_id AND W.id = WC.work_id AND W.id = ?
        AND U.id = C.user_id""" 
    return database.query(sql, [work_id])

def get_all_collections():
    sql = """SELECT 
        C.id, C.title, C.user_id, U.name AS user_name
    FROM 
        Collections C, Users U
    WHERE
        U.id = C.user_id
    """
    return database.query(sql)
    
def get_works_included_in(collection_id):
    sql = """SELECT 
        W.title, W.user_id
    FROM
        Works W, Collections C, WorksInCollection WC
    WHERE
        W.id = WC.work_id AND C.id = WC.collection_id AND C.id = ?"""
    return database.query(sql, [collection_id])
