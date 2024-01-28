# Origin problem: {"question": "Alexis is applying for a new job and bought a new set of business clothes to wear to the interview. She went to a department store with a budget of $200 and spent $30 on a button-up shirt, $46 on suit pants, $38 on a suit coat, $11 on socks, and $18 on a belt. She also purchased a pair of shoes, but lost the receipt for them. She has $16 left from her budget. How much did Alexis pay for the shoes?", "answer": "Let S be the amount Alexis paid for the shoes.\nShe spent S + 30 + 46 + 38 + 11 + 18 = S + <<+30+46+38+11+18=143>>143.\nShe used all but $16 of her budget, so S + 143 = 200 - 16 = 184.\nThus, Alexis paid S = 184 - 143 = $<<184-143=41>>41 for the shoes.\n#### 41"}

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
    activities = ["shopping", "project work", "event organizing", "construction"]

    # Get initial budget/resource and known expenses
    initial_budget, known_expenses = get_params_combination()

    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    activity = random.choice(activities)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} is involved in {activity} at {place} in {county} with a budget of ${initial_budget}. "
    expense_list = ' + '.join([f"${e}" for e in known_expenses[:-1]])
    problem_statement += f"They spent {expense_list} on various items, including {item}. "
    problem_statement += f"There's one item, but they lost the receipt for it. They have ${known_expenses[-1]} left from their budget. "
    problem_statement += f"How much did {name} pay for the lost item?"

    # Generate solution code with specific variable names and comments
    budget_var = f"{activity.replace(' ', '_')}_budget"
    expenses_var = f"{activity.replace(' ', '_')}_expenses"
    remaining_var = f"{activity.replace(' ', '_')}_remaining"
    lost_item_var = f"lost_{item.replace(' ', '_')}"

    solution_code = f"""# Budget and expenses for {name}'s {activity}
{budget_var} = {initial_budget}
{expenses_var} = sum({known_expenses[:-1]})
{remaining_var} = {known_expenses[-1]}

# Calculating the cost of the lost item
{lost_item_var} = {budget_var} - ({expenses_var} + {remaining_var})

result = {lost_item_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} had a budget of ${initial_budget} for {activity}. "
    solution_wocode += f"They spent a total of ${sum(known_expenses[:-1])} on known items. "
    solution_wocode += f"With ${known_expenses[-1]} remaining, the cost of the lost item is ${round(initial_budget - sum(known_expenses[:-1]) - known_expenses[-1], 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial budget
        initial_budget = random.randint(100, 10000)

        # Randomly generate known expenses
        num_expenses = random.randint(2, 5)
        known_expenses = [random.randint(10, initial_budget // (num_expenses + 2)) for _ in range(num_expenses)]

        # Calculate the remaining budget
        spent_budget = sum(known_expenses)
        remaining_budget = random.randint(10, initial_budget - spent_budget - 10)

        # Ensure the remaining budget and lost item expense are positive integers
        if remaining_budget > 0 and initial_budget - spent_budget - remaining_budget > 0:
            known_expenses.append(remaining_budget)
            return initial_budget, known_expenses


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0008-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
