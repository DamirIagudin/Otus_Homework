# Домашнее задание №4 к уроку №10 "Моделирование поведения IoT-устройства"

import sys  # system params and function
import paho.mqtt.client as mqtt  # mqtt paho
import json  # json converter
import time  # for sleep
from datetime import datetime  # for date


### machine and logic
class Machine():
    def __init__(self, mqtt_client, details=0, progress=0, temperature=21, light=True):
        self.mqtt_client = mqtt_client
        self.topic_data = "data/state"
        self.topic_change_temp = "command/change_temp"
        self.topic_change_light = "command/change_light"
        self.temperatureValue = temperature
        self.lightValue = light
        self.detail_count = details
        self.progress = progress

        self.mqtt_client.subscribe(self.topic_change_temp)
        self.mqtt_client.message_callback_add(self.topic_change_temp, self.command_change_temp)
        self.mqtt_client.subscribe(self.topic_change_light)
        self.mqtt_client.message_callback_add(self.topic_change_light, self.command_change_light)

    def command_change_temp(self, client, userdata, message):
        print("CMD: Change temp, value: %s" % message.payload)
        try:
            self.temperatureValue = int(message.payload)
        except:
            print("can't change temp to %s" % message.payload)

    def command_change_light(self, client, userdata, message):
        print("CMD: Change light, value: %s" % message.payload)
        try:
            self.lightValue = int(message.payload)
        except:
            print("can't change light to %s" % message.payload)

    def progress_upd(self):
        if self.progress >= 100:
            self.progress = 0
            self.detail_count += 1
        else:
            self.progress = self.progress + 25
        try:
            f = open('./save_state.txt', 'r')
            file = f.read()
            config = json.loads(file)
            f.close()
        except:
            config = {}
        f = open('./save_state.txt', 'w')
        config["progress"] = self.progress
        config["details"] = self.detail_count
        config = json.dumps(config)
        f.write('%s' % config)
        f.close()
        print("detail count = %d, progress now = %d%% " % (self.detail_count, self.progress))
#        f = open('./save_state.txt', 'w')
#        config = json.dumps({"details": self.detail_count, "progress": self.progress})
#        f.write('%s' % config)
#        f.close()

    def get_data(self):
        data = json.dumps({"temp": self.temperatureValue, "light": self.lightValue, "detail_count": self.detail_count,
                           "time": str(datetime.now())})
        return data


# init mqtt
def init(clientid, clientUsername="", clientPassword=""):
    client = mqtt.Client(client_id=clientid)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=clientUsername, password=clientPassword)
    return client


# connect reaction
def on_connect(client, userdata, flags, rc):
    print("Connected with result code %s" % str(rc))
    if rc == 0:
        isConnect = 1
        client.publish("connect", "true", 1)
    if rc == 5:
        print("Authorization error")


# default message reaction
def on_message(client, userdata, message):
    print("Some message received topic: %s, payload: %s" % (message.topic, message.payload))


# connect to server
def publish_data(client, topic, data):
    print(topic, data)
    return client.publish(topic, data)


def run(client, host="127.0.0.1", port=1883):
    client.connect(host, port, 60)
    client.loop_start()


# function for publish data

# body of emulator
def main():
    # create mqtt with id clinet_id
    mqtt_client = init("client_id")
    run(mqtt_client)
    # read config
    details = 0
    progress = 0
    argv = sys.argv
    try:
        path_to_config = argv[1] if len(argv) > 1 else "./save_state.txt"
        f = open(path_to_config, 'r')
        file = f.read()
        config = json.loads(file)
        f.close()
        details = int(config["details"])
        progress = int(config["progress"])
        print("read config %s" % config)
    except:
        pass

    # init machine
    machine = Machine(mqtt_client, details, progress)

    while True:
        time.sleep(2)
        machine.progress_upd()
        ret = publish_data(mqtt_client, machine.topic_data, machine.get_data())

        if ret[0] != 0:
            print("Fail publish. Save this message if you need")
        else:
            pass


if __name__ == '__main__':
    main()