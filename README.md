# Tilix App
Sovelluksen avulla käyttäjän on mahdollista toteuttaa kaksinkertaista talouden kirjanpitoa, jossa jokaisen tapahtuman yhteydessä merkitään sekä mistä raha on tullut että minne se on päätynyt. Käyttäjä luo sovellukseen henkilökohtaiset tunnukset.
## Dokumentaatio
* [Käyttöohje](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/kayttoohje.md)
* [Vaatimusmäärittely](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)
* [Työaikakirjanpito](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/tyoaikakirjanpito.md)
* [Changelog](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/changelog.md)
* [Arkkitehtuurikuvaus](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/arkkitehtuuri.md)

Viikon 6 release löytyy [täältä](https://github.com/matiashei/ot-harjoitustyo/releases/tag/viikko6).

## Asennus
1. Asenna sovelluksen riippuvuudet komennolla:
```
poetry install
```
2. Käynnistä virtuaaliympäristö komennolla:
```
eval $(poetry env activate)
```
3. Alusta sovellus komennolla:
```
poetry run invoke build
```
4. Käynnistä sovellus komennolla:
```
poetry run invoke start
```
## Komentorivitoiminnot
* Sovelluksen käynnistäminen komennolla:
```
poetry run invoke start
```
* Testien suorittaminen komennolla:
```
poetry run invoke test
```
* Testikattavuusraportin muodostaminen komennolla:
```
poetry run invoke coverage-report
```
* Pylint-tarkistusten suorittaminen komennolla:
```
poetry run invoke lint
```
* Koodin automaattinen formatointi
```
poetry run invoke format
```
