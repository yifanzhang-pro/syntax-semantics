# [Instruction]: Here comes a problem template, Can you compose a new problem template which has exactly the same reasoning structure of this new origin problem?

### Example origin problem 
{
    "question": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?", 
    "answer": "Natalia sold 48/2 = <<48/2=24>>24 clips in May.\nNatalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May.\n#### 72"
}

### Example problem template
```python
# Origin problem: {"question": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. 
#   How many clips did Natalia sell altogether in April and May?", 
#   "answer": "Natalia sold 48/2 = <<48/2=24>>24 clips in May.\nNatalia sold 48+24 = <<48+24=72>>72 clips altogether 
#   in April and May.\n#### 72"}


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
    months = ["January and February", "Februray and March", "March and April", "April and May", "May and June", "June and July", "July and August", "August and September", "September and October", "October and November", "November and December", "December and January"]

    # Get initial amount and subsequent ratio that ensure an integer result
    initial_amount, subsequent_ratio = get_params_combination()
    
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    month = random.choice(months)
    year = random.randint(2003, 2023)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')

    # Construct problem statement with specific details
    problem_statement = f"{name} sold {initial_amount} {item} in {month.split(' and ')[0]}, {year} at {place} in {county}. "
    problem_statement += f"In {month.split(' and ')[1]}, they sold {subsequent_ratio*100:.0f}% of the amount sold in the previous month. "
    problem_statement += f"How many {item} did {name} sell in total during {month}?"

    # Generate solution code with specific variable names and comments
    sales_var = f"{item.replace(' ', '_')}_sold_in_{month.split(' ')[0]}"
    ratio_var = f"{item.replace(' ', '_')}_ratio"
    total_var = f"total_{item.replace(' ', '_')}"

    solution_code = f"""# Number of {item} sold by {name} in {month.split(' and ')[0]}, {year}
{sales_var} = {initial_amount}

# Sales ratio for the next month
{ratio_var} = {subsequent_ratio}

# Calculating the amount of {item} sold in {month.split(' and ')[1]}
# by applying the ratio to the initial sales
subsequent_{sales_var} = {sales_var} * {ratio_var}

# Calculating the total number of {item} sold during {month} at {place} in {county}
{total_var} = {sales_var} + subsequent_{sales_var}

result = {total_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'], 2)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"{name} sold {initial_amount} {item} in {month.split(' and ')[0]}, {year} at {place} in {county}. "
    solution_wocode += f"In {month.split(' and ')[1]}, they sold {subsequent_ratio*100:.0f}% of the amount sold in the previous month. "
    solution_wocode += f"{name} sold {round(subsequent_ratio*initial_amount, 2)} {item} in {month.split(' and ')[1]}. "
    solution_wocode += f"In total, {name} sold {initial_amount} + {round(subsequent_ratio*initial_amount, 2)} = {round(result, 2)} {item} during {month}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial amount
        initial_amount = random.randint(5, 5000000)

        # Randomly generate subsequent ratio
        subsequent_ratio = round(random.uniform(0.5, 9.5), 2)

        # Calculate the product
        product = initial_amount * subsequent_ratio

        # Check if the product is close to an integer
        if math.isclose(product, round(product), rel_tol=1e-15):
            return initial_amount, subsequent_ratio


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    # output jsonl file
    with open(f'./output/gsm-1-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
```

# [Instruction]: Can you compose a new problem template which has exactly the same reasoning structure of this new origin problem? You need to utilized predefined variable lists first_names, last_names, items, places, us_counties. **You only need to write down the function generate_problem_and_solution_code() and get_params_combination()**, I suggest you to get integer params. Your problem and answer should be in the same distribution as GSM8K (Karl Cobbe et al., 2021).

<system>
Requirement:
1. YOU MUST UTILIZE predefined variable lists first_names, last_names, items, places, us_counties. (name, item, place and county may contain blanks ' ', you need to replace it with '_" in as *_var term in the "solution_code" field)
2. YOU MUST NOT PERFORM round(*, 2) in the "solution_code" field.
3. DO NOT USE `//` IN THE "solution_code" field.
4. REMEMBER TO `exec(solution_code, {}, exec_globals)`.
5. YOU MUST PERFORM round(*, 2) in the "solution_wocode" field.
6. In the get_params_combination() functions, Select integer parameters to ensure calculations result in integer values.
</system>

### New origin problem 
{
    "question": "Jill gets paid $20 per hour to teach and $30 to be a cheerleading coach. If she works 50 weeks a year, 35 hours a week as a teacher and 15 hours a week as a coach, what's her annual salary?", 
    "answer": "First find the total amount Jill makes per week teaching: $20/hour * 35 hours/week = $<<20*35=700>>700/week\nThen find the total amount Jill makes per week coaching: $30/hour * 15 hours/week = $<<30*15=450>>450/week\nThen add those two amounts to find the total amount Jill makes per week: $700/week + $450/week = $<<700+450=1150>>1150/week\nThen multiply that number by the number of weeks Jill works in a year to find her annual salary: $1150/week * 50 weeks/year = $<<1150*50=57500>>57,500\n#### 57500"
}

### Analysis and Reasoning

[to be generated]

### New problem template

[to be generated]
