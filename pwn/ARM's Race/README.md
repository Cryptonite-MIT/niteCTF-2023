# ARM's race

Challenge author: Skryptonyte

## Description

Exploit a race condition to leak a libc address and then exploit it again to ROP to /bin/sh.

# Note

-   arms-race_challenge is the binary to be used. This is directly patched against the libc and ld files given.
-   Use QEMU aarch64 userspace program to run this
