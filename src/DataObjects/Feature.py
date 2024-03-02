
class Feature:
    pass

class MeanAbsDiffTransaction(Feature):
    time_diff: int
    pass

class MeanAbsDiffTransactionAmount(Feature):
    amount:int
    pass

class MedianLongitudeLatitude(Feature):
    geo_position:(float, float)
    pass

class MedianTargetIP(Feature):
    median_ip:str
    pass

class MedianDestIP(Feature):
    median_dest_ip:str
    pass