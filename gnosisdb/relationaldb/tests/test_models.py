from django.test import TestCase
from relationaldb.factories import CentralizedOracleFactory, UltimateOracleFactory


class TestModels(TestCase):

    def test_centralized_oracle(self):
        oracle = CentralizedOracleFactory()
        self.assertIsNotNone(oracle.pk)

    def test_ultimate_oracle(self):
        oracle = UltimateOracleFactory()
        self.assertIsNotNone(oracle.pk)