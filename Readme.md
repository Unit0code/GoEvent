# 👨‍🔧 Bienvenidos a GoEvent 🚌
## Descripción 📃:
*  **Un programa capacitado para gestionar eventos con temática dirigida a eventos desarrollados en una base de transporte, donde usted como usuario podrá agendar eventos a conveniencia y el programa verificara y validara el dicho según horarios, colisiones con otros eventos y restricciones que cada uno de estos eventos posea en particular.**

## Características ⚙:
- 🕐Detección de posibles colisiones con otros eventos en el horario escogido e inhabilita los recursos que en el mismo ya están siendo implementados en algún otro evento. 

- Tus vehículos (🚌) y personas (👨‍🔧) según los usas necesitan mantenimiento y descanso respectivamente, cuida de tus recursos. Cada uno constara de un indicador de (energía/usos)⚡ que te diria el estado de este.

- ⭕No se permitirá usar recursos de exclusión mutua o recursos que en el evento no estén permitidos, según el evento estas restricciones varian. 

- ⭕No se podrá realizar eventos en horarios inoportunos, por lo tanto cada evento tendrá un horario de funcionamiento para poder comenzarse.

## Funcionalidades👓:
-	Crear nuevo Usuario/cargar Usuario 👨‍💻:
    *	Cada usuario podrá crearse una cuenta dedicada exclusivamente a si, en dependencia de si ya haya usado el programa con anterioridad o no, tomará la decisión a conveniencia (cada cuenta es asegurada con una contraseña 🔒)

-	Agregar eventos ✅: 
    *	Aquí se seleccionará una fecha, el programa verificará recursos disponibles en dicho horario y te dará la posibilidad de escoger entre ellos.

-	Eliminar eventos ❌:
    *	Descarta eventos agendados y pone a disposición nuevamente los recursos que se empleaban.

-	Recursos y disponibilidad 👀:
    *	Mostrará los recursos, los horarios en los que están ocupados y la (energía/usos) que le quedan. ⚡

-	Actualizar eventos 🔄:
    *	En caso de haber finalizado un evento, esta opción hará que se marque este evento como finalizado y los resultados que generó serán visibles.

-	Recursos rotos o agotados ❗❗:
    *	Visualiza los recursos que necesitan urgente mantenimiento o descanso. 😴

## Eventos 🎫:
### Cada evento posee estas características:
-	Horarios para poder comenzar. Ej.: (8am – 7pm) 🕙

-	Restricciones particulares. Ej.: (no poder utilizarse a Juan el conductor.) ❌👨

-	Restricciones de Exclusión mutua. Ej.: ( no pueden estar juntos Pedro y la transtur1.) 🚌 <=>❌👨

-	Restricción de requisitos mínimos necesarios. Ej.: ( un viaje no podrá comenzar si no tiene un recurso categoría ‘vehículo’ y uno ‘conductor’.) ✅ <=> 👨,🚌

### Los eventos en particular de:
-	Mantenimiento de Vehículos 🔧:
    *	Este evento es considerado como ‘curativo’, los recursos de la categoría ‘vehículo’ que sean agendados a esta actividad una vez finalizada estarán como nuevos. 💚

-	Vacaciones Pagadas 💲🌅:
    *	Este evento es considerado como ‘curativo’, los recursos de categoría diferentes de ‘vehículo’ que sean agendados a esta actividad una vez finalizada estarán como nuevos. 💚

## Tecnologias 💻:
-	Python version 3.17
-	JSON

## Instalacion 🛠:
1.	Clonar el repositorio:
    `git clone https://github.com/Unit0Code/GoEvent.git`

2.	Ejecutar el archivo main.py .

## Informacion de contacto:
* #### Email: `macronymous@gmail.com`

* #### Telegram: `@Cradles0`

-------

