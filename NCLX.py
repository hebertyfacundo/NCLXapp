import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from sklearn.linear_model import LinearRegression
from openpyxl import Workbook
from tkinter import PhotoImage

# Define tkinter window
root = tk.Tk()
root.title("Mitochondrial Calcium Efflux Calculator - Created by Heberty Facundo")
root.geometry('1000x500')

Title_label = ttk.Label(root, text="")
Title_label.pack(pady=5)

#image = PhotoImage(file="image.gif")
#image_label = tk.Label(root, image=image)
#image_label.pack()


def open_window():
    window2 = tk.Toplevel()
    window2.title('Mitochondrial Calcium Efflux Calculation')
    window2.geometry('800x660')

    label_name = tk.Label(window2)

    label_name.pack()
    # label_name.grid(row = 9, column = 0)
    button_voltar = tk.Button(window2, text='Close Window', font=('calibre', 12), command=window2.destroy, cursor="hand2")
    button_voltar.place(x=1050, y=600)
    # Define Treeview widget with scrollbar
    tree_frame = ttk.Frame(window2)
    tree_frame.pack(side=tk.TOP, padx=10, pady=5)
    ysb = ttk.Scrollbar(tree_frame, orient='vertical')
    ysb.pack(side=tk.RIGHT, fill=tk.Y)
    tree = ttk.Treeview(tree_frame, yscrollcommand=ysb.set, columns=('X', 'Y', 'Squared Y'))
    tree.pack(side=tk.LEFT)
    ysb.config(command=tree.yview)

    tree.heading("#1", text="Time")
    tree.column("#1", anchor="center", width=200)

    tree.heading("#2", text="Fluorescence")
    tree.column("#2", anchor="center", width=200)

    # Add new column to Treeview widget
    tree.heading("#3", text="Calcium")
    tree.column("#3", anchor="center", width=200)

    # Define button to import Excel data
    def import_excel_data():
        # Open file dialog window to choose Excel file
        file_path = filedialog.askopenfilename(parent=window2)
        # Import Excel file and convert to pandas DataFrame, starting from row 28
        df = pd.read_excel(file_path, header=0)

        # Clear existing items in Treeview widget
        tree.delete(*tree.get_children())

        # Populate Treeview widget with data
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=(row[0], row[1]))

    # Define button to import Excel data
    import_button = ttk.Button(window2, text="Import Excel Data", command=import_excel_data)
    import_button.pack(pady=5)

    def plot_data():
        x_data = []
        y_data = []
        for item in tree.get_children():
            try:
                x_val = float(tree.item(item, "values")[0])  # Extract time values from the first column
                y_val = float(tree.item(item, "values")[1])  # Extract fluorescence values from the second column
                x_data.append(x_val)
                y_data.append(y_val)
            except ValueError:
                # Handle the case where the values cannot be converted to float
                pass

        plt.plot(x_data, y_data)  # Plot time vs fluorescence
        plt.xlabel('Time (Secs)')
        plt.ylabel('Fluorescence (A.U.)')
        plt.title('Time vs Fluorescence')
        plt.show()

    # Define button to plot data
    plot_button = ttk.Button(window2, text="Time x Fluorescence Plot", command=plot_data)
    plot_button.pack()

    # Create three Entry widgets for user input
    entry_frame = ttk.Frame(window2)
    entry_frame.pack(side=tk.TOP, padx=10, pady=5)

    entry_labels = ["Kd", "Fmin", "Fmax", "Protein"]
    entry_boxes = []
    for i, label in enumerate(entry_labels):
        ttk.Label(entry_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry_box = ttk.Entry(entry_frame)
        entry_box.grid(row=i, column=1, padx=5, pady=5)
        entry_boxes.append(entry_box)

    def square_y():
        # Get values from entry boxes
        Kd = float(entry_boxes[0].get())
        Fmin = float(entry_boxes[1].get())
        Fmax = float(entry_boxes[2].get())

        # Get the value from the Entry box
        protein_entry_value = entry_boxes[3].get()

        # Check if the protein entry is empty or not
        if protein_entry_value:
            Protein = float(protein_entry_value)
        else:
            Protein = 1.0  # Default to 1 if the Entry is empty

        # Calculate squared Y values using input values and Y values from Treeview
        for item in tree.get_children():
            y_val_str = tree.item(item, "values")[1]
            try:
                y_val = float(y_val_str)

                if Fmax != y_val:
                    squared_y_val = Kd * ((y_val - Fmin) / (Fmax - y_val))
                else:
                    # Handle the case where Fmax is equal to y_val (avoid division by zero)
                    squared_y_val = 0  # You can set this value to whatever makes sense in your context

                # Check if the protein entry has a value before dividing
                if protein_entry_value:
                    squared_y_val /= Protein

                tree.set(item, column="Squared Y", value=squared_y_val)
            except ValueError:
                # Handle the case where y_val_str cannot be converted to float
                pass

        # Update difference entry box
        update_difference(None)

    # Define button to calculate squared Y values
    square_y_button = ttk.Button(window2, text="Experimental Kd", command=square_y)
    square_y_button.pack()

    diff_entry = tk.Entry(window2)
    diff_entry.pack(pady=5)

    def update_difference(event):
        # Get the selected items in the Treeview
        selection = tree.selection()

        # Calculate the difference between the last and first item in the selection
        if selection:
            first_item = float(tree.item(selection[0], "values")[2])
            last_item = float(tree.item(selection[-1], "values")[2])
            diff = last_item - first_item
            # Update the value in the entry box
            diff_entry.delete(0, tk.END)
            diff_entry.insert(0, diff)

    tree.bind("<<TreeviewSelect>>", update_difference)

    def XCa_data():
        x_data = []
        y_data = []
        for item in tree.get_children():
            try:
                x_val = float(tree.item(item, "values")[0])  # Extract time values from the first column
                y_val = float(tree.item(item, "values")[2])  # Extract Calcium values from the third column
                x_data.append(x_val)
                y_data.append(y_val)
            except ValueError:
                # Handle the case where the values cannot be converted to float
                pass
        # plt.plot(x_data, label="Y")
        plt.plot(x_data, y_data)  # Plot time vs calcium
        plt.xlabel('Time (Secs)')
        plt.ylabel('Calcium ')
        # plt.legend()
        plt.show()

    # Define button to plot data
    plotXCa_button = ttk.Button(window2, text="Time x Calcium Graph", command=XCa_data)
    plotXCa_button.pack(pady=5)

    # Define global variables
    model = LinearRegression()

    # Define function for linear regression
    def linear_regression():
        x_data = []
        squared_y_data = []
        for item in tree.selection():
            try:
                x_val = float(tree.item(item, "values")[0])
                y_val = float(tree.item(item, "values")[2])
                x_data.append(x_val)
                squared_y_data.append(y_val)
            except ValueError:
                # Handle the case where y_val_str cannot be converted to float
                pass
        X = np.array(x_data).reshape(-1, 1)
        y = np.array(squared_y_data).reshape(-1, 1)
        model.fit(X, y)
        slope = model.coef_[0][0]
        y_pred = model.predict(X)
        plt.plot(X, y_pred, label="Linear Regression")
        plt.scatter(X, y)
        plt.xlabel('Time (Secs)')
        plt.ylabel('Calcium')
        # plt.legend()
        plt.show()

    # Define function to update slope
    def update_slope(event):
        # Get the selected items in the Treeview
        selection = tree.selection()

        # Calculate the difference between the last and first item in the selection
        if selection:
            first_item = float(tree.item(selection[0], "values")[2])
            last_item = float(tree.item(selection[-1], "values")[2])
            # Call the function to train the model
            train_model(selection)
            # Get the slope from the trained model
            slope = model.coef_[0][0]
            # Update the value in the entry box
            slope_entry.delete(0, tk.END)
            slope_entry.insert(0, str(slope))

    def train_model(selection):
        x_data = []
        squared_y_data = []
        for item in selection:
            try:
                x_val = float(tree.item(item, "values")[0])
                y_val = float(tree.item(item, "values")[2])
                x_data.append(x_val)
                squared_y_data.append(y_val)
            except ValueError:
                # Handle the case where y_val_str cannot be converted to float
                pass
        X = np.array(x_data).reshape(-1, 1)
        y = np.array(squared_y_data).reshape(-1, 1)
        model.fit(X, y)

    tree.bind("<<TreeviewSelect>>", update_slope)

    # Define button to trigger linear regression
    linear_regression_button = ttk.Button(window2, text="Linear Regression", command=linear_regression)
    linear_regression_button.pack(pady=5)

    # Define label and entry box to display slope
    slope_label = ttk.Label(window2, text="Ca\u00b2\u207A Efflux Rate")
    slope_label.pack()

    slope_entry = ttk.Entry(window2)
    slope_entry.pack()

    def save_to_excel():
        # Prompt the user to choose a file path and name
        file_path = filedialog.asksaveasfilename(parent=window2,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel File"
        )

        if file_path:
            # Create a new Excel workbook
            workbook = Workbook()
            sheet = workbook.active

            # Add headers to the Excel sheet
            headers = ["Time", "Fluorescence", "Calcium"]
            sheet.append(headers)

            # Get data from the Treeview and save it to the Excel sheet
            for item in tree.get_children():
                values = tree.item(item, 'values')
                sheet.append(values)

            # Save the workbook to the selected file path
            workbook.save(file_path)

    save_button = tk.Button(window2, text="Save Treeview Data", command=save_to_excel)
    save_button.pack(pady=5)


Window2button1 = tk.Button(root, text='Mitochondrial Calcium Efflux Calculator',  font=('calibre', 20),
                            bg=("#2BD5B6"), fg=("Black"), activebackground="#2BD5B6",
                            activeforeground="#2BD5B6", command=open_window, cursor="hand2")
Window2button1.pack(pady = 25)




root.mainloop()
