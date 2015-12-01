# -*- encoding:utf-8 -*-
__author__ = 'Administrator'
import sys,MySQLdb,datetime,os
from email.mime.text import MIMEText
reload(sys)
sys.setdefaultencoding("utf-8")
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from config import *


def wp_post(post_title,post_content,post_tag):
    wp = Client(wprpcurl, username, password)
    print wp.call(GetPosts())
    print wp.call(GetUserInfo())
    post = WordPressPost()
    post.title = post_title
    post.content = post_content
    dict1 = {}
    for x in post_tag:
        dict1.setdefault('post_tag',[]).append(str(x))
    dict1.setdefault('category',[]).append('vps')
    post.terms_names = dict1
    post.post_status = 'publish'
    wp.call(NewPost(post))
    print wp.call(GetPosts())

def replace_afflink(oldlink):
    myconn = MySQLdb.connect(host = dbhost,user = dbuser,passwd = dbpass,db='rffan',charset = dbcharset)
    # if myconn:
        # print 'ok'
    cur=myconn.cursor()
    title = oldlink.split('/')[3]
    # title = 'linode'
    # print title

    sql= "select url from wp_redirection_items where title like '%"+title+"%'"
    cur.execute(sql)
    count=cur.execute(sql)
    # print count
    if count == 1:
        print count
        results= cur.fetchall()
        myconn.commit()
        cur.close()
        myconn.close()
        return results[0][0]
    elif count>1:
        err_msg='Too many answers Please check out the links.Ths post will not be posted'
        err_link=oldlink
        cur.close()
        myconn.close()
        error_log(err_link,err_msg)
        sys.exit()
    elif count<1:
        err_msg='Link is not Found in sql,This post will not be posted'
        err_link=oldlink
        cur.close()
        myconn.close()
        error_log(err_link,err_msg)
        sys.exit()


#
# err_link='http://u.zrblog.net/enzu'
# err_msg='Link is Not Found in sql,This post will not be posted.'

def error_log(err_link,err_msg):
    now = datetime.datetime.now()
    today=now.strftime("%Y/%m/%d-%H:%M:%S")
    err_row = today+'  AffLink:'+err_link+'  Error_msg:'+err_msg+'\n'
    fp= open('./logs/error.log','a')
    fp.write(err_row)
    # fp.close()
    # fp = open('./logs/error.log','r')
    # print fp.read()
    # fp.close()
    # print today



def normal_log():
    pass









