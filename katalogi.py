import tietokanta

def lisaa_kayttaja(tunnus, salasana_hash):
    sql = "INSERT INTO kayttajat (tunnus, salasana_hash) VALUES (?, ?)"
    tietokanta.suorita(sql, [tunnus, salasana_hash])

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

