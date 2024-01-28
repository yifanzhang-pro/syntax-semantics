# Origin problem: {"question": "Mrs. Snyder used to spend 40% of her monthly income on rent and utilities. Her salary was recently increased by $600 so now her rent and utilities only amount to 25% of her monthly income. How much was her previous monthly income?", "answer": "Let her previous monthly income be p\nThe cost of her rent and utilities was 40% of p which is (40/100)*p = 2p/5\nHer income was increased by $600 so it is now p+$600\nThe cost of her rent and utilities now amount to 25% of (p+$600) which is (25/100)*(p+$600) = (p+$600)/4\nEquating both expressions for cost of rent and utilities: 2p/5 = (p+$600)/4\nMultiplying both sides of the equation by 20 gives 8p = 5p+$3000\nSubtracting 5p from both sides gives: 3p = $3000\nDividing both sides by 3 gives p = $1000\n#### 1000"}


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

    # Get initial percentage, new percentage, and budget change that ensure an integer result
    initial_percentage, new_percentage, budget_change = get_params_combination()

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"{name} used to spend {initial_percentage}% of their monthly budget on {item} in {place}, {county}. "
    problem_statement += f"Their budget was recently increased by ${budget_change}, so now their spending on {item} only amounts to {new_percentage}% of their monthly budget. "
    problem_statement += "How much was their previous monthly budget?"

    # Generate solution code with specific variable names and comments
    previous_budget_var = f"previous_budget"
    current_budget_var = f"current_budget"
    initial_expense_var = f"initial_expense"
    new_expense_var = f"new_expense"

    solution_code = f"""from sympy import symbols, Eq, solve

# Define the variables
{previous_budget_var} = symbols('p') # Previous monthly budget
{current_budget_var} = {previous_budget_var} + {budget_change} # Current monthly budget

# Initial and new expense calculations
{initial_expense_var} = {initial_percentage} / 100 * {previous_budget_var}
{new_expense_var} = {new_percentage} / 100 * {current_budget_var}

# Equation based on the problem statement
# Equating the initial and new expense
equation = Eq({initial_expense_var}, {new_expense_var})

# Solving the equation for the previous budget
sol = solve(equation, {previous_budget_var})

result = sol[0]
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 0))

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} used to spend {initial_percentage}% of their monthly budget on {item} in {place}, {county}. "
    solution_wocode += f"Their budget was increased by ${budget_change}, so now their spending on {item} is {new_percentage}% of their budget. "
    solution_wocode += f"The previous monthly budget, denoted as p, satisfies the equation {initial_percentage}% of p = {new_percentage}% of (p + ${budget_change}). "
    solution_wocode += f"Solving this equation gives p = ${round(result, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial and new percentages
        initial_percentage = random.randint(5, 95)
        new_percentage = random.randint(5, 95)

        # Ensure percentages are different to avoid division by zero
        if initial_percentage == new_percentage:
            continue

        # Randomly generate budget change
        budget_change = random.randint(100, 5000)

        # Test the calculation with a placeholder budget
        # The budget is set to a multiple of 100 for simplicity
        test_budget = 10000

        # Calculate initial and new expenses
        initial_expense = initial_percentage / 100 * test_budget
        new_expense = new_percentage / 100 * (test_budget + budget_change)

        # The condition for integer solution:
        # The difference in expenses should be an integer multiple of the difference in percentages
        expense_difference = new_expense - initial_expense
        percentage_difference = new_percentage - initial_percentage
        if expense_difference % percentage_difference == 0:
            return initial_percentage, new_percentage, budget_change


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0029-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
