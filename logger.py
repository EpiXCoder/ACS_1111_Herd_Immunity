class Logger(object):
    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    # The methods below are just suggestions. You can rearrange these or 
    # rewrite them to better suit your code style. 
    # What is important is that you log the following information from the simulation:
    # Meta data: This shows the starting situtation including:
    #   population, initial infected, the virus, and the initial vaccinated.
    # Log interactions. At each step there will be a number of interaction
    # You should log:
    #   The number of interactions, the number of new infections that occured
    # You should log the results of each step. This should inlcude: 
    #   The population size, the number of living, the number of dead, and the number 
    #   of vaccinated people at that step. 
    # When the simulation concludes you should log the results of the simulation. 
    # This should include: 
    #   The population size, the number of living, the number of dead, the number 
    #   of vaccinated, and the number of steps to reach the end of the simulation. 

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        
        with open(self.file_name, 'r') as file:
            log_data = file.readlines()

        num_sim = int(log_data[0][-1])
        log_data[0] = f'Number of Simulations: {num_sim +1}'

        with open(self.file_name, 'w') as file:
            file.writelines(log_data)

        log_data.close()
        file.close()

        with open(self.file_name, 'a') as out_file:
            sim_metadata = f'SIMULATION {num_sim + 1}\n\tMETADATA\n\t\tPopulation Size: {pop_size}\n\tVaccination Percentage: {vacc_percentage}\n\t\tVirus: {virus_name}\n\t\tMortality Rate: {mortality_rate}\n\t\tReproduction Number: {basic_repro_num}\n'
            out_file.write(sim_metadata)

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        interaction_log = f'\n\tINTERACTIONS\n\t\tStep Number: {step_number}\n\t\tNumber of Interactions: {number_of_interactions}\n\t\tNumber of New Infections: {number_of_new_infections}\n'
        with open(self.file_name, 'a') as out_file:
            out_file.write(interaction_log)

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        survival_log = f'\n\tINFECTION SURVIVAL\n\t\tStep Number: {step_number}\n\t\tCurrent Population Count: {population_count}\n\t\tNumber of New Fatalities: {number_of_new_fatalities}\n'
        with open(self.file_name, 'a') as out_file:
            out_file.write(survival_log)

    def log_time_step(self, time_step_number):
        # 
        pass

    def log_final_summary(self, total_living, total_dead, num_vaccinated, sim_end_reason, num_interactions, num_vacc_interaction, num_fatal_interaction):
        final_log1 = f'\n\tSIMULATION SUMMARY\n\t\t The simulation ended with {total_living} survivors, {total_dead} fatalities and {num_vaccinated} vaccinated individuals. The simulation ended because {sim_end_reason}.'
        final_log2 = f'\n\t\t In total, {num_interactions} interactions were simulated. Of which, {num_vacc_interaction} interactions resulted in immunity acquisition and {num_fatal_interaction} interactions were fatal.'
