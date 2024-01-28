# Origin problem: {"question": "Joy can read 8 pages of a book in 20 minutes. How many hours will it take her to read 120 pages?", "answer": "In one hour, there are 3 sets of 20 minutes.\nSo, Joy can read 8 x 3 = <<8*3=24>>24 pages in an hour.\nIt will take her 120/24 = <<120/24=5>>5 hours to read 120 pages.\n#### 5"}


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
    # Lists of random terms
    names = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county_name = county['CountyName'].replace(' ', '_') + ", " + county["StateName"].replace(' ', '_')

    # Get initial amount and subsequent ratio that ensure an integer result
    per_unit, total_amount = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{names} can paint {per_unit} {item} in a day at {place} in {county_name}. "
    problem_statement += f"How many days will it take them to paint {total_amount} {item}?"

    # Generate solution code with specific variable names and comments
    per_day_var = f"{item.replace(' ', '_')}_per_day"
    total_var = f"total_{item.replace(' ', '_')}"
    days_var = f"days_to_paint_{item.replace(' ', '_')}"

    solution_code = f"""# Number of {item} painted by {names} per day
{per_day_var} = {per_unit}

# Total number of {item} to be painted
{total_var} = {total_amount}

# Calculating the number of days required to paint all {item}
{days_var} = {total_var} / {per_day_var}

result = {days_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(exec_globals['result'])

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{names} can paint {per_unit} {item} in a day at {place} in {county_name}. "
    solution_wocode += f"It will take them {total_amount}/{per_unit} = {int(result)} days to paint {total_amount} {item}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate per unit amount
        per_unit = random.randint(1, 50)

        # Randomly generate total amount ensuring it's a multiple of per_unit
        total_amount = random.randint(1, 20) * per_unit

        return per_unit, total_amount


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0014-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
