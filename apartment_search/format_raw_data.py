
import json
import pandas as pd
pd.set_option('display.width', 1000); pd.set_option('max_columns', 8);
pd.set_option('display.max_colwidth', -1)

def main():
    filename = 'data/test.json'
    data = None
    with open(filename) as json_file:
        data = json.load(json_file)
    print(data.keys())
    print(type(data['listing_id']))
    print({x:data['listing_id'][x] for x in data['listing_id'].keys()[:10]})
    growing_df = pd.DataFrame({'id': [int(i) for i in data['listing_id'].keys()], 'listing_id': data['listing_id'].values()}).set_index('id')

    for column in data.keys():
        if column in growing_df.columns:
            continue
        print('Processing ', column)
        entries = data[column]
        df = pd.DataFrame({'id': [int(i) for i in entries.keys()], column: entries.values()}).set_index('id')
        growing_df = growing_df.join(df)
    # growing_df.to_pickle("data/test.pkl")
    print(growing_df[['created', 'price', 'bedrooms', 'bathrooms', 'display_address', 'features', 'description']].head())


if __name__ == '__main__':
    main()
