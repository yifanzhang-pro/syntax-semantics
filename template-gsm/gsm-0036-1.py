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
    # Randomly select names, item, place, and county
    name1 = random.choice(first_names) + ' ' + random.choice(last_names)
    name2 = random.choice(first_names) + ' ' + random.choice(last_names)
    name3 = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county_name = county['CountyName'] + ", " + county["StateName"]
    
    # Variables for use in solution code, with spaces replaced
    name1_var = name1.replace(' ', '_')
    name2_var = name2.replace(' ', '_')
    name3_var = name3.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county_name.replace(' ', '_').replace(',', '')
    
    # Get initial amount
    total_amount, ratio = get_params_combination()
    
    # Construct problem statement
    problem_statement = f"{name1}, {name2}, and {name3} made ${total_amount} from selling {item} at {place} in {county_name}. "
    problem_statement += f"However, half of the ${total_amount} was earned by {name1}. "
    problem_statement += f"{name3} earned half of what {name1} earned. How much more money did {name1} earn than {name3}?"
    
    # Generate solution code
    solution_code = f"""# Total amount made
total_amount = {total_amount}

# {name1}'s share
{name1_var}_share = total_amount * 0.5

# {name3}'s share
{name3_var}_share = {name1_var}_share * 0.5

# Difference in earnings between {name1} and {name3}
difference = {name1_var}_share - {name3_var}_share

result = difference
"""
    
    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'])
    
    # Generate the solution without code
    solution_wocode = f"{name1} earned ${total_amount} * 1/2 = ${round(total_amount*0.5)}. "
    solution_wocode += f"{name3} earned ${round(total_amount*0.5)} * 1/2 = ${round(total_amount*0.25)}. "
    solution_wocode += f"{name1} earned ${round(total_amount*0.5)} - ${round(total_amount*0.25)} = ${round(result)} more than {name3}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Ensure the total amount is a multiple of 4 for easy division
    total_amount = random.choice([x for x in range(100, 10001) if x % 4 == 0])
    ratio = 0.5  # Fixed ratio for this problem structure
    return total_amount, ratio


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0036-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0036-1", "idx": i}) + '\n')
