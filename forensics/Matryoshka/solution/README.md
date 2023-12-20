# Writeup

Given file has one line of base64 encoded string ( although 23 MB ) which on decoding gives hex encoded numbers (no A,B ...) . Decoding these numbers gives you ASCII value numbers, which on decoding give out raw hex stream of a file. (here, hexstream.txt)

Reverting this `hexstream.txt` using `bin.py` gives you an `outer_image.jpg` of matryoshka doll. Binwalk' ing the image shows there's zip and png . Zip has readme.txt file that's useless. We need PNG , note we must use `binwalk --dd=".*" <filename>` to get `PNG file (img.png)` -e and unzipping directly won't work.

Using the `reverser.py`, the (R,G,B) hex values of this image gives you another hexstream of an image (`hexed.txt`) which on reverting gives you another `inside.jpg` . Unzipping this jpg gives an ` nested archive` which at the end give you the `exec` file. This file only prints "MAKE IT STOP" and exits due to function call.

Use Ghidra or gdb to skip over that function call and an file called `compiler` is created. So, exec is just a C executable that prints a python file. Running this python file prints yet another hex stream `final_hex.txt` which reverts into a .class Java file, that prints random string everytime. Easiest way to decompile this file is to use VS Code to open it, `code nite.class` (you can get class name is by decompiling it in VS Code). Just put another `System.out.println(var6)` for var6 to get the flag (`another.class`).

---

### Flag : nite{1_h4v3_w4y_700_m4ny_d0ll5_n0w_hmm_l4y3r5_0f_l1f3_ig}
