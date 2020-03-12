from unittest import TestCase


class Test(TestCase):
    def test_versilibre(self):
        from funcionesreserva import versilibre
        self.assertTrue(versilibre(2))
