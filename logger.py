class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        '''
        writes simulation metadata to log
        '''
        with open(self.file_name, 'w') as out_file:
            sim_metadata = f'SIMULATION METADATA:\n\t\tPopulation Size: {pop_size}\n\t\tVaccination Percentage: {vacc_percentage}\n\t\tVirus: {virus_name}\n\t\tMortality Rate: {mortality_rate}\n\t\tReproduction Number: {basic_repro_num}\n'
            out_file.write(sim_metadata)

    def log_interactions(self, number_of_interactions, number_of_new_infections):
        '''
        writes interacters per step to log
        '''
        interaction_log = f'\n\tINTERACTIONS:\n\t\tNumber of Interactions: {number_of_interactions}\n\t\tNumber of New Infections: {number_of_new_infections}\n'
        with open(self.file_name, 'a') as out_file:
            out_file.write(interaction_log)

    def log_infection_survival(self, population_count, number_of_new_fatalities):
        '''
        writes infection survival statistics per step to log
        '''
        survival_log = f'\n\tINFECTION SURVIVAL:\n\t\tCurrent Population Count: {population_count}\n\t\tNumber of New Fatalities: {number_of_new_fatalities}\n'
        with open(self.file_name, 'a') as out_file:
            out_file.write(survival_log)

    def log_time_step(self, time_step_number):
        '''
        creates line separations per step in the log
        '''
        step_line = f'\n----------------------- Step Number: {time_step_number} -----------------------'
        with open(self.file_name, 'a') as out_file:
            out_file.write(step_line)

    def log_final_summary(self, total_living, total_dead, num_infected, sim_end_reason, num_interactions, num_vacc_interaction, num_inf_interaction):
        '''
        writes the final summary of the simulation to log
        '''
        line = f'\n-------------------------------------------------------------------\n-------------------------------------------------------------------\n'
        final_log1 = f'\n\tSIMULATION SUMMARY:\n\t\t✺ The simulation ended with {total_living} survivors, {num_infected} infected individuals and {total_dead} fatalities.\n\t\t✺ The simulation ended because {sim_end_reason}.'
        final_log2 = f'\n\t\t✺ In total, {num_interactions} interactions were simulated. Of which, {num_vacc_interaction} interactions were condusive to immunity acquisition and {num_inf_interaction} interactions were potentially infectious.'
        final_log = line + final_log1 + final_log2
        with open(self.file_name, 'a') as out_file:
            out_file.write(final_log)