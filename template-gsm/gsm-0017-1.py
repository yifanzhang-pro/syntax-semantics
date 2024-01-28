# Origin problem: {"question": "In a truck, there are 26 pink hard hats, 15 green hard hats, and 24 yellow hard hats.  If Carl takes away 4 pink hard hats, and John takes away 6 pink hard hats and twice as many green hard hats as the number of pink hard hats that he removed, then calculate the total number of hard hats that remained in the truck.", "answer": "If there were 26 pink hard hats and Carl took away 4 pink hard hats, the number of pink hard hats that remained is 26-4 = <<26-4=22>>22\nJohn also took away 6 pink hard hats, leaving 22-6 = <<22-6=16>>16 pink hard hats in the truck.\nIf John also took twice as many green hard hats as pink hard hats, he took 2*6 = <<6*2=12>>12 green hard hats.\nThe total number of green hard hats that remained in the truck is 15-12 = <<15-12=3>>3\nIn the truck, after some are taken, there were 3 green hard hats + 16 pink hard hats = <<3+16=19>>19 hard hats in the truck.\nAltogether, 19 green and pink hard hats + 24 yellow hards hats = <<19+24=43>>43 hard hats remained in the truck\n#### 43"}


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

    # Get initial amounts and subtraction values that ensure non-negative results
    initial_amounts, subtractions = get_params_combination()
    
    # Randomly select terms
    name1 = random.choice(first_names)
    name2 = random.choice(last_names)
    item1, item2, item3 = random.sample(items, 3)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name1_var = name1.replace(' ', '_')
    name2_var = name2.replace(' ', '_')
    item1_var = item1.replace(' ', '_')
    item2_var = item2.replace(' ', '_')
    item3_var = item3.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"In {place} in {county}, there are {initial_amounts[0]} {item1}, "
    problem_statement += f"{initial_amounts[1]} {item2}, and {initial_amounts[2]} {item3}. "
    problem_statement += f"If {name1} takes away {subtractions[0]} {item1}, and {name2} takes away "
    problem_statement += f"{subtractions[1]} {item1} and twice as many {item2} as the number of "
    problem_statement += f"{item1} that he removed, then calculate the total number of {item1}, {item2}, "
    problem_statement += f"and {item3} that remained in the {place}."

    # Generate solution code with specific variable names and comments
    item1_remaining = f"remaining_{item1_var}"
    item2_remaining = f"remaining_{item2_var}"

    solution_code = f"""# Initial quantities of items
initial_{item1_var} = {initial_amounts[0]}
initial_{item2_var} = {initial_amounts[1]}
initial_{item3_var} = {initial_amounts[2]}

# Calculating remaining {item1} after {name1} and {name2} take some
{name1_var}_took = {subtractions[0]}
{name2_var}_took = {subtractions[1]}
{name2_var}_took_{item2_var} = {subtractions[1]} * 2 # twice as many {item2} as {item1}
{item1_remaining} = initial_{item1_var} - ({name1_var}_took + {name2_var}_took)
{item2_remaining} = initial_{item2_var} - {name2_var}_took_{item2_var}

# Total remaining items
total_remaining = {item1_remaining} + {item2_remaining} + initial_{item3_var}

result = total_remaining
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']
    item1_remaining_value = exec_globals[item1_remaining]
    item2_remaining_value = exec_globals[item2_remaining]

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"In {place}, after {name1} took away {subtractions[0]} {item1}, and {name2} "
    solution_wocode += f"took away {subtractions[1]} {item1} and {subtractions[1] * 2} {item2}, "
    solution_wocode += f"there remained {round(item1_remaining_value, 2)} {item1}, {round(item2_remaining_value, 2)} {item2}, "
    solution_wocode += f"and {initial_amounts[2]} {item3}. "
    solution_wocode += f"So, the total remaining items are {result}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in non-negative values.
    """
    while True:
        # Randomly generate initial amounts for three items
        initial_amounts = [random.randint(20, 100) for _ in range(3)]

        # Randomly generate subtraction values for the first item
        # Ensure that the total subtraction (including the double for the second item) is less than the initial amount
        subtractions = [random.randint(1, min(initial_amounts[0]//3, initial_amounts[1]//4)) for _ in range(2)]

        return initial_amounts, subtractions


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0017-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
