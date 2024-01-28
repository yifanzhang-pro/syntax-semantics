# Origin problem: {"question": "In a truck, there are 26 pink hard hats, 15 green hard hats, and 24 yellow hard hats.  If Carl takes away 4 pink hard hats, and John takes away 6 pink hard hats and twice as many green hard hats as the number of pink hard hats that he removed, then calculate the total number of hard hats that remained in the truck.", "answer": "If there were 26 pink hard hats and Carl took away 4 pink hard hats, the number of pink hard hats that remained is 26-4 = <<26-4=22>>22\nJohn also took away 6 pink hard hats, leaving 22-6 = <<22-6=16>>16 pink hard hats in the truck.\nIf John also took twice as many green hard hats as pink hard hats, he took 2*6 = <<6*2=12>>12 green hard hats.\nThe total number of green hard hats that remained in the truck is 15-12 = <<15-12=3>>3\nIn the truck, after some are taken, there were 3 green hard hats + 16 pink hard hats = <<3+16=19>>19 hard hats in the truck.\nAltogether, 19 green and pink hard hats + 24 yellow hards hats = <<19+24=43>>43 hard hats remained in the truck\n#### 43"}


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





parser = argparse.ArgumentParser(description="Generate problems and solutions.")
parser.add_argument("--num_problems", type=int, default=10000, help="Number of problems to generate")

args = parser.parse_args()
NUM_PROBLEMS = args.num_problems

        
if __name__ == "__main__":
    os.makedirs('./output', exist_ok=True)
    # output jsonl file
    with open(f'./output/gsm-0017-1--NUM{NUM_PROBLEMS}.jsonl', 'w') as f:
        for i in range(NUM_PROBLEMS):
            problem, solution_code, result, solution_wocode = generate_problem_and_solution_code()
            # Write problem to file
            f.write(json.dumps({"problem": problem, "solution_code": solution_code, "solution_wocode": solution_wocode, "result": str(result), "idx": i}) + '\n')
