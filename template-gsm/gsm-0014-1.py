# Origin problem: {"question": "Joy can read 8 pages of a book in 20 minutes. How many hours will it take her to read 120 pages?", "answer": "In one hour, there are 3 sets of 20 minutes.\nSo, Joy can read 8 x 3 = <<8*3=24>>24 pages in an hour.\nIt will take her 120/24 = <<120/24=5>>5 hours to read 120 pages.\n#### 5"}


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

    # Get initial cost, selling ratio, and other parameters ensuring integer results
    initial_cost, selling_ratio, daily_sales, sales_days_per_week, total_weeks = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} starts a business in {place} in {county}. They produce a {item} for ${initial_cost}. "
    problem_statement += f"Each {item} is sold for {selling_ratio} times that amount. "
    problem_statement += f"They sell {daily_sales} {item}s a day for {sales_days_per_week} days a week. "
    problem_statement += f"How much profit do they make in {total_weeks} weeks?"

    # Variables for solution code
    item_var = item.replace(' ', '_')
    cost_var = f"{item_var}_cost"
    selling_price_var = f"{item_var}_selling_price"
    profit_per_item_var = f"profit_per_{item_var}"
    daily_profit_var = f"daily_profit"
    weekly_profit_var = f"weekly_profit"
    total_profit_var = f"total_profit"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Cost of producing one {item}
{cost_var} = {initial_cost}

# Selling price of one {item}
{selling_price_var} = {cost_var} * {selling_ratio}

# Profit per {item}
{profit_per_item_var} = {selling_price_var} - {cost_var}

# Daily profit
{daily_profit_var} = {profit_per_item_var} * {daily_sales}

# Weekly profit
{weekly_profit_var} = {daily_profit_var} * {sales_days_per_week}

# Total profit for {total_weeks} weeks
{total_profit_var} = {weekly_profit_var} * {total_weeks}

# Net profit after subtracting initial cost
net_profit = {total_profit_var} - {cost_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['net_profit']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} produces a {item} for ${initial_cost} and sells it for ${round(initial_cost * selling_ratio, 2)}. "
    solution_wocode += f"The profit per {item} is ${round((initial_cost * selling_ratio) - initial_cost, 2)}. "
    solution_wocode += f"Each day, they make a profit of ${round(((initial_cost * selling_ratio) - initial_cost) * daily_sales, 2)}. "
    solution_wocode += f"Weekly, the profit is ${round((((initial_cost * selling_ratio) - initial_cost) * daily_sales) * sales_days_per_week, 2)}. "
    solution_wocode += f"In {total_weeks} weeks, the total profit is ${round((((((initial_cost * selling_ratio) - initial_cost) * daily_sales) * sales_days_per_week) * total_weeks), 2)}. "
    solution_wocode += f"Subtracting the initial cost, the net profit is ${round(result, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        initial_cost = random.randint(50, 10000)  # Cost of producing an item
        selling_ratio = random.randint(2, 10)  # Selling price as a multiple of the cost
        daily_sales = random.randint(10, 1000)  # Number of items sold per day
        sales_days_per_week = random.randint(1, 7)  # Number of days items are sold per week
        total_weeks = random.randint(1, 52)  # Total duration in weeks

        return initial_cost, selling_ratio, daily_sales, sales_days_per_week, total_weeks


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0014-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
