import feedparser
import schedule
import time
import csv
from datetime import datetime

# 구글 뉴스 RSS 피드 URL (예시로 기술 뉴스 카테고리 사용)
RSS_FEED_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"

# CSV 파일 이름 설정
CSV_FILE = "news_feed.csv"

def fetch_news():
    print("Fetching news from Google News RSS...")
    feed = feedparser.parse(RSS_FEED_URL)
    
    # 중복된 제목을 확인하기 위해 기존에 저장된 제목을 불러옵니다.
    existing_titles = load_existing_titles()

    # CSV 파일에 저장하기 위해 뉴스 데이터를 수집
    news_items = []
    if feed.entries:
        print(f"Fetched {len(feed.entries)} news items.")
        for entry in feed.entries:
            title = entry.title
            # RSS 피드에서 게시 시간을 찾기 (없을 경우 현재 시간 사용)
            published_time = entry.published if 'published' in entry else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 중복된 뉴스 제목이 아닌 경우에만 추가
            if title not in existing_titles:
                news_items.append([title, published_time])
                print(f"Title: {title}")
                print(f"Time: {published_time}")
                print("-----")
            else:
                print(f"Duplicate found, skipping: {title}")
        
        # 중복이 아닌 뉴스만 CSV 파일에 저장
        if news_items:
            save_to_csv(news_items)
    else:
        print("No news found.")

def load_existing_titles():
    """CSV 파일에서 기존 뉴스 제목을 불러와 리스트로 반환합니다."""
    titles = set()
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 건너뛰기
            for row in reader:
                if row:  # 빈 행이 아닐 때
                    titles.add(row[0])  # 제목만 저장
    except FileNotFoundError:
        print("No existing CSV file found, starting fresh.")
    return titles

def save_to_csv(news_items):
    """뉴스 항목을 CSV 파일에 저장합니다."""
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in news_items:
            writer.writerow(item)
    print(f"Saved {len(news_items)} new items to {CSV_FILE}.")

# CSV 파일에 헤더 추가 (첫 실행 시)
def initialize_csv():
    """CSV 파일을 초기화하고 헤더를 추가합니다."""
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Time"])  # 헤더 작성
    print(f"Initialized {CSV_FILE} with headers.")

def crawling():
    # CSV 초기화 (첫 실행 시 헤더 추가)
    initialize_csv()

    # 30분마다 fetch_news 함수 실행
    schedule.every(30).minutes.do(fetch_news)

    # 프로그램 지속 실행
    print("Starting scheduled task...")
    fetch_news()  # 처음 시작할 때 즉시 실행

    while True:
        schedule.run_pending()  # 스케줄된 작업 실행
        time.sleep(1)           # 1초 대기
