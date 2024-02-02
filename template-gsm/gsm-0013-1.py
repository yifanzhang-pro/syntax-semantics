# Origin problem: {"question": "Jasper will serve charcuterie at his dinner party. He buys 2 pounds of cheddar cheese for $10, a pound of cream cheese that cost half the price of the cheddar cheese, and a pack of cold cuts that cost twice the price of the cheddar cheese. How much does he spend on the ingredients?", "answer": "A pound of cream cheese cost $10 / 2 = $<<10/2=5>>5.\nA pack of cold cuts cost $10 x 2 = $<<10*2=20>>20.\nJasper spent $10 + $5 + $20 = $<<10+5+20=35>>35 on the ingredients.\n#### 35"}


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
    # Randomly select names, items, and locations
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item1 = random.choice(items)
    item2 = random.choice(items)
    item3 = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'].replace(' ', '_') + ", " + county["StateName"].replace(' ', '_')

    # Get initial cost and proportion factors ensuring integer results
    initial_cost, half_price_factor, double_price_factor = get_params_combination()

    # Construct problem statement
    problem_statement = f"{name} is preparing for a party at {place} in {county}. "
    problem_statement += f"They buy a {item1} for ${initial_cost}, a {item2} for half the price of the {item1}, "
    problem_statement += f"and a {item3} for double the price of the {item1}. "
    problem_statement += f"How much does {name} spend in total?"

    # Construct solution code
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    item3_var = item3.replace(' ', '_')

    solution_code = f"""# Cost of the {item1}
{item1_var}_cost = {initial_cost}

# Cost of the {item2} (half the price of {item1})
{item2_var}_cost = {item1_var}_cost * {half_price_factor}

# Cost of the {item3} (double the price of {item1})
{item3_var}_cost = {item1_var}_cost * {double_price_factor}

# Total cost
total_cost = {item1_var}_cost + {item2_var}_cost + {item3_var}_cost
result = total_cost
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(exec_globals['result'])

    # Generate solution without code
    solution_wocode = f"{name} buys a {item1} for ${initial_cost}, a {item2} for ${int(initial_cost * half_price_factor)}, "
    solution_wocode += f"and a {item3} for ${int(initial_cost * double_price_factor)}. "
    solution_wocode += f"In total, {name} spends ${result}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    # Ensure integer values for initial cost and proportion factors
    initial_cost = random.randint(1, 1000) * 2
    half_price_factor = 0.5
    double_price_factor = 2
    return initial_cost, half_price_factor, double_price_factor


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0013-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0013-1", "idx": i}) + '\n')
