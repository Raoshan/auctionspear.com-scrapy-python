import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.auctionspear.com/auction/search?search_phrase={}&page=1'

class PearSpider(scrapy.Spider):
    name = 'pear'

    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), cb_kwargs={'index':index})

    def parse(self, response, index):
        total_pages = response.xpath("//ul[@id='pagination']/li[last()-1]/a/text()").get()
        # print(total_pages)
        current_page =response.css("li.active::text").get()
        # print(current_page)
        url = response.url
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    url = url.replace(min,max)                            
                    yield response.follow(url, cb_kwargs={'index':index})       

        images = response.xpath("//div[@class='col-xs-12 col-sm-4']//img/@src").getall()       
        links = response.xpath("//div[@class='col-xs-12 col-sm-4']/a/@href")  
        counter = 0
        for link in links:
            image = images[counter]
            yield response.follow("https://www.auctionspear.com"+link.get(),  callback=self.parse_item, cb_kwargs={'index':index,'image':image})  
            counter = counter+1
        
    def parse_item(self, response, index,image): 
        print(".................")  
        product_url = response.url
        print(product_url)
        item_type=index.strip()
        print(item_type)
        image_link = image
        print(image_link)
        auction_date = response.xpath("//span[@id='lot_scheduled_close']/text()").get()
        print(auction_date)
        description = response.xpath('//*[@id="lot_description"]/div[3]/text()').extract()[1].strip()
        print(description)
        location = response.xpath("//span[@class='location']/p/text()").get().strip()
        print(location)
        product_name = response.css('span.lot-title::text').extract()[0]
        print(product_name)
        lot_number = response.css('span.lot-title::text').extract()[1][5:]
        print(lot_number)
        auctioner = response.css('h4 a::text').get()
        print(auctioner)

        yield{            
            'product_url' : response.url,           
            'item_type' :index,            
            'image_link' : image_link,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : "auctionspear",
            'description':description            
        }