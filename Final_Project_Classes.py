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

        # Box size, x_min, x_max, y_min, ...
        self.boxsize =(-board_x,board_x,-board_y,board_y,-board_z,board_z)
        self.volume = 8*board_x*board_y*board_z

        self.n = num_particles
        self.particles = []
        self.dt = 0.01

        self.temp = temp     # degrees Kelvin
        self.pressure = self.n * self.temp / self.volume
        self.energy = 3/2 * self.temp

        self.temp_arr = [self.temp]
        self.pressure_arr = [self.pressure]
        self.energy_arr = [self.energy]
        self.volume_arr = [self.volume]

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
            # for other in self.particles:
            #     if p.pos == other.pos:
            #         continue
            #     dist = np.sqrt((p.pos.x-other.pos.x)**2+(p.pos.y-other.pos.y)**2+(p.pos.z-other.pos.z)**2)
            #     if dist < 0.4:
            #         p.pos.x *= -1
            #         p.pos.y *= -1
            #         p.pos.z *= -1
            # Reflect off walls of box
            if p.pos.x >= (self.board_x-0.2) or p.pos.x <= (-self.board_x+0.2):
                p.velocity.x *= -1
            if p.pos.y >= (self.board_y-0.2) or p.pos.y <= (-self.board_y+0.2):
                p.velocity.y *= -1
            if p.pos.z >= (self.board_z-0.2) or p.pos.z <= (-self.board_z+0.2):
                p.velocity.z *= -1

            if p.pos.x > (self.board_x-0.2):
                p.pos.x = self.board_x-0.2
            elif p.pos.x < -(self.board_x-0.2):
                p.pos.x = -(self.board_x-0.2)
            if p.pos.y > (self.board_y-0.2):
                p.pos.y = self.board_y-0.2
            elif p.pos.y < -(self.board_y-0.2):
                p.pos.y = -(self.board_y-0.2)
            if p.pos.z > (self.board_z-0.2):
                p.pos.z = self.board_z-0.2
            elif p.pos.z < -(self.board_z-0.2):
                p.pos.z = -(self.board_z-0.2)

    def update(self, rate=0):
        '''
        Keep the system the same
        '''
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        self.move()

class isochoric(system):
    # Constant volume

    def update(self, rate=0.1):
        '''
        Change the energy and update state of the particles
        '''
        self.energy += rate
        self.temp = 2/3 * self.energy
        self.pressure = self.n * self.temp / self.volume

        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        self.move()

class isothermal(system):
    # Constant temperature

    def update(self, rate=0.1):
        '''
        Change the volume and update the state of the particles
        '''
        self.volume += rate
        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        self.pressure = self.n * self.temp / self.volume

        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        self.move()

class isentropic(system):
    # Constant entropy

    def update(self, rate):
        '''
        Changing volume and update the state of the particles
        '''
        v1 = self.volume
        self.volume += rate
        self.temp = self.temp * (v1/self.volume)**(0.66)
        self.energy = 3/2 * self.temp
        self.pressure = self.pressure * (v1/self.volume)**(1.66)

        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        self.move()

class carnot(system):

    def update_isothermal(self, rate=0.1):
        '''
        Change the volume and update the state of the particles
        '''
        self.volume += rate
        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        self.pressure = self.n * self.temp / self.volume

        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        self.move()

    def update_isentropic(self, rate):
        '''
        Changing volume and update the state of the particles
        '''
        v1 = self.volume
        self.volume += rate
        self.temp = self.temp * (v1/self.volume)**(0.66)
        self.energy = 3/2 * self.temp
        self.pressure = self.pressure * (v1/self.volume)**(1.66)

        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        self.move()
