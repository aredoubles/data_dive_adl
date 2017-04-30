import os
import pandas as pd


def score_to_numeric(x):
    if x is False:
        return 0
    if x is True:
        return 1
    if x is 0:
        return 0
    if x is 1:
        return 1


def mergecrawl():
    # Need to establish/reset the dataframe
    fulldf = pd.DataFrame()

    for root, dirs, files in os.walk('ArticleCSVs'):
        for file in files:
            print('{}{}'.format('NOW WORKING ON:    ', file))
            if file[-4:] != '.csv':
                continue
            with open('ArticleCSVs/' + file) as f:
                # Read CSV to pandas
                df = pd.read_csv(f)
                # Clean the text columns
                '''
                for i in range(df.shape[0]):
                    fulltext = df['text'][i]    # Iterate over records
                    fulltext = fulltext.replace('\r', ' ').replace('\n', ' ')
                    df['text'][i] = fulltext
                    '''
                df.columns = ['url', 'text', 'source', 'label']
                df['text'] = df['text'].str.slice(start=0, stop=32000)
                df['text'] = df['text'].str.replace('\n', ' ')
                # Append to prev pandas df
                # What if we're starting out, and it's empty?

                # Check if class column is 0,1 or T,F, adjust to 0,1 if latter
                df['label'] = df['label'].apply(score_to_numeric)

                fulldf = pd.concat([fulldf, df])

                fulldf.to_csv('articles-all.csv')

    return fulldf


if __name__ == '__main__':
    mergecrawl()
