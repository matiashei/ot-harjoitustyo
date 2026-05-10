# Käyttöohje

Lataa projektin viimeisin release Githubista.

## Konfigurointi
1. Siirry kansioon ```tilix-app```
2. Asenna riippuvuudet komennolla:
```
poetry install
```
3. Luo tietokantatiedoston nimen määrittelevä .env-tiedosto projektin juureen, tiedoston sisältö voi olla esimerkiksi:
```
DATABASE_FILENAME=database.sqlite
```
4. Aktivoi virtuaaliympäristö komennolla:
```
eval $(poetry env activate)
```
5. Suorita alustustoimenpiteet komennolla:
```
poetry run invoke build
```
6. Käynnistä sovellus komennolla:
```
poetry run invoke start
```
## Kirjautuminen ja rekisteröityminen
Sovellus käynnistyy kirjautumisnäkymään, jossa voi joko kirjautua olemassa olevalla käyttäjällä tai siirtyä näkymään, joka mahdollistaa uuden käyttäjätunnuksen luomisen.

## Tilien katseleminen ja hallinta
Kirjautumisen jälkeen käyttäjälle avautuu näkymä, jossa näkyy kaikki käyttäjän tilit. Näkymässä on myös yhteisbalanssi, joka kertoo tilien yhteenlasketun saldon. Käyttäjä voi luoda uuden tilin, joka voi olla joko käyttäjän itsensä hallinnoima tai jonkin ulkoisen tahon tili (esim. vuokranantaja tai työnantaja), poistaa tilin tai tarkastella tilin tapahtumia. Tuplaklikkaamalla tiliä siirrytään tarkastelemaan tilin tapahtumia. Näkymästä voi myös kirjautua ulos.

## Tilitapahtumien hallinta
Näkymä listaa tilitapahtumat taulukkomuodessa. Käyttäjä voi lisätä uusia tilitapahtumia, muokata luotuja tapahtumia ja poistaa tapahtumia. Tapahtuman muokkaaminen onnistuu myös tuplaklikkaamalla yksittäistä tapahtumaa.
