__author__ = 'yupeng'

import copy
from .assignment import Assignment

class DecisionVariable(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.domain = set()
        self.guards = set()

        self.optimal_utility = 0

    def __lt__(self, other):
        return self.optimal_utility > other.optimal_utility

    def add_domain_value(self,value):
        self.domain.add(value)

    def add_guard(self,guard):
        self.guards.add(guard)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __deepcopy__(self, memo):
        other = DecisionVariable(self.id, self.name)
        memo[id(self)] = other
        other.domain = set()
        for assignment in self.domain:
            new_assignment = Assignment(other, assignment.value, assignment.utility)
            other.domain.add(new_assignment)
        other.guards = copy.deepcopy(self.guards, memo)
        return other
