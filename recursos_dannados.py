import json
from pathlib import Path
from datetime import datetime, date, timedelta
import Recursos
import Events
import Agregar
import Jsons
from user import User
from sys import exit
import time
import Eliminar
import miscelaneo

def recursos_agotados(Recursos_disponibles, user:User):
    print('Los Vehiculos que se encuentran en mal estado son:')
    
    vehiculos = printear_Vehiculos_dannados(Recursos_disponibles) ### muestra los vehiculos y devuelve
                                                     ### una lista con ellos
    print('Las Personas agotadas son: ')
    
    personas = printear_Personas_cansadas(Recursos_disponibles)### muestra las personas y devuelve
                                                    ### una lista con ellos
    print(' ')
    print('Deseas hacer algo al respecto?')
    print('1. Si.')
    print('2. No.')
    option = miscelaneo.try_option(2)
    if option == 1:
        miscelaneo.clean()
        print('1. Llevar los Vehiculos a Mantenimiento.👨‍🔧')
        print('2. Darles a las personas unas vacaciones pagadas.🎫')
        print('3. De vuelta al menu principal.🔙')
        option = miscelaneo.try_option(3)
        if option == 1:
            miscelaneo.clean()
            if not vehiculos:
                print('No existen vehiculos que arreglar.❌')
            else:
                user = Agregar_evento_Vehiculos(vehiculos, Recursos_disponibles, user)
            return user
        elif option == 2:
            miscelaneo.clean()
            if not personas:
                print('No existen personas tales personas.❌')
            else:
                user = Agregar_evento_Personas(personas, Recursos_disponibles, user)
            return user
        elif option == 3:
            miscelaneo.clean()
            print('Los vehiculos y personas no podran usarse hasta no haberles dado solucion a sus problemas.⭕')
            return user
            
    elif option == 2:
        miscelaneo.clean()
        print('Los vehiculos y personas no podran usarse hasta no haberles dado solucion a sus problemas.⭕')
        return user

def printear_Vehiculos_dannados(Recursos_disponibles):
    vehiculos_rotos =[]
    
    for idx, recursos in enumerate(Recursos_disponibles):
        if recursos.categoria == 'Vehiculo' and recursos.usos == 0:
            print(f'* {recursos.nombre} esta roto.🔧')
            vehiculos_rotos.append(recursos)
        elif idx == len(Recursos_disponibles) - 1 and not vehiculos_rotos:
            print('---')
    return vehiculos_rotos
            
def printear_Personas_cansadas(Recursos_disponibles):
    personas_agotadas =[]
    
    for idx, recursos in enumerate(Recursos_disponibles):
        if recursos.categoria != 'Vehiculos' and recursos.energia == 0:
            print(f'* {recursos.nombre} se encuentra agotado.😴')
            personas_agotadas.append(recursos)
        elif idx == len(Recursos_disponibles) - 1 and not personas_agotadas:
            print('---')
    return personas_agotadas

def Agregar_evento_Vehiculos(vehiculos, Recursos_disponibles, user:User):
    min = timedelta(minutes= 5)
    fecha = datetime.today() + min ### creo una fecha cercana
    fecha2 = datetime.strftime(fecha, '%d/%m/%Y --- %H:%M')
    fecha_fin = fecha + timedelta(hours= 5)
    
    verif2 =Agregar.recursos_disponibles_ah(Recursos_disponibles, user, fecha2, fecha_fin, 'Mantenimiento de Vehiculos')
    
    for idx, recurso in enumerate(verif2): ### se revisa si existe algun mecanico disponible
        if recurso.categoria == 'Mecanico':
            vehiculos.append(recurso)
            break
        if idx == len(verif2) - 1:  ### si llego a este punto, no existe ninguno
            print('No hay mecanico disponible para dentro de poco.❌')
            return user
        
    mantenim = Events.Mantenimiento_Vehiculos(fecha2, *vehiculos)
    verif = Agregar.verificador_horarios_adecuados(mantenim)
      
    if not verif:
        return user
    for vehiculos in mantenim.Recursos:
        if vehiculos not in verif2: ### si algun recurso no se encuentra disponible
            print('No todo los vehiculos esta disponibles para dentro de un rato.❌')
            return user
    print('Evento agregado exitosamente.✅')
    user.events.append(mantenim)
    return user

def Agregar_evento_Personas(personas, Recursos_disponibles, user: User):
    min = timedelta(minutes= 5)
    fecha = datetime.today() + min ### creo una fecha cercana
    fecha2 = datetime.strftime(fecha, '%d/%m/%Y --- %H:%M')
    vacaciones  = Events.Vacaciones_trabajadores(fecha2, *personas)
    verif = Agregar.verificador_horarios_adecuados(vacaciones)
    verif2 =Agregar.recursos_disponibles_ah(Recursos_disponibles, user, fecha2, vacaciones.Finish_date, vacaciones.name)
    
    if not verif:
        return user
    for persona in personas:
        if persona not in verif2: ### si algun recurso no se encuentra disponible
            print('No todas las personas estan disponibles para dentro de un rato.❌')
            return user
    print('Evento agregado exitosamente.✅')
    user.events.append(vacaciones)
    return user
    

