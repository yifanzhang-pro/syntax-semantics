# Origin problem: {"question": "John drives for 3 hours at a speed of 60 mph and then turns around because he realizes he forgot something very important at home.  He tries to get home in 4 hours but spends the first 2 hours in standstill traffic.  He spends the next half-hour driving at a speed of 30mph, before being able to drive the remaining time of the 4 hours going at 80 mph.  How far is he from home at the end of those 4 hours?", "answer": "When he turned around he was 3*60=<<3*60=180>>180 miles from home\nHe was only able to drive 4-2=<<4-2=2>>2 hours in the first four hours\nIn half an hour he goes 30*.5=<<30*.5=15>>15 miles\nHe then drives another 2-.5=<<2-.5=1.5>>1.5 hours\nIn that time he goes 80*1.5=<<80*1.5=120>>120 miles\nSo he drove 120+15=<<120+15=135>>135 miles\nSo he is 180-135=<<180-135=45>>45 miles away from home\n#### 45"}

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
    activities = ["reading", "writing", "painting", "coding"]
    time_units = ["hours", "days", "weeks"]

    # Get initial amount and subsequent rates that ensure an integer result
    initial_amount, subsequent_rates = get_params_combination()

    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    activity = random.choice(activities)
    time_unit = random.choice(time_units)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Construct problem statement with specific details
    problem_statement = f"{name} starts {activity} for {initial_amount} {time_unit} in {place} of {county}. "
    problem_statement += f"Afterwards, they encounter different conditions affecting their rate. "
    for rate in subsequent_rates:
        problem_statement += f"They spend the next period of time {activity} at {rate*100:.0f}% of their initial rate. "
    problem_statement += f"How much time does {name} spend {activity} in total?"

    # Generate solution code with specific variable names and comments
    initial_time_var = f"{activity}_initial_time"
    total_time_var = f"total_{activity}_time"

    solution_code = f"""# Initial time spent by {name} {activity}
{initial_time_var} = {initial_amount}

# Total time spent {activity}
{total_time_var} = {initial_time_var}
"""

    for i, rate in enumerate(subsequent_rates, start=1):
        rate_time_var = f"{activity}_rate_{i}_time"
        solution_code += f"""# Time spent {activity} at rate {i}
{rate_time_var} = {initial_time_var} * {rate}
{total_time_var} += {rate_time_var}
"""

    solution_code += f"\nresult = {total_time_var}"

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} spent {initial_amount} {time_unit} {activity} initially. "
    for i, rate in enumerate(subsequent_rates, start=1):
        solution_wocode += f"Then, they spent {round(rate*initial_amount, 2)} {time_unit} {activity} at rate {i}. "
    solution_wocode += f"In total, {name} spent {round(result, 2)} {time_unit} {activity}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    while True:
        # Randomly generate initial amount
        initial_amount = random.randint(1, 10)

        # Randomly generate subsequent rates (2 to 4 rates)
        num_rates = random.randint(2, 4)
        subsequent_rates = [round(random.uniform(0.5, 1.5), 2) for _ in range(num_rates)]

        return initial_amount, subsequent_rates


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-9-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
