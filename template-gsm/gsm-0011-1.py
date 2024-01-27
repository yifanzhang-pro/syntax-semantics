# Origin problem: {"question": "Toula went to the bakery and bought various types of pastries. She bought 3 dozen donuts which cost $68 per dozen, 2 dozen mini cupcakes which cost $80 per dozen, and 6 dozen mini cheesecakes for $55 per dozen. How much was the total cost?", "answer": "The total charge for the doughnuts was 3 x $68 = $<<3*68=204>>204.\nThe total charge for the mini cupcakes was 2 x $80 = $<<2*80=160>>160.\nThe total charge for the mini cheesecakes was 6 x $55 = $<<6*55=330>>330.\nTherefore the total amount Toula paid for the pastries was $204 + $160 + $330 = $<<204+160+330=694>>694.\n#### 694"}


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
    # Lists of random terms
    items_types = random.sample(items, 3)  # Select 3 random items

    # Get quantities and prices for each item
    quantities, prices = get_params_combination(len(items_types))
    
    # Randomly select other terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} went to {place} and bought various types of items. "
    for i, item in enumerate(items_types):
        problem_statement += f"They bought {quantities[i]} dozen {item} which cost ${prices[i]} per dozen, "

    problem_statement = problem_statement.rstrip(", ") + ". "
    problem_statement += "How much was the total cost?"

    # Generate solution code
    total_cost_var = "total_cost"
    solution_code = f"{total_cost_var} = 0\n"

    for i, item in enumerate(items_types):
        cost_var = f"{item.replace(' ', '_')}_cost"
        solution_code += f"# Calculating the cost for {item}\n"
        solution_code += f"{cost_var} = {quantities[i]} * {prices[i]}\n"
        solution_code += f"{total_cost_var} += {cost_var}\n"

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    total_cost = round(exec_globals[total_cost_var], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = ""
    for i, item in enumerate(items_types):
        solution_wocode += f"The total charge for the {item} was {quantities[i]} x ${prices[i]} = ${round(quantities[i] * prices[i], 2)}.\n"

    solution_wocode += f"Therefore, the total amount {name} paid for the items was "
    solution_wocode += " + ".join([f"${round(quantities[i] * prices[i], 2)}" for i in range(len(items_types))])
    solution_wocode += f" = ${total_cost}.\n"

    return problem_statement, solution_code, total_cost, solution_wocode


def get_params_combination(num_items):
    # Randomly generate quantities and prices for each item
    quantities = [random.randint(1, 10) for _ in range(num_items)]
    prices = [round(random.uniform(10, 100), 2) for _ in range(num_items)]

    return quantities, prices


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0011-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
