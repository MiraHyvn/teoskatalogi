# Teoskatalogi
Tietokanta kuvataideteosten teostietoja varten.

Teostiedot sisältävät teoksen nimen ja sen käyttäjätunnuksen, joka on 
tallentanut teoksen tietokantaan.

## Ominaisuudet
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään katalogiin.
* Käyttäjä pystyy lisäämään katalogiin teoksia. Lisäksi käyttäjä pystyy 
muokkaamaan ja poistamaan lisäämiään teostietoja.
* Käyttäjä näkee katalogiin lisätyt teokset. Käyttäjä näkee sekä itse 
lisäämänsä että muiden käyttäjien lisäämät teokset.
* Käyttäjä pystyy etsimään teoksia teoksen nimen tai tekijän nimen perusteella. 
Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä 
teoksia.
* Käyttäjä voi luoda kaikista katalogissa olevista teoksista kokoelmia. Teoksen
tiedoissa näkyy kaikki kokoelmat joihin se kuuluu.

## Suunnitellut ominaisuudet
* Katalogissa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä 
tilastoja ja käyttäjän lisäämät teokset.
* Käyttäjä pystyy valitsemaan teokselle yhden tai useamman luokittelun, kuten 
missä näyttelyssä teos on esitetty; teoksen tyyppi kuten taulu, veistos tai 
video; tai kokoluokitus kuten pieni, keskikokoinen tai suuri. Mahdolliset 
luokat ovat tietokannassa.


## Ratkaisemattomia ongelmia
Jos lisätään teos, jonka nimessä on välilyönti, ja sen jälkeen muokataan sitä,
nimi katkeaa välilyönnin kohdalta.

Jos kirjautuessa syötetään tunnus jota ei ole, tulee "internal server error" 
(500).

Rekisteröityminen on mahdollista vaikka ollaan jo kirjautuneena sisään.

Syötteet voivat olla tyhjiä. (Uuden teoksen nimi, kokoelman nimi)

Kokoelmaan pitäisi voida liittää teoksia vain sen tekijän.

Jos teoksia poistetaan ja lisätään, kokoelmien viitteet eivät pysy oikeina. 
(Esimerkiksi jos teos #4 on liitetty kokoelmaan #1, ja teos #4 poistetaan, ja 
luodaan uusi teos joka saa indeksikseen 4, uusi teos sisältyy kokoelmaan #1.) 

/muokkaa_teosta/1 tuottaa IndexError: list index out of range, kun teosta #1
ei ole. Pitäisi tuottaa 404.

