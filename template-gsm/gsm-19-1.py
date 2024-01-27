# Origin problem: {"question": "Claire makes a 3 egg omelet every morning for breakfast.  How many dozens of eggs will she eat in 4 weeks?", "answer": "She eats 3 eggs every day and there are 7 days in a week so she eats 3*7 = <<3*7=21>>21 eggs a week\nAfter 4 weeks she will have eaten 4*21 = <<4*21=84>>84 eggs\nThere are 12 eggs in 1 dozen and she'll eat 84 eggs so that's 84/12 = <<84/12=7>>7 dozen eggs\n#### 7"}


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


import random

def generate_problem_and_solution_code():
    # Randomly select terms from predefined lists
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get the parameters for the problem
    per_time_unit, time_units, conversion_unit = get_params_combination()

    # Construct the problem statement
    problem_statement = f"{name} uses {per_time_unit} {item} every day at {place} in {county}. "
    problem_statement += f"How many {conversion_unit}s of {item} will {name} use in {time_units} weeks?"

    # Variables for solution code
    daily_use_var = f"daily_{item.replace(' ', '_')}_use"
    total_use_var = f"total_{item.replace(' ', '_')}_use"
    conversion_var = f"{item.replace(' ', '_')}_per_{conversion_unit}"

    # Solution code
    solution_code = f"""# Number of {item} used by {name} daily
{daily_use_var} = {per_time_unit}

# Total number of weeks
weeks = {time_units}

# Total {item} used in {time_units} weeks (7 days in a week)
{total_use_var} = {daily_use_var} * 7 * weeks

# Number of {item} per {conversion_unit}
{conversion_var} = 12  # assuming 12 {item} per {conversion_unit}

# Calculating the total {conversion_unit}s used
total_{conversion_var}s = {total_use_var} // {conversion_var}

result = total_{conversion_var}s
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} uses {per_time_unit} {item} every day. "
    solution_wocode += f"In {time_units} weeks, {name} will use {per_time_unit}*7*{time_units} = {per_time_unit * 7 * time_units} {item}. "
    solution_wocode += f"There are 12 {item} in 1 {conversion_unit}, so that's {round(per_time_unit * 7 * time_units / 12, 2)} {conversion_unit}s."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Prefer integer parameters and ensure numbers have a finite number of digits.
    """
    # Randomly generate the per-time-unit consumption and time units
    per_time_unit = random.randint(1, 10)  # Number of items used per time unit
    time_units = random.randint(1, 52)  # Number of weeks
    conversion_unit = "dozen"  # Unit for conversion (e.g., dozen)

    return per_time_unit, time_units, conversion_unit


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-19-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
