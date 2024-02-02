# Origin problem: {"question": "Ann's favorite store was having a summer clearance. For $75 she bought 5 pairs of shorts for $7 each and 2 pairs of shoes for $10 each. She also bought 4 tops, all at the same price. How much did each top cost?", "answer": "She bought 5 shorts at $7 each so 5*7=$<<5*7=35>>35\nShe bought 2 pair of shoes at $10 each so 2*10=$<<2*10=20>>20\nThe shorts and shoes cost her 35+20 = $<<35+20=55>>55\nWe know she spent 75 total and the shorts and shoes cost $55 which left a difference of 75-55 = $<<75-55=20>>20\nShe bought 4 tops for a total of $20 so 20/4 = $5\n#### 5"}


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
    item3 = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    item3_var = item3.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get the quantities and prices of items, and total amount
    quantity1, price1, quantity2, price2, quantity3, total_amount = get_params_combination()

    # Problem statement
    problem_statement = f"{name} went shopping at {place} in {county}. They spent a total of ${total_amount} buying "
    problem_statement += f"{quantity1} {item1} at ${price1} each and {quantity2} {item2} at ${price2} each. "
    problem_statement += f"They also bought some {item3}, all at the same price. How much did each {item3} cost?"

    # Solution code
    solution_code = f"""# Calculating the total cost of {quantity1} {item1}
{item1_var}_cost = {quantity1} * {price1}

# Calculating the total cost of {quantity2} {item2}
{item2_var}_cost = {quantity2} * {price2}

# Summing up the costs
total_cost = {item1_var}_cost + {item2_var}_cost

# Finding the remaining amount
remaining_amount = {total_amount} - total_cost

# Calculating the cost of each {item3}
{item3_var}_cost_per_item = remaining_amount / {quantity3}

result = {item3_var}_cost_per_item
"""

    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 0))

    # Generate solution without code
    solution_wocode = f"{name} bought {quantity1} {item1} at ${price1} each for a total of ${quantity1*price1}. "
    solution_wocode += f"They bought {quantity2} {item2} at ${price2} each for a total of ${quantity2*price2}. "
    solution_wocode += f"The {item1} and {item2} cost them ${quantity1*price1 + quantity2*price2}. "
    solution_wocode += f"With a total spending of ${total_amount}, the remaining amount is ${total_amount - (quantity1*price1 + quantity2*price2)}. "
    solution_wocode += f"They bought {quantity3} {item3} for a total of ${total_amount - (quantity1*price1 + quantity2*price2)}, so each {item3} cost ${int(round((total_amount - (quantity1*price1 + quantity2*price2)) / quantity3, 0))}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate quantities and prices
        quantity1 = random.randint(1, 10)
        price1 = random.randint(1, 20)
        quantity2 = random.randint(1, 10)
        price2 = random.randint(1, 20)
        quantity3 = random.randint(2, 10)  # Fixed quantity for item3, similar to the original problem

        # Ensure the total amount is a multiple of quantity3 and greater than the sum of costs
        total_amount = random.randint(1, 100) * quantity3
        if total_amount > (quantity1 * price1 + quantity2 * price2) and ((total_amount - (quantity1 * price1 + quantity2 * price2)) % quantity3 == 0):
            return quantity1, price1, quantity2, price2, quantity3, total_amount


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0023-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0023-1", "idx": i}) + '\n')
