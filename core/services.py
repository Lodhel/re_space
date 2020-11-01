import datetime

from models import SESSION
from models import BaseUser, Profile


import hashlib
import uuid

from validate_email import validate_email


class General:

    def generate_id(self, model):

        try:
            obj = SESSION.query(model).all()
            obj = obj[-1]
            pk_instance = General().generate_id(obj)
        except IndexError:
            pk_instance = 0

        return pk_instance

    def generate_token(self):

        result = str(uuid.uuid4())
        return result[0:32]

    def crypt(self, main_string):
        return hashlib.sha256(main_string.encode()).hexdigest()


class UserServices:

    def create(self, data):

        pk_base_user = General().generate_id(BaseUser)
        token = General().generate_token()
        base_user = BaseUser(
            pk_base_user, token=token, password=data["password"], email=data["email"]
        )

        SESSION.add(base_user)
        SESSION.flush()

        pk_instance = General().generate_id(Profile)
        instance = Profile(
            pk_instance, pk_base_user, data["first_name"], datetime.date.today(),
            data["phone"], data["date_birthday"], data["gender"]
        )

        SESSION.add(instance)
        SESSION.flush()

        return {  # TODO I going to data
            "id": pk_instance,
            "email": data["email"],
            "first_name": data["first_name"],
            "token": token
        }

    def unique_mode(self, email):
        login_field = SESSION.query(Profile).filter(BaseUser.email == email).first()
        if not login_field:
            return None
        else:
            return "UniqueError: login fields is busy"

    def validate_mode(self, login):
        unique_data = self.unique_mode(login)
        if unique_data:
            return unique_data
        is_valid = validate_email(login)
        if not is_valid:
            return "TypeError: login field it should be EmailType"

        return None

    def save(self, data):
        try:
            data = {
                "email": data["email"],
                "password": General().crypt(data["password"]),
                'first_name': data["first_name"],
                "phone": data["phone"],
                "date_birthday": data["date_birthday"],
                'gender': data["gender"],
            }

            validation_info = self.validate_mode(data["login"])
            if validation_info:
                return {
                        "success": False,
                        "error": validation_info
                    }

        except KeyError:
            return {
                    "success": False,
                    "error": "one of the arguments was not passed"
                }

        instance = self.create(data)

        return {
                "success": True,
                "data": instance
            }