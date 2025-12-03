import json
from pathlib import Path
from datetime import datetime, date, timedelta
from user import User
from Recursos import Recurso
import Events
import time
import os


def guardar_json (usuario : User): ###guardar los avances en un json con un path 'nombre_user'.json
    data = usuario.__dict__()
    for llave, valor in data.items(): ###convertir todos los tipos en un dict para ser guardados.
        if llave == 'Eventos':
            for idx, eventos in enumerate(valor): ###Itero en los eventos 
                for idc, recursos_evento in enumerate(eventos.Recursos): ###itero en los recursos de ese evento
                    eventos.Recursos[idc] = recursos_evento.__dict__()   ###cada evento lo vuelvo un dict
                valor[idx] = eventos.__dict__() ### y finalizo ese evento volviendolo un dict tambien

    data = json.dumps(data)  ###lo vuelvo un tipo json
    path_user = Path(f'{usuario.path}.json')  ### inicializo una instancia Path 
    path_user.write_text(data)  ### y escribo en el archivo con ese path
    return 'Hecho.'

def cargar_json (path : str):
    path_user = Path(f'{path}.json')
    
    try:
        data_user = path_user.read_text()
    except FileNotFoundError:
        print(f"El archivo con direccion {path_user} no existe.") ###Si el archivo no existe
        return False
    else:
        data_user = json.loads(data_user)
        data_user = inicializar_obj_cargados(data_user) ### se inicializan los tipos recursos y datetime en cada event
        data_user = inicializar_eventos(data_user) ### se inicializan los eventos
        user = inicializar_user(data_user, path) ### se inicializa el usuario
        return user
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
                    recurso_obj = Recurso(nombre, categoria, estado) ### creacion de las inst recursos
                    valor[idc] = recurso_obj
    data_user['Eventos'] = Eventos
    return data_user  ### devuelve los eventos con todos sus tipos inicializados, exceptuando el mismo Evento

def inicializar_eventos (data_user):
    Eventos = data_user.get('Eventos', False)
    if not Eventos and type([]) != type(Eventos):  ### si no existe la llave o no es una lista vacia
        return False
    for idx, evento_p in enumerate(Eventos): ### tomo sus atributos
        nombre = evento_p['Nombre']
        fecha = evento_p['Fecha inicio']
        recursos = evento_p['Recursos']
        
        if nombre == 'Viaje a la Habana':   ### dependiendo del nombre inicializo la instancia Evento(tipo especif)
            evento_p = Events.travel_Habana(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Guantanamo':
            evento_p = Events.travel_Gto(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Santiago de Cuba':
            evento_p = Events.travel_Stgo(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Camaguey':
            evento_p = Events.travel_Camaguey(fecha, *recursos)
            Eventos[idx] = evento_p

        elif nombre == 'Viaje a Las Tunas':
            evento_p = Events.travel_Las_Tunas(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Las Villas':
            evento_p = Events.travel_Las_Villas(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Pinar del Rio': ###
            evento_p = Events.travel_Pinar_Rio(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Matanzas':
            evento_p = Events.travel_Mtz(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Viaje a Cienfuegos':
            evento_p = Events.travel_Cienfuegos(fecha, *recursos)
            Eventos[idx] = evento_p

        elif nombre == 'Mantenimiento de Vehiculos':
            evento_p = Events.Mantenimiento_Vehiculos(fecha, *recursos)
            Eventos[idx] = evento_p
        
        elif nombre == 'Boteo en la Habana':
            evento_p = Events.Botear_Habana(fecha, *recursos)
            Eventos[idx] = evento_p
    data_user['Eventos'] = Eventos
    return data_user

def inicializar_user (data_user, path):
    nombre = data_user['Nombre']
    passw = data_user['Passw']
    path_r = path
    eventos = data_user['Eventos']
    user = User(nombre, passw, path_r, eventos)
    return user
            
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

def printeo_opciones_eventos(): ###Printea los posibles eventos
    clear()
    print('1. Viaje a la Habana.')
    print('2. Viaje a Guantanamo.')
    print('3. Viaje a Santiago de Cuba.')
    print('4. Viaje a Camaguey.')
    print('5. Viaje a Las Tunas.')
    print('6. Viaje a Las Villas.')
    print('7. Viaje a Pinar del Rio.')
    print('8. Viaje a Matanzas.')
    print('9. Viaje a Cienfuegos.')
    print('10. Mantenimiento de Vehiculos.')
    print('11. Boteo en la Habana.')

def dividir_lista_str(lista): ###la implemente yo porque no tengo megas y se que existe pero no se cual es.
    string = ''
    for idx, x in enumerate(lista):
        string += str(x)
        if idx == len(lista) -1:
            return string
        string += ', '

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
            return fecha, fecha_fin
        except Exception:
            print('Ha habido un error. Introduce una fecha en el formato solicitado')

def verificador_restricciones(evento): ### chequea especificamente las restricciones solitarias
    clear()
    for recursos in evento.Recursos:
        for restr, mssg in evento.Restriction_recursos.items(): ###ve las restricciones que hay y si coinciden con los nombre
            if recursos.nombre == restr:                        ### de los recursos
                print(f'{recursos.nombre + ' '+ mssg} ')
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
        print(f'Propon el mismo evento sobre las {evento.Restriction_hour[0]}')
        return False
    elif tiempo > evento.Restriction_hour[1]:
        print('Estas intentando hacerlo demasiado tarde. Mejor duerme a esa hora.')
        print(f'Propon el mismo evento sobre las {evento.Restriction_hour[1]}')
        return False
    return True

def verificador_validez_nuevo_evento(evento): ###llama a todas las funciones que chequean que el evento pueda agregarse
    restricciones_solitarias = verificador_restricciones(evento)
    restricciones_tuplas = verificador_restricciones_tuplas(evento)  ### todos devuelven False si el evento incumple algo
    recursos_necesarios = verificador_necesarias(evento)
    horario_adecuado = verificador_horarios_adecuados(evento)
    if not recursos_necesarios or not horario_adecuado or not restricciones_solitarias or not restricciones_tuplas:
        return False
    else:
        return True

def aux_agregar_eventos(lista_recursos, recursos_disponibles):
        for idx, recurso in enumerate(recursos_disponibles): ### muestra los recursos disponibles ahora
            print(f'{idx+1}. {recurso.nombre} es un {recurso.categoria}')
        while True:
            print('Introduce 0 para salir.')
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
        return None, None  ###doble none para que de error y se ejecute el try-exception

def agrego_eventos(option, recursos_disponibles, user: User): ###Agregar eventos
    clear()
    print('Dime la fecha en la que deseas realizarlo.')
    
    if option == 1: #Viaje a la Habana
        
        even_temporal = Events.travel_Habana('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print('Ahora dime los recursos que emplearas.')
        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Habana(fecha, *lista_recursos)
        
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 2: #viaje a guantanamo
        even_temporal = Events.travel_Gto('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Gto(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user
    
    elif option == 3: #viaje a santiago
        even_temporal = Events.travel_Stgo('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares[0]  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTampoco en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Al igual que ni a Juan o al camion1.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Stgo(fecha, *lista_recursos)
        try:
            user= aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user
    
    elif option == 4:# viaje a camaguey
        even_temporal = Events.travel_Camaguey('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}. Al igual que Juan no puede hacer este viaje.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Camaguey(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 5: #viaje a las tunas
        even_temporal = Events.travel_Las_Tunas('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}. Al igual que Juan no puede hacer este viaje.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Las_Tunas(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 6: #viaje a las villas
        even_temporal = Events.travel_Las_Villas('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares[0]  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Las_Villas(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 7: #viaje a pinar del rio
        even_temporal = Events.travel_Pinar_Rio('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares[0]  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Pinar_Rio(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 8: #viaje a matanzas
        even_temporal = Events.travel_Mtz('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares[0]  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Mtz(fecha, *lista_recursos)
        try:
            user= aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 9: #viaje a cienfuegos
        even_temporal = Events.travel_Cienfuegos('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares[0]  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.travel_Cienfuegos(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 10: #mantenimiento de vehiculos
        even_temporal = Events.Mantenimiento_Vehiculos('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares[0]  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.Mantenimiento_Vehiculos(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

    elif option == 11: #boteo en la habana
        even_temporal = Events.Botear_Habana('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        lista_recursos = [] ### aqui iran los recursos que el usuario decida
        fecha, fecha_fin = verificador_fecha(even_temporal.Duration) ### verifica que la fecha este en el formato correcto

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no es muy necesario que vaya alguno de los guias.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        recursos_disponibles_ahora = recursos_disponibles_horario_especifico(recursos_disponibles, user, fecha, fecha_fin)
        lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles_ahora) ### auxiliar de esta funcion
        evento_final = Events.Botear_Habana(fecha, *lista_recursos)
        try:
            user = aux_agregar_eventos2(evento_final, user) ## 2do auxiliar
        except Exception:
            pass
        return user

def eliminar_eventos (user: User): ###eliminara un evento de los agregados en el atributo eventos del user
    clear()
    for idx, evento in enumerate(user.events):
        print(f'{idx + 1}. {evento.name}:    fecha de inicio -> {evento.fecha} \nfecha de finalizacion -> {evento.Finish_date}')
        print('Recursos:')
        for idx, recurso in enumerate(evento.Recursos):
            print(f'  {idx + 1}. {recurso.nombre}:   categoria -> {recurso.categoria}, estado -> {recurso.estado}')
        print('')
    if not user.events:
        print('No existen eventos que eliminar.')
        return False
    
    print('Cual desea eliminar?')
    option = try_option(len(user.events))
    print(f'Deseas eliminar {user.events[option - 1].name}??')
    print('1. Si.')
    print('2. No')
    option = try_option(2) 
    if option == 1:
        del user.events[option - 1]
        clear()                                                                
        print('Ha sido eliminado el evento.')                                             
        return user
    else:
        clear()
        print('Ok. Entonces volvamos.')
        return user

def mostras_eventos(user: User):
    clear()
    for idx, evento in enumerate(user.events):
        print(f'{idx + 1}. {evento.name}:    fecha de inicio -> {evento.fecha} \nfecha de finalizacion -> {evento.Finish_date}')
        print('Recursos:')
        for idx, recurso in enumerate(evento.Recursos):
            print(f'   {idx + 1}. {recurso.nombre}:   categoria -> {recurso.categoria}, estado -> {recurso.estado}')
        print('')
    if not user.events:
        print('No hay eventos por el momento')

def mostrar_recursos(recursos_disponibles, user: User):
    clear()
    
    for idx, recurso in enumerate(recursos_disponibles):  ### veo todos los recursos
        print(f'{idx + 1}. {recurso.nombre}:   categoria -> {recurso.categoria}, estado -> {recurso.estado}')
        ver, horarios = check_uso(recurso, user.events)
        if ver:
            print('El recurso no estara disponible en los horarios: ')
            for hora_i, hora_f in horarios:
                print(f'**{hora_i}   <->   **{hora_f}   ')
        print('')
    print('')

def verificador_estado_eventos (user: User):
    clear()
    eventos_expirados = []
    fecha_hoy = datetime.today() ###creo la fecha de ese momento

    for idx, eventos in enumerate(user.events):  
        if eventos.Finish_date < fecha_hoy: ###chequeo si la fecha ya es pasada
            eventos_expirados.append(eventos) ###La agrego a eventos expirados
            print(f'Expiro {eventos.name}.')
    
    if not eventos_expirados: ###si la lista esta vacia solo regresara False
        print('No ha expirado ningun evento.')
        return False
    
    for evento in eventos_expirados:
        idx = user.events.index(evento)
        del user.events[idx] ### lo elimino de los atributos del usuario
    return user

def barra_de_progreso(): ###por hacer algo chulo
    a = '.'
    for i in range(3):
        for j in range(7):
            print(a * j, end = '\r')
            time.sleep(0.3)
        print('           ', end= '\r')

def clear(): ###limpia la pantalla
    time.sleep(0.4)
    os.system('cls')      

def verificador_passw(passw : str, user:User):
    return passw == user.passw         ### verifica si la contrasenna es igual.

def recursos_disponibles_horario_especifico(recursos_disponibles,user:User,fecha: str, fecha_fin): ### verificara 
    fecha = datetime.strptime(fecha,'%d/%m/%Y --- %H:%M')                                       ###que recursos estan disponibles en un horario dado
    recursos_disponibles_ahora = []  ###agregare los recursos disponibles en ese horario
    recursos_en_uso = []
    for evento in user.events:                                                                  
        if evento.fecha <= fecha_fin and evento.Finish_date  >= fecha: ### condicion para que dos intervalos de tiempo colisionen
            for recurso in evento.Recursos:  ### indexo en los recursos del evento si colisionan
                recursos_en_uso.append(recurso.nombre) ### le agrego el nombre de cada recursos en uso
    for recurso_disp in recursos_disponibles:
        if recurso_disp.nombre in recursos_en_uso: ### si el nombre de dicho recurso esta en uso, no lo agregues
            continue
        else:  
            recursos_disponibles_ahora.append(recurso_disp) ### agrega los que no estan en uso
    return recursos_disponibles_ahora

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