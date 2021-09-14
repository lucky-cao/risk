import json
from selenium import webdriver
from lxml import etree
import time
import schedule

url = "http://bmfw.www.gov.cn/yqfxdjcx/risk.html"

class Risk:
    
    def __init__(self):
        self.br = webdriver.Chrome()
        self.br.get(url)
        time.sleep(5)

    def high_risk(self):
        """高风险地区"""
        result = self.br.page_source
        html = etree.HTML(result)
        hd_t = '//div[@class="r-high active"]/text()'
        hd = html.xpath(hd_t)
        hd_b = '///div [@class="h-header"]'
        hd_d = html.xpath(hd_b)
        # hd_x = '//td[@class="h-td1"]/text()'
        # hd_xx = html.xpath(hd_x)
        # hd_dict = dict(zip(hd_d, hd_xx))
        h_list = []
        for i in hd_d:
            h_list.append(i.xpath('string(.)').strip().replace('高风险', '').replace(' ', ''))
        hd_json = dict()
        hd_json[hd[0]] = h_list
        time.sleep(2)
        return hd_json

    def medium_risk(self):
        """中风险地区"""
        self.br.find_element_by_css_selector('.r-middle').click()
        time.sleep(6)
        md_json = dict()
        # md_dc = dict()
        while True:
            result = self.br.page_source
            html = etree.HTML(result)
            md_x = '//div[@class="r-middle active"]/text()'
            global md_t
            md_t = html.xpath(md_x)
            # print(md_t)
            md_xd = '//div [@class="m-header"]'
            md_d = html.xpath(md_xd)
            m_list = []
            for i in md_d:
                m_list.append(i.xpath('string(.)').strip().replace('中风险', '').replace(' ', ''))
            # print(m_list)
            # md_xtd = '//table [@class="m-table"]'
            # md_td = html.xpath(md_xtd)[0].xpath('string(.)').strip()
            # print(md_td)
            # md_dict = dict(zip(md_d, md_td))
            # md_dc.update(md_dict)
            # print(md_dc)
            if self.isElement('//div[@class="pages-box"]/button[@id="nextPage"]'):
                el = self.br.find_element_by_xpath('//div[@class="pages-box"]/button[@id="nextPage"]')
                el.click()
            if not self.isElement('//div[@class="pages-box"]/button[@id="nextPage"]'):
                break
            time.sleep(3)
        md_json[md_t[0]] = m_list
        # print(md_json)
        self.br.close()
        return md_json
        
    def isElement(self, element):
        """判断节点是不是置灰"""
        flag = self.br.find_element_by_xpath(element).is_enabled()
        return flag


def dow_risk():
    r = Risk()
    hd = r.high_risk()
    md = r.medium_risk()
    hd.update(md)
    print(hd)
    with open('risk.json', 'w', encoding='utf-8')as f:
        f.write(json.dumps(hd))
    
def start_risk():
    schedule.every(1).hour.do(dow_risk)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    start_risk()
