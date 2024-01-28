# Origin problem: {"question": "Randy has 60 mango trees on his farm. He also has 5 less than half as many coconut trees as mango trees. How many trees does Randy have in all on his farm?", "answer": "Half of the number of Randy's mango trees is 60/2 = <<60/2=30>>30 trees.\nSo Randy has 30 - 5 = <<30-5=25>>25 coconut trees.\nTherefore, Randy has 60 + 25 = <<60+25=85>>85 treeson his farm.\n#### 85"}


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

    # Get initial amount and subsequent adjustment that ensure an integer result
    initial_amount, adjustment = get_params_combination()
    
    # Construct problem statement
    problem_statement = f"{name} has {initial_amount} {item1} at {place} in {county}. "
    problem_statement += f"They also have {adjustment} less than half as many {item2} as {item1}. "
    problem_statement += "How many items does " + name + " have in all?"

    # Generate solution code
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    half_item1 = f"half_{item1_var}"
    total_items = f"total_{item1_var}_and_{item2_var}"

    solution_code = f"""# Number of {item1} owned by {name}
{item1_var} = {initial_amount}

# Calculating half the number of {item1}
{half_item1} = {item1_var} // 2

# Number of {item2} based on {item1}
{item2_var} = {half_item1} - {adjustment}

# Calculating total items
{total_items} = {item1_var} + {item2_var}

result = {total_items}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} has {initial_amount} {item1} at {place} in {county}. "
    solution_wocode += f"They also have {adjustment} less than half as many {item2} as {item1}, which is {int(initial_amount / 2)} - {adjustment} = {int(initial_amount/2 - adjustment)} {item2}. "
    solution_wocode += f"Therefore, {name} has {initial_amount} + {int(initial_amount/2 - adjustment)} = {int(result)} items in total."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial amount. It must be an even number to ensure half of it is an integer.
        initial_amount = random.randint(5, 500) * 2  # Multiply by 2 to ensure it's even

        # Randomly generate adjustment
        adjustment = random.randint(1, 10)

        # Half of the initial amount
        half_initial_amount = initial_amount // 2

        # Ensure the final calculation (half_initial_amount - adjustment) results in a non-negative integer
        if half_initial_amount - adjustment >= 0:
            return initial_amount, adjustment



parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0012-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
