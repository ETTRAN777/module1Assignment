import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Data Collection ---

# Data is manually collected for accuracy and consistency.
# Prices are for College Park, MD.
# Nutritional data is from official company websites.

cfa_data = {
    'Restaurant': 'Chick-fil-A',
    'Item Type': ['Sandwich', 'Fries', 'Sweet Tea'],
    'Item Name': ['Chicken Sandwich', 'Waffle Fries (Lg)', 'Sweet Iced Tea (Lg)'],
    'Price': [5.59, 3.09, 2.59],
    'Protein (g)': [29, 7, 0],
    'Total Fat (g)': [17, 35, 0],
    'Sugars (g)': [6, 0, 44]
}
cfa_df = pd.DataFrame(cfa_data)

popeyes_data = {
    'Restaurant': 'Popeyes',
    'Item Type': ['Sandwich', 'Fries', 'Sweet Tea'],
    'Item Name': ['Classic Chicken Sandwich', 'Cajun Fries (Lg)', 'Sweet Iced Tea (Lg)'],
    'Price': [5.99, 4.19, 3.29],
    'Protein (g)': [28, 10, 0],
    'Total Fat (g)': [42, 41, 0],
    'Sugars (g)': [7, 0, 38]
}
popeyes_df = pd.DataFrame(popeyes_data)

# --- 2. Analysis ---

# Combine data into a single DataFrame
full_df = pd.concat([cfa_df, popeyes_df], ignore_index=True)

# Engineer features for each item's specific context
# For Sandwich: Maximize Protein per Dollar
full_df['Value Metric'] = 0.0 # Initialize column
full_df.loc[full_df['Item Type'] == 'Sandwich', 'Value Metric'] = full_df['Protein (g)'] / full_df['Price']

# For Fries: Minimize Fat per Dollar
full_df.loc[full_df['Item Type'] == 'Fries', 'Value Metric'] = full_df['Total Fat (g)'] / full_df['Price']

# For Tea: Minimize Sugar per Dollar
full_df.loc[full_df['Item Type'] == 'Sweet Tea', 'Value Metric'] = full_df['Sugars (g)'] / full_df['Price']


# --- 3. Create Comparison Table ---

print("--- Full Comparison Table ---")
print(full_df.to_markdown(index=False))


# --- 4. Visualization ---

# Create a 1x3 grid of subplots for each item comparison
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Nutritional Value Showdown: Chick-fil-A vs. Popeyes', fontsize=20, weight='bold')

# Plot 1: Sandwich (Protein per Dollar - Higher is Better)
sandwich_data = full_df[full_df['Item Type'] == 'Sandwich']
sns.barplot(ax=axes[0], x='Restaurant', y='Value Metric', data=sandwich_data, palette={'Chick-fil-A': '#DD0031', 'Popeyes': '#FF8200'})
axes[0].set_title('Sandwich: Protein per Dollar\n(Higher is Better)', fontsize=16)
axes[0].set_ylabel('Protein (g) / $', fontsize=12)
axes[0].set_xlabel('')

# Plot 2: Fries (Fat per Dollar - Lower is Better)
fries_data = full_df[full_df['Item Type'] == 'Fries']
sns.barplot(ax=axes[1], x='Restaurant', y='Value Metric', data=fries_data, palette={'Chick-fil-A': '#DD0031', 'Popeyes': '#FF8200'})
axes[1].set_title('Fries: Fat per Dollar\n(Lower is Better)', fontsize=16)
axes[1].set_ylabel('Total Fat (g) / $', fontsize=12)
axes[1].set_xlabel('Restaurant', fontsize=14)

# Plot 3: Sweet Tea (Sugar per Dollar - Lower is Better)
tea_data = full_df[full_df['Item Type'] == 'Sweet Tea']
sns.barplot(ax=axes[2], x='Restaurant', y='Value Metric', data=tea_data, palette={'Chick-fil-A': '#DD0031', 'Popeyes': '#FF8200'})
axes[2].set_title('Sweet Tea: Sugar per Dollar\n(Lower is Better)', fontsize=16)
axes[2].set_ylabel('Sugars (g) / $', fontsize=12)
axes[2].set_xlabel('')

# Add data labels to each bar
for ax in axes:
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                    textcoords='offset points')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('full_nutritional_comparison.png')
print("\nChart saved as 'full_nutritional_comparison.png'")