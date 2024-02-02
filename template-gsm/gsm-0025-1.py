# Origin problem: {"question": "Ralph is going to practice playing tennis with a tennis ball machine that shoots out tennis balls for Ralph to hit. He loads up the machine with 175 tennis balls to start with. Out of the first 100 balls, he manages to hit 2/5 of them. Of the next 75 tennis balls, he manages to hit 1/3 of them. Out of all the tennis balls, how many did Ralph not hit?", "answer": "Out of the first 100 balls, Ralph was able to hit 2/5 of them and not able to hit 3/5 of them, 3/5 x 100 = 60 tennis balls Ralph didn't hit.\nOut of the next 75 balls, Ralph was able to hit 1/3 of them and not able to hit 2/3 of them, 2/3 x 75 = 50 tennis balls that Ralph didn't hit.\nCombined, Ralph was not able to hit 60 + 50 = <<60+50=110>>110 tennis balls Ralph didn't hit.\n#### 110"}


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
    activities = ["reading books", "painting pictures", "completing puzzles", "baking cakes", "planting trees", "writing poems", "building models", "solving riddles"]
    achievements = ["finished", "completed", "solved", "baked", "planted", "wrote", "built", "solved"]
    failures = ["left unfinished", "not completed", "unsolved", "not baked", "not planted", "not written", "not built", "unsolved"]

    # Get initial amounts and fractions to ensure integer results
    initial_amount, fraction_hit, fraction_miss = get_params_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    activity = random.choice(activities)
    achievement = achievements[activities.index(activity)]
    failure = failures[activities.index(activity)]
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"{name} started {activity} with {initial_amount} {item} at {place} in {county}. "
    problem_statement += f"Of the first half, {name} {achievement} {round(fraction_hit*100)}% of them but {failure} the rest. "
    problem_statement += f"Of the second half, {name} {achievement} {round(fraction_miss*100)}% of them. "
    problem_statement += f"How many {item} did {name} {failure} in total?"

    # Generate solution code with specific variable names and comments
    total_items_var = f"total_{item_var}"
    hit_first_half_var = f"hit_first_half_{item_var}"
    miss_first_half_var = f"miss_first_half_{item_var}"
    miss_second_half_var = f"miss_second_half_{item_var}"
    total_miss_var = f"total_miss_{item_var}"

    solution_code = f"""# Total number of {item} {name} started with
{total_items_var} = {initial_amount}

# Number of {item} {name} {achievement} in the first half
{hit_first_half_var} = {total_items_var} / 2 * {fraction_hit}

# Number of {item} {name} {failure} in the first half
{miss_first_half_var} = {total_items_var} / 2 - {hit_first_half_var}

# Number of {item} {name} {failure} in the second half
{miss_second_half_var} = {total_items_var} / 2 * {1 - fraction_miss}

# Total number of {item} {name} {failure}
{total_miss_var} = {miss_first_half_var} + {miss_second_half_var}

result = {total_miss_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 0))

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} started {activity} with {initial_amount} {item} at {place} in {county}. "
    solution_wocode += f"Of the first half, {name} {achievement} {int(fraction_hit*100)}% of them but {failure} {int((1 - fraction_hit) * initial_amount / 2)} {item}. "
    solution_wocode += f"Of the second half, {name} {failure} {int(fraction_miss * initial_amount / 2)} {item}. "
    solution_wocode += f"In total, {name} {failure} {int(round((1 - fraction_hit) * initial_amount / 2 + (1 - fraction_miss) * initial_amount / 2, 0))} {item}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial amount (even number to divide into two halves)
        initial_amount = random.randint(10, 500) * 2

        # Randomly generate fractions for first and second half (ensuring integer results)
        fraction_hit = random.choice([i / 10 for i in range(1, 10)])
        fraction_miss = random.choice([i / 10 for i in range(1, 10)])

        if (initial_amount / 2 * fraction_hit).is_integer() and (initial_amount / 2 * fraction_miss).is_integer():
            return initial_amount, fraction_hit, fraction_miss


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0025-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0025-1", "idx": i}) + '\n')
