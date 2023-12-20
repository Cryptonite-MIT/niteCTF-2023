# Solution

1. the txt file has random text with no immediate pattern, so they try to inspect the audio. The spectrogram of this audio decodes to ENIGMA M_THREE C IV X A VI X A III X A NITEALMOSTTHERE ERUVKJAAWNRZXYV PLUG ZABDHEOP (shown in spectrogram.png).
2. This gives them the hint that the text is encoded using an enigma machine and all details except rotor positions(X) are given along with sample encoding.
3. Using a python script(decrypt.py), they find the rotor positions as DWG.
4. They then decrypt text.txt using these enigma machine settings to get decrypted_text.txt and find the flag as NITE QUITEENIGMATIC
