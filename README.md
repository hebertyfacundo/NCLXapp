Mitochondrial Calcium Efflux Calculator

Description
Mitochondrial Calcium Efflux Calculator is a desktop application built with Python's Tkinter library for researchers studying mitochondrial calcium dynamics. This tool processes fluorescence data from experiments to calculate calcium concentrations and efflux rates, with particular application to NCLX (Sodium/Calcium/Lithium Exchanger) studies.

The application provides a user-friendly graphical interface for importing Excel data, performing calculations, visualizing results, and exporting processed data.

✨ Features
📂 Excel Data Import - Import experimental data from Excel files
⚙️ Parameter Configuration - Set Kd, Fmin, Fmax, and Protein values
🧮 Experimental Kd Calculation - Compute calcium concentrations using the standard formula
📊 Interactive Data Table - View and select data points with Treeview widget
📈 Visualization Tools:
	Time vs Fluorescence plots
	Time vs Calcium plots
	Linear regression analysis
💾 Export Results - Save calculated data as Excel files
📉 Linear Regression - Calculate Ca²⁺ efflux rates from selected data
🖱️ Interactive Selection - Select data ranges for analysis

🧪 Formula Used
The application calculates calcium concentration using:
text
Calcium = Kd × ((Fluorescence - Fmin) / (Fmax - Fluorescence))
Where:
Kd = Dissociation constant
Fmin = Minimum fluorescence (no calcium)
Fmax = Maximum fluorescence (saturating calcium)
Protein = Protein concentration factor (optional)

📦 Installation
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Step-by-Step Installation
# 1. Download the repository
git clone https://github.com/hebertyfacundo/NCLXapp.git

# 2. Enter the folder
cd NCLXapp

# 3. Create a virtual environment (optional but recommended)
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python NCLX.py  

Main Window:

Click the "Mitochondrial Calcium Efflux Calculator" button to open the main calculation window

Calculation Window:

Import Data: Click "Import Excel Data" to load your Excel file
File must contain Time and Fluorescence columns
Data loads from the first row (header)
Set Parameters: Enter values for:
Kd (Dissociation constant)
Fmin (Minimum fluorescence)
Fmax (Maximum fluorescence)
Protein (Optional - defaults to 1.0)
Calculate: Click "Experimental Kd" to compute calcium values
Results appear in the "Calcium" column

Visualize Data:

Click "Time x Fluorescence Plot" for raw data visualization
Click "Time x Calcium Graph" for calculated calcium data
Perform Regression:
Select data points in the table (click and drag or Ctrl+click)
Click "Linear Regression" to analyze selected data
The Ca²⁺ efflux rate appears in the "Ca²⁺ Efflux Rate" field
Save Results: Click "Save Treeview Data" to export as Excel file

Input File Format
Your Excel file should have at least two columns:

Time	Fluorescence
0.0	100.5
0.5	120.3
1.0	115.7
...	...
Note: The application assumes the first row contains headers

🛠️ Dependencies
pandas - Data manipulation
numpy - Numerical computing
matplotlib - Plotting and visualization
scikit-learn - Linear regression
openpyxl - Excel file support
tkinter - GUI framework (included with Python)

📁 Project Structure
text
NCLXapp/ 
│
├── NCLX.py              # Main application script
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── LICENSE             # MIT License

🖥️ User Interface Guide
Main Window
Single button to launch the calculator
Clean, centered layout
Title includes author attribution

Calculation Window
Data Table: Displays Time, Fluorescence, and Calcium values
Import Button: Load Excel data
Parameter Inputs: Kd, Fmin, Fmax, Protein

Action Buttons:

Experimental Kd - Calculate calcium concentrations
Time x Fluorescence Plot - Visualize raw data
Time x Calcium Graph - Visualize calculated data
Linear Regression - Perform regression on selected data
Save Treeview Data - Export results

Results Display:
Calcium Difference (between first and last selected points)
Ca²⁺ Efflux Rate (slope from linear regression)

📊 Workflow Example
Load Data: Import your Excel file with time and fluorescence data
Set Parameters: Enter your experimental Kd, Fmin, Fmax values
Calculate: Click "Experimental Kd" to generate calcium values
Visualize: Check the Time x Calcium Graph for data quality
Select Range: Click and drag to select the linear portion of your data
Analyze: Click "Linear Regression" to calculate efflux rate
Export: Save your results as an Excel file

🔬 Research Application
This tool is particularly useful for:
NCLX Activity Studies - Measuring mitochondrial sodium/calcium exchanger activity
Calcium Efflux Kinetics - Analyzing rate of calcium release from mitochondria
Drug Screening - Testing compounds affecting mitochondrial calcium handling
Metabolic Research - Studying calcium's role in mitochondrial metabolism

📝 Version History
v1.0.0 (2026)
Initial release
Excel import functionality
Kd calculation
Linear regression analysis
Data export

cff-version: 1.2.0
message: "If you use this software, please cite it using these metadata."
title: "NCLXapp: Mitochondrial Calcium Efflux Calculator"
version: 1.0.0
date-released: 2026-07-12
authors:
  - family-names: "Facundo"
    given-names: "Heberty di Tarso Fernandes"
    email: "Heberty.facundo@gmail.com"
    affiliation: "Universidade Federal do Cariri"
repository-code: "https://github.com/hebertyfacundo/NCLXapp"
keywords:
  - mitochondrial calcium
  - NCLX
  - fluorescence
  - efflux
type: software

📄 License
Distributed under the MIT License. See LICENSE for more information.

Author
Heberty di Tarso Fernandes Facundo

Acknowledgments
Alicia Juliana Kowaltowski and Maiara Ingrid Cavalcante Queiroz (researchers studying mitochondrial calcium dynamics) for testing the software. 
Open-source community for providing essential tools

Contact
For questions, suggestions, or collaboration: Heberty.facundo@gmail.com
GitHub Issues: Create an issue

💡 Tips for Best Results
Data Quality: Ensure your fluorescence data is clean and properly normalized
Parameter Selection: Use literature values or calibration curves for Kd, Fmin, and Fmax
Linear Range: Select only the linear portion of your data for regression analysis
Replicates: Run multiple experiments for statistical significance
Export: Always save your results with appropriate metadata

⚠️ Troubleshooting
Issue	Solution
Excel file won't import	Ensure file has at least 2 columns and first row contains headers
Division by zero error	Check that Fmax ≠ any fluorescence value
Plot won't show	Ensure matplotlib backend is properly configured
Regression fails	              Select at least 2 data points before running regression
