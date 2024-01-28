# Origin problem: {"question": "Ken created a care package to send to his brother, who was away at boarding school.  Ken placed a box on a scale, and then he poured into the box enough jelly beans to bring the weight to 2 pounds.  Then, he added enough brownies to cause the weight to triple.  Next, he added another 2 pounds of jelly beans.  And finally, he added enough gummy worms to double the weight once again.  What was the final weight of the box of goodies, in pounds?", "answer": "To the initial 2 pounds of jelly beans, he added enough brownies to cause the weight to triple, bringing the weight to 2*3=<<2*3=6>>6 pounds.\nNext, he added another 2 pounds of jelly beans, bringing the weight to 6+2=<<6+2=8>>8 pounds.\nAnd finally, he added enough gummy worms to double the weight once again, to a final weight of 8*2=<<8*2=16>>16 pounds.\n#### 16"}


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
    # Randomly select names, items, places, and counties
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item1 = random.choice(items)
    item2 = random.choice(items)
    item3 = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial amount and subsequent multipliers that ensure integer results
    initial_amount, multiplier1, add_amount, multiplier2 = get_params_combination()

    # Construct the problem statement
    problem_statement = f"{name} started a collection of {item1} at {place} in {county}. Initially, they collected {initial_amount} {item1}. "
    problem_statement += f"Then, they added {item2}, which increased the collection size by {multiplier1} times. "
    problem_statement += f"Next, they added {add_amount} {item3}. Finally, the collection size doubled due to adding more {item1}. "
    problem_statement += f"What was the final size of the collection?"

    # Prepare variable names for solution code
    initial_var = item1.replace(' ', '_') + "_initial"
    collection_var = "collection_size"
    final_var = "final_" + collection_var

    # Generate solution code
    solution_code = f"""# Initial size of {item1} collection
{initial_var} = {initial_amount}

# Collection size increases by {multiplier1} times after adding {item2}
{collection_var} = {initial_var} * {multiplier1}

# Adding {add_amount} {item3} to the collection
{collection_var} += {add_amount}

# Collection size doubles after adding more {item1}
{final_var} = {collection_var} * 2

result = {final_var}
"""

    # Execute the solution code to get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} started with {initial_amount} {item1}. "
    solution_wocode += f"After adding {item2}, the collection was {initial_amount * multiplier1} {item1}. "
    solution_wocode += f"Adding {add_amount} {item3} brought the total to {initial_amount * multiplier1 + add_amount}. "
    solution_wocode += f"Finally, doubling the size with more {item1} brought the total to {round((initial_amount * multiplier1 + add_amount) * 2, 2)}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        initial_amount = random.randint(1, 100)
        multiplier1 = random.choice([2, 3, 4, 5])  # Ensure integer multiplication
        add_amount = random.randint(1, 100)
        multiplier2 = 2  # Double the collection

        # Check if the final calculation results in an integer
        final_amount = (initial_amount * multiplier1 + add_amount) * multiplier2
        if final_amount == int(final_amount):
            return initial_amount, multiplier1, add_amount, multiplier2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0007-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
