# The file to store our classes
import numpy as np
from ivisual import *

class system:
    def __init__(self, board_x=10, board_y=10, board_z=10, num_particles=100, temp=2):
        '''
        Initialize the board
        '''
        self.board_x = board_x   # Size is from 0 to these maximums
        self.board_y = board_y
        self.board_z = board_z

        self.n = num_particles
        self.particles = []
        self.initialize_particles()
        self.dt = 0.01

        self.temp = temp     # degrees Kelvin
        self.energy = 3/2 * self.temp


    def initial_particles(self):
        '''
        Initialize the list of particles
        '''
        for i in range(self.n):
            pos_x = np.random.uniform(0,self.board_x-0.2)  # Subtract the radius
            pos_y = np.random.uniform(0,self.board_y-0.2)
            pos_z = np.random.uniform(0,self.board_z-0.2)
            particle = sphere(pos=tuple(pos_x,pos_y,pos_z), radius=0.2)
            particle.mass = 4
            vel = np.random.uniform(0,1,size=3)
            vel = vel/np.linalg.norm(vel)*(2*particle.mass*self.energy)**(1/2)

            self.particles.append(particle)

    def move(self):
        '''
        Update the positions of the particles (one iteration)
        '''
        for p in self.particles:
            p.pos += p.velocity*self.dt
            if p.pos.x >= self.board_x or p.pos.x <= 0:
                p.velocity.x *= -1
            if p.pos.y >= self.board_y or p.pos.y <= 0:
                p.velocity.y *= -1
            if p.pos.z >= self.board_z or p.pos.z <= 0:
                p.velocity.z *= -1
