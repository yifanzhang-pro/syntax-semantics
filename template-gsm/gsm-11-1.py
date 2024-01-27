# Origin problem: {"question": "A new program had 60 downloads in the first month. The number of downloads in the second month was three times as many as the downloads in the first month, but then reduced by 30% in the third month. How many downloads did the program have total over the three months?", "answer": "The number of downloads of the program in the second month increased to 3*60 = <<3*60=180>>180\nIn the first two months, the total number of downloads of the program was 180+60 = <<180+60=240>>240\nIn the third month, the number of downloads of the program reduced by 30/100*180 = <<30/100*180=54>>54\nThere were 180-54 = <<180-54=126>>126 downloads in the third month.\nIn the three months, the total number of downloads of the program was 126+240 = <<126+240=366>>366\n#### 366"}


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


def generate_problem_and_solution_code():
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    year = random.randint(2003, 2023)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get initial amount, multiplication factor, and percentage reduction
    initial_amount, multiplication_factor, percentage_reduction = get_params_combination()
    
    # Construct problem statement with specific details
    problem_statement = f"{name} produced {initial_amount} units of {item} in the first month of {year} at {place} in {county}. "
    problem_statement += f"In the second month, the production was {multiplication_factor} times the first month's production. "
    problem_statement += f"However, in the third month, the production reduced by {percentage_reduction}% compared to the second month. "
    problem_statement += f"How many units of {item} did {name} produce in total over the three months?"

    # Generate solution code with specific variable names and comments
    first_month_var = f"first_month_{item.replace(' ', '_')}"
    second_month_var = f"second_month_{item.replace(' ', '_')}"
    third_month_var = f"third_month_{item.replace(' ', '_')}"
    total_var = f"total_{item.replace(' ', '_')}"

    solution_code = f"""# Production of {item} by {name} in the first month
{first_month_var} = {initial_amount}

# Production in the second month as a multiple of the first month
{second_month_var} = {first_month_var} * {multiplication_factor}

# Reduction in production in the third month
reduction = {second_month_var} * ({percentage_reduction} / 100)

# Production in the third month after reduction
{third_month_var} = {second_month_var} - reduction

# Total production over the three months
{total_var} = {first_month_var} + {second_month_var} + {third_month_var}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"In the first month, {name} produced {initial_amount} units of {item}. "
    solution_wocode += f"In the second month, production increased to {multiplication_factor} times the first month's, totaling {initial_amount * multiplication_factor} units. "
    solution_wocode += f"In the third month, production reduced by {round(percentage_reduction / 100 * initial_amount * multiplication_factor, 2)} units (i.e., {percentage_reduction}% of the second month's production), resulting in {round(initial_amount * multiplication_factor * (1 - percentage_reduction / 100), 2)} units. "
    solution_wocode += f"Overall, {name} produced {round(result, 2)} units of {item} over the three months."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    # Randomly generate initial amount, multiplication factor, and percentage reduction
    initial_amount = random.randint(5, 10000)
    multiplication_factor = random.randint(2, 10)
    percentage_reduction = random.randint(10, 50)

    return initial_amount, multiplication_factor, percentage_reduction


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True) 
    # output jsonl file
    with open(f'./output/gsm-11-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
