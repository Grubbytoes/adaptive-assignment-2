import json
import matplotlib.pyplot as plt

from itertools import product

sizes = ["small", "medium", "large"]
types = ["lonely", "social"]

for size, type in product(sizes, types):
    filename = f"{size}.{type}.json"
    data = json.load(open("results/"+filename, 'r'))
    
    # plotting here