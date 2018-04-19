'''
Final_Project_Classes.py

Contains the classes used in Final_Project_Visualization.ipynb.
The system class is the base class for all models.
Isochoric, isothermal, isentropic, and carnot classes are derived from the system
class.
'''
import numpy as np
from ivisual import *

class system:
    '''
    Serves as the base class for other thermodynamic model classes.
    Initializes the system variables, creates particles, and contains move() for
    particles.
    '''
    def __init__(self, board_x=10, board_y=10, board_z=10, num_particles=100, temp=2):
        '''
        Initialize the box dimensions, system variables, and particles.
        :param board_x: (type int) Half of x axis dimension
        :param board_y: (type int) Half of y axis dimension
        :param board_z: (type int) Half of z axis dimension
        :param num_particles: (type int) Number of particles in system
        :param temp: (type int or float) Initial temperature of the system
        '''
        self.board_x = board_x
        self.board_y = board_y
        self.board_z = board_z

        # Save dimensions of box and calculate volume
        self.boxsize =(-board_x,board_x,-board_y,board_y,-board_z,board_z)
        self.volume = 8*board_x*board_y*board_z

        # Initialize list of particles
        self.n = num_particles
        self.particles = []   # List holding particles (sphere objects)
        self.dt = 0.01        # Step of velocity change for particles

        # Calculate pressure and energy of the system based on temperature
        self.temp = temp
        self.pressure = self.n * self.temp / self.volume
        self.energy = 3/2 * self.temp

        # Initialize lists that will hold system variables throughout simulation
        self.temp_arr = [self.temp]
        self.pressure_arr = [self.pressure]
        self.energy_arr = [self.energy]
        self.volume_arr = [self.volume]

        # Initialize the particles
        self.initial_particles()


    def initial_particles(self):
        '''
        Initialize the list of particles (ivisual sphere objects)
        :return: None
        '''
        # Loop over the number of particles
        for i in range(self.n):
            # Randomly generate position (3 dimensions)
            pos_x = np.random.uniform(-self.board_x+0.2,self.board_x-0.2)  # Subtract the radius
            pos_y = np.random.uniform(-self.board_y+0.2,self.board_y-0.2)
            pos_z = np.random.uniform(-self.board_z+0.2,self.board_z-0.2)

            # Create sphere object with position (above) and add mass
            particle = sphere(pos=tuple((pos_x,pos_y,pos_z)), radius=0.2)
            particle.mass = 4

            # Randomly calculate velocity with equal magnitudes
            vel = np.random.uniform(0,1,size=3)
            vel = vector(vel/np.linalg.norm(vel)*(2*particle.mass*self.energy)**(1/2))
            particle.velocity = vel

            # Add particle to list of particles
            self.particles.append(particle)

    def move(self):
        '''
        Update the positions of the particles (one iteration)
        :return: None
        '''
        # Iterate over list of particles
        for p in self.particles:
            # Update position based on velocity
            p.pos += p.velocity*self.dt

            # Could have particles interact, but chose to not include
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

            # If box size has changed, make sure to stay inside the box
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
        Keep the system variables the same, update the particles
        '''
        # Append to lists of system variables
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        # Update the particles
        self.move()

class isochoric(system):
    '''
    Inherits from the system class; models an isochoric system - constant volume
    '''
    def update(self, rate=0.1):
        '''
        Change the energy and update state of the particles.
        :params rate: (type float) the rate at/amount by which the energy changes
        '''
        # Update energy, temperature and pressure
        self.energy += rate
        self.temp = 2/3 * self.energy
        self.pressure = self.n * self.temp / self.volume

        # Append variables to lists to keep track
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        # Iterate over particles and update velocities
        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        # Update positions of particles
        self.move()

class isothermal(system):
    '''
    Inherits from the system class; models an isothermal system - constant temperature
    '''

    def update(self, rate=0.1):
        '''
        Change the volume and update the state of the particles
        :params rate: (type float) the rate by which the volume changes
        '''
        # Update the volume and dimensions of the box
        self.volume += rate
        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        # Update the pressure
        self.pressure = self.n * self.temp / self.volume

        # Keep track of the state variables
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        # Update the positions of the particles
        self.move()

class isentropic(system):
    '''
    Inherits from the system class; models an isentropic system - constant entropy
    '''

    def update(self, rate=0.1):
        '''
        Changing volume and update the state of the particles:
        :params rate: (type float) the rate by which the volume changes
        '''
        # Update all of the state variables of the system
        v1 = self.volume
        self.volume += rate
        self.temp = self.temp * (v1/self.volume)**(0.66)
        self.energy = 3/2 * self.temp
        self.pressure = self.pressure * (v1/self.volume)**(1.66)

        # Update the dimensions of the box
        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        # Append the variables to lists to keep track
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        # Iterate over particles and update velocities
        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        # Update positions of the particles
        self.move()

class carnot(system):
    '''
    Inherits from the system class; Models a carnot cycle
    '''

    def update_isothermal(self, rate=0.1):
        '''
        Change the volume and update the state of the particles
        :params rate: (type float) the rate by which the volume changes
        '''
        # Update the volume and box dimensions
        self.volume += rate
        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        # Update the pressure
        self.pressure = self.n * self.temp / self.volume

        # Append the state variables to lists to keep track
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        # Update the positions of the particles
        self.move()

    def update_isentropic(self, rate=0.1):
        '''
        Changing volume and update the state of the particles
        :params rate: (type float) the rate by which the volume changes
        '''
        # Update the volume and other system variables
        v1 = self.volume
        self.volume += rate
        self.temp = self.temp * (v1/self.volume)**(0.66)
        self.energy = 3/2 * self.temp
        self.pressure = self.pressure * (v1/self.volume)**(1.66)

        # Update the dimensions of the box
        self.board_y = self.volume/(8*self.board_x*self.board_z)
        self.boxsize =(-self.board_x,self.board_x,-self.board_y,self.board_y,-self.board_z,self.board_z)

        # Keep track of the system variables
        self.energy_arr.append(self.energy)
        self.temp_arr.append(self.temp)
        self.pressure_arr.append(self.pressure)
        self.volume_arr.append(self.volume)

        # Iterate over the particles and update velocities
        for p in self.particles:
            vel = np.array([p.velocity.x, p.velocity.y, p.velocity.z])
            p.velocity = vector(vel/np.linalg.norm(vel)*(2*p.mass*self.energy)**(1/2))

        # Update the positions of the particles
        self.move()
