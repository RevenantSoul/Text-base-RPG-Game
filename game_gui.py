import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class RPGGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Text RPG Adventure")
        self.root.configure(bg="#1e1e2e")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        self.player_name = "Hero"
        self.hp = 100
        self.gold = 50
        self.inventory = ["Potion", "Wooden Sword"]
        self.weapon = "Wooden Sword"
        self.armor = None

        self.set_theme()
        self.create_game_display()
        self.create_controls()
        self.create_status_panel()

        self.log("🎮 Welcome to the text RPG!")
        self.log("✨ Choose an action to begin your journey.")

    def set_theme(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=6,
            background="#4caf50",
            foreground="white",
            borderwidth=0
        )
        style.map(
            "TButton",
            background=[("active", "#388e3c")],
            foreground=[("disabled", "#aaaaaa")]
        )
        style.configure("TLabel", background="#1e1e2e", foreground="#ffffff")
        style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="#ffeb3b")

    def create_game_display(self):
        self.story_text = tk.Text(
            self.root, height=10, state='disabled', wrap='word',
            bg="#282c34", fg="#e6e6e6", font=("Consolas", 11),
            relief="flat", bd=4, padx=10, pady=10
        )
        self.story_text.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=12, pady=(12, 6))

    def create_controls(self):
        self.button_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.button_frame.grid(row=1, column=0, sticky='nsew', padx=12, pady=(6, 12))

        self.explore_btn = ttk.Button(self.button_frame, text="🌲 Explore", width=12, command=self.explore)
        self.quick_attack_btn = ttk.Button(self.button_frame, text="⚡ Quick Attack", width=12, command=lambda: self.fight("quick"))
        self.heavy_attack_btn = ttk.Button(self.button_frame, text="💥 Heavy Attack", width=12, command=lambda: self.fight("heavy"))
        self.magic_attack_btn = ttk.Button(self.button_frame, text="🔮 Magic Attack", width=12, command=lambda: self.fight("magic"))
        self.quit_btn = ttk.Button(self.button_frame, text="🚪 Quit", width=12, command=self.quit_game)

        self.explore_btn.pack(side='left', padx=6)
        self.quick_attack_btn.pack(side='left', padx=6)
        self.heavy_attack_btn.pack(side='left', padx=6)
        self.magic_attack_btn.pack(side='left', padx=6)
        self.quit_btn.pack(side='left', padx=6)

    def create_status_panel(self):
        self.status_frame = tk.Frame(self.root, bg="#212121", relief="flat", bd=2)
        self.status_frame.grid(row=1, column=1, sticky='nsew', padx=12, pady=(6, 12))

        tk.Label(self.status_frame, text="🎯 STATUS", font=("Segoe UI", 11, "bold"),
                 bg="#212121", fg="#03dac6").pack(pady=(0, 5))

        self.hp_label = ttk.Label(self.status_frame, text=f"❤️ HP: {self.hp}", style="Status.TLabel")
        self.hp_label.pack(anchor='w', padx=10)

        self.gold_label = ttk.Label(self.status_frame, text=f"💰 Gold: {self.gold}", style="Status.TLabel")
        self.gold_label.pack(anchor='w', padx=10)

        self.weapon_label = ttk.Label(self.status_frame, text=f"🗡️ Weapon: {self.weapon}", style="Status.TLabel")
        self.weapon_label.pack(anchor='w', padx=10)

        self.armor_label = ttk.Label(self.status_frame, text=f"🛡️ Armor: {self.armor if self.armor else 'None'}", style="Status.TLabel")
        self.armor_label.pack(anchor='w', padx=10)

        ttk.Label(self.status_frame, text="🎒 Inventory:", style="Status.TLabel").pack(anchor='w', padx=10, pady=(8, 0))

        self.inventory_listbox = tk.Listbox(
            self.status_frame, height=5,
            bg="#303030", fg="#c3f3c3",
            font=("Consolas", 10), relief="flat", bd=2,
            highlightbackground="#444", selectbackground="#607d8b"
        )
        self.inventory_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.refresh_inventory()

    def refresh_inventory(self):
        self.inventory_listbox.delete(0, tk.END)
        colors = ['#ff8a65', '#4dd0e1', '#81c784', '#ffd54f']
        for i, item in enumerate(self.inventory):
            self.inventory_listbox.insert(tk.END, f"• {item}")
            self.inventory_listbox.itemconfig(i, fg=random.choice(colors))

    def update_status(self):
        self.hp_label.config(text=f"❤️ HP: {self.hp}")
        self.gold_label.config(text=f"💰 Gold: {self.gold}")
        self.weapon_label.config(text=f"🗡️ Weapon: {self.weapon}")
        self.armor_label.config(text=f"🛡️ Armor: {self.armor if self.armor else 'None'}")
        self.refresh_inventory()

    def log(self, message):
        def type_text(index=0):
            sub_message = message[:index]
            self.story_text.config(state='normal')
            self.story_text.delete("1.0", tk.END)
            self.story_text.insert(tk.END, sub_message)
            self.story_text.config(state='disabled')
            self.story_text.see(tk.END)

            if index < len(message):
                self.root.after(20, type_text, index + 1)

        type_text(0)

    def get_weapon_damage(self):
        weapon_stats = {
            "Wooden Sword": 3,
            "Stone Sword": 5,
            "Alloy Sword": 7,
            "Magic Sword": 10,
            "Hero Sword": 12
        }
        return weapon_stats.get(self.weapon, 1)

    def get_armor_bonus(self):
        armor_bonuses = {
            "Wooden Armor": 1,
            "Stone Armor": 2,
            "Alloy Armor": 3,
            "Magic Armor": 4,
            "Hero Armor": 5
        }
        return armor_bonuses.get(self.armor, 0)

    def fight(self, attack_type):
        base_damage = self.get_weapon_damage() + self.get_armor_bonus()

        if attack_type == "quick":
            damage = base_damage
            self.hp -= 5
            log_msg = f"⚡ You performed a Quick Attack dealing {damage} damage!"
        elif attack_type == "heavy":
            damage = base_damage + 3
            self.hp -= 5
            log_msg = f"💥 You performed a Heavy Attack dealing {damage} damage!"
        elif attack_type == "magic":
            damage = base_damage + 5
            self.hp -= 5
            log_msg = f"🔮 You unleashed a Magic Attack dealing {damage} damage!" 
        else:
            damage = 1
            log_msg = "❓ Unknown attack type..."

        if self.hp <= 0:
            self.hp = 0
            self.update_status()
            self.log("💀 You have fallen in battle...")
            messagebox.showinfo("Game Over", "You died!")
            self.root.quit()
            return

        self.inventory.append("Goblin Ear")
        self.log(f"{log_msg}\n🧠 You looted a Goblin Ear as a trophy!")
        self.update_status()

    def explore(self):
        rewards = [
            ("gold", random.randint(5, 20)),
            ("Potion", 1),
            ("Wooden Sword", 1),
            ("Stone Sword", 1),
            ("Alloy Sword", 1),
            ("Magic Sword", 1),
            ("Hero Sword", 1),
            ("Wooden Armor", 1),
            ("Stone Armor", 1),
            ("Alloy Armor", 1),
            ("Magic Armor", 1),
            ("Hero Armor", 1),
            ("nothing", 0)
        ]

        reward = random.choice(rewards)

        if reward[0] == "gold":
            self.gold += reward[1]
            self.log(f"🌄 You explored a glowing meadow and found ✨ {reward[1]} gold!")
        elif reward[0] == "nothing":
            self.log("🌫️ You wandered aimlessly and found nothing of interest...")
        else:
            item = reward[0]
            self.inventory.append(item)
            if "Sword" in item:
                self.weapon = item
                self.log(f"🗡️ You equipped a new weapon: {item}!")
            elif "Armor" in item:
                self.armor = item
                self.log(f"🛡️ You equipped new armor: {item}!")
            else:
                self.log(f"🌟 You discovered a {item} and added it to your inventory!")
        self.update_status()

    def quit_game(self):
        self.log("👋 Thanks for playing, adventurer!")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = RPGGame(root)
    root.mainloop()
