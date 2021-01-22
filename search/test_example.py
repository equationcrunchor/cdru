__author__ = 'yupeng'

import sys, os
from os.path import join, dirname
sys.path.insert(0, join(dirname(__file__), '..'))

from math import fabs
from tpn import Tpn
from temporal_network.tpnu import Tpnu, ChanceConstrained
from search.search_problem import SearchProblem
from temporal_network.tpnu import FeasibilityType, ObjectiveType
from temporal_network.decision_variable import DecisionVariable
from temporal_network.temporal_constraint import TemporalConstraint
from temporal_network.assignment import Assignment
from search.mip_encode import MipEncode
from datetime import datetime

from uuid import uuid4

#  def getProblemFromFile(path):
#      if Tpnu.isCCTP(path):
#          tpnu = Tpnu.parseCCTP(path)
#      elif Tpnu.isTPN(path):
#          obj = Tpn.parseTPN(path)
#          tpnu = Tpnu.from_tpn_autogen(obj)
#      else:
#          raise Exception("Input file " + path + " is neither a CCTP nor a TPN")

#      return tpnu

#  example_file = 'Zipcar-1.cctp'

#  cdru_dir = dirname(__file__)
#  examples_dir = join(cdru_dir, join('..', 'examples'))
#  path = join(examples_dir, example_file)
#  tpnu = getProblemFromFile(path)


# NOTE: Limitation: Assumes num_nodes = N, then events are indexed by 1, 2, ..., N
# TODO: Currently, Tpnu.from_tpn_autogen does map eventID to numbers, but it does not take TPNU as input, if we want to use arbitrary event names, we need to add such a function/mapping
tpnu = Tpnu(str(uuid4()), 'example-tpnu')
tpnu.start_node = 1
tpnu.num_nodes = 3

# Initialize a decision variable
dv = DecisionVariable(str(uuid4()), 'dv')
as1 = Assignment(dv, 'dv-true', 10)
as2 = Assignment(dv, 'dv-false', 3)
dv.add_domain_value(as1)
dv.add_domain_value(as2)
tpnu.add_decision_variable(dv)

# Initialize temporal constraints
tc1 = TemporalConstraint(str(uuid4()), 'tc1', 1, 2, 0, 10)
tc1.controllable = False
tpnu.add_temporal_constraint(tc1)
tc2 = TemporalConstraint(str(uuid4()), 'tc2', 2, 3, 0, 10)
tc2.controllable = False
tpnu.add_temporal_constraint(tc2)
tc3 = TemporalConstraint(str(uuid4()), 'tc3', 1, 3, 0, 15)
tc3.add_guard(as1)
tc3.relaxable_ub = True
tc3.relaxable_lb = False
tc3.relax_cost_ub = 1
tpnu.add_temporal_constraint(tc3)

#  tpnu = Tpnu.from_tpn_autogen()

print(tpnu)
print(tpnu.decision_variables)
print(tpnu.num_nodes)
print(tpnu.temporal_constraints)
print(tpnu.chance_constraints)
print(tpnu.node_number_to_id)
print(tpnu.start_node)

f_type = FeasibilityType.DYNAMIC_CONTROLLABILITY
o_type = ObjectiveType.MIN_COST
c_type = ChanceConstrained.OFF

startTime = datetime.now()
search_problem = SearchProblem(tpnu,f_type,o_type,c_type)
search_problem.initialize()

# Find all solutions
solution = search_problem.next_solution()
while solution is not None:
    runtime = datetime.now() - startTime
    print("----------------------------------------")
    print("Solution found")
    #  print(example_file)
    solution.pretty_print()
    print(solution.json_print("example-tpnu","CDRU+PuLP",runtime.total_seconds(),search_problem.candidates_dequeued))

    print("Conflicts " + str(len(search_problem.known_conflicts)))
    print("Candidates " + str(search_problem.candidates_dequeued))

    solution = search_problem.next_solution()

print("==========================================")
print("Solution not found")
#  print(example_file)
print(None)
search_problem.pretty_print()
