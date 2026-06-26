pythonimport os
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(
    title="Instant Checkout Monetization Engine", 
    version="1.0.0",
    description="Drop-in micro-upsell component for instant checkout monetization."
)

# Enable global CORS so any online storefront can connect to this microservice securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Transaction Ledger
STORE_FINANCIALS = {
    "total_upsell_revenue": 0.00,
    "transactions_logged": 0
}

class UpsellOrderSchema(BaseModel):
    order_id: str
    base_item_price: float
    upsell_type: str  # "CUSTOM_WRAP", "ANIMATED_CARD", "PREMIUM_SKIN"
    custom_text: str
    design_color: str

@app.post("/api/checkout/upsell")
def process_store_upsell(payload: UpsellOrderSchema):
    """
    Processes the custom add-on at checkout. 
    Appends a clear, immediate micro-premium fee to the customer's cart.
    """
    # Programmatically set the premium fee metrics based on configuration selection
    premium_fee = 2.99
    if payload.upsell_type == "ANIMATED_CARD":
        premium_fee = 4.99
        
    final_total_price = payload.base_item_price + premium_fee
    
    # Instantly credit the store's central financial ledger
    STORE_FINANCIALS["total_upsell_revenue"] += premium_fee
    STORE_FINANCIALS["transactions_logged"] += 1
    
    return {
        "status": "UPSELL_APPLIED",
        "original_item_price": payload.base_item_price,
        "added_premium_fee": premium_fee,
        "new_checkout_total": round(final_total_price, 2),
        "total_store_earnings_to_date": round(STORE_FINANCIALS["total_upsell_revenue"], 2)
    }

@app.get("/api/admin/revenue")
def view_live_earnings():
    """Returns real-time financial tracking metrics for the store owner."""
    return {
        "status": "OPERATIONAL",
        "live_metrics": STORE_FINANCIALS
    }
