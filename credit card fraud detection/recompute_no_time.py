import pandas as pd

df = pd.read_csv('creditcard_cleaned.csv')

def period_of_day(h):
    if 0 <= h <= 5:
        return 'Night (00-05)'
    elif 6 <= h <= 11:
        return 'Morning (06-11)'
    elif 12 <= h <= 17:
        return 'Afternoon (12-17)'
    else:
        return 'Evening (18-23)'

df['Period_of_Day'] = df['Hour_of_Day'].apply(period_of_day)
period_order = ['Night (00-05)', 'Morning (06-11)', 'Afternoon (12-17)', 'Evening (18-23)']
df['Period_of_Day'] = pd.Categorical(df['Period_of_Day'], categories=period_order, ordered=True)

def amount_range(a):
    if a < 10:
        return 'Small (<$10)'
    elif a < 100:
        return 'Medium ($10-$100)'
    elif a < 1000:
        return 'Large ($100-$1,000)'
    else:
        return 'Very Large (>$1,000)'

df['Amount_Range'] = df['Amount'].apply(amount_range)
amount_order = ['Small (<$10)', 'Medium ($10-$100)', 'Large ($100-$1,000)', 'Very Large (>$1,000)']
df['Amount_Range'] = pd.Categorical(df['Amount_Range'], categories=amount_order, ordered=True)

# ---- CUBE: Period_of_Day x Amount_Range, Transaction Count ----
cube_count = pd.pivot_table(df, index='Period_of_Day', columns='Amount_Range',
                             values='Amount', aggfunc='count', observed=True, fill_value=0)
print("CUBE (Transaction Count): Period_of_Day x Amount_Range")
print(cube_count)
print()

# ---- SLICE: Class_Label = 'Fraud' -> Period_of_Day x Amount_Range ----
slice_df = df[df['Class_Label'] == 'Fraud']
slice_result = pd.pivot_table(slice_df, index='Period_of_Day', columns='Amount_Range',
                               values='Amount', aggfunc='count', observed=True, fill_value=0)
print("SLICE: Class_Label = 'Fraud'  |  Period_of_Day x Amount_Range (fraud count)")
print(slice_result)
print()

# ---- DICE: Class_Label = 'Fraud' AND Amount_Range = 'Large ($100-$1,000)' -> by Period_of_Day ----
dice_df = df[(df['Class_Label'] == 'Fraud') & (df['Amount_Range'] == 'Large ($100-$1,000)')]
dice_result = dice_df.groupby('Period_of_Day', observed=True).agg(
    Transaction_Count=('Amount', 'count'),
    Total_Amount=('Amount', 'sum'),
    Avg_Amount=('Amount', 'mean'),
).reset_index()
dice_result['Total_Amount'] = dice_result['Total_Amount'].round(2)
dice_result['Avg_Amount'] = dice_result['Avg_Amount'].round(2)
print("DICE: Class_Label = 'Fraud' AND Amount_Range = 'Large ($100-$1,000)', by Period_of_Day")
print(dice_result)
print()

# ---- DRILL-DOWN: Period_of_Day -> Hour_of_Day, fraud only ----
drill = df[df['Class_Label'] == 'Fraud'].groupby(['Period_of_Day', 'Hour_of_Day'], observed=True).agg(
    Fraud_Count=('Class', 'sum')
).reset_index()
drill = drill[drill['Fraud_Count'] > 0].sort_values(['Period_of_Day', 'Hour_of_Day'])
print("DRILL-DOWN: Fraud count by Hour, within each Period_of_Day")
print(drill.to_string(index=False))
print()

# ---- ROLL-UP: Hour -> Period_of_Day (fraud totals) ----
rollup = df[df['Class_Label'] == 'Fraud'].groupby('Period_of_Day', observed=True).agg(
    Fraud_Count=('Class', 'sum'), Transaction_Count=('Amount', 'count')
).reset_index()
print("ROLL-UP: Fraud count rolled up from Hour to Period_of_Day")
print(rollup)
