# Teoskatalogi

Tietokanta kuvataideteosten teostietoja varten.

Katalogi on taideteosten listaamista varten. Käyttäjä voi lisätä katalogiin
teoksen tiedot kuten teoksen nimen, tekijän nimen ja tekniikan. Käyttäjä
voi muodostaa katalogissa olevista teoksista kokoelmia.

## Käyttöohjeet

Luo venv-virtuaaliympäristö, asenna flask ja luo tietokanta:

```
make
```

Sovellusta voi tämän jälkeen ajaa virtuaaliympäristössä seuraavasti:

```
$ source venv/bin/activate
(venv) $ flask run
```

Tämän ollessa käynnissä websivun pitäisi näkyä osoitteessa `localhost:5000`.

Virtuaaliympäristöstä voi poistua seuraavasti:

```
(venv) $ deactivate
```

Sovelluksen poistaminen:

```
make remove
```

## Ominaisuudet

* Käyttäjä pystyy rekisteröitymään ja kirjautumaan sisään katalogiin.
* Käyttäjä pystyy lisäämään katalogiin teoksia ja muuttamaan lisäämiensä teostennimiä.
* Käyttäjä näkee katalogiin lisätyt teokset. Käyttäjä näkee sekä itse
lisäämänsä että muiden käyttäjien lisäämät teokset.
* Käyttäjä pystyy hakemaan teoksia teoksen nimen tai tekijän nimen perusteella.
Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä
teoksia.
* Käyttäjä voi luoda kaikista katalogissa olevista teoksista kokoelmia. Teoksen tiedoissa näkyy kaikki kokoelmat joihin se kuuluu.
* Katalogissa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä
tilastoja sekä käyttäjän lisäämät teokset ja kokoelmat.
* Käyttäjä pystyy valitsemaan teoksen tekniikan (luokittelu).

## Ratkaisemattomia ongelmia

* Jos yritetään luoda käyttäjä, joka on jo olemassa, tai liittää teos kokoelmaan, johon se kuuluu jo, tietokanta menee lukkoon (database locked). IntegrityError käsitellään mutta yhteyttä ei suljeta missään kohtaa.

## Suunniteltuja ominaisuuksia

* Selkeämpi rekisteröityminen
* CSS ja ulkoasun kehittäminen
* Joku keino poistaa teoksia kokoelmista
* Esteellisyyden arvioiminen
* Vuosiluvun lisääminen teostietoihin
* Teoksen tekijän nimen pitäisi voida olla eri kuin käyttäjätunnus
* Enemmän teostietoja ja kokoelman ominaisuuksia
