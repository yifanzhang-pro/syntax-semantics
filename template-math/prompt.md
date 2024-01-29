# [Instruction]: Here comes a problem template, Can you compose a new problem template which has exactly the same reasoning structure of this new origin problem?

### Example origin problem 
{
    "problem": "If $x = 2$ and $y = 5$, then what is the value of $\\frac{x^4+2y^2}{6}$ ?", 
    "solution": "We have  \\[\\frac{x^4 + 2y^2}{6} = \\frac{2^4 + 2(5^2)}{6} = \\frac{16+2(25)}{6} = \\frac{16+50}{6} = \\frac{66}{6} = \\boxed{11}.\\]"
}

### Example problem template
```python
# Origin problem: {"problem": "If $x = 2$ and $y = 5$, then what is the value of $\\frac{x^4+2y^2}{6}$ ?", "solution": "We have  \\[\\frac{x^4 + 2y^2}{6} = \\frac{2^4 + 2(5^2)}{6} = \\frac{16+2(25)}{6} = \\frac{16+50}{6} = \\frac{66}{6} = \\boxed{11}.\\]"}


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

items = [] # plural items, like 'apples'
with jsonlines.open('./data/items-llm.jsonl') as reader:
    for line in reader:
        items.append(line)

places = [] # like 'a bookstore', 'the xxx', ...
with jsonlines.open('./data/places-llm.jsonl') as reader:
    for line in reader:
        places.append(line)

us_counties = []
with jsonlines.open('./data/us_counties.jsonl') as reader:
    for line in reader:
        us_counties.append(line)


def generate_problem_and_solution_code():
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Get values for variables in the expression
    var1_value, var2_value, divisor = get_params_combination()

    # Construct problem statement with specific details
    problem_statement = f"If {name} has {var1_value} {item}s at {place} in {county}, and {var2_value} more are added, "
    problem_statement += f"what is the total value of {item}s when divided by {divisor}?"

    # Generate solution code with specific variable names and comments
    solution_code = f"""# Initial amount of {item}s
initial_{item.replace(' ', '_')} = {var1_value}

# Added {item}s
added_{item.replace(' ', '_')} = {var2_value}

# Total {item}s
total_{item.replace(' ', '_')} = initial_{item.replace(' ', '_')} + added_{item.replace(' ', '_')}

# Calculating the value when divided by {divisor}
result = total_{item.replace(' ', '_')} / {divisor}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = int(round(exec_globals['result'],0))

    # Generate the solution without code (solution_wocode)
    solution_wocode = f"The initial amount of {item}s is {var1_value}, and {var2_value} more are added, making a total of {var1_value} + {var2_value} = {var1_value + var2_value}. "
    solution_wocode += f"When divided by {divisor}, the result is {int(round(result, 0))}."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in integer values.
    """
    while True:
        # Randomly generate initial value and addition
        var1_value = random.randint(1, 100)
        var2_value = random.randint(1, 100)

        # Randomly select a divisor
        divisor = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])

        # Check if the total and division result are integers
        total = var1_value + var2_value
        if total % divisor == 0:
            return var1_value, var2_value, divisor


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

# [Instruction]: Can you compose a new problem template which has exactly the same reasoning structure of this new origin problem? You need to utilized predefined variable lists first_names, last_names, items, places, us_counties. **You only need to write down the function generate_problem_and_solution_code() and get_params_combination()**, I suggest you to get integer params. Your problem and answer should be in the same distribution as the MATH dataset (Hendrycks et al., 2021).

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
    "problem": "The perimeter of a rectangular garden is 60 feet. If the length of the field is twice the width, what is the area of the field, in square feet?", 
    "solution": "If the length is $l$ and the width is $w$, then the perimeter is $2l+2w$. We can set up the equations $2l+2w=60 \\Rightarrow l+w=30$ and $l=2w$. Now we substitute $l$ in terms of $w$ into the first equation and get $l+w=2w+w=30$, so $w=10$ and $l=2(10)=20$. That means the area of the rectangular garden is $lw=20(10)=\\boxed{200}$ square feet."
}

### Analysis and Reasoning

[to be generated]

### New problem template

[to be generated]
