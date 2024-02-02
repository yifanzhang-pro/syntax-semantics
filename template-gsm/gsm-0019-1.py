# Origin problem: {"question": "Tim rides his bike back and forth to work for each of his 5 workdays.  His work is 20 miles away.  He also goes for a weekend bike ride of 200 miles.    If he can bike at 25 mph how much time does he spend biking a week?", "answer": "He bikes 20*2=<<20*2=40>>40 miles each day for work\nSo he bikes 40*5=<<40*5=200>>200 miles for work\nThat means he bikes a total of 200+200=<<200+200=400>>400 miles for work\nSo he bikes a total of 400/25=<<400/25=16>>16 hours\n#### 16"}


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
    activity = random.choice(['running', 'swimming', 'driving'])
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get parameters for distance and time
    distance_to_destination, days, extra_activity_distance, speed = get_params_combination()

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    activity_var = activity.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement
    problem_statement = f"{name} is {activity} back and forth to a {item} for each of {days} days. "
    problem_statement += f"The {item} is {distance_to_destination} miles away. "
    problem_statement += f"They also go for an extra {activity} of {extra_activity_distance} miles. "
    problem_statement += f"If they can {activity} at {speed} mph, how much time do they spend {activity} in a week?"

    # Generate solution code
    daily_distance_var = f"daily_{activity_var}_distance"
    total_weekly_distance_var = f"total_weekly_{activity_var}_distance"
    time_spent_var = f"time_spent_{activity_var}"

    solution_code = f"""# Distance {name} {activity} each day to the {item}
{daily_distance_var} = {distance_to_destination} * 2

# Total distance {activity} for work in a week
total_work_distance = {daily_distance_var} * {days}

# Total distance {activity} including extra activity
{total_weekly_distance_var} = total_work_distance + {extra_activity_distance}

# Total time spent {activity} in a week
{time_spent_var} = {total_weekly_distance_var} / {speed}

result = {time_spent_var}
"""

    # Execute the solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 0))

    # Generate the solution without code
    solution_wocode = f"{name} {activity} {distance_to_destination*2} miles each day to the {item}. "
    solution_wocode += f"So they {activity} {distance_to_destination*2*days} miles for work. "
    solution_wocode += f"That means they {activity} a total of {distance_to_destination*2*days + extra_activity_distance} miles in a week. "
    solution_wocode += f"So they spend a total of {distance_to_destination*2*days + extra_activity_distance} / {speed} = {int(result)} hours {activity} in a week."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate parameters
        distance_to_destination = random.randint(1, 50) # distance in miles
        days = random.randint(1, 7) # number of days
        extra_activity_distance = random.randint(0, 100) # extra activity distance in miles
        speed = random.randint(1, 30) # speed in mph

        # Check if the total distance results in an integer time
        total_distance = (distance_to_destination * 2 * days) + extra_activity_distance
        time = total_distance / speed
        if time == int(time):
            return distance_to_destination, days, extra_activity_distance, speed


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0019-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0019-1", "idx": i}) + '\n')
