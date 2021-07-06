import requests


# test if the input is not empty and is a number
def get_user_input():
    user_input = input("Enter a phone number: ")
    return user_input
    

def get_data_from_api(phone_number, api_key):
    # response = requests.get("https://phonevalidation.abstractapi.com/v1/?api_key=2240019ef22443bf83b96d9fc4599e31&phone=14152007986")
    abstract_api_base_url = "https://phonevalidation.abstractapi.com/v1/"
    numverify_base_url = 'http://apilayer.net/api/validate'
    # response = requests.get(abstract_api_base_url + "?api_key=" + api_key + "&phone=" + str(phone_number))
    response = requests.get(numverify_base_url + "?access_key=" + api_key + '&number=' + str(phone_number) + '&format=1')
    # response = requests.get('http://apilayer.net/api/validate?access_key=c9c53eb9e5381913088a3aaa5b6555f8&number=16156002012&format=1')
    print(response.status_code)
    print(response.content)
    

# def create_dataframe():
    


def main():
    # Abstract API key
    abstract_api_key = '2240019ef22443bf83b96d9fc4599e31'
    numverify_key = 'c9c53eb9e5381913088a3aaa5b6555f8'
    phone_number = get_user_input()
    get_data_from_api(phone_number, numverify_key)
    
if __name__ == "__main__":
    main()