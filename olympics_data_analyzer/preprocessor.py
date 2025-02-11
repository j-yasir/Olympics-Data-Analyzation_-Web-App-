import pandas as pd



def preprocess(df,region_df):

    #filtering for summer olympics
    df = df[df['Season'] == 'Summer']

    #merge with region df to get region
    df = df.merge(region_df, on = 'NOC', how = 'left')

    #droping duplicates
    df.drop_duplicates(inplace = True)

    #onehot encoding
    df = pd.concat([df, pd.get_dummies(df['Medal'])] , axis =1)

    return df

