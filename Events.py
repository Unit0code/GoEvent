import json
from pathlib import Path
from datetime import datetime, date, time, timedelta

### este archivo solo posee los tipos eventos, todos con mismas propiedades, diferente nombre 
### y valores diferentes asignados a cada propiedad.

class Events: ### Los eventos seran un tipo, con ciertos atributos y  ciertas restricciones.
    def __init__(self, fecha : str):
        self.fecha = datetime.strptime(fecha, '%d/%m/%Y --- %H:%M')
    
    def __dict__ (self):
        Data = {'Nombre': self.name,
            'Fecha inicio': datetime.strftime(self.fecha, '%d/%m/%Y --- %H:%M'),
            'Fecha fin': datetime.strftime(self.Finish_date, '%d/%m/%Y --- %H:%M'),
            'Recursos': self.Recursos
            }
        return Data


class travel_Habana(Events): ### tipo evento de viajes a la habana.
    def __init__ (self, fecha : str, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a la Habana'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours= 2)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Suarez', 'Menedez'), ('Jose', 'Marlon')]  ###No pueden estar en el mismo Evento
        self.message = ['Cuando ambos se juntan, hacen destrozos por la Habana.',
                        'Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = [ 'Conductor','Vehiculo', 'Guia']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class travel_Gto(Events): ### tipo evento de viajes a la Gto.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Guantanamo'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours= 18)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'Juan' : 'No se le dan los viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Pedro', 'Rigoberto'), ('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['La ultima vez que estuvieron esos locos juntos, chocaron.',
                        'Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = [ 'Conductor','Vehiculo']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class travel_Stgo(Events): ### tipo evento de viajes a la Stgo de Cuba.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Santiago de Cuba'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 15)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'Juan' : 'No se le dan los viajes largos.', ### No pueden usarse para este evento.
                                    'camion1': 'Las rutas se encuentran en muy mal estado, y este camion ya esta un poco antiguo'} 
        self.Restriction_recursos_pares = [('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo', 'Guia']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class travel_Camaguey(Events): ### tipo evento de viajes a Camaguey.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Camaguey'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 12)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'Juan' : 'No se le dan los viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Rigoberto', 'Transtur1'), ('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Ese maneja como quiera y la Transtur es muy preciada como para dejarsela en ese viaje.',
                        'Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)
    

class travel_Las_Tunas(Events): ### tipo evento de viajes a Las Tunas.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Las Tunas'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 13)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'Juan' : 'No se le dan los viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Rigoberto', 'Transtur1'), ('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Ese maneja como quiera y la Transtur es muy preciada como para dejarsela en ese viaje.',
                        'Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.' ] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)    
    

class travel_Las_Villas(Events): ### tipo evento de viajes a Las Villas.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Las Villas'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 7)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'camion2' : 'Ese es el bueno, deberiamos reservarlo para viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class travel_Pinar_Rio(Events): ### tipo evento de viajes a Pinar del Rio.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Pinar del Rio'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 5)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'camion2' : 'Ese es el bueno, deberiamos reservarlo para viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class travel_Mtz(Events): ### tipo evento de viajes a Matanzas.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Matanzas'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 2)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'camion2' : 'Ese es el bueno, deberiamos reservarlo para viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class travel_Cienfuegos(Events): ### tipo evento de viajes a Cienfuegos.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Viaje a Cienfuegos'
        self.Restriction_hour = [ time(8), time(21) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 5)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'camion2' : 'Ese es el bueno, deberiamos reservarlo para viajes largos.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Jose', 'Marlon')] ###No pueden estar en el mismo Evento
        self.message = ['Sospecho que entre ellos dos traman algo, no podemos dejarlos a solas.'] ### Mensaje de las restricciones
        self.Needs = ['Conductor' , 'Vehiculo', 'Guia']  ###lo necesario en las catg de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class Botear_Habana(Events): ### tipo evento de Botear en la Habana.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Boteo en la Habana'
        self.Restriction_hour = [ time(6), time(23) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours = 2)  ### duracion del viaje
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'Federico':'No hara falta, son habaneros, buscan moverse, no un tour.',
                                     'Phineas':'No hara falta, son habaneros, buscan moverse, no un tour.'} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [] ###No pueden estar en el mismo Evento
        self.message = [] ### Mensaje de las restricciones
        self.Needs = ['Vehiculo', 'Conductor']  ###lo necesario de los nombres de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)


class Mantenimiento_Vehiculos(Events): ### tipo evento de Mantenimiento de vehiculos.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Mantenimiento de Vehiculos'
        self.Restriction_hour = [ time(8), time(23) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours= 5)  ### duracion del viaje############################################################
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {} ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [('Marlon', 'Diego')] ###No pueden estar en el mismo Evento
        self.message = ['No hacen falta tantos admins pendientes, seria perdida de tiempo.'] ### Mensaje de las restricciones
        self.Needs = ['Vehiculo', 'Mecanico']  ###lo necesario de los nombres de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)
    

class Vacaciones_trabajadores(Events): ### tipo evento de Mantenimiento de vehiculos.
    def __init__ (self, fecha, *Recursos):
        super().__init__( fecha)
        self.name = 'Descanso pagado a los trabajadores'
        self.Restriction_hour = [ time(5), time(23) ] ###Restricciones de horario para iniciar el viaje.
        self.Duration = timedelta(hours= 5)  ### duracion del viaje ##############################
        self.Finish_date = self.Duration + self.fecha ###fecha de finalizacion
        self.Restriction_recursos = {'Transtur1': 'No se necesitan vehiculos para esta actividad',
                                     'Transtur2': 'No se necesitan vehiculos para esta actividad',
                                     'Camion1': 'No se necesitan vehiculos para esta actividad',
                                     'Camion2': 'No se necesitan vehiculos para esta actividad' } ### No pueden usarse para este evento.
        self.Restriction_recursos_pares = [] ###No pueden estar en el mismo Evento
        self.message = [] ### Mensaje de las restricciones
        self.Needs = []  ###lo necesario de los nombres de los recursos para iniciar el viaje.
        self.Recursos = list(Recursos)