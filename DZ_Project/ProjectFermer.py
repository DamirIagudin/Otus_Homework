# Програмный эмулятор проекта "Фермерское хозяйство"
import paho.mqtt.client as mqtt  # mqtt paho
import time
import random
import json

state_temp = "heating"  # состояние для эмуляции работы кондиционера
truck_temp = 3          # начальная температура в кузове грузовика
state_truck = 0         # переменная для эмуляции состояния грузовика
i_truck = 0             # служебная переменная
massa_truck = 0         # масса продукции в грузовике
speed_truck = 0         # скорость грузовика
hard_break = False      # признак резкого торможения
vibration = 0           # уровень вибрации грузовика %
pos = {"lat": 56.17, "lon": 43.88}  # координаты грузовика
state_temp_storage = "heating"  # состояние для эмуляции работы кондиционера склада
storage_temp = 8.0          # начальная температура в складе
COOL = False
GATE = False

# ---------------MQTT-КЛИЕНТ. ЭМУЛЯТОР ГРУЗОВИКА-----------------
# Ф-ция подтверждения подключения от сервера
def truck_on_connect(client, userdata, flags, rc):
    print("Подключение к эмулятору грузовика с кодом: " + str(rc))  # вывод в терминал результата подключения, 0 -OK
    if rc == 0:  # при успешном подключении
        client.subscribe("base/relay/cool")  # подписываемся на топик "base/relay/cool"


# получение сообщения от брокера
def truck_on_message(client, userdata, message):
    print("Получено сообщение в эмулятор грузовика топик: %s, payload: %s" % (message.topic, message.payload))
    is_cool = False
    if str(message.payload) == "b'1'":
        is_cool = True
    elif str(message.payload) == "b'0'":
        is_cool = False
    client.publish("base/state/is_cool", is_cool)     # состояние кондиционера


# подключение к модели "Грузовик. "Фермерское хозяйство"" на dev.rightech.io
client_truck = mqtt.Client(client_id="mqtt-damirjud-dstbf4")
client_truck.username_pw_set(username='TruckFermer', password='2222')  # MQTT аутентификация
client_truck.on_connect = truck_on_connect
client_truck.on_message = truck_on_message
client_truck.connect("dev.rightech.io", 1883, 20)
client_truck.loop_start()


# ---------------MQTT-КЛИЕНТ. ЭМУЛЯТОР CКЛАДА-----------------
# Ф-ция подтверждения подключения от сервера
def storage_on_connect(client, userdata, flags, rc):
    print("Подключение к эмулятору склада с кодом: " + str(rc))  # вывод в терминал результата подключения, 0 -OK
    if rc == 0:  # при успешном подключении
        client.subscribe("base/relay/cmd")  # подписываемся на топик управления кондиционером и шлагбаумом


# получение сообщения от брокера
def storage_on_message(client, userdata, message):
    print("Получено сообщение в эмулятор склада топик: %s, payload: %s" % (message.topic, message.payload))
    is_cool = False
    is_gate = False
    if str(message.payload) == "b'cool_ON'":
        is_cool = True
        client.publish("base/state/is_cool", is_cool)  # состояние кондиционера
    elif str(message.payload) == "b'cool_OFF'":
        is_cool = False
        client.publish("base/state/is_cool", is_cool)  # состояние кондиционера
    elif str(message.payload) == "b'gate_ON'":
        is_gate = True
        client.publish("base/state/is_gate", is_gate)  # состояние шлагбаума
    elif str(message.payload) == "b'gate_OFF'":
        is_gate = False
        client.publish("base/state/is_gate", is_gate)  # состояние шлагбаума



# подключение к брокеру
client_storage = mqtt.Client(
    client_id="mqtt-damirjud-2fb71t")  # подключаемся к модели "Склад. "Фермерское хозяйство"на dev.rightech.io
client_storage.username_pw_set(username='StorageFermer', password='3333')  # MQTT аутентификация
client_storage.on_connect = storage_on_connect
client_storage.on_message = storage_on_message
client_storage.connect("dev.rightech.io", 1883, 20)
client_storage.loop_start()


# ------------------ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ--------------
while True:
    time.sleep(2)

    # ---------------------ГРУЗОВИК-----------------------

    # эмуляция параметров грузовика внутри кузова - random
    client_truck.publish("base/state/humidity_inside", random.random() * (45 - 42) + 42)  # влажность
    client_truck.publish("base/state/argon", random.random() * (1.3 - 1.2) + 1.2)  # аргон
    client_truck.publish("base/state/azot", random.random() * (76 - 74) + 74)  # азот
    client_truck.publish("base/state/gelii", random.random())  # гелий
    client_truck.publish("base/state/vodorod", random.random())  # водород
    client_truck.publish("base/state/co2", random.random())  # углекислый газ
    client_truck.publish("base/state/co", random.random())  # угарный газ
    client_truck.publish("base/state/o2", random.random() * (24 - 21) + 21)  # кислород

    # эмуляция температуры внутри кузова
    match state_temp :
        case "heating" :  # повышение температуры
            truck_temp += 1
            if truck_temp > 10:
                state_temp = "cooling"
        case "cooling" :  # понижение температуры
            truck_temp -= 1
            if truck_temp < 5:
                state_temp = "heating"
    client_truck.publish("base/state/temperature_inside", truck_temp)

    # эмуляция статуса грузовика
    match state_truck:
        case 0:                 # пустой на ферме, остановлен
            massa_truck = 0
            speed_truck = 0
            vibration = 0
            i_truck += 1
            if i_truck > 5:
                i_truck = 0
                massa_truck = 1500
                state_truck = 1
        case 1:                 # загружается на ферме, остановлен
            massa_truck += 20
            speed_truck = 0
            vibration = 0
            i_truck += 1
            if i_truck > 5:
                i_truck = 0
                speed_truck = 40
                state_truck = 2
        case 2:                 # загружен, движется на склад
            speed_truck = random.random() * (50 - 40) + 40
            pos["lat"] -= 0.005
            vibration = 30
            i_truck += 1
            hard_break = (i_truck > 13) & (i_truck < 15)  # эмуляция резкого торможения
            if i_truck > 25:
                i_truck = 0
                state_truck = 3
        case 3:                 # остановлен, разгружается на складе
            speed_truck = 0
            massa_truck -= 200
            vibration = 0
            if massa_truck <= 0:
                i_truck = 0
                massa_truck = 0
                state_truck = 4
        case 4:                 # пустой возвращается на склад, "водитель-лихач"
            i_truck += 1
            pos["lat"] += 0.005
            if i_truck < 10:                             # эмуляция сильной тряски и повышенной скорости
                vibration = 50
                speed_truck = random.random() * (90 - 80) + 80
            elif (i_truck > 14) & (i_truck < 20):
                vibration = 85
                speed_truck = random.random() * (90 - 80) + 80
            else:
                vibration = 40
                speed_truck = 52
            if i_truck > 25:
                i_truck = 0
                state_truck = 0

    client_truck.publish("base/state/speed", speed_truck)  # скорость
    client_truck.publish("base/state/vibration", vibration)  # вибрация
    client_truck.publish("base/state/is_hard_break", hard_break)  # резкое торможение
    client_truck.publish("base/state/massa", massa_truck)  # масса
    client_truck.publish("base/state/pos", json.dumps(pos))  # координаты грузовика

    # эмуляция параметров грузовика снаружи кузова
    client_truck.publish("base/state/temperature_outside", random.random() * (16 - 15) + 15)  # температура
    client_truck.publish("base/state/humidity_outside", random.random() * (60 - 57) + 57)  # влажность

    # ---------------------СКЛАД-----------------------

    # эмуляция параметров внутри склада - random
    client_storage.publish("base/state/humidity_inside", random.random() * (55 - 52) + 52)  # влажность
    client_storage.publish("base/state/argon", random.random() * (1.3 - 1.2) + 1.2)  # аргон
    client_storage.publish("base/state/azot", random.random() * (76 - 74) + 74)  # азот
    client_storage.publish("base/state/gelii", random.random())  # гелий
    client_storage.publish("base/state/vodorod", random.random())  # водород
    client_storage.publish("base/state/co2", random.random())  # углекислый газ
    client_storage.publish("base/state/co", random.random())  # угарный газ
    client_storage.publish("base/state/o2", random.random() * (24 - 21) + 21)  # кислород
    client_storage.publish("base/state/k_air", random.random() * (2 - 1.3) + 1.3)  # кратность воздухообмена
    client_storage.publish("base/state/massa", random.randrange(15000, 20000))  # масса продукции на складе

    # эмуляция температуры внутри склада
    match state_temp_storage:
        case "heating":  # повышение температуры
            storage_temp += 0.5
            if storage_temp > 10:
                state_temp_storage = "cooling"
        case "cooling":  # понижение температуры
            storage_temp -= 0.5
            if storage_temp < 5:
                state_temp_storage = "heating"
    client_storage.publish("base/state/temperature_inside", storage_temp)



