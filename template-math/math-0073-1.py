# Origin problem: {"problem": "Solve for $x$: $\\dfrac{1}{2} + \\dfrac{1}{x} = \\dfrac{5}{6}$.", "solution": "Subtracting $\\frac12$ from both sides gives $\\frac1x = \\frac56-\\frac12 = \\frac13$, so taking the reciprocal of both sides gives $x = \\boxed{3}$.", "idx": 73}


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

    item_var = item.replace(' ', '_')
    county_var = county.replace(' ', '_')
    # Get values for variables in the expression
    fraction_1, fraction_2, fraction_result = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"{name} is organizing {item} at {place} in {county}. Initially, {name} allocates {round(fraction_1*100)}% of the available space to the {item}. "
    problem_statement += f"After rearranging, the space allocated to the {item} increases to {fraction_result*100}%. What percentage of the space was added for the {item}?"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Initial fraction of space allocated to {item}
initial_fraction = {fraction_1}

# Final fraction of space allocated to {item}
final_fraction = {fraction_result}

# Calculating the fraction representing the added space
added_fraction = final_fraction - initial_fraction

# Solving for the added fraction
result = added_fraction
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'], 2) * 100)

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"Initially, {name} allocated {round(fraction_1*100)}% of the space to {item}. After rearranging, this increased to {round(fraction_result*100)}%. "
    solution_wocode += f"The additional space allocated is {round(fraction_result*100)}% - {round(fraction_1*100)}% = {result}%."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select fractional parameters to ensure the calculations result in integers or two-decimal-place numbers.
    """
    # Define a list of fractions that convert neatly to two-decimal-place decimals
    fractions = [1/2, 1/3, 1/4, 1/5, 1/6, 2/3, 3/4, 4/5, 5/6, 1/7, 1/8, 1/9, 1/10]

    # Randomly choose two different fractions
    fraction_1, fraction_result = random.sample(fractions, 2)

    # Ensure fraction_1 is the smaller and fraction_result is the larger
    if fraction_1 > fraction_result:
        fraction_1, fraction_result = fraction_result, fraction_1

    # Calculate the added fraction and round to two decimal places
    fraction_2 = round(fraction_result - fraction_1, 2)

    # Round the fractions to two decimal places for consistency
    fraction_1 = round(fraction_1, 2)
    fraction_result = round(fraction_result, 2)

    return fraction_1, fraction_2, fraction_result



parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/math-0073-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
