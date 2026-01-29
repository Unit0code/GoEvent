import json
from pathlib import Path
from datetime import datetime, date, time, timedelta
from user import User
import Events
from copy import deepcopy, copy


class Recurso:
    def __init__(self, nombre:str , categoria: str, estado: str = 'None', usos:int = None, energia:int = None):
        self.nombre = nombre
        self.categoria = categoria
        self.estado = estado
        self.usos = usos  ### Una vez se agote, los vehiculos no funcionaran
        self.energia = energia ### una vez se agote, las personas no podran trabajar
    
    def __dict__(self):
        Data = { 'Nombre': self.nombre,
                 'Categoria': self.categoria,
                 'Estado': self.estado,
                 'usos': self.usos,
                 'energia': self.energia
                }
        return Data
    
    def __repr__ (self):
        Data = { 'Nombre': self.nombre,
                 'Categoria': self.categoria,
                 'Estado': self.estado,
                 'usos': self.usos,
                 'energia': self.energia
                }
        return f'{Data}'
    
    def __copy__ (self):
        nuevo = Recurso(copy(self.nombre), copy(self.categoria), copy(self.estado), copy(self.usos), copy(self.energia))
        return nuevo

### Se inicializaran recursos siempre que empiece el programa
### y dependiendo que cuales tenga el usuario se eliminaran dichas instancias


def Inicializador_Recursos ():

    transtur1 = Recurso('Transtur1', 'Vehiculo', 'OK', 5)
    transtur2 = Recurso('Transtur2', 'Vehiculo', 'OK',5)
    camion1= Recurso('Camion1', 'Vehiculo', 'OK', 5)
    camion2 = Recurso('Camion2', 'Vehiculo', 'OK', 5)
    chofer_juan = Recurso('Juan', 'Conductor', 'OK', energia= 100)
    chofer_pedro = Recurso('Pedro', 'Conductor', 'OK', energia= 100)
    chofer_rigoberto = Recurso('Rigoberto', 'Conductor', 'OK', energia= 100)
    chofer_menendez = Recurso('Menendez', 'Conductor', 'OK', energia= 100)
    mecanico_suarez = Recurso('Suarez', 'Mecanico', 'OK', energia= 100)
    mecanico_jose = Recurso('Jose', 'Mecanico', 'OK', energia= 100)
    admin_marlon = Recurso('Marlon', 'Admin', 'OK', energia= 100)
    admin_diego = Recurso('Diego', 'Admin', 'OK', energia= 100)
    guias_federico = Recurso('Federico', 'Guia', 'OK', energia= 100)
    guia_phineas = Recurso('Phineas', 'Guia', 'OK', energia= 100)


    Recursos_disponibles = [ ###Todas las instancias inicializadas arriba
    transtur1, transtur2, camion1, camion2,
    chofer_juan,chofer_menendez, chofer_pedro,
    chofer_rigoberto, mecanico_jose, mecanico_suarez,
    admin_marlon, admin_diego, guias_federico, guia_phineas
                        ]
    
    return Recursos_disponibles