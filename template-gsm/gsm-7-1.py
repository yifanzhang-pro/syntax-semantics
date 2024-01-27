# Origin problem: {"question": "Toulouse has twice as many sheep as Charleston. Charleston has 4 times as many sheep as Seattle. How many sheep do Toulouse, Charleston, and Seattle have together if Seattle has 20 sheep?", "answer": "If Seattle has 20 sheep, Charleston has 4 * 20 sheep = <<20*4=80>>80 sheep\nToulouse has twice as many sheep as Charleston, which is 2 * 80 sheep = <<2*80=160>>160 sheep\nTogether, the three has 20 sheep + 160 sheep + 80 sheep = <<20+160+80=260>>260 sheep\n#### 260"}


import random
import math
import json
import argparse
import jsonlines

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


def generate_problem_and_solution_code():
    # Lists of random terms
    locations = ["first", "second", "third"]

    # Get initial amount and subsequent multipliers that ensure integer results
    initial_amount, multiplier_1, multiplier_2 = get_params_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place_1 = random.choice(places)
    place_2 = random.choice(places)
    place_3 = random.choice(places)
    county_1 = random.choice(us_counties)
    county_2 = random.choice(us_counties)
    county_3 = random.choice(us_counties)
    county_1 = county_1['CountyName'] + ", " + county_1["StateName"]
    county_2 = county_2['CountyName'] + ", " + county_2["StateName"]
    county_3 = county_3['CountyName'] + ", " + county_3["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} distributed {initial_amount} {item} to a place in {county_1}. "
    problem_statement += f"The {locations[1]} place, located in {county_2}, received {multiplier_1} times as many {item} as the {locations[0]} place. "
    problem_statement += f"The {locations[2]} place, in {county_3}, received {multiplier_2} times as many {item} as the {locations[1]} place. "
    problem_statement += f"How many {item} did {name} distribute in total to these three places?"

    # Generate solution code with specific variable names and comments
    initial_var = f"{item.replace(' ', '_')}_at_{locations[0]}"
    multiplier_var1 = f"multiplier_{locations[1]}"
    multiplier_var2 = f"multiplier_{locations[2]}"
    total_var = f"total_{item.replace(' ', '_')}"

    solution_code = f"""# Number of {item} distributed by {name} to the {locations[0]} place
{initial_var} = {initial_amount}

# Multipliers for the subsequent places
{multiplier_var1} = {multiplier_1}
{multiplier_var2} = {multiplier_2}

# Calculating the amount of {item} distributed to the {locations[1]} and {locations[2]} places
distributed_{locations[1]} = {initial_var} * {multiplier_var1}
distributed_{locations[2]} = distributed_{locations[1]} * {multiplier_var2}

# Calculating the total number of {item} distributed
{total_var} = {initial_var} + distributed_{locations[1]} + distributed_{locations[2]}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} distributed {initial_amount} {item} to the {locations[0]} place. "
    solution_wocode += f"The {locations[1]} place, in {county_2}, received {initial_amount * multiplier_1} {item} ({multiplier_1} times {initial_amount}). "
    solution_wocode += f"The {locations[2]} place, in {county_3}, received {initial_amount * multiplier_1 * multiplier_2} {item}. "
    solution_wocode += f"In total, {name} distributed {result} {item} to these three places."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    while True:
        # Randomly generate initial amount
        initial_amount = random.randint(10, 1000)

        # Randomly generate multipliers
        multiplier_1 = random.randint(2, 5)
        multiplier_2 = random.randint(2, 5)

        return initial_amount, multiplier_1, multiplier_2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-7-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
