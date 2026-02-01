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
import copy
import miscelaneo
import Agregar


def verificar_restricciones(evento):
    solitarias = Agregar.verificador_restricciones(evento)
    tuplas = Agregar.verificador_restricciones_tuplas(evento)
    necesidad = Agregar.verificador_necesarias(evento)
    if solitarias and tuplas and necesidad:
        return True ### si todas se cumplen, que retorne True
    return False

def recursiva (horarios): ### recibe una lista con intervalos de tiempo y los une si se interceptan
    new_horarios = horarios
    
    for idx, (x,y) in enumerate(horarios):  
        for idy, (x2, y2) in enumerate(horarios):
            if x!= x2 and y!=y2 and x <= y2 and x2 <= y: ### verifica si colisionan
                x1 = min(x,x2)
                y1 = max(y,y2)
                new_horarios[idx] = (x1,y1)
                del new_horarios[idy]   ### si lo hace, crea una nueva lista sin ambos intervalos, y el nuevo siendo la union
                return recursiva(new_horarios)  ### de ellos          
    return new_horarios   ### en el caso que no se ejecute el if, ya termino



def intervalos (horarios, Event_t): ### le suma la duracion de el evento al inicio de cada intervalo
                                    ### luego vuelve los intervalos que colisionan uno mismo.
    horarios_2 = []
    for intervalos in horarios:
        (x,y) = intervalos
        x = x - Event_t.Duration
        horarios_2.append((x,y))

    
    horarios = recursiva(horarios_2)
    return horarios


def colisiones_horarios (recursos, recursos_copia, eventos_planificados, option, Event_t):
    horarios = []
    nombres_recursos = []
    for recurs in recursos:
        nombres_recursos.append(recurs.nombre)
    nombres_recursos = set(nombres_recursos) ### convierto los nombres de la lista de recursos en un set

    if option < 11: ### Para los eventos que no son curativos
        for evento in eventos_planificados:
            recursos_copia = miscelaneo.actualizar_estado_recursos(recursos_copia, evento.Recursos,[]) ### disminuirle todos los estados
        for recurso in recursos_copia:
            if recurso.categoria == 'Vehiculo': ### si alguno de los recursos se encuentra que
                if recurso.usos <= 0:           ### ya no puede usarse antes de arreglarse, ent no existira hueco posible, hasta que se arregle.
                    print(f'El Recursos {recurso.nombre} no puede operar proximamente debido' \
                    ' a que segun la planificacion ya no da para mas, espera a que se desocupe.😊' \
                    '\n o elimine uno de los eventos planificados con este recurso.')
                    return False                    
            if recurso.categoria != 'Vehiculo':
                if recurso.energia <= 0:
                    print(f'El Recursos {recurso.nombre} no puede operar proximamente debido'\
                    ' a que segun la planificacion ya no da para mas, espera a que se desocupe.😊'\
                    '\n o elimine uno de los eventos planificados con este recurso.') 
                    return False
    
    for eventos in eventos_planificados:
        nom_re_pla = [] ### nombre de recursos planificados
        for recurs in eventos.Recursos: ### convierto la lista d recursos en un set
            nom_re_pla.append(recurs.nombre)
        nom_re_pla = set(nom_re_pla)

        if len(nombres_recursos.intersection(nom_re_pla)) > 0:  ### si su interseccion no es vacia
           horarios.append((eventos.fecha, eventos.Finish_date)) ### toma su horario
    
    if not horarios: ### si no existe alguna colision
        print('El evento se puede realizar en cualquier momento que desee, respetando sus horarios de trabajo.😊')
        return False

    horarios = intervalos(horarios, Event_t)  ### los intervalos ya en el mejor formato
    return horarios

def buscar_hueco(Usuario : User, recursos_disponibles):
    Agregar.printeo_opciones_eventos()
    option = try_option(12)
    recursos = []
    miscelaneo.clean()
    print('Eliga los recursos que necesite, presione "0" para salir.')
    recursos = Agregar.aux_agregar_eventos(recursos, recursos_disponibles) ### que eliga que recursos empleara
    recursos_copia = miscelaneo.copia_recursos(recursos) ### creo una copia de los recursos
    clase = Agregar.Relacion_evento_numeracion.get(option)
    Event_t = clase('12/12/2029 --- 12:40', *recursos_copia) ### creo el evento con horario random
    if not verificar_restricciones(Event_t): ### verificar que el evento no incumpla las restricciones de exclusion pares, particular y necesidad
        print('No es posible hacer realizar ese evento. ❌')
        return
    else:
        horarios = colisiones_horarios(recursos, recursos_copia, Usuario.events, option, Event_t)
        if not horarios: ### por si alguno de los recursos ya se encuentra dando todo segun la planificacion
            return
        print('🕐Los horarios disponibles para realizar dicho evento son:')
        for (x,y) in horarios:
            print(F'Antes del {x} o para despues del {y}.🕝')