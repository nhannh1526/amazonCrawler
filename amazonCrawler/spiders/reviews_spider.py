import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"

    def start_requests(self):
        urls = [
            'https://www.amazon.com/dp/B08N7LDM77/ref=fs_a_mbt2_us1',
            'https://www.amazon.com/dp/B08N7NV2KB/ref=fs_a_mbt2_us2',
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
            yield{
                'profile-name': review.css('span.a-profile-name::text').get(),
                'review-star-rating': review.css('span.a-icon-alt::text').get(),
                'review-body': review.css('span.a-size-base.review-text.review-text-content span::text').getall(),
            }

        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_reviews)
