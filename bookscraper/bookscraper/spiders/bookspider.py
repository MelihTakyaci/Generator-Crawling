import scrapy
from scrapy.http import FormRequest

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["kj.com.tr"]
    start_urls = ["https://kj.com.tr/tr/dizel-jeneratorler"]

    def parse(self, response):
        options = response.css('select#ContentPlaceHolder1_drpEngines option')
        for option in options:
            option_value = option.xpath('@value').get()

            # Simulate form submission with each option
            yield FormRequest.from_response(
                response,
                formdata={'ctl00$ContentPlaceHolder1$drpEngines': option_value},
                callback=self.after_option_change,
                meta={'selected_option': option_value},
            )

    def after_option_change(self, response):
        # Click the button to change dynamic content
        yield FormRequest.from_response(
            response,
            formdata={'ctl00$ContentPlaceHolder1$btnSearchGenerators': 'Jeneratörleri Listele'},
            callback=self.after_button_click,
            meta={'selected_option': response.meta['selected_option']},
        )

    def after_button_click(self, response):
        # Handle the page after clicking the button
        gens = response.css('div.item')

        for gen in gens:
            yield {
                'brand': gen.css('div.col-sm-2:nth-child(1) span.mobil-val::text').get(),
                'standbykva': gen.css('div.col-sm-2:nth-child(3) div.col-sm-6 span.mobil-val::text').get(),
                'standbykw': gen.css('div.col-sm-2:nth-child(3) div.col-sm-6:nth-child(2) span.mobil-val::text').get(),
                'primekva': gen.css('div.col-sm-2:nth-child(4) div.col-sm-6 span.mobil-val::text').get(),
                'primekw': gen.css('div.col-sm-2:nth-child(4) div.col-sm-6:nth-child(2) span.mobil-val::text').get(),
                'hz': gen.css('div.col-sm-2:nth-child(5) span.mobil-val::text').get(),
                'selected_option': response.meta['selected_option'],
            }
