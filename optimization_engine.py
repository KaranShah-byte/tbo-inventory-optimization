import pandas as pd
import os

def prepare_real_data(csv_path="hotel_bookings.csv"):
    """
    Transforms transactional hotel booking data into aggregated inventory units.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot find {csv_path}. Make sure it is in your project folder.")

    df = pd.read_csv(csv_path)
    
    # Filter out rows with zero or negative rates
    df = df[df['adr'] > 0].copy()

    # Aggregate history to create unique inventory segments
    inventory_df = df.groupby(['hotel', 'arrival_date_month', 'reserved_room_type']).agg(
        projected_demand=('is_canceled', 'count'),   # Total historical bookings
        cancellation_rate=('is_canceled', 'mean'),   # Actual historical cancellation %
        avg_adr=('adr', 'mean')                      # Average selling price
    ).reset_index()

    # Calculate financial metrics (Assuming a 20% markup from B2B base cost)
    inventory_df['selling_price'] = inventory_df['avg_adr'].round(2)
    inventory_df['base_cost'] = (inventory_df['avg_adr'] * 0.8).round(2) 
    inventory_df['profit_margin'] = (inventory_df['selling_price'] - inventory_df['base_cost']).round(2)
    
    # Assume we can procure slightly more capacity than average historical demand
    inventory_df['total_capacity'] = (inventory_df['projected_demand'] * 1.2).astype(int)

    # Generate a clean ID (e.g., "City Hotel-Apr-RmA")
    inventory_df['inventory_id'] = inventory_df['hotel'] + '-' + inventory_df['arrival_date_month'].str[:3] + '-Rm' + inventory_df['reserved_room_type']
    inventory_df['type'] = 'Hotel'
    inventory_df['destination'] = inventory_df['hotel'] + ' (' + inventory_df['arrival_date_month'] + ')'

    return inventory_df

def optimize_inventory(budget_limit, data_path='hotel_bookings.csv'):
    # 1. Load and prep the REAL dataset
    df = prepare_real_data(data_path)
    
    # 2. Calculate Risk-Adjusted metrics
    # Real expected profit = Margin * Probability of NOT canceling
    df['risk_adjusted_profit'] = df['profit_margin'] * (1 - df['cancellation_rate'])
    
    # Calculate ROI (Expected Profit / Cost) to rank the best investments
    df['roi'] = df['risk_adjusted_profit'] / df['base_cost']
    
    # We shouldn't buy more than the projected demand OR the total capacity
    df['max_units_to_buy'] = df[['total_capacity', 'projected_demand']].min(axis=1)
    
    # 3. Sort inventory by highest ROI first (Greedy Knapsack Algorithm)
    df_sorted = df.sort_values(by='roi', ascending=False)
    
    budget_remaining = budget_limit
    total_expected_profit = 0
    purchases = []
    
    # 4. Allocate Budget
    for index, row in df_sorted.iterrows():
        if budget_remaining <= 0:
            break
            
        cost_per_unit = row['base_cost']
        if cost_per_unit > budget_remaining:
            continue 
            
        affordable_units = int(budget_remaining // cost_per_unit)
        units_to_buy = min(affordable_units, row['max_units_to_buy'])
        
        if units_to_buy > 0:
            total_cost = units_to_buy * cost_per_unit
            expected_gain = units_to_buy * row['risk_adjusted_profit']
            
            budget_remaining -= total_cost
            total_expected_profit += expected_gain
            
            purchases.append({
                'inventory_id': row['inventory_id'],
                'type': row['type'],
                'destination': row['destination'],
                'units_to_buy': units_to_buy,
                'unit_cost': cost_per_unit,
                'total_investment': round(total_cost, 2),
                'expected_profit': round(expected_gain, 2),
                'roi_percentage': round(row['roi'] * 100, 2),
                'real_cancel_rate': f"{round(row['cancellation_rate'] * 100, 1)}%"
            })
            
    return pd.DataFrame(purchases), round(budget_limit - budget_remaining, 2), round(total_expected_profit, 2)

if __name__ == "__main__":
    TEST_BUDGET = 250000 
    purchases_df, amount_spent, projected_profit = optimize_inventory(TEST_BUDGET)
    
    print("✅ Optimization Complete Using REAL Data!")
    print(f"Total Budget Allocated: ${amount_spent:,.2f}")
    print(f"Expected Risk-Adjusted Profit: ${projected_profit:,.2f}")
    print(f"Overall Portfolio ROI: {round((projected_profit/amount_spent)*100, 2)}%")
    print("\n--- Top 5 Recommended Procurements ---")
    print(purchases_df[['inventory_id', 'units_to_buy', 'unit_cost', 'total_investment', 'roi_percentage', 'real_cancel_rate']].head().to_string(index=False))