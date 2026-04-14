## Viikko 3

- Kirjautumisen ja rekisteröitymisen toiminnallisuus on toteutettu, käyttäjät tallennetaan SQLite-tietokantaan ja salasanat salataan Werkzeug-kirjaston avulla.
- Sovellukseen on toteutettu kolme alustavaa näkymää, kirjautumis- ja rekisteröitymisnäkymät vastaavat toiminnallisuutta, ja kolmas näkymä on luotu lähinnä siksi, että voidaan kirjautua ulos.
- Testausta on aloitettu `user_test.py`-testeillä: käyttäjän luominen sekä kirjautumisen onnistumis- ja virhetilanteet on testattu ja testikattavuus on niiden osalta 100%.

## Viikko 4

- Tilien lisäämiseen ja poistamiseen liittyvä perustoiminnallisuus sekä käyttöliittymäpuoli on toteutettu.
- Pylint otettu käyttöön ja invoke-käskyt luotu linttaamisen lisäksi buildaamiselle sekä formatoinnille.