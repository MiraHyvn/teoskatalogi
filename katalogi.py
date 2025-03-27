import tietokanta
from werkzeug.security import generate_password_hash, check_password_hash

def lisaa_kayttaja(tunnus, salasana):
    salasana_hash = generate_password_hash(salasana)
    sql = "INSERT INTO kayttajat (tunnus, salasana_hash) VALUES (?, ?)"
    tietokanta.suorita(sql, [tunnus, salasana_hash])

def tarkista_salasana(tunnus, salasana):
    sql = "SELECT salasana_hash FROM kayttajat WHERE tunnus = ?"
    oikea_hash = tietokanta.kysely(sql, [tunnus])[0][0]
    if check_password_hash(oikea_hash, salasana):
        return True
    else:   
        return False 

def hae_kaikki_teokset():
    sql = "SELECT id, nimi, kayttaja_id FROM teokset"
    return tietokanta.kysely(sql)

def hae_teos(teoksen_id):
    sql = "SELECT id, nimi, kayttaja_id FROM teokset WHERE id = ?"
    return tietokanta.kysely(sql, [teoksen_id])[0]

def lisaa_teos(teoksen_nimi, tekijan_nimi):
    sql = "INSERT INTO teokset (nimi, kayttaja_id) VALUES (?, ?)"
    tietokanta.suorita(sql, [teoksen_nimi, tekijan_nimi])

def poista_teos(teoksen_id):
    sql = "DELETE FROM teokset WHERE id = ?"
    tietokanta.suorita(sql, [teoksen_id])

def muuta_teosta(teoksen_id, kentta, uusi_arvo):
    if kentta == "nimi":
        sql = "UPDATE teokset SET nimi = ? WHERE id = ?"
        tietokanta.suorita(sql, [uusi_arvo, teoksen_id])

def haku(hakusana):
    sql = """SELECT id, nimi, kayttaja_id FROM teokset 
    WHERE nimi LIKE ? OR kayttaja_id LIKE ?"""
    return tietokanta.kysely(sql, ["%"+hakusana+"%", "%"+hakusana+"%"])

