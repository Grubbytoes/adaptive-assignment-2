import json
import matplotlib.pyplot as plt

from itertools import product

sizes = ["small", "medium", "large"]
types = ["lonely", "social"]

def open_and_load(size, type):
    filename = f"{size}.{type}.json"
    data = json.load(open("results/"+filename, 'r'))
    return data

for s in sizes:
    lonely_data = open_and_load(s, "lonely")
    social_data = open_and_load(s, "social")
    
    # seasons
    plt.grid(axis="y")
    for i in range(1, 4):
        plt.axvline(i*12, c='tomato', ls="dashed", linewidth="1")
        
    plt.plot(lonely_data["nectar/cycle/critter"], label="lonely")
    plt.plot(social_data["nectar/cycle/critter"], label="social", c='hotpink')
    plt.ylabel("nectar per cycle per critter")
    plt.xlabel("cycle")
    
    plt.savefig(f"results/{s}.png")
    plt.close()