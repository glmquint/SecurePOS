from unittest import TestCase

from src.Development.DevelopmentSystemMasterOrchestrator import DevelopmentSystemMasterOrchestrator


class TestDevelopmentSystemMasterOrchestrator(TestCase):
    def test_start(self):
        ds = DevelopmentSystemMasterOrchestrator()
        ds.start()


