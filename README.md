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
* Jos teoksia poistetaan ja lisätään, kokoelmien viitteet eivät pysy oikeina. 
(Esimerkiksi jos teos #4 on liitetty kokoelmaan #1, ja teos #4 poistetaan, ja 
luodaan uusi teos joka saa indeksikseen 4, uusi teos sisältyy kokoelmaan #1.) 
* /muokkaa_teosta/1 tuottaa IndexError: list index out of range, kun teosta #1
ei ole. Pitäisi tuottaa 404.

## Suunniteltuja ominaisuuksia
* CSS ja ulkoasun kehittäminen
* Tietokannan laajentaminen
* Tietoturvan parantaminen
* Saavutettavuuden parantaminen
