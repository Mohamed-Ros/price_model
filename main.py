from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProductInput(BaseModel):
    production_date: str  
    expiry_date: str      
    price_fresh: float


def linear_interpolate(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def calculate_discount(days_left: int) -> float:
    if days_left <= 90:  
        return linear_interpolate(days_left, 0, 90, 0.20, 0.18)
    elif days_left <= 150:  
        return linear_interpolate(days_left, 91, 150, 0.12, 0.10)
    elif days_left <= 365: 
        return linear_interpolate(days_left, 151, 365, 0.05, 0.0)
    else:
        return 0.0


@app.post("/predict_price")
def predict_price(data: ProductInput):
    try:
        prod_date = pd.to_datetime(data.production_date)
        exp_date = pd.to_datetime(data.expiry_date)
        current_date = pd.to_datetime(datetime.now().date())

        days_left = max((exp_date - current_date).days, 0)

        discount = calculate_discount(days_left)
        discounted_price = data.price_fresh * (1 - discount)

        months = days_left // 30
        days = days_left % 30

        return {
            "price_fresh": round(data.price_fresh, 2),
            "time_left_until_expiry": f"{months} شهر و {days} يوم",
            "days_left": days_left,
            "discount_applied_percent": round(discount * 100, 2),
            "predicted_price": round(discounted_price, 2),
            "current_date": current_date.strftime("%Y-%m-%d"),
            "production_date": prod_date.strftime("%Y-%m-%d"),
            "expiry_date": exp_date.strftime("%Y-%m-%d"),
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)