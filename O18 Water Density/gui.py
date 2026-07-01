import tkinter as tk
from tkinter import ttk

from serial_reader import Balance


class DensityLogger:

    def __init__(self, root):

        self.root = root

        self.balance = Balance()

        self.weight = tk.StringVar(value="Waiting for PRINT...")

        self.current_weight = None

        ttk.Button(
            root,
            text="Capture Weight",
            command=self.capture_weight
        ).pack(pady=15)

        
        ttk.Label(
            root,
            text="Current Weight",
            font=("Arial",16)
        ).pack(pady=10)

        ttk.Label(
            root,
            textvariable=self.weight,
            font=("Arial",30)
        ).pack()

        # Start checking for new weights
        self.check_serial()

    def check_serial(self):

        while not self.balance.data_queue.empty():

            value = self.balance.data_queue.get()

            self.weight.set(f"{value:.4f} g")

        # Check again in 100 ms
        self.root.after(100, self.check_serial)


    def capture_weight(self):
    #Stores whatever weight is currently displayed.
        try:

            # Remove the " g" from the displayed text
            text = self.weight.get().replace(" g", "")

            self.current_weight = float(text)

            print(f"Captured weight: {self.current_weight:.4f} g")

        except ValueError:

            print("No valid weight to capture.")