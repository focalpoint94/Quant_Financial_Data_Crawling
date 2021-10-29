
"""
get_PCR.py
상장 기업의 PCR를 계산하여 각 연도별로 저장 (2009년 ~ 2020년)
"""
from FD_Handler import FD_Handler
from pykrx import stock
import pandas as pd
import math
import json
import os


def _get_PCR(test_year: str):
    """
    :param test_year: 연도 (e.g. "2010")
    :return:
    당해 연도 상장 기업의 PCR 값을 계산하여 저장
    * PCR 값이 없는 종목 PCR = math.nan
    """
    """
    PCR List
    [(code1, PCR1), ...]
    """
    PCR_list = []

    """
    Dates
    """
    test_date = test_year + "1231"
    test_date = stock.get_nearest_business_day_in_a_week(date=test_date, prev=False)

    """
    Calculate PCR
    """
    df1 = stock.get_market_fundamental_by_ticker(test_date, market="KOSPI")
    df2 = stock.get_market_fundamental_by_ticker(test_date, market="KOSDAQ")
    df = pd.concat([df1, df2])
    code_list = df.index.to_list()
    temp = stock.get_market_cap_by_ticker(test_date)
    temp = temp[['시가총액']]
    for code in code_list:
        """ 시가총액 """
        cap = temp.loc[code]['시가총액']
        """ 영업활동현금흐름 """
        FDH = FD_Handler(code=code)
        # 데이터가 없는 경우
        if not FDH.has_data:
            PCR_list.append((code, math.nan))
            continue
        label_list = ['현금흐름']
        inc_kw_list = []
        exc_kw_list = ['손익', '투자', '재무', '환율', '위험', '종속', '지배력']
        k, v = FDH.get_value(year=test_year, label_list=label_list, inc_kw_list=inc_kw_list, exc_kw_list=exc_kw_list)
        if v is None:
            PCR_list.append((code, math.nan))
            continue
        PCR = cap / v
        PCR_list.append((code, PCR))

    """
    Save Data
    """
    save_dir = './PCR_Data/'
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    file_name = save_dir + test_year + '.json'
    with open(file_name, 'w') as f:
        json.dump(PCR_list, f)


for year in range(2009, 2021):
    _get_PCR(test_year=str(year))


save_dir = './PCR_Data/'
for year in range(2009, 2021):
    file_name = save_dir + str(year) + '.json'
    with open(file_name, 'r') as f:
        PCR_list = json.load(f)
        PCR_list_without_nan = [PCR for PCR in PCR_list if not math.isnan(PCR[1])]
        print(str(year), 'PCR 데이터 확보율:', str(round(len(PCR_list_without_nan)/len(PCR_list)*100, 2)) + '%')
