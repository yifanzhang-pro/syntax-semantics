import jsonlines

# Define the list of names
names1 = [
    "clips", "cupcakes", "handmade soaps", "notebooks", "scarves", 
    "paintings", "books", "plants", "skirts", "wooden furniture", 
    "gourmet chocolates", "potted succulents", "musical instruments", 
    "candles", "pens", "journals", "tea sets", "coffee mugs", "picture frames", "earrings", "bracelets", 
    "necklaces", "watches", "hats", "gloves", "socks", "shoes", "bags", "wallets", "belts", 
    "sunglasses", "umbrellas", "keychains", "stickers", "posters", "calendars", "clocks", 
    "vases", "lamps", "pillows", "throws", "rugs", "curtains", "towels", "bed sheets", 
    "duvet covers", "blankets", "bathrobes", "bath salts", "body lotions", "perfumes", 
    "makeup kits", "hair accessories", "shampoos", "conditioners", "shower gels", "bath bombs", 
    "skincare products", "nail polish", "lipsticks", "eyeshadows", "mascaras", "blushes", 
    "bronzer", "foundation", "concealer", "powder", "makeup brushes", "art supplies", 
    "craft kits", "puzzles", "board games", "video games", "DVDs", "CDs", "vinyl records", 
    "books", "magazines", "notebooks", "diaries", "planners", "stationery sets", "desk organizers", 
    "computer accessories", "phone cases", "tablet covers", "cameras", "headphones", 
    "speakers", "drones", "smart watches", "fitness trackers", "yoga mats", "sports equipment", 
    "bicycles", "scooters", "skateboards", "camping gear", "travel accessories", "luggage", 
    "pet supplies", "toys", "children's clothing", "baby gear", "gourmet foods", "wines", "spirits"
]

names2 = [
    "electronics", "books", "kitchenware", "home decor", "gardening tools", "sports equipment",
    "office supplies", "beauty products", "health supplements", "clothing accessories", 
    "footwear", "handbags", "jewelry", "watches", "sunglasses", "hats", "scarves", 
    "cosmetics", "skin care products", "hair care products", "bath essentials", 
    "bedding", "furniture", "lighting fixtures", "wall art", "photo frames", 
    "candles", "stationery", "craft supplies", "party supplies", "toys for pets",
    "pet food", "aquarium supplies", "bird feeders", "outdoor furniture", "camping gear",
    "bicycles", "fitness equipment", "yoga mats", "sports apparel", "swimwear",
    "travel accessories", "luggage", "backpacks", "world maps", "language learning materials",
    "musical instruments", "headphones", "speakers", "smart home devices", "computer accessories",
    "video games", "board games", "puzzle games", "collectibles", "model kits",
    "DIY tools", "car accessories", "motorcycle gear", "boating supplies", "fishing equipment",
    "gourmet teas", "coffee beans", "baking supplies", "spices and herbs", "organic produce",
    "vegan snacks", "gluten-free products", "ethnic foods", "cooking oils", "sauces and condiments",
    "sweets and chocolates", "fresh flowers", "greeting cards", "gift baskets", "novelty items",
    "seasonal decorations", "religious items", "cultural artifacts", "antiques", "rare collectibles"
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
file_path = "./data/items-openai.jsonl"

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
