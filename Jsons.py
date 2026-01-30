import json
from pathlib import Path
from datetime import datetime, date, timedelta
from user import User
from Recursos import Recurso
import Events
import time
import os
import miscelaneo

Relacion_nombre_evento = { 'Viaje a la Habana': Events.travel_Habana,
 'Viaje a Guantanamo': Events.travel_Gto, 'Viaje a Santiago de Cuba': Events.travel_Stgo,
 'Viaje a Camaguey': Events.travel_Camaguey, 'Viaje a Las Tunas': Events.travel_Las_Tunas,
'Viaje a Las Villas': Events.travel_Las_Villas, 'Viaje a Pinar del Rio': Events.travel_Pinar_Rio,
 'Viaje a Matanzas': Events.travel_Mtz, 'Viaje a Cienfuegos': Events.travel_Cienfuegos,
'Boteo en la Habana': Events.Botear_Habana, 'Mantenimiento de Vehiculos': Events.Mantenimiento_Vehiculos,
'Descanso pagado a los trabajadores': Events.Vacaciones_trabajadores } 

def guardar_json (usuario : User, Recursos_disponibles): ###guardar los avances en un json con un path 'nombre_user'.json
    data = usuario.__dict__()
    for llave, valor in data.items(): ###convertir todos los tipos en un dict para ser guardados.
        if llave == 'Eventos':
            for idx, eventos in enumerate(valor): ###Itero en los eventos 
                for idc, recursos_evento in enumerate(eventos.Recursos): ###itero en los recursos de ese evento
                    eventos.Recursos[idc] = recursos_evento.__dict__()   ###cada evento lo vuelvo un dict
                valor[idx] = eventos.__dict__() ### y finalizo ese evento volviendolo un dict tambien

    Recursos_disponibles = miscelaneo.copia_recursos(Recursos_disponibles)

    for idx, recurso in enumerate(Recursos_disponibles):
        recurso = recurso.__dict__()
        Recursos_disponibles[idx] = recurso ### guardo los recursos globales en el estado que se encuentran

    data['Recursos_disponibles'] = Recursos_disponibles

    data = json.dumps(data)  ###lo vuelvo un tipo json
    path_user = Path(f'{usuario.path}.json')  ### inicializo una instancia Path 
    path_user.write_text(data)  ### y escribo en el archivo con ese path
    return 'Hecho.'

def cargar_json (path : str, recursos_disponibles):
    path_user = Path(f'{path}.json')
    
    try:
        data_user = path_user.read_text()
    except FileNotFoundError:
        print('')
        print(f"El archivo con direccion {path_user} no existe.❌") ###Si el archivo no existe
        return False, recursos_disponibles
    else:
        data_user = json.loads(data_user)
        data_user, recursos_disponibles = inicializar_obj_cargados(data_user) ### se inicializan los tipos recursos y datetime en cada event
        data_user = inicializar_eventos(data_user) ### se inicializan los eventos
        user = inicializar_user(data_user, path) ### se inicializa el usuario
        return user, recursos_disponibles
    ### llamar a todas las funciones de iniacializacion
    
def inicializar_obj_cargados (data_user): ### cuando cargue el archivo, se deben inicializar todos los tipos
    Eventos = data_user.get('Eventos', False)
    if not Eventos and type([]) != type(Eventos): ###si no existe la llave y no es una lista vacia
        return False
    for idx, evento_p in enumerate(Eventos): ### por cada evento
        for llave, valor in evento_p.items(): ### vere las caracteristicas de dicho evento
            if llave == 'Recursos':  ### instancias recursos
                for idc, recurso in enumerate(valor): ### por cada recurso
                    nombre = recurso['Nombre']
                    categoria = recurso['Categoria']
                    estado = recurso['Estado']
                    usos = recurso['usos']
                    energia = recurso['energia']
                    recurso_obj = Recurso(nombre, categoria, estado, usos, energia) ### creacion de las inst recursos
                    valor[idc] = recurso_obj
    data_user['Eventos'] = Eventos

    recursos_disponibles = data_user['Recursos_disponibles']
    for idx, recurso in enumerate(recursos_disponibles):  ### inicializo los recursos en el estado que se quedaron
        nombre = recurso['Nombre']
        categoria = recurso['Categoria']
        estado = recurso['Estado']
        usos = recurso['usos']
        energia = recurso['energia']
        recurso_obj = Recurso(nombre, categoria, estado, usos, energia) ### creacion de las inst recursos
        recursos_disponibles[idx] = recurso_obj

    return data_user, recursos_disponibles  ### devuelve los eventos con todos sus tipos inicializados, exceptuando el mismo Evento

def inicializar_eventos (data_user):
    Eventos = data_user.get('Eventos', False)
    if not Eventos and type([]) != type(Eventos):  ### si no existe la llave o no es una lista vacia
        return False
    for idx, evento_p in enumerate(Eventos): ### tomo sus atributos
        nombre = evento_p['Nombre']
        fecha = evento_p['Fecha inicio']
        recursos = evento_p['Recursos']

        clase = Relacion_nombre_evento.get(nombre) ### busco cual es la clase con mismo nombre
        evento_p = clase(fecha, *recursos) ### creo el evento
        Eventos[idx] = evento_p ### lo agrego a la lista de eventos del user

    data_user['Eventos'] = Eventos
    return data_user

def inicializar_user (data_user, path):
    nombre = data_user['Nombre']
    passw = data_user['Passw']
    path_r = path
    eventos = data_user['Eventos']
    user = User(nombre, passw, path_r, eventos)
    return user
