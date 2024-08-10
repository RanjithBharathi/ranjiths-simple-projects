import tkinter as tk
from tkinter import messagebox

# Extended dataset with more crops
data = {
    "what is the principal name": {"HERE IS YOUR RESULT :":"Dr.P.Govindasamy"},
    "where is office":{"HERE IS YOUR RESULT :":"CABIN NO A108"},
    "how many departments are there in the college":{"HERE IS YOUR RESULT :":"12 Departments"},
    "where is the principal's office located":{"HERE IS YOUR RESULT :":" CABIN A106"},
    "who is the HOD of the AIDS department":{"HERE IS YOUR RESULT :":"Dr.J.Ramprasanth"},
    "what is the room number of the AIDS department":{"HERE IS YOUR RESULT:":"CABIN C321"},
    "how many libraries are there in the college":{"HERE IS YOUR RESULT:":"3 mainlibraries"},
    "how many auditoriums are there in the college":{"HERE IS YOUR RESULT:":"2 Audiotoriums"},
    "when can i meet the principal":{"HERE IS YOUR RESULT:":"you can meet after 4:30pm"}
}


def display_info():
    stu_name = stu_entry.get()
    if stu_name in data:
        stu_info = data[stu_name]
        for i, (heading, value) in enumerate(stu_info.items()):
            tk.Label(root, text=heading, font=("Helvetica", 12, "bold")).grid(row=i+2, column=0, sticky="w", padx=5, pady=5)
            tk.Label(root, text=value, font=("TimesNewRoman", 14, "bold"), wraplength=400).grid(row=i+2, column=1, sticky="w", padx=5, pady=5)
    else:
        messagebox.showerror("Error", "Detail not found in database.")

root = tk.Tk()
root.title("MCET ASSISTANT")

stu_label = tk.Label(root, text="ENTER THE DETAILS YOU WANT", font=("Helvetica", 14, "bold"))
stu_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

stu_entry = tk.Entry(root, width=50)
stu_entry.grid(row=1, column=0, padx=9, pady=9)

show_button = tk.Button(root, text="Show Info", command=display_info)
show_button.grid(row=1, column=1, padx=5, pady=5)

# Display headings initially (empty for now)
headings = []
for i, heading in enumerate(headings):
    tk.Label(root, text=heading, font=("Helvetica", 12, "bold")).grid(row=i+2, column=0, sticky="w", padx=5, pady=5)
    tk.Label(root, text="", font=("TimesNewRoman", 18, "bold"), wraplength=400).grid(row=i+2, column=1, sticky="w", padx=5, pady=5)

root.mainloop()
