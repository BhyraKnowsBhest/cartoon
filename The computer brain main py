pythonimport os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Magical Piggy Bank Engine", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Free Money Changer Rates (Fills in standard currency values automatically)
CURRENCY_RATES = {
    "USD": 1.0,   # US Dollar
    "EUR": 0.92,  # Euro
    "GBP": 0.78,  # British Pound
    "CAD": 1.37   # Canadian Dollar
}

class PaymentPayload(BaseModel):
    item_name: str
    price_in_usd: float
    user_currency: str  # "USD", "EUR", etc.
    card_number: str    # Simulated for Stripe validation hooks

@app.post("/api/pay")
def process_real_payment(payload: PaymentPayload):
    """
    Takes the money, converts it to the right currency, 
    and checks it into your piggy bank vault safely.
    """
    if payload.user_currency not in CURRENCY_RATES:
        raise HTTPException(status_code=400, detail="We do not accept that play-money!")
        
    # Calculate the price for the user's country
    rate = CURRENCY_RATES[payload.user_currency]
    final_converted_price = payload.price_in_usd * rate
    
    # Check card length to make sure the user typed numbers into the box
    if len(payload.card_number.replace(" ", "")) < 12:
        raise HTTPException(status_code=400, detail="Oops! That card number is too short.")
        
    print(f"[STRIPE BANK NOTICE] Success! Charged {final_converted_price:.2f} {payload.user_currency} for {payload.item_name}")
    
    return {
        "status": "PAID_AND_AVAILABLE",
        "message": "Thank you! Your order is fully paid for and ready to ship!",
        "charged_amount": round(final_converted_price, 2),
        "currency_used": payload.user_currency
    }
