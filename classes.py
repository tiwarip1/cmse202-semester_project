# The file to store our classes
import numpy as np
from ivisual import *

class system:
    def __init__(self, board_x=10, board_y=10, board_z=10, num_particles=100, temp=2, pressure=1):
        '''
        Initialize the board
        '''
        self.board_x = board_x   # Size is from 0 to these maximums
        self.board_y = board_y
        self.board_z = board_z

        # Box size, x_min, x_max, y_min, ...
        self.boxsize =(-board_x,board_x,-board_y,board_y,-board_z,board_z)
        self.volume = 8*board_x*board_y*board_z

        self.n = num_particles
        self.particles = []
        self.dt = 0.01

        self.temp = temp     # degrees Kelvin
        self.pressure = pressure
        self.energy = 3/2 * self.temp

        self.temp_arr = []
        self.pressure_arr = []
        self.energy_arr = []
        self.volume_arr = []

        self.initial_particles()


    def initial_particles(self):
        '''
        Initialize the list of particles
        '''
        for i in range(self.n):
            pos_x = np.random.uniform(-self.board_x+0.2,self.board_x-0.2)  # Subtract the radius
            pos_y = np.random.uniform(-self.board_y+0.2,self.board_y-0.2)
            pos_z = np.random.uniform(-self.board_z+0.2,self.board_z-0.2)
            particle = sphere(pos=tuple((pos_x,pos_y,pos_z)), radius=0.2)
            particle.mass = 4
            vel = np.random.uniform(0,1,size=3)
            vel = vector(vel/np.linalg.norm(vel)*(2*particle.mass*self.energy)**(1/2))
            particle.velocity = vel

            self.particles.append(particle)

    def move(self):
        '''
        Update the positions of the particles (one iteration)
        '''
        for p in self.particles:
            p.pos += p.velocity*self.dt
            if p.pos.x >= (self.board_x-0.2) or p.pos.x <= (-self.board_x+0.2):
                p.velocity.x *= -1
            if p.pos.y >= (self.board_y-0.2) or p.pos.y <= (-self.board_y+0.2):
                p.velocity.y *= -1
            if p.pos.z >= (self.board_z-0.2) or p.pos.z <= (-self.board_z+0.2):
                p.velocity.z *= -1

    def update(self):
        self.move()

class isochoric(system):
    # Constant volume
	
    def update(self, rate=0.1):
        '''
        Change the energy and update state of the particles
        '''
        self.energy += (3/2)*self.temp*rate
        self.temp = 2/3 * self.energy
        self.pressure = self.n * self.temp / self.volume

        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)

        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        self.move()
