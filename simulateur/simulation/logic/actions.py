from typing import List, Dict
from datetime import datetime

def create_generic_action(type: str, payload: Dict = None) -> Dict:
    """Create a generic Redux action."""
    action = {'type': type}
    if payload:
        action['payload'] = payload
    return action

def update_stock(stock_name: str, stock: Dict) -> Dict:
    """Create an action to update a single stock."""
    return create_generic_action('UPDATE_STOCK', {'stockName': stock_name, 'stock': stock})

def update_stocks(updates: List[Dict]) -> Dict:
    """Create an action to update multiple stocks."""
    return create_generic_action('UPDATE_STOCKS', {'updates': updates})

def change_stock_quantity(name: str, amount: int) -> Dict:
    """Create an action to change the quantity of a stock."""
    return create_generic_action('CHANGE_STOCK_QUANTITY', {'name': name, 'amount': amount})

def buy_or_sell_stock(stock_name: str, amount: int) -> Dict:
    """Create an action to buy or sell a stock."""
    return create_generic_action('BUY_OR_SELL_STOCKS', {'stockName': stock_name, 'amount': amount})

def add_stocks(stocks: List[Dict]) -> Dict:
    """Create an action to add new stocks."""
    return create_generic_action('ADD_STOCKS', {'stocks': stocks})

def add_news(news_items: List[Dict]) -> Dict:
    """Create an action to add news items."""
    return create_generic_action('ADD_NEWS', {'news': news_items})
