import jwt
import sys
import argparse
import time
import json

# Color codes for styling the output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD_WHITE = "\033[1;37m"
RESET = "\033[0m"

# Default list of weak secrets
default_weak_secrets = [
    "", "secret", "password", "123456", "jwtsecret", "admin", "password1",
    "letmein", "welcome", "123456789", "12345", "qwerty", "123123",
    "password123", "jwt_token_secret", "supersecret", "jwtsecretkey",
    "1234", "123", "guest", "pass", "root", "toor", "token", "access",
    "auth", "authorization", "apitoken", "api_key", "123qwe", "qwe123",
    "test", "testing", "default", "login", "changeme", "temp", "temporary",
    "system", "abc123", "0000", "abcd", "abcd1234", "xyz", "xyz123",
    "master", "manager", "token123", "mysecret", "private", "key",
    "key123", "secure", "unlock", "letmein123", "admin123", "user",
    "system", "session", "adminadmin", "dev", "developer", "production",
    "prod", "test123", "temporary123", "jwt", "jwt123", "secretkey",
    "tokenkey", "security", "mypass", "mypassword", "service", "password!",
    "pass1234", "letmein!", "access123", "authkey", "securitykey",
    "password2022", "password2023", "testpassword", "token_secret",
    "project", "newpassword", "mypassword123", "masterkey", "companyname",
    "organization", "development", "mykey", "token_password", "secrettoken",
    "sessiontoken", "testuser", "superuser", "newtoken", "s3cr3t",
    "passw0rd", "pa$$w0rd", "myp@ssword", "pa55word", "s3cret", "jwt!secret",
    "p@ssword", "P@ssw0rd!", "password@123", "q1w2e3r4", "1qaz2wsx",
    "mysecretpassword", "trustno1", "open sesame", "god", "login123",
    "hunter2", "letmein2", "nothing", "iamadmin", "rootroot"
]

def load_secrets_from_file(filepath):
    try:
        with open(filepath, 'r', encoding="ISO-8859-1") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{RED}[-] File not found: {filepath}{RESET}")
        sys.exit(1)

def attempt_decode(token, secret):
    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        return (True, secret, decoded)
    except jwt.InvalidSignatureError:
        return (False, None, None)
    except jwt.DecodeError:
        print(f"{RED}[-] Invalid JWT format. Ensure the token is correctly formatted.{RESET}")
        sys.exit(1)

def decode_jwt_with_weak_secrets(token, weak_secrets):
    start_time = time.time()
    total_secrets = len(weak_secrets)
    attempts = 0

    try:
        for secret in weak_secrets:
            success, secret_used, decoded = attempt_decode(token, secret)
            attempts += 1

            # Print progress every 2000 attempts to improve speed
            if attempts % 2000 == 0:
                elapsed_time = time.time() - start_time
                speed = attempts / elapsed_time
                percent_complete = (attempts / total_secrets) * 100
                print(f"\r{YELLOW}[Verbose] Tried {attempts}/{total_secrets} secrets "
                      f"({percent_complete:.2f}% complete) | Speed: {speed:.2f} secrets/sec.{RESET}", end="", flush=True)

            if success:
                print(f"\n{GREEN}[+] Valid JWT Secret Key Found!{RESET}")
                print(f"{GREEN}Secret Key: '{secret_used}'{RESET}")
                print(f"{GREEN}Decoded JWT Payload: {decoded}{RESET}")
                return True

    except KeyboardInterrupt:
        print(f"\n{RED}[INFO] Process interrupted by user. Exiting...{RESET}")
        sys.exit(0)

    print(f"{RED}\n[-] No valid weak or empty secret key found.{RESET}")
    print(f"{BLUE}[INFO] You can try a custom wordlist with the -d option for more extensive testing.{RESET}")
    return False

def display_jwt_content(token):
    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})
        print(f"{YELLOW}Decoding JWT:{RESET}\n")
        print(f"{BOLD_WHITE}[INFO] JWT Header:{RESET}\n\n{json.dumps(header, indent=2)}\n")
        print(f"{BOLD_WHITE}[INFO] JWT Payload:{RESET}\n\n{json.dumps(payload, indent=2)}\n")
    except jwt.DecodeError:
        print(f"{RED}[-] Could not decode JWT. Please check the token format.{RESET}")
        sys.exit(1)

# Set up argument parsing
parser = argparse.ArgumentParser(description="Decode JWT with weak or custom secret keys.")
parser.add_argument("token", help="The JWT token to decode.")
parser.add_argument("-d", "--dictionary", help="Path to a custom wordlist file for secret keys.", type=str)
args = parser.parse_args()

# Display decoded JWT content at start
print("\n\n")
display_jwt_content(args.token)
print(f"\n{BLUE}[INFO] Starting JWT secret key brute-force...{RESET}")

# Load weak secrets based on the argument
if args.dictionary:
    weak_secrets = load_secrets_from_file(args.dictionary)
    print(f"{YELLOW}[INFO] Using custom dictionary from '{args.dictionary}' with {len(weak_secrets)} entries.{RESET}")
else:
    print(f"{YELLOW}[INFO] Attempting default weak secrets with {len(default_weak_secrets)} entries.{RESET}")
    weak_secrets = default_weak_secrets

# Run the brute-force decoding
if decode_jwt_with_weak_secrets(args.token, weak_secrets):
    print(f"\n{GREEN}[SUCCESS] The JWT token has a weak or empty secret key.{RESET}")
else:
    print(f"\n{RED}[INFO] The JWT token does not have a weak or empty secret key.{RESET}")
