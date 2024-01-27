# Origin problem: {"question": "Carla is downloading a 200 GB file. Normally she can download 2 GB/minute, but 40% of the way through the download, Windows forces a restart to install updates, which takes 20 minutes. Then Carla has to restart the download from the beginning. How load does it take to download the file?", "answer": "First find how many gigabytes are in 40% of the file: 200 GB * 40% = <<200*40*.01=80>>80 GB\nThen divide that number by the download rate to find the time until Windows restarts: 80 GB / 2 GB/minute = <<80/2=40>>40 minutes\nThen find the time to download the whole file after the restart: 200 GB / 2 GB/minute = <<200/2=100>>100 minutes\nThen add the time to download 40% of the file, to download the whole file, and to wait for Windows to update: 40 minutes + 100 minutes + 20 minutes = <<40+100+20=160>>160 minutes\n#### 160"}


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

    # Problem-specific variables
    total_amount = random.randint(100, 1000)  # total amount of a task (e.g., pages to read)
    rate = random.randint(1, 20)  # fixed rate of completion (e.g., pages per hour)
    interruption_percentage = random.choice([10, 20, 30, 40, 50])  # interruption point as a percentage
    interruption_duration = random.randint(10, 60)  # duration of interruption in minutes

    # Construct problem statement
    problem_statement = (f"{name} needs to complete a task of {total_amount} {item} at {place} in {county}. "
                         f"Normally, they can do {rate} {item}/hour, but {interruption_percentage}% of the way through, "
                         f"an interruption occurs for {interruption_duration} minutes. "
                         f"Then {name} has to restart the task from the beginning. "
                         f"How long does it take to complete the task?")

    # Generate solution code
    solution_code = (f"completed_at_interruption = {total_amount} * {interruption_percentage} / 100\n"
                     f"time_until_interruption = completed_at_interruption / {rate}\n"
                     f"time_to_complete_after_interruption = {total_amount} / {rate}\n"
                     f"total_time = time_until_interruption + {interruption_duration} / 60 + "  # convert minutes to hours
                     f"time_to_complete_after_interruption")

    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['total_time'], 2)

    # Generate the solution without code
    solution_wocode = (f"{name} first completes {round(interruption_percentage, 2)}% of the {total_amount} {item}, "
                       f"which is {round(exec_globals['completed_at_interruption'], 2)} {item}. "
                       f"This takes {round(exec_globals['time_until_interruption'], 2)} hours. "
                       f"After the interruption of {round(interruption_duration, 2)} minutes, "
                       f"it takes an additional {round(exec_globals['time_to_complete_after_interruption'], 2)} hours to complete the task. "
                       f"In total, it takes {result} hours.")

    return problem_statement, solution_code, result, solution_wocode


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0007-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
