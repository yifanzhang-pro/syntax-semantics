# Origin problem: {"problem": "What is the value of $(2x + 5)^2$ when $x = 3$?", "solution": "We have $(2x+5)^2 = (2\\cdot 3 + 5)^2 = 11^2 = \\boxed{121}$.", "idx": 69}


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
    # Randomly select terms, ensuring proper formatting for natural language and code
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Replace spaces with underscores for use in variable names
    item_code = item.replace(' ', '_')

    # Get values for variables in the expression
    var_value, linear_coefficient, constant_term = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"What is the total value of {item} that {name} has at {place} in {county}, "
    problem_statement += f"when the number of {item} is first increased by {linear_coefficient} and then the total is squared, given there are initially {var_value} {item}?"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Initial amount of {item_code}s
initial_{item_code} = {var_value}

# Total number of {item_code}s after linear transformation
total_{item_code} = initial_{item_code} + {linear_coefficient}

# Squaring the total number of {item_code}s
squared_{item_code} = total_{item_code} ** 2

result = squared_{item_code}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    total_items = var_value + linear_coefficient
    squared_total = total_items ** 2
    solution_wocode = f"After increasing the number of {item} by {linear_coefficient}, the total number becomes {var_value} + {linear_coefficient} = {total_items}. "
    solution_wocode += f"Squaring this total, we get {total_items}^2 = {squared_total}. Thus, the total squared value of {item} is {int(round(squared_total, 0))}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Randomly generate initial value, linear coefficient, and constant term
    var_value = random.randint(1, 10)
    linear_coefficient = random.randint(1, 10)
    constant_term = random.randint(1, 10)

    # Ensure the calculation results in an integer value
    return var_value, linear_coefficient, constant_term


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/math-0069-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
