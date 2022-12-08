import random
# random.seed(42)
from virus import Virus


class Person(object):
    # Define a person. 
    def __init__(self, _id, is_vaccinated, infection = None):
        '''
        initalizes Person isntance attributes
        '''
        self._id = _id  # int
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = True
        self.is_infected = None

    def did_survive_infection(self):
        '''
        This method checks if a person survived an infection.
        '''  
        if self.infection is not None:
            mortality_rate = self.infection.mortality_rate
            infection_probability = random.random()
            if infection_probability < mortality_rate:
                self.is_alive = False
                self.is_infected = True
            else:
                self.is_vaccinated = True
                self.is_alive =  True
                self.is_infected = True
        return (self.is_alive, self.is_infected)


        

if __name__ == "__main__":
    '''
    testing Person class
    '''

    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_alive is True
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None
    print(vaccinated_person.did_survive_infection())

    # An unvaccinated person 
    unvaccinated_person = Person(2, False)
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_alive is True
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None
    print(unvaccinated_person.did_survive_infection())

    # An infected person. An infected person has an infection/virus
    virus = Virus("Dysentery", 0.7, 0.2)
   
    infected_person = Person(3, False, virus)
    assert infected_person._id == 3
    assert infected_person.is_alive is False or True
    assert infected_person.is_vaccinated is False
    assert infected_person.infection is virus
    print(infected_person.did_survive_infection())

    # Creating a list to hold 100 people. 
    people = []
    for i in range(1, 101):
        vaccinated = random.choice([True, False])
        person = Person(i, vaccinated, virus)
        people.append(person)

    # Now that we have a list of 100 people, let's resolve whether the Person survives the infection or not by looping over the people list. 
    # Counting the people that survived and did not survive: 
   
    did_survive = 0
    did_not_survive = 0

    for person in people:
        survived = person.did_survive_infection()[0]
        if survived:
            did_survive += 1
        else:
            did_not_survive += 1

    print('Survived:', did_survive)
    print('Did not survive:', did_not_survive)

    # Stretch challenge! 
    # Check the infection rate of the virus by making a group of 
    # unifected people. Loop over all of your people. 
    # Generate a random number. If that number is less than the 
    # infection rate of the virus that person is now infected. 
    # Assign the virus to that person's infection attribute. 

    # Now count the infected and uninfect people from this group of people. 
    # The number of infectedf people should be roughly the same as the 
    # infection rate of the virus.

    # people2 = []
    # for i in range(1, 101):
    #     vaccinated = random.choice([True, False])
    #     person = Person(i, vaccinated)
    #     people2.append(person)

    # infected = 0
    # not_infected = 0

    # for person in people2:
    #     is_infected = person.did_survive_infection()[1]
    #     if is_infected:
    #         infected += 1
    #     else:
    #         not_infected += 1

    # print('Infected:', infected)
    # print('Not infected:', not_infected)