# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError
temp = 0

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}


def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)


# Enigma Logics Start
# Plugboard
def pass_plugboard(param):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, param):
            return plug[1]
        elif str.endswith(plug, param):
            return plug[0]

    return param


# ETW
def pass_etw(param):
    return SETTINGS["ETW"][ord(param) - ord('A')]


# Wheels
def pass_wheels(value, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    if not reverse:  # forward
        for idx in range(len(WHEELS) - 1, -1, -1):
            if idx == len(WHEELS) - 1:
                index = (ord(value) - ord('A') + SETTINGS['WHEEL_POS'][idx]) % 26
            else:
                index = (ord(value) - ord('A') - SETTINGS['WHEEL_POS'][idx + 1] + SETTINGS['WHEEL_POS'][idx]) % 26
            value = SETTINGS['WHEELS'][idx]['wire'][index]
    else:  # backword
        for idx in range(len(WHEELS)):
            if idx == 0:
                index = (ord(value) - ord('A') + SETTINGS['WHEEL_POS'][idx]) % 26
            else:
                index = (ord(value) - ord('A') + SETTINGS['WHEEL_POS'][idx] - SETTINGS['WHEEL_POS'][idx - 1]) % 26
            index = SETTINGS['WHEELS'][idx]['wire'].index(ETW[index])  # output index
            value = ETW[index]
        index -= SETTINGS['WHEEL_POS'][2]
        index += 26 if index < 0 else 0
        value = ETW[index]
    return value


# UKW
def pass_ukw(param):
    return SETTINGS["UKW"][ord(param) - ord('A')]


# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    for idx in range(2, -1, -1):
        SETTINGS['WHEEL_POS'][idx] = (SETTINGS['WHEEL_POS'][idx] + 1) % len(ETW)
        SETTINGS['WHEELS'][idx]['turn'] -= 1
        if SETTINGS['WHEELS'][idx]['turn'] >= 0:
            break
        else:
            SETTINGS['WHEELS'][idx]['turn'] += len(ETW)
    pass


# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = "B"  # input("Set Reflector (A, B, C): ")
wheel_select = "III II I"  # input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = "A A A"  # input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = "AB CD"  # input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    temp += 1
    # print(SETTINGS)
    rotate_wheels()
    # print(SETTINGS)
    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
