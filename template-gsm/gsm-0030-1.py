# Origin problem: {"question": "Ann, Bill, Cate, and Dale each buy personal pan pizzas cut into 4 pieces. If Bill and Dale eat 50% of their pizzas and Ann and Cate eat 75% of the pizzas, how many pizza pieces are left uneaten?", "answer": "In total, there are 4 x 4 = <<4*4=16>>16 pizza pieces.\nBill and Dale eat 2 x 4 x 50% = <<2*4*50*.01=4>>4 pieces.\nAnn and Cate eat 2 x 4 x 75% = <<2*4*75*.01=6>>6 pieces.\nThe four of them eat 4 + 6 = <<4+6=10>>10 pieces.\nThere are 16 - 10 = <<16-10=6>>6 pizza pieces uneaten.\n#### 6"}


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
    # Randomly select names, item, place, and county
    name1, name2, name3, name4 = [random.choice(first_names) for _ in range(4)]
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Replace blanks with '_' for variable names
    name1_var, name2_var, name3_var, name4_var = [name.replace(' ', '_') for name in [name1, name2, name3, name4]]
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get the amounts and rates
    total_amount, rate1, rate2 = get_params_combination()

    # Construct problem statement
    problem_statement = f"{name1}, {name2}, {name3}, and {name4} each buy {total_amount} {item} in {place} in {county}. "
    problem_statement += f"If {name1} and {name2} use {int(round(rate1 * 100,0))}% of their {item} and {name3} and {name4} use {int(round(rate2 * 100, 0))}% of the {item}, "
    problem_statement += f"how many {item} are left unused?"

    # Generate solution code
    total_var = f"total_{item_var}"
    used_var1 = f"{item_var}_used_by_{name1_var}_and_{name2_var}"
    used_var2 = f"{item_var}_used_by_{name3_var}_and_{name4_var}"
    unused_var = f"unused_{item_var}"

    solution_code = f"""# Total {item} bought by each person
{total_var} = {total_amount}

# Amount of {item} used by {name1} and {name2}
{used_var1} = 2 * {total_var} * {rate1}

# Amount of {item} used by {name3} and {name4}
{used_var2} = 2 * {total_var} * {rate2}

# Calculating the unused {item}
{unused_var} = 4 * {total_var} - ({used_var1} + {used_var2})

result = {unused_var}
"""

    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 0))

    # Generate the solution without code
    solution_wocode = f"In total, there are 4 x {total_amount} = {4 * total_amount} {item}. "
    solution_wocode += f"{name1} and {name2} use 2 x {total_amount} x {int(round(rate1 * 100,0))}% = {int(round(2 * total_amount * rate1, 0))} {item}. "
    solution_wocode += f"{name3} and {name4} use 2 x {total_amount} x {int(round(rate2 * 100,0))}% = {int(round(2 * total_amount * rate2, 0))} {item}. "
    solution_wocode += f"The four of them use {int(round(2 * total_amount * rate1, 0))} + {int(round(2 * total_amount * rate2, 0))} = {int(round(2 * total_amount * (rate1 + rate2), 0))} {item}. "
    solution_wocode += f"There are {4 * total_amount} - {int(round(2 * total_amount * (rate1 + rate2), 0))} = {int(round(result, 0))} {item} left unused."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate total amount
        total_amount = random.randint(1, 100)

        # Define potential rates as fractions that will result in whole numbers
        potential_rates = [i / 10 for i in range(1, 10)]  # 10%, 20%, ..., 90%

        # Randomly select two rates
        rate1, rate2 = random.sample(potential_rates, 2)

        # Calculate the amount used by each group and ensure they are integers
        amount_used_group1 = 2 * total_amount * rate1
        amount_used_group2 = 2 * total_amount * rate2

        if amount_used_group1.is_integer() and amount_used_group2.is_integer():
            return total_amount, rate1, rate2


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0030-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
