# visual1.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the excel dataset
df = pd.read_excel('P2_Types of computers and internet subscriptions.xlsx')

# Identify the state columns (skip 'Individual State', 'Unnamed' columns, and 'Puerto Rico')
states = [col for col in df.columns if not col.startswith('Unnamed') and col not in ['Individual State', 'Puerto Rico']]

data = []
for state in states:
    state_idx = df.columns.get_loc(state)
    
    # Helper function to clean and convert string numbers to floats
    # ADDED: col_offset to retrieve percentage estimates next to the totals
    def get_val(row_idx, col_offset=0):
        val = df.iloc[row_idx, state_idx + col_offset]
        if pd.isna(val): return 0
        if isinstance(val, str):
            val = val.replace(',', '').replace('+', '').replace('-', '').replace('%', '')
            if val.strip() in ['', '(X)', 'N']: return 0
            return float(val)
        return float(val)

    # Extract specific rows based on the labels in the dataset
    desktop_laptop = get_val(5)
    smartphone = get_val(7)
    broadband = get_val(20)
    satellite = get_val(21)
    
    income_under_20k_bb = get_val(26)
    income_20k_to_75k_bb = get_val(30)
    income_75k_bb = get_val(34)
    income_75k_bb_pct = get_val(34, 2)  # Percentage estimate is 2 columns over from the total
    
    data.append({
        'State': state,
        'Desktop_Laptop': desktop_laptop,
        'Smartphone': smartphone,
        'Broadband': broadband,
        'Satellite': satellite,
        'Urbanization_Gap': broadband - satellite,
        'Income_Under20k_BB': income_under_20k_bb,
        'Income_20k-75k_BB': income_20k_to_75k_bb,
        'Income_75k+_BB': income_75k_bb,
        'Income_75k+_BB_Pct': income_75k_bb_pct,
    })

# Convert to DataFrame
df_metrics = pd.DataFrame(data)

# Identify all columns except 'State' and convert only those to numeric
numeric_cols = [col for col in df_metrics.columns if col != 'State']
df_metrics[numeric_cols] = df_metrics[numeric_cols].apply(pd.to_numeric, errors='coerce')


# --- Graph 1 (MODIFIED LOGIC) ---
# Pick Top 5 States by broadband usage PERCENTAGE for those who earn $75k or higher
top_5_states_graph1 = df_metrics.sort_values('Income_75k+_BB_Pct', ascending=False).head(5)

# Add the percentage to the state labels
states_labels_1 = [
    f"{state} ({pct}%)" 
    for state, pct in zip(top_5_states_graph1['State'], top_5_states_graph1['Income_75k+_BB_Pct'])
]

# Set up the positions for the bars
x1 = np.arange(len(states_labels_1))
width = 0.25

fig1, ax1 = plt.subplots(figsize=(10, 6))

# Plot each income bracket using the new sorted dataframe
ax1.bar(x1 - width, top_5_states_graph1['Income_Under20k_BB'] / 1_000_000, width, label='Under $20k', color='#5da5da')
ax1.bar(x1, top_5_states_graph1['Income_20k-75k_BB'] / 1_000_000, width, label='$20k - $74.9k', color='#faa43a')
ax1.bar(x1 + width, top_5_states_graph1['Income_75k+_BB'] / 1_000_000, width, label='$75k or more', color='#60bd68')

# Formatting the chart
ax1.set_ylabel('Households with Broadband Estimate (in millions)')
ax1.set_title('Broadband Usage Across Income Brackets\n(Top 5 States by Broadband % for $75k+)')
ax1.set_xticks(x1)
ax1.set_xticklabels(states_labels_1)
ax1.ticklabel_format(style='plain', axis='y') # Disable scientific notation on y-axis
ax1.legend()

plt.tight_layout()
plt.savefig('visual1_income_broadband.png')
plt.show()
