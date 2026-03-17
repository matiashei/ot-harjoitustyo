import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_rahamaara_ja_myytyjen_lounaiden_maara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_toimii_edullisella(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(400), 160)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateisosto_toimii_maukkaalla(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateisosto_ei_toimi_jos_raha_ei_riita_edullisesti(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateisosto_ei_toimi_jos_raha_ei_riita_maukkaasti(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttiosto_toimii_edullisella(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)
        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_korttiosto_toimii_maukkaalla(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)
        self.assertEqual(self.kortti.saldo, 600)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttiosto_ei_toimi_jos_saldo_ei_riita_edullisesti(self):
        self.kortti.ota_rahaa(800)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), False)
        self.assertEqual(self.kortti.saldo, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_korttiosto_ei_toimi_jos_saldo_ei_riita_maukkaasti(self):
        self.kortti.ota_rahaa(800)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), False)
        self.assertEqual(self.kortti.saldo, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kortille_rahaa_ladattaessa_kassan_rahamaara_kasvaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_kortille_rahaa_ladattaessa_negatiivinen_summa_ei_onnistu(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -100)
        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassassa_rahaa_euroina_palauttaa_oikean_arvon(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)