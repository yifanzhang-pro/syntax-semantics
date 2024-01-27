# Origin problem: {"question": "Melanie is a door-to-door saleswoman. She sold a third of her vacuum cleaners at the green house, 2 more to the red house, and half of what was left at the orange house. If Melanie has 5 vacuum cleaners left, how many did she start with?", "answer": "First multiply the five remaining vacuum cleaners by two to find out how many Melanie had before she visited the orange house: 5 * 2 = <<5*2=10>>10\nThen add two to figure out how many vacuum cleaners she had before visiting the red house: 10 + 2 = <<10+2=12>>12\nNow we know that 2/3 * x = 12, where x is the number of vacuum cleaners Melanie started with. We can find x by dividing each side of the equation by 2/3, which produces x = 18\n#### 18"}


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
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place1, place2, place3 = random.sample(places, 3)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial amount, fractions, and additional amounts for each step
    initial_amount, fraction1, additional1 = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} works in retail. They sold {fraction1*100:.0f}% of their {item} at {place1}, {additional1} more at {place2} in {county}, "
    problem_statement += f"and then half of what was left at {place3}. If {name} has {initial_amount} {item} left, how many did they start with?"

    # Variable names for clarity
    initial_var = f"initial_{item.replace(' ', '_')}"
    final_var = f"final_{item.replace(' ', '_')}"
    after_place2_var = f"after_{place2.replace(' ', '_')}_{item.replace(' ', '_')}"
    before_place2_var = f"before_{place2.replace(' ', '_')}_{item.replace(' ', '_')}"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Reversing the action at {place3}
{after_place2_var} = {initial_amount} * 2

# Reversing the action at {place2}
{before_place2_var} = {after_place2_var} + {additional1}

# Calculating the initial amount based on the action at {place1}
{initial_var} = {before_place2_var} / (1 - {fraction1})

result = {initial_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} sold {fraction1*100:.0f}% of their {item} at {place1}, {additional1} more at {place2}, "
    solution_wocode += f"and then half of what was left at {place3}. "
    solution_wocode += f"First, multiply the remaining {initial_amount} {item} by two to find out how many {name} had before {place3}: "
    solution_wocode += f"{initial_amount} * 2 = {after_place2_var}\n"
    solution_wocode += f"Then add {additional1} to figure out how many {item} they had before {place2}: "
    solution_wocode += f"{after_place2_var} + {additional1} = {before_place2_var}\n"
    solution_wocode += f"Now, we know that (1 - {fraction1}) * x = {before_place2_var}, where x is the number of {item} {name} started with. "
    solution_wocode += f"We can find x by dividing each side of the equation by (1 - {fraction1}), which produces x = round({initial_var}, 2)\n"
    solution_wocode += f"#### round({initial_var}, 2)"

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    # Randomly generate initial amount, fractions, and additional amounts
    initial_amount = random.randint(1, 100)
    # Generate a random fraction with two decimal places between 0.01 and 0.99
    fraction1 = round(random.uniform(0.01, 0.99), 2)
    additional1 = random.randint(1, 10)  # Additional amount sold at the second place

    return initial_amount, fraction1, additional1


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0013-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
