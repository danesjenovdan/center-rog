import requests
import xmltodict

from django.conf import settings


class PrimaApi(object):
    def __init__(self, username=settings.PRIMA_USERNAME, password=settings.PRIMA_PASSWORD, url=settings.PRIMA_URL):
        self.username = username
        self.password = password
        self.url = url
        self.session_id = None # Session ID is needed for all other API calls

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

        # get response in text
        response_text = response.text

        # parse xml to dict
        try:
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
        else: # there was an error:
            error_message = response_data.get('@message')
            print(f"Error - {error_message}")
            return None, error_message

    def login(self):
        """ 
        Login to acquire session ID.
        """

        payload = {
            'Request': 'LoginUser', 
            'UsrName': self.username,
            'UsrPassword': self.password
        }

        r = requests.get(self.url, params=payload)

        data, message = self.primaResponse(r, payload)

        if data:
            self.session_id = data['SessionID']
            print("Successful login")
            return data['UsrID']

        else:
            print('Error at login', message)
            return

    def primaRequest(self, payload):
        """ 
        Adds session ID to request.
        If there is no session ID, first call login().
        """

        # if session id does not exist yet
        if not self.session_id:
            logged_in = self.login()
            if not logged_in:
                print("Error - login request failed")
                return

        payload['SessionID'] = self.session_id
        
        response = requests.get(
            self.url,
            params=payload
        )

        return self.primaResponse(response, payload)

    ### USERS CRUD
    
    def readUsers(self, user_id=None):
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
        
        else: # read all users

            payload = {
                'Request': 'ReadUsers', 
                'Range': 'All-preview',
            }

        data, message = self.primaRequest(payload)

        return data, message
    
    def createUser(self, name, lastname, username, email, phone):
        """ 
        ...
        """

        payload = {
            'Request': 'CreateUser', 
            'UsrName': name,
            'UsrLastName': lastname,
            'UsrAccessLevel': '5', # UsrAccessLevel=5 pomeni omejen dostop do requestov
            'UsrLoginName': username,
            'UsrEMail': email,
            'UsrPhone': phone
        }

        print("Create user", payload)

        data, message = self.primaRequest(payload)

        return data, message
    
    def updateUser(self, user_id):
        """ 
        TODO
        """

        payload = {
            'Request': 'UpdateUser', 
            'UsrID': user_id,
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
