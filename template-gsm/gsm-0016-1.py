# Origin problem: {"question": "The profit from a business transaction is shared among 2 business partners, Mike and Johnson in the ratio 2:5 respectively. If Johnson got $2500, how much will Mike have after spending some of his share on a shirt that costs $200?", "answer": "According to the ratio, for every 5 parts that Johnson gets, Mike gets 2 parts\nSince Johnson got $2500, each part is therefore $2500/5 = $<<2500/5=500>>500\nMike will get 2*$500 = $<<2*500=1000>>1000\nAfter buying the shirt he will have $1000-$200 = $<<1000-200=800>>800 left\n#### 800"}


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
    resources = ["profits", "revenue", "earnings"]
    actions = ["spending on", "investing in", "donating to"]

    # Get initial ratio part value and expense amount that ensure an integer result
    ratio_part_value, expense_amount = get_params_combination()

    # Randomly select terms
    name1 = random.choice(first_names) + ' ' + random.choice(last_names)
    name2 = random.choice(first_names) + ' ' + random.choice(last_names)
    name1_var = name1.replace(' ', '_')
    name2_var = name2.replace(' ', '_')
    resource = random.choice(resources)
    action = random.choice(actions)
    item = random.choice(items)
    place = random.choice(places)

    # Construct problem statement with specific details
    problem_statement = f"The {resource} from a business transaction is shared between {name1} and {name2} in the ratio 2:5 respectively. "
    problem_statement += f"If {name2} got ${5 * ratio_part_value}, how much will {name1} have after {action} a {item} that costs ${expense_amount}?"

    # Generate solution code with specific variable names and comments
    ratio_var = f"ratio_{name2_var}"
    expense_var = f"expense_{name1_var}"

    solution_code = f"""# Ratio of the {resource} between {name1} and {name2}
{name1_var}_share = 2
{name2_var}_share = 5

# Total amount received by {name2}
{ratio_var} = {name2_var}_share * {ratio_part_value}  # Each part of the ratio is equivalent to {ratio_part_value}

# Calculating the total amount for {name1}
{name1_var}_total = {name1_var}_share * {ratio_part_value}

# Expense for {name1}
{expense_var} = {expense_amount}

# Calculating the remaining amount for {name1}
{name1_var}_remaining = {name1_var}_total - {expense_var}

result = {name1_var}_remaining
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals[f'result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"According to the ratio, for every 5 parts that {name2} gets, {name1} gets 2 parts. "
    solution_wocode += f"Since {name2} got ${5 * ratio_part_value}, each part is therefore ${ratio_part_value}. "
    solution_wocode += f"{name1} will get 2 * ${ratio_part_value} = ${2 * ratio_part_value}. "
    solution_wocode += f"After {action} a {item}, {name1} will have ${2 * ratio_part_value} - ${expense_amount} = ${round(result, 2)} left."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate ratio part value
        ratio_part_value = random.randint(10, 1000) * 5  # Ensures it's divisible by 5

        # Randomly generate expense amount
        expense_amount = random.randint(50, ratio_part_value * 2)  # Ensures it's less than or equal to twice the part value

        # Check if the expense amount is within a realistic range
        if expense_amount <= 2 * ratio_part_value:
            return ratio_part_value, expense_amount


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0016-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
