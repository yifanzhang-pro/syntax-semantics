# Origin problem: {"question": "Carlos is planting a lemon tree. The tree will cost $90 to plant. Each year it will grow 7 lemons, which he can sell for $1.5 each. It costs $3 a year to water and feed the tree. How many years will it take before he starts earning money on the lemon tree?", "answer": "He makes $10.5 selling lemons each year because 7 x 1.5 = <<7*1.5=10.5>>10.5\nHe earns $7.5 each year from the lemon tree because 10.5 - 3 = <<10.5-3=7.5>>7.5\nIt will take 12 years to earn enough to pay off the tree because 90 / 7.5 = <<90/7.5=12>>12\nHe will make money in year 13 because 12 + 1 = <<12+1=13>>13\n#### 13"}


import random
import math
import json
import argparse
import jsonlines

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
    # Select random terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial cost, yearly income, and yearly expense that ensure an integer result
    initial_cost, yearly_income, yearly_expense = get_params_combination()

    # Construct problem statement
    problem_statement = f"{name} is investing in {item}. The initial cost is ${initial_cost}. "
    problem_statement += f"Each year, it will generate ${yearly_income} in revenue. "
    problem_statement += f"It costs ${yearly_expense} a year for maintenance. "
    problem_statement += f"How many years will it take before {name} starts earning money from the {item} at {place} in {county}?"

    # Variables for solution
    revenue_var = f"yearly_revenue_{item.replace(' ', '_')}"
    profit_var = f"yearly_profit_{item.replace(' ', '_')}"
    years_var = f"years_to_earn_from_{item.replace(' ', '_')}"

    # Generate solution code
    solution_code = f"""import math

# Initial investment for {item}
initial_investment = {initial_cost}

# Yearly revenue and expense for {item}
{revenue_var} = {yearly_income}
yearly_expense = {yearly_expense}

# Calculating net profit per year
{profit_var} = {revenue_var} - yearly_expense

# Calculating the years needed to start earning money
{years_var} = math.ceil(initial_investment / {profit_var})

result = {years_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} makes ${round(yearly_income - yearly_expense, 2)} in net revenue each year. "
    solution_wocode += f"It will take {result - 1} years to earn enough to pay off the initial cost of ${initial_cost}. "
    solution_wocode += f"{name} will start making money in year {result}."

    return problem_statement, solution_code, result, solution_wocode

# Define the get_params_combination function to get integer params
def get_params_combination():
    while True:
        # Randomly generate initial cost, yearly income, and yearly expense
        initial_cost = random.randint(50, 10000)
        yearly_income = random.randint(5, 1000)
        yearly_expense = random.randint(1, 500)

        # Check if the net yearly income is positive and results in an integer break-even point
        net_yearly_income = yearly_income - yearly_expense
        if net_yearly_income > 0 and initial_cost % net_yearly_income == 0:
            return initial_cost, yearly_income, yearly_expense


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-13-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
