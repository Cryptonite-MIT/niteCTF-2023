# conqueror

Author: unspecialfx

flag: `nite{cant_catch_me}`

Memory Dump Link: <https://drive.google.com/file/d/1LbElkzno-FophYpkTLPL5ic2BnZgn-UN/view?usp=sharing>

## Description

Too late. The network admin's system was compromised and we can't access our network anymore. Investigate the memory dump.

`Amour Plastique` will be visible after solving this challenge.

## Solution

1. Use the windows.cmdline plugin to see that the sshd_config file is being edited by notepad.

2. Use filescan to get the address and dump it using dumpfiles.
