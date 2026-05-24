import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime

BG = "#0f1115"
PANEL = "#1c1f26"
TEXT = "#e6e6e6"


BASE_DIR = os.path.dirname(__file__)

SLOTS_FILE = os.path.join(BASE_DIR, "..", "data", "slots.json")
BOOKINGS_FILE = os.path.join(BASE_DIR, "..", "data", "bookings.json")
VEHICLE_FILE = os.path.join(BASE_DIR, "..", "data", "vehicles.json")

# =========================
# BOOT SCREEN
# =========================
def show_boot_screen():
    splash = tk.Toplevel(root)
    splash.attributes('-fullscreen', True)
    splash.configure(bg="black")

    try:
        logo_path = os.path.join(BASE_DIR, "trinetrax_2.0_logo.jpeg")
        img = Image.open(logo_path)
        img = img.resize((650, 650))
        logo = ImageTk.PhotoImage(img)

        label = tk.Label(splash, image=logo, bg="black")
        label.image = logo
        label.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            splash,
            text="TRINETRAX 2.0 INITIALIZING...",
            fg="#00e676",
            bg="black",
            font=("Consolas", 18, "bold")
        ).place(relx=0.5, rely=0.75, anchor="center")

    except:
        tk.Label(
            splash,
            text="TRINETRAX 2.0",
            fg="white",
            bg="black",
            font=("Arial", 20, "bold")
        ).pack(expand=True)

    def close_boot():
        splash.destroy()
        root.deiconify()

    root.after(10000, close_boot)


# =========================
# FILE HANDLING 
# =========================
def load_slots():
    if not os.path.exists(SLOTS_FILE):
        return []
    try:
        with open(SLOTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_slots(data):
    with open(SLOTS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        return []
    try:
        with open(BOOKINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# =========================
# CREATE CENTER POPUP
# =========================
def open_create_popup():
    popup = tk.Toplevel(root)
    popup.title("Create Service Center")
    popup.geometry("300x250")
    popup.configure(bg=BG)

    tk.Label(popup, text="Center Name", fg=TEXT, bg=BG).pack()
    name_entry = tk.Entry(popup)
    name_entry.pack(pady=5)

    tk.Label(popup, text="Pincode", fg=TEXT, bg=BG).pack()
    pin_entry = tk.Entry(popup)
    pin_entry.pack(pady=5)

    def save_center():
        name = name_entry.get().strip()
        pin = pin_entry.get().strip()

        if not name or not pin:
            messagebox.showerror("Error", "Enter all fields")
            return

        data = load_slots()

        for c in data:
            if c["name"].lower() == name.lower():
                messagebox.showerror("Error", "Center already exists")
                return

        # STRUCTURE
        data.append({
            "name": name,
            "pincode": pin,
            "slots": 0,
            "used_slots": 0,
            "date": "--",
            "time": "--"
        })

        save_slots(data)

        messagebox.showinfo("Success", "Service Center Created")
        popup.destroy()
        refresh_centers()

    tk.Button(
        popup,
        text="Save Center",
        command=save_center,
        bg="#00e676",
        fg="black"
    ).pack(pady=15)
# =========================
# OPEN SLOTS 
# =========================
def open_slots():
    center = center_list.get()

    if not center:
        messagebox.showerror("Error", "Select center")
        return

    try:
        slots = int(entry_slots.get())
    except:
        messagebox.showerror("Error", "Enter valid number")
        return

    data = load_slots()

    for c in data:
        if center.startswith(c["name"]):
            now = datetime.now()

            c["slots"] = slots
            c["used_slots"] = 0
            c["date"] = now.strftime("%d-%m-%Y")
            c["time"] = now.strftime("%H:%M")
            break

    save_slots(data)

    messagebox.showinfo("Success", f"{slots} slots opened")
    refresh_centers()


# =========================
# VIEW BOOKINGS 
# =========================
def view_bookings():
    center = center_list.get()

    bookings = load_bookings()
    slots_data = load_slots()

    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)

    center_name = center.split("|")[0].strip()

    slot_info = next((c for c in slots_data if c["name"] == center_name), None)

    total_slots = slot_info.get("slots", 0) if slot_info else 0
    date = slot_info.get("date", "--") if slot_info else "--"
    time = slot_info.get("time", "--") if slot_info else "--"

    used = slot_info.get("used_slots", 0) if slot_info else 0
    available = total_slots - used

    # CURRENT ACTIVE BOOKINGS
    filtered = [b for b in bookings if b.get("center") == center_name]
    current_bookings = len(filtered)

    text_box.insert(tk.END,
        f"📅 Date: {date}\n"
        f"⏰ Time: {time}\n\n"
        f"📊 Total Slots: {total_slots}\n"
        f"☯️ Used Slots: {used}\n"
        f"✅ Available: {available}\n\n"
        f"🔖 Current Active Bookings: {current_bookings}\n\n"
        f"══════════════════════\n\n"
    )

    if not filtered:
        text_box.insert(tk.END, "No bookings\n")
    else:
        for b in filtered:
            text_box.insert(tk.END, f"{b.get('car_id')} | {b.get('status')}\n")

    text_box.config(state="disabled")


# =========================
# REFRESH CENTERS 
# =========================
def refresh_centers():
    center_list['values'] = [
        f"{c['name']} | Slots: {c.get('slots',0)} | {c.get('date','--')} {c.get('time','--')}"
        for c in load_slots()
    ]


# =========================
# UI 
# =========================
root = tk.Tk()
root.withdraw()

show_boot_screen()

root.title("TRINETRAX 2.0")
root.geometry("1000x550")
root.configure(bg=BG)

left = tk.Frame(root, bg=BG)
left.grid(row=0, column=0, padx=20, pady=20)

tk.Label(left, text="Select Service Center", fg=TEXT, bg=BG).pack(anchor="w")

center_list = ttk.Combobox(left)
center_list.pack(pady=10)

tk.Button(
    left,
    text="Create Center",
    command=open_create_popup,
    bg="#00e676"
).pack(pady=10)

tk.Label(left, text="Open Slots (Today)", fg=TEXT, bg=BG).pack(anchor="w")

entry_slots = tk.Entry(left)
entry_slots.pack(pady=5)

tk.Button(
    left,
    text="Open Slots",
    command=open_slots,
    bg="#2196f3"
).pack(pady=10)

tk.Button(
    left,
    text="View Bookings",
    command=view_bookings,
    bg="#ff9800"
).pack(pady=10)

# RIGHT PANEL
right = tk.Frame(root, bg=PANEL)
right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

text_box = tk.Text(
    right,
    font=("Consolas", 13, "bold"),
    bg="#121417",
    fg="#00e676",
    state="disabled"
)
text_box.pack(expand=True, fill="both")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

refresh_centers()

root.mainloop()