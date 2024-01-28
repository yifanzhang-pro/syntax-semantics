# Origin problem: {"question": "Albert is wondering how much pizza he can eat in one day. He buys 2 large pizzas and 2 small pizzas. A large pizza has 16 slices and a small pizza has 8 slices. If he eats it all, how many pieces does he eat that day?", "answer": "He eats 32 from the largest pizzas because 2 x 16 = <<2*16=32>>32\nHe eats 16 from the small pizza because 2 x 8 = <<2*8=16>>16\nHe eats 48 pieces because 32 + 16 = <<32+16=48>>48\n#### 48"}


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


# Function to generate a problem and its solution
def generate_problem_and_solution_code():
    # Randomly select terms from predefined lists
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item1, item2 = random.sample(items, 2)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial quantities and their ratios
    quantity1, quantity2 = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} is organizing a gathering at {place} in {county}. "
    problem_statement += f"They buy {quantity1} packets of {item1} and {quantity2} boxes of {item2}. "
    problem_statement += f"Each packet of {item1} contains 10 pieces and each box of {item2} contains 5 pieces. "
    problem_statement += f"How many pieces in total does {name} have for the gathering?"

    # Generate solution code with specific variable names and comments
    item1_var = f"packets_of_{item1.replace(' ', '_')}"
    item2_var = f"boxes_of_{item2.replace(' ', '_')}"
    total_var = f"total_pieces"

    solution_code = f"""# Number of pieces in {item1_var}
{item1_var} = {quantity1} * 10  # 10 pieces per packet

# Number of pieces in {item2_var}
{item2_var} = {quantity2} * 5  # 5 pieces per box

# Calculating the total number of pieces
{total_var} = {item1_var} + {item2_var}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} has {quantity1 * 10} pieces from {quantity1} packets of {item1} and "
    solution_wocode += f"{quantity2 * 5} pieces from {quantity2} boxes of {item2}. "
    solution_wocode += f"In total, {name} has {quantity1 * 10} + {quantity2 * 5} = {round(result, 2)} pieces for the gathering."

    return problem_statement, solution_code, result, solution_wocode

# Function to get integer parameters for quantities
def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Randomly generate quantities
    quantity1 = random.randint(1, 100)
    quantity2 = random.randint(1, 100)

    return quantity1, quantity2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0006-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
