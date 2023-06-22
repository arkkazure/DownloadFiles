#https://the-internet.herokuapp.com/download/path.txt
import requests


def test_down():
    url = "https://the-internet.herokuapp.com/download/boy.jpg"
    file_path = "boy.jpg"

    response = requests.get(url)
    response = requests.get(url, auth=('user', 'sdsd'))

    with open(file_path, "wb") as file:
        file.write(response.content)

    print("File downloaded successfully.")
