import os
from pathlib import Path
from datetime import datetime

import yaml

# Windows
if os.name == 'nt':
    import msvcrt
# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select



class Constants:
    dir_logs = Path("logs/")
    dir_bank = Path("bank/")
    config_file = Path('config.yml')

class KBHit:

    """
    A Python class implementing KBHIT, the standard keyboard-interrupt poller.
    Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
    with IDLE.
    Under LGP License.
    Made by Simon D. Levy as part of a compilation of software
    https://simondlevy.academic.wlu.edu/software/
    Implemented here with a few modifications.
    """

    def __init__(self):
        """
        Creates a KBHit object that you can call to do various keyboard things.
        """
        if os.name == 'nt':
            pass
        else:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """
         Resets to normal terminal.  On Windows this is a no-op.
        """

        if os.name == 'nt':
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        """
        Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        """

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return sys.stdin.read(1)

    def getarrow(self):
        """Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        """

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))

    def kbhit(self):
        """
        Returns True if keyboard character was hit, False otherwise.
        """
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


class BaseClass:
    """
    Base class for both bank and inspector
    """

    def _log(self, message, stdio: bool = True, in_file: bool = False, file_mode: str = "a"):

        prefix = datetime.now().strftime("%Y-%m-%d:%H:%M:%S ")

        output_string = f"{prefix}{message}"

        if stdio:
            print(output_string)

        if in_file:
            with open(self.log_database, mode=file_mode) as f:
                f.write(output_string + "\n")

    def _id_to_index(self, bid: int) -> int:
        for i, branch in enumerate(self.branches):
            if branch["id"] == bid:
                return i


    def get_config(self, path=None):
        """
        Gets and prepares configurations from yaml config file
        """

        if path is None:
            path = Constants.config_file

        with open(path, 'r') as yaml_file:
            self.config = yaml.load(yaml_file, Loader=yaml.FullLoader)

        self.brnch_confs = self.config['branches']
        self.bank_confs = self.config['bank']
        self.inspctr_confs = self.config['inspector']
