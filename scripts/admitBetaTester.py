import requests

if __name__ == "__main__":

    data = {
        'email': "mbkeating316@gmail.com"
    }

    res = requests.post('http://localhost:8000/grant-access', json=data)

    if res.status_code == 200:
        print('successfully updated email')
    else:
        print('there was some error')