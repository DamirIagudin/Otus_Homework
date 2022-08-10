//Домашнее задание №3 п.2 к уроку №9 "Протоколы передачи данных - часть 2"

#include "Arduino.h"
#include "EspMQTTClient.h" /* https://github.com/plapointe6/EspMQTTClient */
                           /* https://github.com/knolleary/pubsubclient */
#define PUB_DELAY (15 * 1000) /* 15 seconds */

EspMQTTClient client(
  "TP-LINK_86",
  "19791979dg",

  "dev.rightech.io",
  "mqtt-otus-username",                  /*логин*/
  "mqtt-otus-password",                   /*пароль*/
  "mqtt-damirjud-rj6zgu"    /*идентификатор подключения*/ 
  
);

void setup() {
  Serial.begin(9600);  
}

void onConnectionEstablished() {
  Serial.println("success");      //сообщение с подтверждением подключения к брокеру
}

long last = 0;
void publishLed() {
  long now = millis();
  if (client.isConnected() && (now - last > PUB_DELAY)) {
    client.publish("led/single", "TRUE");           //отправка в топик led/single каждые 15 сек
    last = now;
  }
}



void loop() {
  client.loop();


  publishLed();

}
