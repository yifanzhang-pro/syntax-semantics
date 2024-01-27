# Origin problem: {"question": "Raymond and Samantha are cousins. Raymond was born 6 years before Samantha. Raymond had a son at the age of 23. If Samantha is now 31, how many years ago was Raymond's son born?", "answer": "When Raymond's son was born Samantha was 23 - 6 = <<23-6=17>>17 years old.\nThus it has been 31 - 17 = <<31-17=14>>14 years since Raymond's son was born.\n#### 14"}

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
    # Randomly select names, places, and items
    name1 = random.choice(first_names) + ' ' + random.choice(last_names)
    name2 = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)

    # Convert names and item for variable usage
    name1_var = name1.replace(' ', '_')
    name2_var = name2.replace(' ', '_')
    item_var = item.replace(' ', '_')

    # Get initial age difference and other parameters ensuring integer results
    age_difference, event_age, current_age = get_params_combination()

    # Construct problem statement
    problem_statement = f"{name1} and {name2} are friends. {name1} was born {age_difference} years before {name2}. "
    problem_statement += f"{name1} bought a {item} at the age of {event_age}. If {name2} is now {current_age}, "
    problem_statement += f"how many years ago did {name1} buy the {item}?"

    # Variable names for solution code
    event_age_var = f"{name1_var}_age_at_purchase"
    years_since_event_var = f"years_since_{name1_var}_bought_{item_var}"

    # Generate solution code
    solution_code = f"""# Age of {name1} at the time of the purchase
{event_age_var} = {event_age}

# Calculating how many years ago {name1} bought the {item}
{years_since_event_var} = {current_age} - ({event_age_var} - {age_difference})

result = {years_since_event_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate solution without code
    solution_wocode = f"When {name1} bought the {item}, {name2} was {event_age - age_difference} years old. "
    solution_wocode += f"Thus, it has been {current_age - (event_age - age_difference)} years since {name1} bought the {item}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    # Generating parameters ensuring integer results
    while True:
        age_difference = random.randint(1, 20)
        event_age = random.randint(age_difference + 1, 100)
        current_age = random.randint(event_age, 100)

        if event_age - age_difference > 0:
            return age_difference, event_age, current_age



parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0021-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
