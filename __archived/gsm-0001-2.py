# Origin problem: {"question": "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?", 
#  "answer": "Weng earns 12/60 = $<<12/60=0.2>>0.2 per minute.\nWorking 50 minutes, she earned 0.2 x 50 = $<<0.2*50=10>>10.\n#### 10"}


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


def generate_problem_and_solution_code():
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code (replacing spaces with underscores)
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get the unit rate and the duration for the activity
    unit_rate, duration = get_params_combination()

    # Construct the problem statement
    problem_statement = f"{name} earns ${unit_rate} per hour for {item}. Yesterday, they did {duration} minutes of {item} at {place} in {county}. How much did {name} earn?"

    # Generate solution code
    per_minute_rate_var = f"{item_var}_per_minute_rate"
    total_earnings_var = f"total_{item_var}_earnings"

    solution_code = f"""# Calculating the per-minute rate
{per_minute_rate_var} = {unit_rate} / 60

# Calculating total earnings for {duration} minutes of work
{total_earnings_var} = {per_minute_rate_var} * {duration}

result = {total_earnings_var}
"""

    # Execute the solution code to get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} earns ${unit_rate} per hour for {item}. They earn ${unit_rate}/60 = $"
    solution_wocode += f"{round(unit_rate/60, 2)} per minute. Working {duration} minutes, they earned $"
    solution_wocode += f"{round(unit_rate/60, 2)} x {duration} = ${round(result, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Randomly generate unit rate as an integer
    unit_rate = random.randint(10, 100)

    # Randomly generate duration ensuring the product is an integer
    duration = random.choice([15, 30, 45, 60, 75, 90, 105, 120])

    return unit_rate, duration


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0001-2--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
