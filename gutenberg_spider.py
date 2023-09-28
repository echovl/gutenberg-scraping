import re

import scrapy
from scrapy import responsetypes

HEADER_PATTERN = r".*\*\*\* START .*?\*\*\*"
FOOTER_PATTERN = r"\*\*\* END.*"
TITLE_PATTERN = r"Title: (.*)\r"
MAX_BOOKS = 7


class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    start_urls = [
        "https://www.gutenberg.org/ebooks/search/?sort_order=downloads",
    ]
    custom_settings = {"LOG_LEVEL": "INFO"}
    book_count = 0

    def parse(self, response: responsetypes.Response):
        if self.book_count >= MAX_BOOKS:
            return

        for book in response.css("li.booklink"):
            if self.book_count >= MAX_BOOKS:
                return
            book_page = book.css("a.link::attr(href)").get()
            if book_page is not None:
                self.book_count += 1
                yield response.follow(book_page, callback=self.parse_book)

        # Follow next page
        next_page = response.css(
            "span.links a[accesskey*='+']::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response: responsetypes.Response):
        content_page = response.css(
            "a.link[type='text/plain']::attr(href)").get()
        if content_page is not None:
            yield response.follow(content_page, callback=self.parse_book_content)

    def parse_book_content(self, response: responsetypes.Response):
        title_match = re.search(TITLE_PATTERN, response.text)
        if title_match is None:
            return

        # Remove header and footer
        text = re.sub(HEADER_PATTERN, "", response.text,
                      count=1, flags=re.DOTALL)
        text = re.sub(FOOTER_PATTERN, "", text, count=1, flags=re.DOTALL)

        yield {"title": title_match.group(1), "content": text}
