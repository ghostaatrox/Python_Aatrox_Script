#http://ce.baidu.com/index/getRelatedSites?site_address=
#http://tool.chinaz.com/subdomain?domain=

#更新日志
# version=1.0.1 已解决去重问题，下一步解决链接超时问题。
import re,requests
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
requests.packages.urllib3.disable_warnings()  # 防止爬取https时出错
lists1=[]
lists2=[]
double_href=[]
def goto_url_1(url):
    url_1 = 'http://ce.baidu.com/index/getRelatedSites?site_address='
    wb_data = requests.get(url_1+url, headers=headers,verify=False)
    requests.packages.urllib3.disable_warnings()
    links = re.findall('{"domain":"(.*?)","score":.*?}', wb_data.text, re.S)
    for link in links:
        lists1.append(link)
def goto_url_2(url):
    url_2 = 'http://tool.chinaz.com/subdomain?domain=' + url
    wb_data = requests.get(url_2, headers=headers, verify=False)
    requests.packages.urllib3.disable_warnings()
    links = re.findall('<a href="javascript:" onclick="window.open.*?;" target="_blank">(.*?)</a>', wb_data.text, re.S)
    for link in links:
        lists2.append(link)
def check_double():  #解决去重链接函数,采用嵌套循环判断，处理完成。
    for list1 in lists1:
        for list2 in lists2:
            if list1==list2:
                lists2.remove(list2) #进行去重处理
        print(list1)
    for list2 in lists2:
        print(list2)
    print('经过去重后得到'+str(len(lists1+lists2))+'个子域名')

if __name__ == '__main__':
    url=input('please input one url,then press Enter of goto next part:\n')
    goto_url_1(url)
    goto_url_2(url)
    check_double()