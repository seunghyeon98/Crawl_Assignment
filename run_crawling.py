import pandas as pd
from tqdm import tqdm
import re
import requests
from bs4 import BeautifulSoup
import time

# 모든 href 태그 수집
def fetch_links(main_url: str, headers: dict)-> list[str]:
    response = requests.get(main_url, headers=headers)

    href_url_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            sub_url = link['href']
            if len(sub_url) != 0 and ('http' not in sub_url):
                href_url_list.append(sub_url)

    return href_url_list


# href 태그에 대한 모든 text 데이터 수집
def crawl_text(main_url: str, languages: list[str], href_url_list: list[str])-> pd.DataFrame:
    crawled_data_list = []

    for language in tqdm(languages):
        for sub_url in href_url_list:
            source_url = main_url + ('/' + language if language != 'en-US' else '') + sub_url

            try:
                response = requests.get(source_url, timeout=10)
                time.sleep(3)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    crawl_text = soup.get_text()

            except requests.RequestException:
                crawl_text = None

            crawled_data_list.append({'language': language, 'source_url': source_url, 'text': crawl_text})

    return pd.DataFrame(crawled_data_list)


# 수집한 데이터 전처리
def process_text(text: str)-> list[str]:
    fixed_text = re.sub(r"\t", "", text)
    splited_text = fixed_text.split('\n')
    drop_not_text = [elm for elm in splited_text if len(elm) != 0]
    drop_space_text = [item.strip() for item in drop_not_text if item.strip()]

    return drop_space_text


# 저장.
def save_to_file(file_path: str, text_list: list[str]):
    with open(file_path, 'w', encoding='utf-8') as file:
        for sentence in text_list:
            file.write(sentence + "\n")


def main():
    main_url = 'https://www.rust-lang.org'
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}
    # languages = ['en-US', 'es']
    languages = ['en-US','es','fr','it','ja','pt-BR','ru','tr','zh-CN','zh-TW']


    href_url_list = fetch_links(main_url, headers)
    crawled_temp = crawl_text(main_url, languages, href_url_list)
    crawled_temp['prcsed_text'] = crawled_temp['text'].apply(lambda elm: process_text(elm) if elm is not None else None)
    drop_crawled_temp = crawled_temp.dropna(subset=['prcsed_text'])

    for language in languages:
        temp = drop_crawled_temp[drop_crawled_temp['language'] == language]['prcsed_text']
        text_list = [elm for sublist in temp for elm in sublist]
        file_path = f'./resource/{language}.txt'
        save_to_file(file_path, text_list)

    print('success')


if __name__ == "__main__":
    main()