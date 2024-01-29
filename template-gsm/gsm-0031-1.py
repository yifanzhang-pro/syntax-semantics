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
    item1, item2 = random.sample(items, 2)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    month_pairs = [("January", "February"), ("March", "April"), ("May", "June"), ("July", "August"), 
                   ("September", "October"), ("November", "December")]

    # Get unit prices and quantities that ensure integer results
    unit_price1, unit_price2, quantity1, quantity2, scale_factor = get_params_combination()

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    county_var = county.replace(' ', '_')
    month1, month2 = random.choice(month_pairs)

    # Construct problem statement
    problem_statement = f"{name} sells {item1} and {item2} at {place} in {county}. "
    problem_statement += f"They charge ${unit_price1} for each {item1} and ${unit_price2} for each {item2}. "
    problem_statement += f"Last {month1}, they sold {quantity1} {item1} and {quantity2} {item2}. "
    problem_statement += f"If they sold {scale_factor} times as much this {month2}, how much are their sales for this {month2}?"

    # Generate solution code
    solution_code = f"""# Sales calculations
unit_price1 = {unit_price1}
unit_price2 = {unit_price2}
quantity1 = {quantity1}
quantity2 = {quantity2}
scale_factor = {scale_factor}

# Total sales for each item last {month1}
total_sales_{item1_var} = unit_price1 * quantity1
total_sales_{item2_var} = unit_price2 * quantity2

# Total sales for last {month1}
total_sales_last_month = total_sales_{item1_var} + total_sales_{item2_var}

# Sales for this {month2}
total_sales_this_month = total_sales_last_month * scale_factor

result = total_sales_this_month
"""

    # Execute the solution code to get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate solution without code
    solution_wocode = f"{name} charged ${unit_price1} for each {item1} and ${unit_price2} for each {item2}. "
    solution_wocode += f"Last {month1}, they earned ${unit_price1*quantity1} from {item1} and ${unit_price2*quantity2} from {item2}, totaling ${unit_price1*quantity1 + unit_price2*quantity2}. "
    solution_wocode += f"This {month2}, their sales are {scale_factor} times last month, which is ${round(unit_price1*quantity1 + unit_price2*quantity2, 2)} x {scale_factor} = ${round(result, 2)}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        unit_price1 = random.randint(10, 1000)
        unit_price2 = random.randint(10, 1000)
        quantity1 = random.randint(1, 100)
        quantity2 = random.randint(1, 100)
        scale_factor = random.randint(2, 10)

        # Ensure the total sales values are integers
        total_sales1 = unit_price1 * quantity1
        total_sales2 = unit_price2 * quantity2
        total_sales_scaled = (total_sales1 + total_sales2) * scale_factor

        if total_sales_scaled == int(total_sales_scaled):
            return unit_price1, unit_price2, quantity1, quantity2, scale_factor


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0031-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
