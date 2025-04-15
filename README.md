# Teoskatalogi
Tietokanta kuvataideteosten teostietoja varten.

Teostiedot sisältävät teoksen nimen ja sen käyttäjätunnuksen, joka on 
tallentanut teoksen tietokantaan.

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
* Jos lisätään teos, jonka nimessä on välilyönti, ja sen jälkeen muokataan sitä,
nimi katkeaa välilyönnin kohdalta.
* Kokoelmaan pitäisi voida liittää teoksia vain kokoelman tekijän.
* Funktio get_collections_by_user ei huomioi tyhjiä kokoelmia

## Suunniteltuja ominaisuuksia
* Joku keino valita teoksia kokoelmiin
* Vuosiluvun lisääminen teostietoihin
* Teoksen tekijän nimen pitäisi voida olla eri kuin käyttäjätunnus
* CSS ja ulkoasun kehittäminen
* Enemmän teostietoja ja kokoelman ominaisuuksia
* Saavutettavuusselvitys
