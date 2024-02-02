# Origin problem: {"question": "Samantha\u2019s last name has three fewer letters than Bobbie\u2019s last name. If Bobbie took two letters off her last name, she would have a last name twice the length of Jamie\u2019s. Jamie\u2019s full name is Jamie Grey. How many letters are in Samantha\u2019s last name?", "answer": "There are 4 letters in Jamie\u2019s last name, so Bobbie\u2019s name is 4*2 +2 = <<4*2+2=10>>10 letters long.\nSamantha\u2019s last name is 3 letters shorter than Bobbie\u2019s, so there are 10 - 3 = <<10-3=7>>7 letters in Samantha\u2019s last name.\n#### 7"}


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
    # Randomly select names and places
    person1 = random.choice(first_names)
    person2 = random.choice(first_names)
    person3 = random.choice(first_names)
    last_name1 = random.choice(last_names)
    last_name3 = random.choice(last_names)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    person1_var = person1.replace(' ', '_')
    person2_var = person2.replace(' ', '_')
    person3_var = person3.replace(' ', '_')
    last_name1_var = last_name1.replace(' ', '_')
    last_name3_var = last_name3.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Get initial amount and subsequent ratio
    last_name1_length, difference = get_params_combination()
    last_name3_length = len(last_name3)

    # Construct problem statement
    problem_statement = f"{person1}'s last name has {difference} fewer letters than {person2}'s last name. "
    problem_statement += f"If {person2} removed two letters from their last name, they would have a last name twice the length of {person3} {last_name3}. "
    problem_statement += f"How many letters are in {person1}'s last name?"

    # Generate solution code
    solution_code = f"""# Length of {person3}'s last name
{last_name3_var}_length = {last_name3_length}

# Length of {person2}'s last name calculated from {person3}'s last name
{person2_var}_last_name_length = 2 * {last_name3_var}_length + 2

# Length of {person1}'s last name
{person1_var}_last_name_length = {person2_var}_last_name_length - {difference}

result = {person1_var}_last_name_length
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code
    solution_wocode = f"There are {last_name3_length} letters in {person3} {last_name3}'s last name, "
    solution_wocode += f"so {person2}'s last name is 2*{last_name3_length} + 2 = {2*last_name3_length + 2} letters long. "
    solution_wocode += f"{person1}'s last name is {difference} letters shorter than {person2}'s, "
    solution_wocode += f"so there are {2*last_name3_length + 2 - difference} letters in {person1}'s last name."

    return problem_statement, solution_code, round(result, 2), solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate the length of the first last name
        last_name1_length = random.randint(4, 15)

        # Randomly generate the difference in length
        difference = random.randint(1, 4)

        return last_name1_length, difference


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0022-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0022-1", "idx": i}) + '\n')
