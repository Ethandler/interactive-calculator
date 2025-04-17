import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# Monster data
monsters = {
    "Flameo": {"type": "Fire", "hp": 100, "attacks": {"Fireball": 20, "Flare Blast": 25}},
    "AquaDude": {"type": "Water", "hp": 100, "attacks": {"Splash": 15, "Water Cannon": 30}},
    "Leafy": {"type": "Grass", "hp": 100, "attacks": {"Vine Whip": 18, "Leaf Storm": 22}},
    "ElectroCat": {"type": "Electric", "hp": 100, "attacks": {"Zap": 20, "Thunderbolt": 28}}
}

# Battle logic
def battle(attack, player_monster, enemy_monster):
    global player_hp, enemy_hp

    player_attack_power = monsters[player_monster]['attacks'][attack]
    enemy_attack = random.choice(list(monsters[enemy_monster]['attacks'].keys()))
    enemy_attack_power = monsters[enemy_monster]['attacks'][enemy_attack]

    animate_attack(player_label, enemy_label)
    enemy_hp -= player_attack_power
    enemy_hp = max(enemy_hp, 0)
    enemy_hp_label.config(text=f"{enemy_monster} (HP: {enemy_hp})")
    root.update()

    if enemy_hp == 0:
        battle_log.set(f"You used {attack}! {enemy_monster} lost {player_attack_power} HP!\n{enemy_monster} fainted!")
        messagebox.showinfo("Victory!", "You defeated the enemy monster!")
        root.quit()
        return

    battle_log.set(f"You used {attack}! {enemy_monster} lost {player_attack_power} HP!")
    root.update()
    time.sleep(1)

    animate_attack(enemy_label, player_label)
    player_hp -= enemy_attack_power
    player_hp = max(player_hp, 0)
    player_hp_label.config(text=f"{player_monster} (HP: {player_hp})")
    root.update()

    if player_hp == 0:
        battle_log.set(f"{enemy_monster} used {enemy_attack}! You lost {enemy_attack_power} HP!\nYour monster fainted!")
        messagebox.showinfo("Game Over", "Oh no! Your monster fainted!")
        root.quit()
        return

    battle_log.set(f"{enemy_monster} used {enemy_attack}! You lost {enemy_attack_power} HP!")
    root.update()

# Attack animation
def animate_attack(attacker, defender):
    for _ in range(6):
        defender.config(fg=random.choice(["red", "yellow", "blue", "green", "purple"]))
        root.update()
        time.sleep(0.1)
        defender.config(fg="white")
        root.update()
        time.sleep(0.1)

# Start game
def start_game(monster_choice):
    global player_hp, enemy_hp, player_monster, enemy_monster

    player_monster = monster_choice
    enemy_monster = random.choice(list(monsters.keys()))
    while enemy_monster == player_monster:
        enemy_monster = random.choice(list(monsters.keys()))

    player_hp = monsters[player_monster]["hp"]
    enemy_hp = monsters[enemy_monster]["hp"]

    battle_log.set(f"A wild {enemy_monster} appeared!\nChoose your attack!")
    root.update()

    attack1_button.config(
        text=list(monsters[player_monster]['attacks'].keys())[0],
        command=lambda: battle(list(monsters[player_monster]['attacks'].keys())[0], player_monster, enemy_monster)
    )
    attack2_button.config(
        text=list(monsters[player_monster]['attacks'].keys())[1],
        command=lambda: battle(list(monsters[player_monster]['attacks'].keys())[1], player_monster, enemy_monster)
    )

    player_label.config(text=f"{player_monster}")
    enemy_label.config(text=f"{enemy_monster}")
    player_hp_label.config(text=f"{player_monster} (HP: {player_hp})")
    enemy_hp_label.config(text=f"{enemy_monster} (HP: {enemy_hp})")

    attack1_button.pack()
    attack2_button.pack()

    monster_select_frame.pack_forget()
    battle_frame.pack()
    root.update()

# GUI Setup
root = tk.Tk()
root.title("Monster Battle!")
root.geometry("600x400")
root.configure(bg="black")

battle_log = tk.StringVar()
monster_select_frame = tk.Frame(root, bg="black")
monster_select_frame.pack()

tk.Label(monster_select_frame, text="Choose Your Monster!", font=("Arial", 16), fg="white", bg="black").pack()
for monster in monsters.keys():
    tk.Button(monster_select_frame, text=monster, command=lambda m=monster: start_game(m),
              width=20, height=2, bg=random.choice(["red", "blue", "green", "purple", "orange"])).pack(pady=5)

battle_frame = tk.Frame(root, bg="black")
tk.Label(battle_frame, textvariable=battle_log, font=("Arial", 14), fg="white", bg="black").pack()
player_label = tk.Label(battle_frame, font=("Arial", 14), fg="white", bg="black")
player_label.pack()
player_hp_label = tk.Label(battle_frame, font=("Arial", 12), fg="white", bg="black")
player_hp_label.pack()
enemy_label = tk.Label(battle_frame, font=("Arial", 14), fg="white", bg="black")
enemy_label.pack()
enemy_hp_label = tk.Label(battle_frame, font=("Arial", 12), fg="white", bg="black")
enemy_hp_label.pack()
attack1_button = tk.Button(battle_frame, width=20, height=2, bg="red")
attack2_button = tk.Button(battle_frame, width=20, height=2, bg="blue")

root.mainloop()
