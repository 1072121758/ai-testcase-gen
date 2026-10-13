class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def hello(self):
        return f"Hello, {self.name}!"

    def goodbye(self):
        return f"Goodbye, {self.name}!"