import tkinter as tk
from tkinter import messagebox, filedialog
from tool.getData import init, getData, saveResults

def run_program():
    try:
        file = file_entry.get()
        formula = formula_entry.get()
        
        if not file:
            messagebox.showerror("Error", "Please provide a file path.")
            return
        if not formula:
            messagebox.showerror("Error", "Please provide a formula.")
            return
        
        init(file=file, multi_=multi.get(), lc_=lc.get())
        
        V_DATA = getData()
        
        clean_formula = ""
        for i in formula:
            if i.isalpha():
                clean_formula += i
            else:
                clean_formula += " "
        variables = set(clean_formula.split())
        
        output = []
        for i in range(len(list(V_DATA.values())[0])):
            substituted_formula = formula
            for var in variables:
                substituted_formula = substituted_formula.replace(var, f"V_DATA['{var}'][{i}]")
            ans = eval(substituted_formula)
            print(ans)
            output.append(ans)
        
        path = saveResults(output)
        messagebox.showinfo("Success", f"Results is saved at {path}")
    except Exception as e:
        messagebox.showerror("Error", e)


def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("不確定度計算器")

# Create and pack widgets
file_label = tk.Label(root, text="File Path:")
file_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

formula_label = tk.Label(root, text="算式:")
formula_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
formula_entry = tk.Entry(root, width=50)
formula_entry.grid(row=1, column=1, padx=10, pady=5)

multi = tk.BooleanVar()
multi_check = tk.Checkbutton(root, text="Multi", variable=multi)
multi_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

lc_label = tk.Label(root, text="LC:")
lc_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
lc = tk.DoubleVar(value=0.01)
lc_entry = tk.Entry(root, textvariable=lc)
lc_entry.grid(row=3, column=1, padx=10, pady=5)

run_button = tk.Button(root, text="Run", command=run_program)
run_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Start the event loop
root.mainloop()
