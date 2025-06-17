import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import json

def fetch_bbc_news():
    topics = {
        'https://www.bbc.co.uk/news/topics/c302m85q5ljt': 'Gaza',
        'https://www.bbc.co.uk/news/topics/c8nq32jw5r5t': 'Israel', 
        'https://www.bbc.co.uk/news/topics/c207p54m4rqt': 'Palestine',
        'https://www.bbc.co.uk/news/topics/cjnwl8q4ggnt': 'Middle East',
        'https://www.bbc.co.uk/news/topics/cxvmk3z8mn9t': 'West Bank',
        'https://www.bbc.co.uk/news/topics/cnx753jen5zt': 'Hamas',
        'https://www.bbc.co.uk/news/topics/c8nq32jwj2lt': 'Hezbollah'
    }

    articles = []
    seen_urls = set()
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }

    for base_url, topic in topics.items():
        page = 1
        while True:
            try:
                time.sleep(random.uniform(2, 4))
                
                # Try to fetch JSON data first
                json_url = f"{base_url}/more?page={page}"
                json_response = session.get(json_url, headers=headers)
                
                if json_response.status_code == 200:
                    try:
                        data = json_response.json()
                        items = data.get('items', [])
                        if not items:
                            break
                            
                        for item in items:
                            article_url = f"https://www.bbc.co.uk{item['url']}"
                            if article_url in seen_urls:
                                continue
                                
                            time.sleep(random.uniform(1, 2))
                            article_response = session.get(article_url, headers=headers)
                            article_soup = BeautifulSoup(article_response.text, 'html.parser')
                            
                            date_elem = article_soup.find('time', {'datetime': True})
                            if not date_elem:
                                continue

                            date = datetime.fromisoformat(date_elem['datetime'].replace('Z', '+00:00'))
                            if date.date() < datetime(2023, 10, 7).date():
                                continue

                            content_blocks = article_soup.select('[data-component="text-block"], article p')
                            full_text = ' '.join(block.get_text(strip=True) for block in content_blocks if block.get_text(strip=True))
                            
                            if full_text:
                                articles.append({
                                    'date': date,
                                    'title': item.get('title', ''),
                                    'link': article_url,
                                    'content': full_text,
                                    'topic_page': topic
                                })
                                seen_urls.add(article_url)
                                print(f"Scraped ({topic}): {item.get('title', '')}")
                                
                    except json.JSONDecodeError:
                        pass
                
                # Fallback to HTML scraping
                url = f"{base_url}?page={page}"
                response = session.get(url, headers=headers)
                
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                articles_found = False

                promos = soup.select('a[href*="/news/"]')
                if not promos:
                    break

                for link in promos:
                    try:
                        if not link.get('href'):
                            continue

                        article_url = 'https://www.bbc.co.uk' + link['href'] if link['href'].startswith('/') else link['href']
                        if article_url in seen_urls or '/topics/' in article_url:
                            continue

                        time.sleep(random.uniform(1, 2))
                        article_response = session.get(article_url, headers=headers)
                        if article_response.status_code != 200:
                            continue

                        article_soup = BeautifulSoup(article_response.text, 'html.parser')
                        date_elem = article_soup.find('time', {'datetime': True})
                        if not date_elem:
                            continue

                        date = datetime.fromisoformat(date_elem['datetime'].replace('Z', '+00:00'))
                        if date.date() < datetime(2023, 10, 7).date():
                            continue

                        content_blocks = article_soup.select('[data-component="text-block"], article p')
                        full_text = ' '.join(block.get_text(strip=True) for block in content_blocks if block.get_text(strip=True))
                        
                        title = article_soup.find('h1')
                        if full_text and title:
                            articles.append({
                                'date': date,
                                'title': title.get_text(strip=True),
                                'link': article_url,
                                'content': full_text,
                                'topic_page': topic
                            })
                            seen_urls.add(article_url)
                            articles_found = True
                            print(f"Scraped ({topic}): {title.get_text(strip=True)}")

                    except Exception as e:
                        print(f"Error processing article: {str(e)}")
                        continue

                if not articles_found:
                    break

                page += 1

            except Exception as e:
                print(f"Error processing page {page} for {topic}: {str(e)}")
                break

    df = pd.DataFrame(articles)
    if not df.empty:
        df = df.sort_values('date', ascending=False)
        df.to_csv('bbc_articles_3.csv', index=False)
        print(f"\nSaved {len(df)} articles to bbc_articles.csv")
        print(f"\nArticles by topic:")
        print(df['topic_page'].value_counts())
    else:
        print("No articles found")
    return df

if __name__ == "__main__":
    articles_df = fetch_bbc_news()