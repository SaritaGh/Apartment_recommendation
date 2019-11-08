
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
import pygmo as pg
pd.set_option('display.width', 1000); pd.set_option('max_columns', 8);
pd.set_option('display.max_colwidth', -1)

DATAFILE = '/Users/abasak/PycharmProjects/testing/apartment_search/data/test.pkl'
BUDGET = 3000
TOP_N = 10

MIN_BEDROOMS = 2
MIN_BATHROOMS = 1.01
MIN_PRICE = 1000
SAMPLE_APARTMENTS = 400


def find_n_best(df, n):
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(-1.0 * df.to_numpy())
    # print('non dom fronts', ndf)
    # print(ndf[0])
    print('Best: \n', df.iloc[ndf[0][:n]])
    print('Worse: \n', df.iloc[ndf[-2][:n]])
    print('Worst: \n', df.iloc[ndf[-1][:n]])
    return df.sample(n=n)


def main():
    all_apartments = pd.read_pickle(DATAFILE)
    common_features = set(["Elevator", "Cats Allowed", "Hardwood Floors", "Dogs Allowed", "Doorman",
                           "Dishwasher", "No Fee", "Laundry in Building", "Fitness Center", "Pre-War",
                           "Laundry in Unit", "Roof Deck", "Outdoor Space", "Dining Room", "High Speed Internet",
                           "Balcony", "Swimming Pool", "Laundry In Building", "New Construction", "Terrace"])
    relevant_apartments = all_apartments[(all_apartments['price'] >= MIN_PRICE) & (all_apartments['bedrooms'] >= MIN_BEDROOMS) & (all_apartments['bathrooms'] >= MIN_BATHROOMS)]
    apartments_in_budget = relevant_apartments[(relevant_apartments['price'] <= BUDGET)]
    apartments_in_budget['feature_score'] = apartments_in_budget.features.apply(lambda x: len(set(x).intersection(common_features)))
    apartments_in_budget['neg_price'] = - apartments_in_budget.price
    apartments_relevant_columns = apartments_in_budget[['neg_price', 'bedrooms', 'bathrooms', 'feature_score']]

    # find_n_best(apartments_relevant_columns.sample(n=SAMPLE_APARTMENTS), TOP_N)
    find_n_best(apartments_relevant_columns, TOP_N)
    # print(find_n_best(apartments_relevant_columns.sample(n=SAMPLE_APARTMENTS), TOP_N))

if __name__ == '__main__':
    main()