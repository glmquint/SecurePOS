
class Feature:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_json(self):
        return self.__dict__

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

class AttackRiskLabel(Feature):
    attack_risk_label: str
    pass