import os
import praw
import json
from datetime import datetime

def archive_reddit_posts(subreddit_name, limit=100, output_dir='reddit_archive'):
    """Archive posts from a subreddit"""
    
    reddit = praw.Reddit(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        user_agent='ArchiveBot/1.0'
    )
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{subreddit_name}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        posts_data = []
        
        print(f"Archiving {limit} posts from r/{subreddit_name}...")
        
        for post in subreddit.hot(limit=limit):
            post_data = {
                'title': post.title,
                'author': str(post.author),
                'score': post.score,
                'url': post.url,
                'permalink': post.permalink,
                'created_utc': post.created_utc,
                'num_comments': post.num_comments,
                'selftext': post.selftext,
                'is_original_content': post.is_original_content,
                'over_18': post.over_18,
                'spoiler': post.spoiler
            }
            posts_data.append(post_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully archived {len(posts_data)} posts to {filepath}")
        return filepath
    
    except Exception as e:
        print(f"Failed to archive subreddit: {str(e)}")
        return None

if __name__ == "__main__":
    subreddit = input("Enter subreddit name to archive: ")
    limit = int(input("Number of posts to archive (default 100): ") or 100)
    archive_reddit_posts(subreddit, limit)
