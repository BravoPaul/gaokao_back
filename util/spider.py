import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from requests.cookies import RequestsCookieJar
import json
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from multiprocessing.dummy import Pool as ThreadPool
import threadpool
import pandas as pd
import numpy as np
import time

PATH_UNIVERSITY = '../data/data_spider/'


def get_cookie(username, password):
    pass
    chromedriver = '/Users/kunyue/project_personal/my_project/score_traitor/resource/chromedriver-1'
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.wmzy.com/')  # JD 登录页面
    time.sleep(2)  # 等待加载
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.LINK_TEXT, "快速登录"))
    )
    driver.find_element_by_link_text('快速登录').click()  # 切换登录按钮
    time.sleep(2)
    driver.find_element_by_name('mobile').send_keys(username)  # 填写账号
    driver.find_element_by_name('password').send_keys(password)  # 填写密码
    driver.find_element_by_xpath('//button[text()="登录"]').click()  # 点击登录按钮
    driver.delete_all_cookies()
    time.sleep(15)  # 等待加载
    jd_cookies = driver.get_cookies()
    driver.close()  # 关闭浏览器
    pickle.dump(jd_cookies, open('cookies.pkl', 'wb'))  # 保存cookies
    # print('cookies save successfully!')


def download_score_index_page(url):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies)
    cookie_jar = RequestsCookieJar()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    print(soup)
    print(soup.getText())


# //列表页
def download_page_university(url, page_num):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies)
    newHeaders = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Channel': 'www.wmzy.com pc',
        'Connection': 'keep-alive',
        'Content-Length': '37',
        'Content-Type': 'application/json',
        'Host': 'www.wmzy.com',
        'Origin': 'https://www.wmzy.com',
        'Referer': 'https://www.wmzy.com/web/school/list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 x-requested-with: XMLHttpRequest}'}
    cookie_jar = RequestsCookieJar()
    payload = {"filter": {}, "page": page_num, "page_size": 20}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['sch_short_info']
    print('进度：:', page_num)
    return result


# //详情页
def download_page_university_detail(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4147430 Fqag82U0gf2JqIN8bJfzptWQLX4zX1hwqpao4VJRFjLhwYGpQrLe9W862e0R62+6'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?sch_id=' + kargs['sch_id'] + '&tab=0'
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    payload = {
        "sch_id": kargs['sch_id']}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.get(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    soup_done_index = soup.text.find('{"props')
    if soup_done_index!=-1:
        soup_done = soup.text[soup_done_index:]
        site_json = json.loads(soup_done)
        result = site_json['props']['pageProps']['schoolInfor']
        if int(kargs['page_num'])%100==0:
            print('进度：:', kargs['page_num'])
        return result
    else:
        raise ValueError()


# //列表页
def download_major_list(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4147430 Fqag82U0gf2JqIN8bJfzptWQLX4zX1hwqpao4VJRFjLhwYGpQrLe9W862e0R62+6'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/'
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    payload = {"diploma_id": 7}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.get(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    # print(soup.getText())
    site_json = json.loads(soup.text)
    result = site_json['data']['subjects']
    # print('进度：:', kargs['page_num'])
    return result


# //列表页
def download_major_detial(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4147430 Fqag82U0gf2JqIN8bJfzptWQLX4zX1hwqpao4VJRFjLhwYGpQrLe9W862e0R62+6'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/'
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    payload = {"major_id": kargs['mid']}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.get(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']
    print('进度：:', kargs['page_num'])
    return result


def download_page_index(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    # kargs['university_id'] = '52ac2e99747aec013fcf4e6f'
    # kargs['year'] = 2019
    # kargs['wenli'] = 2
    # kargs['page_num'] = 3
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4147430 Fqag82U0gf2JqIN8bJfzptWQLX4zX1hwqpao4VJRFjLhwYGpQrLe9W862e0R62+6'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '221'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Origin': 'https://www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?type=2&sch_id=' + kargs['sch_id'] + ''
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    # batch控制一批还是二批，diploma_id控制本科还是专科
    payload = {"sch_id": "" + kargs['sch_id'] + "", "stu_province_id": "130000000000",
               "enroll_unit_id": "" + kargs['sch_id'] + "", "enroll_adm_type": 2}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    # print(soup.getText())
    result = site_json['data']['drop_box']
    print('进度：:', kargs['page_num'])
    return result


def download_page_school_score(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4147430 Fqag82U0gf2JqIN8bJfzptWQLX4zX1hwqpao4VJRFjLhwYGpQrLe9W862e0R62+6'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '221'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Origin': 'https://www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?type=2&sch_id=' + kargs['sch_id'] + ''
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    payload = {"page": 1, "page_size": 10, "sch_id": kargs['sch_id'],
               "enroll_unit_id": kargs['sch_id'], "enroll_category": 1, "enroll_mode": 1,
               "diploma_id": 1,
               "stu_province_id": "130000000000", "wenli": kargs['wenli'], "only_admission": True}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['eu_list']
    print('进度：:', kargs['page_num'])
    return result


def download_page_major_score(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4147430 Fqag82U0gf2JqIN8bJfzptWQLX4zX1hwqpao4VJRFjLhwYGpQrLe9W862e0R62+6'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '221'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Origin': 'https://www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?=1&sch_id=' + kargs['sch_id'] + ''
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    # batch控制一批还是二批，diploma_id控制本科还是专科
    payload = {"page_size": 100, "stu_province_id": "130000000000", "enroll_category": 1, "enroll_mode": 1,
               "enroll_unit_id": "" + kargs['sch_id'] + "", "sort_key": "enroll_major_code", "sort_type": 1,
               "only_admission": False, "page": 1, "year": kargs['academic_year'],
               "enroll_year": kargs['academic_year'],
               "wenli": kargs['wenli'],
               "academic_year": kargs['academic_year'],
               "diploma_id": kargs['diploma_id'], "batch": kargs['batch'], "batch_ex": kargs['batch_ex'],
               "enroll_stage": kargs['enroll_stage'], "batch_name": kargs['batch_name']}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['enroll_info_list']
    print('进度：:', kargs['page_num'])
    return result


def spider_all_university():
    result = []
    for i in range(1, 140):
        result = result + download_page_university('https://www.wmzy.com/gw/api/sku/sku_service/sch_complete', i)
    pickle.dump(result, open(PATH_UNIVERSITY + 'university' + '.pkl', 'wb'))


def spider_all_school_score(inter):
    sp = SpiderData()
    list_university = sp.get_university_index()[inter[0]:inter[1]]
    result_f = []
    for i, one_data in enumerate(list_university):
        index = one_data['result']
        if index is None:
            result_f.append({'sch_id': one_data['sch_id']})
            continue
        for wenli_i in [1, 2]:
            args = {}
            args['sch_id'] = one_data['sch_id']
            args['wenli'] = wenli_i
            args['page_num'] = i
            result = download_page_school_score(
                'https://www.wmzy.com/gw/api/sku/enroll_admission_service/sch_enroll_data', **args)
            args['result'] = result
            result_f.append(args)
    return result_f


#
def spider_all_major_score(inter):
    sp = SpiderData()
    data = sp.get_university_index()
    list_university = data[inter[0]:inter[1]]
    result_f = []
    for i, one_data in enumerate(list_university):
        index = one_data['result']
        if index is None:
            result_f.append({'sch_id': one_data['sch_id']})
            continue
        for one_index in index:
            one_index['sch_id'] = one_data['sch_id']
            one_index['page_num'] = i
            result = download_page_major_score(
                'https://www.wmzy.com/gw/api/sku/enroll_admission_service/major_enroll_data', **one_index)
            one_index['result'] = result
            result_f.append(one_index)
    return result_f


def spider_all_major_list():
    result_f = []
    for one_diploma_id in ('5', '7'):
        one_index = {}
        one_index['diploma_id'] = one_diploma_id
        result = download_major_list(
            'https://www.wmzy.com/gw/api/sku/sku_service/major_info_all?diploma_id=' + one_diploma_id + '', **one_index)
        one_index['result'] = result
        result_f.append(one_index)
    pickle.dump(result_f,
                open(PATH_UNIVERSITY + 'spider_all_major_list' + '.pkl', 'wb'))
    return result_f


def spider_all_major_detail(inter):
    sp = SpiderData()
    data = sp.get_university_all_major()
    data_format = []
    for one_data in data:
        kargs = {}
        kargs['diploma_id'] = one_data['diploma_id']
        for one_result in one_data['result']:
            kargs['sid'] = one_result['sid']
            kargs['sname'] = one_result['sname']
            for one_cate in one_result['categories']:
                kargs['cid'] = one_cate['cid']
                kargs['cname'] = one_cate['cname']
                for one_major in one_cate['majors']:
                    kargs['mid'] = one_major['mid']
                    kargs['mname'] = one_major['mname']
                    kargs['type'] = one_major['type']
                    data_format.append(kargs.copy())

    list_major = data_format[inter[0]:inter[1]]
    result_f = []
    for i, one_index in enumerate(list_major):
        one_index['page_num'] = i
        result = download_major_detial(
            'https://www.wmzy.com/gw/api/sku/sku_service/major_detail_info?major_id=' + one_index['mid'] + '',
            **one_index)
        result_f.append(result)
    return result_f


def spider_all_university_index(inter):
    print(inter)
    sp = SpiderData()
    list_university = sp.get_university()[inter[0]:inter[1]]
    result_f = []
    kargs = {}
    for i, one_data in enumerate(list_university):
        kargs['sch_id'] = one_data['sch_id']
        kargs['page_num'] = i
        result = download_page_index(
            'https://www.wmzy.com/gw/enroll_admission_service/sku_enroll_adm_data_drop_box', **kargs)
        result_f.append({'sch_id': kargs['sch_id'], 'result': result})
    return result_f


def spider_all_university_detail(inter):
    sp = SpiderData()
    list_university = sp.get_university()[inter[0]:inter[1]]
    result_f = []
    kargs = {}
    for i, one_data in enumerate(list_university):
        id = one_data['sch_id']
        one_data['page_num'] = i
        result = download_page_university_detail(
            'https://www.wmzy.com/web/school?sch_id=' + id+'&tab=0',
            **one_data)
        result_f.append({'sch_id': id, 'result': result})
    return result_f


class SpiderData(object):

    def __init__(self):
        self.basic_path = '../data/data_spider/'

    def __search_print(self, data, university=None):
        result = []
        for one_s in data:
            if one_s['sch_id'] == university:
                result.append(one_s)
        js = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
        print(js)
        return result

    def get_university_by_name(self, name):
        data = pickle.load(open(
            self.basic_path + 'university.pkl', "rb"))
        for one_s in data:
            if one_s['sch_name'] == name:
                return one_s['sch_id']

    def get_university(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'university.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            print(id)
            return self.__search_print(data, id)
        return data

    def get_university_index(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_university_index.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    # def get_university_index_compare(self, university=None, university_name=None):
    #     data = pickle.load(open(
    #         self.basic_path + 'spider_all_university_index.pkl', "rb"))
    #     print('长度为：', len(data))
    #     if university is not None or university_name is not None:
    #         id = university if university is not None else self.get_university_by_name(university_name)
    #         self.__search_print(data, id)
    #
    #     print('分界线-----------------')
    #     data = pickle.load(open(
    #         '/Users/kunyue/project_personal/my_project/gaokao_back/data/data_spider/spider_all_university_index_new.pkl',
    #         "rb"))
    #     print('长度为：', len(data))
    #     if university is not None or university_name is not None:
    #         id = university if university is not None else self.get_university_by_name(university_name)
    #         self.__search_print(data, id)
    #     return data

    def get_university_score(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_school_score.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_detail(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_university_detail.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_major_score(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_major_score.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_major_score_new(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_major_score_new.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_all_major(self, major=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_major_list.pkl', "rb"))
        if major is None:
            result = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
        else:
            for one_major in data:
                if one_major['mname'] == major:
                    result = json.dumps(one_major, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
                    print(result)
        return data

    def get_major_payload_by_university_name(self, university_name=None, year=2019, wenli=1):
        list_university = self.get_university_index(university_name=university_name)
        result_f = []
        for i, one_data in enumerate(list_university):
            index = one_data['result']
            if index is None:
                result_f.append({'sch_id': one_data['sch_id']})
                continue
            for one_index in index:
                one_index['sch_id'] = one_data['sch_id']
                one_index['page_num'] = i
                if one_index['academic_year'] == year and one_index['wenli'] == wenli:
                    result_f.append(one_index)
        return result_f

    def format_school_score(self):
        result = []
        school_score = pickle.load(open(
            self.basic_path + 'spider_all_school_score.pkl', "rb"))
        major_score = pickle.load(open(
            self.basic_path + 'spider_all_major_score.pkl', "rb"))
        result_tmp = {}
        for one_school in major_score:
            result_tmp['sch_id'] = one_school['sch_id']
            print(one_school)
            exit()


def mul_processor_run(func):
    pool = ThreadPool()
    args = []
    for i in range(8):
        args.append((int(2800 / 8 * i), int(2800 / 8 * (i + 1))))
    print(args)
    start_time = time.time()

    results = pool.map(func, args)
    pool.close()
    pool.join()

    end_time = time.time()

    print((end_time - start_time))

    result_final = []
    for one_result in results:
        result_final += one_result
    pickle.dump(result_final, open(PATH_UNIVERSITY + func.__name__ + '_new.pkl', 'wb'))


def mul_thread_run(func):
    results = []

    def get_result(request, result):
        results.append(result)

    args = []

    for i in range(8):
        args_dict = [(int(2800 / 8 * i), int(2800 / 8 * (i + 1)))]
        args.append((args_dict, None))
    print(args)

    start_time = time.time()
    pool = threadpool.ThreadPool(8)
    reqs = threadpool.makeRequests(func, args, get_result)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

    end_time = time.time()

    print((end_time - start_time))
    result_final = []
    for one_result in results:
        result_final += one_result

    pickle.dump(result_final, open(PATH_UNIVERSITY + func.__name__ + '.pkl', 'wb'))


def main():
    # thread
    # 学校和分数类爬虫
    # mul_thread_run(spider_all_university_index)
    # print('爬虫 spider_all_university_detail')
    mul_thread_run(spider_all_university_detail)
    # print('爬虫 spider_all_school_score')
    # mul_thread_run(spider_all_school_score)
    # print('爬虫 spider_all_major_score')
    # mul_thread_run(spider_all_major_score)

    # 专业类爬虫
    # print('爬虫 spider_major_list')
    # spider_all_major_list()
    # print('爬虫 spider_all_major_detail')
    # mul_thread_run(spider_all_major_detail)

    # mul_processor_run(spider_all_university_index)


if __name__ == '__main__':
    main()
    # sp = SpiderData()
    # data = sp.get_university_index_compare(university_name='青岛滨海学院')

    # get_university_index(university_name='河北科技大学')

    #
    #
    # get_cookie('17310541754', '715253pkPK')
    # mul_thread_run(spider_all_major_detail)
    # get_university_index()
    # spider_all_major_list()
    # get_university_major_score()

    # get_cookie('17310541754','715253pkPK')

    # 自定义专业爬虫
    # sp = SpiderData()
    # result = sp.get_major_payload_by_university_name('扬州大学')[0]
    # result_tmp = download_page_major_score('https://www.wmzy.com/gw/api/sku/enroll_admission_service/major_enroll_data',
    #                                        **result)
    # download_page_index('https://www.wmzy.com/gw/enroll_admission_service/sku_enroll_adm_data_drop_box')
