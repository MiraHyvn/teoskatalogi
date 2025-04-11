import database
from werkzeug.security import generate_password_hash, check_password_hash

def lisaa_kayttaja(tunnus, salasana):
    salasana_hash = generate_password_hash(salasana)
    sql = "INSERT INTO kayttajat (tunnus, salasana_hash) VALUES (?, ?)"
    database.suorita(sql, [tunnus, salasana_hash])

def tarkista_salasana(tunnus, salasana):
    sql = "SELECT salasana_hash, id FROM kayttajat WHERE tunnus = ?"
    tulos = database.kysely(sql, [tunnus])
    if len(tulos) == 1:
        oikea_hash = tulos[0]["salasana_hash"]
        if check_password_hash(oikea_hash, salasana):
            return tulos[0]["id"]
    return None

def hae_kaikki_teokset():
    #sql = "SELECT id, nimi, kayttaja_id FROM teokset ORDER BY id DESC"
    sql = """SELECT 
        T.id, T.nimi, T.kayttaja_id, K.tunnus
    FROM 
        teokset T, kayttajat K
    WHERE
        T.kayttaja_id = K.id
        """    
    return database.kysely(sql)

def hae_teos(teoksen_id):
    #sql = "SELECT id, nimi, kayttaja_id FROM teokset WHERE id = ?"
    sql = """SELECT 
        T.id, T.nimi, T.kayttaja_id, K.tunnus
    FROM 
        teokset T, kayttajat K
    WHERE
        T.kayttaja_id = K.id AND T.id = ?
        """
    return database.kysely(sql, [teoksen_id])[0]

def lisaa_teos(teoksen_nimi, tekijan_id):
    sql = "INSERT INTO teokset (nimi, kayttaja_id) VALUES (?, ?)"
    database.suorita(sql, [teoksen_nimi, tekijan_id])

def poista_teos(teoksen_id):
    sql = "DELETE FROM teokset WHERE id = ?"
    database.suorita(sql, [teoksen_id])

def muuta_teosta(teoksen_id, kentta, uusi_arvo):
    if kentta == "nimi":
        sql = "UPDATE teokset SET nimi = ? WHERE id = ?"
        database.suorita(sql, [uusi_arvo, teoksen_id])

def haku(hakusana):
    sql = """SELECT id, nimi, kayttaja_id FROM teokset 
    WHERE nimi LIKE ? OR kayttaja_id LIKE ?"""
    return database.kysely(sql, ["%"+hakusana+"%", "%"+hakusana+"%"])

def luo_kokoelma(nimi, kayttaja_id):
    sql = "INSERT INTO kokoelmat (kayttaja_id, nimi) VALUES (?, ?)"
    database.suorita(sql, [kayttaja_id, nimi])

def liita_teos_kokoelmaan(teoksen_id, kokoelman_nimi, kayttajan_id):
    sql1 = "SELECT id FROM kokoelmat WHERE nimi = ?"
    tulos1 = database.kysely(sql1, [kokoelman_nimi])
    if len(tulos1) == 0:
        luo_kokoelma(kokoelman_nimi, kayttajan_id)
        tulos1 = database.kysely(sql1, [kokoelman_nimi])
    kokoelman_id = tulos1[0][0]
    sql2 = """INSERT INTO kokoelmanTeokset (teos_id, kokoelma_id)
    VALUES (?, ?)"""
    database.suorita(sql2, [teoksen_id, kokoelman_id])
    return

def hae_kokoelmat_joihin_kuuluu(teoksen_id):
    sql = """SELECT
        K.nimi, K.kayttaja_id, Ka.tunnus
    FROM
        kokoelmat K, teokset T, kokoelmanTeokset KT, kayttajat Ka
    WHERE
        K.id = KT.kokoelma_id AND T.id = KT.teos_id AND T.id = ?
        AND Ka.id = K.kayttaja_id""" 
    return database.kysely(sql, [teoksen_id])

def hae_kaikki_kokoelmat():
    sql = """SELECT 
        K.id, K.nimi, K.kayttaja_id, Ka.tunnus
    FROM 
        kokoelmat K, kayttajat Ka
    WHERE
        Ka.id = K.kayttaja_id
    """
    return database.kysely(sql)
    
def hae_teokset_jotka_kuuluvat(kokoelman_id):
    sql = """SELECT 
        T.nimi, T.kayttaja_id
    FROM
        teokset T, kokoelmat K, kokoelmanTeokset KT
    WHERE
        T.id = KT.teos_id AND K.id = KT.kokoelma_id AND K.id = ?"""
    return database.kysely(sql, [kokoelman_id])
