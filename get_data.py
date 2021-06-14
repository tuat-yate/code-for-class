from abc import abstractproperty
import sys
import csv

# read file
file=sys.argv[1]
with open(file) as f:
    reader=csv.reader(f)
    data=[row for row in reader]

# del header
data=data[1:]

# 出力フォーマット
# 打鍵時間(あるキーの押下から解放まで)
# 打鍵間隔(あるキーの解放から次のキーの押下まで)
# 打鍵周期(あるキーの押下から次のキーの押下まで)
# 打鍵周期(あるキーの解放から次のキーの解放まで)

# データの整形
# データを2個刻みで見ていき、同じ文字の押下・解放が続いていないとき1つ先と入れ替え
afdata=list()
for gyou in range(0,len(data)-1,2):
    if(data[gyou][2]==data[gyou+1][2]):
        afdata.append(data[gyou])
        afdata.append(data[gyou+2])
        data[gyou+2]=data[gyou+1]
    else:
        afdata.append(data[gyou])
        afdata.append(data[gyou+1])

afdata.extend(data[len(afdata):])

out=[[0 for i in range(4)] for k in range(len(afdata))]

# 実際の計算
# 0のときは入力なし
for gyou in range(len(afdata)):
    if(gyou==0):
        pass

    # 押下時
    # 打鍵間隔と打鍵周期PPを計算
    elif(gyou%2==0):
        # RP
        out[gyou][1]=float(afdata[gyou][0])-float(afdata[gyou-1][0])
        # PP
        out[gyou][2]=float(afdata[gyou][0])-float(afdata[gyou-2][0])

    # リリースの時
    elif(gyou%2==1):
        # PR
        out[gyou][0]=float(afdata[gyou][0])-float(afdata[gyou-1][0])
        if(gyou!=1):
            # RR
            out[gyou][3]=float(afdata[gyou][0])-float(afdata[gyou-2][0])

for gyou in range(len(out)):
    for retu in range(len(out[gyou])):
        if(out[gyou][retu]==0):
            out[gyou][retu]=''
        else:
            out[gyou][retu]=str(out[gyou][retu])

for gyou in out:
    print(','.join(gyou))

# 出力されたデータをコピペしてExcelに貼り付け
# そのままだとうまく貼れない場合があるので、「データ」タブの「区切り位置」をクリック、区切り文字にカンマを追加する
# 詳しくはこれ→https://poweraddress.jp/ref/csv-header/