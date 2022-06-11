from transactions import *
import numpy as np
import pandas as pd


def transactions_dataframe(product, starting_date, days_forward):
    days_projected = [day for day in range(starting_date, starting_date + days_forward)]
    supply = [0] * days_forward
    demand = [0] * days_forward

    # Fill in supply and demand
    supply[0] = product["inventory"]
    for event in planned_transactions:
        if event.date_of_transaction in range(starting_date, starting_date + days_forward):
            if isinstance(event, ProductionEvent) and event.target == product:
                supply[event.date_of_transaction - starting_date] += event.quantity
            if isinstance(event, SaleEvent) and event.source == product:
                demand[event.date_of_transaction - starting_date] -= event.quantity
    panda = pd.DataFrame({'supply': supply, 'demand': demand}, index=days_projected)

    # Add ATP column: The cumulative sum of supply - demand
    panda["inventory"] = np.cumsum(panda['supply']) + np.cumsum(panda['demand'])
    return pd.DataFrame(panda, index=days_projected)


# ProductionEvent(4, 150, crp_1501, crp_bulk)
# ProductionEvent(9, 150, crp_1501, crp_bulk)
# for i in range(1):
#     add_random_production(crp_1501, crp_bulk)

# SaleEvent(2, 60, shipped, crp_1501)
# SaleEvent(6, 100, shipped, crp_1501)
# SaleEvent(7, 50, shipped, crp_1501)
# SaleEvent(12, 100, shipped, crp_1501)
# for i in range(4):
#     add_random_sale(crp_1501)


if __name__ == '__main__':
    print(planned_transactions)
    print(transactions_dataframe(crp_1501, 0, 8))
else:
    pass
