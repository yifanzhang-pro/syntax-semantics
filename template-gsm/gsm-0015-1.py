# Origin problem: {"question": "James creates a media empire.  He creates a movie for $2000.  Each DVD cost $6 to make.  He sells it for 2.5 times that much.  He sells 500 movies a day for 5 days a week.  How much profit does he make in 20 weeks?", "answer": "He sold each DVD for 6*2.5=$<<6*2.5=15>>15\nSo he makes a profit of 15-6=$<<15-6=9>>9\nSo each day he makes a profit of 9*500=$<<9*500=4500>>4500\nSo he makes 4500*5=$<<4500*5=22500>>22,500\nHe makes 22,500*20=$<<22500*20=450000>>450,000\nThen after the cost of creating the movie he has a profit of 450,000-2000=$<<450000-2000=448000>>448,000\n#### 448000"}


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
    project = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial investment, production cost, sales multiplier, daily sales, and duration
    initial_investment, production_cost, sales_multiplier, daily_sales, days_per_week, total_weeks = get_params_combination()

    # Construct the problem statement
    problem_statement = f"{name} starts a business by creating a {project} at {place} in {county}. "
    problem_statement += f"The initial investment for creating the {project} is ${initial_investment}. "
    problem_statement += f"Each unit of the {project} costs ${production_cost} to produce. "
    problem_statement += f"{name} sells it for {sales_multiplier} times the production cost. "
    problem_statement += f"They sell {daily_sales} units a day for {days_per_week} days a week. "
    problem_statement += f"How much profit does {name} make in {total_weeks} weeks?"

    # Generate solution code with specific variable names
    selling_price_var = f"{project.replace(' ', '_')}_selling_price"
    profit_per_unit_var = f"{project.replace(' ', '_')}_profit_per_unit"
    daily_profit_var = f"daily_{project.replace(' ', '_')}_profit"
    weekly_profit_var = f"weekly_{project.replace(' ', '_')}_profit"
    total_profit_var = f"total_{project.replace(' ', '_')}_profit"
    net_profit_var = f"net_{project.replace(' ', '_')}_profit"

    solution_code = f"""# Selling price of each unit
{selling_price_var} = {production_cost} * {sales_multiplier}

# Profit per unit
{profit_per_unit_var} = {selling_price_var} - {production_cost}

# Daily profit
{daily_profit_var} = {profit_per_unit_var} * {daily_sales}

# Weekly profit
{weekly_profit_var} = {daily_profit_var} * {days_per_week}

# Total profit for {total_weeks} weeks
{total_profit_var} = {weekly_profit_var} * {total_weeks}

# Net profit after subtracting initial investment
{net_profit_var} = {total_profit_var} - {initial_investment}

result = {net_profit_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} sells each unit for ${round(production_cost * sales_multiplier, 2)}.\n"
    solution_wocode += f"Profit per unit is ${round((production_cost * sales_multiplier) - production_cost, 2)}.\n"
    solution_wocode += f"Daily profit is ${round(((production_cost * sales_multiplier) - production_cost) * daily_sales, 2)}.\n"
    solution_wocode += f"Weekly profit is ${round((((production_cost * sales_multiplier) - production_cost) * daily_sales) * days_per_week, 2)}.\n"
    solution_wocode += f"Total profit for {total_weeks} weeks is ${round(((((production_cost * sales_multiplier) - production_cost) * daily_sales) * days_per_week) * total_weeks, 2)}.\n"
    solution_wocode += f"After subtracting the initial investment, the net profit is ${round(((((production_cost * sales_multiplier) - production_cost) * daily_sales) * days_per_week) * total_weeks - initial_investment, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate parameters
        initial_investment = random.randint(1000, 100000)
        production_cost = random.randint(1, 20)
        sales_multiplier = random.randint(2, 10)
        daily_sales = random.randint(10, 1000)
        days_per_week = random.randint(1, 7)
        total_weeks = random.randint(1, 52)

        # Check if the calculations result in integer values
        selling_price = production_cost * sales_multiplier
        profit_per_unit = selling_price - production_cost
        daily_profit = profit_per_unit * daily_sales
        weekly_profit = daily_profit * days_per_week
        total_profit = weekly_profit * total_weeks
        net_profit = total_profit - initial_investment

        if all(isinstance(value, int) for value in [selling_price, profit_per_unit, daily_profit, weekly_profit, total_profit, net_profit]):
            return initial_investment, production_cost, sales_multiplier, daily_sales, days_per_week, total_weeks


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0015-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0015-1", "idx": i}) + '\n')
