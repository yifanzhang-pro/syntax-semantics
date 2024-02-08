# Origin problem: {"question": "Mr. Sam shared a certain amount of money between his two sons, Ken and Tony. If Ken got $1750, and Tony got twice as much as Ken, how much was the money shared?", "answer": "Tony got twice $1750 which is 2*$1750 = $<<2*1750=3500>>3500\nThe total amount shared was $1750+$3500 = $<<1750+3500=5250>>5250\n#### 5250"}


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
    person_name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    entity1, entity2 = random.sample(first_names, 2)  # Assuming entities are named after people for simplicity

    # Get initial amount and subsequent multiplier to ensure an integer result
    initial_amount, subsequent_multiplier = get_params_combination()

    # Replace spaces with underscores for variable names in the solution code
    person_name_var = person_name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_').replace(',', '').replace(' ', '_')  # Remove commas and replace spaces
    entity1_var = entity1.replace(' ', '_')
    entity2_var = entity2.replace(' ', '_')

    # Construct problem statement
    problem_statement = f"{person_name} shared a certain amount of {item} between {entity1} and {entity2} at {place} in {county}. "
    problem_statement += f"If {entity1} got {initial_amount}, and {entity2} got {subsequent_multiplier} times as much as {entity1}, how much was the {item} shared?"

    # Generate solution code
    entity1_amount = initial_amount
    entity2_amount = initial_amount * subsequent_multiplier
    total_amount = entity1_amount + entity2_amount

    solution_code = f"""# Amount of {item} got by {entity1}
{entity1_var}_amount = {entity1_amount}

# Amount of {item} got by {entity2} (multiplier applied)
{entity2_var}_amount = {entity1_var}_amount * {subsequent_multiplier}

# Total amount of {item} shared
total_amount = {entity1_var}_amount + {entity2_var}_amount
"""

    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['total_amount']

    # Generate the solution without code
    solution_wocode = f"{entity2} got {subsequent_multiplier} times {initial_amount} which is {subsequent_multiplier}*{initial_amount} = {entity2_amount}\n"
    solution_wocode += f"The total amount shared was {initial_amount}+{entity2_amount} = {total_amount}\n#### {total_amount}"

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        initial_amount = random.randint(1, 1000)  # Ensure a wide range for initial amount
        subsequent_multiplier = random.randint(2, 5)  # A multiplier to ensure integer results

        # No need for a complex check as subsequent_multiplier is an integer
        return initial_amount, subsequent_multiplier


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0034-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0034-1", "idx": i}) + '\n')
