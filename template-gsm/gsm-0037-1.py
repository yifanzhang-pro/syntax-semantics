# Origin problem: {"question": "Five friends eat at a fast-food chain and order the following: 5 pieces of hamburger that cost $3 each; 4 sets of French fries that cost $1.20; 5 cups of soda that cost $0.5 each; and 1 platter of spaghetti that cost $2.7. How much will each of them pay if they will split the bill equally?", "answer": "The cost of 5 pieces of hamburger is $3 x 5 = $<<3*5=15>>15.\nThe cost of 4 sets of French fries is $1.20 x 4 = $<<1.20*4=4.80>>4.80.\nThe cost of 5 cups of soda is $0.5 x 5 = $<<0.5*5=2.50>>2.50.\nSo their total bill is $15 + $4.80 + $2.50 +$2.7 = $<<15+4.8+2.5+2.7=25>>25.\nHence, each of the five friends will contribute $25/5 = $<<25/5=5>>5.\n#### 5"}


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
    # Randomly select names, items, places, and a county for the scenario
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item1, item2, item3, item4 = random.sample(items, 4)  # Select four different items
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    
    # Ensure variable names are suitable for inclusion in solution_code
    name_var = name.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    item3_var = item3.replace(' ', '_')
    item4_var = item4.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_')
    
    # Randomly determine quantities and prices ensuring integer results for total calculations
    quantity1, price1 = get_params_combination()
    quantity2, price2 = get_params_combination()
    quantity3, price3 = get_params_combination()
    quantity4, price4 = get_params_combination()
    people_count = random.randint(2, 8)  # Number of friends
    
    # Construct the problem statement
    problem_statement = f"{people_count} friends eat at {place} in {county} and order the following: "
    problem_statement += f"{quantity1} pieces of {item1} that cost ${price1} each; "
    problem_statement += f"{quantity2} sets of {item2} that cost ${price2}; "
    problem_statement += f"{quantity3} {item3} that cost ${price3} each; "
    problem_statement += f"and {quantity4} {item4} that cost ${price4}. "
    problem_statement += f"How much will each of them pay if they will split the bill equally?"
    
    # Generate solution code
    solution_code = f"""# Calculating costs of items
cost_{item1_var} = {quantity1} * {price1}
cost_{item2_var} = {quantity2} * {price2}
cost_{item3_var} = {quantity3} * {price3}
cost_{item4_var} = {quantity4} * {price4}

# Total bill
total_bill = cost_{item1_var} + cost_{item2_var} + cost_{item3_var} + cost_{item4_var}

# Amount each friend pays
each_pays = total_bill / {people_count}

result = each_pays
"""

    # Execute the solution code to get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)
    total_bill = round(exec_globals['total_bill'], 2)

    # Generate solution without code
    solution_wocode = f"The cost of {quantity1} pieces of {item1} is ${price1} x {quantity1} = ${price1 * quantity1}.\n"
    solution_wocode += f"The cost of {quantity2} sets of {item2} is ${price2} x {quantity2} = ${price2 * quantity2}.\n"
    solution_wocode += f"The cost of {quantity3} {item3} is ${price3} x {quantity3} = ${price3 * quantity3}.\n"
    solution_wocode += f"The cost of {quantity4} {item4} is ${price4} x {quantity4} = ${price4 * quantity4}.\n"
    solution_wocode += f"So their total bill is ${round(total_bill, 2)}.\n"
    solution_wocode += f"Hence, each of the {people_count} friends will contribute ${round(result, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters for quantities and prices to ensure calculations result in integer or easily rounded values.
    """
    while True:
        quantity = random.randint(1, 10)  # Ensuring a realistic quantity
        price = random.choice([0.5, 1, 1.5, 2, 2.5, 3])  # Ensuring prices lead to easily calculated totals
        
        # Check if the product is close to an integer
        if math.isclose(quantity * price, round(quantity * price), rel_tol=1e-9):
            return quantity, price


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0037-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0037-1", "idx": i}) + '\n')
