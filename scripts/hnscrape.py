import json
import urllib.request
from bs4 import BeautifulSoup

def fetch_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except:
        return None

def to_text(el):
    if el is not None:
        return el.text
    else:
        return ''

def parse_story(story):
    title = story.find('span', class_='titleline').text.strip()
    link = story.find('span', class_='titleline').find('a').get('href')
    
      
    score = story.find_next_sibling('tr').find('td', class_='subtext').find('span', class_='score')
    points = int(score.text.split()[0]) if score else 0
    
    submitter_info = story.find_next_sibling('tr').find('td', class_='subtext')
    submitter = to_text(submitter_info.find('a', class_='hnuser')) if submitter_info else ''
    submit_time = submitter_info.find('span', class_='age').get('title') if submitter_info else ''
    
    comments_link = submitter_info.find('a', string=lambda text: isinstance(text, str) and 'comments' in text)
    num_comments = 0
    comments_url = ''
    if comments_link:
        num_comments = int(to_text(comments_link).split()[0])
        comments_url = f"https://news.ycombinator.com/{comments_link.get('href')}"

    story_data = {
        'title': title,
        'points': points,
        'submitter': submitter,
        'submit_time': submit_time,
        'num_comments': num_comments,
        'comments_url': comments_url,
        'comments': ['xxx'],
        'link': link,
        'first_paragraph': ''
    }
    
    if link and not link.startswith('item?id=') and not link.endswith('pdf'):
        article_html = fetch_url(link)
        if article_html:
            article_soup = BeautifulSoup(article_html, 'html.parser')
            paragraphs = article_soup.find_all('p')
            print("TEXT FROM ARTICLE", link)
            print(paragraphs[:20])
            #if paragraphs:
            story_data['first_paragraph'] = ''.join([to_text(p) for p in paragraphs[:100]])[:1000]
            print("STORING",story_data['first_paragraph'])

    if comments_url:
        comments_html = fetch_url(comments_url)
        if comments_html:
            soup = BeautifulSoup(comments_html, 'html.parser')

            # Try to find comments with different selectors
            selectors = [
                'tr.athing.comtr > td > table > tr > td.default > div.comment > span.commtext',
                'div.comment > span.commtext',
                'span.commtext',
                'div.comment'
            ]

            #print("No comments found with any selector")
            #print("COMMENTS_SOUP",comments_soup)
            top_level_comments = soup.select('div.comment')
            story_data['comments'] = [to_text(comment).strip() for comment in top_level_comments[:10]]
    
    return story_data


def main(num_stories):
    url = 'https://news.ycombinator.com/'
    html = fetch_url(url)
    
    if not html:
        print("Failed to fetch Hacker News.")
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    stories = soup.find_all('tr', class_='athing')
    print("parsing",len(stories),"stories") 
    data = []
    for story in stories[:num_stories]:
        try: 
            story_data = parse_story(story)
        except:
            # if we can't parse a story just skip it
            continue
        #if story_data['link']:
        data.append(story_data)
    
    with open('output/output.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully generated output.json with {len(data)} stories.")

if __name__ == '__main__':
    num_stories = 20
    main(num_stories)
