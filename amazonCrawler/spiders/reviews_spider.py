import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ['amazon.com']

    def start_requests(self):
        urls = [
            'https://www.amazon.com/dp/B09G9DKC87/ref=fs_a_iwp2_0',
            'https://www.amazon.com/dp/B09G9BPWNP/ref=fs_a_iwp2_1',
            'https://www.amazon.com/dp/B09G9CX7DK/ref=fs_a_iwp2_2',
            'https://www.amazon.com/dp/B09G914NDC/ref=fs_a_iwp2_3',
            'https://www.amazon.com/dp/B0932D45W8/ref=fs_a_ipadt2_us0',
            'https://www.amazon.com/dp/B0932B5NVD/ref=fs_a_ipadt2_us1',
            'https://www.amazon.com/dp/B08J66ZMY7/ref=fs_a_ipadt2_us2',
            'https://www.amazon.com/dp/B09G9FPHY6/ref=fs_a_ipadt2_us3',
            'https://www.amazon.com/dp/B09G91LXFP/ref=fs_a_ipadt2_us4',
            'https://www.amazon.com/dp/B09HDZ5MKC/ref=fs_a_wt2_us0',
            'https://www.amazon.com/dp/B09HF1DC1J/ref=fs_a_wt2_us1',
            'https://www.amazon.com/dp/B09G993Q18/ref=fs_a_wt2_us2',
            'https://www.amazon.com/dp/B09G96SSLB/ref=fs_a_wt2_us3',
            'https://www.amazon.com/dp/B08PZHYWJS/ref=fs_a_mdt2_us0',
            'https://www.amazon.com/dp/B09JQMJHXY/ref=fs_a_mdt2_us1',
            'https://www.amazon.com/dp/B09JQL3NWT/ref=fs_a_mdt2_us2',
            'https://www.amazon.com/dp/B08N7LDM77/ref=fs_a_mbt2_us1',
            'https://www.amazon.com/dp/B08N7NV2KB/ref=fs_a_mbt2_us2',
            'https://www.amazon.com/dp/B09JQL8KP9/ref=fs_a_mbt2_us3',
            'https://www.amazon.com/dp/B09JQMW44C/ref=fs_a_mbt2_us4',
            'https://www.amazon.com/dp/B0932FPBV8/?_encoding=UTF8&psc=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_all_reviews_url)

    def get_all_reviews_url(self, response):
        all_reviews_url = response.css(
            'a.a-link-emphasis.a-text-bold::attr(href)').get()
        if all_reviews_url:
            all_reviews_url = response.urljoin(all_reviews_url)
            yield scrapy.Request(all_reviews_url, callback=self.parse_reviews)

    def parse_reviews(self, response):
        for review in response.css('div.a-section.review.aok-relative'):
            yield {
                'profile-name': review.css('span.a-profile-name::text').get(),
                'review-star-rating': review.css('span.a-icon-alt::text').get(),
                'review-body': review.css('span.a-size-base.review-text.review-text-content span::text').getall(),
            }

        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_reviews)
