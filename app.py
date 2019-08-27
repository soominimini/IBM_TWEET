import GetOldTweets3 as got
import datetime, time
from random import uniform
from tqdm import tqdm_notebook

#아래는 ibm API
# -*- coding: utf-8 -*-

#import personaliy insights
from builtins import print

from watson_developer_cloud import PersonalityInsightsV3
#from ibm_watson import PersonalityInsightsV3
import json
from openpyxl import load_workbook
import numpy as np

#아래는 시각화를 위한 라이브러리
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


url = 'https://gateway.watsonplatform.net/personality-insights/api'
apikey = '9aPTQUgHwV74s4gjD7zC4ZsCppop7j1-gNheGmW8S6UA'
service = PersonalityInsightsV3(url = url ,iam_apikey= apikey, version= '2017-10-13')



days_range = []

start = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2019-02-27", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))
#가져올 트위터의 날짜를 정해주어야 함
#나는 여기서 2019 01 01 부터 2019 08 27까지 크롤링을 함


# 수집 기간 맞추기
start_date = days_range[0]
end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
            + datetime.timedelta(days=1)).strftime("%Y-%m-%d") # setUntil이 끝을 포함하지 않으므로, day + 1


tweetCriteria = got.manager.TweetCriteria().setUsername("Oprah") \
                                            .setSince(start_date) \
                                            .setUntil(end_date) \
                                            .setMaxTweets(-1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)

print("Collecting data start.. from {} to {}".format(days_range[0], days_range[-1]))
start_time = time.time()


print("Collecting data end.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
print("=== Total num of tweets is {} ===".format(len(tweet)))

# initialize
tweet_list = ""

for i in range(len(tweet)):
    tweet_list+= tweet[i].text
#for index in tqdm_notebook(tweet):
 #   print(tweet[index])


# string 결과값 보내기
profile = service.profile(tweet_list, content_type='text/plain', content_language='ko',
                          consumption_preferences=True).get_result()

# 결과값 전체 다 가져오기
print(json.dumps(profile, indent=5))