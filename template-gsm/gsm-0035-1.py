# Origin problem: {"question": "Mr. Sanchez found out that 40% of his Grade 5  students got a final grade below B. How many of his students got a final grade of B and above if he has 60 students in Grade 5?", "answer": "Since 40% of his students got below B, 100% - 40% = 60% of Mr. Sanchez's students got B and above.\nThus, 60 x 60/100 = <<60*60/100=36>>36 students got B and above in their final grade.\n#### 36"}


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
    # Random selection of variables
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    percent, total_quantity = get_params_combination()

    # Formatting variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_').replace(',', '')

    # Problem statement
    problem_statement = f"{name} found out that {percent}% of the {item} in {place} at {county} are of type A. "
    problem_statement += f"How many of the {item} are of type B and above if they has {total_quantity} {item} in total?"

    # Solution code generation
    percent_type_a_var = f"amount_{percent}_percent_type_A_{item_var}"
    total_quantity_var = f"total_{item_var}"
    percent_type_b_and_above = f"percent_type_B_and_above_{item_var}"

    solution_code = f"""# Percentage of {item}s that are of type A
{percent_type_a_var} = {percent}

# Total number of {item}s
{total_quantity_var} = {total_quantity}

# Calculating the percentage of {item}s that are of type B and above
{percent_type_b_and_above} = 100 - {percent_type_a_var}

# Calculating the number of {item}s that are of type B and above
type_B_and_above = {total_quantity_var} * {percent_type_b_and_above} / 100

result = type_B_and_above
"""

    # Executing the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'])

    # Generating the solution without code
    solution_wocode = f"Since {percent}% of the {item}s are of type A, 100% - {percent}% = {100-percent}% of the {item}s are of type B and above. "
    solution_wocode += f"Thus, {total_quantity} x {100-percent}/100 = {round(result, 2)} {item}s are of type B and above in total."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate total quantity
        total_quantity = random.randint(50, 500)

        # Randomly generate percentage for type A
        percent = random.choice([10, 20, 30, 40, 50, 60, 70, 80])

        # Ensure the resulting calculation will be integer
        if total_quantity * percent % 100 == 0:
            return percent, total_quantity


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0035-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0035-1", "idx": i}) + '\n')
