# visual2.py

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
    
    data.append({
        'State': state,
        'Desktop_Laptop_Pct': desktop_laptop_pct,
        'Smartphone_Pct': smartphone_pct
    })

# Convert to DataFrame
df_metrics = pd.DataFrame(data)

# Identify all columns except 'State' and convert only those to numeric
numeric_cols = [col for col in df_metrics.columns if col != 'State']
df_metrics[numeric_cols] = df_metrics[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Identify Top 5 States based on highest percentage of Desktop/Laptop ownership
top_5_states = df_metrics.sort_values('Desktop_Laptop_Pct', ascending=False).head(5)
states_labels = top_5_states['State'].tolist()


# --- VISUAL 2: Device Ownership Comparison ---
x = np.arange(len(states_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

# Plot Smartphone vs Desktop/Laptop
ax.bar(x - width/2, top_5_states['Smartphone_Pct'], width, label='Smartphone', color='#4d4d4d')
ax.bar(x + width/2, top_5_states['Desktop_Laptop_Pct'], width, label='Desktop/Laptop', color='#5da5da')

# Formatting the chart
ax.set_ylabel('Percentage of Total State Households (%)')
ax.set_title('Device Ownership Comparison (Top 5 States by Desktop/Laptop Ownership)')
ax.set_xticks(x)
ax.set_xticklabels(states_labels)

# Zoom in on the top 25% of the chart
ax.set_ylim(75, 100)

# Move legend or adjust to avoid overlapping bars 
ax.legend(loc='lower right') 

plt.tight_layout()
plt.savefig('visual2_device_ownership.png')
plt.show()