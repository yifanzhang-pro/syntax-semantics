# Origin problem: {"question": "Two trains leave San Rafael at the same time. They begin traveling westward, both traveling for 80 miles. The next day, they travel northwards, covering 150 miles. What's the distance covered by each train in the two days?", "answer": "On the first day, the trains covered 2 trains * 80 miles/train = <<2*80=160>>160 miles together.\nThey also covered 150 miles/train * 2 trains = <<150*2=300>>300 miles together on the second day.\nThe combined distance the two trains covered in the two days is 300 miles + 160 miles = <<300+160=460>>460 miles\nThe average distance for the two days is 460 miles / 2 trains = <<460/2=230>>230 miles/train\n#### 230"}

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
    # Lists of random terms
    directions = ["northward", "southward", "eastward", "westward"]
    
    # Get initial distance and subsequent distance ensuring integer values
    initial_distance, subsequent_distance = get_params_combination()

    # Randomly select terms
    name1 = random.choice(first_names) + ' ' + random.choice(last_names)
    name2 = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    first_direction = random.choice(directions)
    second_direction = random.choice([d for d in directions if d != first_direction])

    # Construct problem statement with specific details
    problem_statement = f"Two {item}-brand cars, one driven by {name1} and another by {name2}, leave {place} in {county}. "
    problem_statement += f"They begin traveling {first_direction}, both traveling for {initial_distance} miles. The next day, they travel {second_direction}, covering {subsequent_distance} miles. "
    problem_statement += f"What's the distance covered by each {item}-brand car in the two days?"

    # Generate solution code with specific variable names and comments
    first_day_distance_var = f"{first_direction}_distance"
    second_day_distance_var = f"{second_direction}_distance"
    total_distance_var = "total_distance_per_car"

    solution_code = f"""# Distance covered by each {item}-brand car on the first day
{first_day_distance_var} = {initial_distance}

# Distance covered by each {item}-brand car on the second day
{second_day_distance_var} = {subsequent_distance}

# Calculating the total distance covered by each {item}-brand car over the two days
{total_distance_var} = {first_day_distance_var} + {second_day_distance_var}

result = {total_distance_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"On the first day, each {item}-brand car covered {initial_distance} miles. "
    solution_wocode += f"On the second day, each car covered {subsequent_distance} miles. "
    solution_wocode += f"The total distance covered by each car over the two days is {initial_distance} miles + {subsequent_distance} miles = {result} miles."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    # Randomly generate initial and subsequent distances ensuring integer values
    initial_distance = random.randint(10, 500)
    subsequent_distance = random.randint(10, 500)
    return initial_distance, subsequent_distance


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-17-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
