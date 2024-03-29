import os
from unittest import TestCase

from src.DataObjects.LearningSet import LearningSet
from src.Development.DevelopmentSystemMasterOrchestrator import DevelopmentSystemMasterOrchestrator
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus


class TestDevelopmentSystemMasterOrchestrator(TestCase):
    """
    A class used to test the DevelopmentSystemMasterOrchestrator class in the development system.

    Methods
    -------
    test_start(self)
        Tests the start method of the DevelopmentSystemMasterOrchestrator class.
    """
    # class implementation...class
    # TestDevelopmentSystemMasterOrchestrator(TestCase):

    def test_start(self):
        status = DevelopmentSystemStatus(
            f"{os.path.dirname(__file__)}/development_system_status.json",
            f"{os.path.dirname(__file__)}/schema/status_schema.json")
        status.load_status()
        status.status = "pop_learning_set"
        ls_json = {
            "trainingSet": {
                "index": [0, 1, 2, 3, 4, 5],
                "columns": ["median_latitude", "mean_abs_diff_transaction", "median_longitude", "median_target_ip", "mean_abs_diff_transaction_amount", "median_dest_ip"],
                "data": [
                    [39.24486913139725, 29.88888888888889, -30.968318264156352, 4194914035, 18.333333333333332, 2635807090],
                    [-46.24506015397818, 31.666666666666668, 121.43238329449372, 2565504486, 29.11111111111111, 3401492641],
                    [82.35870237955396, 41.0, 94.35881996625989, 995937603, 38.333333333333336, 1898141033],
                    [64.9881861133538, 23.444444444444443, -140.77902563924897, 295323626, 31.333333333333332, 936403347],
                    [-37.19956216614031, 27.0, 39.620514509489965, 681843004, 42.22222222222222, 4103536396],
                    [80.15615489687869, 20.444444444444443, 38.0359539962264, 4013595675, 32.333333333333336, 3543876851]
                ]
            },
            "validationSet": {
                "index": [0, 1],
                "columns": ["median_latitude", "mean_abs_diff_transaction", "median_longitude", "median_target_ip", "mean_abs_diff_transaction_amount", "median_dest_ip"],
                "data": [
                    [31.95266336397235, 25.0, -136.16112874710458, 3321361469, 46.333333333333336, 3871635404],
                    [-76.3063847935743, 28.555555555555557, 99.86064464149018, 4010505449, 35.0, 4106928960]
                ]
            },
            "testSet": {
                "index": [0, 1],
                "columns": ["median_latitude", "mean_abs_diff_transaction", "median_longitude", "median_target_ip", "mean_abs_diff_transaction_amount", "median_dest_ip"],
                "data": [
                    [44.190695743732505, 31.444444444444443, -132.73345323179166, 15867286, 31.0, 1010313832],
                    [83.3818041887979, 32.0, -26.48460882435856, 1824007236, 39.666666666666664, 1773872383]
                ]
            },
            "trainingSetLabel": ["moderate", "moderate", "moderate", "moderate", "normal", "moderate"],
            "validationSetLabel": ["moderate", "high"],
            "testSetLabel": ["normal", "moderate"]
        }
        ls = LearningSet(ls_json, True)
        ds = DevelopmentSystemMasterOrchestrator(status)
        ds.message_bus.pushTopic("LearningSet", ls)
        ds.start()
        assert (ds.status.status ==
                "send_to_production" or ds.status.status == "send_to_messaging")
