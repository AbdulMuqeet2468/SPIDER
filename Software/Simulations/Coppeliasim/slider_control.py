#=========== ALL THE LIBRARIES ================
import math
import numpy as np
import time
import tkinter as tk
from tkinter import ttk
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

#=========== CONNECT TO COPPELIASIM ================
client = RemoteAPIClient()
sim = client.require('sim')
sim.startSimulation()
time.sleep(0.5)

#=========== ROBOT CONFIGURATION & HANDLES ================
LEG_JOINT_NAMES = {
    'R1': ('R1_coxa_joint', 'R1_femur_joint', 'R1_tibia_joint'),
    'R2': ('R2_coxa_joint', 'R2_femur_joint', 'R2_tibia_joint'),
    'L1': ('L1_coxa_joint', 'L1_femur_joint', 'L1_tibia_joint'),
    'L2': ('L2_coxa_joint', 'L2_femur_joint', 'L2_tibia_joint'),
}

handles = {}
print("Fetching joint handles...")
for leg, (cj, fj, tj) in LEG_JOINT_NAMES.items():
    handles[leg] = {
        'coxa' : sim.getObject(f'/{cj}'),
        'femur': sim.getObject(f'/{fj}'),
        'tibia': sim.getObject(f'/{tj}'),
    }

#=========== GUI APPLICATION ================
class QuadrupedControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadruped Joint Controller")
        self.root.geometry("520x780")
        self.root.configure(bg="#f5f5f7") # Clean, light-gray background
        
        # Configure modern theme styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabelframe', background='#f5f5f7', borderwidth=1)
        self.style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold'), foreground='#333333', background='#f5f5f7')
        self.style.configure('TLabel', font=('Helvetica', 10), background='#f5f5f7', foreground='#444444')
        self.style.configure('Reset.TButton', font=('Helvetica', 11, 'bold'), foreground='white', background='#e05252')
        self.style.map('Reset.TButton', background=[('active', '#c0392b')])

        # Dictionaries to store widgets and tracking variables
        self.sliders = {}
        self.value_labels = {}

        # Top Header / Control Panel
        top_panel = ttk.Frame(root, padding=10)
        top_panel.pack(fill="x")
        
        # Reset Button (Sets everything back to 0)
        reset_btn = ttk.Button(top_panel, text="Reset All to 0°", style='Reset.TButton', command=self.reset_all_joints)
        reset_btn.pack(fill="x", ipady=5, padx=5)

        # Create a scrollable container for the sliders
        canvas = tk.Canvas(root, bg="#f5f5f7", highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Build UI layout grouped by Leg (R1, R2, L1, L2)
        for leg_id, joint_types in handles.items():
            leg_frame = ttk.LabelFrame(scrollable_frame, text=f" Leg {leg_id} ", padding=12)
            leg_frame.pack(fill="x", expand=True, pady=8, padx=5)
            
            self.sliders[leg_id] = {}
            self.value_labels[leg_id] = {}

            for joint_type in ['coxa', 'femur', 'tibia']:
                row_frame = ttk.Frame(leg_frame)
                row_frame.pack(fill="x", pady=4)

                # Joint name indicator
                name_label = ttk.Label(row_frame, text=f"{joint_type.capitalize()}:", width=10, font=('Helvetica', 10, 'bold'))                
                name_label.pack(side="left")

                # Dynamic angle feedback label
                v_label = ttk.Label(row_frame, text="0.0° (0.00 rad)", width=18, anchor="e")
                v_label.pack(side="right", padx=5)
                self.value_labels[leg_id][joint_type] = v_label

                # Slider control restricted strictly from -90 to +90 degrees
                slider = ttk.Scale(
                    row_frame, 
                    from_=-90.0, 
                    to=90.0, 
                    orient="horizontal",
                    command=lambda val, l=leg_id, j=joint_type: self.on_slider_move(l, j, val)
                )
                slider.set(0.0) # Default to center position
                slider.pack(side="left", fill="x", expand=True, padx=5)
                self.sliders[leg_id][joint_type] = slider

        # Handle clean window termination
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_slider_move(self, leg_id, joint_type, value):
        """Processes degrees from slider, converts to radians, and commands CoppeliaSim."""
        deg_val = float(value)
        rad_val = math.radians(deg_val)
        
        # Update text layout (displays Degrees first prominently)
        self.value_labels[leg_id][joint_type].config(text=f"{deg_val:.1f}° ({rad_val:.2f} rad)")
        
        # Send target command to CoppeliaSim
        joint_handle = handles[leg_id][joint_type]
        if joint_handle is not None:
            try:
                sim.setJointTargetPosition(joint_handle, rad_val)
            except Exception as e:
                print(f"Error communicating with {leg_id}_{joint_type}: {e}")

    def reset_all_joints(self):
        """Resets every slider back to 0 degrees systematically."""
        for leg_id in self.sliders:
            for joint_type in self.sliders[leg_id]:
                self.sliders[leg_id][joint_type].set(0.0)

    def on_closing(self):
        """Stops simulation loop elegantly on GUI close."""
        print("Stopping simulation...")
        try:
            sim.stopSimulation()
        except Exception:
            pass
        self.root.destroy()

#=========== MAIN EXECUTION ================
if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedControllerGUI(root)
    root.mainloop()