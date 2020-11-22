import datetime
import re

from models import SESSION
from models import BaseUser, Profile, CategoryItem, Location, Item, Food, FriendList


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


class ItemService:

    def save(self, data, pk):
        instance = Item(
            id=pk, article=data["article"], category=data["category"], location=data["location"],
            attribute=data["attribute"], title=data["title"]
        )

        SESSION.add(instance)
        SESSION.flush()

    def get(self):
        data = SESSION.query(Item).all()
        instance = [{
            "id": item.id,
            "category": item.category,
            "location": item.location,
            'title': item.title,
            "article": item.article,
            "attribute": item.attribute
        } for item in data]
        return {
            "success": True,
            "data": instance
        }


class FoodServices:

    def save(self, data, pk, item):
        instance = Food(
            id=pk, item=item, user=data["user"], date_start=data["date_start"],
            date_end=data["date_end"], status=data["status"], amount=data["amount"], measure=data["measure"]
        )

        SESSION.add(instance)
        SESSION.flush()

    def get_or_create_category_for_item(self):
        category = SESSION.query(CategoryItem).filter(CategoryItem.title == "food").first()
        if not category:
            category = General().generate_id(CategoryItem)
            instance = CategoryItem(category, "food")

            SESSION.add(instance)
            SESSION.flush()

            return category

        return category.id

    def get_or_create_location(self):
        location = SESSION.query(Location).filter(Location.title == "cafe").first()
        if not location:
            location = General().generate_id(Location)
            instance = Location(id=location, title="cafe", article="add be later")

            SESSION.add(instance)
            SESSION.flush()

            return location

        return location.id

    def create(self, data):
        if not SESSION.query(Profile).get(data["user"]):
            return {
                "success": False,
                "error": "UserNotFound"
            }
        data["location"] = self.get_or_create_location()
        data["category"] = self.get_or_create_category_for_item()
        item = General().generate_id(Item)
        ItemService().save(data, item)
        pk_food = General().generate_id(Food)
        self.save(data, pk_food, item)

        instance_item = {
            "id": item,
            "category": data["category"],
            "location": data["location"],
            'title': data["title"],
            "article": data["article"],
            "attribute": data["attribute"]
        }

        instance_food = {
            "id": pk_food,
            "item": item,
            "user": data["user"],
            "date_start": data["date_start"],
            "date_end": data["date_end"],
            "status": data["status"],
            "amount": data["amount"],
            "measure": data["measure"]
        }

        return {
            "success": True,
            "data": {
                "item": instance_item,
                "food": instance_food
            }
        }


class FriendService:

    def streamline(self, string):
        array = string.split(', ')
        return [int(pk) for pk in array]

    def validate(self, data):
        if not SESSION.query(Profile).get(data["user"]):
            return {
                "success": False,
                "error": "UserNotFound"
            }

        if data["user"] == data["friend"]:
            return {
                "success": False,
                "error": "UserIsFriend"
            }

        return None

    def get(self, data):
        return {
            "success": True,
            "data": self.streamline(SESSION.query(FriendList).filter(FriendList.user == data["user"]).first())
        }

    def delete(self, data):
        validation_case = self.validate(data)
        if validation_case:
            return validation_case

        friend_list = SESSION.query(FriendList).filter(FriendList.user == data["user"]).first()
        if not friend_list and int(data["friend"]) not in self.streamline(friend_list):
            return {
                "success": False,
                "error": "NotFound"
            }

        array = self.streamline(friend_list.array)
        string_array = ""

        for index, friend in enumerate(array):
            if friend == data["friend"]:
                del array[index]
            else:
                "{}, {}".format(string_array, friend)

        friend_list.array = string_array

        SESSION.add(friend_list)
        SESSION.flush()

        return {
            "success": True,
            "data": {
                "user": data["user"],
                "list": array
            }
        }

    def add(self, data):
        if data["command"] == "get":
            return self.get(data)
        if data["command"] == "delete":
            return self.delete(data)
        validation_case = self.validate(data)
        if validation_case:
            return validation_case

        pk = General().generate_id(FriendList)
        friend_list = SESSION.query(FriendList).filter(FriendList.user == data["user"]).first()

        if not friend_list:
            instance = FriendList(pk, user=data["user"], array=data["friend"])

            SESSION.add(instance)
            SESSION.flush()

            return {
                "success": True,
                "data": {
                    "id": pk,
                    "user": data["user"],
                    "list": data["friend"]
                }
            }

        if data["friend"] in self.streamline(friend_list.aray):
            return {
                "success": False,
                "error": "FriendAddedList"
            }

        array = "{}, {}".format(friend_list.array, data["friend"])
        friend_list.array = array

        SESSION.add(friend_list)
        SESSION.flush()

        return {
            "success": True,
            "data": {
                "id": pk,
                "user": data["user"],
                "list": self.streamline(array)
            }
        }