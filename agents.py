from mesa import Agent
import numpy as np

class Car(Agent):
    DIRECTIONS = ['right', 'down', 'left', 'up']
    COLOURS = ('orange', 'blue', 'black', 'purple')
    DIRECTIONS_SET1 = ['down', 'right']


    #Every car agent is initialiized with a waiting time of cero, direcition and a color
    def __init__(self, unique_id, model, colour=None, direction=None, turning_rate=0.2):
        super().__init__(unique_id, model)
        self.colour = self.random.choice(self.COLOURS) if not colour else colour
        self._direction = None
        self.next_pos = None
        self.turning_rate = turning_rate
        self.waiting = 0

        self.direction = self.random.choice(self.DIRECTIONS) if not direction else direction

    #@property decorator in python is for ussing getter and setters
    @property
    def direction(self):
        return self._direction

    #setter de direction
    @direction.setter
    def direction(self, direction):
        self._direction = direction
        if self._direction == 'up':
            self.dx, self.dy = -1, 0
        elif self._direction == 'down':
            self.dx, self.dy = 1, 0
        if self._direction == 'right':
            self.dx, self.dy = 0, 1
        elif self._direction == 'left':
            self.dx, self.dy = 0, -1


    def step(self):

        #if the car agent is in the center of the grid, there will be a possibility of turning
        #the posibble turn are available in the dictionary possible_turns in the model
        
        
        if self.pos in self.model.centre and np.random.rand() < self.turning_rate:
            if self.pos != (21,21) and self.direction != 'right':
                self.direction = self.model.possible_turns[self.direction][self.pos]
            
        #this line makes no going to the right down parrt of the cross
        if self.pos==(21,19) and self.direction == 'down':
           self.direction='right'
        
        #for the ones como from the right going down
        if self.pos == (19,19):
            self.direction='left'
        
        if self.pos==(19,21) and self.direction=='up':
            self.direction='left'
        
        if self.pos == (21,21) and np.random.rand() < self.turning_rate:
            self.direction='right'
        
        if self.pos == (10,19):
            self.direction='down'

        if self.pos == (15, 21):
            self.direction=('right')
        
        if self.pos == (15, 29):
            self.direction=('up')
        
        if self.pos in [(19,31), (19,30)] and np.random.rand() < self.turning_rate:
            self.direction = ('up')
        
        if(self.pos == (21,30) and np.random.rand() < self.turning_rate):
            self.direction = ('up')
        
        #for crazy drivers
        if(self.pos in [(22,21),(23,21)]):
            self.direction=('up')

        if(self.pos == (21,20)):
            self.direction=('right')
        
        if self.pos == (9,19) and np.random.rand() < self.turning_rate:
            self.direction=('left')

        next_pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

        #if the next pos is out of grid bound the position will be adjusted
        if self.model.grid.out_of_bounds(next_pos):
            if next_pos==(-1,31) and self.model.grid.is_cell_empty(self.model.grid.torus_adj((40,21))):
                self.next_pos = self.model.grid.torus_adj((40,21))
                self.direction ='down'
            elif next_pos==(-1,30) and self.model.grid.is_cell_empty(self.model.grid.torus_adj((40,20))):
                self.next_pos = self.model.grid.torus_adj((40,20))
                self.direction ='down'
            elif next_pos==(-1,29) and self.model.grid.is_cell_empty(self.model.grid.torus_adj((40,19))):
                self.next_pos = self.model.grid.torus_adj((40,19))
                self.direction ='down'
            elif next_pos==(9,-1) and self.model.grid.is_cell_empty(self.model.grid.torus_adj((-1,21))):
                if self.model.pass_:
                    self.next_pos = self.model.grid.torus_adj((-1,21))
                    self.direction ='up'
                    self.model.pass_ -= 1
                else:
                    self.next_pos = self.model.grid.torus_adj((10,40))
                    self.direction ='right'
                    self.model.pass_ += 1
                
            else:
                self.next_pos = self.model.grid.torus_adj(next_pos)
                
        else:
            self.next_pos = next_pos

        # print(self.pos, next_pos, self.direction, self.next_pos)


    #regresa true si hay al menos un semaforo como vecino del vehiculo
    def near_traffic_light(self):
        return any([isinstance(obj, TrafficLight) for obj in self.model.grid.get_neighbors(
            self.pos, moore=False, include_center=False)])

    #de acuerdo a su direccion sabemos si se encuentra antes del centro del grid
    def is_before_crossroad(self):
        if self.direction == 'right':
            return self.pos[1] < self.model.centre_bounds[0]
        elif self.direction == 'left':
            return self.pos[1] > self.model.centre_bounds[1]
        elif self.direction == 'down':
            return self.pos[0] < self.model.centre_bounds[0]
        elif self.direction == 'up':
            return self.pos[0] > self.model.centre_bounds[1]

    #no debera avanzar en el caso que este detras del cruce, tenga semaforo adelante y este sea rojo
    def advance(self):
        #verificamos en que parte del grid se encuentra el carro para saber a que semaforo hacer caso
        if self.pos==(11,19):
            should_advance = True
        elif self.pos in self.model.newStreets:
            should_advance = not (self.pos in [(8,19), (8,20), (8,21)] and
                              self.model.traffic_lights_set1[self.direction].colour == 'red')
        elif self.pos==(10,18):
            should_advance = not (self.model.traffic_lights_set1[self.direction].colour == 'red')
        elif self.pos==(21,28):
            should_advance = self.model.traffiic_light7.colour == 'green'
        elif self.pos==(18,20):
            should_advance = self.model.traffic_lights['down'].colour == 'green'
        else:
            should_advance = not (self.is_before_crossroad() and self.near_traffic_light() and
                              self.model.traffic_lights[self.direction].colour == 'red')
        
        
        if self.model.grid.is_cell_empty(self.next_pos) and should_advance:
            self.model.grid.move_agent(self, self.next_pos)
            self.waiting = 0
            
        else:
            self.waiting = 1
            # self.pos = self.next_pos


class TrafficLight(Agent):
    TRAFFIC_LIGHT_COLOURS = ('red', 'green')

    def __init__(self, unique_id, colour, model):
        super().__init__(unique_id, model)
        self.colour = colour

class Field(Agent):
    FIELD_COLOURS = ('olive', 'dark_green', 'brown')

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.colour = self.random.choice(self.FIELD_COLOURS)

    def step(self):
        if np.random.rand() < 0.1:
            self.colour = self.random.choice(self.FIELD_COLOURS)