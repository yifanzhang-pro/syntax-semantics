# Origin problem: {"question": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. 
#   How many clips did Natalia sell altogether in April and May?", 
#   "answer": "Natalia sold 48/2 = <<48/2=24>>24 clips in May.\nNatalia sold 48+24 = <<48+24=72>>72 clips altogether 
#   in April and May.\n#### 72"}


import random
import math
import json
import argparse


def get_integer_combination():
    while True:
        # Randomly generate initial amount
        initial_amount = random.randint(5, 500000)

        # Randomly generate subsequent ratio
        subsequent_ratio = round(random.uniform(0.5, 9.5), 2)

        # Calculate the product
        product = initial_amount * subsequent_ratio

        # Check if the product is close to an integer
        if math.isclose(product, round(product), rel_tol=1e-9):
            return initial_amount, subsequent_ratio


def generate_problem_and_solution_code():
    # Lists of random terms
    names = ["Natalia", "Carlos", "Aisha", "Liam", "Emma", "James", "Fatima", "John"]
    items = ["clips", "cupcakes", "handmade soaps", "notebooks", "scarves", "paintings", "books", "plants"]
    dates = ["January and February", "Februray and March", "March and April", "April and May", "May and June", "June and July", "July and August", "August and September", "September and October", "October and November", "November and December", "December and January"]
    places = ["the city center", "a local market", "an online store", "the neighborhood fair", "the downtown area"]

    # Get initial amount and subsequent ratio that ensure an integer result
    initial_amount, subsequent_ratio = get_integer_combination()
    
    # Randomly select terms
    name = random.choice(names)
    item = random.choice(items)
    date = random.choice(dates)
    place = random.choice(places)

    # Construct problem statement with specific details
    problem_statement = f"{name} sold {initial_amount} {item} in {date.split(' and ')[0]} at {place}. "
    problem_statement += f"In {date.split(' and ')[1]}, they sold {subsequent_ratio*100:.0f}% of the amount sold in the previous month. "
    problem_statement += f"How many {item} did {name} sell in total during {date}?"

    # Generate solution code with specific variable names and comments
    sales_var = f"{item.replace(' ', '_')}_sold_in_{date.split(' ')[0]}"
    ratio_var = f"{item.replace(' ', '_')}_ratio"
    total_var = f"total_{item.replace(' ', '_')}"

    solution_code = f"""# Number of {item} sold by {name} in {date.split(' and ')[0]}
{sales_var} = {initial_amount}

# Sales ratio for the next month
{ratio_var} = {subsequent_ratio}

# Calculating the amount of {item} sold in {date.split(' and ')[1]}
# by applying the ratio to the initial sales
subsequent_{sales_var} = {sales_var} * {ratio_var}

# Calculating the total number of {item} sold during {date}
{total_var} = {sales_var} + subsequent_{sales_var}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(exec_globals['result'])

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} sold {initial_amount} {item} in {date.split(' and ')[0]}. "
    solution_wocode += f"In {date.split(' and ')[1]}, they sold {subsequent_ratio*100:.0f}% of the amount sold in the previous month. "
    solution_wocode += f"{name} sold {int(subsequent_ratio*initial_amount)} {item} in {date.split(' and ')[1]}. "
    solution_wocode += f"In total, {name} sold {initial_amount} + {int(subsequent_ratio*initial_amount)} = {int(result)} {item} during {date}."

    return problem_statement, solution_code, result, solution_wocode


# Generate a problem, its solution code, and the result
# problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
# print("Generated Problem:")
# print(problem)
# print("\nGenerated Solution Code with Comments:")
# print(solution_code)
# print("\nResult of the Solution Code:")
# print(result)
# print("\nGenerated Solution without Code:")
# print(solution_wocode)


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        

if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-1-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "result": str(result), "solution_wocode": solution_wocode}) + '\n')
