# Origin problem: {"problem": "The sum of two numbers is $45$. Their difference is $3$. What is the lesser of the two numbers?", "solution": "Let $x,y$ be the larger and smaller numbers, respectively. We have $x+y=45$ and $x-y=3$. Thus: $y=\\frac{1}{2}((x+y)-(x-y))=\\frac{1}{2}(45-3)=\\boxed{21}$.", "idx": 52}


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

    # Get values for variables in the expression
    total_amount, difference = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"At {place} in {county}, {name} has a collection of {item1}s and {item2}s. "
    problem_statement += f"The total number of items is {total_amount}, and the difference between the number of {item1}s and {item2}s is {difference}. "
    problem_statement += "What is the number of " + item2 + "s?"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Total number of items
total_items = {total_amount}

# Difference between {item1}s and {item2}s
difference_items = {difference}

# Let item1_var be the number of {item1}s and item2_var be the number of {item2}s
# We have item1_var + item2_var = total_items and item1_var - item2_var = difference_items

# Solving for item2_var
item2_var = (total_items - difference_items) / 2

result =  item2_var
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    item2_count = int(round(exec_globals['result'], 0))

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"The total number of items is {total_amount}, and the difference between the number of {item1}s and {item2}s is {difference}. "
    solution_wocode += f"So, the number of {item2}s is (total - difference) / 2 = ({total_amount} - {difference}) / 2 = {int(round(item2_count, 0))}."

    return problem_statement, solution_code, round(item2_count, 2), solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate total amount and difference
        total_amount = random.randint(2, 200) # Ensure it's even for integer division
        difference = random.randint(1, total_amount - 1) # Ensure difference is smaller than total

        # Check if the total and difference result in integer values for each item
        if (total_amount - difference) % 2 == 0:
            return total_amount, difference


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/math-0052-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
