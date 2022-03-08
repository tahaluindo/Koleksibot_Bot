import sys
import pandas as pd
import requests
import json

BASEURL = 'https://api.appnexus.com/auth'
AUTHTOKEN = None
USERNAME = 'Test_Account_Janina'
PASSWORD = 'Test123456!'

report_type = 'seller_brand_review'
start_date = '2019-09-01'
end_date = '2019-10-01'
columns: list = [
    'day', "imp_type_id", 'imp_type',
    'imps', 'revenue',
]
filters = [{"imp_type_id": ["6", "7"]}]
# --
report_json_query = {
    "report": {
        "report_type": report_type,
        "start_date": start_date,
        "end_date": end_date,
        "columns": columns,
        "filters": filters,
        "reporting_decimal_type": "decimal",
        "format": "csv"
    }
}

def Res_Message(response):
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return False
    elif response.status_code == 404:
        print('[!] [{0}] URL not found'.format(response.status_code))
        return False
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        return False
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        return False
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return False
    elif response.status_code == 200:
        #ssh_keys = json.loads(response.content.decode('utf-8'))
        return True
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    return None

s = requests.Session()
# Proxy
# s.proxies = {
#               'http':'http://proxy.xxxxxx.net:xxxxx',
#              'https':'https://proxy.xxxxxx.net:xxxxx'
#             }
auth_app = json.dumps({'auth': {'username': USERNAME, 'password': PASSWORD}})

Report_Req_url = 'https://api.appnexus.com/report'
Auth_Token = s.post(BASEURL, data=auth_app)  # ,proxies=proxy})
if (Res_Message(Auth_Token)==True):
    Auth_Res_Data = json.loads(Auth_Token.text)
    AUTHTOKEN = Auth_Res_Data['response']['token']
    print(Auth_Res_Data)
else : sys.exit()

Request_a_report = 'https://api.appnexus.com/report'
Report_Resp = s.post(Request_a_report, data=report_json_query)
if (Res_Message(Report_Resp)==True):
    Report_Data = json.loads(Report_Resp.text)
    print(Report_Data)
else : sys.exit()

Report_Status_Check = 'https://api.appnexus.com/report?id={}'.format(Report_Data['REPORT_ID'])
Report_Status_Check_Resp = s.get(Report_Status_Check, headers={"Authorization": AUTHTOKEN},timeout=1)
if (Res_Message(Report_Status_Check_Resp)==True):
    Report_Status_Check_Data = json.loads(Report_Status_Check_Resp.text)
    print(Report_Status_Check_Data)
else : sys.exit()
Download_Report = 'https://api.appnexus.com/report-download?id={}'.format(Report_Data['REPORT_ID'])
Download_Report_Resp = s.get(Download_Report, headers={"Authorization": AUTHTOKEN},timeout=1)
if (Res_Message(Download_Report_Resp) == True):
    Download_Report_Data = json.loads(Download_Report_Resp.text)
    print(Download_Report_Data)
else : sys.exit()

#pd.DataFrame(list(JSON.items()), columns=['Date', 'DateValue'])
Report_DF=pd.DataFrame()
Report_Data.to_csv("seller_brand_review.csv")


