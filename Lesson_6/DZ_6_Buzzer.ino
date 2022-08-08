//Домашнее задание к уроку№6 "Датчики и актуаторы - часть 2"

#define FORCE_PIN A0  //задаем номер пина для датчика силы нажатия 
#define BUZZER_PIN 8  //задаем номер пина зуммера
#define MIN_FORCE 1000  //макс значение датчика
#define MAX_FORCE 2500  //мин значение датчика

void setup() {
    //задаем скорость обмена последовательного порта
  Serial.begin(9600);
}

void loop() {
  
    // считываем значение с датчика нажатия
    int sensorReading = analogRead(FORCE_PIN);
  
  //переводим сигнала с датчика к заданным пределам
    //учитываем максимально возможное значение, 
    //получаемое от датчика при текущем подключении - 914
    sensorReading = map(sensorReading, 0, 914, MIN_FORCE, MAX_FORCE);   
    
    //выводим на последовательный монитор сигнал датчика силы нажатия
    Serial.println(sensorReading);

    // вывод сигнала на зуммер
    tone(BUZZER_PIN, sensorReading);
  
    delay(1); 
  
}
