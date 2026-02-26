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
    # Row 20 corresponds to 'Broadband such as cable, fiber optic or DSL'
    # Row 21 corresponds to 'Satellite Internet service'
    optic_dsl_pct = get_pct(20)
    satellite_pct = get_pct(21)
    
    data.append({
        'State': state,
        'Optic_DSL_Pct': optic_dsl_pct,
        'Satellite_Pct': satellite_pct,
        'Gap_Pct': optic_dsl_pct - satellite_pct # Difference in percentage points
    })

# Convert to DataFrame
df_metrics = pd.DataFrame(data)

# Identify all columns except 'State' and convert only those to numeric
numeric_cols = [col for col in df_metrics.columns if col != 'State']
df_metrics[numeric_cols] = df_metrics[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Identify Top 5 States based on highest percentage gap between Optic/DSL and Satellite
top_5_states = df_metrics.sort_values('Gap_Pct', ascending=False).head(5)
states_labels = top_5_states['State'].tolist()


# --- VISUAL 3 ---
# Set up the positions for the bars
x = np.arange(len(states_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

# Plot Optic/DSL vs Satellite
ax.bar(x - width/2, top_5_states['Optic_DSL_Pct'], width, label='Broadband (Optic/DSL)', color='steelblue')
ax.bar(x + width/2, top_5_states['Satellite_Pct'], width, label='Satellite', color='darkorange')

# Formatting the chart
ax.set_ylabel('Percentage of Total State Households (%)')
ax.set_title('Top 5 States with Largest Gap between Optic/DSL and Satellite')
ax.set_xticks(x)
ax.set_xticklabels(states_labels, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.savefig('visual3_urbanization_gap_clustered.png')
plt.show()