#-*- encoding:utf-8 -*-
from lxml import etree
import requests,re,sys,time,MySQLdb,sys
from main import *
reload(sys)
sys.setdefaultencoding("utf-8")
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
index = requests.get('http://www.zrblog.net',headers = header)
selector = etree.HTML(index.text)
urllist = []

for i in range(2,11):
    inti = str(i)
    xpathcode = '//*[@id="art_main"]/div[' + inti + ']/div[2]/div/span[1]/text()'
    post_type_xpath_code = '//*[@id="art_main"]/div['+ inti + ']/div[2]/ul/li[1]/a/text()'
    post_type_data = selector.xpath(post_type_xpath_code)
    writetime = selector.xpath(xpathcode)
    a = writetime[0].split('：')
    # b=time.strftime("%Y年%m月%d日")
    b = '2015年11月18日'
    print b

    if a[1] == b and (post_type_data[0] == "VPS优惠动态" or post_type_data[0] == "服务器"):
        xpathcode_link= '//*[@id="art_main"]/div['+ inti +']/div[2]/h2/a/@href'
        need_to_spide_link = selector.xpath(xpathcode_link)
        urllist.append(need_to_spide_link[0])

for x in xrange(len(urllist)):
    inpage = requests.get(urllist[x],headers = header)
    inpagecontent = etree.HTML(inpage.text)
    title_xpathcode = '//*[@id="art_main1"]/div[1]/h1/text()'
    page_title = inpagecontent.xpath(title_xpathcode)
    # print page_title[0]
    content_breif_xpathcode = '//*[@id="art_main1"]/div[2]/p[1]'
    content_breif_data = inpagecontent.xpath(content_breif_xpathcode)[0]
    content_breif_data1 = content_breif_data.xpath('string(.)')
    content_breif_data2 = content_breif_data1.replace('赵容部落','阿福')
    content_inter_data = inpagecontent.xpath('//*[@id="art_main1"]/div[2]/p[3]')[0]
    content_inter_data1 = content_inter_data.xpath('string(.)')
    content_inter_data2 = content_inter_data1.replace('赵容部落','阿福')
    content_back_data = inpagecontent.xpath('//*[@id="art_main1"]/div[2]/blockquote')[0]
    content_back_data1 = content_back_data.xpath('string(.)')
    content_back_data2 = content_back_data1.replace('赵容部落','阿福')
    content_promo_data = inpagecontent.xpath('//*[@id="art_main1"]/div[2]/div[3]')[0]
    content_promo_data1 = content_promo_data.xpath('string(.)')
    content_promo_data2 = content_promo_data1.replace('赵容部落','阿福')
    content_aff_data = inpagecontent.xpath('//*[@id="art_main1"]/div[2]/p[4]/a/@href')
    #get_tags
    tag_xpathcode='//*[@id="art_main1"]/div[2]/div[1]/p/a/text()'
    tag_content = inpagecontent.xpath(tag_xpathcode)
    # print tag_content
    # for x in tag_content:
    #     print x
    # print str(tag_content)

    if content_aff_data:
        aff_data = content_aff_data[0]
    else:
        content_aff_data = inpagecontent.xpath('//*[@id="art_main1"]/div[2]/p[4]/text()')
        aff_data = content_aff_data[0]

    content_after_pro = inpagecontent.xpath('//*[@id="art_main1"]/div[2]/p[5]')[0]
    content_after_pro1 = content_after_pro.xpath('string(.)')
    content_after_pro2 = content_after_pro1.replace('赵容部落','阿福')

    myaff_source = replace_afflink(aff_data)

    before_content = "消息来自<a href='http://www.zrblog.net' target='_blank'>赵蓉博客<a>"
    myaff = "http://rffan.info"+myaff_source
    aff_link = "<a href='"+myaff+"' target='_blank'>点击直达<a>"
    print aff_link


    post_data = before_content+"\n"+content_breif_data2+"\n" + content_inter_data2+"\n"+ content_back_data2+"\n" + content_promo_data2+"\n"+content_after_pro2+"\n"+aff_link
    post_title = page_title[0]

    wp_post(str(post_title),str(post_data),tag_content)



