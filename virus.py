class Virus(object):
    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


# Test the Virus class
if __name__ == "__main__":
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    tb = Virus("Tuberculosis", 0.6, 0.07)
    assert tb.name == "Tuberculosis"
    assert tb.repro_rate == 0.6
    assert tb.mortality_rate == 0.07

    tb = Virus("Ebola", 1.5, 0.5)
    assert tb.name == "Ebola"
    assert tb.repro_rate == 1.5
    assert tb.mortality_rate == 0.5