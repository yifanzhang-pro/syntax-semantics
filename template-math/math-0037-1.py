# Origin problem: {"problem": "The function $f(x)$ is defined by $f(x)=x^{2}-x$. What is the value of $f(4)$?", "solution": "$f(4)=4^2-4=16-4=\\boxed{12}$.", "idx": 37}


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
    # Randomly select a name, an item, a place, and a county
    name = random.choice(first_names).replace(' ', '_') + '_' + random.choice(last_names).replace(' ', '_')
    item = random.choice(items).replace(' ', '_')
    place = random.choice(places).replace(' ', '_')
    county = random.choice(us_counties)
    county = county['CountyName'].replace(' ', '_') + ",_" + county["StateName"].replace(' ', '_')

    # Define a simple mathematical function and select a specific value for calculation
    function_input = random.randint(1, 100)
    a, b = get_params_combination()  # Coefficients for the function

    # Construct the problem statement
    problem_statement = f"The function $g(x)$ is defined by $g(x) = {a}x + {b}$. What is the value of $g({function_input})$?"

    # Generate the solution code
    solution_code = f"""# Value of x
x = {function_input}

# Calculating g(x)
g_x = {a} * x + {b}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['g_x']

    # Generate the solution without code
    solution_wocode = f"$g({function_input}) = {a} * {function_input} + {b} = {a * function_input} + {b} = {result}$."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    # Randomly generate coefficients a and b for the function
    a = random.randint(1, 100)
    b = random.randint(1, 100)

    return a, b



parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/math-0037-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
