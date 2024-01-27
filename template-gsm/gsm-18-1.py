# Origin problem: {"question": "Jill gets paid $20 per hour to teach and $30 to be a cheerleading coach. If she works 50 weeks a year, 35 hours a week as a teacher and 15 hours a week as a coach, what's her annual salary?", "answer": "First find the total amount Jill makes per week teaching: $20/hour * 35 hours/week = $<<20*35=700>>700/week\nThen find the total amount Jill makes per week coaching: $30/hour * 15 hours/week = $<<30*15=450>>450/week\nThen add those two amounts to find the total amount Jill makes per week: $700/week + $450/week = $<<700+450=1150>>1150/week\nThen multiply that number by the number of weeks Jill works in a year to find her annual salary: $1150/week * 50 weeks/year = $<<1150*50=57500>>57,500\n#### 57500"}
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
    item1 = random.choice(items)
    item2 = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get pay rates and hours
    pay_rate1, hours1, pay_rate2, hours2, weeks = get_params_combination()

    # Construct problem statement
    problem_statement = f"{name} earns ${pay_rate1} per hour working as a {item1} and ${pay_rate2} per hour as a {item2} at {place} in {county}. "
    problem_statement += f"If {name} works {weeks} weeks a year, {hours1} hours a week for {item1} and {hours2} hours a week for {item2}, what's their annual salary?"

    # Generate solution code
    salary_var1 = f"{item1.replace(' ', '_')}_salary"
    salary_var2 = f"{item2.replace(' ', '_')}_salary"
    annual_salary_var = "annual_salary"

    solution_code = f"""# Salary for working as {item1}
{salary_var1} = {pay_rate1} * {hours1}

# Salary for working as {item2}
{salary_var2} = {pay_rate2} * {hours2}

# Weekly salary
weekly_salary = {salary_var1} + {salary_var2}

# Calculating annual salary
{annual_salary_var} = weekly_salary * {weeks}

result = {annual_salary_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['result']

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} earns ${pay_rate1} per hour working as a {item1} and ${pay_rate2} per hour as a {item2} at {place} in {county}. "
    solution_wocode += f"Weekly, {name} earns ${pay_rate1*hours1} from {item1} and ${pay_rate2*hours2} from {item2}, totaling ${pay_rate1*hours1 + pay_rate2*hours2}. "
    solution_wocode += f"Annually, this amounts to ${round((pay_rate1*hours1 + pay_rate2*hours2) * weeks, 2)}."

    return problem_statement, solution_code, result, solution_wocode

def get_params_combination():
    # Randomly generate hourly rates and hours
    pay_rate1 = random.randint(10, 100)
    hours1 = random.randint(1, 40)
    pay_rate2 = random.randint(10, 100)
    hours2 = random.randint(1, 40)

    # Randomly generate number of weeks worked per year
    weeks = random.randint(1, 52)

    return pay_rate1, hours1, pay_rate2, hours2, weeks


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-18-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
