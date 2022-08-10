# CircuitPython Blink Example

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP5)
led.direction = digitalio.Direction.OUTPUT


morse_code = {
    "A": ['DOT', 'DASH'],
    "B": ['DASH', 'DOT', 'DOT', 'DOT'],
    "C": ['DASH', 'DOT', 'DASH', 'DOT'],
    "D": ['DASH', 'DOT', 'DOT'],
    "E": ['DOT'],
    "F": ['DOT', 'DOT', 'DASH', 'DOT'],
    "G": ['DASH', 'DASH', 'DOT'],
    "H": ['DOT', 'DOT', 'DOT', 'DOT'],
    "I": ['DOT', 'DOT'],
    "J": ['DOT', 'DASH', 'DASH', 'DASH'],
    "K": ['DASH', 'DOT', 'DASH'],
    "L": ['DOT', 'DASH', 'DOT', 'DOT'],
    "M": ['DASH', 'DASH'],
    "N": ['DASH', 'DOT'],
    "O": ['DASH', 'DASH', 'DASH'],
    "P": ['DOT', 'DASH', 'DASH', 'DOT'],
    "Q": ['DASH', 'DASH', 'DOT', 'DASH'],
    "R": ['DOT', 'DASH', 'DOT'],
    "S": ['DOT', 'DOT', 'DOT'],
    "T": ['DASH'],
    "U": ['DOT', 'DOT', 'DASH'],
    "V": ['DOT', 'DOT', 'DOT', 'DASH'],
    "W": ['DOT', 'DASH', 'DASH'],
    "X": ['DASH', 'DOT', 'DOT', 'DASH'],
    "Y": ['DASH', 'DOT', 'DASH', 'DASH'],
    "Z": ['DASH', 'DASH', 'DOT', 'DOT'],
    "1": ['DOT', 'DASH', 'DASH', 'DASH', 'DASH'],
    "2": ['DOT', 'DOT', 'DASH', 'DASH', 'DASH'],
    "3": ['DOT', 'DOT', 'DOT', 'DASH', 'DASH'],
    "4": ['DOT', 'DOT', 'DOT', 'DOT', 'DASH'],
    "5": ['DOT', 'DOT', 'DOT', 'DOT', 'DOT'],
    "6": ['DASH', 'DOT', 'DOT', 'DOT', 'DOT'],
    "7": ['DASH', 'DASH', 'DOT', 'DOT', 'DOT'],
    "8": ['DASH', 'DASH', 'DASH', 'DOT', 'DOT'],
    "9": ['DASH', 'DASH', 'DASH', 'DASH', 'DOT'],
    "0": ['DASH', 'DASH', 'DASH', 'DASH', 'DASH']
}

dash = 3
dot = 1
space_parts = 1

result_list = []



while True:
    input_str = str(input("Введите символы:"))             
    input_list = list(input_str.upper()) 


    for letter in input_list:
        if ((ord(letter) > 64) and (ord(letter) < 92)) or ((ord(letter) > 47) and (ord(letter) < 58)):
            bin_letter = morse_code[letter]
            print(bin_letter)
            for number in bin_letter:
                if number == 'DASH':
                    result_list.append('1' * dash)               
                    led.value = True
                    time.sleep(0.5 * dash)
                elif number == 'DOT':
                    result_list.append('1' * dot) 
                    led.value = True
                    time.sleep(0.5 * dot)
                result_list.append(space_parts) 
                led.value = False
                time.sleep(0.5 * space_parts)
            result_list.append('00')     
            led.value = False
            time.sleep(0.5 * 2)
        elif letter == (' '):                                        
            result_list.append('0000')
            led.value = False
            time.sleep(0.5 * 4)
        else:
            print("Invalid text!!!!")
            break
