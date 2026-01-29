import json
from pathlib import Path
from datetime import datetime, date, timedelta
import Recursos
import Events
import Agregar
import Jsons
import user
from sys import exit
import time
import Eliminar
import miscelaneo
from recursos_dannados import recursos_agotados

name_user = ''
Recursos_disponibles = Recursos.Inicializador_Recursos() #carga recursos por defecto

def main(Recursos_disponibles, Usuario): ### una vez cargada las cuentas, el usuario solo interacciona aqui
    while True:
        print('Que deseas?')
        print('1. Agregar Eventos a tu agenda.')
        print('2. Eliminar Eventos de tu agenda.') 
        print('3. Ver los Eventos agendados.')
        print('4. Ver los Recursos y su disponibilidad.')
        print('5. Actualizar Agenda.')
        print('6. Ver los Recursos rotos o agotados.')
        print('7. Salir al menu principal.')

        option = miscelaneo.try_option(7)
        if option == 1: ### Agrega eventos como al usuario le plazca
            print('Tienes para agregar:')
            Agregar.printeo_opciones_eventos() ### printea las opciones
            option = miscelaneo.try_option(12)
            try:    ###hace todo el proceso de agrego
                Usuario = Agregar.agrego_eventos(option, Recursos_disponibles, Usuario) 
            except Exception:
                pass

        elif option == 2: ### eliminar eventos
            print('Veamos cuales tienes y puedes eliminar.')
            try:    
                Usuario= Eliminar.eliminar_eventos(Usuario) ### se encarga de eliminar eventos.
            except Exception:
                pass

        elif option == 3: ### mostrar los eventos
            print('Los Eventos agendados hasta el momento son:')
            Eliminar.mostras_eventos(Usuario) ### indexa en los eventos con un for y los printea
                        
        elif option == 4: ### mostrar los recursos disponibles
            miscelaneo.clean
            print('Los recursos disponibles en este momento son:')
            miscelaneo.mostrar_recursos(Recursos_disponibles, Usuario)
                        
        elif option == 5: ###actualizar los eventos
            print('Veamos si no hay ningun Evento que ya haya expirado.')
            try:
                Usuario, recursos_usados, recursos_renovados = miscelaneo.verificador_estado_eventos(Usuario)
                Recursos_disponibles = miscelaneo.actualizar_estado_recursos(Recursos_disponibles, recursos_usados, recursos_renovados)
            except Exception:
                pass
        
        elif option == 6:### Observar los recursos dannados y da la posibilidad de repararlos
            miscelaneo.clean()
            Usuario = recursos_agotados(Recursos_disponibles, Usuario)

        elif option == 7: ### salir al menu principal
            print('Primero, guardemos el perfil, para asegurarnos de que no se pierda la info.')
            Jsons.guardar_json(Usuario, Recursos_disponibles)
            #miscelaneo.barra_de_progreso()
            print('Hecho.')
            time.sleep(0.5) ### detiene el programa por 0.5 segundos
            break

###inicio del programa
while True:
    miscelaneo.clean()
    print('Hola, Bienvenido al Gestor de tareas para tu empresa de vehiculos.')
    print('1. Crearse una cuenta.')
    print('2. Cargar una cuenta.')
    print('3. Salir del Programa.')

    option = miscelaneo.try_option(3)
    if option == 1:  ### Creacion de nueva cuenta
        while True:
            miscelaneo.clean() ###limpia la pantalla   
            print('Perfecto, entonces, cual sera tu nombre?')
            name_user = input()
            print('Y ahora establezcamos una contraseña para asegurarnos de que nadie acceda a tu perfil.')
            passw = input()
            print(f'Tu perfil sera {name_user} con contraseña {passw}, estas de acuerdo?')
            print('1. Si \n2. No \n3. Ir al menu principal.')
            option = miscelaneo.try_option(3)
            if option == 1:
                miscelaneo.clean()
                Usuario = user.User(name_user, passw, name_user, []) ### se crea una instancia usuario
                print(f'Bienvenido {name_user}')
                main(Recursos_disponibles, Usuario)  ### el usuario interactua solo aqui
                break  ### para que salga al menu principal una vez cierre 'sesion'
            
            elif option == 2: ### Va a la sgt iteracion del bucle.
                continue
            elif option == 3: ### Rompe el bucle y vuelve al menu inicial.
                break

    elif option == 2: ### carga una 'cuenta' (un archivo .json)
        while True:
            miscelaneo.clean()
            print('1. Introducir el nombre de usuario.')
            print('2. Salir al menu principal.')
            option = miscelaneo.try_option(2)
            if option == 1:
                miscelaneo.recomendador_cuentas()
                path = input('Usuario: ') ### el usuario introduce el nombre de usuario (y el path de esa cuenta es 'nombre'.json )
                Usuario, Recursos_disponibles = Jsons.cargar_json(path, Recursos_disponibles)
                if not Usuario: ### devuelve False si no logra cargar el usuario.
                    print('Puede volverlo a intentar.')
                    time.sleep(0.5)
                else:
                    print('El Perfil ha sido encontrado, ahora necesitamos su contraseña para verificar.')
                    while True:
                        passw = input('Contraseña: ')
                        if miscelaneo.verificador_passw(passw, Usuario):  ### la contrasenna es la correcta y puede ejecutarse el programa.
                            miscelaneo.clean()
                            print(f'Bienvenido {Usuario.name}')
                            main(Recursos_disponibles, Usuario)  ### el usuario interactua solo aqui
                            passw = 'salir' ### para que cuando salga, vaya directo al menu principal

                        if passw == 'salir':
                            break  ### sale al menu de cargar nuevamente el usuario 
                        else:
                            print('No es la contraseña. Vuelva a intentarlo o introduzca "salir"'
                                  ' para volver al menu principal.')
                    
                    if passw == 'salir':
                        break ### para salir al menu principal, solo se activa una vez estuviste dentro
                              ### de la cuenta
            elif option == 2:
                break ### Vuelve al bucle principal.
                 
    elif option == 3:
        if name_user == '':
            print('Hasta luego.')
            exit()
        else:
            print(f'Hasta luego {name_user}.')
            exit()