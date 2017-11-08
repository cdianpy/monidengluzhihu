import scrapy
import re
import time
class yizz(scrapy.Spider):
    name = "yiz"
    start_urls = ["http://yishixiejun.quanwenyuedu.io/xiaoshuo.html"]

    def parse(self, response):

        url_list = response.xpath("//ul[@class='list']/li")
        url = response.url

        for li in url_list:
            href =url.split('io')[0] + 'io' + li.xpath(".//a/@href").extract()[0]
            yield scrapy.Request(href,callback=self.download)

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
        yield scrapy.FormRequest(
            url = url_str,
            formdata=form_data,
            callback=self.getdown
        )
    def getdown(self,response):
        p_list = response.xpath("//p")
        for p in p_list:
            cont = p.xpath(".//text()").extract()[0]
            print(cont)
