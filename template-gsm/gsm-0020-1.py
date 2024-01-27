# Origin problem: {"question": "I have 10 liters of orange drink that are two-thirds water and I wish to add it to 15 liters of pineapple drink that is three-fifths water. But as I pour it, I spill one liter of the orange drink. How much water is in the remaining 24 liters?", "answer": "There are 15 x 3/5 = <<15*3/5=9>>9 liters of water from the 15 liters pineapple drink.\nAfter 1 liter of orange drink was spilled, there were 10 - 1 = <<10-1=9>>9 liters of orange drink left.\nOut of the 9 liters, 9 x 2/3 = <<9*2/3=6>>6 liters are water.\nThus, there are a total of 9 + 6 = <<9+6=15>>15 liters of water out of the 24 liters.\n#### 15"}


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
    substances = ["juice", "sauce", "soup", "mixture"]
    components = ["sugar", "salt", "herbs", "spices"]

    # Randomly select terms
    substance1 = random.choice(substances)
    substance2 = random.choice(list(set(substances) - {substance1}))
    component = random.choice(components)
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial volumes and component ratios
    volume1, volume2, ratio1, ratio2, spill = get_params_combination()

    # Construct problem statement
    problem_statement = f"{name} has {volume1} liters of {substance1} that is {ratio1*100:.0f}% {component} and wishes to add it to "
    problem_statement += f"{volume2} liters of {substance2} that is {ratio2*100:.0f}% {component} at {place} in {county}. "
    problem_statement += f"But as they pour it, {spill} liters of the {substance1} is spilled. "
    problem_statement += f"How much {component} is in the remaining {volume1 + volume2 - spill} liters?"

    # Generate solution code
    comp_amount1 = f"{component}_{substance1}_amount"
    comp_amount2 = f"{component}_{substance2}_amount"
    total_comp = f"total_{component}"

    solution_code = f"""# Component amount in {substance1}
{comp_amount1} = {volume1} * {ratio1} - {spill} * {ratio1}

# Component amount in {substance2}
{comp_amount2} = {volume2} * {ratio2}

# Total component amount
{total_comp} = {comp_amount1} + {comp_amount2}
result = {total_comp}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code
    solution_wocode = f"There are {volume2} x {ratio2} = {round(volume2 * ratio2, 2)} liters of {component} from the {volume2} liters {substance2}. "
    solution_wocode += f"After {spill} liters of {substance1} was spilled, there were {volume1 - spill} liters of {substance1} left. "
    solution_wocode += f"Out of the remaining {volume1 - spill} liters, {round((volume1 - spill) * ratio1, 2)} liters are {component}. "
    solution_wocode += f"Thus, there are a total of {round(volume2 * ratio2, 2)} + {round((volume1 - spill) * ratio1, 2)} = {round(result, 2)} liters of {component} out of the {volume1 + volume2 - spill} liters."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    # Integer parameters for volume and spill, finite digit floating numbers for ratios
    volume1 = random.randint(5, 20)  # Liters
    volume2 = random.randint(10, 30)  # Liters
    ratio1 = round(random.uniform(0.1, 0.9), 2)  # Ratio of component in substance1
    ratio2 = round(random.uniform(0.1, 0.9), 2)  # Ratio of component in substance2
    spill = random.randint(1, min(volume1, 5))  # Liters spilled

    return volume1, volume2, ratio1, ratio2, spill


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0020-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
