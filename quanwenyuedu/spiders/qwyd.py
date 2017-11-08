import scrapy
import os
import re
import time

class qunwyd(scrapy.Spider):
    name = 'qwyd'
    start_urls = ['http://www.quanwenyuedu.io/']
    path = os.path.abspath(os.path.dirname(__name__))
    pathx = os.path.join(path,'xiaoshuml')
    def parse(self, response):
        all_urls =  response.xpath("//div[@class='box']/ul[@class='list']/li/a")

        for url in all_urls:
            XSurl = url.xpath(".//@href").extract()[0]

            yield scrapy.Request(XSurl,
                                 callback=self.allXs)
    def allXs(self,response):
        xsmlurls = response.url + response.xpath("//div[@class='read']/a[@class='button s1']/@href").extract()[0]
        yield scrapy.Request(xsmlurls,
                             callback=self.allml)
    def allml(self,response):
        xsnames = response.xpath("//div[@class='top']/p[@class='title']//text()").extract()[0]
        xsname = (xsnames + ":").split(':')[0]
        xsxz = self.pathx + '\\' + xsname + '.txt'
        with open(xsxz,'a') as f:
            f.write(xsname)
            f.write('\n')
            f.close()
        url_list = response.xpath("//ul[@class='list']/li")
        url_list.reverse()
        url = response.url
        for li in url_list:
            href = url.split('io')[0] + 'io' + li.xpath(".//a/@href").extract()[0]
            yield scrapy.Request(href,
                                 callback=self.download,
                                 meta={'xsxz':xsxz})
    def download(self,response):
        form_data = {
            'c': 'book',
            'a': 'ajax',
        }
        zz = re.compile(r'setTimeout.*')
        js = zz.search(response.text)
        js_list = js.group().split("','")
        # print(js_list[7])
        form_data['id'] = js_list[3]
        form_data['sky'] = js_list[5]
        form_data['t'] = js_list[7].split("'")[0]
        form_data['rndval'] = str(int(time.time() * 1000))
        url_str = ''.join(response.url.split('io/')[:-1]) + 'io/index.php?c=book&a=ajax'
        # print(url_str)
        xsxz = response.meta['xsxz']
        yield scrapy.FormRequest(
            url = url_str,
            formdata=form_data,
            callback=self.getdown,
            meta={'xsxz':xsxz}
        )
    def getdown(self,response):
        p_list = response.xpath("//p")
        xsxz = response.meta['xsxz']
        for p in p_list:
            cont = p.xpath(".//text()").extract()[0]
            with open(xsxz, 'a') as f:
                f.write(cont)
                f.write('\n')
