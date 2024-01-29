import json

# Define the input and output file paths
input_file_path = "./math/train.jsonl"
output_file_path = "./math/train-simplesub.jsonl"

# Function to check if a sample satisfies the criteria
def satisfies_criteria(sample):
    # Check if "level" is 1, 2, or 3
    if 'level' in sample and sample['level'] in ["Level 1"]:
        # Check if "problem" field does not contain '[asy]'
        if 'problem' in sample and '[asy]' not in sample['problem']:
            if 'type' in sample and 'type' not in ["Geometry"]:
                return True
            
    return False

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    # Process each line in the input file
    idx = 0
    for line in input_file:
        sample = json.loads(line.strip())  # Load JSON object from the line
        if satisfies_criteria(sample):
            sample['idx'] = idx
            sample.pop('level', None)
            sample.pop('type', None)
            # Write the sample to the output file if it satisfies the criteria
            output_file.write(json.dumps(sample) + '\n')
        idx += 1

print("Filtered samples have been saved to", output_file_path)
