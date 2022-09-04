# Домашнее задание №4 к уроку №10 "Моделирование поведения IoT-устройства"
import sys  # system params and function
import paho.mqtt.client as mqtt  # mqtt paho
import json  # json converter
import time  # for sleep
from datetime import datetime  # for date


### machine and logic
class Machine():
    def __init__(self, mqtt_client, koordinates, commands="pause"):
        self.mqtt_client = mqtt_client
        self.topic_data = "data/state"
        self.topic_commands = "commands"
        self.commands = commands  # команды: 1 - работа, 2 - пауза, 0 - возврат на базу
        self.koordinates = koordinates  # текущие координаты
        self.course = 'forward_X'  # направление движения
        self.state = ''  # текущее состояние

        self.mqtt_client.subscribe(self.topic_commands)
        self.mqtt_client.message_callback_add(self.topic_commands, self.reaction_command)

    def reaction_command(self, client, userdata, message):
        self.input_list = list(str(message.payload))
        del self.input_list[0:2]
        del self.input_list[-1]
        if self.input_list == ['0']:
            self.commands = "on_base"
            print("commands:", self.commands)
        elif self.input_list == ['1']:
            self.commands = "work"
            print("commands:", self.commands)
        elif self.input_list == ['2']:
            self.commands = "pause"
            print("commands:", self.commands)
        else:
            print("Incorrect command")

    def progress_upd(self):
        if self.commands == "work":  # РАБОТА
            match self.course:
                case "forward_X":  # движение вперед по оси Х
                    self.koordinates['X'] += 1
                    if self.koordinates['X'] >= 10:
                        self.course = "right_Y"
                    self.state = 'WORK_forward_X'
                case "right_Y":  # поворот направо по оси Y
                    self.koordinates['Y'] += 1
                    self.course = "backward_X"
                    self.state = 'WORK_right_Y'
                case "backward_X":  # движение назад по оси X
                    self.koordinates['X'] -= 1
                    if self.koordinates['X'] <= 0:
                        self.course = "left_Y"
                    self.state = 'WORK_backward_X'
                case "left_Y":  # поворот на налево по оси Y
                    self.koordinates['Y'] += 1
                    self.course = "forward_X"
                    self.state = 'WORK_left_Y'

        elif self.commands == "on_base":  # ДВИЖЕНИЕ НА БАЗУ
            self.course = "forward_X"
            if self.koordinates['Y'] > 0:
                self.koordinates['Y'] -= 1
                self.state = 'move_TO_BASE'
            elif self.koordinates['X'] > 0:
                self.koordinates['X'] -= 1
                self.state = 'move_TO_BASE'
            else:
                self.state = 'ON_BASE'

        elif self.commands == "pause":  # ПАУЗА
            self.state = 'PAUSE'

        try:
            f = open('./save_state.txt', 'r')
            file = f.read()
            config = json.loads(file)
            f.close()
        except:
            config = {}
        f = open('./save_state.txt', 'w')
        config["koordinates"] = self.koordinates
        config["state"] = self.state
        config = json.dumps(config)
        f.write('%s' % config)
        f.close()

    def get_data(self):
        data = json.dumps({"koordinates": self.koordinates, "state": self.state, "time": str(datetime.now())})
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



# body of emulator
def main():
    # create mqtt with id clinet_id
    mqtt_client = init("client_id")
    run(mqtt_client)
    # read config
    koordinates = {'X': 0, 'Y': 0}
    argv = sys.argv;
    try:
        path_to_config = argv[1] if len(argv) > 1 else "./save_state.txt"
        f = open(path_to_config, 'r')
        file = f.read()
        config = json.loads(file)
        f.close()
        koordinates = dict(config["koordinates"])
        print("read config %s" % config)
    except:
        pass

    # init machine
    machine = Machine(mqtt_client, koordinates)

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
