from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from agents import Car, TrafficLight, Field

import numpy as np
import random


def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))

    # Por todas las celdas del grid
    for cell in model.grid.coord_iter():
        agent, x, y = cell

        if isinstance(agent, Car):
            if agent.colour == 'orange':
                grid[x][y] = 6
            elif agent.colour == 'blue':
                grid[x][y] = 7
            elif agent.colour == 'purple':
                grid[x][y] = 8
            else:  # black
                grid[x][y] = 9

        elif isinstance(agent, Field):
            if agent.colour == 'brown':
                grid[x][y] = 3
            elif agent.colour == 'olive':
                grid[x][y] = 4
            else:  # dark green
                grid[x][y] = 5

        elif isinstance(agent, TrafficLight):
            if agent.colour == 'green':
                grid[x][y] = 2
            else:  # red
                grid[x][y] = 1

        else:  # Street
            grid[x][y] = 0

    return grid


#sum all the waiting attributes of car agents that are in the grid and return the sum
def get_waiting(model):
    total_waiting_time = 0

    # Por todas las celdas del grid
    for cell in model.grid.coord_iter():
        agent, x, y = cell
        if isinstance(agent, Car):
            total_waiting_time += agent.waiting

    return total_waiting_time


#returns the number of agents minus the cars that have a waiting attribute
def get_running(model):
    return model.num_agents - get_waiting(model)


class CrossRoad(Model):
    """A model with some number of agents."""

    def __init__(self, num_agents=10, half_length=20, traffic_time=10, car_turning_rate=0.1):
        self.num_agents = num_agents
        self.running = True

        # Dimensions are double of given values
        self.centre_bounds = (half_length - 1, half_length + 1)
        self.width = half_length * 2
        self.height = half_length * 2

        self.grid = SingleGrid(self.width, self.height, True)
        self.schedule = SimultaneousActivation(self)
        self.traffic_counter = 0
        self.traffic_time = traffic_time

        # Define cross road centre
        no_car_zone = half_length + np.arange(-2, 2)

        # Define traffic light positions according to street direction
        traffic_light_positions = {
            'right': (half_length + 2, half_length + 2),
            'left': (half_length - 2, half_length - 2),
            'up': (half_length - 2, half_length + 2),
            'down': (half_length + 2, half_length - 2),
        }
        #traffic_light_positions: {'right': (22, 22), 'left': (18, 18), 'up': (18, 22), 'down': (22, 18)}

        # Possible turns and centre for crossroad
        self.centre = [(half_length + x, half_length + y) for x in [-1, 1] for y in [-1, 1]]
        # centre is an array of tupples: [(19, 19), (19, 21), (21, 19), (21, 21)]

        self.possible_turns = {
            'right': {self.centre[2]: 'down', self.centre[3]: 'up'},
            'left': {self.centre[1]: 'up', self.centre[0]: 'down'},
            'up': {self.centre[3]: 'up', self.centre[1]: 'left'},
            'down': {self.centre[0]: 'left', self.centre[2]: 'right'}
        }
        
        # possibble turns is: {'right': {(21, 19): 'down', (21, 21): 'up'}, 'left': {(19, 21): 'up', (19, 19): 'down'}, 'up': {(21, 21): 'right', (19, 21): 'left'}, 'down': {(19, 19): 'left', (21, 19): 'right'}}

       

        # Define streets
        streets = {
            'left': [(half_length - 1, y) for y in range(self.height)
                     if y not in no_car_zone],
            'right': [(half_length + 1, y) for y in range(self.height-17)
                      if y not in no_car_zone],
            'up': [(x, half_length + 1) for x in range(self.width)
                   if x not in no_car_zone],
            'down': [(x, half_length - 1) for x in range(self.width)
                     if x not in no_car_zone]
        }
       #streets:
        """
        {'left': [(19, 0), (19, 1), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (19, 10), (19, 11), (19, 12), (19, 13), (19, 14), (19, 15), (19, 16), (19, 17), (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), (19, 27), (19, 28), (19, 29), (19, 30), (19, 31), (19, 32), (19, 33), (19, 34), (19, 35), (19, 36), (19, 37), (19, 38), (19, 39)], 
        'right': [(21, 0), (21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7), (21, 8), (21, 9), (21, 10), (21, 11), (21, 12), (21, 13), (21, 14), (21, 15), (21, 16), (21, 17), (21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27), (21, 28), (21, 29), (21, 30), (21, 31), (21, 32), (21, 33), (21, 34), (21, 35), (21, 36), (21, 37), (21, 38), (21, 39)], 
        'up': [(0, 21), (1, 21), (2, 21), (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21), (10, 21), (11, 21), (12, 21), (13, 21), (14, 21), (15, 21), (16, 21), (17, 21), (22, 21), (23, 21), (24, 21), (25, 21), (26, 21), (27, 21), (28, 21), (29, 21), (30, 21), (31, 21), (32, 21), (33, 21), (34, 21), (35, 21), (36, 21), (37, 21), (38, 21), (39, 21)], 
        'down': [(0, 19), (1, 19), (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19), (11, 19), (12, 19), (13, 19), (14, 19), (15, 19), (16, 19), (17, 19), (22, 19), (23, 19), (24, 19), (25, 19), (26, 19), (27, 19), (28, 19), (29, 19), (30, 19), (31, 19), (32, 19), (33, 19), (34, 19), (35, 19), (36, 19), (37, 19), (38, 19), (39, 19)]}
        """

        print(streets['right'])
        

        traffic_light_count = 100
        self.traffic_lights = {}
        # Create traffic light agents 
        #position the traffic light agents
        #assigns the col green to the first traffic light to initialize it
        for direction, pos in traffic_light_positions.items():
            col = 'green' if traffic_light_count == 100 else 'red'
            a = TrafficLight(traffic_light_count, col, self)

            self.traffic_lights[direction] = a
            traffic_light_count += 1
            self.grid.place_agent(a, pos)

        #self.trafficlights = {'right': <agents.TrafficLight object at 0x1119dfa90>, 'left': <agents.TrafficLight object at 0x1119dfb10>, 'up': <agents.TrafficLight object at 0x1119dced0>, 'down': <agents.TrafficLight object at 0x1119dfad0>}
        #create a traffic light and assign it to one direction (right, up etc..) and the placed it into the grid
        

        field_count = 1000
        for cell in self.grid.coord_iter():
            _, x, y = cell
            # Create field agents
            if np.abs(x - half_length) > 1 and np.abs(y - half_length) > 1 and self.grid.is_cell_empty((x, y)):
                a = Field(field_count, self)
                self.schedule.add(a)
                field_count += 1
                self.grid.place_agent(a, (x, y))
        
        #create field for right down line
        for i in range (24-39):
            a = Field(field_count, self)
            self.schedule.add(a)
            field_count += 1
            self.grid.place_agent(a, (21, i))


        # Create Car agents
        #just creates an array of random choices of the colours and directions for car agents
        car_colours = random.choices(Car.COLOURS, k=self.num_agents)
        car_directions = random.choices(Car.DIRECTIONS, k=self.num_agents)


        #this function is to randomly allocate the car agents in the grid, assignim the random colours and diirections 
        for i, (col, direction) in enumerate(zip(car_colours, car_directions)):
            a = Car(i, self, col, direction, car_turning_rate)
            self.schedule.add(a)

            # Picks a position and remove it from the availables
            #picks a position from the streets that are made
            position = random.choices(streets[direction], k=1)[0]
            streets[direction].remove(position)

            self.grid.place_agent(a, position)

        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid, "Waiting": get_waiting, "Running": get_running}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        #self.traffic_time is set to 10, the number of steps one traffic light lasts
        #until reset the variable 

        if self.traffic_counter < self.traffic_time:
            self.traffic_counter += 1
        else:
            for i, direction in enumerate(Car.DIRECTIONS):
                # print(self.traffic_lights)
                if self.traffic_lights[direction].colour == 'green':
                    self.traffic_counter = 0
                    self.traffic_lights[direction].colour = 'red'

                    next_i = i + 1 if i < len(Car.DIRECTIONS) - 1 else 0
                    self.traffic_lights[Car.DIRECTIONS[next_i]].colour = 'green'
                    break