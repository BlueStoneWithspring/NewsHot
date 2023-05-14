from utils.util_news import write_news_json
from pathlib import Path
from utils.util_news import read_news_json
from utils.util_tencent_news import get_tencent_hot_ranking_list
from enum import Enum
import time
import os
import config
import dataclasses
from chatgpt_api import chatGpt
from utils.class_news import News
from typing import Optional


class NewsSource(Enum):
    TENCENT = 'tencent'


def summarize_news_with_gpt(
        news: News,
        retry_times: int = 3,
        delay: float = 25,
) -> Optional[News]:
    content = news.content
    _SUMMARIZE_QUESTION_FMT = '请为以下新闻写一篇100字以内、不含标题的中文摘要：\n\n《{title}》\n{content}'
    prompt=_SUMMARIZE_QUESTION_FMT.format(
        title=news.title,
        content=content,
    )
    response = chatGpt(prompt)
    news_with_summary = dataclasses.replace(news)
    news_with_summary.brief_content = response['choices'][0]['message']['content']
    return news_with_summary


def summarize_news(news_json: str):
    news_json_path = Path(news_json)
    news_list_without_summary = read_news_json(news_json_path)
    print(news_list_without_summary)
    news_list = []
    # init_openai(_CONFIG['openai_api_key'], _CONFIG['openai_proxy'])
    for news in news_list_without_summary:
        news_with_summary = summarize_news_with_gpt(news=news)
        if news_with_summary:
            news_list.append(news_with_summary)
    write_news_json(news_list, news_json_path)
    news_json_text = news_json_path.read_text(encoding='utf-8')
    return news_json_text


def fetch_news(news_json: str, image_dir: str, news_num: int = 20, source: str = 'tencent'):
    news_json_path = Path(news_json)
    news_json_path.parent.mkdir(parents=True, exist_ok=True)
    image_dir_path = Path(image_dir)
    image_dir_path.mkdir(parents=True, exist_ok=True)
    if source == NewsSource.TENCENT.value:
        news_list = get_tencent_hot_ranking_list(news_num=news_num, image_dir_path=image_dir_path)
    else:
        raise ValueError('Unknown news source {}'.format(source))
    write_news_json(news_list, news_json_path)


def newsGenerator():
    today = time.time()
    dir_path = os.path.join(config.dirpath, str(today))
    image_dir_path = os.path.join(dir_path, "IMAGES")
    news_json_path = os.path.join(dir_path, "news.json")

    fetch_news(news_json_path, image_dir_path, 1)
    all_news = summarize_news(news_json_path)
    newstxt = ""
    for n, news in enumerate(eval(all_news)):
        newstxt += "<p>【热搜{}】：".format(n+1)+'<strong>{}</strong></p>'.format(news["title"])\
                   + "<p>{}</p>".format(news["brief_content"])
    return newstxt.strip().replace("\n", "</br>")


if __name__ == '__main__':
    newsGenerator()

