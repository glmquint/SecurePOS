class Message:
    def __init__(self, message):
        self.message = message

    def to_json(self):
        return {
            "message": self.message
        }

    def __str__(self):
        return (f"Message: {self.message}")