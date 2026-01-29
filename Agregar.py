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

Relacion_evento_numeracion = { 1: Events.travel_Habana, 2: Events.travel_Gto,
3: Events.travel_Stgo, 4: Events.travel_Camaguey, 5: Events.travel_Las_Tunas,
6: Events.travel_Las_Villas, 7: Events.travel_Pinar_Rio, 8: Events.travel_Mtz,
9: Events.travel_Cienfuegos, 10: Events.Botear_Habana, 11: Events.Mantenimiento_Vehiculos,
12: Events.Vacaciones_trabajadores } 
### estas son para identificar que numeracion tiene asignada cada evento

def printeo_opciones_eventos(): ###Printea los posibles eventos
    clean()
    print('1. Viaje a la Habana.')
    print('2. Viaje a Guantanamo.')
    print('3. Viaje a Santiago de Cuba.')
    print('4. Viaje a Camaguey.')
    print('5. Viaje a Las Tunas.')
    print('6. Viaje a Las Villas.')
    print('7. Viaje a Pinar del Rio.')
    print('8. Viaje a Matanzas.')
    print('9. Viaje a Cienfuegos.')
    print('10. Boteo en la Habana.')
    print('11. Mantenimiento de Vehiculos.')
    print('12. Descanso pagado a los trabajadores.')

def agrego_eventos(option, recursos_disponibles, user: User): ###Agregar eventos
    clean()
    print('Dime la fecha en la que deseas realizarlo.')

    if option == 1: #Viaje a la Habana
        even_temporal = Events.travel_Habana('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Habana(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 2: #viaje a guantanamo
        even_temporal = Events.travel_Gto('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Gto(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)
    
    elif option == 3: #viaje a santiago
        even_temporal = Events.travel_Stgo('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Stgo(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)
    
    elif option == 4:# viaje a camaguey
        even_temporal = Events.travel_Camaguey('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Camaguey(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 5: #viaje a las tunas
        even_temporal = Events.travel_Las_Tunas('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Las_Tunas(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 6: #viaje a las villas
        even_temporal = Events.travel_Las_Villas('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Las_Villas(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 7: #viaje a pinar del rio
        even_temporal = Events.travel_Pinar_Rio('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Pinar_Rio(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 8: #viaje a matanzas
        even_temporal = Events.travel_Mtz('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Mtz(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 9: #viaje a cienfuegos
        even_temporal = Events.travel_Cienfuegos('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.travel_Cienfuegos(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

    elif option == 10: #boteo en la habana
        even_temporal = Events.Botear_Habana('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.Botear_Habana(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)
    
    elif option == 11: #mantenimiento de vehiculos
        even_temporal = Events.Mantenimiento_Vehiculos('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.Mantenimiento_Vehiculos(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)
    
    elif option == 12: #descanso para trabajadores
        even_temporal = Events.Vacaciones_trabajadores('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        fecha, lista_recursos = proceso_agregar(even_temporal, user, recursos_disponibles)
        evento_final = Events.Vacaciones_trabajadores(fecha, *lista_recursos) ### se crea el evento
        return proceso_agregar2(evento_final, user)

def proceso_agregar (even_temporal, user: User, recursos_disponibles): ### Aqui se reune todas las funciones para crear y verificar el evento
    
    
    lista_recursos = [] ### aqui iran los recursos que el usuario decida
    fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto
    
    print('Ahora dime los recursos que emplearas.')
    print(f'Este evento en especifico necesita de {dividir_lista_str(even_temporal.Needs)}.')

    if even_temporal.Restriction_recursos: ### printera todas las excepciones que no se pueden usar en el evento
        for restr1 in even_temporal.Restriction_recursos:
            print(f'No puede ir a dicho viaje {restr1}.')
    if even_temporal.Restriction_recursos_pares: 
        for (restr1, restr2) in even_temporal.Restriction_recursos_pares:
            print(f'En este viaje no pueden estar juntos {restr1} y {restr2}')
    print(" ")
    print('Toma los que necesites. Estos son los disponibles en dicho horario.')
    print('Escribe 0 para avisar que ya terminaste.')

    recursos_disponibles_a = recursos_disponibles_ah(recursos_disponibles, user, fecha, fecha_fin, even_temporal.name) ### aqui veo los recursos disponibles en ese intervalo
    lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_a) ### para que el usuario elija los recursos
    return fecha, lista_recursos

def proceso_agregar2 (evento_final, user):
    try:
        user = aux_agregar_eventos2(evento_final, user) ## verifica que no incumpla nada
    except Exception:
        pass
    return user

def aux_agregar_eventos(lista_recursos, recursos_disponibles):
        for idx, recurso in enumerate(recursos_disponibles): ### muestra los recursos disponibles ahora
            print(f'{idx+1}. {recurso.nombre} es un {recurso.categoria}')
        while True:
            print('Introduce "0" para salir.')
            input_user = try_option(len(recursos_disponibles), 0)
            
            if input_user == 0:  ### el usuario elige entre todos los recursos disponibles
                break
            elif not (recursos_disponibles[input_user - 1] in lista_recursos): ### para que no se repitan
                lista_recursos.append(recursos_disponibles[input_user - 1]) 
                print(f'Agregaste a recursos para este evento a {recursos_disponibles[input_user -1].nombre}.')
            else:
                print('Ya annadiste ese recurso.') ###

        return lista_recursos

def aux_agregar_eventos2(evento_final, user):
    
    if verificador_validez_nuevo_evento(evento_final): ###verifica si no tiene problemas y lo agrega a los eventos del usuario
        user.events.append(evento_final)
        print('Se ha agregado el evento a la agenda.')
        return user
    else:
        print('El evento no se ha agendado por incumplir ciertos parametros. Vuelva a intentarlo.')
        return user

def verificador_fecha(duration_event):  ### recibe la duracion del evento para que me devuelva la fecha fin
    while True:
        print('Introduce la fecha en el formato DIA/MES/ANNO --- HORA:MINUTOS.')
        fecha = input()
        try:
            string = datetime.strptime(fecha , '%d/%m/%Y --- %H:%M')
            fecha_hoy = datetime.today()
            if string < fecha_hoy:
                print('Esta fecha es anterior al dia de hoy. Vuelve a introducirla.')
                continue
            fecha_fin = string + duration_event
            clean()
            return fecha, fecha_fin
        except Exception:
            print('Ha habido un error. Introduce una fecha en el formato solicitado')

def verificador_restricciones(evento): ### chequea especificamente las restricciones solitarias
    clean()
    for recursos in evento.Recursos:
        for restr, mssg in evento.Restriction_recursos.items(): ###ve las restricciones que hay y si coinciden con los nombre
            if recursos.nombre == restr:                        ### de los recursos
                print(f'{recursos.nombre + 'no deberia ir en este viaje. '+ mssg} ')
                return False
    return True

def verificador_restricciones_tuplas(evento): ###chequea especificamente las restricciones en tuplas
    lista_nombres_recursos = []
    for recursos in evento.Recursos:
        lista_nombres_recursos.append(recursos.nombre) ### tomo todos los nombres de los recursos que se agregaron
    
    for idx, tupla_restriccion in enumerate(evento.Restriction_recursos_pares):  
        if set(tupla_restriccion) <= set(lista_nombres_recursos):  ### comparo si la tupla restringida esta dentro de los nombres
            print(f'{dividir_lista_str(tupla_restriccion)} no pueden estar juntos, {evento.message[idx]}')
            return False
    return True

def verificador_necesarias (evento): ###chquea si cumple con los recursos necesarios
    lista_nombres_recursos = []
    for recursos in evento.Recursos:
        lista_nombres_recursos.append(recursos.nombre) ### tomo todos los nombres de los recursos que se agregaron
        lista_nombres_recursos.append(recursos.categoria) ### y las categorias tambien

    if set(evento.Needs) <= set(lista_nombres_recursos): ### verifica si las necesidades estan dentro de los recursos
        return True
    print('Te faltan recursos necesarios para empezar el evento.')
    return False

def verificador_horarios_adecuados (evento): ###chequea si esta en el intervalo de tiempo en el que se puede iniciar este evento
    tiempo = evento.fecha.time()
    if tiempo < evento.Restriction_hour[0]: 
        print('Estas intentando hacerlo muy temprano. No madruges tanto.')
        print(f'Propon el mismo evento a partir de las {evento.Restriction_hour[0]}')
        return False
    elif tiempo > evento.Restriction_hour[1]:
        print('Estas intentando hacerlo demasiado tarde. Mejor duerme a esa hora.')
        print(f'Propon el mismo evento antes de las {evento.Restriction_hour[1]}')
        return False
    return True

def verificador_validez_nuevo_evento(evento): ###llama a todas las funciones que chequean que el evento pueda agregarse
    restricciones_solitarias = verificador_restricciones(evento)
    restricciones_tuplas = verificador_restricciones_tuplas(evento)  ### todos devuelven False si el evento incumple algo
    recursos_necesarios = verificador_necesarias(evento)
    horario_adecuado = verificador_horarios_adecuados(evento)
    estado = recursos_saludables(evento)
    
    if not recursos_necesarios or not horario_adecuado or not restricciones_solitarias or not restricciones_tuplas or not estado:
        return False
    else:
        return True

def dividir_lista_str(lista): ###la implemente yo porque no tengo megas y se que existe pero no se cual es.
    string = ''
    for idx, x in enumerate(lista):
        string += str(x)
        if idx == len(lista) -1:
            return string
        string += ', '

def recursos_disponibles_ah(recursos_disponibles,user:User,fecha: str, fecha_fin, nombre_evento): ### verificara 
    fecha = datetime.strptime(fecha,'%d/%m/%Y --- %H:%M')                                      ###que recursos estan disponibles en un horario dado
    recursos_disponibles_ahora = []  ###agregare los recursos disponibles en ese horario
    recursos_en_uso = []
    
    for evento in user.events:                                                                  
        if evento.fecha <= fecha_fin and evento.Finish_date  >= fecha: ### condicion para que dos intervalos de tiempo colisionen
            for recurso in evento.Recursos:  ### indexo en los recursos del evento si colisionan
                recursos_en_uso.append(recurso.nombre) ### le agrego el nombre de cada recursos en uso
    
    recursos_excedidos = revision_recursos_excedidos(nombre_evento, user, recursos_disponibles) 
    recursos_en_uso += recursos_excedidos

    for recurso_disp in recursos_disponibles:
        if recurso_disp.nombre in recursos_en_uso: ### si el nombre de dicho recurso esta en uso, no lo agregues
            continue
        else:  
            recursos_disponibles_ahora.append(recurso_disp) ### agrega los que no estan en uso

    return recursos_disponibles_ahora

def recursos_saludables (evento):  ### verificar que todos los recursos estan en buen estado
    if evento.name != 'Descanso pagado a los trabajadores' and evento.name != 'Mantenimiento de Vehiculos':
        for recurso in evento.Recursos:
            if recurso.usos == 0:
                print(f'El Recurso {recurso.nombre} se encuentra roto, necesitas llevarlo a "Mantenimiento de Vehiculos".')
                return False
            elif recurso.energia == 0:
                print(f'El compannero {recurso.nombre} no tiene energia, debes darle un merecido descanso.')
                return False
    return True

def revision_recursos_excedidos (nombre_evento: str, user: User, recursos_disponibles:list):
    recursos_excedidos = []
    recursoscopia = []

    for recurs in recursos_disponibles:
        recursoscopia.append(copy.copy(recurs))                                                   
    
    if nombre_evento != 'Mantenimiento de Vehiculos' and nombre_evento!='Descanso pagado a los trabajadores':
        for evento in user.events:
            if evento.name != 'Mantenimiento de Vehiculos' and evento.name !='Descanso pagado a los trabajadores':
                for recurso in evento.Recursos:
                    if recurso.categoria == 'Vehiculo':
                        idx = comparador_nombres(recursoscopia, recurso)
                        recursoscopia[idx].usos -=1
                    else:
                        idx = comparador_nombres(recursoscopia, recurso)
                        recursoscopia[idx].energia -= 20
            elif evento.name == 'Mantenimiento de Vehiculos':
                for recurso in evento.Recursos:
                    if recurso.categoria != 'Vehiculo':
                        idx = comparador_nombres(recursoscopia, recurso)
                        recursoscopia[idx].energia -= 20
    
        for recurso in recursoscopia:
            if recurso.categoria == 'Vehiculo':
                if recurso.usos <= 0:
                    recursos_excedidos.append(recurso.nombre)
            elif recurso.energia <= 0:
                recursos_excedidos.append(recurso.nombre)
    return recursos_excedidos
    ### esta funcion en especifico se encarga de revisar si los recursos ya se le agendaron a eventos de
    ### forma tal que cuando los terminen, ya no tengan energia/uso, entonces no se mostraran para crear un nuevo evento 

def comparador_nombres (lista1, elemento):
    for idx, x in enumerate(lista1):
        if x.nombre == elemento.nombre:
            return idx