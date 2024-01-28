# Origin problem: {"question": "Marissa is hiking a 12-mile trail. She took 1 hour to walk the first 4 miles, then another hour to walk the next two miles. If she wants her average speed to be 4 miles per hour, what speed (in miles per hour) does she need to walk the remaining distance?", "answer": "First figure out how many hours it takes to hike a 12-mile trail at 4 mph by dividing the distance by the speed: 12 miles / 4 mph = <<12/4=3>>3 hours\nNext subtract the time Marissa already spent walking to find out how much time she has left: 3 hours - 1 hour - 1 hour = <<3-1-1=1>>1 hour\nNow figure out how much distance she has left by subtracting the distance she already traveled from the total distance: 12 miles - 4 miles - 2 miles = <<12-4-2=6>>6 miles\nNow divide the remaining distance by the remaining time to find out how fast in miles per hour Marissa has to travel: 6 miles / 1 hour = <<6/1=6>>6 mph\n#### 6"}


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
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]
    item = random.choice(items)

    # Get initial distance, segment distances, times, and desired average speed
    total_distance, segment_distances, segment_times, desired_avg_speed = get_params_combination()
    
    # Construct the problem statement
    problem_statement = f"{name} is driving a total of {total_distance} miles to deliver {item} to {place} in {county}. "
    problem_statement += f"They drove the first {segment_distances[0]} miles in {segment_times[0]} hours, "
    problem_statement += f"and then another {segment_distances[1]} miles in {segment_times[1]} hours. "
    problem_statement += f"If they want their average speed to be {desired_avg_speed} miles per hour, "
    problem_statement += f"what speed (in miles per hour) do they need to drive the remaining distance?"

    # Generate solution code
    total_time = f"{total_distance} / {desired_avg_speed}"
    time_spent = f"{segment_times[0]} + {segment_times[1]}"
    remaining_time = f"{total_time} - {time_spent}"
    distance_travelled = f"{segment_distances[0]} + {segment_distances[1]}"
    remaining_distance = f"{total_distance} - {distance_travelled}"
    required_speed = f"{remaining_distance} / {remaining_time}"

    solution_code = f"""# Calculate total time for desired average speed
total_time = {total_distance} / {desired_avg_speed}

# Calculate time already spent
time_spent = {segment_times[0]} + {segment_times[1]}

# Calculate remaining time
remaining_time = total_time - time_spent

# Calculate distance already traveled
distance_travelled = {segment_distances[0]} + {segment_distances[1]}

# Calculate remaining distance
remaining_distance = {total_distance} - distance_travelled

# Calculate required speed for remaining distance
required_speed = remaining_distance / remaining_time

result = required_speed
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"To achieve an average speed of {desired_avg_speed} mph over {total_distance} miles, "
    solution_wocode += f"{name} must drive the remaining distance at a speed of {round(result, 2)} mph."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    while True:
        total_distance = random.randint(20, 500)  # Total distance in miles
        segment_distances = [random.randint(5, total_distance // 3), random.randint(5, total_distance // 3)]
        segment_times = [random.randint(1, 5), random.randint(1, 5)]  # Time taken for each segment in hours
        desired_avg_speed = random.randint(10, 100)  # Desired average speed in mph

        total_time_for_desired_speed = total_distance / desired_avg_speed
        time_already_spent = sum(segment_times)

        # Ensure remaining time is positive
        if total_distance > sum(segment_distances) and desired_avg_speed > 0 and total_time_for_desired_speed > time_already_spent:
            return total_distance, segment_distances, segment_times, desired_avg_speed


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-test-0019-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
