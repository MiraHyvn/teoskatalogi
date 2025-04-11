import database
from werkzeug.security import generate_password_hash, check_password_hash

def lisaa_kayttaja(tunnus, salasana):
    salasana_hash = generate_password_hash(salasana)
    sql = "INSERT INTO Users (name, password_hash) VALUES (?, ?)"
    database.execute(sql, [tunnus, salasana_hash])

def tarkista_salasana(tunnus, salasana):
    sql = "SELECT password_hash, id FROM Users WHERE name = ?"
    tulos = database.query(sql, [tunnus])
    if len(tulos) == 1:
        oikea_hash = tulos[0]["password_hash"]
        if check_password_hash(oikea_hash, salasana):
            return tulos[0]["id"]
    return None

def hae_kaikki_teokset():
    sql = """SELECT 
        W.id, W.name, W.user_id, U.name AS user_name
    FROM 
        Works W, Users U
    WHERE
        W.user_id = U.id
        """    
    return database.query(sql)

def hae_teos(teoksen_id):
    sql = """SELECT 
        W.id, W.name, W.user_id, U.name AS user_name
    FROM 
        Works W, Users U
    WHERE
        W.user_id = U.id AND W.id = ?
        """
    return database.query(sql, [teoksen_id])[0]

def lisaa_teos(teoksen_nimi, tekijan_id):
    sql = "INSERT INTO Works (name, user_id) VALUES (?, ?)"
    database.execute(sql, [teoksen_nimi, tekijan_id])

def poista_teos(teoksen_id):
    sql = "DELETE FROM Works WHERE id = ?"
    database.execute(sql, [teoksen_id])

def muuta_teosta(teoksen_id, kentta, uusi_arvo):
    if kentta == "nimi":
        sql = "UPDATE Works SET name = ? WHERE id = ?"
        database.execute(sql, [uusi_arvo, teoksen_id])

def haku(hakusana):
    sql = """SELECT 
    		W.id, W.name, W.user_id, U.name AS user_name 	
	FROM 
		Works W, Users U 
    WHERE 
    		W.name LIKE ? OR user_name LIKE ?"""
    return database.query(sql, ["%"+hakusana+"%", "%"+hakusana+"%"])

def luo_kokoelma(nimi, kayttaja_id):
    sql = "INSERT INTO Collections (user_id, name) VALUES (?, ?)"
    database.execute(sql, [kayttaja_id, nimi])

def liita_teos_kokoelmaan(teoksen_id, kokoelman_nimi, kayttajan_id):
    sql1 = "SELECT id FROM Collections WHERE name = ?"
    tulos1 = database.query(sql1, [kokoelman_nimi])
    if len(tulos1) == 0:
        luo_kokoelma(kokoelman_nimi, kayttajan_id)
        tulos1 = database.query(sql1, [kokoelman_nimi])
    kokoelman_id = tulos1[0][0]
    sql2 = """INSERT INTO WorksInCollection (work_id, collection_id)
    VALUES (?, ?)"""
    database.execute(sql2, [teoksen_id, kokoelman_id])
    return

def hae_kokoelmat_joihin_kuuluu(teoksen_id):
    sql = """SELECT
        C.name, C.user_id, U.name AS user_name
    FROM
        Collections C, Works W, WorksInCollection WC, Users U
    WHERE
        C.id = WC.collection_id AND W.id = WC.work_id AND W.id = ?
        AND U.id = C.user_id""" 
    return database.query(sql, [teoksen_id])

def hae_kaikki_kokoelmat():
    sql = """SELECT 
        C.id, C.name, C.user_id, U.name AS user_name
    FROM 
        Collections C, Users U
    WHERE
        U.id = C.user_id
    """
    return database.query(sql)
    
def hae_teokset_jotka_kuuluvat(kokoelman_id):
    sql = """SELECT 
        W.name, W.user_id
    FROM
        Works W, Collections C, WorksInCollection WC
    WHERE
        W.id = WC.work_id AND C.id = WC.collection_id AND C.id = ?"""
    return database.query(sql, [kokoelman_id])
