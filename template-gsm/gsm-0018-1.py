# Origin problem: {"question": "It takes Roque two hours to walk to work and one hour to ride his bike to work. Roque walks to and from work three times a week and rides his bike to and from work twice a week. How many hours in total does he take to get to and from work a week with walking and biking?", "answer": "Roque takes 2*3 = <<2*3=6>>6 hours a week to walk to work.\nRoque takes 6*2 = <<6*2=12>>12 hours a week to walk to and from work.\nRoque takes 1*2 = <<1*2=2>>2 hours a week to bike to work.\nRoque takes 2*2 = <<2*2=4>>4 hours a week to bike to and from work.\nIn total, Roque takes 12+4 = <<12+4=16>>16 hour a week to go to and from work.\n#### 16"}


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
    item1 = random.choice(items)
    item2 = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get initial amounts and frequencies ensuring an integer result
    amount1, freq1, amount2, freq2 = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} spends {amount1} hours on {item1} and {amount2} hours on {item2} each time. "
    problem_statement += f"They do {item1} {freq1} times a week and {item2} {freq2} times a week in {place} in {county}. "
    problem_statement += f"How many hours in total does {name} spend on {item1} and {item2} a week?"

    # Generate solution code with specific variable names and comments
    total_item1 = f"total_hours_{item1_var}"
    total_item2 = f"total_hours_{item2_var}"

    solution_code = f"""# Total hours spent on {item1} by {name}
{total_item1} = {amount1} * {freq1}

# Total hours spent on {item2} by {name}
{total_item2} = {amount2} * {freq2}

# Calculating the total hours spent on both {item1} and {item2}
total_hours = {total_item1} + {total_item2}

result = total_hours
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} spends {amount1} hours on {item1} and {amount2} hours on {item2} each time. "
    solution_wocode += f"They do {item1} {freq1} times and {item2} {freq2} times a week in {place} in {county}. "
    solution_wocode += f"In total, {name} spends {round(amount1*freq1, 2)} hours on {item1} and {round(amount2*freq2, 2)} hours on {item2} a week. "
    solution_wocode += f"Thus, {name} spends {round(amount1*freq1, 2)} + {round(amount2*freq2, 2)} = {round(result, 2)} hours in total a week."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Randomly generate amounts and frequencies
    amount1 = random.randint(1, 10)
    freq1 = random.randint(1, 7)  # Assuming a maximum of 7 days a week
    amount2 = random.randint(1, 10)
    freq2 = random.randint(1, 7)

    return amount1, freq1, amount2, freq2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0018-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
