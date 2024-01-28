# Origin problem: {"question": "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?", "answer": "First find the total number of snakes eaten: 5 snakes/jaguar * 6 jaguars = <<5*6=30>>30 snakes\nThen find the total number of birds eaten per day: 30 snakes * 3 birds/snake = <<30*3=90>>90 snakes\nThen multiply the number of snakes by the number of beetles per snake to find the total number of beetles eaten per day: 90 snakes * 12 beetles/snake = <<90*12=1080>>1080 beetles\n#### 1080"}


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
    # Lists of random terms (already defined in the script)
    
    # Get initial amount and subsequent ratio that ensure an integer result
    initial_amount, subsequent_ratio, final_ratio = get_params_combination()
    
    # Randomly select terms
    person_name = random.choice(first_names) + ' ' + random.choice(last_names)
    machine = random.choice(items)
    product = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    person_name_var = person_name.replace(' ', '_')
    machine_var = machine.replace(' ', '_')
    product_var = product.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"Each {machine} produces {initial_amount} {product}s per day, "
    problem_statement += f"each {person_name} operates {subsequent_ratio} {machine}s, "
    problem_statement += f"and each factory in {county} employs {final_ratio} workers like {person_name}. "
    problem_statement += f"How many {product}s are produced each day in the factory?"

    # Generate solution code with specific variable names and comments
    machines_operated_var = f"{machine_var}_operated_by_{person_name_var}"
    total_workers_var = f"total_{person_name_var}s"
    total_production_var = f"total_{product_var}_production"

    solution_code = f"""# Number of {machine}s operated by each worker
{machines_operated_var} = {subsequent_ratio}

# Total number of workers like {person_name} in the factory
{total_workers_var} = {final_ratio}

# Total number of {machine}s in the factory
total_{machine_var}s = {total_workers_var} * {machines_operated_var}

# Total production of {product}s per day in the factory
{total_production_var} = total_{machine_var}s * {initial_amount}

result = {total_production_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"Each {machine} produces {initial_amount} {product}s per day, "
    solution_wocode += f"each {person_name} operates {subsequent_ratio} {machine}s, "
    solution_wocode += f"and each factory in {county} employs {final_ratio} workers like {person_name}. "
    solution_wocode += f"Therefore, the total production of {product}s per day in the factory is {round(subsequent_ratio*final_ratio*initial_amount, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial amount (similar to beetles per bird)
        initial_amount = random.randint(1, 100)

        # Randomly generate subsequent ratios (similar to birds per snake and snakes per jaguar)
        subsequent_ratio = random.randint(1, 10)
        final_ratio = random.randint(1, 10)

        # Check if the final product is an integer
        if isinstance(initial_amount * subsequent_ratio * final_ratio, int):
            return initial_amount, subsequent_ratio, final_ratio


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0021-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
