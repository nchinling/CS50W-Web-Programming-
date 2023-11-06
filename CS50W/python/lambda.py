people = [
    {"name": "Tan", "house":"ABC"},
    {"name": "Harry", "house":"Gryffindor"},
    {"name": "Ling", "house":"Slytherin"},
    {"name": "Shan", "house":"Ravenclaw"}
]

# def f(person):
#     return person["house"]

people.sort(key=lambda person: person["name"])

print(people)