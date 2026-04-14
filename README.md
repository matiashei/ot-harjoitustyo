# Tilix App
Sovelluksen avulla käyttäjän on mahdollista toteuttaa kaksinkertaista talouden kirjanpitoa, jossa jokaisen tapahtuman yhteydessä merkitään sekä mistä raha on tullut että minne se on päätynyt. Käyttäjä luo sovellukseen henkilökohtaiset tunnukset.
## Dokumentaatio
* [Vaatimusmäärittely](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)
* [Työaikakirjanpito](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/tyoaikakirjanpito.md)
* [Changelog](https://github.com/matiashei/ot-harjoitustyo/blob/main/dokumentaatio/changelog.md)

## Asennus
1. Asenna sovelluksen riippuvuudet komennolla:
```bash
poetry install
```
2. Alusta sovellus komennolla:
```bash
poetry run invoke build
```
3. Käynnistä sovellus komennolla:
```bash
poetry run invoke start
```
## Komentorivitoiminnot
* Sovelluksen käynnistäminen komennolla:
```bash
poetry run invoke start
```
* Testien suorittaminen komennolla:
```bash
póetry run invoke test
```
* Testikattavuusraportin muodostaminen komennolla:
```bash
poetry run invoke coverage-report
```
* Pylint-tarkistusten suorittaminen komennolla:
```bash
poetry run invoke lint
```
