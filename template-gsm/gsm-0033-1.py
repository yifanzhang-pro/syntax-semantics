# Origin problem: {"question": "To make pizza, together with other ingredients, Kimber needs 10 cups of water, 16 cups of flour, and 1/2 times as many teaspoons of salt as the number of cups of flour. Calculate the combined total number of cups of water, flour, and teaspoons of salt that she needs to make the pizza.", "answer": "To make the pizza, Kimber half as many teaspoons of salt as the number of cups of flour, meaning she needs 1/2*16 = <<16*1/2=8>>8 teaspoons of salt.\nThe total number of cups of flour and teaspoons of salt she needs is 8+16 = <<8+16=24>>24\nShe also needs 10 cups of water, which means the total number of cups of water and flour and teaspoons of salt she needs is 24+10 = <<24+10=34>>34\n#### 34"}


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
    # Random selection of names, items, and locations from predefined lists
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item1, item2 = random.sample(items, 2) # Select two different items
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables adjusted for solution code
    name_var = name.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_')

    initial_amount1, initial_amount2, ratio = get_params_combination()

    problem_statement = f"To complete a project at {place} in {county}, {name} needs {initial_amount1} {item1}, "
    problem_statement += f"{initial_amount2} {item2}, and {ratio} times as many {item1} as the number of {item2}. "
    problem_statement += f"Calculate the total number of {item1}, {item2}, and additional {item1} needed for the project."

    # Solution code
    item1_initial_var = f"{item1_var}_initial"
    item2_initial_var = f"{item2_var}_initial"
    item1_additional_var = f"{item1_var}_additional"
    total_var = f"total_needed"

    solution_code = f"""# Initial quantities
{item1_initial_var} = {initial_amount1}
{item2_initial_var} = {initial_amount2}

# Calculating additional {item1} based on {item2}
{item1_additional_var} = {item2_initial_var} * {ratio}

# Total quantity needed
{total_var} = {item1_initial_var} + {item2_initial_var} + {item1_additional_var}
"""

    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals[total_var]

    # Solution without code
    solution_wocode = f"To complete the project, {name} needs {ratio} times as many {item1} as the number of {item2}, meaning "
    solution_wocode += f"an additional {initial_amount2*ratio} {item1}. "
    solution_wocode += f"The total number of {item1}, {item2}, and additional {item1} needed is {initial_amount1} + {initial_amount2} + {round(initial_amount2*ratio)} = {round(result)}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        initial_amount1 = random.randint(5, 100) # Quantity of item1
        initial_amount2 = random.randint(5, 100) # Quantity of item2
        ratio = random.choice([0.5, 1, 1.5, 2]) # Ensures an integer or easily calculable result for additional item1

        # Ensuring additional item1 calculation results in an integer
        if initial_amount2 * ratio % 1 == 0:
            return initial_amount1, initial_amount2, ratio


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0033-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0033-1", "idx": i}) + '\n')
