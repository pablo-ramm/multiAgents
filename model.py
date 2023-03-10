from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from agents import Car, TrafficLight, Field

import numpy as np
import random

#define a class to store information about a given traffic light
# class TrafficLightInfo:
#     def __init__(self, id, position, spaces):
#         self.id = id
#         self.position = position
#         self.spaces = spaces

# traffic_lights.append(TrafficLightInfo(2,(17,18),[(17,19)]))
# traffic_lights.append(TrafficLightInfo(3,(21,13),[(21,11),(21,12)]))
# traffic_lights.append(TrafficLightInfo(4,(21,18),[(19,18),(20,18)]))
# traffic_lights.append(TrafficLightInfo(5,(21,21),[(21,20)]))
# traffic_lights.append(TrafficLightInfo(6,(18,21),[(19,21)]))
# traffic_lights.append(TrafficLightInfo(7,(16,21),[(16,20)]))
# traffic_lights.append(TrafficLightInfo(8,(21,9),[(20,9),(19,9),(18,9)]))
# traffic_lights.append(TrafficLightInfo(9,(10,18),[(10,19)]))

#define all trafic light locations and spaces
#traffic_lights_pos = ((17,18),(21,13)(21,18),(21,21),(18,21),(16,21),(21,9),(10,18))

pos_always_turn = {
    (15,20): lambda x: print("Always Turn Left - 9"),
    (12,11): lambda x: print("Always Turn Right - 11"),
    (15,11): lambda x: print("Always Turn Up - 12"),
    (20,10): lambda x: print("Always Turn Up - 16"),
    (19,9): lambda x: print("Always Turn Down - 20")
}

pos_turn = {
    (19,18): lambda x: print("Has a {} chance to turn Left - 4".format(np.random.rand())),
    (19,19): lambda x: print("Has a {} chance to turn Left - 6".format(np.random.rand())),
    (20,19): lambda x: print("Has a {} chance to turn Left - 7".format(np.random.rand())),
    (12,10): lambda x: print("Has a {} chance to turn Right - 14".format(np.random.rand())),
    (19,10): lambda x: print("Has a {} chance to turn Down - 15".format(np.random.rand())),
    (11,9): lambda x: print("Has a {} chance to turn Down - 18".format(np.random.rand())),
    (12,9): lambda x: print("Has a {} chance to turn Right - 19".format(np.random.rand()))
}

# Largo
# Ancho
# Largo[n - 1] = ultimo renglon derecha
# Largo[0] = primer renglon 

traffic_light_positions = {
    (18,12): 1,
    (13,8): 2,
    (18,8): 3,
    (21,8): 4,
    (21,11): 5,
    (21,13): 6,
    (9,8): 7,
    (18,19): 8
}
spawn_positions=[(0,9),(0,10),(0,11),(19,29),(0,20),(29,10),(12,0)]
despawn_postions=[(20,29),(0,18),(0,19),(0,20),(11,0),(19,0)]

def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))

    # Por todas las celdas del grid
    for cell in model.grid.coord_iter():
        agent, x, y = cell

        # if isinstance(agent, Car):
        #     if agent.colour == 'orange':
        #         grid[x][y] = 6
        #     elif agent.colour == 'blue':
        #         grid[x][y] = 7
        #     elif agent.colour == 'purple':
        #         grid[x][y] = 8
        #     else:  # black
        #         grid[x][y] = 9

        if isinstance(agent, Field):
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

class CrossRoad(Model):
    def __init__(self, num_agents=10, car_turning_rate=0.1):
        self.num_agents = num_agents
        self.running = True

        self.width = 30
        self.height = 30

        self.grid = SingleGrid(self.width, self.height, True)
        self.schedule = SimultaneousActivation(self)

        col = 'red'

        #place field agents
        for (cell, x, y) in self.grid.coord_iter():
            #place traffic light
            #  if (x,y) in traffic_light_positions:
            #      a = TrafficLight(traffic_light_positions[(x,y)], col, self)
            #      self.grid.place_agent(a, (x,y))

            #place field agent

            if not((x >= 0 and x <= 18) and (y <= 18 and y >= 16) or (x >= 0 and x <= 18) and (y <= 11 and y >= 9) or (x == 11) and (y <= 8 and y >= 0) or (x == 12) and (y <= 8 and y >= 0) or (x == 15) and (y <= 15 and y >= 12) or (x == 20) or (x == 19) or (x >= 21 and x <= 29) and (y == 10)):
                if (x,y) in traffic_light_positions:
                    a = TrafficLight(traffic_light_positions[(x,y)], col, self)
                    self.grid.place_agent(a, (x,y))
                else:
                    a = Field((x,y), self)
                    self.grid.place_agent(a, (x,y))
            # elif not((x >= 0 and x <= 18) and (y <= 11 and y >= 9)):
            #    a = Field((x,y), self)
            #    self.grid.place_agent(a, (x,y))

            # elif not((x == 11) and (y <= 8 and y >= 0)):
            #     a = Field((x,y), self)
            #     self.grid.place_agent(a, (x,y))

            # elif not((x == 12) and (y <= 8 and y >= 0)):
            #     a = Field((x,y), self)
            #     self.grid.place_agent(a, (x,y))

            # elif not((x == 15) and (y = 15 and y >= 12)):
            #     a = Field((x,y), self)
            #     self.grid.place_agent(a, (x,y))

            # elif not((y == 20) or (y == 19)):
            #     a = Field((x,y), self)
            #     self.grid.place_agent(a, (x,y))
            
            # elif not((x >= 21 and x <= 29) and (y == 10)):
            #     a = Field((x,y), self)
            #     self.grid.place_agent(a, (x,y))

        self.datacollector = DataCollector(
        model_reporters={"Grid": get_grid}
        )
        
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # if self.traffic_counter < self.traffic_time:
        #     self.traffic_counter += 1
        # else:
        #     for i, direction in enumerate(Car.DIRECTIONS):
        #         # print(self.traffic_lights)
        #         if self.traffic_lights[direction].colour == 'green':
        #             self.traffic_counter = 0
        #             self.traffic_lights[direction].colour = 'red'

        #             next_i = i + 1 if i < len(Car.DIRECTIONS) - 1 else 0
        #             self.traffic_lights[Car.DIRECTIONS[next_i]].colour = 'green'
        #             break
            


                


# -17



        

