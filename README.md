YouTube Comment Scraper
A Python script to scrape comments (and optionally replies) from a YouTube video using the YouTube Data API v3. The script performs sentiment analysis on comments using VADER and generates a bar chart visualization of sentiment distribution. Results are saved as a CSV file, and visualizations (if enabled) are saved as PNG files, all stored in a dedicated output folder.
Features

Scrape main comments and optionally replies from a YouTube video.
Filter comments by search terms (optional).
Perform sentiment analysis (Positive, Negative, Neutral) using VADER.
Generate a bar chart of sentiment distribution (optional).
Save results in a CSV file and visualization in a PNG file within a named output folder.
Load API key securely from a .env file.
User-defined output file naming with a custom title or video ID.

Prerequisites

Python 3.x installed.
YouTube Data API Key:
Create a project in Google Cloud Console.
Enable YouTube Data API v3.
Generate an API key in the Credentials section.

Required Python Libraries:google-api-python-client
pandas
vaderSentiment
matplotlib
python-dotenv

Installation

Clone or Download the Repository (if using Git):
git clone <repository-url>
cd youtube_comment_scraper

Or download the script files manually to a folder (e.g., D:\DEVELOPMENT\PYTHON\tools\youtube_comment_scraper).

Install Dependencies:Run the following command to install required libraries:
pip install google-api-python-client pandas vaderSentiment matplotlib python-dotenv

Set Up the .env File:

Create a file named .env in the project directory.
Add your YouTube API key:YOUTUBE_API_KEY=your_actual_api_key_here

Replace your_actual_api_key_here with your API key.
Ensure .env is not shared publicly (it’s ignored by .gitignore).

Usage

Navigate to the Project Directory:
cd D:\DEVELOPMENT\PYTHON\tools\youtube_comment_scraper

Run the Script:
python main.py

Provide Inputs:

YouTube Video URL: Enter the URL of the video (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ).
Maximum Number of Comments and Replies: Enter the maximum number to scrape (e.g., 50).
Search Terms (optional): Enter keywords to filter comments (e.g., great) or press Enter to skip.
Output File Title (optional): Enter a title for the output folder and files (e.g., rick_astley_review) or press Enter to use the video ID.
Fetch Comment Replies: Enter y to include replies, or N (or Enter) for main comments only.
Generate Sentiment Visualization: Enter y to generate a bar chart, or N (or Enter) to skip.

Output:

A folder (e.g., output_rick_astley_review) will be created in the project directory, containing:
youtube_comments_rick_astley_review.csv: Comments, replies (if enabled), and sentiment analysis.
sentiment_distribution_rick_astley_review.png (if visualization is enabled): Bar chart of sentiment distribution.

Example CSV content:Type,Comment,Author,Published At,Like Count,Sentiment,Sentiment Score
Comment,"This is a great video!",User123,2023-10-01T12:00:00Z,15,Positive,0.6249
Reply,"Yeah, great song!",User456,2023-10-01T12:05:00Z,3,Positive,0.6588
Comment,"Not my favorite.",User789,2023-10-02T15:30:00Z,1,Negative,-0.4588

Example
Input:
Enter YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Enter maximum number of comments and replies to scrape: 50
Enter search terms to filter comments (optional, press Enter to skip): great
Enter title for output file (optional, press Enter to use video ID): rick_astley_review
Fetch comment replies? (y/N): y
Generate sentiment visualization? (y/N): y

Output:

Folder: output_rick_astley_review
youtube_comments_rick_astley_review.csv
sentiment_distribution_rick_astley_review.png (bar chart)

Terminal:Scraping comments for video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Successfully scraped 50 comments and replies. Saved to output_rick_astley_review/youtube_comments_rick_astley_review.csv
Sentiment distribution saved to output_rick_astley_review/sentiment_distribution_rick_astley_review.png

Notes

API Quota: Each commentThreads.list request consumes 1 unit of the YouTube Data API quota (default 10,000 units/day). Fetching replies increases quota usage. Check quota in Google Cloud Console if errors occur.
Sentiment Analysis: VADER is optimized for English. For Indonesian comments, consider using a model like IndoBERT.
Security: Do not share your .env file or API key. The .gitignore file ensures .env is not uploaded to Git.
Output Files: Use unique titles to avoid overwriting existing output folders.
Dependencies: Ensure all libraries are installed to avoid ModuleNotFoundError.

Troubleshooting

IndentationError:
Open main.py in an editor (e.g., VS Code) and ensure all indentation uses 4 spaces (not tabs).
Enable "Show Whitespace" to verify.

YOUTUBE_API_KEY not found:
Ensure .env exists in the project directory with YOUTUBE_API_KEY=your_key.
Check for typos or extra spaces in .env.

API Errors:
Verify the API key is valid and YouTube Data API v3 is enabled.
Check for quota exhaustion in Google Cloud Console.

Visualization Issues:
Ensure matplotlib is installed (pip install matplotlib).
Check write permissions in the project directory.

License
This project is for personal use and complies with the YouTube Terms of Service. Ensure you have permission to scrape and analyze comments for your use case.
Contributing
Feel free to fork this repository, submit issues, or create pull requests to improve the script (e.g., adding Indonesian sentiment analysis, new visualizations, or advanced filters).
