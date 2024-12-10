from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random  # Make sure to import random module
import json  # Import JSON module for saving/loading

app = Ursina()
player = FirstPersonController()
# Load a player model (make sure to have a player model in your assets)
player_model = Entity(model='cube',texture='figur', parent=player, position=(0, 1, 0))  # Adjust position as needed
Sky()

boxes = []


def add_box(position,texture='Grass2'):
    boxes.append(Button(
        parent=scene,
        model='cube',
        origin=0.3,
        color=color.white,  # Assign a random color here
        position=position,
        texture=texture
    ))
# Function to save the game state
def save_game(filename='save_game.json'):
    game_state = []
    for box in boxes:
        game_state.append({
            'position': list(box.position),
            'texture': box.texture.name  # Save the texture name
        })
    print("Game state to save:", game_state)  # Debug print
    try:
        with open(filename, 'w') as f:
            json.dump(game_state, f)
        print("Game saved!") # Confirm save
    except Exception as e:
        print("Error saving game:", e)  # Print any errors

# Function to load the game state
def load_game(filename='save_game.json'):
    global boxes
    # Clear existing boxes
    for box in boxes:
        destroy(box)
    boxes = []  # Reset the boxes list

    try:
        with open(filename, 'r') as f:
            game_state = json.load(f)
            for state in game_state:
                add_box(state['position'], state['texture'])
        print("Game loaded!")
    except FileNotFoundError:
        print("No save file found.")

# Create initial boxes
for x in range(20):
    for y in range(20):
        add_box((x, 0, y))

textures = ['Grass2', 'Grass1', 'Path1', 'Stone1', 'Wood2', 'Stone','Wood1', 'Soil1', 'Ice1']
current_texture_index = 0  

def input(key):
    global current_texture_index 
    for box in boxes:
        if box.hovered:
            if key == "left mouse down":
                add_box(box.position + mouse.normal)
            if key == "right mouse down":
                boxes.remove(box)
                destroy(box)
            if key == "e":  # Change texture on 'e' key press
                current_texture_index = (current_texture_index + 1) % len(textures)
                box.texture = textures[current_texture_index]
            if key == "k":  # Save game on 'k' key press
                save_game()
            if key == "l":  # Load game on 'l' key press
                load_game()
app.run()  