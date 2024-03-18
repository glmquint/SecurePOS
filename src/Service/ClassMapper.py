from src.DataObjects.Label import Label
from src.DataObjects.LocalizationSys import LocalizationSys
from src.DataObjects.NetworkMonitor import NetworkMonitor
from src.DataObjects.TransactionCloud import TransactionCloud


class ClassMapper:
    def __init__(self):
        pass

    @staticmethod
    def map_to_class(chosen_df_name, dict1):
        if chosen_df_name == 'labels':
            mapped_class = Label(dict1['UUID'], dict1['LABEL'])
        elif chosen_df_name == 'localizationSys':
            # Assuming you have a class called LocalizationSys
            mapped_class = LocalizationSys(dict1['UUID'], dict1['longitude'],
                                           dict1['latitude'])
        elif chosen_df_name == 'networkMonitor':
            # Assuming you have a class called NetworkMonitor
            mapped_class = NetworkMonitor(dict1['UUID'], dict1['targetIP'],
                                          dict1['destIP'])
        elif chosen_df_name == 'transactionCloud':
            # Assuming you have a class called TransactionCloud
            mapped_class = TransactionCloud(dict1['UUID'], dict1['ts'],
                                            dict1['am'])
        return mapped_class