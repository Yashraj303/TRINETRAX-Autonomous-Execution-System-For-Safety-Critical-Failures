import sys
import os
import socket   # ESP32 WiFi

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agents import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import winsound
import json

# =========================
# ESP32 WIFI CONNECTION
# =========================
ESP_IP = "192.168.31.4"
ESP_PORT = 80

sock = None

def connect_esp():
    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ESP_IP, ESP_PORT))
        print("✅ ESP32 Connected")
    except Exception as e:
        print("❌ ESP32 connection failed:", e)
        sock = None


# =========================
# HARDWARE INPUT FUNCTION
# =========================
def get_hardware_data():
    global sock

    # reconnect if needed
    if sock is None:
        connect_esp()
        return None, None, None

    try:
        sock.settimeout(0.5)

        # request data
        sock.send(b"GET\n")

        data = sock.recv(1024).decode().strip()
        print("ESP32:", data)

        # expected format: THICK:0.51 BRAKE:12
        if "THICK:" in data and "BRAKE:" in data:
            parts = data.split()

            thickness = float(parts[0].split(":")[1])
            braking = int(parts[1].split(":")[1])
            driving_style = "UNKNOWN"

            if len(parts) > 2 and "STYLE:" in parts[2]:
               driving_style = parts[2].split(":")[1]

               print("Driving Style:", driving_style)

            initial = 10.0   # fixed baseline

            return initial, thickness, braking, driving_style

    except Exception as e:
        print("Socket issue:", e)
        sock = None   # force reconnect next time

    return None, None, None, None
BG = "#0f1115"
PANEL = "#1c1f26"
TEXT = "#e6e6e6"

COLORS = {
    "CRITICAL": "#ff3b3b",
    "HIGH": "#ff9800",
    "MODERATE": "#2196f3",
    "NORMAL": "#00e676"
}

FLASH_INTERVAL = 600
flashing = False

# =========================
# PATH
# =========================
BASE_DIR = os.path.dirname(__file__)

SLOTS_FILE = os.path.join(BASE_DIR, "..", "data", "slots.json")
BOOKINGS_FILE = os.path.join(BASE_DIR, "..", "data", "bookings.json")
VEHICLE_FILE = os.path.join(BASE_DIR, "..", "data", "vehicles.json")


# =========================
# BOOKING FUNCTIONS
# =========================
def save_booking(vehicle, center):
    booking = {
        "car_id": vehicle,
        "center": center,
        "status": "Scheduled"
    }

    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(booking)

    with open(BOOKINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def remove_booking(vehicle):
    if not os.path.exists(BOOKINGS_FILE):
        return

    with open(BOOKINGS_FILE, "r") as f:
        data = json.load(f)

    updated = [b for b in data if b.get("car_id") != vehicle]

    with open(BOOKINGS_FILE, "w") as f:
        json.dump(updated, f, indent=4)


def select_best_center(pincode):
    try:
        with open(SLOTS_FILE, "r") as f:
            centers = json.load(f)

        filtered = [c for c in centers if c.get("pincode") == pincode]

        if not filtered:
            return "Tata Motors Authorized Service - 2.3 km"

        best = max(filtered, key=lambda x: x.get("slots", 0))
        return best["name"]

    except:
        return "Tata Motors Authorized Service - 2.3 km"


# =========================
# SLOT TRACKING
# =========================
def increment_used_slot(center_name):
    if not os.path.exists(SLOTS_FILE):
        return

    with open(SLOTS_FILE, "r") as f:
        data = json.load(f)

    for c in data:
        if c.get("name") == center_name:
            c["used_slots"] = c.get("used_slots", 0) + 1

    with open(SLOTS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# VEHICLE TRACKING
# =========================
def load_vehicles():
    if not os.path.exists(VEHICLE_FILE):
        return []
    try:
        with open(VEHICLE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_vehicles(data):
    with open(VEHICLE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def update_vehicle(vehicle, status, center=None):
    data = load_vehicles()
    found = False

    for v in data:
        if v["vehicle"] == vehicle:
            v["status"] = status
            if center:
                v["center"] = center
            found = True

    if not found:
        data.append({
            "vehicle": vehicle,
            "status": status,
            "center": center
        })

    save_vehicles(data)
# =========================
# BOOT SCREEN
# =========================
def show_boot_screen():
    splash = tk.Toplevel(root)
    splash.attributes('-fullscreen', True)
    splash.configure(bg="black")

    try:
        img = Image.open("trinetrax_logo.jpeg")
        img = img.resize((650, 650))
        logo = ImageTk.PhotoImage(img)

        label = tk.Label(splash, image=logo, bg="black")
        label.image = logo
        label.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            splash,
            text="TRINETRAX INITIALIZING...",
            fg="#00e676",
            bg="black",
            font=("Consolas", 18, "bold")
        ).place(relx=0.5, rely=0.75, anchor="center")

    except:
        tk.Label(
            splash,
            text="TRINETRAX",
            fg="white",
            bg="black",
            font=("Arial", 20, "bold")
        ).pack(expand=True)

    def close_boot():
        splash.destroy()
        root.deiconify()

    root.after(5000, close_boot)


# =========================
# BUZZER
# =========================
def play_buzzer(times=10, count=0):
    if count >= times:
        return
    try:
        winsound.Beep(1000, 300)
    except:
        pass
    root.after(400, play_buzzer, times, count + 1)


# =========================
# FLASH WARNING
# =========================
def flash_warning():
    global flashing
    if not flashing:
        return

    current = text_box.cget("fg")

    if current == COLORS["CRITICAL"]:
        text_box.config(fg="#ffffff")
    else:
        text_box.config(fg=COLORS["CRITICAL"])

    root.after(FLASH_INTERVAL, flash_warning)


# =========================
# MAIN SYSTEM 
# =========================
def run_system():
    global flashing

    try:
        # =========================
        # CONNECT ESP32
        # =========================
        connect_esp()

        # =========================
        # GET HARDWARE DATA (MANDATORY)
        # =========================
        initial_h, current_h, braking_h, driving_style = get_hardware_data()
    
        if current_h is None:
            text_box.config(state="normal")
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, "❌ ESP32 NOT RESPONDING\nCheck connection")
            text_box.config(state="disabled")
            return

        # =========================
        # USE ONLY ESP32 VALUES
        # =========================
        initial = 10.0
        current = current_h
        braking = braking_h
        # =========================
        # INITIAL FIELD
        # =========================
        entry_initial.config(state="normal")
        entry_initial.delete(0, tk.END)
        entry_initial.insert(0, "10.0")
        entry_initial.config(state="disabled")
        # =========================
        # UI DISPLAY
        # =========================
        entry_current.config(state="normal")
        entry_current.delete(0, tk.END)
        entry_current.insert(0, str(round(current, 2)))
        entry_current.config(state="disabled")

        entry_brake.config(state="normal")
        entry_brake.delete(0, tk.END)
        entry_brake.insert(0, str(braking))
        entry_brake.config(state="disabled")

        # =========================
        # USER INPUTS ONLY
        # =========================
        distance = float(entry_distance.get())
        pincode = entry_pincode.get()
        vehicle = entry_vehicle.get()

        # =========================
        # AI PROCESSING
        # =========================
        data = data_agent(initial, current, distance, braking)

        health, wear, rul, style, trend, usage, env, pattern, failure, confidence = diagnosis_agent(data)
        risk = decision_agent(health, rul)

        print("DEBUG →", initial, current, health, rul, risk)

        # =========================
        # SEND RISK TO ESP32
        # =========================
        try:
            if sock:
                sock.send((risk + "\n").encode())
        except Exception as e:
            print("ESP send error:", e)

        # =========================
        # DISPLAY FUNCTION
        # =========================
        def show(msg):
            text_box.config(state="normal")
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, msg)
            text_box.config(state="disabled")
        # =========================
        # RESET CONDITION
        # =========================
        if health > 40:
            reset_service_status()
            remove_booking(vehicle)

            update_vehicle(vehicle, "SERVICED")

            flashing = False
            health_label.grid()
            progress.grid()

        # =========================
        # COLOR UPDATE
        # =========================
        text_box.config(state="normal")
        text_box.config(fg=COLORS[risk])
        text_box.config(state="disabled")

        # =========================
        # HEALTH BAR
        # =========================
        if not is_service_booked():
            health_label.grid(row=0, column=0, sticky="w")
            progress.grid(row=1, column=0, sticky="ew")

            progress['value'] = max(0, min(health, 100))

            style_bar = ttk.Style()
            style_bar.theme_use('default')

            style_bar.configure(
                "custom.Horizontal.TProgressbar",
                troughcolor="#2a2e36",
                background=COLORS[risk]
            )

            progress.config(style="custom.Horizontal.TProgressbar")

        # =========================
        # CRITICAL FLOW
        # =========================
        if risk == "CRITICAL":

            selected_center = select_best_center(pincode)

            # Already booked case
            if is_service_booked():
                health_label.grid_remove()
                progress.grid_remove()

                show(
                    "⚠️ SERVICE ALREADY SCHEDULED\n\n"
                    f"Drive ONLY to:\n📍 {selected_center}\n\n"
                    "Avoid normal usage\n\n"
                    "🧭 Navigation will be enabled in production"
                )

                flashing = True
                flash_warning()
                play_buzzer()
                return

            # First time booking
            set_service_booked()

            save_booking(vehicle, selected_center)
            increment_used_slot(selected_center)
            update_vehicle(vehicle, "CRITICAL", selected_center)

            # Step flow (clean UI animation)
            def pre_diagnosis():
                show(
                    "🔍 SYSTEM DIAGNOSIS\n\n"
                    f"Health: {health:.2f}%\n"
                    f"Failure Risk: {failure}\n"
                    f"AI Confidence: {confidence:.2f}%\n\n"
                    "Analyzing severity..."
                )

            health_label.grid_remove()
            progress.grid_remove()

            def step1():
                show("🚨 CRITICAL FAILURE DETECTED\n\nAnalyzing system...")

            def step2():
                show("🛑 SAFE STOP ACTIVATED\n\nVehicle stabilizing...")

            def step3():
                show("📡 Connecting to service network...")

            def step4():
                try:
                    with open(SLOTS_FILE, "r") as f:
                        centers = json.load(f)

                    filtered = [c for c in centers if c.get("pincode") == pincode]

                    if not filtered:
                        filtered = centers

                    text = "🛜 Nearby Service Centers:\n\n"

                    for i, c in enumerate(filtered[:3], 1):
                        text += f"{i}. {c['name']} | Slots: {c.get('slots',0)}\n"

                    text += "\nSelecting optimal center..."

                    show(text)

                except:
                    show(
                        "🛜 Nearby Service Centers:\n\n"
                        "1. Tata Motors - 2.3 km\n"
                        "2. Mahindra - 3 km\n"
                        "3. Maruti - 4 km\n\n"
                        "Selecting optimal center..."
                    )

            def step5():
                show(
                    "✅ SERVICE BOOKED\n\n"
                    f"{selected_center}\n"
                    "Slot Confirmed"
                )

            def final_step():
                global flashing

                show(
                    "⚠️ EMERGENCY INSTRUCTION\n\n"
                    f"Drive ONLY to:\n📍 {selected_center}\n\n"
                    "Avoid normal usage\n\n"
                    "🧭 Navigation will be enabled in production"
                )

                flashing = True
                flash_warning()
                play_buzzer()

            root.after(0, pre_diagnosis)
            root.after(2000, step1)
            root.after(5000, step2)
            root.after(8000, step3)
            root.after(11000, step4)
            root.after(13000, step5)
            root.after(16000, final_step)

        # =========================
        # NORMAL / NON-CRITICAL FLOW
        # =========================
        else:
            flashing = False

            result = (
                "🚗 TRINETRAX SYSTEM\n"
                "══════════════════════════════\n\n"
                f"Health: {health:.2f}% | {risk}\n\n"
                f"RUL: {rul:.2f} km\n"
                f"Wear: {wear:.4f}\n\n"
                f"Driving Style: {style}\n"
                f"Usage: {usage}\n"
                f"Pattern: {pattern}\n"
                f"Environment: {env}\n\n"
                f"Failure Risk: {failure}\n"
                f"AI Confidence: {confidence:.2f}%\n"
            )

            show(result)

    except Exception as e:
        text_box.config(state="normal")
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, f"Error: {e}")
        text_box.config(state="disabled")
# =========================
# UI SETUP
# =========================
root = tk.Tk()
root.withdraw()

show_boot_screen()

root.title("TRINETRAX ADAS System")
root.geometry("1000x550")
root.configure(bg=BG)

left = tk.Frame(root, bg=BG)
left.grid(row=0, column=0, padx=20, pady=20)

def create_input(label, default, state="normal"):
    tk.Label(left, text=label, fg=TEXT, bg=BG).pack(anchor="w")
    e = tk.Entry(left, bg="#2a2e36", fg="white", insertbackground="white", state=state)
    e.pack(pady=4)
    e.insert(0, default)
    return e

# =========================
# INPUT FIELDS
# =========================

# ❌ USER CANNOT CHANGE THESE (ESP32 CONTROLLED)
entry_initial = create_input("Initial Thickness", "10", state="disabled")
entry_current = create_input("Current Thickness", "0", state="disabled")
entry_brake = create_input("Braking Events", "0", state="disabled")

# ✅ USER INPUT ONLY
entry_distance = create_input("Distance (km)", "5000")
entry_pincode = create_input("Pincode", "411001")
entry_vehicle = create_input("Vehicle Number", "MH14AB1234")

# =========================
# BUTTON
# =========================
tk.Button(
    left,
    text="Run TRINETRAX",
    command=run_system,
    bg="#00e676",
    fg="black",
    font=("Arial", 11, "bold")
).pack(pady=15)

# =========================
# RIGHT PANEL
# =========================
right = tk.Frame(root, bg=PANEL)
right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

health_label = tk.Label(right, text="Brake Health", fg=TEXT, bg=PANEL)
health_label.grid(row=0, column=0)

progress = ttk.Progressbar(right, length=500, maximum=100, mode='determinate')
progress.grid(row=1, column=0, sticky="ew")

text_box = tk.Text(
    right,
    wrap="word",
    font=("Consolas", 15, "bold"),
    bg="#121417",
    fg="#00e676",
    state="disabled"
)
text_box.grid(row=2, column=0, sticky="nsew")

right.grid_rowconfigure(2, weight=1)

# =========================
# START UI
# =========================
root.mainloop()