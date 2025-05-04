import re
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL or video ID not found.")

def analyze_sentiment(comment):
    """Analyze sentiment of a comment using VADER."""
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(comment)
    compound = score['compound']
    if compound >= 0.05:
        return 'Positive', compound
    elif compound <= -0.05:
        return 'Negative', compound
    else:
        return 'Neutral', compound

def create_output_folder(folder_name):
    """Create a folder for output files if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def scrape_youtube_comments(api_key, video_url, max_data, search_terms=None, title=None, fetch_replies=False, visualize=False):
    """Scrape YouTube comments with optional replies, sentiment analysis, and visualization."""
    try:
        # Initialize YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Extract video ID from URL
        video_id = extract_video_id(video_url)
        
        # List to store comments and replies
        data = []
        next_page_token = None
        total_collected = 0

        print(f"Scraping comments for video: {video_url}")
        
        # Loop to fetch comments (handles pagination)
        while total_collected < max_data:
            request = youtube.commentThreads().list(
                part="snippet,replies" if fetch_replies else "snippet",
                videoId=video_id,
                maxResults=min(100, max_data - total_collected),
                pageToken=next_page_token,
                searchTerms=search_terms if search_terms else ''
            )
            response = request.execute()
            
            # Process each comment thread
            for item in response['items']:
                # Process top-level comment
                snippet = item['snippet']['topLevelComment']['snippet']
                comment_text = snippet['textDisplay']
                sentiment, score = analyze_sentiment(comment_text)
                comment_data = {
                    'Type': 'Comment',
                    'Comment': comment_text,
                    'Author': snippet['authorDisplayName'],
                    'Published At': snippet['publishedAt'],
                    'Like Count': snippet['likeCount'],
                    'Sentiment': sentiment,
                    'Sentiment Score': score
                }
                data.append(comment_data)
                total_collected += 1
                
                # Process replies if enabled and available
                if fetch_replies and 'replies' in item and total_collected < max_data:
                    for reply in item['replies']['comments']:
                        reply_snippet = reply['snippet']
                        reply_text = reply_snippet['textDisplay']
                        reply_sentiment, reply_score = analyze_sentiment(reply_text)
                        reply_data = {
                            'Type': 'Reply',
                            'Comment': reply_text,
                            'Author': reply_snippet['authorDisplayName'],
                            'Published At': reply_snippet['publishedAt'],
                            'Like Count': reply_snippet['likeCount'],
                            'Sentiment': reply_sentiment,
                            'Sentiment Score': reply_score
                        }
                        data.append(reply_data)
                        total_collected += 1
                        
                        # Break if max_data is reached
                        if total_collected >= max_data:
                            break
                
                # Break if max_data is reached
                if total_collected >= max_data:
                    break
            
            # Check for next page
            next_page_token = response.get('nextPageToken')
            if not next_page_token or total_collected >= max_data:
                break
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Generate output folder and filename
        sanitized_title = video_id  # Default to video_id
        if title:
            # Sanitize title for folder and filename
            sanitized_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_').lower()
        
        folder_name = f"output_{sanitized_title}"
        base_name = f'youtube_comments_{sanitized_title}'
        
        # Create output folder
        output_folder = create_output_folder(folder_name)
        
        # Save CSV to output folder
        output_file = os.path.join(output_folder, f"{base_name}.csv")
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Successfully scraped {len(data)} comments{' and replies' if fetch_replies else ''}. Saved to {output_file}")
        
        # Visualize sentiment distribution as bar chart if enabled
        if visualize and not df.empty:
            sentiment_counts = df['Sentiment'].value_counts()
            plt.figure(figsize=(8, 6))
            sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
            plt.title('Sentiment Distribution of YouTube Comments')
            plt.xlabel('Sentiment')
            plt.ylabel('Number of Comments')
            plt.xticks(rotation=0)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            viz_file = os.path.join(output_folder, f"sentiment_distribution_{sanitized_title}.png")
            plt.savefig(viz_file, bbox_inches='tight')
            plt.close()
            print(f"Sentiment distribution saved to {viz_file}")
        
        return df
    
    except HttpError as e:
        error_reason = e.error_details[0]['reason'] if e.error_details else str(e)
        if error_reason == 'commentsDisabled':
            print("Error: Comments are disabled for this video.")
        elif error_reason == 'videoNotFound':
            print("Error: Video not found or invalid video ID.")
        else:
            print(f"Error: {error_reason}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # Load environment variables from .env file
    load_dotenv()
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    if not API_KEY:
        print("Error: YOUTUBE_API_KEY not found in .env file.")
        return
    
    # Get user inputs
    VIDEO_URL = input("Enter YouTube video URL: ")
    MAX_DATA = int(input("Enter maximum number of comments and replies to scrape: "))
    SEARCH_TERMS = input("Enter search terms to filter comments (optional, press Enter to skip): ")
    TITLE = input("Enter title for output file (optional, press Enter to use video ID): ")
    FETCH_REPLIES = input("Fetch comment replies? (y/N): ").strip().lower() == 'y'
    VISUALIZE = input("Generate sentiment visualization? (y/N): ").strip().lower() == 'y'
    
    # Run scraper
    scrape_youtube_comments(
        api_key=API_KEY,
        video_url=VIDEO_URL,
        max_data=MAX_DATA,
        search_terms=SEARCH_TERMS if SEARCH_TERMS else None,
        title=TITLE if TITLE else None,
        fetch_replies=FETCH_REPLIES,
        visualize=VISUALIZE
    )

if __name__ == "__main__":
    main()