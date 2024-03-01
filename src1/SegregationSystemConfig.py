class SegregationSystemConfig:
    sufficientSessionNumber = 0
    messageSystemIp = 0
    messageSystemPort = 0
    segregationSystemIp = 0
    segregationSystemPort = 0
    developmentSystemIp = 0
    developmentSystemPort = 0
    toleraceDataBalancing = 0

    def __init__(self,
                 sufficientSessionNumber ,
                 messageSystemIp ,
                 messageSystemPort ,
                 segregationSystemIp ,
                 segregationSystemPort ,
                 developmentSystemIp ,
                 developmentSystemPort,
                 toleraceDataBalancing):
        self.sufficientSessionNumber = sufficientSessionNumber
        self.messageSystemIp = messageSystemIp
        self.messageSystemPort = messageSystemPort
        self.segregationSystemIp = segregationSystemIp
        self.segregationSystemPort = segregationSystemPort
        self.developmentSystemIp = developmentSystemIp
        self.developmentSystemPort = developmentSystemPort
        self.toleraceDataBalancing = toleraceDataBalancing







