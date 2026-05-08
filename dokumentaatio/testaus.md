# Testausdokumentti
Ohjelmaa on testattu manuaalisesti sekä automatisoiduin yksikkö- ja integraatiotestein Unittest-kirjastolla. Testit sijaitsevat `tests`-hakemistossa.

## Testikattavuus
Käyttöliittymäkerroksen testien haaraumakattavuus on seuraavia polkuja lukuunottamatta 100%: _src/**/__init__.py, src/tests/**, src/ui/**, src/index.py, src/build.py, src/db.py, src/config.py_.
![](./kuvat/testikattavuus.png)

## Järjestelmätestaus
Sovelluksen järjestelmätestaus on toteutettu manuaalisesti.

### Asennus ja konfigurointi
Asennus on testattu manuaalisesti [käyttöohjeen](./kayttoohje.md) kuvaamalla tavalla Linux-ympäristössä. Sovellusta on testattu siten, että tietokantatiedosto on valmiiksi olemassa ja siten, ettei sitä ole aluksi ollut.

### Toiminnallisuus
Kaikki [vaatimusmäärittelyssä](./vaatimusmaarittely.md) mainittu toiminnallisuus on testattu manuaalisesti, myös virhetilanteet on pyritty testaamaan mahdollisimman kattavasti.
