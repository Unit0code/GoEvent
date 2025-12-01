import json
from pathlib import Path
from datetime import datetime, date, time, timedelta
from user import User
from Recursos import Recurso
import Events


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
    if not Eventos: ###si no existe la llave
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
    if not Eventos:
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

def verificador_fecha():
    while True:
        print('Introduce la fecha en el formato DIA/MES/ANNO --- HORA:MINUTOS.')
        fecha = input()
        try:
            string = datetime.strptime(fecha , '%d/%m/%Y --- %H:%M')
            fecha_hoy = datetime.today()
            if string < fecha_hoy:
                print('Esta fecha es anterior al dia de hoy. Vuelve a introducirla.')
                continue
            return fecha
        except Exception:
            print('Ha habido un error. Introduce una fecha en el formato solicitado')

def verificador_restricciones(evento): ### chequea especificamente las restricciones solitarias
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

def actualizacion_recursos_disponibles(evento, recursos_disponibles): ### Actualiza los recursos (los quita especificamente de los q se usan un nuevo evento)
    lista_nombres_recursos_evento = [] ### se ubicaran los recursos que se usan en el evento
    nuevos_recursos_disponibles = []
    
    for recursos in evento.Recursos:
        lista_nombres_recursos_evento.append(recursos.nombre)
    
    for recursos_disp in recursos_disponibles:
        if recursos_disp.nombre in lista_nombres_recursos_evento:
            continue
        nuevos_recursos_disponibles.append(recursos_disp)
    return nuevos_recursos_disponibles

def aux_agregar_eventos(lista_recursos, recursos_disponibles, user: User):
        for idx, recurso in enumerate(recursos_disponibles): ### muestra los recursos disponibles
            print(f'{idx+1}. {recurso.nombre} es un {recurso.categoria}')
        while True:
            print('Introduce 0 para salir.')
            input_user = try_option(len(recursos_disponibles), 0)
            
            if not (recursos_disponibles[input_user - 1] in lista_recursos): ### para que no se repitan
                lista_recursos.append(recursos_disponibles[input_user - 1]) 
                print(f'Agregaste a recursos para este evento a {recursos_disponibles[input_user -1].nombre}.')
            else:
                print('Ya annadiste ese recurso.') ###
            
            if input_user == 0:  ### el usuario elige entre todos los recursos disponibles
                break
        
        print('Y para cuando lo deseas?')
        fecha = verificador_fecha() ### verifica que la fecha este en el formato correcto
        return fecha, lista_recursos 

def aux_agregar_eventos2(evento_final, user, recursos_disponibles):
    
    if verificador_validez_nuevo_evento(evento_final): ###verifica si no tiene problemas y lo agrega a los eventos del usuario
        user.events.append(evento_final)
        print('Se ha agregado el evento a la agenda.')
        recursos_disponibles = actualizacion_recursos_disponibles(evento_final, recursos_disponibles) ### actualizo los recursos disponibles
        return user, recursos_disponibles
    else:
        print('El evento no se ha agendado por incumplir ciertos parametros. Vuelva a intentarlo.')
        return None

def agrego_eventos(option, recursos_disponibles, user: User): ###Agregar eventos
    print('Dime los Recursos que emplearas para este Evento.')
    
    if option == 1: #Viaje a la Habana
        
        even_temporal = Events.travel_Habana('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Habana(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles 

    elif option == 2: #viaje a guantanamo
        even_temporal = Events.travel_Gto('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Gto(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles
    
    elif option == 3: #viaje a santiago
        even_temporal = Events.travel_Stgo('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTampoco en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Al igual que ni a Juan o al camion1.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Stgo(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles
    
    elif option == 4:# viaje a camaguey
        even_temporal = Events.travel_Camaguey('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}. Al igual que Juan no puede hacer este viaje.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Camaguey(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 5: #viaje a las tunas
        even_temporal = Events.travel_Las_Tunas('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1, restr2 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)} o {dividir_lista_str(restr2)}. Al igual que Juan no puede hacer este viaje.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Las_Tunas(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 6: #viaje a las villas
        even_temporal = Events.travel_Las_Villas('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Las_Villas(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 7: #viaje a pinar del rio
        even_temporal = Events.travel_Pinar_Rio('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Pinar_Rio(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 8: #viaje a matanzas
        even_temporal = Events.travel_Mtz('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Mtz(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 9: #viaje a cienfuegos
        even_temporal = Events.travel_Cienfuegos('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}. Y no seria sugerible emplear al camion2.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.travel_Cienfuegos(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 10: #mantenimiento de vehiculos
        even_temporal = Events.Mantenimiento_Vehiculos('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        restr1 = even_temporal.Restriction_recursos_pares  ### tomo las restricciones de pares
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden estar juntos {dividir_lista_str(restr1)}.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.Mantenimiento_Vehiculos(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles

    elif option == 11: #boteo en la habana
        even_temporal = Events.Botear_Habana('10/10/2005 --- 12:40', 1) ###inicializo una instancia cualquiera temporal
        lista_recursos = [] ### aqui iran los recursos que el usuario decida

        print(f'Este en especifico necesita de {dividir_lista_str(even_temporal.Needs)}. \nTambien en este viaje\
 no pueden es muy necesario que vaya alguno de los guias.')
        print('Toma los que necesites.')
        print('Escribe 0 para avisar que ya terminaste.')
        
        fecha, lista_recursos = aux_agregar_eventos(lista_recursos, recursos_disponibles, user) ### auxiliar de esta funcion
        evento_final = Events.Botear_Habana(fecha, *lista_recursos)
        try:
            user, recursos_disponibles = aux_agregar_eventos2(evento_final, user, recursos_disponibles) ## 2do auxiliar
        except Exception:
            pass
        return user, recursos_disponibles
