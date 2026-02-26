# PCID-3140-Project-2: Internet Subscriptions & Device Ownership Analysis

## Project Overview

This project analyzes household internet subscriptions and device ownership patterns across U.S. states using data from the Census Bureau. The analysis focuses on understanding digital divides by examining broadband penetration across income levels, device ownership rates, and the gap between fiber-optic/DSL and satellite internet access.

## Visualizations

The main script (`all_visuals.py`) generates three visualizations:

### 1. Broadband Usage Across Income Brackets (`visual1_income_broadband.png`)

- Compares broadband household subscriptions across three income brackets: under $20k, $20k–$74.9k, and $75k+
- Selects the top 5 states by broadband percentage for the $75k+ bracket
- Displays household counts in millions

### 2. Device Ownership Comparison (`visual2_device_ownership.png`)

- Compares smartphone vs. desktop/laptop ownership as a percentage of total state households
- Selects the top 5 states by desktop/laptop ownership percentage
- Y-axis zoomed to 75–100% to highlight differences

### 3. Optic/DSL vs Satellite Gap (`visual3_optic_satellite_gap.png`)

- Compares fiber-optic/DSL and satellite internet subscriptions
- Filters to states that appeared in Visual 1 or Visual 2, then ranks by the largest gap
- Displays the top 5 states in millions of households

## Requirements

- Python
- pandas
- numpy
- matplotlib
- openpyxl

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install pandas numpy matplotlib openpyxl
```

## Usage

Place `P2_Types of computers and internet subscriptions.xlsx` in the project root, then run:

```bash
python all_visuals.py
```

The script will display each chart and save them as PNG files.

## Data Source

Census Bureau — Types of Computers and Internet Subscriptions by State.

## Project Structure

```
PCID-3140-Project-2/
├── README.md
├── all_visuals.py          # Main script (all three visuals)
├── visual1.py              # Standalone Visual 1
├── visual2.py              # Standalone Visual 2
├── old/                    # Previous script versions
│   ├── visual3.py
│   ├── visuals_v2.py
│   └── visuals.py
└── P2_Types of computers and internet subscriptions.xlsx
```