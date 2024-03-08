# this is the object that is going to be sent to the ingestion system
class Content:
    def __init__(self, content, obj):
        self.content = content
        self.obj = obj

    def to_json(self):
        return {
            "content": self.content,
            "obj": self.obj.to_json()
        }

    def __str__(self):
        return f"content: {self.content}, obj: {self.obj.to_json()}"
