import pandas as pd
import matplotlib.pyplot as plt


def question1(dataframe1, dataframe2):
    print('Q1')
    pd.set_option('display.max_columns',None,'display.max_rows',None)
    pd.set_option('display.width', 1000)
    df = pd.merge(dataframe1, dataframe2, how='inner', left_index=True, right_index=True)
    print(df.head(5))
    return df


def question2(dataframe):
    print('Q2')
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    pd.set_option('display.width', 1000)
    dataframe.index.name = 'country name'
    print(dataframe.head(1))


def question3(dataframe):
    print('Q3')
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    pd.set_option('display.width', 1000)
    del dataframe['Rubish']
    print(dataframe.head(5))


def question4(dataframe):
    print('Q4')
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    pd.set_option('display.width', 1000)
    dataframe = dataframe.dropna(how = 'any')
    print(dataframe.tail(10))


def question5(dataframe):
    print('Q5')
    dataframe = dataframe.drop('Totals')
    dataframe = dataframe.dropna(how = 'any')
    dataframe['Gold_x'] = dataframe['Gold_x'].str.replace(',', '').astype(int)
    country  = dataframe.sort_values('Gold_x', ascending=False).head(1).index.values[0]
    Gold = dataframe.sort_values('Gold_x', ascending=False).head(1)['Gold_x'].values[0]
    print(f'The country who wins the most gold medal is:{country} and the number is {Gold}.')


def question6(dataframe):
    print('Q6')
    dataframe = dataframe.drop('Totals')
    dataframe = dataframe.dropna(how = 'any')
    dataframe['Gold_x'] = dataframe['Gold_x'].str.replace(',', '').astype(int)
    dataframe['Gold_y'] = dataframe['Gold_y'].str.replace(',', '').astype(int)
    dataframe['difference'] = abs(dataframe['Gold_x']-dataframe['Gold_y'])
    country = dataframe.sort_values('difference',ascending=False).head(1).index.values[0]
    difference = dataframe.sort_values('difference',ascending=False).head(1)['difference'].values[0]
    print(f'The country who has the biggest difference between the summer and winter gold mental is {country}'
          f' and the difference is {difference}.')


def question7(dataframe):
    print('Q7')
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    dataframe = dataframe.drop('Totals')
    dataframe['Total.1'] = dataframe['Total.1'].str.replace(',', '').astype(float)
    print(dataframe.sort_values('Total.1', ascending = False).head(5))
    print(dataframe.sort_values('Total.1', ascending=False).tail(5))


def question8(dataframe):
    dataframe = dataframe.drop('Totals')
    dataframe = dataframe.dropna(how = 'any')
    dataframe['Total.1'] = dataframe['Total.1'].str.replace(',', '').astype(int)
    dataframe['Total_x'] = dataframe['Total_x'].str.replace(',', '').astype(int)
    dataframe['Total_y'] = dataframe['Total_y'].str.replace(',', '').astype(int)
    dataframe = dataframe.sort_values('Total.1', ascending=False).head(10)
    dataframe = dataframe[['Total_x','Total_y']]
    dataframe = dataframe.rename(columns={'Total_x':'Summer games','Total_y':'Winter games'})
    dataframe.plot.barh(stacked=True);
    plt.title('Q8 : Medals for Winter and Summer Games')
    plt.show()


def question9(dataframe2):
    dataframe2 = dataframe2.loc[[' United States (USA) [P] [Q] [R] [Z]',' Australia (AUS) [AUS] [Z]',
                   ' Great Britain (GBR) [GBR] [Z]',' Japan (JPN)',' New Zealand (NZL) [NZL]']]
    dataframe2 = dataframe2[['Gold','Silver','Bronze']]
    dataframe2['Gold'] = dataframe2['Gold'].str.replace(',', '').astype(int)
    dataframe2['Silver'] = dataframe2['Silver'].str.replace(',', '').astype(int)
    dataframe2['Bronze'] = dataframe2['Bronze'].str.replace(',', '').astype(int)
    dataframe2 = dataframe2.rename(index={' United States (USA) [P] [Q] [R] [Z]':'United States',
                            ' Australia (AUS) [AUS] [Z]':'Australia',
                            ' Great Britain (GBR) [GBR] [Z]':'Great Britain',
                            ' Japan (JPN)':'Jpapan',
                            ' New Zealand (NZL) [NZL]':'New Zealand'
                            })
    dataframe2.plot.bar(color=['cornflowerblue', 'darkorange', 'lightgray'])
    plt.title('Q9 : Winter Games')
    plt.xticks(rotation=0)
    plt.show()


if __name__ == '__main__':
    df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
    df2 = pd.read_csv('Olympics_dataset2.csv' , index_col=0, skiprows=1)

    df = question1(df1,df2)
    question2(df.copy())
    question3(df.copy())
    question4(df.copy())
    question5(df.copy())
    question6(df.copy())
    question7(df.copy())
    question8(df.copy())
    question9(df2)