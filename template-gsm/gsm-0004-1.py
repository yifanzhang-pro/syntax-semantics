# Origin problem: {"question": "James writes a 3-page letter to 2 different friends twice a week.  How many pages does he write a year?", 
# "answer": "He writes each friend 3*2=<<3*2=6>>6 pages a week\nSo he writes 6*2=<<6*2=12>>12 pages every week\n
# That means he writes 12*52=<<12*52=624>>624 pages a year\n#### 624"}


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
    activity = "writes letters to"
    friend_count = random.randint(1, 5)  # Number of friends
    pages_per_letter = random.randint(1, 10)  # Pages per letter
    letters_per_week = random.randint(1, 7)  # Letters per week
    year = random.randint(2003, 2023)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} {activity} {friend_count} different friends, writing a {pages_per_letter}-page letter to each, {letters_per_week} times a week. "
    problem_statement += f"How many pages does {name} write in a year?"

    # Generate solution code with specific variable names and comments
    pages_var = "pages_written_per_week"
    total_pages_var = "total_pages_per_year"

    solution_code = f"""# Number of pages {name} writes per week
{pages_var} = {pages_per_letter} * {friend_count} * {letters_per_week}

# Calculating the total number of pages written in a year
{total_pages_var} = {pages_var} * 52  # There are 52 weeks in a year

result = {total_pages_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'])

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} writes {pages_per_letter} pages to each of {friend_count} friends, {letters_per_week} times a week. "
    solution_wocode += f"So, {name} writes {pages_per_letter*friend_count} pages each time and {pages_per_letter*friend_count*letters_per_week} pages per week. "
    solution_wocode += f"In a year, {name} writes {pages_per_letter*friend_count*letters_per_week} * 52 = {round(result)} pages."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Prefer integer parameters and ensure numbers have a finite number of digits.
    """
    # This function is not required in the new template as the parameters are straightforward.
    pass


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0004-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
