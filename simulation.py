import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
import argparse



class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        
        # TODO: Store the virus in an attribute
        # TODO: Store pop_size in an attribute
        # TODO: Store the vacc_percentage in a variable
        # TODO: Store initial_infected in a variable
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not. 
        # Use the _create_population() method to create the list and 
        # return it storing it in an attribute here. 
        # TODO: Call self._create_population() and pass in the correct parameters.
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
        self.sim_end_reason = ''


    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people
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
        # This method will return a booleanb indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        should_continue = True
        vulnerable = 0
        infected = 0
        for person in self.people:
            if person.is_vaccinated == False and person.is_alive:
                vulnerable = True
            if person.is_alive and person.infection is not None:
                infected = True
            self.sim_end_reason = 'everyone in the population were either immune or dead'

        return vulnerable and infected


    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        time_step_counter = 0
        should_continue = True

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            time_step_counter += 1
            self.time_step(time_step_counter)
            should_continue = self._simulation_should_continue()


        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 
        people_alive_final = 0
        vaccinated_individuals = 0
        for person in self.people:
            if person.is_alive:
                people_alive_final += 1
            if person.is_vaccinated and person.is_alive:
                vaccinated_individuals +=1

        self.logger.log_final_summary(people_alive_final, self.deaths_total, vaccinated_individuals, self.sim_end_reason, self.number_of_interactions, self.protected_by_vaccine, self.infection_event)
        
    def time_step(self, step_number):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        case_interactions = 0
        for person in self.people:
            if person.infection is not None:
                for i in range(0,100):
                    random_pick = random.randint(0, self.pop_size-1)
                    self.interaction(person, self.people[random_pick])
                    case_interactions += 1 

        self.number_of_interactions += case_interactions

        self.logger.log_interactions(step_number, case_interactions, len(self.newly_infected))

        self._infect_newly_infected()

        # determine if vaccinations and fatalities from infections
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
                
        self.logger.log_infection_survival(step_number, people_alive, new_deaths)

    def interaction(self, infected_person, random_person):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0.0 and 1.0.  If that number is smaller
            #     than repro_rate, add that person to the newly infected array
            #     Simulation object's newly_infected array, so that their infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        if random_person.is_vaccinated == False and random_person.is_alive == True and random_person.infection == None:
            random_chance = random.random()
            if random_chance < self.virus.repro_rate:
                self.infection_event += 1
                if random_person not in self.newly_infected:
                    self.newly_infected.append(random_person)                
        elif random_person.is_vaccinated and random_person.is_alive and random_person.infection == None:
            self.protected_by_vaccine += 1


    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.people:
            if person in self.newly_infected:
                person.infection = self.virus
                
            
        self.newly_infected = []


# if __name__ == "__main__":
#     # Test your simulation here
#     virus_name = "Sniffles"
#     repro_num = 0.5
#     mortality_rate = 0.12
   

#     # Set some values used by the simulation
#     pop_size = 1000
#     vacc_percentage = 0.1
#     initial_infected = 10

#     # Make a new instance of the simulation
#     # virus = Virus(virus, pop_size, vacc_percentage, initial_infected)
#     virus = Virus(virus_name, repro_num, mortality_rate)
#     sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
#     sim.run()


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
# {virus_name} {repro_rate} {mortality_rate} {population size} {vacc_percentage} {optional: number of people initially infected (default is 1)}
# $ python3 simulation.py Ebola 0.25 0.70 10000 0.70 10
