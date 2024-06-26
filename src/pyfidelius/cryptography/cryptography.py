import subprocess
import os
import json
import base64
import logging
import platform
import re
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
    def __init__(self) -> None:
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.abspath(os.path.join(current_file_path, ".."))

        self.os_platform = platform.system()

        if self.os_platform == "Windows":
            script_path = os.path.join(
                root_path, "fidelius-cli-1.2.0", "bin", "fidelius-cli.bat"
            )
        else:
            script_path = os.path.join(
                root_path, "fidelius-cli-1.2.0", "bin", "fidelius-cli"
            )

        self.SCRIPT_PATH = script_path

        if self.os_platform != "Windows":
            self.__prepare_script()

    def __prepare_script(self):
        """
        Prepares the script to be executable by fixing line endings and setting execute permissions.
        """
        try:
            # Fix line endings to Unix style (LF)
            with open(self.SCRIPT_PATH, "rb") as file:
                content = file.read()
            content = content.replace(b"\r\n", b"\n")  # Convert CRLF to LF

            with open(self.SCRIPT_PATH, "wb") as file:
                file.write(content)

            # Make the script executable
            subprocess.run(["chmod", "+x", self.SCRIPT_PATH], check=True)
        except Exception as e:
            log.error(f"Failed to prepare script. Error: {e}")
            raise

    def __execute_cli_commands(self, args: List[str]) -> str:
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

    def sane_encrypt(
        self,
        encoded_string_to_encrypt,
        sender_nonce,
        requester_nonce,
        sender_private_key,
        requester_private_key,
    ):
        """
        `sane-encrypt` is same as ncrypt command, with the only difference being that it accepts base64 encoded version of the input string.

        Arguments:
        - `encoded_string_to_encrypt`: The base64 encoded string that needs to be encrypted.
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
                        encoded_string_to_encrypt,
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
                    encoded_string_to_encrypt,
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

    def decrypt(
        self,
        encrypted_data,
        sender_nonce,
        requester_nonce,
        sender_private_key,
        requester_public_key,
    ):
        """
        Decrypt the encoded data back to original string.

        Arguments:
        - `encrypted_data`: The encrypted data which is required to decrypt.
        - `sender_nonce`: The nonce (number used once) of the sender for encryption.
        - `requester_nonce`: The nonce of the requester for encryption.
        - `sender_private_key`: The private key of the sender for encryption.
        - `requester_public_key`: The public key of the requester for encryption.

        Response:
        ```json
        {
            "decryptedData": "Hello World"
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
                        requester_public_key,
                    ],
                )
            ):
                log.warning(
                    "sender_nonce, requester_nonce, sender_private_key, and requester_public_key must be base64 encoded"
                )
                return None
            output = self.__execute_cli_commands(
                [
                    "d",
                    encrypted_data,
                    sender_nonce,
                    requester_nonce,
                    sender_private_key,
                    requester_public_key,
                ]
            )

            encrypted_data = self.__parse_output_to_dict(output)
            return encrypted_data

        except Exception as e:
            log.error("Unable to decrypt the encrypted data.\nError: ", e)
            return None

    def file_operation(self, file_path):
        """
        ECDH Cryptography can also be applied on file for both encryption and decryption.

        The file needs to be in certain formats

        - For encoding, text file should be in following format

        ```txt
        e
        <string-to-encrypt>
        <sender-nonce>
        <requester-nonce>
        <sender-private-key>
        <requester-public-key>
        ```

        - For decoding, text file should be in following format

        ```txt
        d
        <encrypted-data>
        <requester-nonce>
        <sender-nonce>
        <requester-private-key>
        <sender-public-key>
        ```
        """
        if not os.path.exists(file_path):
            log.error(f"File not found: {file_path}")
            return None

        with open(file_path, "r") as file:
            file_content = file.read()

        if file_content is None or file_content == "":
            log.error("File is empty.")
            return None

        file_content_list = file_content.split("\n")

        # Checks
        if len(file_content_list) > 6:
            log.error("No more than 6 lines are allowed")
            return None

        if file_content_list[0] not in ["e", "d"]:
            log.error(
                "Invalid operation. First line must be 'e' for encryption or 'd' for decryption"
            )
            return None

        if not all(
            map(
                self.__isBase64,
                file_content_list[2:],
            )
        ):
            log.warning(
                "sender_nonce, requester_nonce, sender_private_key, and requester_public_key must be base64 encoded"
            )
            return None

        output = self.__execute_cli_commands(file_content_list)

        processed_data = self.__parse_output_to_dict(output)

        return processed_data
