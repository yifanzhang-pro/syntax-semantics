# Origin problem: {"question": "Artemis is making tea for a party. She knows her mom drinks an 8-ounce cup of tea and uses one ounce of tea. She will use this same ratio for the party. The party has 12 people there and each of them wants a 6-ounce cup of tea. How many ounces of tea does she need?", "answer": "She is making 72 ounces of water because 12 x 6 = <<12*6=72>>72\nShe needs 9 ounces of tea because 72 / 8 = <<72/8=9>>9\n#### 9"}


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
    # Assuming predefined lists for names, items, places, and counties are available
    # Randomly select terms
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    item = random.choice(items)  # Let's say 'bags of snacks' to fit the context
    place = random.choice(places)
    county = random.choice(us_counties)
    county = county['CountyName'] + ", " + county["StateName"]

    # Variables for use in solution code, replacing spaces with underscores
    name_var = name.replace(' ', '_')
    item_var = item.replace(' ', '_')
    place_var = place.replace(' ', '_')
    county_var = county.replace(' ', '_').replace(',', '')

    # Set up a scenario similar to the tea and water ratio
    ratio, total_people = get_params_combination()
    # For this example, let's say the ratio is 1 unit of item serves 3 people
    ratio_people_served_per_unit = ratio  # Fixed ratio for simplicity

    # Construct problem statement
    problem_statement = f"{name} is preparing {item} for an event at {place} in {county}. "
    problem_statement += "They know that one unit of " + item + " serves " + str(ratio_people_served_per_unit) + " people. "
    problem_statement += f"For the event, there are {total_people} people. "
    problem_statement += f"How many units of {item} does {name} need in total?"

    # Generate solution code with specific variable names and comments
    units_needed_per_person_var = f"units_needed_per_person"
    total_people_var = f"total_people"
    total_units_needed_var = f"total_units_needed"

    solution_code = f"""# Ratio of people served per unit of {item}
ratio_people_served_per_unit = {ratio_people_served_per_unit}

# Total number of people at the event
{total_people_var} = {total_people}

# Calculating the total units of {item} needed by dividing the total people by the ratio
{total_units_needed_var} = {total_people_var} / ratio_people_served_per_unit

result = {total_units_needed_var}
"""

    # Execute the solution code and get the result
    exec_globals = {}
    exec(solution_code, {}, exec_globals)
    result = round(exec_globals['result'])

    # Generate the solution without code
    solution_wocode = f"For the event with {total_people} people, where one unit of {item} serves {ratio_people_served_per_unit} people, "
    solution_wocode += f"{name} needs {total_people} / {ratio_people_served_per_unit} = {result} units of {item} in total."

    return problem_statement, solution_code, result, solution_wocode


def get_params_combination():
    """
    Select integer parameters to ensure calculations result in an integer value for total units needed without rounding up.
    This function will ensure that the total number of people is a direct multiple of the ratio of people served per unit.
    """
    # Possible ratios of people served per unit
    ratios = [1, 2, 3, 4, 5, 6, 7, 8]  # Example ratios

    # Select a random ratio
    ratio = random.choice(ratios)

    # Ensure total_people is a multiple of the selected ratio to avoid the need for rounding up
    # This could be achieved by generating a multiplier and then multiplying it by the ratio
    multiplier = random.randint(1, 20)  # Adjust range as needed for more variety
    total_people = ratio * multiplier  # This ensures the division is always exact

    return ratio, total_people


parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0038-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "template_name": "gsm-0038-1", "idx": i}) + '\n')
