import re
import os
import json
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

    def generate_key_material(self) -> dict:
        """
        Generates an ECDH key pair, and a random nonce.
        """
        try:
            output = self.__execute_cli_commands(["gkm"])
            key_materials = self.__parse_output_to_dict(output)

            return key_materials
        except Exception as e:
            log.error("Unable to generate key materials.\nMessgae: ", e)
            return None


ecdh = Cryptography()
key_materials = ecdh.generate_key_material()
