# I give up Solution

`frame_splitter.py` splits video into frames. images were put in in "source" folder.<br>\_

-   The fake flag `nite{n3v3r_g0nn4_g1ve_u_+he_fl4g!}` is hidden in the **audio.wav** file. Encryption is done using `audacity.py` and fake flag can be extracted by `decaudacity.py`.
-   Frames are in a pcap file `file.pcap` after xoring using `encrypter.py` with fake flag.<br>
-   `decrypter.py` unxors and gets the original images in "reformed_images" folder.<br>
-   one of the images will be lsb'd using steghide and password will be the fakeflag. currently that image is "41.jpg" and flag.txt can be extracted. (41 because NGGYU release date 27/07/1987 => 2+7+0+7+1+9+8+7 = 41).
-   The 41st image therefore, has a COMMENT.
-   flag.txt will give real flag, currently set as `nite{h4nging_0n_+o_th3_la5t_b1ts}`
