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
            pk_instance = obj.id + 1
        except:
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

        return {
            "id": pk_instance,
            "email": data["email"],
            "first_name": data["first_name"],
            "phone": data["phone"],
            "date_birthday": data["date_birthday"],
            "gender": data["gender"],
            "token": token
        }

    def unique_mode(self, email, phone):
        email_field = SESSION.query(Profile).filter(BaseUser.email == email).first()
        if not email_field:
            phone_field = SESSION.query(Profile).filter(Profile.phone == phone).first()
            if not phone_field:
                return None
        else:
            return "UniqueError: email or phone fields is busy"

    def validate_mode(self, email, phone):
        unique_data = self.unique_mode(email, phone)
        if unique_data:
            return unique_data
        is_valid = validate_email(email)
        if not is_valid:
            return "TypeError: email field it should be EmailType"

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

            validation_info = self.validate_mode(data["email"], data["phone"])
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

    def authentication(self, user, password):
        if user and user.password == password:
            profile = SESSION.query(Profile).filter(Profile.user == user.id).first()
            instance = {
                "id": profile.id,
                "email": user.email,
                "token": user.token,  # TODO update token
                'first_name': profile.first_name,
                "phone": profile.phone,
                "date_birthday": str(profile.date_birthday),
                'gender': profile.gender,
            }
            return {
                "success": True,
                "data": instance
            }

        else:
            return {
                "success": False,
                "error": "AuthError"
            }

    def check_data(self, data):
        if data["email"]:
            user = SESSION.query(BaseUser).filter(BaseUser.email == data["email"]).first()

            return self.authentication(user, data["password"])

        if data["phone"]:
            profile = SESSION.query(Profile).filter(Profile.phone == data["phone"]).first()
            user = SESSION.query(Profile).get(profile.user)

            return self.authentication(user, data["password"])

        return {
            "success": False,
            "error": "Sorry, but something went wrong"
        }

    def check(self, data):
        try:
            data = {
                "email": data["email"],
                "password": General().crypt(data["password"]),
                "phone": None
            }
        except KeyError:
            data = {
                "password": General().crypt(data["password"]),
                "phone": data["phone"],
                "email": None
            }
        except:
            return {
                    "success": False,
                    "error": "one of the arguments was not passed"
                }

        instance = self.check_data(data)

        return {
                "success": True,
                "data": instance
            }