# Origin problem: {"question": "Kylar went to the store to buy glasses for his new apartment. One glass costs $5, but every second glass costs only 60% of the price.
#   Kylar wants to buy 16 glasses. How much does he need to pay for them?", 
#   "answer": "The discount price of one glass is 60/100 * 5 = $<<60/100*5=3>>3.
#   \nIf every second glass is cheaper, that means Kylar is going to buy 16 / 2 = <<16/2=8>>8 cheaper glasses.\nSo for the cheaper glasses, Kylar is going to pay 8 * 3 = $<<8*3=24>>24.\n
#   And for the regular-priced glasses, Kylar will pay 8 * 5 = $<<8*5=40>>40.\nSo in total Kylar needs to pay 24 + 40 = $<<24+40=64>>64 for the glasses he wants to buy.\n#### 64"}

import random
import math
import json
import argparse
import jsonlines

random.seed(42) # Consistent random generation

first_names = []
with jsonlines.open('./data/top_first_names.jsonl') as reader:
    for line in reader:
        first_names.append(line['first_name'])

last_names = []
with jsonlines.open('./data/top_last_names.jsonl') as reader:
    for line in reader:
        last_names.append(line['last_name'])

items = []
with jsonlines.open('./data/items-llm.jsonl') as reader:
    for line in reader:
        items.append(line)

places = []
with jsonlines.open('./data/places-llm.jsonl') as reader:
    for line in reader:
        places.append(line)

us_counties = []
with jsonlines.open('./data/us_counties.jsonl') as reader:
    for line in reader:
        us_counties.append(line)


def generate_problem_and_solution_code():
    # Get initial price, discount ratio, total quantity, and discount frequency
    initial_price, discount_ratio, total_quantity, discount_frequency = get_params_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} went to {place} in {county} to buy {item}. One {item} costs ${initial_price}, "
    problem_statement += f"but every {ordinal(discount_frequency)} {item} costs only {discount_ratio*100:.0f}% of the price. "
    problem_statement += f"{name} wants to buy {total_quantity} {item}. How much do they need to pay for them?"

    # Generate solution code with specific variable names and comments
    discounted_price_var = f"discounted_price_of_one_{item.replace(' ', '_')}"
    num_discounted_items_var = f"number_of_discounted_{item.replace(' ', '_')}"
    total_cost_var = f"total_cost_for_{item.replace(' ', '_')}"

    solution_code = f"""# Discounted price of one {item}
{discounted_price_var} = {discount_ratio} * {initial_price}

# Number of discounted {item}
{num_discounted_items_var} = {total_quantity} // {discount_frequency}

# Total cost calculation
# Full-priced items
full_price_cost = ({total_quantity} - {num_discounted_items_var}) * {initial_price}
# Discounted items
discounted_price_cost = {num_discounted_items_var} * {discounted_price_var}

{total_cost_var} = full_price_cost + discounted_price_cost

result = {total_cost_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"The discounted price of one {item} is {discount_ratio*100:.0f}% of ${initial_price} = ${round(discount_ratio*initial_price, 2)}. "
    solution_wocode += f"If every {ordinal(discount_frequency)} {item} is cheaper, that means {name} is going to buy {total_quantity} // {discount_frequency} = "
    solution_wocode += f"{total_quantity // discount_frequency} discounted {item}. "
    solution_wocode += f"So, for the discounted {item}, {name} is going to pay {total_quantity // discount_frequency} * ${round(discount_ratio*initial_price, 2)} = "
    solution_wocode += f"${round((total_quantity // discount_frequency) * (discount_ratio*initial_price), 2)}. "
    solution_wocode += f"And for the regular-priced {item}, {name} will pay ({total_quantity} - {total_quantity // discount_frequency}) * ${initial_price} = "
    solution_wocode += f"${round((total_quantity - (total_quantity // discount_frequency)) * initial_price, 2)}. "
    solution_wocode += f"In total, {name} needs to pay ${round((total_quantity - (total_quantity // discount_frequency)) * initial_price, 2)} + "
    solution_wocode += f"${round((total_quantity // discount_frequency) * (discount_ratio*initial_price), 2)} = ${round(result, 2)} for the {item} they want to buy."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    while True:
        # Randomly generate initial price
        initial_price = random.randint(1, 1000)

        # Randomly generate discount ratio
        discount_ratio = round(random.uniform(0.1, 0.9), 2)

        # Randomly generate total quantity
        total_quantity = random.randint(2, 100)

        # Set discount frequency (e.g., every second, third, etc. item)
        discount_frequency = random.randint(2, 10)

        return initial_price, discount_ratio, total_quantity, discount_frequency

def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-6-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
 