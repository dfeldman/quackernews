import json
import urllib.request
from bs4 import BeautifulSoup

def fetch_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except:
        return None


def parse_story(story):
    title = story.find('span', class_='titleline').text.strip()
    link = story.find('span', class_='titleline').find('a').get('href')
    
      
    score = story.find_next_sibling('tr').find('td', class_='subtext').find('span', class_='score')
    points = int(score.text.split()[0]) if score else 0
    
    submitter_info = story.find_next_sibling('tr').find('td', class_='subtext')
    submitter = submitter_info.find('a', class_='hnuser').text if submitter_info else ''
    submit_time = submitter_info.find('span', class_='age').get('title') if submitter_info else ''
    
    comments_link = submitter_info.find('a', string=lambda text: isinstance(text, str) and 'comments' in text)
    num_comments = 0
    comments_url = ''
    if comments_link:
        num_comments = int(comments_link.text.split()[0])
        comments_url = f"https://news.ycombinator.com/{comments_link.get('href')}"

    story_data = {
        'title': title,
        'points': points,
        'submitter': submitter,
        'submit_time': submit_time,
        'num_comments': num_comments,
        'comments_url': comments_url,
        'comments': [],
        'link': link,
        'first_paragraph': ''
    }
    
    if link and not link.startswith('item?id=') and not link.endswith('pdf'):
        article_html = fetch_url(link)
        if article_html:
            article_soup = BeautifulSoup(article_html, 'html.parser')
            paragraphs = article_soup.find_all('p')
            if paragraphs:
                story_data['first_paragraph'] = paragraphs[0].text.strip()[:1000]

    if comments_url:
        comments_html = fetch_url(comments_url)
        if comments_html:
            comments_soup = BeautifulSoup(comments_html, 'html.parser')
            top_level_comments = comments_soup.select('tr.athing.comtr > td > table > tr > td.default > div.comment > span.commtext')
            story_data['comments'] = [comment.text.strip() for comment in top_level_comments[:10]]
    
    return story_data


def main(num_stories):
    url = 'https://news.ycombinator.com/'
    html = fetch_url(url)
    
    if not html:
        print("Failed to fetch Hacker News.")
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    stories = soup.find_all('tr', class_='athing')
    
    data = []
    for story in stories[:num_stories]:
        print(story)
        story_data = parse_story(story)
        if story_data['link']:
            data.append(story_data)
    
    with open('output/output.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully generated output.json with {len(data)} stories.")

if __name__ == '__main__':
    num_stories = 10
    main(num_stories)