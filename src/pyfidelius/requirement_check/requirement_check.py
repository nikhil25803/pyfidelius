import re
import logging
import platform
import subprocess
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)],
)
log = logging.getLogger("rich")


class RequirementCheck:
    """
    Fidelius CLI requires JRE installed in the system (version 1.8+)
    ```py
    rcheck = RequirementCheck()
    res = rcheck.check()
    ```
    """

    def __init__(self) -> None:
        pass

    def __validate(self, outputs):
        version_line = outputs[0]
        match = re.search(r'version "(\d+\.\d+)', version_line)
        if match:
            version = float(match.group(1))
            if version < 1.8:
                return False, "Java version is less than 1.8\nRequired: 1.8 or 1.8+"

        if not any("Java(TM) SE Runtime Environment" in line for line in outputs):
            return False, "Java(TM) SE Runtime Environment not found."

        if not any("Java HotSpot(TM)" in line for line in outputs):
            return False, "Java HotSpot(TM) not found."

        return True, "All requirements satisfied."

    def check(self):
        cli_command = subprocess.run(
            ["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        response = cli_command.stdout
        outputs = response.decode("utf-8").split("\n")

        validation_res = self.__validate(outputs)

        if validation_res[0] is False:
            log.warning(validation_res[1])
            return False

        log.info(validation_res[1])
        return True

    def identify_os(self):
        os_name = platform.system()
        if os_name == "Linux":
            return "linux"
        elif os_name == "Windows":
            return "windows"
        elif os_name == "Darwin":
            return "mac"
        else:
            return "unknown"


# Example usage
rcheck = RequirementCheck()
os_identified = rcheck.identify_os()
log.info(f"Operating System identified: {os_identified}")
res = rcheck.check()
