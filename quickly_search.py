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
end_list=[]
double_href=[]
def goto_url_1(url):
    url_1 = 'http://ce.baidu.com/index/getRelatedSites?site_address='
    wb_data = requests.get(url_1+url, headers=headers,verify=False)
    wb_data.encoding = wb_data.apparent_encoding
    requests.packages.urllib3.disable_warnings()
    links = re.findall('{"domain":"(.*?)","score":.*?}', wb_data.text, re.S)
    for link in links:
        lists1.append(link)
def goto_url_2(url):
    url_2 = 'http://tool.chinaz.com/subdomain?domain=' + url
    wb_data = requests.get(url_2, headers=headers, verify=False)
    wb_data.encoding = wb_data.apparent_encoding
    requests.packages.urllib3.disable_warnings()
    links = re.findall('<a href="javascript:" onclick="window.open.*?;" target="_blank">(.*?)</a>', wb_data.text, re.S)
    for link in links:
        lists2.append(link)
def check_double():  #解决去重链接函数,采用嵌套循环判断，处理完成。
    for list1 in lists1:
        for list2 in lists2:
            if list1==list2:
                lists2.remove(list2) #进行去重处理
        #print(list1)
        end_list.append(list1)
    for list2 in lists2:
        #print(list2)
        end_list.append(list2)
    print('经过去重后得到'+str(len(lists1+lists2))+'个子域名')
    print('loading....')
def get_ip_address(url):
    from_chinaz='http://seo.chinaz.com/?q='
    try:
        wb_data = requests.get(from_chinaz+url, headers=headers, verify=False,timeout=3)
        wb_data.encoding=wb_data.apparent_encoding
        ip_address = re.findall('<a href=".*?" target="_blank" title=".*?">(.*?)</a>', wb_data.text, re.S)
        try:
            if len(ip_address[0])>10:
                print(url+':   '+ip_address[0])
            else:
                print('nothing found:'+end)
        except:
            print('error'+end)
    except:
        print('timeout~~~~'+url+'   next')
if __name__ == '__main__':
    url=input('please input one url,then press Enter of goto next part:\n')
    goto_url_1(url)
    goto_url_2(url)
    check_double()
    for end in end_list:
        get_ip_address(end)