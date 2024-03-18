import pandas as pd


class RawInputLoader:
    def __init__(self, path_to_csv):
        self.path = path_to_csv

    def load(self):
        df_array = []
        df_name = []
        # load the csv files
        for i in range(len(self.path)):
            dataframe = pd.read_csv(self.path[i])
            df_name.append(self.path[i].split("/")[-1].split(".")[0])
            df_array.append(dataframe)
        return df_array, df_name
        """
        label_df = pd.read_csv('../../data/labels.csv')
        localizationSys_df = pd.read_csv('../../data/localizationSys.csv')
        networkMonitor_df = pd.read_csv('../../data/networkMonitor.csv')
        transactionCloud_df = pd.read_csv('../../data/transactionCloud.csv')

        csvFiles = ["labels", "localizationSys", "networkMonitor", "transactionCloud"]
        pandasFiles = [label_df, localizationSys_df, networkMonitor_df, transactionCloud_df]
        return pandasFiles, csvFiles
        """

if __name__ == "__main__":
    path_to_files = ["../../data/labels.csv", "../../data/localizationSys.csv",
                     "../../data/networkMonitor.csv", "../../data/transactionCloud.csv"]
    raw_input_loader = RawInputLoader(path_to_files)
    pandasFiles, csvFiles = raw_input_loader.load()
    print(pandasFiles)
    print(csvFiles)
    print(pandasFiles[0])
    print(csvFiles[0])
    print(pandasFiles[1])
    print(csvFiles[1])
    print(pandasFiles[2])
    print(csvFiles[2])
    print(pandasFiles[3])
    print(csvFiles[3])