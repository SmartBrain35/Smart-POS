from sqlalchemy.orm import Session
from models import StockItem
from datetime import datetime

class StockController:
    def __init__(self, db: Session):
        self.db = db

    # ---------------- Add a new stock item ----------------
    def add_item(self, name: str, unit_type: str, category: str,
                 cost_price: float, selling_price: float,
                 quantity: int = 0, min_quantity: int = 0):
        item = StockItem(
            name=name.strip(),
            unit_type=unit_type.strip(),
            category=category.lower(),
            cost_price=cost_price,
            selling_price=selling_price,
            quantity=quantity,
            min_quantity=min_quantity,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------- Update an existing item ----------------
    def update_item(self, item_id: int, **kwargs):
        item = self.db.query(StockItem).filter(StockItem.id == item_id).first()
        if not item:
            return None

        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------- Delete a stock item ----------------
    def delete_stock(self, stock_id):
        stock_item = self.db.query(StockItem).get(stock_id)
        if stock_item:
            self.db.delete(stock_item)
            self.db.commit()
            return True
        return False

    # ---------------- Fetch item by ID ----------------
    def get_item(self, item_id: int):
        return self.db.query(StockItem).filter(StockItem.id == item_id).first()

    # ---------------- Fetch all items ----------------
    def get_all_items(self, category: str = None, active_only: bool = True):
        query = self.db.query(StockItem)
        if category:
            query = query.filter(StockItem.category == category.lower())
        if active_only:
            query = query.filter(StockItem.is_active == True)
        return query.all()

    # ---------------- Adjust stock quantity ----------------
    def adjust_quantity(self, item_id: int, quantity_change: int):
        item = self.get_item(item_id)
        if not item:
            return None

        item.quantity += quantity_change
        item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------- Deactivate item ----------------
    def deactivate_item(self, item_id: int):
        item = self.get_item(item_id)
        if not item:
            return None
        item.is_active = False
        item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------- Profit calculation ----------------
    def calculate_profit(self, item_id: int, sold_quantity: int):
        item = self.get_item(item_id)
        if not item:
            return 0
        return (item.selling_price - item.cost_price) * sold_quantity
