import requests

if __name__ == "__main__":
    email_input = input('Enter email: ')

    data = {
        'email': email_input
    }

    res = requests.post('https://voicingvault.onrender.com/grant-access', json=data)

    if res.status_code == 200:
        print('successfully updated email')
    else:
        print('there was some error')