# Origin problem: {"question": "Anna goes trick-or-treating in a subdivision where she gets 14 pieces of candy per house. Her brother Billy goes trick-or-tricking in a neighboring subdivision where he gets 11 pieces of candy per house. If the first subdivision has 60 houses and the second subdivision has 75 houses, how many more pieces of candy does Anna get?", "answer": "First find the total number of pieces of candy Anna gets: 14 pieces/house * 60 houses = 840 pieces\nThen find the total number of pieces of candy Billy gets: 11 pieces/house * 75 houses = <<11*75=825>>825 pieces\nThen subtract the number of pieces Billy gets from the number Anna gets to find the difference: 840 pieces - 825 pieces = <<840-825=15>>15 pieces\n#### 15"}


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
    name1 = random.choice(first_names) + ' ' + random.choice(last_names)
    name2 = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place1 = random.choice(places)
    place2 = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get parameters for accumulation rates and totals ensuring integer results
    rate1, total1, rate2, total2 = get_params_combination()

    # Variables for use in solution code, ensuring '_' replaces spaces for variables
    name1_var = name1.replace(' ', '_')
    name2_var = name2.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place1_var = place1.replace(' ', '_')
    place2_var = place2.replace(' ', '_')
    county_var = county.replace(' ', '_').replace(',', '')

    # Construct problem statement
    problem_statement = f"{name1} participates in an activity at {place1} in {county}, where they receive {rate1} {item} per instance. "
    problem_statement += f"Meanwhile, {name2} engages in a similar activity at {place2} in {county}, receiving {rate2} {item} per instance. "
    problem_statement += f"If the first scenario involves {total1} instances and the second {total2} instances, how many more {item} does {name1} receive than {name2}?"

    # Generate solution code
    total1_var = f"{item_var}_total_{name1_var}"
    total2_var = f"{item_var}_total_{name2_var}"
    difference_var = f"difference_{item_var}"

    solution_code = f"""# Total {item} received by {name1}
{total1_var} = {rate1} * {total1}

# Total {item} received by {name2}
{total2_var} = {rate2} * {total2}

# Difference in {item} received
{difference_var} = {total1_var} - {total2_var}

result = {difference_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"First, calculate the total number of {item} {name1} receives: {rate1} {item}/instance * {total1} instances = {rate1*total1} {item}. "
    solution_wocode += f"Then, calculate the total number of {item} {name2} receives: {rate2} {item}/instance * {total2} instances = {rate2*total2} {item}. "
    solution_wocode += f"Subtracting the totals, {name1} receives {rate1*total1} - {rate2*total2} = {result} more {item} than {name2}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values for rates and totals.
    """
    # Randomly generate rates and totals that ensure integer outcomes
    rate1 = random.randint(1, 20)  # pieces per instance for the first scenario
    total1 = random.randint(10, 100)  # total instances in the first scenario
    rate2 = random.randint(1, 20)  # pieces per instance for the second scenario
    total2 = random.randint(10, 100)  # total instances in the second scenario

    return rate1, total1, rate2, total2


def get_params_combination():
    """
    Select integer parameters to ensure the total for the first scenario
    is greater than or equal to the total for the second, avoiding negative results.
    """
    while True:
        # Randomly generate rates and totals
        rate1 = random.randint(1, 20)  # pieces per instance for the first scenario
        total1 = random.randint(50, 100)  # total instances in the first scenario to increase chances of higher total
        rate2 = random.randint(1, 20)  # pieces per instance for the second scenario
        total2 = random.randint(30, 50)  # total instances in the second scenario, lower to ensure less total
        
        # Calculate totals
        total_items1 = rate1 * total1
        total_items2 = rate2 * total2
        
        # Ensure the first total is greater than or equal to the second
        if total_items1 >= total_items2:
            return rate1, total1, rate2, total2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems
        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0039-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0039-1", "idx": i}) + '\n')
