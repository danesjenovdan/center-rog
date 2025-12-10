import requests
import xmltodict

from datetime import datetime
from enum import Enum

from django.conf import settings


class PrimaApi(object):
    class SubscriptionGroupsEnum(Enum):
        MEMBER = 100
        MONTHLY = 101
        YEARLY = 102

    def __init__(self, api_key=settings.PRIMA_API_KEY, url=settings.PRIMA_URL):
        self.api_key = api_key
        self.url = url

    ### REQUEST AND RESPONSE PROCESSING

    def primaResponse(self, response, payload):
        """
        Parses general response from Prima server.
        Returns data, message.
        """

        error_message = ""

        if not response:
            error_message = "Error - cannot process response."
            return None, error_message

        # parse xml to dict
        try:
            # get response in text
            print("prima response", response, response.text)
            response_text = response.text
            response_dict = xmltodict.parse(response_text)
        except:
            error_message = "Error - Response could not be parsed to XML!"
            print(error_message)
            return None, error_message

        try:
            response_data = response_dict.get("responses").get("response")
            response_status = response_data["@status"]
        except:
            error_message = "Error - Response data in not the correct XML format!"
            print(error_message)
            return None, error_message

        if response_status == "0":  # successful response
            data = response_data.get("data")
            return data, "Success"
        elif response_status == "2":  # session expired
            # remove token
            self.session_id = None
            # retry request
            response = self.primaRequest(payload)
            return self.primaResponse(response, payload)
        elif response_status == "15":  # user already exists
            data = response_data.get("data")
            return data, "User exists"
        else:  # there was an error:
            error_message = response_data.get("@message")
            print(f"Error - {error_message}")
            return None, error_message

    def primaRequest(self, payload):
        """
        Adds api key to request.
        """

        payload["ApiKey"] = self.api_key

        response = requests.get(self.url, params=payload)

        return self.primaResponse(response, payload)

    ### USERS CRUD

    def readUsers(self, user_id=None, user_login_name=None):
        """
        Returns user data:
        { 'user': {
            '@UsrID': '5',
            '@UsrName': 'Janez',
            '@UsrLastName': 'Novak',
            '@UsrPhone': '0038640111111',
            '@UsrEMail': 'jn@test.si',
            '@UsrOfflineScheduleID': '1',
            '@UsrLanguage': 'en_US',
            '@UsrAccessLevel': '5',
            '@UsrValidFrom': '2000-01-01 12:00:00',
            '@UsrValidTo': '2035-01-01 12:00:00',
            '@UsrLoginName': 'jn@test.si'
          }
        }
        """

        if user_id:  # read specific user

            payload = {"Request": "ReadUsers", "Range": "UsrID", "UsrID": user_id}

        elif user_login_name:  # filter users by login name

            payload = {
                "Request": "ReadUsers",
                "Range": "All-preview",
                "FilterFields": "UsrLoginName",
                "Filter": user_login_name,
            }

        else:  # read all users

            payload = {
                "Request": "ReadUsers",
                "Range": "All-preview",
            }

        data, message = self.primaRequest(payload)

        return data, message

    def createUser(self, email):
        """
        Create user in Prima system.
        """

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "Request": "CreateUser",
            # 'UsrName': name,
            # 'UsrLastName': lastname,
            "UsrAccessLevel": "5",  # UsrAccessLevel=5 pomeni omejen dostop do requestov
            "UsrLoginName": email,
            "UsrEMail": email,
            # 'UsrPhone': phone
            "UsrValidFrom": now,
            "UsrValidTo": now,
        }

        print("Create user", payload)

        data, message = self.primaRequest(payload)

        # WARNING this code contains assumptions
        if message == "User exists":
            existing_user = self.readUsers(user_login_name=email)

            # finally, remove all the @ signs from the beginning of keys
            data = {
                key[1:]: value
                for key, value in existing_user[0].get("user", {}).items()
            }

        return data, message

    def updateUser(self, user_id, name, last_name, valid_from, valid_to):
        """
        TODO
        """

        payload = {
            "Request": "UpdateUser",
            "UsrID": user_id,
            "UsrName": name,
            "UsrLastName": last_name,
            "UsrValidFrom": valid_from,
            "UsrValidTo": valid_to,
        }

        data, message = self.primaRequest(payload)

        return data, message

    def deleteUser(self, user_id):
        """
        ...
        """

        payload = {
            "Request": "DeleteUser",
            "UsrID": user_id,
        }

        data, message = self.primaRequest(payload)

        return data, message

    def setPrimaDates(self, user_id, valid_from, valid_to):
        payload = {
            "Request": "UpdateUser",
            "UsrID": user_id,
            # 'UsrValidFrom': valid_from, # disable setting valid from date
            "UsrValidTo": valid_to,
        }

        data, message = self.primaRequest(payload)

        return data, message

    ### BOOKINGS

    def readUserBalances(self, user_id):
        """
        Returns user balance data:
        data = { 'balance': [
            {'@WltID': '1', '@WltTitle': 'Ure za CNC'},
            {'@WltID': '2', '@WltTitle': 'Ure za Stroje'},
            {'@WltID': '4', '@WltTitle': 'Ure za laser'},
            {'@WltID': '5', '@WltTitle': 'Digitalni tiskalnik za tekstil'},
            {'@WltID': '6', '@WltTitle': '3D printer za keramiko'}
            ]
        },
        message = 'Success'
        """

        payload = {"Request": "ReadUserBalances", "Range": "UsrID", "UsrID": user_id}

        data, message = self.primaRequest(payload)

        return data, message

    def updateUserBalance(self, user_id):
        """
        TODO
        """

        payload = {"Request": "UpdateUserBalance", "UsrID": user_id}

        data, message = self.primaRequest(payload)

        return data, message

    def addTokensToUserBalance(self, user_id, tokens):
        """
        Adds tokens to user balance for WltID = 8 (Enkratni obisk).
        """

        payload = {
            "Request": "UpdateUserBalance",
            "UsrID": user_id,
            "WltID": 8,  # WltID Enkratni obisk = 8
            "AddBalance": tokens,
        }

        data, message = self.primaRequest(payload)

        return data, message

    def addUserToSubscriptionGroup(self, user_id, group_id):
        """
        Adds user to subscription group.

        """

        payload = {
            "Request": "CreateUsersList",
            "UsrID": user_id,
            "LstID": group_id,
        }

        data, message = self.primaRequest(payload)

        for group in PrimaApi.SubscriptionGroupsEnum:
            if group.value == group_id:
                continue
            group_id = group.value
            payload = {
                "Request": "DeleteUsersList",
                "UsrID": user_id,
                "LstID": group_id,
            }
            data, message = self.primaRequest(payload)

        return data, message
    
    def removeUserFromSubscriptionGroup(self, user_id, group_id):
        """
        Adds user to subscription group.

        """
        payload = {
            "Request": "DeleteUsersList",
            "UsrID": user_id,
            "LstID": group_id,
        }
        data, message = self.primaRequest(payload)

        return data, message