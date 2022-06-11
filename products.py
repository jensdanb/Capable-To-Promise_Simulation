
inventories_day_zero = {
    'raw_material': 1000,
    'bulk': 300,  # centiliters. 1 = enough for 1 kit. 100 = 1 Liter.
    'kits_USA': 100,
    'kits_BC': 150,
    'kits_EU': 100,  # 10mL = 1cL per kit
    'shipped': 0
}

cys_1101 = {
    'name': "cys_1101",
    'inventory': 100,
    'supply': {
        "E(lead_time)": 5,
        "SD(lead_time)": 4,
        "capacity": 200
    },
    'demand': {
        'E(daily_demand)': 5,
        'P(new_PO_today)': 1/4,
        'E(PO_size)': 20,
        'large_orders': {
            'proportion' : 12/24,
            'avg_size': 26.8,
            'variance': 141.8
        },
        'small_orders': {
            'proportion': 12/24,
            'avg_size': 3.2,
            'variance': 2.14
        },
        'SD(PO_size)': 20,
        'E(PO_due_date)': 6
    }
}

crp_1501 = {
    'name': 'crp_1501',
    'inventory': 120,
    'supply': {
        'E(lead_time)': 5,
        'SD(lead_time)': 4,
        'capacity': 40
    },
    'demand': {
        'E(daily_demand)': 5,
        'P(new_PO_today)': 1/4,
        'E(PO_size)': 20,
        'SD(PO_size)': 20,
        'E(PO_due_date)': 6
    }
}

crp_raw = {'name': 'crp_raw', 'inventory': 100}
crp_bulk = {'name': 'crp_bulk', 'inventory': 300}
shipped = {'name': 'shipped', 'inventory': 0}

products = [cys_1101, crp_1501, crp_bulk]
valid_production_sources = [crp_bulk, crp_raw]
valid_production_targets = products
valid_sales_sources = [products]
valid_sales_targets = [shipped]

demand_1101 = {
    'E(daily_demand)': 5,
    'P(new_PO_today)': 1/4,
    'E(PO_size)': 20,
    'SD(PO_size)': 20,
    'E(PO_due_date)': 6
}

forewarned_PO = {
    'expected_quantity': 200,
    'standard_deviation': 50,  # short: 'sd'. variance = sd^2
    'expected_date_of_PO': 6,
    'expected_due_date': 10  # days from PO placement! Not calendar date
}
