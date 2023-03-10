from mesa import Agent
import numpy as np

class Car(Agent):
    DIRECTIONS = ['right', 'down','left','up']
    COLOURS = ('orange','blue','black','purple')

    def __init__(self, unique_id, model, colour = None, direction = None, turning_rate = 0.2):
        super().__init__(unique_id, model)
        self.colour = self.random.choice(self.COLOURS) if not colour else colour
        self.direction = None
        self.next_pos = None
        self.turning_rate = turning_rate
        self.waiting = 0

        self.direction = self.random.choice(self.DIRECTIONS) if not direction else direction
        
    def step(self):
        if self.pos in self.model.centre and np.random.rand() < self.turning_rate:
            self.direction = self.model.possible_turns[self.direction][self.pos]

        next_pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

        if self.model.grid.out_of_bounds(next_pos):
            self.next_pos = self.model.grid.torus_adj(next_pos)
        else:
            self.next_pos = next_pos

@property
def direction(self):
    return self._direction

@direction.setter
def direction(self, direction):
    self.direction = direction
    if self._direction == 'up':
        self.dx, self.dy = -1, 0
    elif self._direction == 'down':
        self.dx, self.dy = 1, 0
    if self._direction == 'right':
        self.dx, self.dy = 0, 1
    elif self._direction == 'left':
        self.dx, self.dy = 0, -1

#def near_traffic_light(self):
    

#def step(self):

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