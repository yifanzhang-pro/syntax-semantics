# Origin problem: {"question": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. 
#   How many clips did Natalia sell altogether in April and May?", 
#   "answer": "Natalia sold 48/2 = <<48/2=24>>24 clips in May.\nNatalia sold 48+24 = <<48+24=72>>72 clips altogether 
#   in April and May.\n#### 72"}


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


def get_integer_combination():
    while True:
        # Randomly generate initial quantity
        initial_quantity = random.randint(10, 10000)

        # Randomly generate subsequent percentage change
        percentage_change = round(random.uniform(-50, 50), 2)

        # Calculate the new quantity
        new_quantity = initial_quantity * (1 + percentage_change / 100)

        # Check if the new quantity is close to an integer
        if math.isclose(new_quantity, round(new_quantity), rel_tol=1e-15):
            return initial_quantity, percentage_change

def generate_problem_and_solution_code():
    # Lists of random terms
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Get initial quantity and subsequent percentage change that ensure an integer result
    initial_quantity, percentage_change = get_integer_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    day = random.choice(days)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"On a {day}, {name} had {initial_quantity} {item} in stock at their store in {place} in {county}. "
    problem_statement += f"Due to a special promotion, there was a {percentage_change}% change in the quantity of {item} by the end of the day. "
    problem_statement += f"How many {item} did {name} have at the end of the day?"

    # Generate solution code with specific variable names and comments
    stock_var = f"{item.replace(' ', '_')}_in_stock"
    change_var = f"{item.replace(' ', '_')}_change"
    end_stock_var = f"end_day_{item.replace(' ', '_')}"

    solution_code = f"""# Initial quantity of {item} in stock
{stock_var} = {initial_quantity}

# Percentage change in the stock
{change_var} = {percentage_change}

# Calculating the quantity of {item} at the end of the day
# by applying the percentage change to the initial stock
{end_stock_var} = {stock_var} * (1 + {change_var} / 100)

result = {end_stock_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'])

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"On a {day}, {name} had {initial_quantity} {item} in stock at their store in {place} in {county}. "
    solution_wocode += f"Due to a special promotion, there was a {percentage_change}% change in the quantity of {item} by the end of the day. "
    solution_wocode += f"This resulted in {name} having {round(result)} {item} at the end of the day."

    return problem_statement, solution_code, result, solution_wocode


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-1-2--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
