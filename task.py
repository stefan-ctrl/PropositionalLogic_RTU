#You have the following conditions that can influence your decision:
import sys
from itertools import product
from mimetypes import knownfiles

from pyparsing import conditionAsParseAction

from logic import *

# Task 1 - Represent the conditions
raining = Symbol("Raining")
heavy_traffic = Symbol("HeavyTraffic")
early_meeting = Symbol("EarlyMeeting")
strike = Symbol("Strike")

# Task 2 - Define the Commuting Options
wfh = Symbol("WFH")
drive = Symbol("Drive")
public_transport = Symbol("PublicTransport")

# Task 3 - Create the Knowledge Base
knowledge_base = And(
    Biconditional(Or(raining, early_meeting), wfh),
    Biconditional(And(Not(raining), Not(heavy_traffic)), drive),
    Biconditional(And(Not(strike), Not(raining)), public_transport)
)

# Task 4 - Define Queries
should_wfh = Implication(knowledge_base, wfh)
should_drive = Implication(knowledge_base, drive)
should_public_transport = Implication(knowledge_base, public_transport)


# Task 5 - Perform Model Checking
#print('It is raining. Should I work from home? ', model_check(And(raining, knowledge_base), should_wfh))
#print('It is raining. Should I drive? ', model_check(And(raining, knowledge_base), should_drive))
#print('It is raining. Should I take public transport? ', model_check(And(raining, knowledge_base), should_public_transport))

#print('There is heavy traffic. Should I work from home? ', model_check(And(heavy_traffic, knowledge_base), should_wfh))
#print('There is heavy traffic. Should I drive? ', model_check(And(heavy_traffic, knowledge_base), should_drive))
#print('There is heavy traffic. Should I take public transport? ', model_check(And(heavy_traffic, knowledge_base), should_public_transport))

#print('I have an early meeting. Should I work from home? ', model_check(And(early_meeting, knowledge_base), should_wfh))
#print('I have an early meeting. Should I drive? ', model_check(And(early_meeting, knowledge_base), should_drive))
#print('I have an early meeting. Should I take public transport? ', model_check(And(early_meeting, knowledge_base), should_public_transport))

#print('There is a strike. Should I work from home? ', model_check(And(strike, knowledge_base), should_wfh))
#print('There is a strike. Should I drive? ', model_check(And(strike, knowledge_base), should_drive))
#print('There is a strike. Should I take public transport? ', model_check(And(strike, knowledge_base), should_public_transport))

# Task 6 - Answer the Queries

##Scenario 1: It’s raining, and there’s heavy traffic.
print('Scenario 1: It’s raining, and there’s heavy traffic. Work from home? ',
      model_check(And(raining, heavy_traffic, knowledge_base), should_wfh))
print('Scenario 1: It’s raining, and there’s heavy traffic. Drive? ',
      model_check(And(raining, heavy_traffic, knowledge_base), should_drive))
print('Scenario 2: It’s not raining, and there’s a strike. Should I take public transport? ',
      model_check(And(Not(raining), strike, knowledge_base), should_public_transport))
print('Scenario 3: There’s no rain, traffic is light, and there’s no strike. Drive? ',
        model_check(And(Not(raining), Not(heavy_traffic), Not(strike), knowledge_base), should_drive))
print('Scenario 3: There’s no rain, traffic is light, and there’s no strike. Take public transport? ',
        model_check(And(Not(raining), Not(heavy_traffic), Not(strike), knowledge_base), should_public_transport))

# Task 7 - Add more Rules
afternoon_appointment = Symbol("AfternoonAppointment")
road_construction = Symbol("RoadConstruction")
knownledge_base = Or(
    Implication(afternoon_appointment, drive),
    Implication(road_construction, Not(drive)),
    Implication(Or(raining, early_meeting), wfh),
    Implication(And(Not(raining), Not(heavy_traffic)), drive),
    Implication(And(Not(strike), Not(raining)), public_transport))

condition_symbols = [raining, heavy_traffic, early_meeting, strike, afternoon_appointment, road_construction]
opposite_conditions = [Not(raining), Not(heavy_traffic), Not(early_meeting), Not(strike), Not(afternoon_appointment), Not(road_construction)]


# write the output also to a file
output_file = open("task_7.md", "w")
sys.stdout = output_file
print(f"| {condition_symbols[0].name} | {condition_symbols[1].name} | {condition_symbols[2].name} | {condition_symbols[3].name} | {condition_symbols[4].name} | {condition_symbols[5].name} | Should I WFH? | Should I Drive? | Should I take Public Transport? |")
print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")

for i in range(2**6):
    # choose raining from first and the remaining from the second array
    # iterate through all the possible combinations so that always 6 elements are chosen but never with the same index from the two arrays

    conditions_list = [condition_symbols[j] if i & (1 << j) else opposite_conditions[j] for j in range(6)]
    conditions = And(conditions_list[0], conditions_list[1], conditions_list[2], conditions_list[3], conditions_list[4], conditions_list[5])


    # print 1 if True else 0. first all conditions from conditions_list and then the results of the model_check
    # check if conditions_list is type 'not' print 0 else print 1
    print(f"| {int(conditions_list[0] == condition_symbols[0])} | {int(conditions_list[1] == condition_symbols[1])} | {int(conditions_list[2] == condition_symbols[2])} | {int(conditions_list[3] == condition_symbols[3])} | {int(conditions_list[4] == condition_symbols[4])} | {int(conditions_list[5] == condition_symbols[5])} | {int(model_check(conditions, should_wfh))} | {int(model_check(conditions, should_drive))} | {int(model_check(conditions, should_public_transport))} |")

