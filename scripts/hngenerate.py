import json
from urllib.parse import urlparse
import os
import datetime

def generate_html(data):
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quacker News</title>
    <style>
        body { font-family: Verdana, Geneva, sans-serif; font-size: 14pt; color: #828282; background-color: #f0e6ff; }
        td { font-family: Verdana, Geneva, sans-serif; font-size: 14pt; color: #828282; padding-right: 20px;}
        .title { font-family: Verdana, Geneva, sans-serif; font-size: 14pt; color: #828282; overflow: hidden; padding-top:10px; }
        .subtext { font-family: Verdana, Geneva, sans-serif; font-size: 10pt; color: #828282; padding-top: 5px; }
        .titlelink { color: #000000; text-decoration: none; }
        .titlelink:visited { color: #828282; text-decoration: none; }
        .summary { font-family: Verdana, Geneva, sans-serif; font-size: 12pt; color: #828282; padding: 10px; text-indent: none; padding-right: 10px; padding: 20px; }
        .summarylink { color: #828282; text-decoration: none; }
        .summarylink:visited { color: #828282; text-decoration: none; }
        .morelink { color: white; text-decoration: none; font-size: 14pt; margin-top:20px; margin-bottom: 20px; }
        .morelink:visited { color: white; text-decoration: none; }
    </style>
</head>
<body>
    <center>
        <table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef" style="padding:0px">
            <tr>
                <td bgcolor="#800080">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px">
                        <tr>
                            <td style="width:18px;padding:10px; padding-left: 12px; padding-right: 12px;">
                                <a href="#" style="color: white; text-decoration: none;">🦆</a>
                            </td>
                            <td style="line-height:12pt; height:10px;">
                                <span class="pagetop" style="color: white;">
                                    <b class="hnname"><a href="#" style="color: white;">Quacker News</a></b>
                                    <a href="#" style="color: white;">new</a> | <a href="#" style="color: white;">past</a> | <a href="#" style="color: white;">comments</a> | <a href="#" style="color: white;">ask</a> | <a href="#" style="color: white;">show</a> | <a href="#" style="color: white;">jobs</a> | <a href="#" style="color: white;">submit</a>
                                </span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr id="pagespace" title="" style="height:10px"></tr>
            <tr>
                <td>
                    <table border="0" cellpadding="0" cellspacing="0">
    '''

    for i, story in enumerate(data, start=1):
        domain = urlparse(story["link"]).netloc
        summary = story["summary"].replace('\n', '<br>')
        html += f'''
                        <tr class='athing' id='story-{i}' >
                            <td align="right" valign="top" class="title" style="padding: 10px"><span class="rank">{i}.</span></td>
                            <td></td>
                            <td class="title">
                                <span class="titleline">
                                    <span class="votelinks">▲</span><a href="{story["link"]}" class="titlelink">  {story["title"]}</a>
                                    <span class="sitebit comhead"> ({domain})</span>
                                </span>
                                <br>
                                <span class="summary">
                                    <a href="{story["link"]}" class="summarylink">{summary}</a>
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2"></td>
                            <td class="subtext">
                                <span class="score">{story["points"]} points</span> by <a href="#">{story["submitter"]}</a> 
                                <span class="age" title="{story["submit_time"]}">{story["submit_time"]}</span> |
                                <a href="{story["comments_url"]}">{story["num_comments"]} comments</a>
                            </td>
                        </tr>
                        <tr class="spacer" style="height:5px"></tr>
        '''

    html += '''
                    </table>
                </td>
            </tr>
            <tr>
                <td>
                    <table width="100%" cellspacing="0" cellpadding="4" style="margin-top:50px">
                        <tr>
                            <td bgcolor="#800080">
                                <a href="history.html" class="morelink">More</a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>
    '''

    return html

def generate_history_html(history_files):
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quacker News History</title>
    <style>
        body { font-family: Verdana, Geneva, sans-serif; font-size: 14pt; color: #828282; background-color: #f0e6ff; }
        .history-link { color: #828282; text-decoration: none; }
        .history-link:visited { color: #828282; text-decoration: none; }
    </style>
</head>
<body>
    <center>
        <h1>Quacker News History</h1>
        <ul>
'''
    for file in history_files:
        html += f'            <li><a href="{file}" class="history-link">{file}</a></li>\n'
    html += '''
        </ul>
    </center>
</body>
</html>
'''
    return html

if __name__ == '__main__':
    with open('output/output2.json', 'r') as f:
        data = json.load(f)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    output_file = f'output-{current_date}.html'
    index_file = 'index.html'
    history_file = 'history.html'

    html = generate_html(data)

    with open(output_file, 'w') as f:
        f.write(html)

    with open(index_file, 'w') as f:
        f.write(html)

    history_files = [file for file in os.listdir() if file.startswith('output-') and file.endswith('.html')]
    history_files.sort(reverse=True)

    history_html = generate_history_html(history_files)

    with open(history_file, 'w') as f:
        f.write(history_html)

    print(f"Successfully generated {output_file}, {index_file}, and {history_file}")
