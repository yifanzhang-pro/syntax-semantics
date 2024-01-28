# Origin problem: {"question": "Mary does her grocery shopping on Saturday. She does her shopping only at a specific store where she is allowed a credit of $100, which must be paid in full before her next shopping trip. That week she spent the full credit limit and paid $15 of it on Tuesday and $23 of it on Thursday. How much credit will Mary need to pay before her next shopping trip?", "answer": "So far, Mary has paid back $15 +$23=$<<15+23=38>>38 of the credit.\nSo she still needs to pay $100-$38=$<<100-38=62>>62\n#### 62"}


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


# Function to generate problem and solution code
def generate_problem_and_solution_code():
    # Lists of random terms
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Get initial amount and subsequent subtractions ensuring integer results
    initial_amount, subtraction1, subtraction2 = get_params_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    day1 = random.choice(days_of_week)
    day2 = random.choice([day for day in days_of_week if day != day1])  # Ensure different day

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"{name} receives an initial amount of {initial_amount} {item} at {place} in {county}. "
    problem_statement += f"On {day1}, {name} uses {subtraction1} {item}, and on {day2}, uses another {subtraction2} {item}. "
    problem_statement += f"How many {item} does {name} have left?"

    # Generate solution code with specific variable names and comments
    initial_var = f"initial_{item_var}"
    used_var1 = f"{item_var}_used_on_{day1}"
    used_var2 = f"{item_var}_used_on_{day2}"
    remaining_var = f"remaining_{item_var}"

    solution_code = f"""# Initial amount of {item} received by {name}
{initial_var} = {initial_amount}

# {item} used by {name} on {day1} and {day2}
{used_var1} = {subtraction1}
{used_var2} = {subtraction2}

# Calculating the remaining amount of {item}
{remaining_var} = {initial_var} - {used_var1} - {used_var2}

result = {remaining_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"{name} initially received {initial_amount} {item}. "
    solution_wocode += f"On {day1}, {name} used {subtraction1} {item}, and on {day2}, used another {subtraction2} {item}. "
    solution_wocode += f"Thus, {name} has {initial_amount} - {subtraction1} - {subtraction2} = {round(result, 2)} {item} remaining."

    return problem_statement, solution_code, result, solution_wocode


# Function to get integer parameters for the problem
def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial amount
        initial_amount = random.randint(50, 1000)

        # Randomly generate subtraction amounts
        subtraction1 = random.randint(1, initial_amount // 2)
        subtraction2 = random.randint(1, initial_amount - subtraction1)

        # Ensure the remaining amount is non-negative
        if initial_amount - subtraction1 - subtraction2 >= 0:
            return initial_amount, subtraction1, subtraction2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0024-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
