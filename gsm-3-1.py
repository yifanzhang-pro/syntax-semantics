# Origin problem: {"question": "Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. 
# Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. 
# How much more money does Betty need to buy the wallet?", "answer": "In the beginning, Betty has only 100 / 2 = $<<100/2=50>>50.\n
# Betty's grandparents gave her 15 * 2 = $<<15*2=30>>30.\nThis means, Betty needs 100 - 50 - 30 - 15 = $<<100-50-30-15=5>>5 more.\n#### 5"}


import random
import math
import json
import argparse
import jsonlines

random.seed(42) # Consistent random generation

first_names = []
with jsonlines.open('./data/top_first_names.jsonl') as reader:
    for line in reader:
        first_names.append(line['first_name'])

last_names = []
with jsonlines.open('./data/top_last_names.jsonl') as reader:
    for line in reader:
        last_names.append(line['last_name'])

items = []
with jsonlines.open('./data/items-llm.jsonl') as reader:
    for line in reader:
        items.append(line)

places = []
with jsonlines.open('./data/places-llm.jsonl') as reader:
    for line in reader:
        places.append(line)

us_counties = []
with jsonlines.open('./data/us_counties.jsonl') as reader:
    for line in reader:
        us_counties.append(line)


def generate_problem_and_solution_code():
    # Lists of random terms
    items = ["bicycle", "laptop", "camera", "smartphone", "guitar", "skateboard"]

    # Get target amount and initial savings
    target_amount, initial_savings = get_params_combination()

    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)

    # Construct problem statement with specific details
    problem_statement = f"{name} is saving money to buy a {item} which costs ${target_amount}. "
    problem_statement += f"{name} has already saved ${initial_savings}. "
    problem_statement += f"Their friend decided to give them ${initial_savings // 2} for this purpose, "
    problem_statement += f"and their neighbor, twice as much as the friend. "
    problem_statement += f"How much more money does {name} need to buy the {item}?"

    # Generate solution code with specific variable names and comments
    savings_var = f"{item}_savings"
    friend_contribution = f"friend_contribution_for_{item}"
    neighbor_contribution = f"neighbor_contribution_for_{item}"
    total_var = f"total_{item}_fund"

    solution_code = f"""# Initial savings for {item}
{savings_var} = {initial_savings}

# Contribution from friend
{friend_contribution} = {initial_savings // 2}

# Contribution from neighbor, twice as much as the friend
{neighbor_contribution} = 2 * {friend_contribution}

# Calculating the total funds accumulated
{total_var} = {savings_var} + {friend_contribution} + {neighbor_contribution}

# Calculating the additional amount needed
amount_needed = {target_amount} - {total_var}

result = amount_needed
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} initially saved ${initial_savings} to buy a {item}. "
    solution_wocode += f"Their friend contributed ${initial_savings // 2}, and their neighbor contributed ${2 * (initial_savings // 2)}. "
    solution_wocode += f"In total, {name} now has ${initial_savings} + ${initial_savings // 2} + ${2 * (initial_savings // 2)} = ${initial_savings + initial_savings // 2 + 2 * (initial_savings // 2)}. "
    solution_wocode += f"Therefore, {name} still needs ${target_amount - (initial_savings + initial_savings // 2 + 2 * (initial_savings // 2))} to buy the {item}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    while True:
        # Randomly generate target amount for an item
        target_amount = random.randint(50, 5000)

        # Randomly generate initial savings as a fraction of the target
        initial_savings_ratio = random.uniform(0.1, 0.9)
        initial_savings = round(target_amount * initial_savings_ratio)

        # Determine if the initial savings is a significant fraction of the target
        if initial_savings > 10 and initial_savings < target_amount - 30:
            return target_amount, initial_savings


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-3-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
