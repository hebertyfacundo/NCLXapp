"""
MITOCHONDRIAL EFFLUX CALCULATOR - Fluorescence-based Kd Iteration
With Interactive Linear Regression for Time vs Calcium
"""

import streamlit as st
import math
import pandas as pd
import numpy as np
from datetime import datetime
import io
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit.dataframe_util")

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="MITOCHONDRIAL Calcium Efflux Calculator - Fluorescence Analysis",
    page_icon="🧪",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 5px solid #2E86AB;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border-radius: 5px;
    }
    .result-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1.5rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .success-box {
        background-color: #d1e7dd;
        border: 1px solid #0f5132;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .regression-box {
        background-color: #f0f7ff;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if 'df_export' not in st.session_state:
    st.session_state.df_export = None
if 'regression_data' not in st.session_state:
    st.session_state.regression_data = None
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False


# ============================================================================
# FUNCTIONS
# ============================================================================

def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        col_str = str(col)
        col_str = col_str.replace(':', '_')
        col_str = col_str.replace(' ', '_')
        col_str = col_str.replace('.', '_')
        col_str = col_str.replace('(', '_')
        col_str = col_str.replace(')', '_')
        new_columns.append(col_str)
    df.columns = new_columns
    return df


def read_excel_file(uploaded_file):
    file_name = uploaded_file.name
    file_extension = file_name.split('.')[-1].lower()

    if file_extension == 'csv':
        return pd.read_csv(uploaded_file)

    try:
        if file_extension in ['xlsx', 'xlsm']:
            return pd.read_excel(uploaded_file, engine='openpyxl')
        elif file_extension == 'xls':
            return pd.read_excel(uploaded_file, engine='xlrd')
        else:
            try:
                return pd.read_excel(uploaded_file, engine='openpyxl')
            except:
                return pd.read_excel(uploaded_file, engine='xlrd')
    except Exception as e:
        try:
            return pd.read_excel(uploaded_file, engine='openpyxl')
        except:
            raise Exception(f"Could not read file: {str(e)}")


def display_dataframe_safely(df):
    df_display = df.copy()
    for col in df_display.columns:
        try:
            df_display[col] = df_display[col].astype(str)
        except:
            df_display[col] = df_display[col].apply(lambda x: str(x))
    return df_display


def fluorescence_to_calcium(F, Fmin, Fmax, Kd):
    try:
        if Fmax - F == 0:
            return float('inf')
        calcium = Kd * ((F - Fmin) / (Fmax - F))
        return round(calcium, 4)
    except:
        return None


def linear_regression_slope(x, y):
    try:
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)
        reg = LinearRegression()
        reg.fit(x, y)
        slope = reg.coef_[0]
        intercept = reg.intercept_
        r_squared = reg.score(x, y)
        return slope, intercept, r_squared
    except:
        return None, None, None


def validate_number(value, field_name):
    if value is None or value == "":
        return False, f"{field_name}: Campo não pode estar vazio"
    try:
        str_value = str(value).strip().replace(',', '.')
        float_value = float(str_value)
        if float_value <= 0:
            return False, f"{field_name}: Valor deve ser maior que 0"
        return True, float_value
    except ValueError:
        return False, f"{field_name}: Deve ser um número válido (use ponto '.')"


def validate_all_inputs(inputs_dict):
    errors = []
    validated = {}
    for field_name, value in inputs_dict.items():
        is_valid, result = validate_number(value, field_name)
        if not is_valid:
            errors.append(result)
        else:
            validated[field_name] = result
    return len(errors) == 0, errors, validated


# ============================================================================
# MAIN INTERFACE
# ============================================================================

st.markdown('<h1 class="main-header">🧪 Mitochondrial Calcium Efflux Calculator - Fluorescence Analysis</h1>',
            unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<h4>📋 <strong>How to use this calculator:</strong></h4>
<ol>
    <li>Enter <strong>Fmin</strong>, <strong>Fmax</strong>, fluorescence values, and <strong>Kd guess</strong></li>
    <li>Click <strong>"Calculate"</strong> and iterate Kd until calcium difference matches expected</li>
    <li>Upload time series data and <strong>calculate calcium</strong> for each time point</li>
    <li>Use <strong>interactive slider</strong> to select data range for linear regression</li>
    <li>View and download <strong>slope</strong> (rate of calcium change over time)</li>
</ol>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# STEP 1: FLUORESCENCE LIMITS
# ============================================================================

st.markdown("## 📊 Step 1: Enter Fluorescence Limits")

col1, col2 = st.columns(2)

with col1:
    fmin = st.text_input("Fmin (minimum fluorescence)", value="", placeholder="e.g., 100")
    fmax = st.text_input("Fmax (maximum fluorescence)", value="", placeholder="e.g., 500")

with col2:
    protein_level = st.text_input("Protein concentration (mg/mL)", value="", placeholder="e.g., 2.5")

# ============================================================================
# STEP 2: FLUORESCENCE VALUES
# ============================================================================

st.markdown("## 🔬 Step 2: Enter Fluorescence Values")

col1, col2, col3 = st.columns(3)

with col1:
    f_before = st.text_input("Fluorescence BEFORE calcium", value="", placeholder="e.g., 150")

with col2:
    f_after = st.text_input("Fluorescence AFTER calcium", value="", placeholder="e.g., 180")

with col3:
    total_calcium_added = st.text_input("Total calcium added (µM)", value="5.0", placeholder="e.g., 5.0")

# ============================================================================
# STEP 3: KD ITERATION
# ============================================================================

st.markdown("## 🎯 Step 3: Kd Iteration")

col1, col2 = st.columns(2)

with col1:
    kd_guess = st.text_input("Kd guess (µM)", value="30", placeholder="e.g., 30")

with col2:
    expected_diff = st.text_input("Expected calcium difference (µM)", value="5.0", placeholder="e.g., 5.0")

# ============================================================================
# CALCULATE BUTTON (KD ITERATION)
# ============================================================================

st.markdown("---")

if st.button("🔬 Calculate Calcium Levels", type="primary"):
    inputs = {
        "Fmin": fmin, "Fmax": fmax, "Protein concentration (mg/mL)": protein_level,
        "Fluorescence BEFORE calcium": f_before, "Fluorescence AFTER calcium": f_after,
        "Total calcium added": total_calcium_added, "Kd guess": kd_guess,
        "Expected difference": expected_diff
    }

    is_valid, errors, validated = validate_all_inputs(inputs)

    if not is_valid:
        st.markdown("""
        <div style='background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 1rem; margin-top: 1rem;'>
            <h4 style='color: #721c24;'>❌ Validation Errors:</h4>
        """, unsafe_allow_html=True)
        for error in errors:
            st.markdown(f"- {error}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        Fmin = validated["Fmin"]
        Fmax = validated["Fmax"]
        F_before = validated["Fluorescence BEFORE calcium"]
        F_after = validated["Fluorescence AFTER calcium"]
        Ca_added = validated["Total calcium added"]
        Kd = validated["Kd guess"]
        Expected = validated["Expected difference"]

        calcium_before = fluorescence_to_calcium(F_before, Fmin, Fmax, Kd)
        calcium_after = fluorescence_to_calcium(F_after, Fmin, Fmax, Kd)
        diff_calcium = calcium_after - calcium_before if calcium_before and calcium_after else None

        st.markdown("""
        <div class="result-box">
        <h3>🎯 Results</h3>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Calcium BEFORE", f"{calcium_before:.4f} µM" if calcium_before else "Error")
            st.metric("Calcium AFTER", f"{calcium_after:.4f} µM" if calcium_after else "Error")
        with col2:
            st.metric("Fluorescence Difference", f"{F_after - F_before:.4f}")
            st.metric("Calcium Difference", f"{diff_calcium:.4f} µM" if diff_calcium else "Error")
        with col3:
            st.metric("Expected Difference", f"{Expected:.4f} µM")
            st.metric("Calcium Added", f"{Ca_added:.4f} µM")

        if diff_calcium and Expected:
            if abs(diff_calcium - Expected) <= 0.1:
                st.markdown(f"""
                <div class="success-box">
                <h4 style='color: #0f5132;'>✅ Kd is CORRECT! Kd = {Kd:.2f} µM</h4>
                </div>
                """, unsafe_allow_html=True)
            else:
                suggested_kd = Kd * (Expected / diff_calcium) if diff_calcium != 0 else Kd
                st.markdown(f"""
                <div class="warning-box">
                <h4 style='color: #856404;'>⚠️ Kd needs adjustment</h4>
                <p>Current Kd: {Kd:.2f} µM → Suggested: {suggested_kd:.2f} µM</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# EXPORT & REGRESSION SECTION
# ============================================================================

st.markdown("---")
st.markdown("## 💾 Export Results & Linear Regression")

st.markdown("""
<div class="info-box">
<p><strong>Upload time series data:</strong> Calculate calcium for each time point, then select data range for linear regression.</p>
<p><strong>Slope interpretation:</strong> Rate of calcium change over time (∆Ca²⁺ / ∆time)</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload time series data",
    type=['csv', 'xlsx', 'xls', 'xlsm'],
    help="Upload a file with Time and Fluorescence columns"
)

if uploaded_file:
    # Read original file
    df_original = read_excel_file(uploaded_file)
    df_original = clean_column_names(df_original)
    original_columns = list(df_original.columns)

    st.success(f"✅ File loaded: {len(df_original)} rows")
    st.dataframe(display_dataframe_safely(df_original), width='stretch')

    if len(df_original.columns) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            time_col = st.selectbox("Select Time column", options=original_columns, index=0)

        with col2:
            fluo_col = st.selectbox("Select Fluorescence column", options=original_columns,
                                    index=1 if len(original_columns) > 1 else 0)

        st.markdown("### Calculation Parameters")
        col1, col2, col3 = st.columns(3)

        with col1:
            export_fmin = st.text_input("Fmin", value=fmin)
        with col2:
            export_fmax = st.text_input("Fmax", value=fmax)
        with col3:
            export_kd = st.text_input("Kd (corrected)", value=kd_guess)

        if st.button("Calculate Calcium for Time Series"):
            inputs_export = {"Fmin": export_fmin, "Fmax": export_fmax, "Kd": export_kd}
            is_valid_exp, errors_exp, validated_exp = validate_all_inputs(inputs_export)

            if not is_valid_exp:
                st.error("Please fill all parameters with valid numbers.")
            else:
                Fmin_exp = validated_exp["Fmin"]
                Fmax_exp = validated_exp["Fmax"]
                Kd_exp = validated_exp["Kd"]

                df_export = pd.DataFrame()
                df_export['Time'] = df_original[time_col].values
                df_export['Fluorescence'] = df_original[fluo_col].values
                df_export['Calcium_UM'] = df_original[fluo_col].apply(
                    lambda x: fluorescence_to_calcium(x, Fmin_exp, Fmax_exp, Kd_exp)
                )

                st.session_state.df_export = df_export
                st.session_state.calculation_done = True
                st.session_state.regression_data = None

# ============================================================================
# REGRESSION SECTION (EXECUTED ALWAYS WHEN DATA IS AVAILABLE)
# ============================================================================

if st.session_state.df_export is not None and st.session_state.calculation_done:
    df_export = st.session_state.df_export

    st.markdown("---")
    st.markdown("## 📊 Calculated Data")
    st.dataframe(display_dataframe_safely(df_export), width='stretch')

    st.markdown("---")
    st.markdown("## 📈 Linear Regression: Time vs Calcium")

    # Clean data for regression
    df_clean = df_export.dropna(subset=['Time', 'Calcium_UM'])
    df_clean = df_clean[np.isfinite(df_clean['Calcium_UM'])]

    if len(df_clean) < 3:
        st.warning("Need at least 3 valid data points for regression.")
    else:
        st.session_state.regression_data = df_clean

        # Slider for range selection
        min_idx = 0
        max_idx = len(df_clean) - 1

        st.markdown("""
        <div class="info-box">
        <p><strong>Select data range for linear regression:</strong></p>
        <p>Use the slider to select a subset of data points. The regression will be calculated on the selected range.</p>
        </div>
        """, unsafe_allow_html=True)

        range_selection = st.slider(
            "Select data range (row indices)",
            min_value=0,
            max_value=len(df_clean) - 1,
            value=(0, len(df_clean) - 1),
            step=1,
            key="regression_slider"
        )

        start_idx, end_idx = range_selection

        time_selected = df_clean['Time'].iloc[start_idx:end_idx + 1]
        calcium_selected = df_clean['Calcium_UM'].iloc[start_idx:end_idx + 1]

        slope, intercept, r_squared = linear_regression_slope(time_selected, calcium_selected)

        if slope is not None:
            st.markdown("""
            <div class="regression-box">
            <h4>📊 Linear Regression Results</h4>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📈 Slope (∆Ca²⁺/∆time)", f"{slope:.4f} µM/unit time")
            with col2:
                st.metric("📉 Intercept", f"{intercept:.4f} µM")
            with col3:
                st.metric("📊 R²", f"{r_squared:.4f}")

            st.markdown(f"""
            <p><strong>Selected range:</strong> {start_idx} to {end_idx} ({len(time_selected)} points)</p>
            <p><strong>Equation:</strong> Calcium = {slope:.4f} × Time + {intercept:.4f}</p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Plot
            fig, ax = plt.subplots(figsize=(10, 6))

            ax.plot(df_clean['Time'], df_clean['Calcium_UM'],
                    'o', color='lightgray', alpha=0.5, label='All data')

            ax.plot(time_selected, calcium_selected,
                    'o', color='#1f77b4', label='Selected data', markersize=8)

            x_range = np.linspace(min(time_selected), max(time_selected), 100)
            y_range = slope * x_range + intercept
            ax.plot(x_range, y_range, 'r-', linewidth=2, label=f'Regression (R²={r_squared:.3f})')

            ax.set_xlabel('Time')
            ax.set_ylabel('Calcium (µM)')
            ax.set_title('Calcium vs Time - Linear Regression')
            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

    # ========================================================================
    # DOWNLOAD SECTION
    # ========================================================================

    st.markdown("---")
    st.markdown("### 💾 Download Data")

    col1, col2 = st.columns(2)

    with col1:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.df_export.to_excel(writer, index=False, sheet_name='Calcium Data')
        excel_data = output.getvalue()

        st.download_button(
            label="📥 Download Excel (.xlsx)",
            data=excel_data,
            file_name=f"calcium_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        csv = st.session_state.df_export.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"calcium_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;'>
    <p>🧪 <strong>Mitochondrial Calcium Efflux Calculator - Fluorescence Analysis</strong></p>
    <p>📌 Iterate Kd until calcium difference matches expected value</p>
    <p>🔗 <a href='https://github.com/seuuser/calcium-calculator' target='_blank'>View source code on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
