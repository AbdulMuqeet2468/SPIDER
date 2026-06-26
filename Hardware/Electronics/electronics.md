# Electronics Documentation

## Overview

This document covers the electronics design for SPIDER, including the power system, servo control, and microcontroller setup.

---

## Components

| Component | Specification | Purpose |
|---|---|---|
| Microcontroller | ESP32 | Main controller (Wi-Fi/BT capable) |
| PWM Driver | PCA9685 | 16-channel servo driver via I²C |
| Buck Converter | 10A, 300W | Steps down battery voltage to 5V for servos |
| Battery Pack | 2S3P Li-Ion | Main power source (~7.4V nominal) |
| BMS | 2S BMS | Cell protection & balancing |

---

## Power System

### Battery Pack — 2S3P Li-Ion

SPIDER is powered by a custom **2S3P Li-Ion battery pack**:

- **2S** → 2 cells in series → ~7.4V nominal, 8.4V fully charged
- **3P** → 3 cells in parallel per series group → higher capacity (3× a single cell)


#### How to Build a Custom Li-Ion Battery Pack

> ⚠️ **Warning:** Li-Ion cells can catch fire or explode if mishandled. Work carefully, avoid shorts, and never leave charging unattended.

**Materials needed:**
- 6× Li-Ion 18650 cells (matched capacity recommended)
- 2S BMS module (rated for your current draw)
- Nickel strips (0.15–0.2 mm thickness)
- Solder iron (spot welder recommended)
- Heat shrink tubing
- Kapton tape (recommended)
- Multimeter

**Steps:**

1. **Test all cells** — Measure each cell's voltage and internal resistance. Use only cells within ±0.05V of each other.

2. **Build the parallel groups (P groups)** — Place 3 cells side-by-side (same orientation). Solder nickel strips across the positive ends and negative ends to connect them in parallel. You now have two 3P groups.

3. **Connect groups in series (S)** — Connect the negative terminal of one 3P group to the positive terminal of the other using a nickel strip. This gives you 2S3P.

4. **Attach the BMS** — Wire the BMS according to its datasheet:
   - `B-` → pack negative
   - `B1` (balance tap) → midpoint between the two groups
   - `B+` → pack positive
   - `P-` and `P+` → output terminals

5. **Insulate & wrap** — Apply Kapton tape between cells to prevent shorts. Slide heat shrink tubing over the entire pack and shrink with a heat gun.

6. **Verify output** — Measure voltage at the output terminals. Should read ~7.4–8.4V.

---

### 2S BMS

The BMS (Battery Management System) provides:
- **Overcurrent protection**
- **Overcharge / over-discharge protection**
- **Cell balancing** between the two series groups

Select a BMS rated for at least the peak current draw of your robot.

---

### Buck Converter (10A, 300W)

Servos typically require **5V**, but the 2S battery outputs ~7.4–8.4V. The buck converter steps this down.

**Wiring:**
```
Battery (+) ──► Buck IN+
Battery (-) ──► Buck IN-
Buck OUT+ ──► 5V Rail (PCA9685 VCC + Servo power)
Buck OUT- ──► GND Rail
```

**Setup:**
- Adjust the output trim potentiometer to exactly **5.0V** before connecting servos.
- Ensure the converter is rated beyond your total servo stall current (sum of all servos × stall current).

---

## Servo Control

### PCA9685 PWM Driver

The **PCA9685** is a 16-channel PWM driver communicating over **I²C**, allowing the ESP32 to control all leg servos with just 2 GPIO pins.

**Wiring to ESP32:**

| PCA9685 Pin | ESP32 Pin |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |
| V+ | 5V Rail (from buck converter) |

> The `V+` pin powers the servo motors directly — connect it to the 5V output of the buck converter, **not** the ESP32's 3.3V or 5V pin.


## Safety Notes

- Always **power down** before rewiring.
- Never bypass the BMS output for servo power.
- Add a **main fuse** (10–15A) between the battery and the rest of the circuit.
- Use adequately rated wires for the high-current servo rail (18–20 AWG minimum).


**Note**
We removed DC motor feature, thats why it is not mentioned in the documentation
