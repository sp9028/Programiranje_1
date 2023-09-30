import collections
import unittest
import warnings
from collections import defaultdict


def brisi_ponovitve(s):
    ponovitve = defaultdict(int)
    i = 0
    while i < len(s):
        ponovitve[s[i]] += 1
        if ponovitve[s[i]] > s[i]:
            del s[i]
        else:
            i += 1


def najvecji_v_vseh(s):
    # Če naloga hoče da ni prepočasna uporabi množice slovarje itd in ne seznamov
    if not s:
        return None
    presek = set(s[0])
    for t in s:
        presek &= set(t)
    if presek:
        return max(presek)


def vrstni_red(ime_datoteke):
    # metoda sort() posortira vse vrednostiče so številke po velikosti če sta pa številki enaki pa glede na črko če
    # je zravn še ime
    rezultati = []
    for v in open(ime_datoteke, encoding="utf8"):
        ime, m, s = v.strip().split(":")
        rezultati.append((int(m), int(s), ime))
    rezultati.sort()
    return [ime for m, s, ime in rezultati]


def preveri_vsoto(s, n):
    if not s:
        return n == 0
    else:
        return preveri_vsoto(s[1:], n - s[0])


class Cakalnica:

    def __init__(self):
        self.prihodi = []
        self.odhod = []

    def prihod(self, ime, cas):
        self.prihodi.append((ime, cas))

    def cakajocih(self):
        return len(self.prihodi)

    def naslednji(self, cas):
        if not self.prihodi:
            return None
        else:
            oseba,_cas = self.prihodi[0]
            self.odhod.append((oseba,_cas, cas))
            del self.prihodi[0]
        return oseba

    def skupni_cas_cakanja(self):
        skupni_cas = 0
        if not self.odhod:
            return skupni_cas
        else:
            for ime,prihod,odhod in self.odhod:
                skupni_cas += abs(prihod - odhod)
        return skupni_cas

    def povprecni_cas_cakanja(self):
        if not self.odhod:
            return 0
        else:
            return self.skupni_cas_cakanja() / len(self.odhod)


class Test(unittest.TestCase):
    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)

    def test_01_brisi_ponovitve(self):
        a = [1, 3, 4, 1, 3, 2, 2, 3, 5, 3, 2, 4]
        self.assertIsNone(brisi_ponovitve(a), "Funkcija naj ne vrne ničesar")
        self.assertEqual([1, 3, 4, 3, 2, 2, 3, 5, 4], a)

        a = [3, 1, 3, 3, 2, 3, 4, 3, 3, 3, 5, 3, 6]
        brisi_ponovitve(a)
        self.assertEqual([3, 1, 3, 3, 2, 4, 5, 6], a)

    def test_02_najvecji_v_vseh(self):
        self.assertEqual(3, najvecji_v_vseh([[5, 1, 2, 3], [3, 1, 8], [42, 5, 3, 1]]))
        self.assertIsNone(najvecji_v_vseh([[5, 1, 2, 3], [4, 1, 8], [42, 5, 3, 2]]))
        self.assertIsNone(najvecji_v_vseh([]))

        a = list(range(1_000_000)) + list(range(2_000_000, 2_100_000))
        b = list(range(500_000, 1_500_000))
        self.assertEqual(999_999, najvecji_v_vseh([a, b]))

    def test_03_vrstni_red(self):
        with open("f1.txt", "wt", encoding="utf8") as f:
            f.write("""Ana Anžič: 5:12
Berta Bertolin: 4:48
Cilka Centrih: 5:05
Dani Dolinar: 10:12
Ema Evelina Estrih: 4:45""")
        self.assertEqual(
            ["Ema Evelina Estrih", "Berta Bertolin", "Cilka Centrih", "Ana Anžič", "Dani Dolinar"],
            vrstni_red("f1.txt"))

        with open("f1.txt", "wt", encoding="utf8") as f:
            f.write("""Ana Anžič: 5:12
Berta Bertolin: 4:45
Cilka Centrih: 5:05
Dani Dolinar: 10:12
Ema Evelina Estrih: 4:45""")
        self.assertEqual(
            ["Berta Bertolin", "Ema Evelina Estrih", "Cilka Centrih", "Ana Anžič", "Dani Dolinar"],
            vrstni_red("f1.txt"))

    def test_04_preveri_vsoto(self):
        try:
            preveri_vsoto(list(range(1111)), 4_000_000)
            self.fail("Funkcija mora biti rekurzivna")
        except RecursionError:
            pass
        self.assertTrue(preveri_vsoto([5, 1, 2, 5, 6], 19))
        self.assertFalse(preveri_vsoto([5, 1, 2, 5, 6], 22))
        self.assertFalse(preveri_vsoto([5, 1, 2, 5, 6], 0))
        self.assertFalse(preveri_vsoto([], 19))
        self.assertTrue(preveri_vsoto([], 0))

    def test_05_cakalnica(self):
        cakalnica = Cakalnica()
        self.assertEqual(0, cakalnica.cakajocih())
        self.assertEqual(0, cakalnica.skupni_cas_cakanja())
        self.assertIsNone(cakalnica.naslednji(8.00))

        self.assertIsNone(cakalnica.prihod("Dani", 8.50))
        cakalnica.prihod("Berta", 9.00)
        cakalnica.prihod("Cilka", 9.25)
        self.assertEqual(3, cakalnica.cakajocih())
        self.assertEqual(0, cakalnica.skupni_cas_cakanja())

        self.assertEqual("Dani", cakalnica.naslednji(9.75))
        self.assertEqual(2, cakalnica.cakajocih())
        self.assertAlmostEqual(1.25, cakalnica.skupni_cas_cakanja())
        self.assertAlmostEqual(1.25, cakalnica.povprecni_cas_cakanja())

        self.assertEqual("Berta", cakalnica.naslednji(10))
        self.assertEqual(1, cakalnica.cakajocih())
        self.assertAlmostEqual(1.25 + 1, cakalnica.skupni_cas_cakanja())
        self.assertAlmostEqual((1.25 + 1) / 2, cakalnica.povprecni_cas_cakanja())

        self.assertEqual("Cilka", cakalnica.naslednji(10.15))
        self.assertEqual(0, cakalnica.cakajocih())
        self.assertAlmostEqual(1.25 + 1 + 0.9, cakalnica.skupni_cas_cakanja())
        self.assertAlmostEqual((1.25 + 1 + 0.9) / 3, cakalnica.povprecni_cas_cakanja())

        self.assertIsNone(cakalnica.naslednji(10.15))
        self.assertEqual(0, cakalnica.cakajocih())
        self.assertAlmostEqual(1.25 + 1 + 0.9, cakalnica.skupni_cas_cakanja())
        self.assertAlmostEqual((1.25 + 1 + 0.9) / 3, cakalnica.povprecni_cas_cakanja())


if __name__ == "__main__":
    unittest.main()
