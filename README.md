# Teoskatalogi
Tietokanta kuvataideteosten teostietoja varten.

Katalogi on taideteosten listaamista varten. Käyttäjä voi lisätä katalogiin
teoksen tiedot kuten teoksen nimen, tekijän nimen ja tekniikan. Käyttäjä
voi muodostaa katalogissa olevista teoksista kokoelmia.

## Ominaisuudet
* Käyttäjä pystyy rekisteröitymään ja kirjautumaan sisään katalogiin.
* Käyttäjä pystyy lisäämään katalogiin teoksia ja muuttamaan lisäämiensä teosten
nimiä.
* Käyttäjä näkee katalogiin lisätyt teokset. Käyttäjä näkee sekä itse 
lisäämänsä että muiden käyttäjien lisäämät teokset.
* Käyttäjä pystyy hakemaan teoksia teoksen nimen tai tekijän nimen perusteella. 
Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä 
teoksia.
* Käyttäjä voi luoda kaikista katalogissa olevista teoksista kokoelmia. Teoksen
tiedoissa näkyy kaikki kokoelmat joihin se kuuluu.
* Katalogissa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä 
tilastoja sekä käyttäjän lisäämät teokset ja kokoelmat.
* Käyttäjä pystyy valitsemaan teoksen tekniikan (luokittelu).

## Ratkaisemattomia ongelmia
* Teoksen muuttaminen aiheuttaa "Database is locked" -virheen, jos sitä ennen on liitetty teoksia kokoelmiin
* Teokset-sivulla kokoelmavalikossa ei ole kaikkia vaihtoehtoja
* Jos lisätään teos tai kokoelma, ja nimikenttä jätetään tyhjäksi, seuraa Forbidden 403
* Jos lisätään teos, jonka nimessä on välilyönti, ja sen jälkeen muokataan sitä,
nimi katkeaa välilyönnin kohdalta.
* Funktio get_collections_by_user ei huomioi tyhjiä kokoelmia
* Saman teoksen voi liittää samaan kokoelmaan monta kertaa
* Käyttäjän syötteiden tarkastaminen

## Suunniteltuja ominaisuuksia
* Käyttöönotto-ohjeet testaamista varten Flask-ympäristöllä
* Joku keino poistaa teoksia kokoelmista
* Vuosiluvun lisääminen teostietoihin
* Teoksen tekijän nimen pitäisi voida olla eri kuin käyttäjätunnus
* CSS ja ulkoasun kehittäminen
* Enemmän teostietoja ja kokoelman ominaisuuksia
* Saavutettavuusselvitys
