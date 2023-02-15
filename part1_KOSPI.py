import pandas as pd
import numpy as np


df_w = pd.DataFrame()

for year in [22, 23]:
    for month in range (1, 13):
            try:
                file_name = './data' + '/' + 'Kospi_'+str(year)+'_'+str(month)+'.csv'.format()  # 파일명 지정
                print(file_name)
                df_new = pd.read_csv(file_name, encoding='cp949')  # 시가총액 데이터 로드
                df_new['연도'] = year
                df_new['월'] = month
                df_new['상장시가총액'] = df_new['상장시가총액'].astype(np.int64)
                df_new['시가총액비율'] = df_new['상장시가총액'] / df_new['상장시가총액'].sum()  # 시가총액비율 계산
                df_new.drop(df_new[df_new['종목명']=='LX세미콘'].index, inplace=True) # 22년 12월부터 나오기 때문에 제거
                df_w = pd.concat([df_w, df_new])  # 하나의 데이터프레임으로 병합
            except FileNotFoundError:  # 파일이 존재하지 않으면 pass
                pass

df_w = df_w[['연도', '월', '종목명', '시가총액비율']]
df_w.to_csv('concat.csv', index=False)
