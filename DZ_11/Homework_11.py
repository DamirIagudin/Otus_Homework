# Домашнее задание №11 к уроку №26 "Издание сертификата X.509 и подключение к IoT платформе по протоколу MQTTS"
from random import uniform
from threading import Timer
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("on_connect rc: [%d]" % (rc))


def on_disconnect(client, userdata, rc):
    print("disconnected with rtn code [%d]" % (rc))


client = mqtt.Client(client_id="mqtt-damirjud-e4xr1q")  # подключаемся к модели "Raspberry home" на dev.rightech.io
client.username_pw_set(username='1111', password='2222')  # MQTT аутентификация

client.tls_set(certfile="cert.pem",     #добавление ключа и сертификата, изданных на платформе
               keyfile="key.pem")

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect("dev.rightech.io", 8883, 60)


def publish():
    temp = round(uniform(20, 30), 2)
    client.publish("base/state/temperature", temp, qos=0)
    Timer(10, publish).start()


Timer(1, publish).start()

client.loop_forever()