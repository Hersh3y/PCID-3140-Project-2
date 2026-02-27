import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the excel dataset
df = pd.read_excel('P2_Types of computers and internet subscriptions.xlsx')

# Identify the state columns (skip 'Individual State', 'Unnamed' columns, 'Puerto Rico', and 'Totals')
states = [col for col in df.columns if not col.startswith('Unnamed') and col not in ['Individual State', 'Puerto Rico', 'Totals and Percentages ']]

data = []
for state in states:
    state_idx = df.columns.get_loc(state)
    
    # Helper function to clean and convert string numbers to floats
    # col_offset retrieves values or percentages adjacent to the totals
    def get_val(row_idx, col_offset=0):
        val = df.iloc[row_idx, state_idx + col_offset]
        if pd.isna(val): return 0
        if isinstance(val, str):
            val = val.replace(',', '').replace('+', '').replace('-', '').replace('%', '')
            if val.strip() in ['', '(X)', 'N']: return 0
            return float(val)
        return float(val)

    # Extract data for Visual 1 (Broadband & Income)
    income_under_20k_bb = get_val(26)
    income_20k_to_75k_bb = get_val(30)
    income_75k_bb = get_val(34)
    income_75k_bb_pct = get_val(34, 2)  # Percentage estimate is 2 columns over
    
    # Extract data for Visual 2 (Device Ownership Percentages)
    desktop_laptop_pct = get_val(5, 2)
    smartphone_pct = get_val(7, 2)
    
    # Extract data for Visual 3 (Optic/DSL vs Satellite)
    optic_dsl = get_val(20)
    satellite = get_val(21)
    
    data.append({
        'State': state,
        'Income_Under20k_BB': income_under_20k_bb,
        'Income_20k-75k_BB': income_20k_to_75k_bb,
        'Income_75k+_BB': income_75k_bb,
        'Income_75k+_BB_Pct': income_75k_bb_pct,
        'Desktop_Laptop_Pct': desktop_laptop_pct,
        'Smartphone_Pct': smartphone_pct,
        'Optic_DSL': optic_dsl,
        'Satellite': satellite,
        'Optic_Satellite_Gap': optic_dsl - satellite  # Calculate the Total Gap
    })

# Convert to DataFrame
df_metrics = pd.DataFrame(data)

# Convert all metrics columns to numeric
numeric_cols = [col for col in df_metrics.columns if col != 'State']
df_metrics[numeric_cols] = df_metrics[numeric_cols].apply(pd.to_numeric, errors='coerce')


# ==========================================
# --- VISUAL 1: Broadband by Income Gap ---
# ==========================================

# Pick Top 5 States by broadband usage PERCENTAGE for those who earn $75k or higher
top_5_states_graph1 = df_metrics.sort_values('Income_75k+_BB_Pct', ascending=False).head(5)

# Add the percentage to the state labels
states_labels_1 = [
    f"{state} ({pct}%)" 
    for state, pct in zip(top_5_states_graph1['State'], top_5_states_graph1['Income_75k+_BB_Pct'])
]

x1 = np.arange(len(states_labels_1))
width1 = 0.25

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(x1 - width1, top_5_states_graph1['Income_Under20k_BB'] / 1_000_000, width1, label='Under $20k', color='#5da5da')
ax1.bar(x1, top_5_states_graph1['Income_20k-75k_BB'] / 1_000_000, width1, label='$20k - $74.9k', color='#faa43a')
ax1.bar(x1 + width1, top_5_states_graph1['Income_75k+_BB'] / 1_000_000, width1, label='$75k or more', color='#60bd68')

ax1.set_ylabel('Households with Broadband Estimate (in millions)')
ax1.set_title('Broadband Usage Across Income Brackets\n(Top 5 States ordered by Broadband % for $75k+)')
ax1.set_xticks(x1)
ax1.set_xticklabels(states_labels_1)
ax1.ticklabel_format(style='plain', axis='y')
ax1.legend()
plt.tight_layout()
plt.savefig('visual1_income_broadband.png')
plt.show()


# ==========================================
# --- VISUAL 2: Device Ownership Comparison ---
# ==========================================

# Identify Top 5 States based on highest percentage of Desktop/Laptop ownership
top_5_states_graph2 = df_metrics.sort_values('Desktop_Laptop_Pct', ascending=False).head(5)
states_labels_2 = top_5_states_graph2['State'].tolist()

x2 = np.arange(len(states_labels_2))
width2 = 0.35

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(x2 - width2/2, top_5_states_graph2['Smartphone_Pct'], width2, label='Smartphone', color='#4d4d4d')
ax2.bar(x2 + width2/2, top_5_states_graph2['Desktop_Laptop_Pct'], width2, label='Desktop/Laptop', color='#5da5da')

ax2.set_ylabel('Percentage of Total State Households (%)')
ax2.set_title('Device Ownership (Top 5 States ordered by Desktop/Laptop %)')
ax2.set_xticks(x2)
ax2.set_xticklabels(states_labels_2)

# Zoom in on the top 25% of the chart
ax2.set_ylim(75, 100)

ax2.legend(loc='upper right') 
plt.tight_layout()
plt.savefig('visual2_device_ownership.png')
plt.show()


# ==========================================
# --- VISUAL 3: Optic/DSL vs Satellite Gap ---
# ==========================================

# 1. Gather all states that showed up in Visual 1 and Visual 2
v1_states = top_5_states_graph1['State'].tolist()
v2_states = top_5_states_graph2['State'].tolist()
combined_states = list(set(v1_states + v2_states))  # `set()` removes duplicates

# 2. Filter dataset to ONLY include states that appeared in the prior two visual lists
df_v3_candidates = df_metrics[df_metrics['State'].isin(combined_states)]

# 3. Sort by highest total gap between optic/DSL and satellite, keeping top 5
top_5_states_graph3 = df_v3_candidates.sort_values('Optic_Satellite_Gap', ascending=False).head(5)
states_labels_3 = top_5_states_graph3['State'].tolist()

x3 = np.arange(len(states_labels_3))
width3 = 0.35

fig3, ax3 = plt.subplots(figsize=(10, 6))

# Dividing by 1_000_000 to display in millions (to stay consistent with Visual 1)
ax3.bar(x3 - width3/2, top_5_states_graph3['Optic_DSL'] / 1_000_000, width3, label='Optic/DSL', color='#4d4d4d')
ax3.bar(x3 + width3/2, top_5_states_graph3['Satellite'] / 1_000_000, width3, label='Satellite', color='#faa43a')

# Formatting the chart
ax3.set_ylabel('Households (in millions)')
ax3.set_title('Optic/DSL vs Satellite Internet Users\n(Top 5 states from previous charts, ordered by highest gap)')
ax3.set_xticks(x3)
ax3.set_xticklabels(states_labels_3)
ax3.ticklabel_format(style='plain', axis='y')
ax3.legend()

plt.tight_layout()
plt.savefig('visual3_optic_satellite_gap.png')
plt.show()
