# Origin problem: {"question": "Mark has a garden with flowers. He planted plants of three different colors in it. Ten of them are yellow, and there are 80% more of those in purple. There are only 25% as many green flowers as there are yellow and purple flowers. How many flowers does Mark have in his garden?", "answer": "There are 80/100 * 10 = <<80/100*10=8>>8 more purple flowers than yellow flowers.\nSo in Mark's garden, there are 10 + 8 = <<10+8=18>>18 purple flowers.\nPurple and yellow flowers sum up to 10 + 18 = <<10+18=28>>28 flowers.\nThat means in Mark's garden there are 25/100 * 28 = <<25/100*28=7>>7 green flowers.\nSo in total Mark has 28 + 7 = <<28+7=35>>35 plants in his garden.\n#### 35"}


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
    county_var = county.replace(' ', '_')

    # Get initial amount and subsequent ratios that ensure integer results
    initial_amount, extra_ratio, percentage = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} has a collection of {item} in {place}, {county}. "
    problem_statement += f"They have {initial_amount} {item} of one type, and there are {int(extra_ratio*100)}% more of another type. "
    problem_statement += f"There are only {int(percentage * 100)}% as many of a third type as there are of the first two types combined. "
    problem_statement += f"How many {item} does {name} have in total?"

    # Generate solution code with specific variable names and comments
    first_type_var = f"{item.replace(' ', '_')}_first_type"
    second_type_var = f"{item.replace(' ', '_')}_second_type"
    third_type_var = f"{item.replace(' ', '_')}_third_type"
    total_var = f"total_{item.replace(' ', '_')}"

    solution_code = f"""# Number of {item} of the first type
{first_type_var} = {initial_amount}

# Calculating the number of {item} of the second type based on the extra ratio
{second_type_var} = {first_type_var} + {first_type_var} * {extra_ratio}

# Total of first and second types
total_first_second = {first_type_var} + {second_type_var}

# Calculating the number of {item} of the third type based on percentage of first two types
{third_type_var} = total_first_second * {percentage}

# Calculating the total number of {item}
{total_var} = total_first_second + {third_type_var}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']
    if math.isclose(result, int(result), rel_tol=1e-15):
        result = int(result)
    else: 
        result = round(result, 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} has {initial_amount} {item} of one type, and there are {int(extra_ratio*100)}% more of another type, making it {int(round(initial_amount + initial_amount * extra_ratio, 2))} {item} of the second type. "
    solution_wocode += f"The total of the first two types is {int(round(initial_amount + initial_amount * extra_ratio + initial_amount, 2))} {item}. "
    solution_wocode += f"There are only {int(percentage*100)}% as many of the third type as the first two combined, which is {int(round((initial_amount + initial_amount * extra_ratio + initial_amount) * percentage, 2))} {item}. "
    solution_wocode += f"So, {name} has a total of {round(result, 2)} {item}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    """
    Configure integer parameters for the initial amount, extra ratio, and percentage to ensure the final result is an integer.
    """
    while True:
        # Randomly generate initial amount as an integer
        initial_amount = random.randint(5, 5000)

        # Define ratios as integers for easy calculation
        extra_ratio = random.randint(10, 99)  # This will be used as a percentage

        # Calculate the second type amount and ensure it's an integer
        second_type_amount = initial_amount * extra_ratio // 100 + initial_amount
        if second_type_amount != initial_amount * extra_ratio / 100 + initial_amount:
            continue

        percentage = random.randint(10, 99)  # This will be used as a percentage
        # Calculate the third type amount based on the sum of the first two types
        third_type_amount = (initial_amount + second_type_amount) * percentage // 100
        if third_type_amount != (initial_amount + second_type_amount) * percentage / 100:
            continue

        return initial_amount, extra_ratio / 100, percentage / 100


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0005-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0005-1", "idx": i}) + '\n')
