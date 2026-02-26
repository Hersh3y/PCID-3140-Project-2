import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the dataset (Ensure your file is named exactly this in your folder)
df = pd.read_excel('P2_Types of computers and internet subscriptions.xlsx')

# Identify the state columns
states = [col for col in df.columns if not col.startswith('Unnamed') and col not in ['Individual State', 'Puerto Rico', 'Totals and Percentages ']]

data = []
for state in states:
    state_idx = df.columns.get_loc(state)
    
    # Helper function to grab the PRE-CALCULATED PERCENTAGE directly from the dataset
    # In the Census dataset, the "Percent Estimate" column is exactly 2 columns to the right of the state name
    def get_pct(row_idx):
        val = df.iloc[row_idx, state_idx + 2]
        if pd.isna(val): return 0
        if isinstance(val, str):
            val = val.replace('%', '').replace(',', '').replace('+', '').replace('-', '')
            if val.strip() in ['', '(X)', 'N']: return 0
            return float(val)
        return float(val)

    # Extract specific percentages directly from the dataset rows
    desktop_laptop_pct = get_pct(5)
    smartphone_pct = get_pct(7)
    broadband_pct = get_pct(20)
    satellite_pct = get_pct(21)
    
    # Broadband user percentages within each income bracket
    income_under_20k_bb_pct = get_pct(26)
    income_20k_to_75k_bb_pct = get_pct(30)
    income_75k_bb_pct = get_pct(34)
    
    data.append({
        'State': state,
        'Desktop_Laptop_Pct': desktop_laptop_pct,
        'Smartphone_Pct': smartphone_pct,
        'Broadband_Pct': broadband_pct,
        'Satellite_Pct': satellite_pct,
        'Urbanization_Gap_Pct': broadband_pct - satellite_pct, # Difference in percentage points
        'Income_Under20k_BB_Pct': income_under_20k_bb_pct,
        'Income_20k-75k_BB_Pct': income_20k_to_75k_bb_pct,
        'Income_75k+_BB_Pct': income_75k_bb_pct,
    })

# Convert to DataFrame
df_metrics = pd.DataFrame(data)

# Identify all columns except 'State' and convert only those to numeric
numeric_cols = [col for col in df_metrics.columns if col != 'State']
df_metrics[numeric_cols] = df_metrics[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Identify Top 5 States based on highest percentage gap between broadband and satellite
top_5_states = df_metrics.sort_values('Urbanization_Gap_Pct', ascending=False).head(5)
states_labels = top_5_states['State'].tolist()


# --- VISUAL 1 ---
# Set up the positions for the bars
x = np.arange(len(states_labels))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))

# Plot each income bracket 
ax.bar(x - width, top_5_states['Income_Under20k_BB_Pct'], width, label='Under $20k', color='#5da5da')
ax.bar(x, top_5_states['Income_20k-75k_BB_Pct'], width, label='$20k - $74.9k', color='#faa43a')
ax.bar(x + width, top_5_states['Income_75k+_BB_Pct'], width, label='$75k or more', color='#60bd68')

# Formatting the chart
ax.set_ylabel('Broadband Adoption Rate within Bracket (%)')
ax.set_title('Broadband Adoption Rate Across Income Brackets (Top 5 States)')
ax.set_xticks(x)
ax.set_xticklabels(states_labels)
ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig('visual1_income_broadband.png')
plt.show()


# --- VISUAL 2 ---
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Smartphone vs Desktop/Laptop
ax.bar(x - width/2, top_5_states['Smartphone_Pct'], width, label='Smartphone', color='#4d4d4d')
ax.bar(x + width/2, top_5_states['Desktop_Laptop_Pct'], width, label='Desktop/Laptop', color='#5da5da')

# Formatting the chart
ax.set_ylabel('Percentage of Total State Households (%)')
ax.set_title('Device Ownership Comparison (Top 5 States)')
ax.set_xticks(x)
ax.set_xticklabels(states_labels)
ax.legend(loc='lower right') 

plt.tight_layout()
plt.savefig('visual2_device_ownership.png')
plt.show()


# --- VISUAL 3 ---
width = 0.35
fig, ax = plt.subplots(figsize=(12, 6))

# Plot Broadband vs Satellite
ax.bar(x - width/2, top_5_states['Broadband_Pct'], width, label='Broadband', color='steelblue')
ax.bar(x + width/2, top_5_states['Satellite_Pct'], width, label='Satellite', color='darkorange')

# Formatting the chart
ax.set_ylabel('Percentage of Total State Households (%)')
ax.set_title('Top 5 States with Largest Gap between Broadband and Satellite')
ax.set_xticks(x)
ax.set_xticklabels(states_labels, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.savefig('visual3_urbanization_gap_clustered.png')
plt.show()