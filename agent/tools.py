from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()

@tool
def get_user_order_history(user:str) -> dict:
    """
    This tool takes user's name and return the user's purchase history if user exists.
    """
    logging.info(f"Using get_user_order_history tool on user: {user}")
    if users_data.get(user):
        return users_data[user]
    return {"status": "There was no username found"} 

@tool
def calculate_right_refund_amount(user:str,items:list[PurchaseItem]) -> float:
    """
    This tool takes user's name and a list of returned items and return the total refund amount for the items if user exists.
    """
    logging.info(f"Using calculate_right_refund_amount tool on user: {user} to get user refund amount")
    if not users_data.get(user):
        return {"status": "There was no username found"}
    else: 
        user_data = users_data[user]
        total_refund = 0
        for item in items:
            if user_data.get(item.name):
                item_name = item.name
                item_price = user_data.get(item_name).get("price")
                item_purchase_date = date.fromisoformat(user_data.get(item_name).get("purchase_date"))
                current_date = date.today()
                days_since_purchase = (current_date - item_purchase_date).days
            
                if days_since_purchase <= 30:
                    total_refund += item_price
        return total_refund

@tool
def issue_refund_ticket(user:str,refund_amount:float) -> str:
    """
    This tool takes user's name and the refund amount and send a refund ticket to the right team
    """
    logging.info(f"Using issue_refund_ticket tool on user: {user} to issue refund ticket with amount: ${refund_amount}")
    if not users_data.get(user):
        return {"status": "There was no username found"}
    else:
        return f"Refund ticket for {user} has been issued successfully for the amount of ${refund_amount}"

@tool
def check_today_date(user:str) -> str:
    """
    This tool returns the current date in YYYY-MM-DD format
    """
    if user not in users_data:
        return {"status": "There was no username found"}
    logging.info("Using check_today_date tool to get current date")
    return date.today().isoformat()

book = PurchaseItem(name="book")
pen = PurchaseItem(name="pen")

##  Invoke function takes input as dictionary and returns the output of the function
print(calculate_right_refund_amount.invoke({"user": "user123", "items": [book, pen]}))
print(check_today_date.invoke({"user": "user123"}))
print(issue_refund_ticket.invoke({"user": "user123", "refund_amount": 30.0}))

