import requests
from bs4 import BeautifulSoup
import argparse
import sys

LETA_BASE_URL = "https://leta.mullvad.net/search"
SUPPORTED_ENGINES = ["brave", "google"]

def get_urls_from_leta(query: str, page: int, engine: str) -> list[str]:
    params = {
        "q": query,
        "engine": engine,
        "page": page
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(LETA_BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        urls = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('http://') or href.startswith('https://'):
                urls.append(href)
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URLs: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Leta Searcher",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "query",
        help="The search query. Example: python search.py 'my search terms'"
    )
    parser.add_argument(
        "-p", "--page",
        type=int,
        default=1,
        help="Page number for the search results (default: 1)."
    )
    parser.add_argument(
        "-e", "--engine",
        default="brave",
        choices=SUPPORTED_ENGINES,
        help=f"Search engine to use (choices: {', '.join(SUPPORTED_ENGINES)}; default: brave)."
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Leta Searcher 0.2.0",
        help="Show version number and exit."
    )

    args = parser.parse_args()

    current_query = args.query.replace(" ", "+")
    current_page = args.page
    current_engine = args.engine

    urls = get_urls_from_leta(current_query, current_page, current_engine)

    if urls:
        for i, url in enumerate(urls):
            print(f"{i+1}. {url}")
    else:
        print("No URLs found for this query/page, or an error occurred.", file=sys.stderr)

if __name__ == "__main__":
    main()
