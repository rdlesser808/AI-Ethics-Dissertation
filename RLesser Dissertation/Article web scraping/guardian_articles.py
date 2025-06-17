import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

all_articles = []  

def fetch_guardian_news(max_pages_per_topic=10):
    topics = {
        'world/gaza': 'Gaza',
        'world/israel': 'Israel',
        'world/palestinian-territories': 'Palestine',
        'world/middleeast': 'Middle East',
        'world/west-bank': 'West Bank',
        'world/hamas': 'Hamas',
        'world/hezbollah': 'Hezbollah'
    }

    seen_urls = set()
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    for topic_path, topic in topics.items():
        page = 1
        consecutive_duplicate_pages = 0
        
        while page <= max_pages_per_topic:
            try:
                time.sleep(random.uniform(1, 2))
                
                url = f"https://www.theguardian.com/{topic_path}"
                if page > 1:
                    url += f"?page={page}"
                    
                print(f"\nChecking {topic} - Page {page}")
                response = session.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get all article links on the page
                new_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if '/20' in href and not any(x in href for x in ['/live/', '/video/', '/picture/', '.pdf']):
                        full_url = f"https://www.theguardian.com{href}" if not href.startswith('http') else href
                        if full_url not in seen_urls:
                            new_links.append(full_url)
                            seen_urls.add(full_url)
                
                if not new_links:
                    print(f"No new articles found on page {page} for {topic}")
                    consecutive_duplicate_pages += 1
                    if consecutive_duplicate_pages >= 2:
                        print(f"No new content found for {topic} after {page} pages")
                        break
                    page += 1
                    continue
                
                print(f"Found {len(new_links)} new links to check")
                consecutive_duplicate_pages = 0

                for article_url in new_links:
                    try:
                        article_response = session.get(article_url)
                        article_soup = BeautifulSoup(article_response.text, 'html.parser')

                        # Get date from meta tag
                        date_meta = article_soup.find('meta', property='article:published_time')
                        if not date_meta:
                            print("  Skipping - no date found")
                            continue
                            
                        date = datetime.fromisoformat(date_meta['content'].replace('Z', '+00:00'))
                        if date.date() < datetime(2023, 10, 7).date():
                            print("  Skipping - before Oct 7")
                            continue

                        # Get content using the correct class
                        content_div = article_soup.find('div', class_='article-body-commercial-selector')
                        if not content_div:
                            print("  Skipping - no content found")
                            continue
                            
                        content_blocks = content_div.find_all('p')
                        full_text = ' '.join(block.get_text(strip=True) for block in content_blocks if block.get_text(strip=True))
                        
                        # Get title
                        title = article_soup.find('h1')
                        
                        if full_text and title and len(full_text) > 200:
                            article_data = {
                                'date': date,
                                'title': title.get_text(strip=True),
                                'link': article_url,
                                'content': full_text,
                                'topic_page': topic
                            }
                            all_articles.append(article_data)
                            print(f"  Scraped: {title.get_text(strip=True)}")
                        else:
                            print("  Skipping - insufficient content")
                            
                        time.sleep(random.uniform(1, 2))
                        
                    except Exception as e:
                        print(f"  Error processing article {article_url}: {str(e)}")
                        continue

                print(f"Total articles collected so far: {len(all_articles)}")
                page += 1

            except Exception as e:
                print(f"Error on page {page} for {topic}: {str(e)}")
                break

        print(f"\nCompleted topic: {topic}")
        print(f"Current article count: {len(all_articles)}")

    # Create DataFrame from all collected articles
    df = pd.DataFrame(all_articles)
    if not df.empty:
        # Remove any duplicate articles based on URL
        df = df.drop_duplicates(subset='link')
        df = df.sort_values('date', ascending=False)
        df.to_csv('guardian_articles.csv', index=False)
        print(f"\nSaved {len(df)} unique articles")
        print("\nArticles by topic:")
        print(df['topic_page'].value_counts())
        return df
    else:
        print("No articles found")
        return None

if __name__ == "__main__":
    articles_df = fetch_guardian_news()