# PyFidelius

Python SDK for Fidelius CLI, a tool designed for ECDH cryptography.

## How to use it?

Install the package from PyPi
```bash
pip install pyfidelius
```

Create an instance of the class

```py
from pyfidelius.cryptography import Cryptography

ecdh = Cryptography()
```

**NOTE**: Make sure that JRE 1.8+ is installed, to run the binaries in the release.

Methods available :

| Method                  | Details                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `generate_key_material` | Generates an ECDH key pair, and a random nonce.                                                                    |
| `encrypt`               | Encrypts a given string of data.                                                                                      |
| `sane_encrypt`          | Same as the ncrypt command, the only difference being that it accepts a base64 encoded version of the input string. |
| `decrypt`               | Decrypt the encoded data back to the original string.                                                                  |
| `file_operation`        | ECDH Cryptography can also be applied to files for both encryption and decryption.                                  |

> A brief documentation about each method is mentioned in the method's docstring.
