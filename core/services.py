

class UserServices:
    def save(self, data):
        return {
            "phone": data["phone"],
            "email": data["email"],
            "first_name": data["first_name"]
        }