import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_on_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(2000)
        self.assertEqual(self.maksukortti.saldo, 3000)

    def test_rahan_ottaminen_toimii_kun_saldo_on_riittava(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 500)

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(2000)
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_ota_rahaa_palauttaa_true_jos_rahaa_riittaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(100), True)

    def test_ota_rahaa_palauttaa_false_jos_rahaa_ei_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(5000), False)

    def test_saldo_euroina_palauttaa_oikean_arvon(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_str_palauttaa_oikean_merkkijonon(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")