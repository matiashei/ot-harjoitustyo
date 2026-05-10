# Käyttöohje

Lataa projektin viimeisin release Githubista.

## Konfigurointi
Asenna riippuvuudet komennolla:
```
poetry install
```
Aktivoi virtuaaliympäristö komennolla:
```
eval $(poetry env activate)
```
Suorita alustustoimenpiteet komennolla:
```
poetry run invoke build
```
Käynnistä sovellus komennolla:
```
poetry run invoke start
```
## Kirjautuminen ja rekisteröityminen
Sovellus käynnistyy kirjautumisnäkymään, jossa voi joko kirjautua olemassa olevalla käyttäjällä tai siirtyä näkymään, joka mahdollistaa uuden käyttäjätunnuksen luomisen.

## Tilien katseleminen ja hallinta
Kirjautumisen jälkeen käyttäjälle avautuu näkymä, jossa näkyy kaikki käyttäjän tilit. Näkymässä on myös yhteisbalanssi, joka kertoo tilien yhteenlasketun saldon. Käyttäjä voi luoda uuden tilin, joka voi olla joko käyttäjän itsensä hallinnoima tai jonkin ulkoisen tahon tili (esim. vuokranantaja tai työnantaja), poistaa tilin tai tarkastella tilin tapahtumia. Tuplaklikkaamalla tiliä siirrytään tarkastelemaan tilin tapahtumia. Näkymästä voi myös kirjautua ulos.

## Tilitapahtumien hallinta
Näkymä listaa tilitapahtumat taulukkomuodessa. Käyttäjä voi lisätä uusia tilitapahtumia, muokata luotuja tapahtumia ja poistaa tapahtumia. Tapahtuman muokkaaminen onnistuu myös tuplaklikkaamalla yksittäistä tapahtumaa.
