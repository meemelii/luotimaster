# luotimaster

Luotimaster on kevään 2025 Tietokannat ja web-ohjelmointi-kurssityö. Se on kehitetty toimimaan opiskelijajärjestön [Helsingin yliopiston salamurhaajien](https://salamurhaajat.net/) hallituksen pelaaman _Luotipelin_ hallintointivälineenä. Luotipelissä kaikki hallituksen jäsenet jahtaavat ja pyrkivät "murhaamaan" toisensa sääntöjen mukaisesti hallituksen kokouksien välissä, esimerkiksi nerf-pistooleilla tai "myrkyllisillä" muovihämähäkeillä. 
Ohjelmiston tavoitteena olisi mahdollistaa murhien kirjaamisen yksinkertaisesti ja toimivasti. Luotimaster nimi viittaa järjestön varsinaiseen turnaushallintajärjestelmän, [Surman](https://github.com/hys-helsinki/surma), vaihtoehtoiseen nimeen _Murhamaster 3.0_.


## Kurssin määräämät sovelluksen toiminnot:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. 
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoitettuja tapahtumia ("raportti").
- Käyttäjä näkee sovellukseen lisätyt varmistetut tapahtumat ("murhat"), sekä häntä koskevat raportit.
- Käyttäjä pystyy etsimään kaikkien käyttäjien murhia hakusanalla.
- Käyttäjä pystyy varmistamaan muiden käyttäjien tekemiä, häntä koskevia raportteja, tehden niistä murhia.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjien lisäämät murhat.
- Käyttäjä pystyy valitsemaan tapahtumalleen asetyypin ja sijainnin.
- Käyttäjät pystyvät lisäämään kuvan profiilikuvakseen.

## Sovelluksen nykytilanne
Sovellus on hyvässä tilanteessa, joskin se sisältää vielä useita kehityskohteita ja epäoptimaalisuuksia, ja vaatii työtä mm. suuren tietomäärän, saavutettavuuden ja koodin siivoamisen osalta. 
- Kirjautuminen ja rekistöröinti toimivat.
- Tapahtumien lisääminen, muokkaaminen, poistaminen ja raportointi toimivat. Tapahtumiin voi lisätä postinumeron ja murhatavan. 
- Tapahtuman ilmoittaja sekä sen kohde voivat kommentoida tapahtumaa. Kommentit voi nähdä tapahtumasivulla, joskin niiden visuaalisointi on hyvin kesken. 
- Käyttäjä voi nähdä omat, häneen kohdistetut raportit, sekä kaikkien käyttäjien murhat. Murha-arkistossa on alkeellinen hakutoiminto.
- Etusivulla näkyy top 5 pelaajaa (murhien määrä).
- Käyttäjillä on omat sivut, joilla näkyy profiilikuva, murhien ja kuolemien määrä, viimeisimmät 5 murhaa ja kuolemaa eriteltyinä, sekä linkki kaikkiin murhiin ja kuolemiin.
- Sovelluksella on visuaalisesti oma ulkonäkö. 


## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
