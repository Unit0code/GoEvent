import json
from pathlib import Path
from datetime import datetime, date, timedelta
from user import User
from Recursos import Recurso
import Events
import time
import os
import copy

def recomendador_cuentas (): ### lee los archivos en la carpeta del proyecto y ve cuales son los .json 
    ruta_relativa = './'
    contenido = os.listdir(ruta_relativa)
    archivos_json = []

    clean()
    for nombre in contenido:
        if nombre.endswith('.json'):
            archivos_json.append(nombre)
    if not archivos_json:
        print('No hay cuentas existentes.')
    else:
        print('Posibles cuentas:')
        for nombre in archivos_json:
            print(nombre)
        print('')

def verificador_passw(passw : str, user:User):
    return passw == user.passw         ### verifica si la contrasenna es igual.

def try_option (max, min = 1): ###Para los errores que pudiera generar el int(input())
    while True:
        try:
            option = int(input())
            if  option > max or option < min:
                print('El valor no esta en el intervalo esperado.\nVuelva a introducirlo.')
                continue
            return option
        except Exception:
            print('El valor introducido ha generado un error.\nVuelva a introducirlo.')

def clean(): ###limpia la pantalla
    time.sleep(0.2)
    os.system('cls')

def barra_de_progreso(): ###por hacer algo chulo
    a = '🚌'
    for i in range(2):
        for j in range(7):
            print(a*j, end = '\r')
            time.sleep(0.3)
        print('                              ', end= '\r')

def mostrar_recursos(recursos_disponibles, user: User):
    clean()
    print('--------------------------------')
    for idx, recurso in enumerate(recursos_disponibles):  ### veo todos los recursos
        print(f'📎{idx + 1}. {recurso.nombre}:   categoria -> {recurso.categoria}, estado -> {recurso.estado}')
        if recurso.categoria == 'Vehiculo':
            print(f'Usos restantes: {recurso.usos}🚌🔧')
        else:
            print(f'Energia: {recurso.energia}⚡')
        ver, horarios = check_uso(recurso, user.events)
        if ver:
            print('\n📑El recurso no estara disponible en los horarios: ')
            for hora_i, hora_f in horarios:
                print(f'**⏳{hora_i}   <->   **⌛{hora_f}   ')
        print('')
    print('')

def check_uso(recurso, eventos: list):
    horarios = []
    if not eventos:
        return False, False ### lista vacia
    else:
        for evento in eventos:  ### veo en cada evento los recursos que estan en uso en algun horario
            for recurso_uso in evento.Recursos:
                if recurso_uso.nombre == recurso.nombre: ### analizo si el recurso que estoy analizando esta dentro de algun evento
                    horarios.append((evento.fecha, evento.Finish_date)) ### tomo sus horarios.
        if not horarios:
            return False, False ### por si los eventos no son vacios pero el recurso no se usa
        return True, horarios 

def verificador_estado_eventos (user: User):
    clean()
    eventos_expirados = []
    recurso_usados = []
    recursos_renovados = []
    fecha_hoy = datetime.today() ###creo la fecha de ese momento

    for idx, eventos in enumerate(user.events):  
        if eventos.Finish_date < fecha_hoy: ###chequeo si la fecha ya es pasada
            eventos_expirados.append(eventos) ###La agrego a eventos expirados
            print(f'Expiro {eventos.name}.💢')

            if eventos.name != 'Mantenimiento de Vehiculos' and eventos.name != 'Descanso pagado a los trabajadores':
                for recurso in eventos.Recursos: ### analizare que recursos se usaron para descontar a energia o uso
                    recurso_usados.append(recurso)
            else:
                for recurso in eventos.Recursos: ### se ejecuta cuando son las actividades de renovacion de estado
                    if eventos.name == 'Mantenimiento de Vehiculos' and recurso.categoria == 'Vehiculo':
                        recursos_renovados.append(recurso) ### en el mantenimiento tambien hay mecanicos, y ellos si se cansan
                        continue                           ### por eso la diferenciacion
                    elif eventos.name == 'Mantenimiento de Vehiculos':
                        recurso_usados.append(recurso)
                        continue
                    recursos_renovados.append(recurso)
    
    if not eventos_expirados: ###si la lista esta vacia solo regresara False
        print('No ha expirado ningun evento.❌')
        return user
    
    for evento in eventos_expirados:
        idx = user.events.index(evento)
        del user.events[idx] ### lo elimino de los atributos del usuario
    return user, recurso_usados, recursos_renovados

def actualizar_estado_recursos (Recursos_disponibles, recursos_recien_usados, recursos_renovados): ### actualizare el estado de cada recurso
    for recurso in recursos_recien_usados:
        for recurso2 in Recursos_disponibles:
            if recurso.nombre == recurso2.nombre and recurso2.categoria == 'Vehiculo': ### disminuyo el uso en uno
                recurso2.usos -= 1
                if recurso2.usos <3:
                    recurso2.estado = 'Deplorable'
                if recurso2.usos == 0:
                    recurso2.estado = 'Roto' ### cambiandole el estado al vehiculo
            
            elif recurso.nombre == recurso2.nombre: ### disminuyo la energia en 20 por cada evento
                recurso2.energia -= 20
                if recurso2.energia < 50:
                    recurso2.estado = 'Cansado'
                if recurso2.energia == 0:
                    recurso2.estado = 'Agotado'  ### cambio el estado segun la cantidad de energia que posea
    
    for recurso in recursos_renovados: ### renueva los recursos
        for recurso2 in Recursos_disponibles: ### funcionan especificamente para los eventos 'Vacaciones' y 'Mantenimiento'
            if recurso.nombre == recurso2.nombre and recurso2.categoria == 'Vehiculo':
                recurso2.usos = 5
                recurso2.estado = 'OK'
            elif recurso.nombre == recurso2.nombre:
                recurso2.energia = 100
                recurso2.estado = 'OK'
    
    return Recursos_disponibles

def copia_recursos (Recursos_disponibles):
    recursoscopia = []
    
    for recurs in Recursos_disponibles:
        recursoscopia.append(copy.copy(recurs))
    return recursoscopia 