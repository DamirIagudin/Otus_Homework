# Домашнее задание №3 к уроку №9 "Протоколы передачи данных часть 2" - п.1
import paho.mqtt.client as mqtt

#словарь символов азбуки Морзе
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

dash = '111'
dot = '1'
space_parts = '0'
space_letters = '000'
space_words = '000000'


# Ф-ция подтверждения подключения от сервера
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))  # вывод в терминал результата подключения, 0 -OK
    if rc == 0:  # при успешном подключении
        client.subscribe("led/morse")               #подписываемся на топик "led/morse"

#вывод сообщения от брокера
def on_message(client, userdata, msg):
    print("Получено сообщение '" + str(msg.payload))
    input_str = str(msg.payload)

    result_list = []
    input_list = list(input_str.upper())                    #перевод символов в верхний регистр и преобразование в список
    del input_list[0:2]                                     #удаление лишних символов
    del input_list[-1]                                      #удаление лишних символов
    for letter in input_list:
        if ((ord(letter) > 64) and (ord(letter) < 92)) or ((ord(letter) > 47) and (ord(letter) < 58)):   #символы в диапазоне
            bin_letter = morse_code[letter]                 #считываем значения ключей из словаря morse_code
            print(bin_letter)
            for number in bin_letter:
                if number == 'DASH':                        #"тире"
                    result_list.append(dash)
                elif number == 'DOT':                       #"точка"
                    result_list.append(dot)
                result_list.append(space_parts)             #раздел между точкой/тире одного символа
            result_list.append('00')                        #раздел между символами
        elif letter == (' '):                               #раздел между словами
            print("Пробел")
            result_list.append('0000')
        else:
            print("Invalid text!!!!")
            break
    print("Конец строки")
    c = ''.join(result_list)                                #сброка итоговой строки
    print(c)                                                #вывод итоговой строки азбукой Морзе
    result_list = []                                        #очитска списка для следующего ввода

client = mqtt.Client(client_id="mqtt-damirjud-e4xr1q")      #подключаемся к модели "Raspberry home" на dev.rightech.io
client.username_pw_set(username='1111', password='2222')    #MQTT аутентификация

client.on_connect = on_connect
client.on_message = on_message
client.connect("dev.rightech.io", 1883, 60)

#client.loop_start()

client.loop_forever()