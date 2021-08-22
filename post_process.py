import pandas as pd

data_path='test.csv'

data=pd.read_csv(data_path)
data.rename(columns={'0':'image_path','1':'车牌','2':'开始时间','3':'结束时间','4':'播放时间','5':'里程数1','6':'里程数2'},inplace=True)
# data.rename(columns={'0':'image_path'},inplace=True)
def judge(x):
    if(x['车牌']==x['车牌gt']):
        return "一致"
    else:
        return '不一致'

def judge_date(x):
    pred=x['播放时间'].split('-')
    pred=''.join(pred)
    if(pred==x['日期gt']):
        return "一致"
    else:
        return '不一致'

def merge_milestone(x):
    # print(x.columns)
    x1=x['里程数1']
    x2=x['里程数2']
    if('总里程' in x1):
        return x1
    else:
        return x2

print(data.columns)
data['播放时间']=data['播放时间'].apply(lambda x:x.replace('速度',""))
data['开始时间']=data['开始时间'].apply(lambda x:x[:-5])
data['IMEI']=data['车牌'].apply(lambda x:x.split(':')[1])
data['IMEI']=data['IMEI'].apply(lambda x:x.split(')')[0])
data['车牌']=data['车牌'].apply(lambda x:x.split('(')[0])

data['车牌gt']=data['image_path'].apply(lambda x:x.split('-')[-2])
data['日期gt']=data['image_path'].apply(lambda x:x.split('-')[-1])
data['日期gt']=data['日期gt'].apply(lambda x:x.split('.')[-2])

data['结束时间']=data['结束时间'].apply(lambda x:x[:-5])
data['播放时间']=data['播放时间'].apply(lambda x:x[:10])
data['里程数']=data.apply(lambda x:merge_milestone(x),axis=1)
data['车牌号是否一致']=data.apply(lambda x:judge(x),axis=1)
data['日期是否一致']=data.apply(lambda x:judge_date(x),axis=1)
data=data.drop(columns=['7','车牌gt','日期gt', '里程数1', '里程数2'])
# data.to_csv('test_process.csv',index=False)
data.to_excel('test_process.xlsx',index=False)

