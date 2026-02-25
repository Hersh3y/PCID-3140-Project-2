# PCID-3140-Project-2: Internet Subscriptions & Device Ownership Analysis

## Project Overview

This project analyzes household internet subscriptions and device ownership patterns across U.S. states using data from the Census Bureau. The analysis focuses on understanding digital divides by examining broadband penetration, device ownership, income levels, and urbanization gaps.

## Features

The script generates three main visualizations:

1. **Broadband Usage Across Income Brackets** (`visual1_income_broadband.png`)
   - Compares broadband household subscriptions across three income brackets
   - Data for the top 5 states by urbanization gap
   - Shows how internet access varies by income level

2. **Device Ownership Comparison** (`visual2_device_ownership.png`)
   - Compares smartphone vs. desktop/laptop ownership
   - Highlights differences in device preferences across top states
   - Measured in millions of households

3. **Urbanization Gap Analysis** (`visual3_urbanization_gap_clustered.png`)
   - Displays the gap between broadband and satellite internet subscriptions
   - Identifies states with the largest digital divide
   - Shows top 5 states ranked by urbanization gap

## Requirements

- Python
- pandas
- numpy
- matplotlib
- openpyxl (for reading Excel files)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib openpyxl
   ```

## Usage

1. Place the Excel file `P2_Types of computers and internet subscriptions.xlsx` in the project directory

2. Run the analysis:
   ```bash
   python visuals.py
   ```

3. The script will generate three PNG files with the visualizations and display them

## Data Source

The data comes from the Census Bureau dataset on types of computers and internet subscriptions by state.

## Output Files

- `visual1_income_broadband.png` - Income bracket broadband analysis
- `visual2_device_ownership.png` - Device ownership comparison
- `visual3_urbanization_gap_clustered.png` - Urbanization gap analysis

## Project Structure

```
PCID-3140-Project-2/
├── README.md
├── visuals.py
└── P2_Types of computers and internet subscriptions.xlsx
```