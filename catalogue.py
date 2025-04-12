import database
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(new_username, new_password):
    new_hash = generate_password_hash(new_password)
    sql = "INSERT INTO Users (name, password_hash) VALUES (?, ?)"
    database.execute(sql, [new_username, new_hash])

def get_user_name(user_id):
	sql = "SELECT name FROM users WHERE id = ?"
	query_result = database.query(sql, [user_id])
	if query_result:
		return query_result[0]["name"]
	else:
		return None

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

def get_works_by_user(user_id):
	sql = """SELECT DISTINCT
		W.id, W.title, W.user_id, U.name AS user_name
	FROM
		Works W, Users U
	WHERE
		W.user_id = ? AND W.user_id = U.id"""
	return database.query(sql, [user_id])

def create_work(new_work_title, classes, creator_user_id):
    sql1 = "INSERT INTO Works (title, user_id) VALUES (?, ?)"
    database.execute(sql1, [new_work_title, creator_user_id])
    new_work_id = database.get_last_insert_id()
    for c in classes:
        sql2 = """INSERT INTO WorkClasses (work_id, class_id)
            SELECT W.id, C.id
            FROM Classes C, Works W
            WHERE W.id = ? AND C.title = ? AND C.value = ?"""
        database.execute(sql2, [new_work_id, c, classes[c]])
                

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
    
def get_collections_by_user(user_id):
	sql = """SELECT
		C.id, C.title, C.user_id, U.name AS user_name
	FROM
		Collections C, Users U
	WHERE
		C.user_id = U.id AND C.user_id = ?
	"""
	return database.query(sql, [user_id])

def get_works_included_in(collection_id):
    sql = """SELECT 
        W.title, W.user_id
    FROM
        Works W, Collections C, WorksInCollection WC
    WHERE
        W.id = WC.work_id AND C.id = WC.collection_id AND C.id = ?"""
    return database.query(sql, [collection_id])

def get_user_stats(user_id, collections_by_user):
	# How many works and collections added by user
	# How many times a work by user is added to a collection
	# Average number of works in collections created by user
	sql1 = """SELECT COUNT(id) FROM Works WHERE user_id = ?"""
	work_count = database.query(sql1, [user_id])[0][0]
	sql2 = """SELECT COUNT(id) FROM Collections WHERE user_id = ?"""
	collection_count = database.query(sql2, [user_id])[0][0]
	sql3 = """SELECT
		COUNT(WC.id)
	FROM 
		WorksInCollection WC, Works W 
	WHERE
		W.user_id = ? AND WC.work_id = W.id
	"""
	pick_count = database.query(sql3, [user_id])[0][0]
	sum_works_in_collections = 0
	for c in collections_by_user:
		n = len(get_works_included_in(c["id"]))
		sum_works_in_collections += n
	avg_works_in_collections = sum_works_in_collections / len(collections_by_user)
	result = {}
	result["works"] = work_count
	result["collections"] = collection_count
	result["picks"] = pick_count
	result["avg_collection_size"] = avg_works_in_collections
	return result

def get_all_classes():
	sql = "SELECT title, value FROM Classes"
	query_result = database.query(sql)
	classes = {}
	for title, value in query_result:
		classes[title] = []
	for title, value in query_result:
		classes[title].append(value)
	return classes

def get_classes(work_id):
	sql = """SELECT
		C.title, C.value
	FROM
		Classes C, WorkClasses WC
	WHERE
		WC.work_id = ? AND C.id = WC.class_id"""
	return database.query(sql, [work_id])
