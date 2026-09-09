# cryptography — encryption, hashing, and signatures

> `cryptography` is the standard, actively-audited library for real crypto
> in Python. It exposes a safe "recipes" layer (`Fernet`) for common cases,
> plus lower-level primitives for when you need them.

## Install

```bash
python -m pip install cryptography
```

## symmetric encryption with Fernet

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()          # store this, do not hardcode it
f = Fernet(key)

token = f.encrypt(b"the message")
print(f.decrypt(token))              # b"the message"
```

`Fernet` bundles AES-128 encryption with a message authentication code and
a timestamp — it is the right default for "encrypt this blob" unless you
have a specific reason to need something else. Never reuse a key across
unrelated applications, and never commit a key to source control.

## hashing (not for passwords)

```python
from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256())
digest.update(b"some file contents")
print(digest.finalize().hex())
```

Anything under `cryptography.hazmat` is a low-level primitive: powerful,
but easy to misuse. Plain SHA-256 is fine for checksums and integrity
checks — it is **not** safe for hashing passwords (no salt, too fast to
brute-force). Use a password-hashing library (`argon2-cffi`, `bcrypt`,
or `hashlib.scrypt`) for that instead.

## password-based key derivation

```python
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

salt = os.urandom(16)   # store alongside the derived output, per user
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
key = kdf.derive(b"user password")
```

A unique, random salt per secret is what stops precomputed rainbow-table
attacks — never reuse a salt across users, and never derive a key from a
password without one.

## verifying a digital signature

```python
from cryptography.hazmat.primitives.asymmetric import ed25519

private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

signature = private_key.sign(b"payload to authenticate")
public_key.verify(signature, b"payload to authenticate")  # raises if invalid
```

`verify` raises `InvalidSignature` rather than returning `False` — wrap it
in a `try/except` rather than checking a return value.

## Safety notes

Use the high-level recipes (`Fernet`, `ChaCha20Poly1305`) unless you have a
concrete, informed reason to reach for raw primitives. Never invent your
own cipher mode, never encrypt without authentication, and keep keys in a
secret manager or environment variable — never in source control.

Next door: [python-dotenv](079-python-dotenv.md) for keeping secrets out
of code, and [pydantic](080-pydantic.md) for validating the config that
often surrounds credential handling.
