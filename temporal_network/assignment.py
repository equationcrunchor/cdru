__author__ = 'yupeng'

class Assignment(object):

    def __init__(self, decision_variable, value, utility):
        self.decision_variable = decision_variable
        self.value = value
        self.utility = utility

    def __lt__(self, other):
        return self.utility > other.utility

    def pretty_print(self):
        print(self)

    def __eq__(self, other):
        return self.decision_variable == other.decision_variable and self.value == other.value

    def __hash__(self):
        return hash((self.decision_variable, self.value))

    def __str__(self):
        return self.decision_variable.name + " <- "+ self.value +" ("+str(self.utility)+")"

    def __repr__(self):
        return str(self)
