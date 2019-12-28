#http://ce.baidu.com/index/getRelatedSites?site_address=  子域名查找接口1
#http://tool.chinaz.com/subdomain?domain=   子域名查找接口2
#http://seo.chinaz.com/?q=   #归属地查询、IP解析

#更新日志
# version=1.0.4 已重构代码，完成快速接口接入、使用。
import re,requests
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
requests.packages.urllib3.disable_warnings()  # 防止爬取https时出错
lists1=[]
lists2=[]
end_list=[]
double_href=[]
def goto_url(url):
    requests.packages.urllib3.disable_warnings()
    url_list = ['http://ce.baidu.com/index/getRelatedSites?site_address=' + url,
                'http://tool.chinaz.com/subdomain?domain=' + url]
    for i in range(0,2):
        wb_data= requests.get(url_list[i], headers=headers,verify=False,timeout=3)
        wb_data.encoding = wb_data.apparent_encoding
        if i==0:
            links_1 = re.findall('{"domain":"(.*?)","score":.*?}', wb_data.text, re.S)
            for link in links_1:
                lists1.append(link)
        if i==1:
            links = re.findall('<a href="javascript:" onclick="window.open.*?;" target="_blank">(.*?)</a>', wb_data.text, re.S)
            for link in links:
                lists2.append(link)
        else:
            pass
def check_double():  #解决去重链接函数,采用嵌套循环判断，处理完成。
    for list1 in lists1:
        for list2 in lists2:
            if list1==list2:
                lists2.remove(list2) #进行去重处理
        end_list.append(list1)
    for list2 in lists2:
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
    print('Design by GhostAatrox,version---1.0.4')
    print('1 Θ使用默认配置(全部功能)Θ')
    print('2 ΘIP解析、归属地查询功能(单ip)Θ')
    print('3 Θ子域名查找功能Θ')
    print('4 Θ退出Θ')
    if url != '':
        keyword=input('please press what u want:\n')
        if len(keyword)>1:
            print('Θ暂不支持这种输入,请等待后续拓展Θ')
        else:
            try:
                if int(keyword)>=5:
                    print('Θ暂无此功能,请等待后续拓展Θ')
            except:
                print('Θerror:请输入数字Θ')
        if keyword=='1':
            goto_url(url)
            check_double()
            for end in end_list:
                get_ip_address(end)
        if keyword=='2':
            get_ip_address(url)
        if keyword=='4':
            print('Θsee u laterΘ')
            exit()