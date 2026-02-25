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
    def get_val(row_idx):
        val = df.iloc[row_idx, state_idx]
        if pd.isna(val): return 0
        if isinstance(val, str):
            val = val.replace(',', '').replace('+', '').replace('-', '')
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
    })

# Convert to DataFrame
df_metrics = pd.DataFrame(data)

# Identify all columns except 'State' and convert only those to numeric
numeric_cols = [col for col in df_metrics.columns if col != 'State']
df_metrics[numeric_cols] = df_metrics[numeric_cols].apply(pd.to_numeric, errors='coerce')

# 3. Identify Top 5 States by Urbanization Gap/Size
top_5_states = df_metrics.sort_values('Urbanization_Gap', ascending=False).head(5)
states_labels = top_5_states['State'].tolist()


# Set up the positions for the bars
x = np.arange(len(states_labels))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))

# Plot each income bracket
ax.bar(x - width, top_5_states['Income_Under20k_BB'] / 1_000_000, width, label='Under $20k', color='#5da5da')
ax.bar(x, top_5_states['Income_20k-75k_BB'] / 1_000_000, width, label='$20k - $74.9k', color='#faa43a')
ax.bar(x + width, top_5_states['Income_75k+_BB'] / 1_000_000, width, label='$75k or more', color='#60bd68')

# Formatting the chart
ax.set_ylabel('Households with Broadband Estimate (in millions)')
ax.set_title('Broadband Usage Across Income Brackets (Top 5 States)')
ax.set_xticks(x)
ax.set_xticklabels(states_labels)
ax.ticklabel_format(style='plain', axis='y') # Disable scientific notation on y-axis
ax.legend()

plt.tight_layout()
plt.savefig('visual1_income_broadband.png')
plt.show()


width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Smartphone vs Desktop/Laptop
ax.bar(x - width/2, top_5_states['Smartphone'] / 1_000_000, width, label='Smartphone', color='#4d4d4d')
ax.bar(x + width/2, top_5_states['Desktop_Laptop'] / 1_000_000, width, label='Desktop/Laptop', color='#5da5da')

# Formatting the chart
ax.set_ylabel('Number of Households Owning Device (in millions)')
ax.set_title('Device Ownership Comparison (Top 5 States)')
ax.set_xticks(x)
ax.set_xticklabels(states_labels)
ax.ticklabel_format(style='plain', axis='y') # Disable scientific notation on y-axis
ax.legend()

plt.tight_layout()
plt.savefig('visual2_device_ownership.png')
plt.show()


# Identify the top 5 states based on the gap between Broadband and Satellite
# We can just reuse top_5_states here!
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))

# Plot Broadband vs Satellite
ax.bar(x - width/2, top_5_states['Broadband'] / 1_000_000, width, label='Broadband', color='steelblue')
ax.bar(x + width/2, top_5_states['Satellite'] / 1_000_000, width, label='Satellite', color='darkorange')

# Formatting the chart
ax.set_ylabel('Number of Households (in millions)')
ax.set_title('Top 5 States with the Largest Gap between Broadband and Satellite')
ax.set_xticks(x)
ax.set_xticklabels(states_labels, rotation=45, ha='right')
ax.ticklabel_format(style='plain', axis='y') # Disable scientific notation on y-axis
ax.legend()

plt.tight_layout()
plt.savefig('visual3_urbanization_gap_clustered.png')
plt.show()