import jsonlines

# Define the list of names
names1 = [
    "Natalia", "Carlos", "Aisha", "Liam", "Emma", "James", "Fatima", "John", "Olivia", "Benjamin",
    "Sophia", "Elijah", "Ava", "Daniel", "Mia", "William", "Isabella", "Alexander", "Sophia",
    "Michael", "Abigail", "Ethan", "Emily", "Matthew", "Charlotte", "Joseph", "Harper", "Samuel",
    "Amelia", "David", "Evelyn", "Andrew", "Elizabeth", "Gabriel", "Sofia", "Henry", "Grace",
    "Christopher", "Chloe", "Nicholas", "Ella", "Anthony", "Scarlett", "Thomas", "Victoria",
    "Oliver", "Aria", "Eli", "Madison", "Jonathan", "Lily", "Daniel", "Aubrey", "Aiden", "Layla",
    "Jackson", "Zoe", "Sebastian", "Nora", "Caleb", "Riley", "Dylan", "Penelope", "Logan", "Lillian",
    "Carter", "Hannah", "Ryan", "Addison", "Nicholas", "Brooklyn", "William", "Grace", "Christopher",
    "Zoey", "Matthew", "Luna", "Julian", "Stella", "Nathan", "Hazel", "Samuel", "Leah", "Christian",
    "Natalie", "Jack", "Samantha", "Isaac", "Audrey", "Owen", "Lucy", "Eli", "Alyssa", "Luke", "Ellie",
    "Isaiah", "Claire", "John", "Violet", "James", "Skylar", "Andrew", "Mila", "Nathan", "Peyton"
]

names2 = [
    "Oliver", "Sophia", "William", "Aria", "Elijah", "Grace", "Benjamin", "Luna", "Samuel", "Chloe",
    "Daniel", "Zoe", "Matthew", "Lily", "Henry", "Ava", "Joseph", "Harper", "Michael", "Evelyn",
    "Alexander", "Madison", "David", "Scarlett", "Jameson", "Abigail", "Nicholas", "Ella", "Ethan", "Emma",
    "Jackson", "Charlotte", "Sebastian", "Liam", "Gabriel", "Avery", "Christopher", "Sofia", "Daniel", "Eleanor",
    "Leo", "Penelope", "Caleb", "Hannah", "Ryan", "Nora", "Julian", "Amelia", "Isaac", "Aubrey", "Mason", "Addison",
    "Lucas", "Ellie", "Matthew", "Stella", "Liam", "Mackenzie", "Dylan", "Natalie", "Connor", "Aurora", "Thomas", "Lillian",
    "Eli", "Lucy", "Anthony", "Leah", "Luke", "Elizabeth", "Isabelle", "Victoria", "Bella", "Eva", "Maya", "Eliana",
    "Xavier", "Hazel", "Christian", "Zara", "Nicholas", "Grace", "Jonathan", "Layla", "Aaron", "Sophie", "Nolan", "Harper",
    "Dominic", "Riley", "Jeremiah", "Zoey", "Gavin", "Aria"
]

names3 = [

]

names4 = [

]

names5 = [

]

all_names = names1 + names2 + names3 + names4 + names5


# Printing the list of names
NAME = list(set(all_names))
NAME.sort()
print(NAME)


# Specify the file path for the JSONL file
file_path = "./data/names-openai.jsonl"

# Write the names to the JSONL file
with jsonlines.open(file_path, mode='w') as writer:
    writer.write_all(NAME)

# Now you can load the names from the JSONL file
loaded_names = []
with jsonlines.open(file_path) as reader:
    for line in reader:
        loaded_names.append(line)

# Print the loaded names
print(len(loaded_names))
