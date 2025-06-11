import db 
from feed_scrapper import feed_scrapper
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

if __name__ == "__main__":

    urls = [
        {"MIT News": "https://news.mit.edu/rss/topic/artificial-intelligence2"},
        {"Wired":"https://www.wired.com/feed/tag/ai/latest/rss"},
        {"KnowTechie":"https://knowtechie.com/category/ai/feed/"},
        {"AI News":"https://www.artificialintelligence-news.com/feed/rss/"},
        {"Science Daily":"https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml"},
        
    ]
    entries = []

    for feed in urls:
        for source_name, feed_url in feed.items():
            articles = feed_scrapper(source_name, feed_url)
            entries.extend(articles)

    for entry in entries:
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(entry['title'])
        entry.update(sentiment)

    conn = db.connect_db()
    db.create_table(conn)
    db.insert_articles(conn,entries)
    db.close_db(conn)
    