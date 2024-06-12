import tkinter as tk
from tkinter import messagebox, filedialog
from getData import *

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
        
        init(file = file, multi_ = multi.get(), lc_ = lc.get())
        
        V_DATA = getData()
        
        clean_formula = ""
        for i in formula:
            if i.isalpha():
                clean_formula += i
            else:
                clean_formula += " "
            # if i == '.': clean_formula += '.'
        variables = set(i for i in clean_formula.split() if i[0] != '.')
        
        output = [f"公式: {formula}, 計算 A 類不確定度: {multi.get()}, lc: {lc.get()}"]
        res = []

        for i in range(len(list(V_DATA.values())[0])):
            substituted_formula = formula
            for var in variables:
                substituted_formula = substituted_formula.replace(var, f"V_DATA['{var}'][{i}]")
            print("Formula:", substituted_formula)
            ans = eval(substituted_formula)
            print(ans)
            output.append(f"第 {i + 1} 次結果: {ans}")
            res.append(ans)
        
        length = Data(len(res), 0)
        for i in res[1:]: res[0] = res[0] + i
        res[0] = res[0] / length
        output.append(f"最後平均: {res[0]}") # 待補
        path = saveResults(output, file)
        print("Success")
        messagebox.showinfo("Success", f"Results is saved at {path}")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", e)


def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("不確定度計算器")

# Set the window size to double
root.geometry("800x300")  # Width: 800, Height: 400

# Define Microsoft JhengHei font
font_msjh = ("Microsoft JhengHei", 12)  # Font: Microsoft JhengHei, Size: 12

# Create and pack widgets
file_label = tk.Label(root, text="File Path:", font=font_msjh)  # Set font to Microsoft JhengHei
file_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")
file_entry = tk.Entry(root, width=60, font=font_msjh)  # Set font to Microsoft JhengHei
file_entry.grid(row=0, column=1, padx=20, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_file, font=font_msjh)  # Set font to Microsoft JhengHei
browse_button.grid(row=0, column=2, padx=10, pady=10)

formula_label = tk.Label(root, text="算式:", font=font_msjh)  # Set font to Microsoft JhengHei
formula_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
formula_entry = tk.Entry(root, width=60, font=font_msjh)  # Set font to Microsoft JhengHei
formula_entry.grid(row=1, column=1, padx=20, pady=10)

multi = tk.BooleanVar()
multi_check = tk.Checkbutton(root, text="同組實驗多次重複操作(A 類不確定度)", variable=multi, font=font_msjh)  # Set font to Microsoft JhengHei
multi_check.grid(row=2, column=1, padx=20, pady=10, sticky="w")

lc_label = tk.Label(root, text="LC:", font=font_msjh)  # Set font to Microsoft JhengHei
lc_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")
lc = tk.DoubleVar(value=0.1)
lc_entry = tk.Entry(root, textvariable=lc, font=font_msjh)  # Set font to Microsoft JhengHei
lc_entry.grid(row=3, column=1, padx=20, pady=10)

run_button = tk.Button(root, text="Run", command=run_program, font=font_msjh)  # Set font to Microsoft JhengHei
run_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

# Start the event loop
root.mainloop()
