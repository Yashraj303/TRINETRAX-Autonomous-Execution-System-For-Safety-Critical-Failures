> 🚨 TRINETRAX is not just a monitoring system.  
> It is an **autonomous execution system** that ensures safety actions are completed in the real world.
---

# 🚨 Problem Statement

Modern vehicles can **detect critical failures** (e.g., brake wear), but they still rely on the **driver’s decision** to act.

In real-world scenarios:

> If a system continues to function, users tend to delay action — even under risk.

This creates a dangerous gap between **detection and resolution**.

---

# ⚠️ Core Challenge

The problem is not detection.
The problem is **decision delay under risk**.

In safety-critical systems:

> **Delay directly increases accident probability.**

---

# ⚡ Our Approach

TRINETRAX introduces a new paradigm:

> **Execution-Oriented Intelligence**

Instead of assisting decisions, the system:

* Removes unsafe choices
* Takes control when required
* Ensures action is executed

---

# 🚀 What is TRINETRAX?

TRINETRAX is an **Agentic AI-powered autonomous execution ecosystem** that:

* Detects failures
* Diagnoses system health
* Classifies risk levels
* Triggers safety actions
* Executes real-world solutions

---

# 🧩 System Architecture

The system is designed as a **modular, layered architecture** for scalability and real-world integration.

---

## 🧠 1. Core Intelligence Layer (`core/`)

* `agents.py` → Multi-agent AI system
* `logic.py` → Risk evaluation & execution logic
* `service_status.txt` → Execution state tracking

### Responsibilities:

* Data interpretation
* Health computation
* Risk classification
* Decision generation

---

## 💾 2. Data Persistence Layer (`data/`)

* `vehicles.json` → Vehicle lifecycle tracking
* `slots.json` → Service slot management
* `bookings.json` → Booking records

### Key Properties:

* Persistent state management
* No duplicate bookings
* Real-time slot validation

---

## 🏢 3. Service Execution Layer (`service_system/`)

* Service center interface
* Slot-based booking system
* Pincode-based filtering

### Real-World Constraints Modeled:

* Limited slot availability
* No artificial slot reset
* Booking visibility

---

## 🖥️ 4. User Interface Layer (`ui/`)

* `trinetrax_ui.py` → Main execution interface

### Role:

* System interaction
* Workflow initiation
* Output visualization

---

## 🖥️ 5. ESP-32 Hardware Layer(`ESP-32.txt/`)

### Role:

* Integrates the software to hardware prototype

---

# 🧠 Multi-Agent System

TRINETRAX uses structured agents:

* **Data Agent** → collects input parameters
* **Diagnosis Agent** → evaluates system condition
* **Decision Agent** → classifies risk (NORMAL → CRITICAL)
* **Execution Agent** → triggers actions

---

# 🚗 Execution Workflow

1. Vehicle data is processed
2. AI computes system health
3. Risk level is classified
4. If CRITICAL → ADAS safety triggered
5. Vehicle identified (tracking system)
6. Service centers filtered (pincode-based)
7. Available slots evaluated
8. Booking automatically confirmed

---

# 🔒 Core Innovation

Traditional systems:

* Provide warnings
* Offer flexibility
* Depend on user action

TRINETRAX:

* Does not provide delay options
* Does not expose “safe usage limits”
* Enforces immediate resolution

> **User decision → System execution**

---

# 🚗 ADAS Safety Integration

When risk becomes CRITICAL:

* Safe stop is triggered
* Vehicle stabilization executed
* Driver notified

This ensures **physical safety enforcement**, not just alerts.

---

# 🔄 State-Aware Execution

The system maintains continuity using:

* `vehicles.json`
* `slots.json`
* `bookings.json`
* `service_status.txt`

Ensuring:

* No duplicate execution
* No slot overflow
* Reliable workflow tracking

---

# ⚙️ Setup Instructions

## 1. Install Python (if not installed)

Download from: https://www.python.org/downloads/

---

## 2. Install Dependencies

```bash
pip install pillow
```

---

##  Run TRINETRAX (Main System)

```bash
cd Documents/TRINETRAX-Hardware/ui
python trinetrax_ui.py
```

---

##  Run TRINETRAX 2.0 (Service System)

```bash
cd Documents/TRINETRAX-Hardware/service_system
python ui.py
```
---

## Upload code in ESP-32 via ARUDINO_IDE application

```bash
ESP-32.txt
```
---

## 📌 Notes

* Ensure the `TRINETRAX` folder is inside the `Documents` directory
* Run both systems in separate terminals if needed
* Data files (`vehicles.json`, `slots.json`, `bookings.json`) are automatically managed


---

# 📁 Project Structure

```bash
TRINETRAX-Hardware/
├── core/
│   ├── agents.py
│   ├── logic.py
│   └── service_status.txt
│
├── data/
│   ├── bookings.json
│   ├── slots.json
│   └── vehicles.json
│
├── service_system/
│   ├── ui.py
│   └── trinetrax_2.0_logo.jpeg
│
├── ui/
│   ├── trinetrax_ui.py
│   ├── trinetrax_logo.jpeg
│   └── service_status.txt
│
├── ESP-32.txt/
```

---

# 📊 Impact Potential

* Reduces accident probability
* Eliminates unsafe delay behavior
* Improves maintenance compliance
* Optimizes service infrastructure usage

---

# 🧠 Innovation Summary

TRINETRAX introduces:

> **Execution-Oriented Intelligence**

Where systems:

* Do not wait for user decisions
* Do not allow unsafe delays
* Do not stop at detection

---

# 🏆 Final Perspective

Most systems:
→ Detect problems

Some systems:
→ Predict problems

**TRINETRAX:**
→ Ensures problems are resolved

---

#  One-Line Insight

> **TRINETRAX removes the option to ignore safety**

---

# 👥 Team

Cosmic Shifts
---
