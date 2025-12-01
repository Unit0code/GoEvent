import json
from pathlib import Path
from datetime import datetime, date, time, timedelta
import Recursos
import Events
import funtion
import user
from sys import exit

name_user = ''
Recursos_disponibles = Recursos.Recursos_disponibles
###inicio del programa
while True:
    print('Hola, Bienvenido al Gestor de tareas para tu empresa de vehiculos.')
    print('1. Crearse una cuenta.')
    print('2. Cargar una cuenta.')
    print('3. Salir del Programa.')

    option = funtion.try_option(3)
    if option == 1:  ### Creacion de nueva cuenta
        while True:    
            print('Perfecto, entonces, cual sera tu nombre?')
            name_user = input()
            print('Y ahora establezcamos una contrasenna para asegurarnos de que nadie acceda a tu perfil.')
            passw = input()
            print(f'Tu perfil sera {name_user} con contrasenna {passw}, estas de acuerdo?')
            print('1. Si \n2. No \n3. Ir al menu principal.')
            option = funtion.try_option(3)
            if option == 1:
                Usuario = user.User(name_user, passw, name_user, []) ### creo el usuario
                print(f'Bienvenido {name_user}')
                while True:
                    print('Que deseas?')
                    print('1. Agregar Eventos a tu agenda.') ################### agregar nuevos eventos ????
                    print('2. Eliminar Eventos de tu agenda.') 
                    print('3. Ver los Eventos agendados.')
                    print('4. Ver los Recursos y su disponibilidad.')
                    print('5. Actualizar Agenda.')
                    print('6. Salir al menu principal.')

                    option = funtion.try_option(6)
                    if option == 1: ### Agrega eventos como al usuario le plazca
                        print('Tienes para agregar:')
                        funtion.printeo_opciones_eventos() ### printea las opciones
                        option = funtion.try_option(11)
                        try:    ###hace todo el proceso de arreglo
                            Usuario, Recursos_disponibles = funtion.agrego_eventos(option, Recursos_disponibles, Usuario) 
                        except Exception:
                            pass

                    elif option == 2:
                        print('Veamos cuales tienes y puedes eliminar.')
                        Usuario, Recursos_disponibles = funtion.eliminar_eventos(Usuario, Recursos_disponibles) ### se encarga de eliminar eventos.

                    elif option == 3:
                        print('Los Eventos agendados hasta el momento son:')
                        funtion.mostras_eventos(Usuario) ### indexa en los eventos con un for y los printea
                    
                    elif option == 4:
                        print('Los recursos disponibles en este momento son:')
                        funtion.mostrar_recursos(Recursos_disponibles)
                    
                    elif option == 5:
                        print('Veamos si no hay ningun Evento que ya haya expirado.')
                        try:
                            Usuario, Recursos_disponibles = funtion.verificador_estado_eventos(Usuario, Recursos_disponibles)
                        except Exception:
                            pass

                    elif option == 6:
                        print('Primero, guardemos el perfil, para asegurarnos de que no se pierda la info.')
                        funtion.guardar_json(Usuario)
                        
                        break
            
            elif option == 2: ### Va a la sgt iteracion del bucle.
                continue
            elif option == 3: ### Rompe el bucle y vuelve al menu inicial.
                break
            
            if option == 6: ###Esta opcion solo entrara en ella cuando haya estado ya en la cuenta
                break       ### y haya posterior a eso salido.


    elif option == 2:
        pass
    elif option == 3:
        print(f'Hasta luego {name_user}.')
        exit()