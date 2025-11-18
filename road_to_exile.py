import os
import json
import random
import time

# ---------------------------
# Game Data
# ---------------------------

player = {
    "name": "",
    "health": 100,
    "stamina": 100,
    "inventory": [],
    "location": "start",
    "story_flags": {}
}

save_file = "road_to_exile_save.json"

# ---------------------------
# Utility Functions
# ---------------------------

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def save_game():
    with open(save_file, "w") as f:
        json.dump(player, f)
    slow_print("Game saved successfully!")

def load_game():
    global player
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            player = json.load(f)
        slow_print("Game loaded successfully!")
        return True
    else:
        slow_print("No save found.")
        return False

def check_health():
    if player["health"] <= 0:
        slow_print("You have died on your journey. Game over.")
        exit()

def random_event():
    events = [
        {"desc": "You found a hidden potion! +20 health", "effect": lambda: add_health(20)},
        {"desc": "A wild animal attacks! -15 health", "effect": lambda: add_health(-15)},
        {"desc": "You find some food. +10 stamina", "effect": lambda: add_stamina(10)},
        {"desc": "You trip and fall. -10 stamina", "effect": lambda: add_stamina(-10)}
    ]
    event = random.choice(events)
    slow_print(f"Random event: {event['desc']}")
    event["effect"]()
    check_health()

def add_health(amount):
    player["health"] += amount
    if player["health"] > 100: player["health"] = 100
    slow_print(f"Health: {player['health']}")

def add_stamina(amount):
    player["stamina"] += amount
    if player["stamina"] > 100: player["stamina"] = 100
    slow_print(f"Stamina: {player['stamina']}")

def add_item(item):
    player["inventory"].append(item)
    slow_print(f"You received: {item}")

# ---------------------------
# Story Functions
# ---------------------------

def start():
    slow_print("Welcome to Road to Exile!")
    player["name"] = input("Enter your character's name: ")
    slow_print(f"Greetings, {player['name']}. Your journey begins...\n")
    town_square()

def town_square():
    slow_print("You are at the town square. Paths lead to the forest, the mountains, and the river.")
    slow_print(f"Health: {player['health']}, Stamina: {player['stamina']}, Inventory: {player['inventory']}")
    
    choice = input("Where do you want to go? (forest/mountains/river/save/load/exit): ").lower()
    
    if choice == "forest":
        forest()
    elif choice == "mountains":
        mountains()
    elif choice == "river":
        river()
    elif choice == "save":
        save_game()
        town_square()
    elif choice == "load":
        load_game()
        town_square()
    elif choice == "exit":
        slow_print("Exiting game. Goodbye!")
        exit()
    else:
        slow_print("Invalid choice.")
        town_square()

def forest():
    slow_print("You enter the dark forest. The trees loom over you.")
    random_event()
    slow_print("You see a mysterious cave and a narrow path deeper into the forest.")
    
    choice = input("Do you enter the cave or go deeper? (cave/deeper/back): ").lower()
    if choice == "cave":
        cave()
    elif choice == "deeper":
        deep_forest()
    elif choice == "back":
        town_square()
    else:
        slow_print("Invalid choice.")
        forest()

def cave():
    slow_print("The cave is dark but you find an old sword on the ground.")
    add_item("Old Sword")
    random_event()
    forest()

def deep_forest():
    slow_print("You venture deeper and encounter a band of exiles.")
    if "band_of_exiles" not in player["story_flags"]:
        slow_print("They attack you! You fight bravely.")
        outcome = random.choice(["win", "lose"])
        if outcome == "win":
            slow_print("You defeat them and gain a shield!")
            add_item("Shield")
        else:
            slow_print("You are injured in the fight. -30 health")
            add_health(-30)
        player["story_flags"]["band_of_exiles"] = True
    random_event()
    forest()

def mountains():
    slow_print("The mountains are steep and treacherous.")
    random_event()
    choice = input("Do you climb or explore a cave? (climb/cave/back): ").lower()
    if choice == "climb":
        slow_print("You reach a high peak and find a healing herb.")
        add_item("Healing Herb")
        add_health(20)
        mountains()
    elif choice == "cave":
        slow_print("You enter a mountain cave and find treasure!")
        add_item("Gold Coins")
        mountains()
    elif choice == "back":
        town_square()
    else:
        slow_print("Invalid choice.")
        mountains()

def river():
    slow_print("The river is wide and fast-flowing.")
    random_event()
    choice = input("Do you swim across or follow the river? (swim/follow/back): ").lower()
    if choice == "swim":
        slow_print("You brave the river and find a fishing rod.")
        add_item("Fishing Rod")
        add_stamina(-20)
        river()
    elif choice == "follow":
        slow_print("Following the river, you find a peaceful village.")
        add_health(10)
        river_village()
    elif choice == "back":
        town_square()
    else:
        slow_print("Invalid choice.")
        river()

def river_village():
    slow_print("Villagers welcome you and offer food.")
    add_item("Bread")
    add_stamina(20)
    choice = input("Do you stay or leave? (stay/leave): ").lower()
    if choice == "stay":
        slow_print("You rest and recover fully.")
        player["health"] = 100
        player["stamina"] = 100
        river_village()
    elif choice == "leave":
        river()
    else:
        slow_print("Invalid choice.")
        river_village()

# ---------------------------
# Main Game Loop
# ---------------------------

if __name__ == "__main__":
    slow_print("Road to Exile - Text Adventure Game")
    slow_print("Type 'save' anytime to save, 'load' to load, 'exit' to quit.\n")
    
    if os.path.exists(save_file):
        choice = input("Load previous save? (yes/no): ").lower()
        if choice == "yes":
            load_game()
            town_square()
        else:
            start()
    else:
        start()
