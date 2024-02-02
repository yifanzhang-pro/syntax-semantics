# Origin problem: {"question": "There are 5 houses on a street, and each of the first four houses has 3 gnomes in the garden. If there are a total of 20 gnomes on the street, how many gnomes does the fifth house have?", "answer": "In the first four houses, there are a total of 4 houses * 3 gnomes = <<4*3=12>>12 gnomes.\nTherefore, the fifth house had 20 total gnomes \u2013 12 gnomes = <<20-12=8>>8 gnomes.\n#### 8"}


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

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get initial number of units and quantity per unit
    num_units, quantity_per_unit, total_quantity = get_params_combination()

    # Construct problem statement
    problem_statement = f"There are {num_units} {item} at {place} in {county}, and each of the first {num_units - 1} {item} has {quantity_per_unit} {name_var}s. "
    problem_statement += f"If there are a total of {total_quantity} {name_var}s, how many {name_var}s does the last {item} have?"

    # Generate solution code
    total_for_first_units_var = f"total_for_first_{num_units - 1}_{item_var}s"
    remaining_var = f"remaining_{name_var}s_for_last_{item_var}"

    solution_code = f"""# Total {name_var}s for the first {num_units - 1} {item_var}s
{total_for_first_units_var} = ({num_units - 1}) * {quantity_per_unit}

# Calculating the {name_var}s for the last {item_var}
{remaining_var} = {total_quantity} - {total_for_first_units_var}

result = {remaining_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"In the first {num_units - 1} {item_var}s, there are a total of ({num_units - 1}) * {quantity_per_unit} = {num_units - 1} * {quantity_per_unit} = {exec_globals[total_for_first_units_var]} {name_var}s. "
    solution_wocode += f"Therefore, the last {item_var} had {total_quantity} total {name_var}s - {exec_globals[total_for_first_units_var]} {name_var}s = {result} {name_var}s."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate the number of units (at least 2)
        num_units = random.randint(2, 10)

        # Randomly generate quantity per unit
        quantity_per_unit = random.randint(1, 10)

        # Ensure the total quantity is an integer and greater than the total for first units
        total_quantity = random.randint(num_units * quantity_per_unit, num_units * quantity_per_unit + 100)

        # Check if total_quantity is greater than total for first units
        if total_quantity > (num_units - 1) * quantity_per_unit:
            return num_units, quantity_per_unit, total_quantity


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0028-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0028-1", "idx": i}) + '\n')
