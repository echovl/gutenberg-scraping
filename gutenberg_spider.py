import scrapy
from scrapy import responsetypes


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    start_urls = [
        "https://www.gutenberg.org/ebooks/search/?sort_order=downloads",
    ]
    custom_settings = {"LOG_LEVEL": "INFO"}

    def parse(self, response: responsetypes.Response):
        for book in response.css("li.booklink"):
            book_page = book.css("a.link::attr(href)").get()
            if book_page is not None:
                yield response.follow(book_page, callback=self.parse_book)

        next_page = response.css("span.links a[accesskey*='+']::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response: responsetypes.Response):
        content_page = response.css("a.link[title='Read online']::attr(href)").get()
        if content_page is not None:
            yield response.follow(content_page, callback=self.parse_book_content)

    def parse_book_content(self, response: responsetypes.Response):
        title = response.css("div#pg-machine-header p::text").get().replace(": ", "")
        content = ""
        for paragraph in response.css("p"):
            paragraph_content = paragraph.css("::text").get()
            if paragraph_content is not None:
                content += paragraph_content + " "

        yield {
            "title": title,
            "content": content,
        }
