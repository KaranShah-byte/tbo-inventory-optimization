import pandas as pd
import numpy as np
import random

# Core parameters
DESTINATIONS = ['Dubai', 'London', 'Singapore', 'New York', 'Paris', 'Bali']
INVENTORY_TYPES = ['Hotel', 'Flight']

def generate_mock_inventory(num_records=500):
    data = []
    
    for i in range(num_records):
        inv_type = random.choice(INVENTORY_TYPES)
        dest = random.choice(DESTINATIONS)
        
        # 1. Pricing and Capacity
        if inv_type == 'Hotel':
            base_cost = round(random.uniform(50, 300), 2)
            capacity = random.randint(10, 50) # Rooms available
        else:
            base_cost = round(random.uniform(200, 1000), 2)
            capacity = random.randint(20, 150) # Seats available
            
        # Markup between 10% and 50%
        selling_price = round(base_cost * random.uniform(1.1, 1.5), 2) 
        
        # 2. Historical Trends & Risk
        # look_to_book_ratio: What percentage of searches convert to bookings?
        look_to_book_ratio = round(random.uniform(0.01, 0.15), 3) 
        
        # cancellation_rate: Historical cancellation probability (5% to 30%)
        cancellation_rate = round(random.uniform(0.05, 0.30), 2) 
        
        # 3. External Signals
        # seasonality_multiplier: 1.0 = normal demand, >1.0 = peak season, <1.0 = off-season
        seasonality_multiplier = round(random.uniform(0.7, 1.6), 2)
        
        # Calculate expected demand based on seasonality and look-to-book
        base_searches = random.randint(1000, 10000)
        projected_demand = int(base_searches * look_to_book_ratio * seasonality_multiplier)
        
        data.append({
            'inventory_id': f"{inv_type[:1].upper()}-{1000+i}",
            'type': inv_type,
            'destination': dest,
            'base_cost': base_cost,
            'selling_price': selling_price,
            'profit_margin': round(selling_price - base_cost, 2),
            'total_capacity': capacity,
            'projected_demand': projected_demand,
            'cancellation_rate': cancellation_rate,
            'seasonality_multiplier': seasonality_multiplier
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Generate 500 rows of mock inventory
    mock_df = generate_mock_inventory(500)
    
    # Save to CSV
    filename = 'tbo_mock_inventory.csv'
    mock_df.to_csv(filename, index=False)
    
    print(f"✅ Successfully generated {len(mock_df)} records and saved to '{filename}'")
    print("\nPreview of the data:")
    print(mock_df.head())



    