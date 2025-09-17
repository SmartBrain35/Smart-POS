import random
from datetime import datetime, timedelta, date
from faker import Faker
from sqlmodel import Session, create_engine
from backend.auth import hash_password

from backend.storage.models import (
    SQLModel, Account, Employee, Stock, Sale, SaleItem,
    Damage, Expenditure, Return,
    UserRole, EmployeeDesignation, PaymentMethod,
    StockType, DamageStatus, ExpenditureCategory, ReturnReason
)

# --- Setup ---
fake = Faker()
engine = create_engine("sqlite:///backend/storage/app.db")


def seed_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # --- Accounts (exclude ADMIN) ---
        accounts = []
        roles = [UserRole.MANAGER, UserRole.CASHIER, UserRole.SALES_PERSON]
        for _ in range(20):
            account = Account(
                name=fake.name(),
                phone=fake.unique.msisdn()[0:10],
                email=fake.unique.email(),
                password=hash_password('password123'),
                role=random.choice(roles),
            )
            accounts.append(account)
            session.add(account)

        session.commit()
        session.refresh(accounts[0])

        # --- Employees ---
        employees = []
        for _ in range(30):
            employee = Employee(
                name=fake.name(),
                phone=fake.unique.msisdn()[0:10],
                ghana_card=fake.unique.uuid4(),
                address=fake.address(),
                hire_date=fake.date_between(start_date="-2y", end_date="today"),
                salary=round(random.uniform(300, 2000), 2),
                designation=random.choice(list(EmployeeDesignation)),
            )
            employees.append(employee)
            session.add(employee)

        # --- Stocks ---
        stocks = []
        for _ in range(50):
            stock = Stock(
                item_name=fake.word().capitalize(),
                quantity=random.randint(10, 200),
                cost_price=round(random.uniform(5, 100), 2),
                selling_price=round(random.uniform(101, 200), 2),
                category=random.choice(list(StockType)),
                expiry_date=fake.date_between(start_date="today", end_date="+1y"),
            )
            stocks.append(stock)
            session.add(stock)

        session.commit()

        # --- Sales ---
        sales = []
        for _ in range(100):
            cashier = random.choice(accounts)
            sale = Sale(
                sale_date=fake.date_between(start_date="-1y", end_date="today"),
                sale_time=datetime.now() - timedelta(days=random.randint(0, 365)),
                discount_amount=round(random.uniform(0, 20), 2),
                amount_paid=round(random.uniform(50, 500), 2),
                change_given=round(random.uniform(0, 50), 2),
                payment_method=random.choice(list(PaymentMethod)),
                cashier_id=cashier.id,
            )
            sales.append(sale)
            session.add(sale)

        session.commit()

        # --- Sale Items ---
        sale_items = []
        for sale in sales:
            for _ in range(random.randint(1, 5)):
                stock = random.choice(stocks)
                item = SaleItem(
                    sale_id=sale.id,
                    stock_id=stock.id,
                    quantity_sold=random.randint(1, 5),
                )
                sale_items.append(item)
                session.add(item)

        # --- Damages ---
        damages = []
        for _ in range(30):
            stock = random.choice(stocks)
            damage = Damage(
                stock_id=stock.id,
                quantity_damaged=random.randint(1, 5),
                damage_status=random.choice(list(DamageStatus)),
                damage_date=fake.date_between(start_date="-6m", end_date="today"),
            )
            damages.append(damage)
            session.add(damage)

        # --- Expenditures ---
        expenditures = []
        for _ in range(40):
            exp = Expenditure(
                description=fake.sentence(nb_words=6),
                amount=round(random.uniform(50, 1000), 2),
                category=random.choice(list(ExpenditureCategory)),
                expense_date=fake.date_between(start_date="-1y", end_date="today"),
            )
            expenditures.append(exp)
            session.add(exp)

        # --- Returns ---
        returns = []
        for _ in range(20):
            sale = random.choice(sales)
            stock = random.choice(stocks)
            ret = Return(
                sale_id=sale.id,
                stock_id=stock.id,
                quantity=random.randint(1, 3),
                reason=random.choice(list(ReturnReason)),
                return_date=fake.date_between(start_date="-6m", end_date="today"),
            )
            returns.append(ret)
            session.add(ret)

        session.commit()

        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed_db()
