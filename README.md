# luotimaster

Luotimaster on kevään 2025 Tietokannat ja web-ohjelmointi-kurssityö. Se on kehitetty toimimaan opiskelijajärjestön [Helsingin yliopiston salamurhaajien](https://salamurhaajat.net/) hallituksen pelaaman _Luotipelin_ hallintointivälineenä. Luotipelissä kaikki hallituksen jäsenet jahtaavat ja pyrkivät "murhaamaan" toisensa sääntöjen mukaisesti hallituksen kokouksien välissä, esimerkiksi nerf-pistooleilla tai "myrkyllisillä" muovihämähäkeillä. 
Ohjelmiston tavoitteena olisi mahdollistaa murhien kirjaamisen yksinkertaisesti ja toimivasti. Luotimaster nimi viittaa järjestön varsinaiseen turnaushallintajärjestelmän, [Surman](https://github.com/hys-helsinki/surma), vaihtoehtoiseen nimeen _Murhamaster 3.0_.


## Kurssin määräämät sovelluksen toiminnot:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. 
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoitettuja tapahtumia ("raportti").
- Käyttäjä näkee sovellukseen lisätyt varmistetut tapahtumat ("murhat"), sekä häntä koskevat raportit.
- Käyttäjä pystyy etsimään kaikkien käyttäjien varmistettuja raportteja hakusanalla.
- Käyttäjä pystyy varmistamaan muiden käyttäjien tekemiä, häntä koskevia raportteja, tehden niistä murhia.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjien lisäämät murhat.
- Käyttäjä pystyy valitsemaan tapahtumalleen asetyypin ja sijainnin. Lisäksi käyttäjät pystyvät lisäämään kuvia tapahtumiin.


## Sovelluksen nykytilanne (27.3.)
Sovellus on kaikkea muuta kuin valmis, mutta sen perustoiminnot, ml. tapahtumien raportointi toimii kuin pitäisi:
- Kirjautuminen ja rekistöröinti toimivat.
- Tapahtumien lisääminen, muokkaaminen, poistaminen ja raportointi toimivat. Tapahtumiin voi lisätä postinumeron ja murhatavan. Käyttäjä voi nähdä omat, häneen kohdistetut raportit, sekä kaikkien käyttäjien murhat.
- Murha-arkistossa on alkeellinen hakutoiminto.




## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql

```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
