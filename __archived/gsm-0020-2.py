# Origin problem: {"question": "Bella bought stamps at the post office. Some of the stamps had a snowflake design, some had a truck design, and some had a rose design. Bella bought 11 snowflake stamps. She bought 9 more truck stamps than snowflake stamps, and 13 fewer rose stamps than truck stamps. How many stamps did Bella buy in all?", "answer": "The number of truck stamps is 11 + 9 = <<11+9=20>>20.\nThe number of rose stamps is 20 \u2212 13 = <<20-13=7>>7.\nBella bought 11 + 20 + 7 = <<11+20+7=38>>38 stamps in all.\n#### 38"}


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
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    items_subset = random.sample(items, 3)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item1_var = items_subset[0].replace(' ', '_')
    item2_var = items_subset[1].replace(' ', '_')
    item3_var = items_subset[2].replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get initial amount and subsequent differences
    initial_amount, extra_amount, less_amount = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} bought items at {place} in {county}. "
    problem_statement += f"Some of the items were {items_subset[0]}, some were {items_subset[1]}, and some were {items_subset[2]}. "
    problem_statement += f"{name} bought {initial_amount} {items_subset[0]}. "
    problem_statement += f"They bought {extra_amount} more {items_subset[1]} than {items_subset[0]}, and {less_amount} fewer {items_subset[2]} than {items_subset[1]}. "
    problem_statement += f"How many items did {name} buy in all?"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Number of {items_subset[0]} bought by {name}
{item1_var} = {initial_amount}

# Calculating the number of {items_subset[1]}
{item2_var} = {item1_var} + {extra_amount}

# Calculating the number of {items_subset[2]}
{item3_var} = {item2_var} - {less_amount}

# Calculating the total number of items bought
total_items = {item1_var} + {item2_var} + {item3_var}

result = total_items
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"The number of {items_subset[1]} is {initial_amount} + {extra_amount} = <<{initial_amount}+{extra_amount}={initial_amount + extra_amount}>>{initial_amount + extra_amount}.\n"
    solution_wocode += f"The number of {items_subset[2]} is {initial_amount + extra_amount} - {less_amount} = <<{initial_amount + extra_amount}-{less_amount}={initial_amount + extra_amount - less_amount}>>{initial_amount + extra_amount - less_amount}.\n"
    solution_wocode += f"{name} bought {initial_amount} + {initial_amount + extra_amount} + {initial_amount + extra_amount - less_amount} = <<{initial_amount}+{initial_amount + extra_amount}+{initial_amount + extra_amount - less_amount}={result}>>{result} items in all.\n#### {result}"

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    initial_amount = random.randint(1, 50)  # Base number of items
    extra_amount = random.randint(1, 10)    # Extra number for the second item
    less_amount = random.randint(1, 10)     # Less number for the third item

    return initial_amount, extra_amount, less_amount


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0020-2--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
