from known__transactions import *
from products import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Projection():
    def __init__(self, product, start_date, duration):
        self.product = self.is_valid_product(product)
        self.start_date = self.is_valid_date(start_date)
        self.duration = self.is_valid_duration(duration)
        self.end_date = self.is_valid_end_date(start_date + self.duration)

        self.current_inventory = self.product['inventory']
        self.panda = transactions_dataframe(self.product, self.start_date, self.duration)
        self.panda["ATP"] = [self.panda.loc[i:self.end_date - 1, "inventory"].min() for i in self.panda["inventory"].index]

    def is_valid_product(self, product):
        if product not in products:
            raise ValueError(f'Error: No product named "{product}" exists.')
        return product

    def is_valid_date(self, date):
        if date not in calendar:
            raise ValueError('Error: Date must be an integer within the calendar (day 0 to 200)')
        return date

    def is_valid_end_date(self, end_date):
        if not self.is_valid_date(end_date) or end_date <= self.start_date:
            return ValueError('Invalid end date. Date is out of range or before start date. ')
        return end_date

    def is_valid_duration(self, duration):
        if not isinstance(duration, int) and duration > 0:
            return ValueError('Duration must be a positive integer.')
        return duration

    def is_valid_transaction_list(self, transactions):
        for transaction in transactions:
            if not isinstance(transaction, TransactionEvent):
                raise ValueError('Error! List of transactions contains a non-transaction')
            if not transaction.affects_this(self.product):
                transactions.remove(transaction)
        return transactions

    def plot_selected(self, column_list):
        self.panda.loc[:, column_list].plot(kind="bar")  # plot(kind="bar")
        plt.title('General CTP')  # 'ATP/CTP Plot'
        plt.xlabel('Day')
        plt.ylabel('CTP')
        plt.show()

    def plot(self):
        self.panda.plot(kind="bar")
        plt.title('ATP Chart')
        plt.xlabel('Day')
        plt.ylabel('Quantity')
        plt.show()

    def estimate_demand(self):  # Inputs: Dataframe, Dict
        avg_new_demand = self.product['demand']["P(new_PO_today)"] * self.product['demand']["E(PO_size)"]
        estimate_per_day = [avg_new_demand] * len(self.panda.index)

        self.panda["E(demand)"] = - np.cumsum(self.panda["demand"]) + np.cumsum(estimate_per_day)

    def estimate_supply(self):
        self.panda["E(supply)"] = [0] * self.duration
        # After lead time, add daily capacity:
        self.panda.loc[self.start_date + self.product['supply']['E(lead_time)']:10, 'E(supply)'] = \
            self.product['supply']['capacity']
        # If there is already a bigger production planned that day, use that instead:
        self.panda["E(supply)"] = self.panda.loc[:, ["supply", "E(supply)"]].max(axis = 1)
        self.panda["E(supply)"] = np.cumsum(self.panda["E(supply)"])

    def estimate_ctp(self):
        self.estimate_supply()
        self.estimate_demand()
        self.panda["CTP"] = self.panda["E(supply)"] + np.cumsum(self.panda["demand"])  # - self.panda["E(demand)"]  to include estimated new POs

    def plot_estimate(self):
        self.panda.loc[:, ["E(supply)", "E(demand)", "E(CTP)"]].plot(kind="bar")
        plt.title('ATP Chart')
        plt.xlabel('Day')
        plt.ylabel('Cumulative quantity')
        plt.show()


if __name__ == '__main__':
    print('Production and shipping plan: ')
    print(planned_transactions)
    
    projection = Projection(crp_1501, 0, 15)
    projection.estimate_ctp()

    print(projection.panda)
    projection.plot_selected(["CTP"])

else:
    pass
