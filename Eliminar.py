import json
from pathlib import Path
from datetime import datetime, date, timedelta
import Recursos
import Events
import Jsons
from user import User
from sys import exit
import time
from miscelaneo import clean, try_option

def eliminar_eventos (user: User): ###eliminara un evento de los agregados en el atributo eventos del user
    clean()
    eventos_no_iniciados = verificador_inicio(user.events)   ### verifica los eventos aun no iniciados
    print('------------------')
    for idx, evento in enumerate(eventos_no_iniciados):
        print(f'📎{idx + 1}. {evento.name}:    ⏳fecha de inicio -> {evento.fecha} \n    ⌛fecha de finalizacion -> {evento.Finish_date}')
        print('📑Recursos:')
        for idx, recurso in enumerate(evento.Recursos):
            print(f'      {idx + 1}. {recurso.nombre}:   categoria -> {recurso.categoria}, estado -> {recurso.estado}') ### los printea con detalles
        print('')
    
    print('Si el evento que esperabas no se muestra, probablemente es porque ya finalizo.')
    if not eventos_no_iniciados:
        print('No existen eventos que eliminar.')  ### si la lista es vacia
        return user

    print('Cual desea eliminar?❌')
    option = try_option(len(eventos_no_iniciados))
    print(f'Deseas eliminar {eventos_no_iniciados[option - 1].name}??')
    indc = option   ### para almacenar el indice del objeto en dicha lista
    print('1. Si.')
    print('2. No.')
    option = try_option(2) 
    if option == 1:      
        idx = user.events.index(eventos_no_iniciados[indc - 1]) ### veo que indice es en la lista de user.events
        del user.events[idx]   ### lo elimino
        clean()                                                                
        print('Ha sido eliminado el evento.✅')                                             
        return user
    else:
        clean()
        print('Ok. Entonces volvamos.')
        return user

def mostras_eventos(user: User): ### printea los eventos con detalles
    clean()
    if not user.events:
        print('No hay eventos por el momento.❌')
        return
    print('------------------')
    for idx, evento in enumerate(user.events):
        print(f'📎{idx + 1}. {evento.name}:    ⏳fecha de inicio -> {evento.fecha} \n    ⌛fecha de finalizacion -> {evento.Finish_date}')
        print('📑Recursos:')
        for idx, recurso in enumerate(evento.Recursos):
            print(f'        {idx + 1}. {recurso.nombre}:   categoria -> {recurso.categoria}, estado -> {recurso.estado}')
        print('')

def verificador_inicio(user_eventos:list): ### recibira los eventos del usuario, y sacara de esa lista los que ya hallan
    eventos_no_iniciados = []        ### empezado, para que no puedan ser eliminados 
    fecha_hoy = datetime.today()  ### fecha de hoy

    for evento in user_eventos:
        if evento.fecha < fecha_hoy: ### si el evento ya inicio, ignoralo
            continue
        else:
            eventos_no_iniciados.append(evento) ###si no, entonces agregalo
    return eventos_no_iniciados
        