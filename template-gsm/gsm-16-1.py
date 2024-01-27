# Origin problem: {"question": "Melanie is a door-to-door saleswoman. She sold a third of her vacuum cleaners at the green house, 2 more to the red house, and half of what was left at the orange house. If Melanie has 5 vacuum cleaners left, how many did she start with?", "answer": "First multiply the five remaining vacuum cleaners by two to find out how many Melanie had before she visited the orange house: 5 * 2 = <<5*2=10>>10\nThen add two to figure out how many vacuum cleaners she had before visiting the red house: 10 + 2 = <<10+2=12>>12\nNow we know that 2/3 * x = 12, where x is the number of vacuum cleaners Melanie started with. We can find x by dividing each side of the equation by 2/3, which produces x = 18\n#### 18"}


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
    # Selecting random names, places, and items
    investor_name = random.choice(first_names) + ' ' + random.choice(last_names)
    investment1 = random.choice(items)
    investment2 = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county_name = county['CountyName'] + ", " + county["StateName"]
    
    # Ensuring that the two investments are distinct
    while investment2 == investment1:
        investment2 = random.choice(items)

    # Randomly generated investment amounts and profit percentages
    amount1, profit_percent1 = get_params_combination()
    amount2, profit_percent2 = get_params_combination()

    # Constructing the problem statement
    problem_statement = f"{investor_name} wants to make an investment in {county_name}. They are considering two options: "
    problem_statement += f"investing ${amount1} in {investment1} or ${amount2} in {investment2}. "
    problem_statement += f"The market speculates a {profit_percent1}% increase in {investment1} and a {profit_percent2}% increase in {investment2} within a month. "
    problem_statement += f"Which investment will maximize {investor_name}'s profit after one month, and what will be the profit?"

    # Solution code
    solution_code = f"""# Investment amounts and expected profit percentages
amount1 = {amount1}
profit_percent1 = {profit_percent1}
amount2 = {amount2}
profit_percent2 = {profit_percent2}

# Calculating profits for each investment
profit1 = amount1 * (profit_percent1 / 100)
profit2 = amount2 * (profit_percent2 / 100)

# Determining the better investment and its profit
if profit1 > profit2:
    best_investment = '{investment1}'
    max_profit = profit1
else:
    best_investment = '{investment2}'
    max_profit = profit2

result = max_profit
"""

    # Generating the solution without code
    profit1 = amount1 * (profit_percent1 / 100)
    profit2 = amount2 * (profit_percent2 / 100)
    if profit1 > profit2:
        best_investment = investment1
        max_profit = round(profit1, 2)
    else:
        best_investment = investment2
        max_profit = round(profit2, 2)

    solution_wocode = f"If {investor_name} invests in {investment1}, the profit will be ${round(profit1, 2)}. "
    solution_wocode += f"If they invest in {investment2}, the profit will be ${round(profit2, 2)}. "
    solution_wocode += f"The better investment is in {best_investment}, with a profit of ${max_profit}."

    return problem_statement, solution_code, max_profit, solution_wocode


def get_params_combination():
    # Generate investment amount and profit percentage ensuring they are integers
    amount = random.randint(1000, 50000)  # Investment amount between $1,000 and $50,000
    profit_percent = random.randint(1, 20)  # Profit percentage between 1% and 20%
    return amount, profit_percent


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-16-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
