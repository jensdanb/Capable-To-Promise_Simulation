from probability import *
from products import *
from scipy.stats import poisson, norm


def chance_that_q_is_x(x, n_orders, product):
    if product == cys_1101:
        return split_distribution(x, n_orders, cys_1101)


def split_distribution(x, n_orders, product):
    p_large_orders = product['demand']['large_orders']['proportion']
    p_small_orders = product['demand']['small_orders']['proportion']

    avg_large_order = product['demand']['large_orders']['avg_size']
    avg_small_order = product['demand']['small_orders']['avg_size']

    var_large_order = product['demand']['large_orders']['variance']
    var_small_order = product['demand']['small_orders']['variance']




if __name__ == '__main__':
    print(orders_today(cys_1101, 5))
    # print(sum(orders_today(crp_1501, 5)))

else:
    pass
