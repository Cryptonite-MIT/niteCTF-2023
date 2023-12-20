# conqueror

Author: unspecialfx

flag: `nite{napoleon_shorty}`

Memory Dump Link: <https://drive.google.com/file/d/14MWp-UtVPAcu1hEyv1_xBhpdO3nIrEBo/view?usp=sharing>

## Description

Our company is dealing with a possible case of corporate espionage.
The credentials of one of our systems were changed and it was used to gain access to our internal network.

Help us gain access to the system before its too late.

`Flag Format: nite{user_password}`

`coup de réseau` will be visible after solving this challenge.

## Solution

1. Use the windows.hashdump volatility3 plugin to dump the NT hash for the user napoleon.
2. Use hashcat along with the rockyou.txt dictionary to crack the password.
