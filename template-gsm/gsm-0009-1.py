# Origin problem: {"question": "Tina makes $18.00 an hour.  If she works more than 8 hours per shift, she is eligible for overtime, which is paid by your hourly wage + 1/2 your hourly wage.  If she works 10 hours every day for 5 days, how much money does she make?", "answer": "She works 8 hours a day for $18 per hour so she makes 8*18 = $<<8*18=144.00>>144.00 per 8-hour shift\nShe works 10 hours a day and anything over 8 hours is eligible for overtime, so she gets 10-8 = <<10-8=2>>2 hours of overtime\nOvertime is calculated as time and a half so and she makes $18/hour so her overtime pay is 18*.5 = $<<18*.5=9.00>>9.00\nHer overtime pay is 18+9 = $<<18+9=27.00>>27.00\nHer base pay is $144.00 per 8-hour shift and she works 5 days and makes 5 * $144 = $<<144*5=720.00>>720.00\nHer overtime pay is $27.00 per hour and she works 2 hours of overtime per day and makes 27*2 = $<<27*2=54.00>>54.00 in overtime pay\n2 hours of overtime pay for 5 days means she makes 54*5 = $270.00\nIn 5 days her base pay is $720.00 and she makes $270.00 in overtime pay so she makes $720 + $270 = $<<720+270=990.00>>990.00\n#### 990"}


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
    
    # Get base quantity and price, and discounted price for additional quantity
    base_quantity, base_price, discount_price = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} sells {item} at {place} in {county}. The price of one {item} is ${base_price}. "
    problem_statement += f"For quantities beyond {base_quantity}, the price per {item} is ${discount_price}. "
    problem_statement += f"If {name} sells {base_quantity + 5} {item}, how much money does they make?"

    # Generate solution code with specific variable names and comments
    item_var = item.replace(' ', '_')
    total_sales_var = f"total_{item_var}_sales"

    solution_code = f"""# Base sales for the first {base_quantity} {item}
base_sales = {base_quantity} * {base_price}

# Sales for the additional {item} with discounted price
additional_sales = 5 * {discount_price}

# Calculating the total sales
{total_sales_var} = base_sales + additional_sales

result = {total_sales_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} sells {base_quantity} {item} at the price of ${base_price} each, making ${base_quantity*base_price}. "
    solution_wocode += f"For the additional 5 {item}, sold at ${discount_price} each, they make ${5*discount_price}. "
    solution_wocode += f"In total, {name} makes ${base_quantity*base_price} + ${5*discount_price} = ${round(result, 2)}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate base quantity
        base_quantity = random.randint(10, 500)

        # Randomly generate base price ensuring it's at least 2
        base_price = random.randint(2, 100)

        # Randomly generate discounted price which should be lower than the base price
        discount_price = random.randint(1, base_price - 1)

        return base_quantity, base_price, discount_price


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0009-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0009-1", "idx": i}) + '\n')
