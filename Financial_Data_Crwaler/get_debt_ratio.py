
"""
get_debt_ratio.py
상장 기업의 부채비율 계산하여 각 연도별로 저장 (2009년 ~ 2020년)
"""
from FD_Handler import FD_Handler
from pykrx import stock
import pandas as pd
import math
import json
import os


def _get_debt_ratio(test_year: str):
    """
    :param test_year: 연도 (e.g. "2010")
    :return:
    당해 연도 상장 기업의 부채비율을 계산하여 저장
    * 부채비율이 없는 종목 부채비율 = math.nan
    """
    """
    부채비율 List
    [(code1, debt_ratio1), ...]
    """
    debt_ratio_list = []

    """
    Dates
    """
    test_date = test_year + "0101"
    test_date = stock.get_nearest_business_day_in_a_week(date=test_date, prev=False)

    """
    Calculate debt ratio
    """
    df1 = stock.get_market_fundamental_by_ticker(test_date, market="KOSPI")
    df2 = stock.get_market_fundamental_by_ticker(test_date, market="KOSDAQ")
    df = pd.concat([df1, df2])
    code_list = df.index.to_list()
    for code in code_list:
        FDH = FD_Handler(code=code)
        # 데이터가 없는 경우
        if not FDH.has_data:
            debt_ratio_list.append((code, math.nan))
            continue
        label_list = ['자본총계']
        inc_kw_list = []
        exc_kw_list = ['부채', '자산']
        k, equity = FDH.get_value(year=test_year, label_list=label_list, inc_kw_list=inc_kw_list,
                                  exc_kw_list=exc_kw_list)
        if equity is None:
            debt_ratio_list.append((code, math.nan))
            continue
        label_list = ['부채총계']
        inc_kw_list = []
        exc_kw_list = ['자본', '자산']
        k, debt = FDH.get_value(year=test_year, label_list=label_list, inc_kw_list=inc_kw_list,
                                  exc_kw_list=exc_kw_list)
        if debt is None:
            debt_ratio_list.append((code, math.nan))
            continue
        debt_ratio = debt / equity * 100
        debt_ratio_list.append((code, debt_ratio))

    """
    Save Data
    """
    save_dir = './debt_ratio_Data/'
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    file_name = save_dir + test_year + '.json'
    with open(file_name, 'w') as f:
        json.dump(debt_ratio_list, f)


for year in range(2009, 2021):
    _get_debt_ratio(test_year=str(year))


save_dir = './debt_ratio_Data/'
for year in range(2009, 2021):
    file_name = save_dir + str(year) + '.json'
    with open(file_name, 'r') as f:
        debt_ratio_list = json.load(f)
        debt_ratio_list_without_nan = [debt_ratio for debt_ratio in debt_ratio_list if not math.isnan(debt_ratio[1])]
        print(str(year), '부채비율 데이터 확보율:', str(round(len(debt_ratio_list_without_nan)/len(debt_ratio_list)*100, 2)) + '%')

