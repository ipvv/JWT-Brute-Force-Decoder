
---

# JWT Brute-Force Decoder 

A fast Python tool for checking weak or commonly used JWT (JSON Web Token) secret keys. Ideal for quick security testing, this tool helps identify easily guessable secrets for JWTs using HS256. It also decodes valid tokens, giving you an instant look at the payload.

## Features ✨

- **Quick Checks for Weak Secrets**: Scans for non-secret and popular weak keys to ensure your JWTs aren't easily cracked.
- **High-Speed Performance**: Handles large dictionaries efficiently, reaching 20,000+ attempts per second.
- **Custom Wordlist Support**: Easily add a custom dictionary file for brute-forcing.

## Requirements 🛠️

- **Python 3.x**
- **PyJWT**: Install via `pip install pyjwt[crypto]` to optimize cryptographic functions.

## Usage 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/ipvv/jwt-brute-force-decoder.git
   cd jwt-brute-force-decoder
   ```

2. Run the tool with a JWT token and optional wordlist:

   ```bash
   python3 Check-Jwt.py <jwt_token> -d /path/to/wordlist.txt
   ```

   Example:
   ```bash
   python3 Check-Jwt.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ... -d /usr/share/wordlists/rockyou.txt
   ```

## Example Output 

```plaintext
[INFO] Starting JWT secret key brute-force...

Decoding JWT:

[INFO] JWT Header:
{
  "typ": "JWT",
  "alg": "HS256"
}

[INFO] JWT Payload:
{
  "sub": "e5edac3b-82a4-5030-8fac-fe233fbba092"
}

[INFO] Using custom dictionary from '/usr/share/wordlists/rockyou.txt' with 14344392 entries.
[Verbose] Tried 2000/14344392 secrets (0.01% complete) | Speed: 20234.56 secrets/sec.
```

## Options ⚙️

- `-d, --dictionary`: Path to a custom dictionary file for testing JWT secret keys. If not provided, the tool uses a default list of common weak secrets.
