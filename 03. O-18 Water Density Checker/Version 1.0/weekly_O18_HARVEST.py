import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import serial.tools.list_ports
import csv
from datetime import datetime


# ==========================
# SETTINGS
# ==========================

SYNTHESIZERS = [
    "Synthesizer H",
    "Synthesizer J",
    "Synthesizer K",
    "Synthesizer L",
    "Synthesizer M",
    "Synthesizer N",
    "Synthesizer O",
    "Synthesizer P",
    "Synthesizer Q",
    "Additional Collection"
]

BAUD_RATE = 9600


# ==========================
# SCALE
# ==========================

class Scale:

    def __init__(self):
        self.connection = None


    def connect(self, port):

        try:
            self.connection = serial.Serial(
                port,
                BAUD_RATE,
                timeout=2
            )

            return True

        except Exception as e:

            messagebox.showerror(
                "Connection Error",
                str(e)
            )

            return False



    def read_weight(self):

        if self.connection is None:
            return None


        try:

            self.connection.reset_input_buffer()

            data = self.connection.readline()

            value = data.decode().strip()

            return float(value)


        except:

            return None



# ==========================
# APPLICATION
# ==========================

class WeightCollector:


    def __init__(self, root):

        self.root = root

        self.root.title(
            "Weekly Synthesizer Harvest Collection"
        )


        self.scale = Scale()

        self.records = []

        self.captured_weight = None


        self.create_gui()



    def create_gui(self):


        tk.Label(
            self.root,
            text="Synthesizer",
            font=("Arial",14)
        ).pack()


        self.synth_box = ttk.Combobox(

            self.root,

            values=SYNTHESIZERS,

            state="readonly"

        )

        self.synth_box.pack()

        self.synth_box.current(0)



        # COM PORT


        frame = tk.Frame(self.root)

        frame.pack(pady=10)


        tk.Label(
            frame,
            text="COM Port"
        ).grid(
            row=0,
            column=0
        )


        ports = [

            p.device

            for p in serial.tools.list_ports.comports()

        ]


        self.port_box = ttk.Combobox(

            frame,

            values=ports

        )


        self.port_box.grid(
            row=0,
            column=1
        )


        tk.Button(

            frame,

            text="Connect",

            command=self.connect

        ).grid(
            row=0,
            column=2
        )



        # WEIGHT DISPLAY


        self.weight_display = tk.Label(

            self.root,

            text="0.000 g",

            font=("Arial",28)

        )


        self.weight_display.pack(
            pady=20
        )



        tk.Button(

            self.root,

            text="Capture Weight",

            command=self.capture

        ).pack()



        self.captured_label = tk.Label(

            self.root,

            text="Captured: ---"

        )

        self.captured_label.pack()



        # VOLUME


        tk.Label(

            self.root,

            text="Volume (mL)"

        ).pack()


        self.volume = tk.Entry(

            self.root

        )

        self.volume.pack()


        self.volume.bind(

            "<Return>",

            lambda x: self.save()

        )


        tk.Button(

            self.root,

            text="Save Entry",

            command=self.save

        ).pack(pady=10)



        # TABLE


        columns = (

            "Synthesizer",

            "Weight",

            "Volume",

            "Density (g/mL)",

            "Time"

        )


        self.table = ttk.Treeview(

            self.root,

            columns=columns,

            show="headings"

        )


        for col in columns:

            self.table.heading(

                col,

                text=col

            )


        self.table.pack(
            pady=20
        )



        tk.Button(

            self.root,

            text="Export CSV",

            command=self.export

        ).pack()



        tk.Button(

            self.root,

            text="Clear Collection",

            command=self.clear

        ).pack()



    def connect(self):

        if self.scale.connect(

            self.port_box.get()

        ):

            messagebox.showinfo(

                "Connected",

                "Scale connected"

            )



    def capture(self):

        weight = self.scale.read_weight()


        if weight is None:

            messagebox.showerror(

                "Error",

                "No weight received"

            )

            return


        self.captured_weight = weight


        self.weight_display.config(

            text=f"{weight:.3f} g"

        )


        self.captured_label.config(

            text=f"Captured: {weight:.3f} g"

        )



    def save(self):

        if self.captured_weight is None:

            messagebox.showwarning(

                "Missing",

                "Capture weight first"

            )

            return



        try:
            
            vol = float(

                self.volume.get(),

            )


        except:

            messagebox.showerror(

                "Error",

                "Invalid volume"

            )

            return

        density = self.captured_weight / vol # TAG



        row = [

            self.synth_box.get(),
            round(self.captured_weight, 3),
            round(vol, 2),
            round(density, 4),
            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        ]


        self.records.append(row)



        self.table.insert(

            "",

            "end",

            values=row

        )


        self.volume.delete(

            0,

            tk.END

        )


        self.captured_weight = None



    def export(self):


        filename = filedialog.asksaveasfilename(

            defaultextension=".csv",

            filetypes=[

                ("CSV","*.csv")

            ],

            initialfile=

            "Synthesizer_Harvest.csv"

        )


        if filename:


            with open(

                filename,

                "w",

                newline=""

            ) as f:


                writer = csv.writer(f)


                writer.writerow(

                    [

                    "Synthesizer",

                    "Weight (g)",

                    "Volume (mL)",

                    "Density (g/mL)",

                    "Timestamp"

                    ]

                )


                writer.writerows(

                    self.records

                )


            messagebox.showinfo(

                "Complete",

                "CSV exported"

            )



    def clear(self):

        self.records.clear()

        for row in self.table.get_children():

            self.table.delete(row)




root = tk.Tk()

app = WeightCollector(root)

root.mainloop()