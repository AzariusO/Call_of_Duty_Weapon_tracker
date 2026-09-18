import json
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

DB_NAME = "cod_tracker_desktop.db"
MAX_LEVEL = 55
MAX_BP_TIER = 100


class CODTrackerApp:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "Call of Duty Weapon, Prestige & Battle Pass Tracker (Pro Edition)"
    )
    self.root.geometry("1020x1000")

    # Tracking collapsed UI sections
    self.collapsed_sections = {
        "prestige": False,
        "battlepass": False,
        "events": False,
    }

    # Search filter keyword
    self.search_filter = ""

    # Theme Palettes
    self.themes = {
        "MW Dark (Default)": {
            "bg": "#121417",
            "card": "#1c2026",
            "accent": "#ff6b00",
            "text": "#e1e6ed",
            "gold": "#ffd700",
            "card_wep": "#14171c",
        },
        "Cold War Red": {
            "bg": "#140f0f",
            "card": "#241a1a",
            "accent": "#ff3333",
            "text": "#f0e6e6",
            "gold": "#ffd700",
            "card_wep": "#1a1212",
        },
        "Vanguard Gold": {
            "bg": "#12110e",
            "card": "#211e18",
            "accent": "#d4af37",
            "text": "#f5f3e9",
            "gold": "#ffae00",
            "card_wep": "#171510",
        },
        "Tactical Matrix": {
            "bg": "#0a120b",
            "card": "#122114",
            "accent": "#00ff66",
            "text": "#e0f5e5",
            "gold": "#ffff00",
            "card_wep": "#0d170e",
        },
        "Zombies Dark Matter": {
            "bg": "#0f0814",
            "card": "#1d1026",
            "accent": "#d946ef",
            "text": "#f3e8ff",
            "gold": "#a855f7",
            "card_wep": "#140b1c",
        },
        "Ghost Modern Warfare": {
            "bg": "#0f172a",
            "card": "#1e293b",
            "accent": "#38bdf8",
            "text": "#f1f5f9",
            "gold": "#e2e8f0",
            "card_wep": "#111827",
        },
        "Warzone Verdansk": {
            "bg": "#111612",
            "card": "#1c241e",
            "accent": "#84cc16",
            "text": "#ecfccb",
            "gold": "#eab308",
            "card_wep": "#141a15",
        },
        "80s Synthwave": {
            "bg": "#180b24",
            "card": "#28133d",
            "accent": "#06b6d4",
            "text": "#fdf4ff",
            "gold": "#f43f5e",
            "card_wep": "#1f0e2e",
        },
        "MW II Lime": {
            "bg": "#0d0f0d",
            "card": "#181c18",
            "accent": "#10b981",
            "text": "#e6f4ea",
            "gold": "#facc15",
            "card_wep": "#121412",
        },
        "Solar Flare": {
            "bg": "#1a0c0c",
            "card": "#2e1212",
            "accent": "#f97316",
            "text": "#fef2f2",
            "gold": "#fef08a",
            "card_wep": "#210e0e",
        },
        "Cyberpunk Neon": {
            "bg": "#0d0814",
            "card": "#1a1028",
            "accent": "#f43f5e",
            "text": "#f8fafc",
            "gold": "#38bdf8",
            "card_wep": "#130b1e",
        },
        "Desert Stealth": {
            "bg": "#171412",
            "card": "#26211d",
            "accent": "#d97706",
            "text": "#fef3c7",
            "gold": "#f59e0b",
            "card_wep": "#1c1815",
        },
        "Ocean Ops": {
            "bg": "#071318",
            "card": "#0f232c",
            "accent": "#14b8a6",
            "text": "#ccfbf1",
            "gold": "#38bdf8",
            "card_wep": "#0a1920",
        },
        "Monochrome Elite": {
            "bg": "#0f0f0f",
            "card": "#1f1f1f",
            "accent": "#ffffff",
            "text": "#e5e5e5",
            "gold": "#a3a3a3",
            "card_wep": "#171717",
        },
        "B.O. Cold Orange": {
            "bg": "#18100a",
            "card": "#2b1c10",
            "accent": "#ff7700",
            "text": "#fbebe0",
            "gold": "#ffb700",
            "card_wep": "#20140b",
        },
        "MW3 Crimson": {
            "bg": "#1a0808",
            "card": "#2e1010",
            "accent": "#dc2626",
            "text": "#fee2e2",
            "gold": "#f59e0b",
            "card_wep": "#220a0a",
        },
        "Zombies Aether Purple": {
            "bg": "#13091c",
            "card": "#241236",
            "accent": "#a855f7",
            "text": "#f3e8ff",
            "gold": "#ec4899",
            "card_wep": "#1a0b28",
        },
        "Night Vision Goggles": {
            "bg": "#031405",
            "card": "#072b0c",
            "accent": "#22c55e",
            "text": "#dcfce7",
            "gold": "#86efac",
            "card_wep": "#051f08",
        },
        "Thermal Vision White Hot": {
            "bg": "#050505",
            "card": "#18181b",
            "accent": "#f4f4f5",
            "text": "#ffffff",
            "gold": "#a1a1aa",
            "card_wep": "#0f0f11",
        },
        "Rust Sandstorm": {
            "bg": "#1c1510",
            "card": "#2e2219",
            "accent": "#ea580c",
            "text": "#ffedd5",
            "gold": "#facc15",
            "card_wep": "#241b13",
        },
        "Shipment Container Green": {
            "bg": "#0c1713",
            "card": "#172b23",
            "accent": "#10b981",
            "text": "#d1fae5",
            "gold": "#fbbf24",
            "card_wep": "#11211b",
        },
        "Nuketown 84": {
            "bg": "#1c0d18",
            "card": "#33152c",
            "accent": "#ec4899",
            "text": "#fce7f3",
            "gold": "#06b6d4",
            "card_wep": "#260e21",
        },
        "Warzone Caldera": {
            "bg": "#0d1a12",
            "card": "#172e20",
            "accent": "#65a30d",
            "text": "#ecfccb",
            "gold": "#eab308",
            "card_wep": "#112419",
        },
        "Retrowave Sunset": {
            "bg": "#160b24",
            "card": "#28123d",
            "accent": "#f43f5e",
            "text": "#fff1f2",
            "gold": "#fbbf24",
            "card_wep": "#1e0e30",
        },
        "Blood Diamond": {
            "bg": "#170509",
            "card": "#2e0b12",
            "accent": "#e11d48",
            "text": "#ffe4e6",
            "gold": "#fb7185",
            "card_wep": "#21070d",
        },
        "Emerald Ordnance": {
            "bg": "#061712",
            "card": "#0c2e24",
            "accent": "#059669",
            "text": "#d1fae5",
            "gold": "#34d399",
            "card_wep": "#09211a",
        },
        "Amethyst Crystal": {
            "bg": "#13091d",
            "card": "#251238",
            "accent": "#9333ea",
            "text": "#faf5ff",
            "gold": "#c084fc",
            "card_wep": "#1a0b29",
        },
        "Titanium Silver": {
            "bg": "#111318",
            "card": "#1f242d",
            "accent": "#94a3b8",
            "text": "#f8fafc",
            "gold": "#cbd5e1",
            "card_wep": "#171a21",
        },
        "Stealth Bomber Dark": {
            "bg": "#090a0f",
            "card": "#12141d",
            "accent": "#64748b",
            "text": "#e2e8f0",
            "gold": "#38bdf8",
            "card_wep": "#0d0e14",
        },
        "Solarized Dark": {
            "bg": "#002b36",
            "card": "#073642",
            "accent": "#b58900",
            "text": "#839496",
            "gold": "#cb4b16",
            "card_wep": "#00212b",
        },
        "Nord Frost": {
            "bg": "#2e3440",
            "card": "#3b4252",
            "accent": "#88c0d0",
            "text": "#eceff4",
            "gold": "#ebcb8b",
            "card_wep": "#353b49",
        },
        "Dracula Castle": {
            "bg": "#282a36",
            "card": "#44475a",
            "accent": "#ff79c6",
            "text": "#f8f8f2",
            "gold": "#bd93f9",
            "card_wep": "#343746",
        },
        "Pastel Tactical": {
            "bg": "#181a1b",
            "card": "#242729",
            "accent": "#f4a261",
            "text": "#e8e6e3",
            "gold": "#e76f51",
            "card_wep": "#1d2021",
        },
        "Cyber Punk 2077": {
            "bg": "#121100",
            "card": "#262400",
            "accent": "#facc15",
            "text": "#fefce8",
            "gold": "#06b6d4",
            "card_wep": "#1c1a00",
        },
    }
    self.current_theme = "MW Dark (Default)"

    self.set_theme_colors(self.current_theme)
    self.init_db()
    self.build_ui()
    self.apply_theme(self.current_theme)
    self.load_categories_into_dropdown()
    self.load_battle_passes()
    self.refresh_display()
    self.refresh_events()

  # --- DATABASE SETUP ---
  def init_db(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS weapons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                level INTEGER DEFAULT 1,
                max_level INTEGER DEFAULT 50,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weapon_id INTEGER,
                description TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (weapon_id) REFERENCES weapons (id) ON DELETE CASCADE
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                prestige INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            )
        """)
    # Updated events table to support nested categories & sub-quests
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER,
                name TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (parent_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS battle_passes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                bp_tier INTEGER DEFAULT 0,
                bp_tokens INTEGER DEFAULT 0,
                bp_sector INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 0
            )
        """)

    cursor.execute(
        "INSERT OR IGNORE INTO user_progress (id, prestige, level) VALUES (1,"
        " 0, 1)"
    )

    cursor.execute("SELECT COUNT(*) FROM battle_passes")
    if cursor.fetchone()[0] == 0:
      cursor.execute(
          "INSERT INTO battle_passes (name, bp_tier, bp_tokens, bp_sector,"
          " is_active) VALUES ('Season 1', 0, 0, 0, 1)"
      )

    conn.commit()
    conn.close()

  # --- THEME MANAGEMENT ---
  def set_theme_colors(self, theme_name):
    t = self.themes[theme_name]
    self.bg_color = t["bg"]
    self.card_bg = t["card"]
    self.accent_color = t["accent"]
    self.text_color = t["text"]
    self.gold_color = t["gold"]
    self.wep_card_bg = t["card_wep"]

  def apply_theme(self, theme_name):
    self.current_theme = theme_name
    self.set_theme_colors(theme_name)

    self.root.configure(bg=self.bg_color)
    if hasattr(self, "canvas"):
      self.canvas.configure(bg=self.bg_color)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background=self.bg_color)
    style.configure("Card.TFrame", background=self.card_bg)
    style.configure(
        "TLabel",
        background=self.bg_color,
        foreground=self.text_color,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Header.TLabel",
        font=("Segoe UI", 16, "bold"),
        foreground=self.accent_color,
        background=self.bg_color,
    )

    style.configure(
        "Accent.TButton",
        background=self.accent_color,
        foreground="black",
        font=("Segoe UI", 9, "bold"),
    )
    style.map("Accent.TButton", background=[("active", self.accent_color)])

    if hasattr(self, "prestige_card"):
      self.update_prestige_ui()
    if hasattr(self, "bp_card"):
      self.update_battlepass_ui()
    if hasattr(self, "scrollable_frame"):
      self.refresh_display()
    if hasattr(self, "events_container"):
      self.refresh_events()

  # --- PRESTIGE TRACKER LOGIC ---
  def toggle_prestige_collapse(self):
    self.collapsed_sections["prestige"] = not self.collapsed_sections[
        "prestige"
    ]
    if self.collapsed_sections["prestige"]:
      self.p_body_frame.pack_forget()
      self.p_toggle_btn.configure(text="[+] Expand")
    else:
      self.p_body_frame.pack(fill="x", padx=15, pady=(2, 6))
      self.p_toggle_btn.configure(text="[-] Minimize")

  def get_user_data(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT prestige, level FROM user_progress WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return row if row else (0, 1)

  def update_prestige_db(self, prestige, level):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_progress SET prestige = ?, level = ? WHERE id = 1",
        (prestige, level),
    )
    conn.commit()
    conn.close()
    self.update_prestige_ui()

  def change_level(self, amount):
    p, l = self.get_user_data()
    self.update_prestige_db(p, max(1, min(MAX_LEVEL, l + amount)))

  def reset_level(self):
    p, _ = self.get_user_data()
    if messagebox.askyesno("Reset Level?", "Reset your level back to Level 1?"):
      self.update_prestige_db(p, 1)

  def advance_prestige(self):
    p, l = self.get_user_data()
    if l < MAX_LEVEL and not messagebox.askyesno(
        "Prestige Early?",
        f"You are Level {l}. Advance to Prestige {p + 1}?",
    ):
      return
    self.update_prestige_db(p + 1, 1)

  def revert_prestige(self):
    p, l = self.get_user_data()
    if p <= 0:
      messagebox.showinfo("Info", "Already at Prestige 0.")
      return
    if messagebox.askyesno(
        "Revert Prestige", f"Go back from Prestige {p} to Prestige {p - 1}?"
    ):
      self.update_prestige_db(p - 1, l)

  def update_prestige_ui(self):
    p, l = self.get_user_data()
    self.prestige_card.configure(bg=self.card_bg)
    self.rank_title_lbl.configure(
        bg=self.card_bg,
        fg=self.gold_color if p > 0 else self.accent_color,
        text=f"🎖 PRESTIGE TRACKER (Prestige {p} | Level {l}/{MAX_LEVEL})",
    )
    self.level_progress["value"] = l

  # --- BATTLE PASS MANAGEMENT & LOGIC ---
  def toggle_bp_collapse(self):
    self.collapsed_sections["battlepass"] = not self.collapsed_sections[
        "battlepass"
    ]
    if self.collapsed_sections["battlepass"]:
      self.bp_body_frame.pack_forget()
      self.bp_toggle_btn.configure(text="[+] Expand")
    else:
      self.bp_body_frame.pack(fill="x", padx=15, pady=(2, 6))
      self.bp_toggle_btn.configure(text="[-] Minimize")

  def get_active_bp(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, bp_tier, bp_tokens, bp_sector FROM battle_passes"
        " WHERE is_active = 1 LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    return row

  def load_battle_passes(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM battle_passes ORDER BY id ASC")
    passes = cursor.fetchall()
    conn.close()

    self.bp_map = {name: b_id for b_id, name in passes}
    self.bp_selector["values"] = list(self.bp_map.keys())

    active = self.get_active_bp()
    if active:
      self.bp_selector.set(active[1])
    elif passes:
      self.bp_selector.set(passes[0][1])

    self.update_battlepass_ui()

  def switch_battle_pass(self, event=None):
    selected_name = self.bp_selector.get()
    if selected_name not in self.bp_map:
      return

    bp_id = self.bp_map[selected_name]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE battle_passes SET is_active = 0")
    cursor.execute(
        "UPDATE battle_passes SET is_active = 1 WHERE id = ?", (bp_id,)
    )
    conn.commit()
    conn.close()
    self.update_battlepass_ui()

  def create_new_bp(self):
    name = simpledialog.askstring(
        "New Battle Pass", "Enter a name for the new Battle Pass:"
    )
    if not name or not name.strip():
      return

    name = name.strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE battle_passes SET is_active = 0")
    cursor.execute(
        "INSERT INTO battle_passes (name, bp_tier, bp_tokens, bp_sector,"
        " is_active) VALUES (?, 0, 0, 0, 1)",
        (name,),
    )
    conn.commit()
    conn.close()

    self.load_battle_passes()

  def rename_active_bp(self):
    active = self.get_active_bp()
    if not active:
      return
    bp_id, old_name, _, _, _ = active

    new_name = simpledialog.askstring(
        "Rename Battle Pass",
        f"Enter new name for '{old_name}':",
        initialvalue=old_name,
    )
    if not new_name or not new_name.strip() or new_name.strip() == old_name:
      return

    new_name = new_name.strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE battle_passes SET name = ? WHERE id = ?", (new_name, bp_id)
    )
    conn.commit()
    conn.close()

    self.load_battle_passes()

  def delete_active_bp(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM battle_passes")
    total = cursor.fetchone()[0]

    if total <= 1:
      messagebox.showwarning(
          "Action Blocked",
          "You must keep at least one Battle Pass in your list.",
      )
      conn.close()
      return

    active = self.get_active_bp()
    if not active:
      conn.close()
      return
    bp_id, name, _, _, _ = active

    if messagebox.askyesno(
        "Delete Battle Pass?",
        f"Are you sure you want to permanently delete Battle Pass '{name}'?",
    ):
      cursor.execute("DELETE FROM battle_passes WHERE id = ?", (bp_id,))
      cursor.execute(
          "UPDATE battle_passes SET is_active = 1 WHERE id = (SELECT id FROM"
          " battle_passes LIMIT 1)"
      )
      conn.commit()
      conn.close()
      self.load_battle_passes()
    else:
      conn.close()

  def update_bp_db(self, tier, tokens, sector):
    active = self.get_active_bp()
    if not active:
      return
    bp_id = active[0]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE battle_passes SET bp_tier = ?, bp_tokens = ?, bp_sector = ?"
        " WHERE id = ?",
        (tier, tokens, sector, bp_id),
    )
    conn.commit()
    conn.close()
    self.update_battlepass_ui()

  def change_bp_tier(self, amount):
    active = self.get_active_bp()
    if not active:
      return
    _, _, t, tok, sec = active
    self.update_bp_db(max(0, min(MAX_BP_TIER, t + amount)), tok, sec)

  def change_bp_tokens(self, amount):
    active = self.get_active_bp()
    if not active:
      return
    _, _, t, tok, sec = active
    self.update_bp_db(t, max(0, tok + amount), sec)

  def change_bp_sector(self, amount):
    active = self.get_active_bp()
    if not active:
      return
    _, _, t, tok, sec = active
    self.update_bp_db(t, tok, max(0, min(20, sec + amount)))

  def reset_bp(self):
    if messagebox.askyesno(
        "Reset Battle Pass?",
        "Are you sure you want to reset this Battle Pass progress back to 0?",
    ):
      self.update_bp_db(0, 0, 0)

  def update_battlepass_ui(self):
    active = self.get_active_bp()
    if not active:
      return
    _, name, tier, tokens, sector = active

    self.bp_card.configure(bg=self.card_bg)
    self.bp_title_lbl.configure(
        bg=self.card_bg,
        fg=self.gold_color if tier == MAX_BP_TIER else self.accent_color,
        text=(
            f"⚡ BATTLE PASS: {name.upper()} COMPLETE!"
            if tier == MAX_BP_TIER
            else f"⚡ BATTLE PASS: {name.upper()} (Tier {tier}/{MAX_BP_TIER})"
        ),
    )
    self.bp_sub_lbl.configure(
        bg=self.card_bg,
        fg=self.text_color,
        text=f"Sectors: {sector}/20 | Tokens: {tokens}",
    )
    self.bp_progress["value"] = tier

  # --- WEAPON LOGIC ---
  def change_weapon_level(self, weapon_id, delta):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT level, max_level FROM weapons WHERE id = ?", (weapon_id,)
    )
    row = cursor.fetchone()
    if row:
      current, max_lvl = row
      new_lvl = max(1, min(max_lvl, current + delta))
      cursor.execute(
          "UPDATE weapons SET level = ? WHERE id = ?", (new_lvl, weapon_id)
      )
      conn.commit()
    conn.close()
    self.refresh_display()

  def set_custom_max_level(self, weapon_id, weapon_name, current_max):
    new_max = simpledialog.askinteger(
        "Max Weapon Level",
        f"Set Max Level for '{weapon_name}':",
        initialvalue=current_max,
        minvalue=1,
        maxvalue=100,
    )
    if new_max is not None:
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute(
          "UPDATE weapons SET max_level = ?, level = MIN(level, ?) WHERE id ="
          " ?",
          (new_max, new_max, weapon_id),
      )
      conn.commit()
      conn.close()
      self.refresh_display()

  # --- EVENTS AND HIERARCHICAL QUESTS LOGIC ---
  def toggle_events_collapse(self):
    self.collapsed_sections["events"] = not self.collapsed_sections["events"]
    if self.collapsed_sections["events"]:
      self.events_body_frame.pack_forget()
      self.ev_toggle_btn.configure(text="[+] Expand")
    else:
      self.events_body_frame.pack(fill="x", padx=10, pady=2)
      self.ev_toggle_btn.configure(text="[-] Minimize")

  def load_event_categories_into_dropdown(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM events WHERE parent_id IS NULL")
    cats = cursor.fetchall()
    conn.close()

    self.event_cat_map = {name: c_id for c_id, name in cats}
    self.event_cat_dropdown["values"] = list(self.event_cat_map.keys())
    if cats:
      self.event_cat_dropdown.set(cats[0][1])
    else:
      self.event_cat_dropdown.set("")

  def add_event_category(self):
    cat_name = self.event_entry.get().strip()
    if not cat_name:
      messagebox.showwarning("Warning", "Enter a Quest Category name.")
      return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
      cursor.execute(
          "INSERT INTO events (parent_id, name, completed) VALUES (NULL, ?, 0)",
          (cat_name,),
      )
      conn.commit()
    except Exception as e:
      messagebox.showerror("Error", f"Could not add category: {e}")
    conn.close()

    self.event_entry.delete(0, tk.END)
    self.load_event_categories_into_dropdown()
    self.refresh_events()

  def add_sub_event(self):
    selected_cat_name = self.event_cat_dropdown.get()
    sub_name = self.event_sub_entry.get().strip()

    if not selected_cat_name or not sub_name:
      messagebox.showwarning(
          "Warning", "Select a category and enter a sub-quest description."
      )
      return

    parent_id = self.event_cat_map.get(selected_cat_name)
    if not parent_id:
      return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (parent_id, name, completed) VALUES (?, ?, 0)",
        (parent_id, sub_name),
    )
    conn.commit()
    conn.close()

    self.event_sub_entry.delete(0, tk.END)
    self.refresh_events()

  def toggle_event(self, event_id, var):
    completed = var.get()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Update target quest and cascade completion downwards if it's a category
    cursor.execute(
        "UPDATE events SET completed = ? WHERE id = ? OR parent_id = ?",
        (1 if completed else 0, event_id, event_id),
    )
    conn.commit()
    conn.close()
    self.refresh_events()

  def remove_event_item(self, event_id, name, is_category):
    item_type = "Category and its sub-quests" if is_category else "Sub-quest"
    if messagebox.askyesno(
        "Confirm Delete", f"Are you sure you want to delete {item_type} '{name}'?"
    ):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON;")
      cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
      conn.commit()
      conn.close()
      self.load_event_categories_into_dropdown()
      self.refresh_events()

  def refresh_events(self):
    for widget in self.events_container.winfo_children():
      widget.destroy()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Fetch main categories
    cursor.execute("SELECT id, name, completed FROM events WHERE parent_id IS NULL")
    categories = cursor.fetchall()
    conn.close()

    if not categories:
      tk.Label(
          self.events_container,
          text=(
              "No quest categories found. Add a category above, then add"
              " sub-quests!"
          ),
          font=("Segoe UI", 9, "italic"),
          bg=self.card_bg,
          fg="#8a99ad",
      ).pack(anchor="w", padx=10, pady=5)
      self.load_event_categories_into_dropdown()
      return

    for cat_id, cat_name, cat_completed in categories:
      cat_frame = tk.Frame(
          self.events_container,
          bg=self.wep_card_bg,
          bd=1,
          relief="solid",
          highlightbackground="#2e3540",
          highlightthickness=1,
      )
      cat_frame.pack(fill="x", padx=5, pady=4, ipady=2)

      cat_header = tk.Frame(cat_frame, bg=self.wep_card_bg)
      cat_header.pack(fill="x", padx=8, pady=3)

      cat_var = tk.BooleanVar(value=bool(cat_completed))
      cat_chk = tk.Checkbutton(
          cat_header,
          text=cat_name.upper(),
          variable=cat_var,
          bg=self.wep_card_bg,
          fg="#8a99ad" if cat_completed else self.accent_color,
          font=(
              "Segoe UI",
              9,
              "bold overstrike" if cat_completed else "bold",
          ),
          selectcolor="#0d0f12",
          activebackground=self.wep_card_bg,
          activeforeground=self.accent_color,
          command=lambda cid=cat_id, v=cat_var: self.toggle_event(cid, v),
      )
      cat_chk.pack(side="left")

      tk.Button(
          cat_header,
          text="🗑 Delete Category",
          font=("Segoe UI", 7, "bold"),
          bg="#2e3540",
          fg="#d9534f",
          bd=0,
          cursor="hand2",
          command=lambda cid=cat_id, cname=cat_name: self.remove_event_item(
              cid, cname, True
          ),
      ).pack(side="right", padx=5)

      # Fetch sub-quests for this category
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute(
          "SELECT id, name, completed FROM events WHERE parent_id = ?", (cat_id,)
      )
      sub_quests = cursor.fetchall()
      conn.close()

      sub_container = tk.Frame(cat_frame, bg=self.wep_card_bg)
      sub_container.pack(fill="x", padx=20, pady=(0, 3))

      if not sub_quests:
        tk.Label(
            sub_container,
            text="No sub-quests added yet.",
            font=("Segoe UI", 8, "italic"),
            bg=self.wep_card_bg,
            fg="#8a99ad",
        ).pack(anchor="w", padx=5, pady=2)
      else:
        for sub_id, sub_name, sub_completed in sub_quests:
          sub_item_frame = tk.Frame(sub_container, bg=self.wep_card_bg)
          sub_item_frame.pack(fill="x", pady=1)

          sub_var = tk.BooleanVar(value=bool(sub_completed))
          sub_chk = tk.Checkbutton(
              sub_item_frame,
              text=sub_name,
              variable=sub_var,
              bg=self.wep_card_bg,
              fg="#8a99ad" if sub_completed else self.text_color,
              font=("Segoe UI", 9, "overstrike" if sub_completed else "normal"),
              selectcolor="#0d0f12",
              activebackground=self.wep_card_bg,
              activeforeground=self.text_color,
              command=lambda sid=sub_id, v=sub_var: self.toggle_event(sid, v),
          )
          sub_chk.pack(side="left")

          tk.Button(
              sub_item_frame,
              text="✕",
              font=("Segoe UI", 8, "bold"),
              bg=self.wep_card_bg,
              fg="#d9534f",
              bd=0,
              cursor="hand2",
              command=lambda sid=sub_id, sname=sub_name: self.remove_event_item(
                  sid, sname, False
              ),
          ).pack(side="right", padx=5)

    self.load_event_categories_into_dropdown()

  # --- BACKUP & RESTORE DATA (JSON) ---
  def export_backup(self):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Export Tracker Backup",
    )
    if not file_path:
      return

    try:
      conn = sqlite3.connect(DB_NAME)
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()

      data = {}
      for table in [
          "categories",
          "weapons",
          "challenges",
          "user_progress",
          "events",
          "battle_passes",
      ]:
        cursor.execute(f"SELECT * FROM {table}")
        data[table] = [dict(row) for row in cursor.fetchall()]

      conn.close()

      with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

      messagebox.showinfo("Success", "Backup exported successfully!")
    except Exception as e:
      messagebox.showerror("Error", f"Failed to export backup:\n{e}")

  def import_backup(self):
    if not messagebox.askyesno(
        "Import Backup",
        "Importing a backup will overwrite your current database progress."
        " Continue?",
    ):
      return

    file_path = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Import Tracker Backup",
    )
    if not file_path:
      return

    try:
      with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = OFF;")

      for table in [
          "challenges",
          "weapons",
          "categories",
          "user_progress",
          "events",
          "battle_passes",
      ]:
        cursor.execute(f"DELETE FROM {table}")

        if table in data and data[table]:
          keys = data[table][0].keys()
          cols = ", ".join(keys)
          placeholders = ", ".join(["?" for _ in keys])
          for row in data[table]:
            cursor.execute(
                f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
                list(row.values()),
            )

      cursor.execute("PRAGMA foreign_keys = ON;")
      conn.commit()
      conn.close()

      self.load_categories_into_dropdown()
      self.load_battle_passes()
      self.load_event_categories_into_dropdown()
      self.refresh_display()
      self.refresh_events()
      messagebox.showinfo("Success", "Backup imported successfully!")
    except Exception as e:
      messagebox.showerror("Error", f"Failed to import backup:\n{e}")

  # --- STATISTICS WINDOW ---
  def open_stats_window(self):
    stats_win = tk.Toplevel(self.root)
    stats_win.title("Global Tracking Statistics")
    stats_win.geometry("400x350")
    stats_win.configure(bg=self.card_bg)
    stats_win.grab_set()

    tk.Label(
        stats_win,
        text="📊 GLOBAL STATS & METRICS",
        font=("Segoe UI", 12, "bold"),
        bg=self.card_bg,
        fg=self.accent_color,
    ).pack(pady=15)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM weapons")
    total_weps = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categories")
    total_cats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM challenges")
    total_ch = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM challenges WHERE completed = 1")
    done_ch = cursor.fetchone()[0]

    cursor.execute("SELECT prestige, level FROM user_progress WHERE id = 1")
    p_row = cursor.fetchone()
    prestige, level = p_row if p_row else (0, 1)

    conn.close()

    ch_percent = int((done_ch / total_ch * 100)) if total_ch > 0 else 0

    frame = tk.Frame(stats_win, bg=self.card_bg)
    frame.pack(fill="both", expand=True, padx=25, pady=5)

    labels = [
        ("Current Rank/Prestige:", f"Prestige {prestige} (Level {level})"),
        ("Total Categories:", f"{total_cats}"),
        ("Total Tracked Weapons:", f"{total_weps}"),
        ("Total Challenges:", f"{total_ch}"),
        ("Challenges Completed:", f"{done_ch} ({ch_percent}%)"),
    ]

    for label_text, val_text in labels:
      row_f = tk.Frame(frame, bg=self.card_bg)
      row_f.pack(fill="x", pady=6)
      tk.Label(
          row_f,
          text=label_text,
          font=("Segoe UI", 10, "bold"),
          bg=self.card_bg,
          fg=self.text_color,
      ).pack(side="left")
      tk.Label(
          row_f,
          text=val_text,
          font=("Segoe UI", 10),
          bg=self.card_bg,
          fg=self.gold_color,
      ).pack(side="right")

    tk.Button(
        stats_win,
        text="Close",
        bg=self.accent_color,
        fg="black",
        font=("Segoe UI", 9, "bold"),
        command=stats_win.destroy,
    ).pack(pady=15)

  # --- UI CONSTRUCTION ---
  def build_ui(self):
    header_frame = ttk.Frame(self.root)
    header_frame.pack(fill="x", padx=20, pady=(15, 5))

    ttk.Label(
        header_frame, text="WEAPON PROGRESS TRACKER", style="Header.TLabel"
    ).pack(side="left")

    theme_frame = ttk.Frame(header_frame)
    theme_frame.pack(side="right")

    # Stats & Backup Buttons
    tk.Button(
        theme_frame,
        text="📊 Stats",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg=self.gold_color,
        bd=0,
        cursor="hand2",
        command=self.open_stats_window,
    ).pack(side="left", padx=4)
    tk.Button(
        theme_frame,
        text="💾 Export",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#38bdf8",
        bd=0,
        cursor="hand2",
        command=self.export_backup,
    ).pack(side="left", padx=2)
    tk.Button(
        theme_frame,
        text="📂 Import",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#00ff66",
        bd=0,
        cursor="hand2",
        command=self.import_backup,
    ).pack(side="left", padx=2)

    ttk.Label(theme_frame, text="  Theme: ").pack(side="left")
    self.theme_dropdown = ttk.Combobox(
        theme_frame,
        state="readonly",
        values=sorted(list(self.themes.keys())),
        width=20,
    )
    self.theme_dropdown.set(self.current_theme)
    self.theme_dropdown.bind(
        "<<ComboboxSelected>>",
        lambda e: self.apply_theme(self.theme_dropdown.get()),
    )
    self.theme_dropdown.pack(side="left")

    # Prestige Banner
    self.prestige_card = tk.Frame(self.root, bg=self.card_bg, bd=1, relief="solid")
    self.prestige_card.pack(fill="x", padx=20, pady=(5, 5), ipady=2)

    p_header_frame = tk.Frame(self.prestige_card, bg=self.card_bg)
    p_header_frame.pack(fill="x", padx=15, pady=4)

    self.rank_title_lbl = tk.Label(
        p_header_frame, font=("Segoe UI", 10, "bold"), anchor="w"
    )
    self.rank_title_lbl.pack(side="left")

    self.p_toggle_btn = tk.Button(
        p_header_frame,
        text="[-] Minimize",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=self.toggle_prestige_collapse,
    )
    self.p_toggle_btn.pack(side="right")

    self.p_body_frame = tk.Frame(self.prestige_card, bg=self.card_bg)
    self.p_body_frame.pack(fill="x", padx=15, pady=(2, 6))

    p_bar_frame = tk.Frame(self.p_body_frame, bg=self.card_bg)
    p_bar_frame.pack(side="left", fill="x", expand=True, padx=(0, 15))
    self.level_progress = ttk.Progressbar(
        p_bar_frame, orient="horizontal", maximum=MAX_LEVEL, mode="determinate"
    )
    self.level_progress.pack(fill="x", expand=True)

    p_ctrl_frame = tk.Frame(self.p_body_frame, bg=self.card_bg)
    p_ctrl_frame.pack(side="right")

    tk.Button(
        p_ctrl_frame,
        text="-1 Lvl",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_level(-1),
    ).pack(side="left", padx=2)
    tk.Button(
        p_ctrl_frame,
        text="+1 Lvl",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_level(1),
    ).pack(side="left", padx=2)
    tk.Button(
        p_ctrl_frame,
        text="+5 Lvl",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_level(5),
    ).pack(side="left", padx=2)
    tk.Button(
        p_ctrl_frame,
        text="↺ Reset",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#ff9999",
        bd=0,
        cursor="hand2",
        command=self.reset_level,
    ).pack(side="left", padx=(4, 2))
    tk.Button(
        p_ctrl_frame,
        text="-1 Prestige",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#ffcc66",
        bd=0,
        cursor="hand2",
        command=self.revert_prestige,
    ).pack(side="left", padx=2)
    tk.Button(
        p_ctrl_frame,
        text="🎖 Prestige",
        font=("Segoe UI", 8, "bold"),
        bg=self.gold_color,
        fg="black",
        bd=0,
        cursor="hand2",
        command=self.advance_prestige,
    ).pack(side="left", padx=(4, 0))

    # --- BATTLE PASS TRACKER BANNER ---
    self.bp_card = tk.Frame(self.root, bg=self.card_bg, bd=1, relief="solid")
    self.bp_card.pack(fill="x", padx=20, pady=(5, 5), ipady=2)

    bp_header_frame = tk.Frame(self.bp_card, bg=self.card_bg)
    bp_header_frame.pack(fill="x", padx=15, pady=4)

    self.bp_title_lbl = tk.Label(
        bp_header_frame, font=("Segoe UI", 10, "bold"), anchor="w"
    )
    self.bp_title_lbl.pack(side="left")

    self.bp_toggle_btn = tk.Button(
        bp_header_frame,
        text="[-] Minimize",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=self.toggle_bp_collapse,
    )
    self.bp_toggle_btn.pack(side="right")

    self.bp_body_frame = tk.Frame(self.bp_card, bg=self.card_bg)
    self.bp_body_frame.pack(fill="x", padx=15, pady=(2, 6))

    bp_menu_bar = tk.Frame(self.bp_body_frame, bg=self.card_bg)
    bp_menu_bar.pack(fill="x", pady=(2, 4))

    tk.Label(
        bp_menu_bar,
        text="Active Pass:",
        font=("Segoe UI", 9, "bold"),
        bg=self.card_bg,
        fg=self.text_color,
    ).pack(side="left", padx=(0, 5))

    self.bp_selector = ttk.Combobox(bp_menu_bar, state="readonly", width=18)
    self.bp_selector.pack(side="left", padx=(0, 5))
    self.bp_selector.bind("<<ComboboxSelected>>", self.switch_battle_pass)

    tk.Button(
        bp_menu_bar,
        text="+ New Pass",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#00ff66",
        bd=0,
        cursor="hand2",
        command=self.create_new_bp,
    ).pack(side="left", padx=2)
    tk.Button(
        bp_menu_bar,
        text="✏️ Rename",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#38bdf8",
        bd=0,
        cursor="hand2",
        command=self.rename_active_bp,
    ).pack(side="left", padx=2)
    tk.Button(
        bp_menu_bar,
        text="🗑 Delete Pass",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#d9534f",
        bd=0,
        cursor="hand2",
        command=self.delete_active_bp,
    ).pack(side="left", padx=2)

    bp_main_frame = tk.Frame(self.bp_body_frame, bg=self.card_bg)
    bp_main_frame.pack(fill="x", pady=(2, 2))

    bp_info_frame = tk.Frame(bp_main_frame, bg=self.card_bg)
    bp_info_frame.pack(side="left")
    self.bp_sub_lbl = tk.Label(bp_info_frame, font=("Segoe UI", 8), anchor="w")
    self.bp_sub_lbl.pack(anchor="w")

    bp_bar_frame = tk.Frame(bp_main_frame, bg=self.card_bg)
    bp_bar_frame.pack(side="left", fill="x", expand=True, padx=15)
    self.bp_progress = ttk.Progressbar(
        bp_bar_frame, orient="horizontal", maximum=MAX_BP_TIER, mode="determinate"
    )
    self.bp_progress.pack(fill="x", expand=True)

    bp_ctrl_frame = tk.Frame(bp_main_frame, bg=self.card_bg)
    bp_ctrl_frame.pack(side="right")

    tk.Button(
        bp_ctrl_frame,
        text="-5",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#ff9999",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_tier(-5),
    ).pack(side="left", padx=1)
    tk.Button(
        bp_ctrl_frame,
        text="-1 Tier",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_tier(-1),
    ).pack(side="left", padx=2)
    tk.Button(
        bp_ctrl_frame,
        text="+1 Tier",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_tier(1),
    ).pack(side="left", padx=2)
    tk.Button(
        bp_ctrl_frame,
        text="+5 Tiers",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_tier(5),
    ).pack(side="left", padx=2)
    tk.Button(
        bp_ctrl_frame,
        text="-1 Sec",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#ffcc66",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_sector(-1),
    ).pack(side="left", padx=(4, 1))
    tk.Button(
        bp_ctrl_frame,
        text="+1 Sec",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#38bdf8",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_sector(1),
    ).pack(side="left", padx=1)
    tk.Button(
        bp_ctrl_frame,
        text="-1 Tok",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#ffcc66",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_tokens(-1),
    ).pack(side="left", padx=(4, 1))
    tk.Button(
        bp_ctrl_frame,
        text="+1 Tok",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#00ff66",
        bd=0,
        cursor="hand2",
        command=lambda: self.change_bp_tokens(1),
    ).pack(side="left", padx=1)
    tk.Button(
        bp_ctrl_frame,
        text="↺ Reset",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="#d9534f",
        bd=0,
        cursor="hand2",
        command=self.reset_bp,
    ).pack(side="left", padx=(6, 0))

    # Control Frame for Weapons
    self.control_frame = ttk.Frame(self.root, style="Card.TFrame")
    self.control_frame.pack(fill="x", padx=20, pady=5, ipady=5)

    ttk.Label(
        self.control_frame, text="Add Category:", background=self.card_bg
    ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    self.cat_entry = ttk.Entry(self.control_frame, width=20)
    self.cat_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(
        self.control_frame,
        text="Add Category",
        style="Accent.TButton",
        command=self.add_category,
    ).grid(row=0, column=2, padx=10, pady=5)

    ttk.Label(
        self.control_frame, text="Add Weapon:", background=self.card_bg
    ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    self.cat_dropdown = ttk.Combobox(
        self.control_frame, state="readonly", width=18
    )
    self.cat_dropdown.grid(row=1, column=1, padx=5, pady=5)
    self.weapon_entry = ttk.Entry(self.control_frame, width=20)
    self.weapon_entry.grid(row=1, column=2, padx=5, pady=5)
    ttk.Button(
        self.control_frame,
        text="Add Weapon",
        style="Accent.TButton",
        command=self.add_weapon,
    ).grid(row=1, column=3, padx=10, pady=5)

    # Search / Filter Bar
    search_bar_frame = ttk.Frame(self.root)
    search_bar_frame.pack(fill="x", padx=20, pady=(2, 2))

    ttk.Label(search_bar_frame, text="🔍 Filter Weapons:").pack(
        side="left", padx=(0, 5)
    )
    self.search_entry = ttk.Entry(search_bar_frame, width=35)
    self.search_entry.pack(side="left", padx=(0, 10))
    self.search_entry.bind(
        "<KeyRelease>", lambda e: self.on_search_query_changed()
    )

    ttk.Button(
        search_bar_frame, text="Clear", command=self.clear_search
    ).pack(side="left")

    # Scrollable Display Area
    canvas_container = ttk.Frame(self.root)
    canvas_container.pack(fill="both", expand=True, padx=20, pady=(5, 5))

    self.canvas = tk.Canvas(
        canvas_container, bg=self.bg_color, highlightthickness=0
    )
    scrollbar = ttk.Scrollbar(
        canvas_container, orient="vertical", command=self.canvas.yview
    )
    self.scrollable_frame = ttk.Frame(self.canvas)

    self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ),
    )
    self.canvas.create_window(
        (0, 0), window=self.scrollable_frame, anchor="nw"
    )
    self.canvas.configure(yscrollcommand=scrollbar.set)

    self.canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- HIERARCHICAL QUESTS & EVENTS SECTION ---
    events_main_card = tk.Frame(
        self.root, bg=self.card_bg, bd=1, relief="solid"
    )
    events_main_card.pack(fill="x", padx=20, pady=(5, 15), ipady=2)

    events_head = tk.Frame(events_main_card, bg=self.card_bg)
    events_head.pack(fill="x", padx=10, pady=5)

    tk.Label(
        events_head,
        text="🎯 ACTIVE EVENTS & QUEST CATEGORIES",
        font=("Segoe UI", 10, "bold"),
        bg=self.card_bg,
        fg=self.accent_color,
    ).pack(side="left")

    self.ev_toggle_btn = tk.Button(
        events_head,
        text="[-] Minimize",
        font=("Segoe UI", 8, "bold"),
        bg="#2e3540",
        fg="white",
        bd=0,
        cursor="hand2",
        command=self.toggle_events_collapse,
    )
    self.ev_toggle_btn.pack(side="right")

    self.events_body_frame = tk.Frame(events_main_card, bg=self.card_bg)
    self.events_body_frame.pack(fill="x", padx=10, pady=2)

    # Add Category Row
    events_input_row = tk.Frame(self.events_body_frame, bg=self.card_bg)
    events_input_row.pack(fill="x", pady=(0, 4))

    ttk.Label(
        events_input_row,
        text="Category:",
        background=self.card_bg,
        font=("Segoe UI", 9),
    ).pack(side="left", padx=(0, 2))
    self.event_entry = ttk.Entry(events_input_row, width=20)
    self.event_entry.pack(side="left", padx=(0, 5))

    ttk.Button(
        events_input_row,
        text="+ Add Category",
        style="Accent.TButton",
        command=self.add_event_category,
    ).pack(side="left", padx=(0, 15))

    # Add Sub-Quest Row
    sub_input_row = tk.Frame(self.events_body_frame, bg=self.card_bg)
    sub_input_row.pack(fill="x", pady=(0, 5))

    ttk.Label(
        sub_input_row,
        text="Sub-Quest to:",
        background=self.card_bg,
        font=("Segoe UI", 9),
    ).pack(side="left", padx=(0, 2))
    self.event_cat_dropdown = ttk.Combobox(
        sub_input_row, state="readonly", width=15
    )
    self.event_cat_dropdown.pack(side="left", padx=(0, 5))

    self.event_sub_entry = ttk.Entry(sub_input_row, width=20)
    self.event_sub_entry.pack(side="left", padx=(0, 5))

    ttk.Button(
        sub_input_row,
        text="+ Add Sub-Quest",
        style="Accent.TButton",
        command=self.add_sub_event,
    ).pack(side="left")

    self.events_container = tk.Frame(self.events_body_frame, bg=self.card_bg)
    self.events_container.pack(fill="x")
    self.load_event_categories_into_dropdown()

  # --- SEARCH HELPERS ---
  def on_search_query_changed(self):
    self.search_filter = self.search_entry.get().strip().lower()
    self.refresh_display()

  def clear_search(self):
    self.search_entry.delete(0, tk.END)
    self.search_filter = ""
    self.refresh_display()

  # --- CATEGORY MANAGEMENT ---
  def toggle_category_collapse(self, cat_id):
    key = f"cat_{cat_id}"
    self.collapsed_sections[key] = not self.collapsed_sections.get(key, False)
    self.refresh_display()

  def load_categories_into_dropdown(self):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()

    self.cat_dropdown["values"] = categories
    if categories:
      self.cat_dropdown.current(0)
    else:
      self.cat_dropdown.set("")

  def add_category(self):
    cat_name = self.cat_entry.get().strip()
    if not cat_name:
      messagebox.showwarning("Warning", "Category name cannot be empty.")
      return
    try:
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO categories (name) VALUES (?)", (cat_name,)
      )
      conn.commit()
      conn.close()
      self.cat_entry.delete(0, tk.END)
      self.load_categories_into_dropdown()
      self.refresh_display()
    except sqlite3.IntegrityError:
      messagebox.showerror("Error", "Category already exists.")

  def remove_category(self, cat_id, cat_name):
    if messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{cat_name}' and ALL weapons inside"
        " it?",
    ):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON;")
      cursor.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
      conn.commit()
      conn.close()
      self.load_categories_into_dropdown()
      self.refresh_display()

  def add_weapon(self):
    cat_name = self.cat_dropdown.get()
    weapon_name = self.weapon_entry.get().strip()
    if not cat_name or not weapon_name:
      messagebox.showwarning(
          "Warning", "Select a category and enter a weapon name."
      )
      return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM categories WHERE name = ?", (cat_name,)
    )
    row = cursor.fetchone()
    if not row:
      conn.close()
      return

    cat_id = row[0]
    cursor.execute(
        "INSERT INTO weapons (name, category_id, level, max_level) VALUES (?, ?,"
        " 1, 50)",
        (weapon_name, cat_id),
    )
    weapon_id = cursor.lastrowid

    for desc in [
        "Get 50 Kills",
        "Get 15 Headshots",
        "Get 10 Double Kills",
        "Gold Camo Unlock",
    ]:
      cursor.execute(
          "INSERT INTO challenges (weapon_id, description) VALUES (?, ?)",
          (weapon_id, desc),
      )

    conn.commit()
    conn.close()
    self.weapon_entry.delete(0, tk.END)
    self.refresh_display()

  def remove_weapon(self, weapon_id, weapon_name):
    if messagebox.askyesno(
        "Confirm Delete", f"Delete '{weapon_name}' and its challenges?"
    ):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON;")
      cursor.execute("DELETE FROM weapons WHERE id = ?", (weapon_id,))
      conn.commit()
      conn.close()
      self.refresh_display()

  def toggle_challenge(self, challenge_id, var):
    completed = var.get()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE challenges SET completed = ? WHERE id = ?",
        (1 if completed else 0, challenge_id),
    )
    conn.commit()
    conn.close()
    self.refresh_display()

  # --- CHALLENGE EDITOR ---
  def open_challenge_editor(self, weapon_id, weapon_name):
    editor = tk.Toplevel(self.root)
    editor.title(f"Customize Challenges: {weapon_name}")
    editor.geometry("400x400")
    editor.configure(bg=self.card_bg)
    editor.grab_set()

    tk.Label(
        editor,
        text=f"Challenges for {weapon_name}",
        font=("Segoe UI", 11, "bold"),
        bg=self.card_bg,
        fg=self.accent_color,
    ).pack(pady=10)

    listbox_frame = tk.Frame(editor, bg=self.card_bg)
    listbox_frame.pack(fill="both", expand=True, padx=15, pady=5)

    listbox = tk.Listbox(
        listbox_frame,
        bg=self.wep_card_bg,
        fg=self.text_color,
        selectbackground=self.accent_color,
        bd=0,
    )
    listbox.pack(side="left", fill="both", expand=True)

    def populate_list():
      listbox.delete(0, tk.END)
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute(
          "SELECT id, description FROM challenges WHERE weapon_id = ?",
          (weapon_id,),
      )
      self.current_challs = cursor.fetchall()
      conn.close()
      for _, desc in self.current_challs:
        listbox.insert(tk.END, desc)

    def add_ch():
      desc = simpledialog.askstring(
          "New Challenge", "Enter challenge description:", parent=editor
      )
      if desc:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO challenges (weapon_id, description) VALUES (?, ?)",
            (weapon_id, desc),
        )
        conn.commit()
        conn.close()
        populate_list()
        self.refresh_display()

    def remove_ch():
      sel = listbox.curselection()
      if sel:
        c_id = self.current_challs[sel[0]][0]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM challenges WHERE id = ?", (c_id,))
        conn.commit()
        conn.close()
        populate_list()
        self.refresh_display()

    btn_frame = tk.Frame(editor, bg=self.card_bg)
    btn_frame.pack(fill="x", padx=15, pady=10)
    tk.Button(
        btn_frame,
        text="+ Add",
        bg=self.accent_color,
        fg="black",
        font=("Segoe UI", 9, "bold"),
        command=add_ch,
    ).pack(side="left", padx=5)
    tk.Button(
        btn_frame,
        text="- Remove Selected",
        bg="#d9534f",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        command=remove_ch,
    ).pack(side="left", padx=5)

    populate_list()

  # --- MAIN RENDER LOGIC ---
  def refresh_display(self):
    for widget in self.scrollable_frame.winfo_children():
      widget.destroy()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()

    for cat_id, cat_name in categories:
      cursor.execute(
          "SELECT id, name, level, max_level FROM weapons WHERE category_id = ?",
          (cat_id,),
      )
      weapons = cursor.fetchall()

      if self.search_filter:
        weapons = [w for w in weapons if self.search_filter in w[1].lower()]
        if not weapons:
          continue

      cat_weapons_complete = 0
      total_weapons_in_cat = len(weapons)
      weapon_details = []

      for w_id, w_name, w_lvl, w_max in weapons:
        cursor.execute(
            "SELECT id, description, completed FROM challenges WHERE"
            " weapon_id = ?",
            (w_id,),
        )
        challenges = cursor.fetchall()
        all_completed = (
            all(ch[2] == 1 for ch in challenges) if challenges else False
        )
        if all_completed:
          cat_weapons_complete += 1
        weapon_details.append(
            (w_id, w_name, w_lvl, w_max, challenges, all_completed)
        )

      category_mastered = (
          total_weapons_in_cat > 0
          and cat_weapons_complete == total_weapons_in_cat
          and not self.search_filter
      )

      cat_frame = tk.Frame(
          self.scrollable_frame,
          bg=self.card_bg,
          bd=2 if category_mastered else 1,
          relief="solid",
          highlightbackground=self.gold_color
          if category_mastered
          else "#2e3540",
          highlightcolor=self.gold_color if category_mastered else "#2e3540",
          highlightthickness=1,
      )
      cat_frame.pack(fill="x", expand=True, pady=6, ipady=3)

      header_bg = "#2a2415" if category_mastered else self.card_bg
      cat_header = tk.Frame(cat_frame, bg=header_bg)
      cat_header.pack(fill="x", padx=10, pady=4)

      cat_title_text = (
          f"🏆 MASTERED: {cat_name.upper()} [ALL WEAPONS COMPLETE]"
          if category_mastered
          else f"{cat_name.upper()} ({cat_weapons_complete}/{total_weapons_in_cat} COMPLETED)"
      )
      title_color = self.gold_color if category_mastered else self.accent_color

      tk.Label(
          cat_header,
          text=cat_title_text,
          font=("Segoe UI", 11, "bold"),
          bg=header_bg,
          fg=title_color,
      ).pack(side="left")

      tk.Button(
          cat_header,
          text="🗑 Delete Category",
          font=("Segoe UI", 8, "bold"),
          bg="#2e3540",
          fg="#d9534f",
          bd=0,
          cursor="hand2",
          command=lambda cid=cat_id, cname=cat_name: self.remove_category(
              cid, cname
          ),
      ).pack(side="right", padx=(5, 0))

      is_collapsed = self.collapsed_sections.get(f"cat_{cat_id}", False)
      toggle_txt = "[+] Expand" if is_collapsed else "[-] Minimize"

      tk.Button(
          cat_header,
          text=toggle_txt,
          font=("Segoe UI", 8, "bold"),
          bg="#2e3540",
          fg="white",
          bd=0,
          cursor="hand2",
          command=lambda cid=cat_id: self.toggle_category_collapse(cid),
      ).pack(side="right")

      if not is_collapsed:
        grid_frame = tk.Frame(cat_frame, bg=self.card_bg)
        grid_frame.pack(fill="x", padx=10, pady=5)

        col = 0
        row = 0
        for (
            w_id,
            w_name,
            w_lvl,
            w_max,
            challenges,
            all_completed,
        ) in weapon_details:
          border_col = self.gold_color if all_completed else "#2e3540"
          title_col = self.gold_color if all_completed else self.text_color
          border_width = 2 if all_completed else 1

          wep_card = tk.Frame(
              grid_frame,
              bg=self.wep_card_bg,
              bd=border_width,
              relief="solid",
              highlightbackground=border_col,
              highlightcolor=border_col,
              highlightthickness=1,
          )
          wep_card.grid(row=row, column=col, padx=5, pady=5, sticky="nw")

          card_header = tk.Frame(wep_card, bg=self.wep_card_bg)
          card_header.pack(fill="x", padx=8, pady=(8, 2))

          tk.Label(
              card_header,
              text=f"{'★ ' if all_completed else ''}{w_name}",
              font=("Segoe UI", 10, "bold"),
              bg=self.wep_card_bg,
              fg=title_col,
          ).pack(side="left")

          tk.Button(
              card_header,
              text="✕",
              font=("Segoe UI", 8, "bold"),
              bg="#2e3540",
              fg="#d9534f",
              bd=0,
              cursor="hand2",
              command=lambda wid=w_id, wname=w_name: self.remove_weapon(
                  wid, wname
              ),
          ).pack(side="right", padx=(2, 0))

          tk.Button(
              card_header,
              text="⚙",
              font=("Segoe UI", 8),
              bg="#2e3540",
              fg="white",
              bd=0,
              cursor="hand2",
              command=lambda wid=w_id,
              wname=w_name: self.open_challenge_editor(wid, wname),
          ).pack(side="right", padx=(0, 2))

          wep_lvl_frame = tk.Frame(wep_card, bg=self.wep_card_bg)
          wep_lvl_frame.pack(fill="x", padx=8, pady=(2, 6))

          lvl_lbl_col = (
              self.gold_color if w_lvl >= w_max else self.accent_color
          )
          tk.Label(
              wep_lvl_frame,
              text=f"Lvl {w_lvl}/{w_max}",
              font=("Segoe UI", 8, "bold"),
              bg=self.wep_card_bg,
              fg=lvl_lbl_col,
          ).pack(side="left")

          tk.Button(
              wep_lvl_frame,
              text="+5",
              font=("Segoe UI", 7, "bold"),
              bg="#2e3540",
              fg="white",
              bd=0,
              cursor="hand2",
              command=lambda wid=w_id: self.change_weapon_level(wid, 5),
          ).pack(side="right", padx=1)
          tk.Button(
              wep_lvl_frame,
              text="+1",
              font=("Segoe UI", 7, "bold"),
              bg="#2e3540",
              fg="white",
              bd=0,
              cursor="hand2",
              command=lambda wid=w_id: self.change_weapon_level(wid, 1),
          ).pack(side="right", padx=1)
          tk.Button(
              wep_lvl_frame,
              text="-1",
              font=("Segoe UI", 7, "bold"),
              bg="#2e3540",
              fg="white",
              bd=0,
              cursor="hand2",
              command=lambda wid=w_id: self.change_weapon_level(wid, -1),
          ).pack(side="right", padx=1)

          tk.Button(
              wep_lvl_frame,
              text=f"Max: {w_max}",
              font=("Segoe UI", 7),
              bg="#2e3540",
              fg="#8a99ad",
              bd=0,
              cursor="hand2",
              command=lambda wid=w_id,
              wname=w_name,
              wm=w_max: self.set_custom_max_level(wid, wname, wm),
          ).pack(side="right", padx=(0, 2))

          wep_bar = ttk.Progressbar(
              wep_card, orient="horizontal", maximum=w_max, mode="determinate"
          )
          wep_bar["value"] = w_lvl
          wep_bar.pack(fill="x", padx=8, pady=(0, 4))

          for ch_id, desc, completed in challenges:
            var = tk.BooleanVar(value=bool(completed))
            chk = tk.Checkbutton(
                wep_card,
                text=desc,
                variable=var,
                bg=self.wep_card_bg,
                fg="#8a99ad" if completed else self.text_color,
                selectcolor="#0d0f12",
                activebackground=self.wep_card_bg,
                activeforeground=self.text_color,
                command=lambda c_id=ch_id, v=var: self.toggle_challenge(
                    c_id, v
                ),
            )
            chk.pack(anchor="w", padx=8, pady=2)

          col += 1
          if col > 2:
            col = 0
            row += 1

    conn.close()


if __name__ == "__main__":
  root = tk.Tk()
  app = CODTrackerApp(root)
  root.mainloop()