# Origin problem: {"question": "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?", 
#  "answer": "Weng earns 12/60 = $<<12/60=0.2>>0.2 per minute.\nWorking 50 minutes, she earned 0.2 x 50 = $<<0.2*50=10>>10.\n#### 10"}


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


import random
import math

def get_hourly_rate_and_minutes():
    # Randomly generate hourly rate
    hourly_rate = random.randint(10, 100)

    # Randomly generate minutes worked
    minutes_worked = random.randint(10, 120)

    return hourly_rate, minutes_worked

def generate_problem_and_solution_code():
    # Lists of random terms
    jobs = ["babysitting", "tutoring", "gardening", "dog walking", "house cleaning"]

    # Get hourly rate and minutes worked
    hourly_rate, minutes_worked = get_hourly_rate_and_minutes()

    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    job = random.choice(jobs)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} earns ${hourly_rate} an hour for {job}. "
    problem_statement += f"Yesterday, they did {minutes_worked} minutes of {job} at {place} of {county}. "
    problem_statement += f"How much did {name} earn?"

    # Generate solution code with specific variable names and comments
    hourly_rate_var = f"{job.replace(' ', '_')}_hourly_rate"
    minutes_var = f"{job.replace(' ', '_')}_minutes_worked"
    earnings_var = f"{name.replace(' ', '_')}_earnings"

    solution_code = f"""# Hourly rate for {job} by {name}
{hourly_rate_var} = {hourly_rate}

# Minutes worked by {name} in {job}
{minutes_var} = {minutes_worked}

# Calculating earnings based on the hourly rate and minutes worked
earnings_per_minute = {hourly_rate_var} / 60
{earnings_var} = earnings_per_minute * {minutes_var}

result = {earnings_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} earns ${hourly_rate}/60 = ${hourly_rate/60:.2f} per minute.\n"
    solution_wocode += f"Working {minutes_worked} minutes, {name} earned ${hourly_rate/60:.2f} x {minutes_worked} = ${result}.\n"
    solution_wocode += f"#### {result}"

    return problem_statement, solution_code, result, solution_wocode




parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-2-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result)}) + '\n')
