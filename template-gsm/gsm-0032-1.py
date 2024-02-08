# Origin problem: {"question": "A car is driving through a tunnel with many turns. After a while, the car must travel through a ring that requires a total of 4 right-hand turns. After the 1st turn, it travels 5 meters. After the 2nd turn, it travels 8 meters. After the 3rd turn, it travels a little further and at the 4th turn, it immediately exits the tunnel. If the car has driven a total of 23 meters around the ring, how far did it have to travel after the 3rd turn?", "answer": "From the details given, the car has traveled 5 meters at the 1st turn + 8 meters after the 2nd turn + 0 meters after the 4th turn = <<5+8+0=13>>13 meters around the ring.\nIt must therefore have driven 23 total meters \u2013 13 calculated meters = 10 meters after the 3rd turn.\n#### 10"}


import random
import math
import json
import argparse
import jsonlines
import os

random.seed(42) # Consistent random generation

first_names = []
with jsonlines.open('../data/top_first_names.jsonl') as reader:
    for line in reader:
        first_names.append(line['first_name'])

last_names = []
with jsonlines.open('../data/top_last_names.jsonl') as reader:
    for line in reader:
        last_names.append(line['last_name'])

items = []
with jsonlines.open('../data/items-llm.jsonl') as reader:
    for line in reader:
        items.append(line)

places = []
with jsonlines.open('../data/places-llm.jsonl') as reader:
    for line in reader:
        places.append(line)

us_counties = []
with jsonlines.open('../data/us_counties.jsonl') as reader:
    for line in reader:
        us_counties.append(line)




parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems


def generate_problem_and_solution_code():
    # Selecting a character, item, and context from predefined lists
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county_formatted = county['CountyName'] + ", " + county["StateName"]

    # Variable names adjusted for code (replace spaces with underscores)
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county_formatted.replace(' ', '_')

    # Generating parameters for the sequence of actions
    initial_actions, total_units = get_params_combination()

    # Problem statement
    problem_statement = f"{name} started collecting {item} in {place} in {county_formatted}. Initially, they got {initial_actions[0]} units, then added {initial_actions[1]} more units. If the total collection reached {total_units} units, how many units did {name} collect in the last action?"

    # Calculating units collected in the last action
    last_action_units = total_units - sum(initial_actions)

    # Solution code
    solution_code = f"""# Initial units collected
initial_units = sum({initial_actions})

# Total units collected
total_units = {total_units}

# Units collected in the last action
last_action_units = total_units - initial_units

result = last_action_units
"""

    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Solution without code
    solution_wocode = f"To reach a total of {total_units} units, after initially collecting {initial_actions[0]} and then {initial_actions[1]} units, {name} must have collected {result} units in the last action."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Generates initial actions and a total that ensures the problem makes sense.
    """
    initial_actions = [random.randint(1, 20), random.randint(1, 20)]
    # Ensure the total is greater than the sum of initial actions for a sensible outcome
    total_units = sum(initial_actions) + random.randint(1, 20)

    return initial_actions, total_units
      

if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0032-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0032-1", "idx": i}) + '\n')
