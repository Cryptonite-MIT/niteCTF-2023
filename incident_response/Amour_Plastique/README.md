# conqueror

Author: unspecialfx

flag: `nite{8_bit_synths}`

Memory Dump Link:

## Description

It seems the intruder likes to hack in style. Analysis reveals the hacker was listening to a playlist while destroying the admin's system. Surely they might have left their tracks. Use dump2 to investigate.

`cheval de troie` will be visible after solving this challenge.

## Solution

1. Use the windows.pslist plugin to note the pid of VLC.
2. Dump the memory of the vlc plugin using memmap and use strings to look for the necessary data.
