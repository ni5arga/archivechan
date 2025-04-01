import os
import tweepy
import json
from datetime import datetime

def archive_twitter_thread(tweet_url, output_dir='twitter_archive'):
    """Archive a Twitter thread and its replies"""
    
    auth = tweepy.OAuthHandler('YOUR_CONSUMER_KEY', 'YOUR_CONSUMER_SECRET')
    auth.set_access_token('YOUR_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN_SECRET')
    api = tweepy.API(auth)
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        tweet_id = tweet_url.split('/')[-1].split('?')[0]
        
        main_tweet = api.get_status(tweet_id, tweet_mode='extended')
        
        replies = []
        for tweet in tweepy.Cursor(api.search_tweets, q=f"to:{main_tweet.user.screen_name}", 
                                 since_id=main_tweet.id, tweet_mode='extended').items():
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if tweet.in_reply_to_status_id_str == main_tweet.id_str:
                    replies.append(tweet)
        
        thread_data = {
            'main_tweet': {
                'id': main_tweet.id_str,
                'created_at': str(main_tweet.created_at),
                'user': main_tweet.user.screen_name,
                'text': main_tweet.full_text,
                'likes': main_tweet.favorite_count,
                'retweets': main_tweet.retweet_count,
                'url': f"https://twitter.com/{main_tweet.user.screen_name}/status/{main_tweet.id}"
            },
            'replies': [
                {
                    'id': tweet.id_str,
                    'created_at': str(tweet.created_at),
                    'user': tweet.user.screen_name,
                    'text': tweet.full_text,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                } for tweet in replies
            ]
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"thread_{main_tweet.id}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(thread_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully archived thread with {len(replies)} replies to {filepath}")
        return filepath
    
    except Exception as e:
        print(f"Failed to archive Twitter thread: {str(e)}")
        return None

if __name__ == "__main__":
    url = input("Enter Twitter thread URL: ")
    archive_twitter_thread(url)
