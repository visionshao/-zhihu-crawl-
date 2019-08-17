"""
爬取知乎话题下的若干个话题下面的问题，做文本分类，预计一个话题爬10000个问题
1."accept-encoding": "gzip, deflate, br",会引起乱码
"""
from crawl.utils import *

temp_dict = {}
headers = {
    "authority": "www.zhihu.com",
    "method": "POST",
    "scheme": "https",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": '_zap=4b8fd0b0-5ece-4710-8a39-4690be3cc915; d_c0="ACDn4-HhLA-PTloTkzkSI1g9NSQ0UNbecnY=|1553490041"; _xsrf=iqWraCpzOAEVVHNZGwDfyaUPzBb7lkuI; z_c0="2|1:0|10:1553513989|4:z_c0|92:Mi4xTHpaZUJBQUFBQUFBSU9majRlRXNEeVlBQUFCZ0FsVk5CUXlHWFFCVjdwTFIwbjFVeXdZWmREdDVybTVvVWtVa0NR|e97ba19d5423a0bb2269441eb310b80853aaed3e4cfdcd555c5b4517e681824d"; __gads=ID=ef86bad0aef0dc13:T=1553514097:S=ALNI_MaIcscAZVawHrwdA_5OzAq3gGMLfg; __utmv=51854390.100-1|2=registration_date=20170314=1^3=entry_date=20170314=1; _ga=GA1.2.1820027566.1554478077; tst=r; q_c1=c09535e464704c7e8aa93032d032f507|1556906107000|1553490042000; __utma=51854390.1820027566.1554478077.1555816095.1556906108.7; __utmz=51854390.1556906108.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; tgw_l7_route=060f637cd101836814f6c53316f73463',
    "origin": "https://www.zhihu.com",
    "referer": "https://www.zhihu.com/topic",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrftoken": "iqWraCpzOAEVVHNZGwDfyaUPzBb7lkuI",
    "_xsrf":"697157726143707a4f41455656484e5a47774466796155507a4262376c6b7549"
}

lock = threading.Lock()
class SpiderTopic(threading.Thread):

    def __init__(self, topic_item):
        threading.Thread.__init__(self)
        self.item = topic_item

    def run(self):

        item = self.item
        print("The threading ",item[1],"has run!" )
        new_url = r'http://www.zhihu.com/api/v4/topics/' + item[
            0] + '/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=5'

        # print(new_url)
        if item[1] not in temp_dict:
            temp_dict[item[1]] = []
        while True:
            try:
                html = r.get(new_url, headers=headers)
                html.encoding = "utf8"
                data_list = html.json()['data']
                for data in data_list:
                    try:
                        q_name = data["target"]["question"]["title"]
                        lock.acquire()
                        if q_name not in temp_dict[item[1]]:
                            temp_dict[item[1]].append(q_name)
                            print(q_name)
                        lock.release()
                    except Exception as e:
                        pass
                        # print(e)
                tmp_url = html.json()["paging"]["next"]
                if tmp_url == new_url:
                    break
                else:
                    new_url = tmp_url
            except Exception as e:
                break


def get_topic_nodes():
    html = r.get(r'https://www.zhihu.com/topic', headers=headers)
    print(html.status_code)
    html.encoding = 'utf8'
    soup = BeautifulSoup(html.text, "html.parser")
    # 获取所有话题id
    topic_nodes = {(item["data-href"].split("/")[2], item.text)for item in soup.findAll("li", attrs={"class":"zm-topic-cat-item"})}
    return topic_nodes


if __name__ == '__main__':
    s1 = time.time()
    print(s1)
    topic_nodes = get_topic_nodes()
    threading_list = [SpiderTopic(item) for item in topic_nodes]
    for thread in threading_list:
        thread.start()
    for thread in threading_list:
        thread.join()
    s2 = time.time()
    print(s2-s1)
    file = open("crawl_01.csv", "w", encoding="utf8")
    for k, v in temp_dict.items():
        for item in v:
            file.write(k+"----"+item+"\n")
    s3 = time.time()
    print(s3-s1)
