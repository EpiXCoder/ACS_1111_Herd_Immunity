import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
import argparse



class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        '''
        This function initalizes the Simulation object instance
        '''
        self.logger = Logger('log.txt')
        self.virus  = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.people = self._create_population()
        self.new_vaccinations = 0
        self.newly_infected = []
        self.fatality_list = []
        self.deaths_total = 0
        self.protected_by_vaccine = 0
        self.number_of_interactions = 0
        self.infection_event = 0
        self.infected_individuals = 0
        self.sim_end_reason = ''


    def _create_population(self):
        '''
        This function creates the population for the simulation
        '''
        number_vaccinated = self.vacc_percentage * self.pop_size
        people= []
        for i in range(1, int(self.pop_size)+1):
            if i <= self.initial_infected:
                person = Person(i, False, self.virus)
            elif number_vaccinated > 0: 
                person = Person(i, True)
                number_vaccinated -= 1
            else:
                person = Person(i, False)
            people.append(person)
        return people
        

    def _simulation_should_continue(self):
        '''
        This method returns a boolean indicating if the simulation should continue. The simulation will not continue if all of the people are dead, or if all of the living people have been vaccinated. 
        '''
        should_continue = True
        vulnerable = None
        infected = None
        for person in self.people:
            if person.is_vaccinated == False and person.is_alive:
                vulnerable = True
            if person.is_alive and person.infection is not None:
                infected = True
            
        self.sim_end_reason = 'everyone in the population were either immune or dead'
        should_continue = vulnerable and infected
        return should_continue


    def run(self):
        '''
        This method starts the simulation. It tracks the number of steps the simulation has run and checks if the simulation should continue at the end of each step. 
        It also writes the simulation statistics to the log file
        '''

        time_step_counter = 0
        should_continue = True

        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while should_continue:
            time_step_counter += 1
            self.time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        people_alive_final = 0
        vaccinated_individuals = 0
        for person in self.people:
            if person.is_alive:
                people_alive_final += 1
            if person.is_vaccinated and person.is_alive:
                vaccinated_individuals +=1

        self.logger.log_final_summary(people_alive_final, self.deaths_total, self.infected_individuals, self.sim_end_reason, self.number_of_interactions, self.protected_by_vaccine, self.infection_event)
        
    def time_step(self, step_number):
        '''
        This method simulates interactions between people, calulates new infections, and determines if vaccinations and fatalities from infections
        The goal is to have each infected person interact with a number of other people in the population
        '''
        case_interactions = 0
        for person in self.people:
            if person.infection is not None:
                for i in range(0,100):
                    random_pick = random.randint(0, self.pop_size-1)
                    self.interaction(person, self.people[random_pick])
                    case_interactions += 1 

        self.number_of_interactions += case_interactions

        self.logger.log_time_step(step_number)

        self.logger.log_interactions(case_interactions, len(self.newly_infected))

        self._infect_newly_infected()

        # determines if vaccinations and fatalities from infections
        new_deaths = 0
        people_alive = 0
        for person in self.people:
            if person.infection is not None and person.is_alive:
                is_now_alive = person.did_survive_infection()[0]
                if is_now_alive == False:
                    new_deaths += 1
                    self.fatality_list.append(person)
                    self.deaths_total += 1
            if person.is_alive:
                people_alive += 1
                
        self.logger.log_infection_survival(people_alive, new_deaths)

    def interaction(self, infected_person, random_person):
        '''
        This method simulated the interaction between an infected person and a random person from the population
        '''
        if random_person.is_vaccinated == False and random_person.is_alive == True and random_person.infection == None:
            random_chance = random.random()
            if random_chance < self.virus.repro_rate:
                self.infection_event += 1
                if random_person not in self.newly_infected:
                    self.newly_infected.append(random_person)                
        elif random_person.is_vaccinated and random_person.is_alive and random_person.infection == None:
            self.protected_by_vaccine += 1


    def _infect_newly_infected(self):
        '''
        this method is called at the end of every time step and infect each people who have been selected as infectees after interactions
        '''
        for person in self.people:
            if person in self.newly_infected:
                person.infection = self.virus
                self.infected_individuals +=1
                
            
        self.newly_infected = []


#Tests for the simulation has been moved to simulation_test.py


# argparse

parser = argparse.ArgumentParser(description = 'adds arguments for the simulator')

parser.add_argument('virus_name', metavar='virus_name', type=str, help='enter virus_name')
parser.add_argument('repro_num', metavar='repro_num', type=float, help='enter repro_num')
parser.add_argument('mortality_rate', metavar='mortality_rate', type=float, help='enter mortality_rate')
parser.add_argument('pop_size', metavar='pop_size', type=int, help='enter pop_size')
parser.add_argument('vacc_percentage', metavar='vacc_percentage', type=float, help='enter vacc_percentage')
parser.add_argument('initial_infected', metavar='initial_infected', type=int, help='enter initial_infected')
args = parser.parse_args()


virus_name = args.virus_name
repro_num = args.repro_num
mortality_rate = args.mortality_rate
pop_size = args.pop_size
vacc_percentage = args.vacc_percentage 
initial_infected = args.initial_infected

virus = Virus(virus_name, repro_num, mortality_rate)
sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

sim.run()

# ARGPARSE NOTES - enter values in the following order:
    # {virus_name} {repro_rate} {mortality_rate} {population size} {vacc_percentage} {number of people initially infected (default is 1)}
# $ python3 simulation.py Ebola 0.25 0.70 10000 0.70 10
