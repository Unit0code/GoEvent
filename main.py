import json
from pathlib import Path
from datetime import datetime, date, timedelta
import Recursos
import Events
import funtion
import user
from sys import exit
import time

name_user = ''
Recursos_disponibles = Recursos.Recursos_disponibles
###inicio del programa
while True:
    funtion.clear()
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
                funtion.clear()
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
                        try:    ###hace todo el proceso de agrego
                            Usuario = funtion.agrego_eventos(option, Recursos_disponibles, Usuario) 
                        except Exception:
                            pass

                    elif option == 2: ### eliminar eventos
                        print('Veamos cuales tienes y puedes eliminar.')
                        try:    
                            Usuario= funtion.eliminar_eventos(Usuario) ### se encarga de eliminar eventos.
                        except Exception:
                            pass

                    elif option == 3: ### mostrar los eventos
                        print('Los Eventos agendados hasta el momento son:')
                        funtion.mostras_eventos(Usuario) ### indexa en los eventos con un for y los printea
                    
                    elif option == 4: ### mostrar los recursos disponibles
                        print('Los recursos disponibles en este momento son:')
                        funtion.mostrar_recursos(Recursos_disponibles, Usuario)
                    
                    elif option == 5: ###actualizar los eventos
                        print('Veamos si no hay ningun Evento que ya haya expirado.')
                        try:
                            Usuario = funtion.verificador_estado_eventos(Usuario)
                        except Exception:
                            pass

                    elif option == 6: ### salir al menu principal
                        print('Primero, guardemos el perfil, para asegurarnos de que no se pierda la info.')
                        funtion.guardar_json(Usuario)
                        funtion.barra_de_progreso()
                        print('Hecho.')
                        time.sleep(1.5) ### detiene el programa por 1.5 segundos
                        break
            
            elif option == 2: ### Va a la sgt iteracion del bucle.
                continue
            elif option == 3: ### Rompe el bucle y vuelve al menu inicial.
                break
            
            if option == 6: ###Esta opcion solo entrara en ella cuando haya estado ya en la cuenta
                break       ### y haya posterior a eso salido.


    elif option == 2:
        while True:
            print('1. Digame su nombre de usuario.')
            print('2. Salir al menu principal.')
        ###########################################funcion que cargue las posibles opciones de cuenta(archivos .json en la carpeta.)
            option = funtion.try_option(2)
            if option == 1:
                path = input('Usuario: ') ### el usuario introduce el nombre de usuario (y el path de esa cuenta es 'nombre'.json )
                Usuario = funtion.cargar_json(path)
                if not Usuario: ### devuelve False si no logra cargar el usuario.
                    print('Puede volverlo a intentar.')
                else:
                    print('El Perfil ha sido encontrado, ahora necesitamos su contrasenna para verificar.')
                    while True:
                        passw = input('Contrasenna: ')
                        if funtion.verificador_passw(passw, Usuario):  ### la contrasenna es la correcta y puede ejecutarse el programa.
                            funtion.clear()
                            print(f'Bienvenido {Usuario.name}')
                            while True:
                                print('Que deseas?')
                                print('1. Agregar Eventos a tu agenda.') 
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
                                    try:    ###hace todo el proceso de agrego
                                        Usuario = funtion.agrego_eventos(option, Recursos_disponibles, Usuario) 
                                    except Exception:
                                        pass

                                elif option == 2: ### eliminar eventos
                                    print('Veamos cuales tienes y puedes eliminar.')
                                    try:    
                                        Usuario = funtion.eliminar_eventos(Usuario) ### se encarga de eliminar eventos.
                                    except Exception:
                                        pass

                                elif option == 3: ### mostrar los eventos
                                    funtion.clear()
                                    print('Los Eventos agendados hasta el momento son:')
                                    funtion.mostras_eventos(Usuario) ### indexa en los eventos con un for y los printea
                                
                                elif option == 4: ### mostrar los recursos disponibles
                                    funtion.clear()
                                    print('Los recursos disponibles en este momento son:')
                                    funtion.mostrar_recursos(Recursos_disponibles, Usuario)
                                
                                elif option == 5: ###actualizar los eventos
                                    print('Veamos si no hay ningun Evento que ya haya expirado.')
                                    try:
                                        Usuario= funtion.verificador_estado_eventos(Usuario)
                                    except Exception:
                                        pass

                                elif option == 6: ### salir al menu principal
                                    print('Primero, guardemos el perfil, para asegurarnos de que no se pierda la info.')
                                    funtion.guardar_json(Usuario)
                                    funtion.barra_de_progreso()
                                    print('Hecho.')
                                    time.sleep(1.5) ### detiene el programa por 1.5 segundos
                                    passw = 'salir' ### para que se ejecute el sgt if y salga al bucle principal
                                    break
                        if passw == 'salir':
                            break  ### sale al menu de cargar nuevamente el usuario 
                        else:
                            print('No es la contrasenna. Vuelva a intentarlo o introduzca salir'
                                  ' para volver al menu principal.')
                    if passw == 'salir':
                        break ### para salir al menu principal, solo se activa una vez estuviste dentro
                              ### de la cuenta
            elif option == 2:
                break ### Vuelve al bucle principal.
        
         
    elif option == 3:
        print(f'Hasta luego {name_user}.')
        exit()