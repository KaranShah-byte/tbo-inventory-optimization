from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from optimization_engine import optimize_inventory
import pandas as pd

app = FastAPI(title="TBO Inventory Optimization API")

# Enable CORS so the frontend dashboard can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    # This tells FastAPI to serve your dashboard instead of a JSON message
    return FileResponse("index.html")

@app.get("/api/optimize")
def get_optimization(budget: float = 100000):
    """
    Endpoint to calculate optimal inventory allocation for a given budget.
    """
    if budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than zero.")
        
    try:
        # Call the engine we built in Phase 2
        purchases_df, amount_spent, projected_profit = optimize_inventory(budget_limit=budget)
        
        # Convert DataFrame to a list of dictionaries for JSON response
        purchases_list = purchases_df.to_dict(orient='records')
        
        return {
            "status": "success",
            "input_budget": budget,
            "total_spent": amount_spent,
            "expected_profit": projected_profit,
            "portfolio_roi_percentage": round((projected_profit / amount_spent) * 100, 2) if amount_spent > 0 else 0,
            "purchases": purchases_list
        }
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Mock data file not found. Run generate_mock_data.py first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))