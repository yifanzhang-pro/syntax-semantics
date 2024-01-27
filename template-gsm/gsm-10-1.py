# Origin problem: {"question": "Eliza's rate per hour for the first 40 hours she works each week is $10. She also receives an overtime pay of 1.2 times her regular hourly rate. If Eliza worked for 45 hours this week, how much are her earnings for this week?", "answer": "Eliza is entitled to 45 -40 = <<45-40=5>>5 hours overtime pay.\nHer hourly rate for the overtime pay is $10 x 1.2 = $<<10*1.2=12>>12.\nSo, Eliza will receive $12 x 5 =$<<12*5=60>>60 for overtime pay.\nHer regular weekly earning is $10 x 40 = $<<10*40=400>>400.\nThus, Eliza will receive a total of $400 + $60 = $<<400+60=460>>460 for this week's work.\n#### 460"}


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

    # Get initial rate, standard hours, and multiplier for overtime
    hourly_rate, standard_hours, overtime_multiplier = get_params_combination()
    
    # Random number of total hours worked
    total_hours_worked = random.randint(standard_hours, standard_hours + 10)

    # Construct problem statement with specific details
    problem_statement = f"{name} earns ${hourly_rate} per hour for the first {standard_hours} hours working as a {item} at {place} in {county}. "
    problem_statement += f"They also receive an overtime pay of {overtime_multiplier} times their regular hourly rate. "
    problem_statement += f"If {name} worked for {total_hours_worked} hours this week, how much are their earnings for this week?"

    # Generate solution code with specific variable names and comments
    overtime_hours = f"overtime_hours_{item.replace(' ', '_')}"
    overtime_pay_rate = f"overtime_pay_rate_{item.replace(' ', '_')}"
    overtime_pay = f"overtime_pay_{item.replace(' ', '_')}"
    regular_pay = f"regular_pay_{item.replace(' ', '_')}"
    total_earnings = f"total_earnings_{item.replace(' ', '_')}"

    solution_code = f"""# Calculating overtime hours
{overtime_hours} = max({total_hours_worked} - {standard_hours}, 0)

# Calculating the overtime pay rate
{overtime_pay_rate} = {hourly_rate} * {overtime_multiplier}

# Calculating the overtime pay
{overtime_pay} = {overtime_hours} * {overtime_pay_rate}

# Calculating the regular pay
{regular_pay} = min({total_hours_worked}, {standard_hours}) * {hourly_rate}

# Calculating the total earnings
{total_earnings} = {regular_pay} + {overtime_pay}

result = round({total_earnings}, 2)
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} is entitled to {total_hours_worked} - {standard_hours} = <<{total_hours_worked}-{standard_hours}={exec_globals[overtime_hours]}>>{exec_globals[overtime_hours]} hours overtime pay. "
    solution_wocode += f"Their hourly rate for the overtime pay is ${hourly_rate} x {overtime_multiplier} = $<<{hourly_rate}*{overtime_multiplier}={exec_globals[overtime_pay_rate]}>>{exec_globals[overtime_pay_rate]}. "
    solution_wocode += f"So, {name} will receive ${exec_globals[overtime_pay_rate]} x {exec_globals[overtime_hours]} = $<<{exec_globals[overtime_pay_rate]}*{exec_globals[overtime_hours]}={exec_globals[overtime_pay]}>>{exec_globals[overtime_pay]} for overtime pay. "
    solution_wocode += f"Their regular weekly earning is ${hourly_rate} x {standard_hours} = $<<{hourly_rate}*{standard_hours}={exec_globals[regular_pay]}>>{exec_globals[regular_pay]}. "
    solution_wocode += f"Thus, {name} will receive a total of ${exec_globals[regular_pay]} + ${exec_globals[overtime_pay]} = $<<{exec_globals[regular_pay]}+{exec_globals[overtime_pay]}={result}>>{result} for this week's work.\n#### {result}"

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    # Randomly generate hourly rate, standard hours, and overtime multiplier
    hourly_rate = random.randint(8, 50)
    standard_hours = random.randint(35, 45)
    overtime_multiplier = round(random.uniform(1.1, 2.0), 1)

    return hourly_rate, standard_hours, overtime_multiplier


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-10-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
