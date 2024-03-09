# this is the object that is going to be sent to the ingestion system
class Content:
    def __init__(self, class_type, obj):
        self.class_type = class_type
        self.obj = obj

    def to_json(self):
        return {
            "class_type": self.class_type,
            "obj": self.obj.to_json()
        }

    def __str__(self):
        return f"class_type: {self.class_type}, obj: {self.obj.to_json()}"
