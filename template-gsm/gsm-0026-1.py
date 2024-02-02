# Origin problem: {"question": "Jack is stranded on a desert island. He wants some salt to season his fish. He collects 2 liters of seawater in an old bucket. If the water is 20% salt, how many ml of salt will Jack get when all the water evaporates?", "answer": "First find how many liters of the seawater are salt: 2 liters * 20% = <<2*20*.01=.4>>.4 liters\nThen multiply that amount by 1000 ml/liter to find the number of ml of salt Jack gets: .4 liters * 1000 ml/liter = <<.4*1000=400>>400 ml\n#### 400"}


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
    # Selecting random elements for the problem
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county_name = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code (replacing spaces with underscores)
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county_name.replace(' ', '_')

    # Get initial volume and concentration
    volume, concentration = get_params_combination()

    # Constructing the problem statement
    problem_statement = f"{name} finds a container with {volume} liters of a solution at {place} in {county_name}. "
    problem_statement += f"The solution is {concentration}% {item}. How many ml of {item} are in the solution?"

    # Generating the solution code
    volume_var = f"{item_var}_volume"
    concentration_var = f"{item_var}_concentration"
    ml_var = f"ml_of_{item_var}"

    solution_code = f"""# Volume of the solution in liters
{volume_var} = {volume}

# Concentration of {item} in the solution
{concentration_var} = {concentration}

# Calculating the volume of {item} in the solution in liters
{item_var}_in_liters = {volume_var} * ({concentration_var} / 100)

# Converting the volume from liters to milliliters
{ml_var} = {item_var}_in_liters * 1000

result = {ml_var}
"""

    # Executing the solution code to get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 0))

    # Generating the solution without code
    solution_wocode = f"{name} finds that the solution is {concentration}% {item}. "
    solution_wocode += f"Therefore, the amount of {item} in the solution is {volume} liters * {concentration}% = {volume * (concentration / 100)} liters. "
    solution_wocode += f"Converting this to milliliters gives {volume * (concentration / 100)} * 1000 = {int(round(result, 0))} ml."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters for volume and concentration to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate volume (in liters)
        volume = random.randint(1, 1000)

        # Randomly generate concentration (in percentage)
        concentration = random.randint(1, 100)

        # Calculate the volume of the substance in liters
        substance_volume = volume * (concentration / 100)

        # Check if the volume in milliliters (substance_volume * 1000) is an integer
        if substance_volume * 1000 == int(substance_volume * 1000):
            return volume, concentration


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0026-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0026-1", "idx": i}) + '\n')
