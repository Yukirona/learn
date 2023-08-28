import requests
import json

def O_token():
    # Set the API endpoint URL
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/auth/tokens"

    # Set the request payload
    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "eric.bonnet1",
                        "password": "!8e7gpSfcb/74UB",
                        "domain": {
                            "name": "OCB0002982"
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": "eu-west-0"
                }
            }   
        }

    }

    print("--------------start token accquisition--------------------------------")
    # Make the API request to obtain the authentication token
    response = requests.post(api_endpoint, json=payload)
    
    # Check the response status
    if response.status_code == 201:
        # Get the authentication token from the response headers
        auth_token = response.headers.get("X-Subject-Token")
        # Store the authentication token in a file
        with open("auth_token.txt", "w") as token_file:
            token_file.write(auth_token)
            #print("Authentication token stored successfully.")
            print("--------------end token accquisition--------------------------------")
    else:
        print("Error occurred while retrieving the authentication token.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    
    return auth_token

    pass


def O_token_domain():
    # Set the API endpoint URL
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/auth/tokens"

    # Set the request payload
    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "eric.bonnet1",
                        "password": "!8e7gpSfcb/74UB",
                        "domain": {
                            "name": "OCB0002982"
                        }
                    }
                }
            },
            "scope": {
                "domain": {
                "name": "OCB0002982"
                }
            }   
        }

    }

    print("--------------start token accquisition--------------------------------")
    # Make the API request to obtain the authentication token
    response = requests.post(api_endpoint, json=payload)
    
    # Check the response status
    if response.status_code == 201:
        # Get the authentication token from the response headers
        auth_token = response.headers.get("X-Subject-Token")
        # Store the authentication token in a file
        with open("auth_token.txt", "w") as token_file:
            token_file.write(auth_token)
            #print("Authentication token stored successfully.")
            print("--------------end token accquisition--------------------------------")
    else:
        print("Error occurred while retrieving the authentication token.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    
    return auth_token

    pass

def check_token():

    # Read the stored token from the file
    with open("auth_token.txt", "r") as token_file:
        auth_token = token_file.read().strip()

    # Set the API endpoint URL for token validation
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/auth/tokens"

    # Set the headers with the authentication token
    headers = {
        "X-Auth-Token": auth_token
    }

    # Make the API request to validate the token
    response = requests.get(api_endpoint, headers=headers)

    # Check the response status
    if response.status_code == 200:
        # Get the token expiration date from the response headers
        expiration_date_str = response.headers.get("X-Subject-Token-Expires-At")
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_date = datetime.now()

        # Check if the token is still valid
        if current_date < expiration_date:
            print("Token is still valid.")
        else:
            print("Token has expired.")
    else:
        print("Error occurred while validating the token.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)




        