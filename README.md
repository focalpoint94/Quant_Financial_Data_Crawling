# Quant_Financial_Data_Crawling
상장 기업 재무 정보 크롤링

## get_codes.py
상장 기업 종목 코드를 저장합니다. 종목 코드는 "krx_codes.json"으로 저장됩니다.

## get_company_info.py
Dart 공시 주식회사 Info Excel File 생성합니다. 생성된 파일은 "company_info.xlsx"로 저장됩니다.

## get_all_financial_data.py
company_info.xlsx 파일로부터 공시 기업 목록을 불러온 뒤, 특정 기간부터의 재무 데이터를 fsdata 폴더에 저장합니다.

## FD_Handler.py
저장한 fsdata에서 유용한 지표들을 산출해내기 위한 모듈입니다.
Dart에 공시된 재무정보는 그 양식이 통일되어있지 않습니다.
따라서 keyword를 적절히 조합하여 재무 정보를 적절한 형태로 다시 표현할 필요가 있습니다.
사용 예시는 아래와 같습니다.
```
FDH = FD_Handler(code='000060')
all_list = FDH.get_data(type='all')
print(all_list)
label_list = ['당기순이익', '계속영업이익']
inc_kw_list = []
exc_kw_list = ['귀속']
k, v = FDH.get_value(year='2015', label_list=label_list, inc_kw_list=inc_kw_list, exc_kw_list=exc_kw_list)
```
- label_list: 공시 정보에서 찾을 keyword입니다.
- inc_kw_list: 꼭 포함해야 하는 keyword list입니다.
- exc_kw_list: 배제해야 하는 keyword list입니다.
유용한 예시는 아래와 같습니다.
```
* 영업활동현금흐름 *
label_list = ['현금흐름']
inc_kw_list = []
exc_kw_list = ['손익', '투자', '재무', '환율', '위험', '종속', '지배력']
* 당기순이익 *
label_list = ['당기순이익']
inc_kw_list = []
exc_kw_list = ['귀속', '조정', '가감', '법인세', '관계', '계속', '중단', '지분', '세', '분류']
* 자본총계 *
label_list = ['자본총계']
inc_kw_list = []
exc_kw_list = ['부채', '자산']
* 부채총계 *
label_list = ['부채총계']
inc_kw_list = []
exc_kw_list = ['자본', '자산']
* 유동자산 *
label_list = ['유동자산']
inc_kw_list = []
exc_kw_list = ['비', '기타']
```

## get_PCR_Data.py
FD_Handler 모듈을 사용하는 예시입니다. 상장 기업의 PCR를 계산하여 각 연도별로 저장합니다.

## get_debt_ratio.py
FD_Handler 모듈을 사용하는 예시입니다. 상장 기업의 부채비율 계산하여 각 연도별로 저장합니다.


