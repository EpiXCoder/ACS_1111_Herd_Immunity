import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
from simulation import Simulation

'''This is where the tests for the simulation will be run.'''

if __name__ == "__main__":
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
   
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim.run()
