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


def generate_problem_and_solution_code():
    # Lists of random terms
    hourly_rates = [10, 15, 20, 25, 30]  # Hourly rates in dollars

    # Get hourly rate and working time that ensure a solution in whole dollars
    hourly_rate, working_minutes = get_params_combination()

    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    activity = random.choice(items)
    day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} earns ${hourly_rate} an hour for {activity} on {day} at {place} in {county}. "
    problem_statement += f"Yesterday, they did {working_minutes} minutes of {activity}. How much did {name} earn?"

    # Generate solution code with specific variable names and comments
    earnings_per_minute_var = f"earnings_per_minute_for_{activity.replace(' ', '_')}"
    total_earnings_var = f"total_earnings_for_{activity.replace(' ', '_')}"

    solution_code = f"""# Earnings per minute for {activity}
{earnings_per_minute_var} = {hourly_rate} / 60

# Total earnings for {working_minutes} minutes of {activity}
{total_earnings_var} = {earnings_per_minute_var} * {working_minutes}

result = round({total_earnings_var}, 2)
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} earns ${hourly_rate}/60 = ${hourly_rate/60:.2f} per minute for {activity}. "
    solution_wocode += f"Working {working_minutes} minutes, they earned ${hourly_rate/60:.2f} x {working_minutes} = ${result:.2f}. "
    solution_wocode += f"In total, {name} earned ${result:.2f} for {working_minutes} minutes of {activity} on {day}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    while True:
        # Randomly generate hourly rate
        hourly_rate = random.choice([10, 15, 20, 25, 30])

        # Randomly generate working minutes
        working_minutes = random.randint(10, 300)  # Between 10 and 300 minutes

        # Calculate the earnings for the given time
        earnings = (hourly_rate / 60) * working_minutes

        # Check if the earnings are close to an integer (in whole dollars)
        if math.isclose(earnings, round(earnings, 2), rel_tol=1e-15):
            return hourly_rate, working_minutes


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
