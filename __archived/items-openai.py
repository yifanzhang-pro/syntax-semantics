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
    "craft kits", "board games", "video games", "DVDs", "CDs", 
    "books", "magazines", "notebooks", "diaries", "planners", "stationery sets", "desk organizers", 
    "computer accessories", "phone cases", "tablet covers", "cameras", "headphones", 
    "speakers", "drones", "smart watches", "fitness trackers", "yoga mats", "sports equipment", 
    "bicycles", "scooters", "skateboards", "camping gear", "travel accessories", "luggage", 
    "pet supplies", "toys", "baby gear", "gourmet foods", "wines"
]

names2 = [
    "electronics", "books", "kitchenware", "home decor", "gardening tools", "sports equipment",
    "office supplies", "beauty products", "health supplements", "clothing accessories", 
    "footwear", "handbags", "jewelry", "watches", "sunglasses", "hats", "scarves", 
    "cosmetics", "skin care products", "hair care products", "bath essentials", 
    "bedding", "furniture", "lighting fixtures", "wall art", "photo frames", 
    "candles", "stationery", "craft supplies", "party supplies", "toys for pets",
    "pet food", "bird feeders", "outdoor furniture", "camping gear",
    "bicycles", "yoga mats", "sports apparel", "swimwear",
    "travel accessories", "luggage", "backpacks", "world maps", "language learning materials",
    "musical instruments", "headphones", "speakers", "smart home devices", "computer accessories",
    "video games", "board games", "puzzle games", "collectibles", "model kits",
    "DIY tools", "car accessories", "motorcycle gear", "boating supplies", "fishing equipment",
    "gourmet teas", "coffee beans", "baking supplies", "spices and herbs", "organic produce",
    "vegan snacks", "ethnic foods", "cooking oils", "sauces and condiments",
    "sweets and chocolates", "fresh flowers", "greeting cards"
]

names3 = [
    "handcrafted candles", "vintage novels", "artisanal breads", "luxury perfumes",
    "organic teas", "customized mugs", "leather journals", "designer scarves",
    "wooden puzzles", "handmade soaps", "silk ties", "gourmet coffees",
    "puzzle games", "antique clocks", "wool blankets", "bamboo cutting boards",
    "travel guides", "yoga mats", "watercolor sets", "gardening tools",
    "fountain pens", "cooking spices", "photo albums", "scented lotions",
    "beaded necklaces", "cozy slippers", "abstract paintings", "kitchen gadgets",
    "decorative vases", "acoustic guitars", "digital cameras", "board games",
    "gemstone rings", "comfy robes", "model airplanes", "fitness trackers",
    "wine glasses", "astronomy books", "baking sets", "bluetooth speakers",
    "wall calendars", "plant pots", "camping gear", "knitting kits",
    "solar chargers", "beach towels", "bird feeders", "smart watches",
    "sun hats", "novelty socks", "coffee table books", "video games",
    "picnic baskets", "drone cameras", "tea infusers", "backpacks",
    "bath bombs", "night lights", "scratch maps", "sleep masks",
    "card games", "sunglasses", "chess sets",
    "pottery supplies", "ice cream makers", "sweatshirts", "hiking boots",
    "cookware sets", "action cameras", "jigsaw puzzles", "scented candles",
    "running shoes", "smartphone cases", "herbal teas", "canvas prints",
    "travel pillows", "guitar strings", "art supplies", "memory cards",
    "desk organizers", "fitness DVDs", "water bottles", "earphones",
    "gym bags", "laptop sleeves", "passport holders", "graphic novels",
    "wireless chargers", "embroidery kits", "tote bags", "cocktail shakers",
    "massage rollers", "sketchbooks", "webcams", "turbans"
]

names4 = [
    "lamps", "candles", "vases", "clocks", "mirrors", 
    "rugs", "cushions", "blankets", "coffee tables", "sofas", 
    "armchairs", "ottomans", "bookshelves", "desks", "office chairs", 
    "computers", "tablets", "smartphones", "headphones", "speakers", 
    "cameras", "watches", "sunglasses", "laptops",
    "handbags", "suitcases", "shoes", "boots",
    "sneakers", "hats", "scarves", "gloves", "belts", 
    "shirts", "blouses", "jeans", "trousers", 
    "shorts", "jackets", "coats", "sweaters", "cardigans", 
    "dresses", "ties", "socks", "underwear", "swimwear", 
    "sports equipment", "bicycles", "skateboards", "surfboards", "snowboards", 
    "tennis rackets", "basketballs", "footballs", 
    "baseballs", "volleyballs", "badminton rackets", "squash rackets", "bowling balls", 
    "fishing rods", "camping tents", "sleeping bags", "hiking boots", "binoculars", 
    "maps", "compasses", "flashlights", "first aid kits", "water bottles", 
    "picnic baskets", "grills", "coolers", "insect repellent", 
    "board games", "puzzle books", "playing cards", "video games"
]

names5 = [
    "scarves", "rings", "bracelets", "earrings", "sunglasses", "tights", "sandals", "boots",
    "cufflinks", "tie clips", "ties", "bow ties", "pocket squares", "umbrellas", "headbands",
    "hair clips", "hair ties", "brooches", "slippers",
    "ankle boots", "ballet flats", "loafers",
    "derby shoes", "oxford shoes", "sneakers", "high heels", "pumps", "wedges", "espadrilles",
    "swimwear", "goggles", "swimming caps", "rash guards", "wetsuits", "diving fins",
    "snorkels", "trunks", "swimming shorts", "tankinis",
    "swim dresses", "sarongs", "beach towels", "sun hats", "beach bags",
    "sunglass cases", "watch cases", "jewelry boxes", "travel bags", "luggage tags",
    "passport holders", "travel pillows", "sleep masks", "keychains", "backpacks",
    "messenger bags", "laptop bags", "briefcases", "duffel bags", "tote bags",
    "crossbody bags", "satchels", "clutch bags", "fanny packs",
    "camera bags", "diaper bags", "gym bags", "yoga mats", "water bottles"
]

names6 = [
    "computer accessories", "phone cases", "tablet covers", "cameras", "headphones",
    "smart watches", "USB cables", "power banks", "screen protectors", "wireless chargers",
    "memory cards", "flash drives", "external hard drives", "keyboard covers", "mouse pads",
    "webcams", "microphones", "speakers", "VR headsets", "drone accessories",
    "fitness trackers", "gaming controllers", "console skins", "game storage cases", "laptop bags",
    "printer cartridges", "graphic tablets", "digital pens", "monitor stands",
    "cooling pads", "router extenders", "network switches", "HDMI cables", "adapter plugs",
    "smart light bulbs", "smart thermostats", "home security cameras", "robot vacuums", "smart locks",
    "voice assistants", "streaming devices", "TV mounts", "soundbars", "bluetooth receivers",
    "photo printers", "tripods", "camera lenses", "camera bags", "lens filters",
    "studio lights", "backdrops", "memory card readers", "battery chargers", "camera cleaning kits",
    "smart scales", "blood pressure monitors", "glucose meters", "thermometers", "smart toothbrushes",
    "electric shavers", "hair dryers", "microwaves", "slow cookers",
    "food processors", "mixers", "juicers", "rice cookers", "air fryers",
    "induction cooktops", "electric grills", "bread makers", "ice cream makers", "waffle irons",
    "smart doorbells", "window sensors", "smart plugs", "water leak detectors", "carbon monoxide detectors",
    "wireless headphones", "earbuds", "Bluetooth speakers",
]


all_names = names1 + names2 + names3 + names4 + names5 + names6


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
