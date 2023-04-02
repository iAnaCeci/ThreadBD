import random
import threading
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['bancoiot']

sensores = db.sensores


class Sensor(threading.Thread):
    def __init__(self, nome, intervalo):
        threading.Thread.__init__(self)
        self.nome = nome
        self.intervalo = intervalo
        self.sensorAlarmado = False

    def run(self):
        while not self.sensorAlarmado:
            temp = random.randint(30, 40)
            print(f"Temperatura sensor {self.nome}: {temp}")
            if temp > 38:
                self.sensorAlarmado = True
                print(f"Atenção! Temperatura muito alta! Verificar sensor {self.nome}")
            newtemp = {
                "nomeSensor": self.nome,
                "valorSensor": temp,
                "unidadeMedida": "C°",
                "sensorAlarmado": self.sensorAlarmado
            }
            db.sensores.insert_one(newtemp)
            time.sleep(self.intervalo)


class SensorPH(Sensor):
    def __init__(self, intervalo):
        Sensor.__init__(self, "pH", intervalo)


class SensorLuminosidade(Sensor):
    def __init__(self, intervalo):
        Sensor.__init__(self, "Luminosidade", intervalo)


class SensorUmidade(Sensor):
    def __init__(self, intervalo):
        Sensor.__init__(self, "Umidade", intervalo)


sensorPH = SensorPH(5)
sensorLuminosidade = SensorLuminosidade(5)
sensorUmidade = SensorUmidade(5)

sensorPH.start()
sensorLuminosidade.start()
sensorUmidade.start()
