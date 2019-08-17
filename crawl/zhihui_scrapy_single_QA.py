import requests
from bs4 import BeautifulSoup
import json
import re
REG = re.compile('<[^>]*>')


def extract_answer(s):
    temp_list = REG.sub("", s).replace("\n", "").replace(" ","")
    return temp_list


headers = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://www.zhihu.com',
    'referer': 'https://www.zhihu.com/question/290268306',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

start_url = 'https://www.zhihu.com/api/v4/questions/268384579/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&sort_by=default'

next_url = [start_url]
answers = []
for url in next_url:
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, "lxml")
    content = str(soup.p).split("<p>")[1].split("</p>")[0]
    c = json.loads(content)
    answers += [extract_answer(item["content"]) for item in c["data"] if extract_answer(item["content"]) != ""]
    next_url.append(c["paging"]["next"])
    if c["paging"]["is_end"]:
        break
for item in answers:
    print(item)
print(len(answers))