import os
import pandas as pd


def localart():
    textdict = {}

    for root, dirs, files in os.walk('Articles/Local-Hate'):
        for file in files:
            with open('Articles/Local-Hate/' + file) as f:
                string = f.read()
                string = string.replace('\r', ' ').replace('\n', ' ')
                textdict[file] = string

    build = pd.DataFrame.from_dict(textdict, orient='index')
    build.columns = ['Text']
    build['Source'] = 'A local paper'
    build['Hate crime'] = 1
    build.index.names = ['URL']
    build.to_csv('Local1.csv')

    return build


if __name__ == '__main__':
    localart()
