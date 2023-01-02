import os
import logging
import src.constants as con

from src.start import Start

def create_kill_script(filename):
    shebang = "#!/bin/bash"
    command = f"kill -9 {os.getpid()}"
    with open(filename, "w") as f:
        f.truncate(0)
        f.write(f"{shebang}\n\n{command}")
create_kill_script("stop")

Start()
