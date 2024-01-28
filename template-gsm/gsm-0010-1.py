# Origin problem: {"question": "A deep-sea monster rises from the waters once every hundred years to feast on a ship and sate its hunger. Over three hundred years, it has consumed 847 people. Ships have been built larger over time, so each new ship has twice as many people as the last ship. How many people were on the ship the monster ate in the first hundred years?", "answer": "Let S be the number of people on the first hundred years\u2019 ship.\nThe second hundred years\u2019 ship had twice as many as the first, so it had 2S people.\nThe third hundred years\u2019 ship had twice as many as the second, so it had 2 * 2S = <<2*2=4>>4S people.\nAll the ships had S + 2S + 4S = 7S = 847 people.\nThus, the ship that the monster ate in the first hundred years had S = 847 / 7 = <<847/7=121>>121 people on it.\n#### 121"}


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
    
    # Get initial quantity and total
    initial_quantity, total = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"Every year, {name} plants {item} in {place} at {county}. Over the last three years, {name} has planted a total of {total} {item}. "
    problem_statement += f"Each year, the number of {item} planted is double the previous year. "
    problem_statement += f"How many {item} did {name} plant in the first year?"

    # Replace spaces with underscores for variable names in code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')

    # Generate solution code
    solution_code = f"""# Initial number of {item_var} planted by {name_var} in the first year
initial_{item_var} = {initial_quantity}

# Total number of {item_var} planted over three years
# follows the pattern: initial + 2*initial + 4*initial = total
total_{item_var} = 7 * initial_{item_var}

# Asserting the total number to the known total
assert total_{item_var} == {total}

# Returning the initial number of {item_var}
result = initial_{item_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"Let T be the number of {item} {name} planted in the first year.\n"
    solution_wocode += f"In the second year, they planted 2T {item}, and in the third year, 4T {item}.\n"
    solution_wocode += f"All years together, they planted T + 2T + 4T = 7T = {total} {item}.\n"
    solution_wocode += f"Therefore, the number of {item} planted in the first year was T = {int(result)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate an initial quantity (ensuring it's an integer)
        initial_quantity = random.randint(1, 1000)

        # The total number of items over the period, given the doubling pattern
        total = initial_quantity * 7  # Sum of geometric series for three terms: 1 + 2 + 4 = 7

        # Return the parameters
        return initial_quantity, total


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0010-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
