# Origin problem: {"question": "Melanie is a door-to-door saleswoman. She sold a third of her vacuum cleaners at the green house, 2 more to the red house, and half of what was left at the orange house. If Melanie has 5 vacuum cleaners left, how many did she start with?", "answer": "First multiply the five remaining vacuum cleaners by two to find out how many Melanie had before she visited the orange house: 5 * 2 = <<5*2=10>>10\nThen add two to figure out how many vacuum cleaners she had before visiting the red house: 10 + 2 = <<10+2=12>>12\nNow we know that 2/3 * x = 12, where x is the number of vacuum cleaners Melanie started with. We can find x by dividing each side of the equation by 2/3, which produces x = 18\n#### 18"}


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

    # Define initial total and subsequent percentages
    initial_total, first_percentage, second_percentage = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"In a {item} competition organized by {name} in {place} in {county}, there were {initial_total} participants. "
    problem_statement += f"{first_percentage}% of them participated in the first category, "
    problem_statement += f"{second_percentage}% of the remaining participated in the second category, and the rest in the final category. "
    problem_statement += f"What percentage of the total participants were in the final category?"

    # Generate solution code with specific variable names and comments
    first_category_var = f"first_category_{item.replace(' ', '_')}"
    second_category_var = f"second_category_{item.replace(' ', '_')}"
    final_category_var = f"final_category_{item.replace(' ', '_')}"

    # Calculate variables for solution without code
    first_category = initial_total * first_percentage / 100
    remaining_after_first = initial_total - first_category
    second_category = remaining_after_first * second_percentage / 100
    final_category = remaining_after_first - second_category
    final_category_percentage = final_category / initial_total * 100

    solution_code = f"""# Number of participants in the first category
{first_category_var} = {initial_total} * {first_percentage} / 100

# Remaining participants after the first category
remaining_after_first = {initial_total} - {first_category_var}

# Number of participants in the second category
{second_category_var} = remaining_after_first * {second_percentage} / 100

# Remaining participants in the final category
{final_category_var} = remaining_after_first - {second_category_var}

# Percentage of total participants in the final category
final_category_percentage = {final_category_var} / {initial_total} * 100

result = {final_category_percentage}
"""

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"In the {item} competition, there were {round(first_category, 2)} participants in the first category. "
    solution_wocode += f"So, {initial_total} - {round(first_category, 2)} = {round(remaining_after_first, 2)} participants were in either the second or the final category. "
    solution_wocode += f"{round(second_category, 2)} participants were in the second category. "
    solution_wocode += f"Hence, {round(remaining_after_first, 2)} - {round(second_category, 2)} = {round(final_category, 2)} participants were in the final category. "
    solution_wocode += f"This is {round(final_category_percentage, 2)}% of the total participants."

    return problem_statement, solution_code, round(final_category_percentage, 2), solution_wocode


def get_params_combination():
    # Randomly generate initial total, first percentage, and second percentage
    initial_total = random.randint(10, 500)
    first_percentage = random.randint(5, 30)
    second_percentage = random.randint(10, 40)

    return initial_total, first_percentage, second_percentage


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-15-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
