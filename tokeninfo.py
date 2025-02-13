import requests

def get_token_info(access_token):
    tokeninfo_url = "https://oauth2.googleapis.com/tokeninfo"
    response = requests.post(tokeninfo_url, data={'access_token': access_token})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get token info. Status code: {response.status_code}, Response: {response.text}")
        return None

def main():
    # Replace 'YOUR_ACCESS_TOKEN' with the actual access token you want to inspect
    access_token = "YOUR_ACCESS_TOKEN"

    token_info = get_token_info(access_token)
    if token_info:
        print("Token Info:")
        for key, value in token_info.items():
            print(f"{key}: {value}")
        print("\nScopes: ", token_info.get('scope'))
    else:
        print("Failed to retrieve token information.")

if __name__ == "__main__":
    main()