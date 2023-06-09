from time import sleep

from bs4 import BeautifulSoup
import pandas as pd
import requests

d_list = []
df = pd.DataFrame(d_list)

# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=060&bs=040&ra=026&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=242028425&ek=242038640&ek=242026920&rn=2420&ek=209526950&ek=209529420&ek=209532470&ek=209553950&rn=2095&page={}'

# 変数d_listに空のリストを作成する
d_list = []

# アクセスするためのURLをtarget_urlに格納する
for i in range(1, 4):
    print('d_listの大きさ：', len(d_list))
    target_url = url.format(i)

    # print()してtarget_urlを確認する
    print(target_url)

    # target_urlへのアクセス結果を、変数rに格納
    r = requests.get(target_url)
    
    sleep(1)

    # 取得結果を解析してsoupに格納
    soup = BeautifulSoup(r.text)
    
    # すべての物件情報を取得する
    contents = soup.find_all('div', class_='cassetteitem')

    # 各物件情報をforループで取得する
    for content in contents:
        # 物件情報と部屋情報を取得しておく
        detail = content.find('div', class_='cassetteitem_content')
        table = content.find('table', class_='cassetteitem_other')

        # 物件情報から必要な情報を取得する
        title = detail.find('div', class_='cassetteitem_content-title').text
        address = detail.find('li', class_='cassetteitem_detail-col1').text
        access = detail.find('li', class_='cassetteitem_detail-col2').text
        age = detail.find('li', class_='cassetteitem_detail-col3').text

        # 部屋情報のブロックから、各部屋情報を取得する
        tr_tags = table.find_all('tr', class_='js-cassette_link')

        # 各部屋情報をforループで取得する
        for tr_tag in tr_tags:        

            # 部屋情報の行から、欲しい情報を取得する
            floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

            # さらに細かい情報を取得する
            fee, management_fee = price.find_all('li')
            deposit, gratuity = first_fee.find_all('li')
            madori, menseki = capacity.find_all('li')

            # 取得したすべての情報を辞書に格納する
            d = {
                'title': title,
                'address': address,
                'access': access,
                'age': age,
                'floor': floor.text,
                'fee': fee.text,
                'management_fee': management_fee.text,
                'deposit': deposit.text,
                'gratuity': gratuity.text,
                'madori': madori.text,
                'menseki': menseki.text
            }

            # 取得した辞書をd_listに格納する
            d_list.append(d)

# 変数d_listを使って、データフレームを作成する
df = pd.DataFrame(d_list)

# to_csv()を使って、データフレームをCSV出力する
df.to_csv('suumo_info20230531.csv', index=None, encoding='utf-8-sig')