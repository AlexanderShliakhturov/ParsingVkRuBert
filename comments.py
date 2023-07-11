import requests
import transformers
from transformers import pipeline
import torch
import seaborn as sns
import matplotlib.pyplot as plt

url ='https://vk.com/wall-55516315_787108'

#Получаем массив из словарей, где каждый словарь - комментарий, текст комментария в значении ключа 'text'
def get_post_comments(url, count, offset):
    owner_id = int(url.split('wall')[1].split('_')[0])
    post_id = int(url.split('wall')[1].split('_')[1])
    version = 5.131
    access_token = '2fbfb12f2fbfb12f2fbfb12f722cab7cae22fbf2fbfb12f4b1ca480bb0e53066c73f1d9'
    comments_request = (f"https://api.vk.com/method/wall.getComments?owner_id={owner_id}&post_id={post_id}&count={count}&access_token={access_token}&v={version}")
    params = {'owner_id': owner_id,
              'post_id': post_id,
              'count': count,
              'access_token': access_token,
              'v': version,
              'sort': 'desc',
              'offset': offset
              }
    response = requests.get('https://api.vk.com/method/wall.getComments', params = params )
    if response.status_code == 200:
        data = response.json()['response']['items']
        return data
    else:
        print('Произошла ошибка при запросе комментариев')
        return []
#Пополняем массив словарей всеми комментариями, меняя offset, а дальше создаем массив "comment_list" только из текстов
def get_comments_list(url):
    count = 100
    offset = 0
    all_comments = []
    while True:
        comments = get_post_comments(url, count, offset)
        all_comments.extend(comments)
        if len(comments) < count:
            break
        offset += count
    #print(len(all_comments))

    comments_list = []
    for elem in all_comments:
        if len(elem.get('text')) != 0:
            comments_list.append(elem.get('text'))
        #print(elem.get('text')+'\n')
    return comments_list
#Скармливаем модели массив "comment list", получаем массив "for histogram", где 1 - позитивный, 2 - негативный, 0 - нейтральный.
def ml(comments_list):
    pos_count = neg_count = neutral_count = 0
    all_list = []
    pos_list = []
    neg_list = []
    neutral_list = []
    clf = pipeline(
        task = 'sentiment-analysis',
        model = 'blanchefort/rubert-base-cased-sentiment-rusentiment')
    for_histogram_012 = []
    for item in comments_list:
        sentiment_dict = clf(item)[0]
        sentiment_dict['text'] = item
        if sentiment_dict.get('label') == 'POSITIVE':
            for_histogram_012.append(1)
            pos_count +=1
            pos_list.append(sentiment_dict.get('text'))
        elif sentiment_dict.get('label') == 'NEGATIVE':
            for_histogram_012.append(2)
            neg_count += 1
            neg_list.append(sentiment_dict.get('text'))
        else:
            for_histogram_012.append(0)
            neutral_count += 1
            neutral_list.append(sentiment_dict.get('text'))
        #print(sentiment_dict)
        all_list.append(sentiment_dict.get('text'))
    for_histogram_number = {'Positive': pos_count, 'Negative': neg_count, 'Neutral': neutral_count}
    #print(for_histogram_012, for_histogram_number)
    return for_histogram_number, pos_list, neg_list, neutral_list, all_list
#Строим визуализацию количества различных отзывов
def visual(for_histogram_number):
    data = for_histogram_number
    plt.hist(data)
    plt.show()

def get_pos_comments(url):
    list = get_comments_list(url)
    pos_list = ml(list)[1]
    return pos_list

def get_neg_comments(url):
    list = get_comments_list(url)
    neg_list = ml(list)[2]
    return neg_list

def get_neutral_comments(url):
    list = get_comments_list(url)
    neutral_list = ml(list)[3]
    return neutral_list

def get_all(url):
    list = get_comments_list(url)
    number_of_different_comments = ml(list)[0]
    return number_of_different_comments

def get_all_list(url):
    list = get_comments_list(url)
    all_list = ml(list)[4]
    return all_list

#get_neutral_comments(url)