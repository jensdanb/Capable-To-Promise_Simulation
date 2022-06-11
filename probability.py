from projections import *
from scipy.stats import poisson, norm


class ProbabilityFunction(Projection):
    def __init__(self, product, start_date, duration):
        super(ProbabilityFunction, self).__init__(product, start_date, duration)
        self.array = self.create_array()
        self.estimate_ctp()

    def create_array(self):
        days = self.duration
        max_feasible_demand = self.panda["ATP"].min() + days * self.product['demand']['E(daily_demand)'] + \
                              self.product['demand']['SD(PO_size)'] * 2
        max_feasible_supply = self.panda["ATP"].max() + (days - self.product['supply']['E(lead_time)']) * \
                              self.product['supply']['capacity']
        max_size = max(max_feasible_demand, max_feasible_supply)
        return pd.DataFrame(np.zeros((days, int(max_size + 1))), index=self.panda.index)

    def atp_array(self):
        supply_array = self.array
        for day in supply_array.index:
            supply_array.loc[day, :self.panda["atp"][day]] = 1  # cell is further left than atp[day]
        return supply_array

    def plot_2d(self, array):
        plt.imshow(array.T, aspect=1/100)  # , x=self.panda.index
        plt.gca().invert_yaxis()
        plt.show()

    def probable_demand(self):  # Probability that cumulative demand D at day D is more than cell Q
        self.panda['cumulative_demand'] = - np.cumsum(self.panda['demand'])
        probable_demand = self.array
        for day in self.panda.index:
            probable_demand.loc[day, :self.panda['cumulative_demand'][day]] = 0  # Already have more demand than this
            possible_demands = probable_demand.loc[day, self.panda['cumulative_demand'][day]:]

            order_number_distribution = self.distribute_n_of_orders(day)
            possible_demands.apply(self.dist_possible_demand(possible_demands, order_number_distribution, day))

    def dist_possible_demand(self, possible_demands, order_number_distribution, day):
        # given n orders, return P-distribution for total quantity
        possible_demands = 0
        offset_from_zero = self.panda['cumulative_demand'][day] + 5.2
        variance = 3.1

        for n in order_number_distribution:
            distribution_given_n = n * norm.pdf(possible_demands, offset_from_zero, variance)
            print(distribution_given_n)
            possible_demands += sum(distribution_given_n)
        return possible_demands

        # return [P(c=0), P(c=1), P(c=2), ... P(c=len(size_range))]

    def distribute_n_of_orders(self, days_forward):
        intensity = self.product['demand']['P(new_PO_today)']
        probable_orders = []
        number = 0
        remaining_p = 1.0
        while remaining_p >= 0.025:
            chance = poisson.pmf(k=number, mu=intensity * days_forward)
            probable_orders.append(chance)
            remaining_p -= chance
            number += 1
        return probable_orders


if __name__ == '__main__':
    # print(planned_transactions)
    my_array = ProbabilityFunction(cys_1101, 0, 11)
    my_array.plot_estimate()

    # print(my_array.atp_array())
    # my_array.plot_2d(my_array.atp_array())

    # my_array.probable_demand()
    print(my_array.panda)
    print(my_array.array)
    my_array.plot_2d(my_array.array)
