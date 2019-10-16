

# Storage for user data
# In perspective will be changed to Redis
class UserStorage:

    def __init__(self):
        self.data = {}

    def data_set(self, user: str, field: str, value) -> str:
        if user in self.data:
            self.data[user][field] = value
        else:
            self.data[user] = {
                field: value
            }

    def data_get(self, user: str, field: str) -> str:
        if user in self.data and field in self.data[user]:
            return self.data[user][field]

        return ""
