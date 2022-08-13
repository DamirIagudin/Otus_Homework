# Домашнее задание №3 к уроку №9 "Протоколы передачи данных часть 2" - п.2
import paho.mqtt.client as mqtt
import time


# Ф-ция подтверждения подключения от сервера
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))  # вывод в терминал результата подключения, 0 -OK
    if rc == 0:  # при успешном подключении
        client.subscribe("led/single")  # подписываемся на топик "led/single"


input_str = ''

# вывод сообщения от брокера
def on_message(client, userdata, msg):
    print("Получено сообщение '" + str(msg.payload))
    input_str = str(msg.payload)
    print(input_str)

    if input_str == "b'TRUE'":
        print("LED - ON")
        time.sleep(1)
        print("LED - off")


client = mqtt.Client(client_id="mqtt-damirjud-e4xr1q")  # подключаемся к модели "Raspberry home" на dev.rightech.io
client.username_pw_set(username='1111', password='2222')  # MQTT аутентификация

client.on_connect = on_connect
client.on_message = on_message

client.connect("dev.rightech.io", 1883, 60)

client.loop_forever()
# client.loop_start()
# client.loop_stop()



