from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from pycate.items import Identity, Course, Note
from urlparse import urljoin
import re

CATE = "https://cate.doc.ic.ac.uk"

class CateSpider(CrawlSpider):
    name = "cate"
    allowed_domains = ["cate.doc.ic.ac.uk"]
    start_urls = [CATE]
    http_user = ''
    http_pass = ''

    def parse(self, response):
        self.year = re.search(r"keyp=(\d+)", response.url).group(1)

        hxs = HtmlXPathSelector(response)
	idt = hxs.select('//font[text()="Your identity:"]/following::table')[0]
	values = idt.select("descendant::b/text()").extract()

        identity = Identity()
	identity['first_name']  = values[0]
	identity['last_name']   = values[1]
        self.course             = re.match(r"\((\w+)", values[4]).group(1)
	identity['course']      = self.course
	identity['cid']         = values[7]
	identity['tutor_name']  = values[8]
	identity['tutor_login'] = re.match(r"\((\w+)\)", values[9]).group(1)

        yield identity

        for period in xrange(1, 8):
            url = '%s/timetable.cgi?period=%d&class=c2&keyt=%s:none:none:%s' % (CATE, period, self.year, self.http_user)
            request = Request(url, callback = self.parse_term)
            request.meta['period'] = period
            yield request

    def parse_term(self, response):
        period = response.meta['period']
        hxs = HtmlXPathSelector(response)

        course_headers = hxs.select('//tr/td[2 and b[font[@color="blue"]]]')
        for header in course_headers:
            course = Course()
            course['code'] = header.select('b/font/text()').extract()[0]
            course['name'] = header.select('b/text()').extract()[0][3:]

            note_url = header.select('a/@href').extract()
            
            yield course

            if note_url:
                request = Request(urljoin(CATE, note_url[0]), callback = self.parse_notes)
                request.meta['period'] = period
                yield request

    def parse_notes(self, response):
        period = response.meta['period']
        hxs = HtmlXPathSelector(response)
	note_table = hxs.select('//font[text()="Existing notes:"]/following::table[1]//table')[0]

        for note_row in note_table.select('descendant::tr')[1:]:
            note = Note()
            note['title']     = note_row.select('td[2]/a/text()').extract()[0]

            note_onclick = note_row.select('td[2]/a/@onclick')
            if note_onclick:
                identifier = note_onclick[0].re(r'clickpage\((\d+)\)') 
                note['url'] = 'showfile.cgi?key=%s:%s:%s:%s:NOTES:%s' % (self.year, period, identifier, self.course, self.http_user )
            else:
                note_href = note_row.select('td[2]/a/@href')
                if note_href:
                    note['url'] = note_href.extract()[0]

            note['note_type'] = note_row.select('td[3]/text()').extract()[0]
            yield note
