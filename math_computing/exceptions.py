class MultiMathWorkRequest(Exception):
    def __init__(self, message='you cant execute multiple tasks in one time!'):
        self.message = message

    def __str__(self):
        return self.message
