import pandas as pd
import numpy as np
from tqdm import tqdm, trange

data_raw = pd.read_csv('./data/NewsResult_20221101-20230201.csv', encoding='utf-8')
data = data_raw[['일자','제목']]

data['연도'] = data['일자'].astype(str).str[2:4].astype(int)
data['월'] = data['일자'].astype(str).str[4:6].astype(int)
data = data[['일자','연도','월','제목']]
print(data)

df_w = pd.read_csv('concat.csv')
stock_list = list(df_w['종목명'].unique())
print(stock_list)
print(len(stock_list))

data['종목명'] = 'default'
data_mt = []    # multiple title

for sl in tqdm(stock_list) :
    for i in range(len(data)) :
        if sl in data.loc[i, '제목'].upper() :         # 제목에 종목명이 있을 때(대문자로 통일)
            if data.loc[i, '종목명'] == 'default' :    # 종목명이 하나인 경우
                data.loc[i, '종목명'] = sl             # 종목명 부여
            else :                                     # 종목명이 여러개인 경우
                row_tmp = data.loc[i]                  # 행 복사
                row_tmp['종목명'] = sl                 # 종목명 부여
                data_mt.append(row_tmp)

data_mt = pd.DataFrame(data_mt)
data = pd.concat([data,data_mt])
data = data.reset_index(drop=True)

data = data.drop_duplicates(ignore_index=True)
# data.drop(data[data['종목명']=='default'].index, inplace=True)

data.to_csv('concat_01.csv', index=False)
