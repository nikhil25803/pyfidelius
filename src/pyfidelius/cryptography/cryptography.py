import re
import os
import json
import base64
import logging
import platform
import subprocess
from typing import List
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)],
)
log = logging.getLogger("rich")


class Cryptography:
    """
    Class responsible for different operations like encoding, decoding, etc.

    Create an instance of the class
    ```py
    from pyfidelius.cryptography import Cryptography

    ecdh = Cryptography()
    ```

    Methods available :

    | Method                        | Details                                                               |
    | ----------------------------- | --------------------------------------------------------------------- |
    | `generate_key_material` | Generates an ECDH key pair, and a random nonce.|
    """

    def __init__(self) -> None:
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.abspath(os.path.join(current_file_path, "..", ".."))

        os_platform = platform.system()

        if os_platform == "Windows":
            script_path = os.path.join(
                root_path, "fidelius-cli-1.2.0", "bin", "fidelius-cli.bat"
            )
        else:
            script_path = os.path.join(
                root_path, "fidelius-cli-1.2.0", "bin", "fidelius-cli"
            )

        self.SCRIPT_PATH = script_path

    def __execute_cli_commands(self, args: List[str]) -> str:
        """
        Executes CLI commands based on the arguments passed in a list.
        """
        command_to_execute = [self.SCRIPT_PATH] + args

        result = subprocess.run(
            command_to_execute,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
        )

        if result.returncode != 0:
            raise Exception(f"Command failed with error: {result.stderr}")

        return result.stdout

    def __parse_output_to_dict(self, output: str) -> dict:
        """
        Parses the JSON-like output from the CLI command and converts it to a dictionary.
        """
        pattern = r"\{.*?\}"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            json_str = match.group(0)
            data_dict = json.loads(json_str)
            return data_dict
        else:
            raise ValueError("No valid JSON content found in the output")

    def __isBase64(self, value):
        try:
            if isinstance(value, str):
                sb_bytes = bytes(value, "ascii")
            elif isinstance(value, bytes):
                sb_bytes = value
            else:
                raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
        except Exception:
            return False

    def generate_key_material(self) -> dict:
        """
        Generates an ECDH key pair, and a random nonce.
        """
        try:
            output = self.__execute_cli_commands(["gkm"])
            key_materials = self.__parse_output_to_dict(output)
            return key_materials
        except Exception as e:
            log.error("Unable to generate key materials.\nError: ", e)
            return None

    def encrypt(
        self,
        string_to_encrypt,
        sender_nonce,
        requester_nonce,
        sender_private_key,
        requester_private_key,
    ):
        """
        Encrypts a given string data.

        Arguments:
        - `string_to_encrypt`: The string data to be encrypted.
        - `sender_nonce`: The nonce (number used once) of the sender for encryption.
        - `requester_nonce`: The nonce of the requester for encryption.
        - `sender_private_key`: The private key of the sender for encryption.
        - `requester_private_key`: The private key of the requester for encryption.

        Response:
        ```json
        {
            "encryptedData": "pzMvVZNNVtJzqPkkxcCbBUWgDEBy/mBXIeT2dJWI16ZAQnnXUb9lI+S4k8XK6mgZSKKSRIHkcNvJpllnBg548wUgavBa0vCRRwdL6kY6Yw=="
        }
        """
        try:
            if not all(
                map(
                    self.__isBase64,
                    [
                        sender_nonce,
                        requester_nonce,
                        sender_private_key,
                        requester_private_key,
                    ],
                )
            ):
                log.warning(
                    "sender_nonce, requester_nonce, sender_private_key, and requester_private_key must be base64 encoded"
                )
                return None
            output = self.__execute_cli_commands(
                [
                    "e",
                    string_to_encrypt,
                    sender_nonce,
                    requester_nonce,
                    sender_private_key,
                    requester_private_key,
                ]
            )

            encrypted_data = self.__parse_output_to_dict(output)
            return encrypted_data

        except Exception as e:
            log.error("Unable to encrypt message.\nError: ", e)
            return None


ecdh = Cryptography()
key_materials = ecdh.generate_key_material()
print("Key Material: \n", key_materials)
encodeed_data = ecdh.encrypt(
    string_to_encrypt="Wormtail should never have been Potter cottage's secret keeper.",
    sender_nonce="lmXgblZwotx+DfBgKJF0lZXtAXgBEYr5khh79Zytr2Y=",
    requester_nonce="6uj1RdDUbcpI3lVMZvijkMC8Te20O4Bcyz0SyivX8Eg=",
    sender_private_key="AYhVZpbVeX4KS5Qm/W0+9Ye2q3rnVVGmqRICmseWni4=",
    requester_private_key="BAheD5rUqTy4V5xR4/6HWmYpopu5CO+KO8BECS0udNqUTSNo91TIqIIy1A4Vh+F94c+n9vAcwXU2bGcfsI5f69Y=",
)
print("\nEncrypted data: \n", encodeed_data)
