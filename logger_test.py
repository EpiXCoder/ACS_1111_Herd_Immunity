from logger import Logger

'''
This file tests the logger.py program
'''

test_log = Logger('test_logger_py.txt')
test_log.write_metadata(10000, 0.4, 'Corona Virus', 0.3, 0.5)
test_log.log_interactions(104566, 2345)
test_log.log_infection_survival(9500, 345)
test_log.log_final_summary(6890, 3110, 6890, 'everyone became zombies', 20495776, 0, 20495776)


with open('test_logger_py.txt') as log_file:
        lines = log_file.readlines()
        assert lines[0] == 'SIMULATION METADATA:\n'
        assert lines[1] == '\t\tPopulation Size: 10000\n'
        assert lines[2] == '\t\tVaccination Percentage: 0.4\n'
        assert lines[3] == '\t\tVirus: Corona Virus\n'
        assert lines[4] == '\t\tMortality Rate: 0.3\n'
        assert lines[5] == '\t\tReproduction Number: 0.5\n'

        assert lines[6] == '\n'
        assert lines[7] == '\tINTERACTIONS:\n'
        assert lines[8] == '\t\tNumber of Interactions: 104566\n'
        assert lines[9] == '\t\tNumber of New Infections: 2345\n'

        assert lines[10] == '\n'
        assert lines[11] == '\tINFECTION SURVIVAL:\n'
        assert lines[12] == '\t\tCurrent Population Count: 9500\n'
        assert lines[13] == '\t\tNumber of New Fatalities: 345\n'
        

        assert lines[14] == '\n'
        assert lines[15] == '-------------------------------------------------------------------\n'
        assert lines[16] == '-------------------------------------------------------------------\n'
        assert lines[17] == '\n'
        assert lines[18] == '\tSIMULATION SUMMARY:\n'
        assert lines[19] == '\t\t✺ The simulation ended with 6890 survivors (of whom 6890 are now vaccinated) and 3110 fatalities.\n'
        assert lines[20] == '\t\t✺ The simulation ended because everyone became zombies.\n'
        assert lines[21] == '\t\t✺ In total, 20495776 interactions were simulated. Of which, 0 interactions were conducive to immunity acquisition and 20495776 interactions were potentially infectious.'

