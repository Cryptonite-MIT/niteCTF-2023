from enigma.machine import EnigmaMachine
from itertools import product


def char_to_int(char):
    return ord(char) - ord("A")


def int_to_char(num):
    return chr(num + ord("A"))


def convert_plugboard_settings(plugboard):
    plugboard_pairs = plugboard.split()
    return " ".join([pair.upper() for pair in plugboard_pairs])


def find_rotor_positions(message, cipher_text, rotor_rings, plugboard):
    machine = EnigmaMachine.from_key_sheet(
        rotors="IV VI III",
        reflector="C",
        ring_settings=tuple(map(char_to_int, rotor_rings)),
        plugboard_settings=convert_plugboard_settings(plugboard),
    )
    rotor_positions = product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=len(machine.rotors))
    for rotor_pos in rotor_positions:
        machine.set_display(rotor_pos)
        decrypted_message = machine.process_text(cipher_text)
        if decrypted_message == message:
            return "".join(rotor_pos)
    return None


rotor_rings = "AAA"
plugboard = "ZA BD HE OP"
message = "NITEALMOSTTHERE"
cipher_text = "ERUVKJAAWNRZXYV"
result = find_rotor_positions(message, cipher_text, rotor_rings, plugboard)
if result:
    print(f"Original Message: {message}")
    print(f"Cipher Text: {cipher_text}")
    print(f"Found Rotor Positions: {result}")
else:
    print("Rotor positions not found.")
