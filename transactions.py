import random
from products import *

calendar = tuple(range(0, 200))
current_date = 0
planned_transactions = []
past_transactions = []
used_transaction_numbers = []


def new_transaction_number():
    if not used_transaction_numbers:
        production_number = 0
    else:
        production_number = used_transaction_numbers[-1] + 1
    used_transaction_numbers.append(production_number)
    return production_number


class TransactionEvent:
    def __init__(self, date, quantity, target, source):  # [0: date, 1: quantity, 2: target, 3: source]
        self.date_of_transaction = self.is_valid_date(date)
        self.quantity = self.is_valid_quantity(quantity)
        self.target = self.is_valid_target(target)
        self.source = source  # self.is_valid_source(source)

        self.date_of_registration = current_date
        self._id_number = new_transaction_number()
        planned_transactions.append(self)

    @property
    def id_number(self):
        return self._id_number

    def is_valid_date(self, date):
        if date not in calendar:
            raise ValueError('Error: Date must be an integer within the calendar (day 0 to 200)')
        elif date < current_date:
            raise ValueError('Error: Cannot change to past date.')
        return date

    def is_valid_quantity(self, quantity):
        if not isinstance(quantity, int):
            raise ValueError('Error: Quantity must be an integer. ')
        if quantity < 0:
            raise ValueError('Error: Quantity must not be negative. ')
        return quantity

    def is_valid_target(self, target):
        if isinstance(target, ProductionEvent) and target not in valid_production_targets:
            raise ValueError(f'No target named "{target}" exists.')
        if isinstance(self, SaleEvent) and target not in valid_sales_targets:
            raise ValueError(f'Can only send to "shipped" inventory.')
        return target

    def is_valid_source(self, source):
        if isinstance(self, ProductionEvent) and source not in valid_production_sources:
            raise ValueError(f'Inventory "{source}" is an invalid Production source.')
        if isinstance(self, SaleEvent) and source not in valid_sales_sources:
            raise ValueError(f'Inventory "{source}" is an invalid ShipOut source.')
        return source

    def affects_this(self, inventory):  # checks if an event affects the checked inventory
        does_affect = False
        if isinstance(self, ProductionEvent) and self.target == inventory:
            does_affect = True
        elif isinstance(self, SaleEvent) and self.source == inventory:
            does_affect = True
        return does_affect

    def change_quantity(self, new_quantity):
        self.quantity = new_quantity

    def change_date(self, new_date):
        if new_date > current_date:
            print('Warning: You are changing the date to a past date!')
        self.date_of_transaction = new_date


class ProductionEvent(TransactionEvent):
    def __repr__(self):
        return f'P{self.id_number}: On day {self.date_of_transaction} ' \
               f'make {self.quantity} {self.target["name"]} from {self.source["name"]}'


def add_random_production(target, source):
    random_date = random.randint(current_date +1, current_date + 12)
    quantity = random.choice([100, 200])
    ProductionEvent(random_date, quantity, target, source)


class SaleEvent(TransactionEvent):
    def __repr__(self):
        return f'S{self.id_number}: On day {self.date_of_transaction} ship {self.quantity} from {self.source["name"]}'


def add_random_sale(source):
    random_date = random.randint(current_date + 1, current_date + 12)
    quantity = random.choice([random.randint(1,30), 100])
    target = shipped
    # source = 'kits_EU'

    SaleEvent(random_date, quantity, target, source)


if __name__ == '__main__':
    add_random_production(crp_1501, crp_bulk)
    add_random_production(crp_1501, crp_bulk)
    add_random_sale(crp_1501)
    add_random_sale(crp_1501)
    add_random_sale(crp_1501)
    add_random_sale(crp_1501)

    # print(f'List of past productions: {past_productions}')
    print(f'List of planned productions: ')
    print(planned_transactions)

    print(f'List of transaction numbers: {used_transaction_numbers}')
else:
    pass