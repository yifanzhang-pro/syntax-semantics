# Origin problem: 

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

    # Get initial quantity and subsequent quantity with their respective ratios
    initial_quantity, initial_ratio, subsequent_quantity, subsequent_ratio = get_params_combination()

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')
    place_var = place.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"{name} started a project at {place} in {county} and collected {initial_quantity} {item}. "
    problem_statement += f"However, they found that {initial_ratio*100:.0f}% of them were unsuitable and discarded them. "
    problem_statement += f"Later, {name} added {subsequent_quantity} more {item} but discovered that {subsequent_ratio*100:.0f}% of these were also unsuitable. "
    problem_statement += f"How many {item} were suitable for {name}'s project after discarding the unsuitable ones?"

    # Variables for calculations
    initial_discarded_var = f"initial_discarded_{item_var}"
    subsequent_discarded_var = f"subsequent_discarded_{item_var}"
    total_suitable_var = f"total_suitable_{item_var}"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Initial quantity of {item}
initial_{item_var} = {initial_quantity}

# Ratio of unsuitable {item} in the initial collection
initial_ratio_{item_var} = {initial_ratio}

# Calculating the number of unsuitable {item} in the initial collection
{initial_discarded_var} = initial_{item_var} * initial_ratio_{item_var}
initial_suitable_{item_var} = initial_{item_var} - {initial_discarded_var}

# Subsequent quantity of {item} added
subsequent_{item_var} = {subsequent_quantity}

# Ratio of unsuitable {item} in the subsequent collection
subsequent_ratio_{item_var} = {subsequent_ratio}

# Calculating the number of unsuitable {item} in the subsequent collection
{subsequent_discarded_var} = subsequent_{item_var} * subsequent_ratio_{item_var}
subsequent_suitable_{item_var} = subsequent_{item_var} - {subsequent_discarded_var}

# Total suitable {item}
{total_suitable_var} = initial_suitable_{item_var} + subsequent_suitable_{item_var}

result = {total_suitable_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(exec_globals['result'])

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} collected {initial_quantity} {item}, but {initial_ratio*100:.0f}% of them were unsuitable, leaving {initial_quantity - round(initial_ratio * initial_quantity)} suitable {item}. "
    solution_wocode += f"After adding {subsequent_quantity} more {item}, {subsequent_ratio*100:.0f}% of these were unsuitable, leaving {subsequent_quantity - round(subsequent_ratio * subsequent_quantity)} suitable {item}. "
    solution_wocode += f"In total, {name} had {initial_quantity - round(initial_ratio * initial_quantity)} + {subsequent_quantity - round(subsequent_ratio * subsequent_quantity)} = {round(result, 2)} suitable {item} for the project."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        initial_quantity = random.randint(50, 1000)
        initial_ratio = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        subsequent_quantity = random.randint(50, 1000)
        subsequent_ratio = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

        # Ensure that the results are integers
        if (initial_quantity * initial_ratio).is_integer() and (subsequent_quantity * subsequent_ratio).is_integer():
            return initial_quantity, initial_ratio, subsequent_quantity, subsequent_ratio


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0027-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
