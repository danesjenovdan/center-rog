import requests
import xmltodict

from django.conf import settings


class PrimaApi(object):
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
            response_data = response_dict.get('responses').get('response')
            response_status = response_data['@status']
        except:
            error_message = "Error - Response data in not the correct XML format!"
            print(error_message)
            return None, error_message
        
        if response_status == '0': # successful response
            data = response_data.get('data')
            return data, "Success"
        elif response_status == '2': # session expired
            # remove token
            self.session_id = None
            # retry request
            response = self.primaRequest(payload)
            return self.primaResponse(response, payload)
        elif response_status == '15': # user already exists
            data = response_data.get('data')
            return data, "User exists"
        else: # there was an error:
            error_message = response_data.get('@message')
            print(f"Error - {error_message}")
            return None, error_message

    def primaRequest(self, payload):
        """ 
        Adds api key to request.
        """

        payload['ApiKey'] = self.api_key
        
        response = requests.get(
            self.url,
            params=payload
        )

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

        if user_id: # read specific user

            payload = {
                'Request': 'ReadUsers', 
                'Range': 'UsrID',
                'UsrID': user_id
            }

        elif user_login_name: # filter users by login name

            payload = {
                'Request': 'ReadUsers',
                'Range': 'All-preview',
                'FilterFields': 'UsrLoginName',
                'Filter': user_login_name,
            }
        
        else: # read all users

            payload = {
                'Request': 'ReadUsers', 
                'Range': 'All-preview',
            }

        data, message = self.primaRequest(payload)

        return data, message
    
    def createUser(self, email):
        """ 
        Create user in Prima system.
        """

        payload = {
            'Request': 'CreateUser', 
            # 'UsrName': name,
            # 'UsrLastName': lastname,
            'UsrAccessLevel': '5', # UsrAccessLevel=5 pomeni omejen dostop do requestov
            'UsrLoginName': email,
            'UsrEMail': email,
            # 'UsrPhone': phone
        }

        print("Create user", payload)

        data, message = self.primaRequest(payload)

        # WARNING this code contains assumptions
        if message == 'User exists':
            existing_user = self.readUsers(user_login_name=email)
            
            # finally, remove all the @ signs from the beginning of keys
            data = {key[1:]: value for key, value in existing_user[0].get('user', {}).items()}

        return data, message
    
    def updateUser(self, user_id, name, last_name):
        """ 
        TODO
        """

        payload = {
            'Request': 'UpdateUser', 
            'UsrID': user_id,
            'UsrName': name,
            'UsrLastName': last_name,
        }

        data, message = self.primaRequest(payload)

        return data, message
    
    def deleteUser(self, user_id):
        """ 
        ...
        """

        payload = {
            'Request': 'DeleteUser', 
            'UsrID': user_id,
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

        payload = {
            'Request': 'ReadUserBalances',
            'Range': 'UsrID',
            'UsrID': user_id
        }

        data, message = self.primaRequest(payload)

        return data, message
    
    def updateUserBalance(self, user_id):
        """ 
        TODO
        """

        payload = {
            'Request': 'UpdateUserBalance',
            'UsrID': user_id
        }

        data, message = self.primaRequest(payload)

        return data, message
