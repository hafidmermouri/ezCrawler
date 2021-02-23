import multiprocessing, os

seed_url = "https://www.lanebryant.com/"
allowed_domains = []

#constants
_ROOT_ =  os.path.dirname(__file__)
RENDER_JS = False
INTERNAL_LINKS_ONLY = True
NB_CONCURRENT_REQUESTS = multiprocessing.cpu_count()
SLEEP_TIME = 0
MAX_URLS_COUNT = 100

CACHE_DAYS = 1 # 0=no cache
CACHE_DELAY_MINUTES = 60*60*24*CACHE_DAYS
CACHE_DIR = os.path.join(_ROOT_, "cache")
OUTPUT_DIR = os.path.join(_ROOT_, "output")

PARSER_XPATH = {
    "title" : "//head/title",
    "h1" : "//h1",
    "rating" : '//div[contains(@class, "bv_avgRating_component_container")]',
    "nb_reviews" : '//div[@class="bv_numReviews_component_container"]'
}
