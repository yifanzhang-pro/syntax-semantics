# Origin problem: {"problem": "The perimeter of a rectangular garden is 60 feet. If the length of the field is twice the width, what is the area of the field, in square feet?", "solution": "If the length is $l$ and the width is $w$, then the perimeter is $2l+2w$. We can set up the equations $2l+2w=60 \\Rightarrow l+w=30$ and $l=2w$. Now we substitute $l$ in terms of $w$ into the first equation and get $l+w=2w+w=30$, so $w=10$ and $l=2(10)=20$. That means the area of the rectangular garden is $lw=20(10)=\\boxed{200}$ square feet.", "idx": 36}


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
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get values for variables in the expression
    total_cost, item_cost, additional_cost = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} plans to buy some {item}s from a store in {place}, {county}. The total cost is supposed to be ${total_cost}. "
    problem_statement += f"If one {item} costs ${item_cost} and there is an additional cost which is twice the cost of one {item}, how many {item}s can {name} buy?"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Cost of one {item.replace(' ', '_')}
item_cost = {item_cost}

# Additional cost which is twice the cost of one {item}
additional_cost = 2 * item_cost

# Total cost
total_cost = {total_cost}

# Number of {item}s that can be bought
num_{item.replace(' ', '_')} = (total_cost - additional_cost) / item_cost

result = num_{item.replace(' ', '_')}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals[f'result']

    # Generate the solution without code
    solution_wocode = f"With a total budget of ${total_cost}, and considering each {item} costs ${item_cost}, "
    solution_wocode += f"and an additional cost of ${2 * item_cost}, {name} can buy {int(result)} {item}s."

    return problem_statement, solution_code, int(result), solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate cost of one item and total cost
        item_cost = random.randint(1, 50)
        total_cost = random.randint(3 * item_cost, 300)  # Ensuring it's higher than thrice the item cost for feasibility

        # Ensure the total cost minus twice the item cost is divisible by the item cost
        if (total_cost - 2 * item_cost) % item_cost == 0:
            return total_cost, item_cost, 2 * item_cost


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/math-0036-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
