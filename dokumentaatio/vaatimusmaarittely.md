# Vaatimusmäärittely
## Sovelluksen tarkoitus
Sovelluksen avulla käyttäjän on mahdollista toteuttaa kaksinkertainen kirjanpito, jossa jokaisen tapahtuman yhteydessä merkitään sekä mistä raha on tullut että minne se on päätynyt.

## Käyttäjät
Sovelluksella on alkuvaiheessa yksi käyttäjärooli eli _normaali käyttäjä_✅, muiden käyttäjäroolien tarpeellisuutta punnitaan myöhemmässä vaiheessa.

## Käyttöliittymäluonnos
Sovellus koostuu kuudesta eri näkymästä, jotka ovat:
* kirjautumisnäkymä✅
* rekisteröitymisnäkymä✅
* tilit listaava sekä yhteisbalanssin laskeva näkymä✅
* uuden tilin lisäämisen mahdollistava näkymä ✅
* tilin tapahtumat näyttävä näkymä
* uusien tapahtumien lisäämisen mahdollistava näkymä
```mermaid
flowchart TD

A[Login] -->|Login| C[Dashboard]
A -->|Register| B[Create Account]
B --> C

C --> D[Accounts Overview]
D --> E[Account Details]
```

```mermaid
flowchart TD

subgraph Login_View [Login View]
    A1[Username]
    A2[Password]
    A3[Login Button]
    A4[Register Button]
end

subgraph Register_View [Register View]
    B1[Username]
    B2[Password]
    B3[Create Account Button]
end

subgraph Dashboard_View [Accounts Overview]
    D1[Assets]
    D2[Equity]
    D3[Expenses]
end

subgraph Account_Details_View [Account Details]
    E1[Date]
    E2[Description]
    E3[Amount]
end
```
## Perusversion toiminnallisuus
* Käyttäjä voi luoda sovellukseen käyttäjätunnuksen ja asettaa sille salasanan.
    * Jos käyttäjätunnus on jo käytössä, järjestelmä ilmoittaa asiasta.
    * Jos salasana tai käyttäjätunnus on väärä, järjestelmä ilmoittaa asiasta.
* Käyttäjä voi luoda, poistaa ja tarkastella tilejä.
* Käyttäjä voi luoda, poistaa ja tarkastella tilitapahtumia.
* Käyttäjä voi kirjautua ulos järjestelmästä.

## Jatkokehitysideoita
* Tilitapahtumien editointi.
* Käyttäjätiimit, joiden jäsenillä voi olla erilaisia oikeuksia.
* Tietokanta, johon tilit ja tilitiedot tallentuvat, on salattu ja salaamisen voi purkaa kirjautumalla sisään. Tämän myötä kirjautumisominaisuudesta tulee merkityksellinen järjestelmän toiminnan kannalta.
