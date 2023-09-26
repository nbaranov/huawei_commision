from typing import Dict, List, Optional, Any, Union, Sequence, Iterator, TextIO
import time
import re
import warnings

from netmiko.no_enable import NoEnable
from netmiko.base_connection import DELAY_FACTOR_DEPR_SIMPLE_MSG
from netmiko.cisco_base_connection import CiscoBaseConnection
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko import log


class N3ComBase(NoEnable, CiscoBaseConnection):
    def session_preparation(self) -> None:
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        # The _test_channel_read happens in special_login_handler()
        self.set_base_prompt()
        self.disable_paging(command="screen-length 0 temporary")

    def send_command_n3com(self, command):
        i = 0
        prompt = self.find_prompt()
        regex_prompt = re.escape(prompt)
        expect_string = f"[\-\-More\-\-|{regex_prompt}]"
        output = self.send_command(command, expect_string=expect_string, strip_prompt=False)
        while prompt not in output:
            output += self.send_command(' ', normalize=False, expect_string=expect_string, strip_prompt=False)
            i += 1
            if i > 100:
                return "More 100 read iterations"
        clired_output = output.replace(' --More-- ', '').replace(prompt, '')
        return clired_output
        

    def config_mode(
        self,
        config_command: str = "enable",
        pattern: str = "",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def exit_config_mode(self, exit_config: str = "return", pattern: str = r">") -> str:
        """Exit configuration mode."""
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)

    def check_config_mode(
        self, check_string: str = "]", pattern: str = "", force_regex: bool = False
    ) -> bool:
        """Checks whether in configuration mode. Returns a boolean."""
        return super().check_config_mode(check_string=check_string)

    def set_base_prompt(
        self,
        pri_prompt_terminator: str = ">",
        alt_prompt_terminator: str = "#",
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        """
        Sets self.base_prompt

        Used as delimiter for stripping of trailing prompt in output.

        This will be set on logging in, but not when entering system-view
        """

        prompt = super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )

        # Strip off any leading HRP_. characters for USGv5 HA
        prompt = re.sub(r"^HRP_.", "", prompt, flags=re.M)

        # Strip off leading terminator
        prompt = prompt[:-1]
        prompt = prompt.strip()
        self.base_prompt = prompt
        log.debug(f"prompt: {self.base_prompt}")
        return self.base_prompt

    def save_config(
        self, cmd: str = "save", confirm: bool = True, confirm_response: str = "y"
    ) -> str:
        """Didn't changed! Save Config for N3ComSSH"""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )

    def cleanup(self, command: str = "quit") -> None:
        return super().cleanup(command=command)


class N3ComSSH(N3ComBase):
    """N3Com SSH driver."""

    def special_login_handler(self, delay_factor: float = 1.0) -> None:
        # N3Com prompts for password change before displaying the initial base prompt.
        # Search for that password change prompt or for base prompt.
        password_change_prompt = r"(Change now|Please choose)"
        prompt_or_password_change = r"(?:Change now|Please choose|[>\]#])"
        data = self.read_until_pattern(pattern=prompt_or_password_change)
        if re.search(password_change_prompt, data):
            self.write_channel("N" + self.RETURN)
            self.read_until_pattern(pattern=r"[>\]#]")


class N3ComTelnet(N3ComBase):
    """N3Com Telnet driver."""

    def telnet_login(
        self,
        pri_prompt_terminator: str = r"#\s*$",
        alt_prompt_terminator: str = r">\s*$",
        username_pattern: str = r"(?:user:|username|login|user name)",
        pwd_pattern: str = r"assword",
        delay_factor: float = 1.0,
        max_loops: int = 50,
    ) -> str:
        """Telnet login for N3Com Devices"""

        delay_factor = self.select_delay_factor(delay_factor)
        password_change_prompt = r"(Change now|Please choose 'YES' or 'NO').+"
        combined_pattern = r"({}|{}|{})".format(
            pri_prompt_terminator, alt_prompt_terminator, password_change_prompt
        )

        output = ""
        return_msg = ""
        i = 1
        while i <= max_loops:
            try:
                # Search for username pattern / send username
                output = self.read_until_pattern(
                    pattern=username_pattern, re_flags=re.I
                )
                return_msg += output
                self.write_channel(self.username + self.TELNET_RETURN)

                # Search for password pattern / send password
                output = self.read_until_pattern(pattern=pwd_pattern, re_flags=re.I)
                return_msg += output
                assert self.password is not None
                self.write_channel(self.password + self.TELNET_RETURN)

                # Waiting for combined output
                output = self.read_until_pattern(pattern=combined_pattern)
                return_msg += output

                # Search for password change prompt, send "N"
                if re.search(password_change_prompt, output):
                    self.write_channel("N" + self.TELNET_RETURN)
                    output = self.read_until_pattern(pattern=combined_pattern)
                    return_msg += output

                # Check if proper data received
                if re.search(pri_prompt_terminator, output, flags=re.M) or re.search(
                    alt_prompt_terminator, output, flags=re.M
                ):
                    return return_msg

                self.write_channel(self.TELNET_RETURN)
                time.sleep(0.5 * delay_factor)
                i += 1

            except EOFError:
                assert self.remote_conn is not None
                self.remote_conn.close()
                msg = f"Login failed: {self.host}"
                raise NetmikoAuthenticationException(msg)

        # Last try to see if we already logged in
        self.write_channel(self.TELNET_RETURN)
        time.sleep(0.5 * delay_factor)
        output = self.read_channel()
        return_msg += output
        if re.search(pri_prompt_terminator, output, flags=re.M) or re.search(
            alt_prompt_terminator, output, flags=re.M
        ):
            return return_msg

        assert self.remote_conn is not None
        self.remote_conn.close()
        msg = f"Login failed: {self.host}"
        raise NetmikoAuthenticationException(msg)


if __name__ == '__main__':
    ne = N3ComSSH(ip="10.172.220.7", username='n3com', password='n3com')
    prompt = ne.find_prompt()
    command = 'show version'
    print(prompt + command)
    output = ne.send_command_n3com(command)
    print(output)
    
    command = 'show alarm log'
    print(prompt + command)
    output = ne.send_command_n3com(command)
    print(output)
    
    
    