import requests
import bs4
import linebot

indURL = "https://fx.minkabu.jp/indicators"
USER_IDs = [
    "U6b6d2104d9f00e1a0bcca6a2d31e7ead"
]
CAT = "hFM49n3kvJIK/3HOhCHymikcXOQha/wpi1ZkIzl2XcXyrja8OAEnSErkw4iYJoV1DLNkqNeB1+zVDH+joG4kRo+xQHFVFxf29ShNiebeb43z63eBBjqdCNGVTl9PQsjn9SZHQQjLEQZs06zxDyw3FAdB04t89/1O/w1cDnyilFU="

res = requests.get(indURL)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
date = soup.select_one('caption.tbl__caption.tlft.pl10.pt5.pb5.fs-s.fbd').text
elmIndTbl = soup.select_one('.tbl-border.tbl-fixed.tbl-alternate.mt5.mb5')
lineMsg = date + "の経済指標です\n"
for i in elmIndTbl.select('tr'):
    impCnt = 0
    if i.select_one('td.eilist__time span') != None:
        #clc import level
        for j in i.select('img.i-star'):
            if "Star fill" in j.attrs['alt']:
                impCnt += 1
        
        lineMsg += i.select_one('td.eilist__time').text.replace("\n","") + " "
        lineMsg += "重要度" + str(impCnt) + "\n"
        lineMsg += i.select_one('p.flexbox__grow.fbd').text.replace("\n","") + "\n"
        lineMsg += "------------------------------------------------------------\n"
        
lineMsg += indURL
messages = linebot.models.TextSendMessage(text = lineMsg)
linebot.LineBotApi(CAT).push_message(USER_IDs[0], messages = messages)
print(lineMsg)
