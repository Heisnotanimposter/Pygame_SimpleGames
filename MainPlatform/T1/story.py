import random

templates = [
    "In the shadowed [location], a rumor reached [character]'s ears...",
    "A quest began!  [character] must find the lost [item].",
]
locations =  ["ancient forest", "forgotten mine", "haunted castle"]
characters = ["Maya the Ranger", "Gorn the Strong", "Willow the Wise"] 
items = ["Amulet of Power", "Sword of Legends", "Mystic Scroll"]

def Story():
    template = random.choice(templates)
    return template.replace("[location]", random.choice(locations)) \
                   .replace("[character]", random.choice(characters)) \
                   .replace("[item]", random.choice(items)) 

print(Story())
