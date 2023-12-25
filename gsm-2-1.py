import random
import math
import json
import argparse
import jsonlines

# Consistent random generation
random.seed(42)

first_names = []
with jsonlines.open('./data/top_first_names.jsonl') as reader:
    for line in reader:
        first_names.append(line['first_name'])

last_names = []
with jsonlines.open('./data/top_last_names.jsonl') as reader:
    for line in reader:
        last_names.append(line['last_name'])


def get_saving_scenario():
    # Target amount for the item
    while True:
        target_amount = random.randint(50, 500000)

        # Initial fraction of the target amount
        initial_fraction = round(random.uniform(0.01, 0.5), 2)

        # Calculate the product
        product = initial_fraction * target_amount

        if math.isclose(product, round(product), rel_tol=1e-12):
            # Additional contributions (from 1 to 3 contributors)
            num_contributors = random.randint(1, 3)
            contributions = [random.randint(5, target_amount // 4) for _ in range(num_contributors)]

            return target_amount, initial_fraction, contributions


def generate_problem_and_solution_code():
    # Randomly generate scenario details
    target_amount, initial_fraction, contributions = get_saving_scenario()

    # Lists of random terms
    names = ["Natalia", "Carlos", "Aisha", "Liam", "Emma", "James", "Fatima", "John", "Olivia", "Benjamin", "Sophia", "Elijah", "Ava"]
    items = ["wallet", "bicycle", "laptop", "camera", "smartphone", "pair of sneakers", "backpack"]
    contributors = ["parents", "grandparents", "uncle", "aunt", "friend", "sibling"]

    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)
    contributor_names = random.sample(contributors, len(contributions))

    # Problem narrative
    problem_statement = f"{name} is saving money for a new {item} which costs {target_amount} dollars. "
    problem_statement += f"Initially, she has only {int(initial_fraction * 100)}% of the money she needs. "
    
    for i, amount in enumerate(contributions):
        problem_statement += f"Her {contributor_names[i]} decided to give her {amount} dollars for that purpose. "
    
    problem_statement += f"How much more money does {name} need to buy the item?"

    # Solution code
    initial_amount_var = "initial_amount"
    total_contributions_var = "total_contributions"
    remaining_amount_var = "remaining_amount"

    solution_code = f"""# Initial amount {name} has
{initial_amount_var} = {target_amount} * {initial_fraction}

# Total contributions
{total_contributions_var} = sum({contributions})

# Remaining amount needed
{remaining_amount_var} = {target_amount} - {initial_amount_var} - {total_contributions_var}

# Final result
result = {remaining_amount_var}
"""

    # Execute solution code
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = exec_globals['remaining_amount']

    # Solution without code
    initial_amount = target_amount * initial_fraction
    solution_wocode = f"In the beginning, {name} has only {initial_amount:.2f} dollars.\n"
    total_contributions = 0
    for i, amount in enumerate(contributions):
        solution_wocode += f"{name}'s {contributor_names[i]} gave her {amount} dollars. "
        total_contributions += amount

    remaining_amount = target_amount - initial_amount - total_contributions
    contributions_str = ' + '.join(map(str, contributions))
    solution_wocode += f"This means, {name} needs {target_amount} - {initial_amount:.2f} - ({contributions_str}) = {remaining_amount:.2f} dollars more."

    return problem_statement, solution_code, result, solution_wocode


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
            f.write(json.dumps({"problem": problem, "solution_code": "<code>\n" + solution_code + "</code>\n", "solution_wocode": solution_wocode, "result": f"{result:.2f}"}) + '\n')
