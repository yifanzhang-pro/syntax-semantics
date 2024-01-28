# Origin problem: {"question": "Billy sells DVDs. He has 8 customers on Tuesday. His first 3 customers buy one DVD each.  His next 2 customers buy 2 DVDs each.  His last 3 customers don't buy any DVDs. How many DVDs did Billy sell on Tuesday?", "answer": "His first 3 customers buy 3 * 1 = <<3*1=3>>3 DVDs.\nHis next 2 buy 2 * 2 = <<2*2=4>>4 DVDs.\nHe sells a total of 3 + 4 + 0 = <<3+4+0=7>>7 DVDs.\n#### 7"}


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
    day_of_week = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # Get customer groups and items per customer
    customer_groups, items_per_customer = get_params_combination()

    # Problem statement
    problem_statement = f"{name} sells {item} at {place} in {county} on {day_of_week}. "
    total_customers = sum(customer_groups)
    problem_statement += f"They have {total_customers} customers on that day. "

    for i, group in enumerate(customer_groups):
        problem_statement += f"Their next {group} customers buy {items_per_customer[i]} {item} each. " if group > 0 else ""

    problem_statement += f"How many {item} did {name} sell on {day_of_week}?"

    # Generate solution code
    total_sales_var = f"total_{item.replace(' ', '_')}_sold"
    solution_code = f"{total_sales_var} = 0\n"

    for i, group in enumerate(customer_groups):
        group_var = f"group_{i+1}_sales"
        solution_code += f"{group_var} = {group} * {items_per_customer[i]}\n"
        solution_code += f"{total_sales_var} += {group_var}\n"

    solution_code += f"result = {total_sales_var}"

    # Solution without code
    solution_wocode = ""
    total_sales = 0

    for i, group in enumerate(customer_groups):
        group_sales = round(group * items_per_customer[i], 2)
        total_sales += group_sales
        solution_wocode += f"The next {group} customers buy {group_sales} {item}. " if group > 0 else ""

    solution_wocode += f"In total, {name} sold {total_sales} {item} on {day_of_week}."

    return problem_statement, solution_code, total_sales, solution_wocode


def get_params_combination():
    """
    Configure integer parameters for customer groups and items per customer.
    """
    # Define number of customer groups (between 2 and 4)
    num_groups = random.randint(2, 4)

    # Generate random customer groups ensuring a non-zero total
    customer_groups = [random.randint(0, 10) for _ in range(num_groups)]
    while sum(customer_groups) == 0:
        customer_groups = [random.randint(0, 10) for _ in range(num_groups)]

    # Generate random items per customer for each group
    items_per_customer = [random.randint(0, 5) for _ in range(num_groups)]

    return customer_groups, items_per_customer


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-test-0022-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
