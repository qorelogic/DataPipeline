
import base64
import random

# http://stackoverflow.com/questions/4710483/scrapy-and-proxies
# add the following to settings.py:
#DOWNLOADER_MIDDLEWARES = {
#'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#'numbeo.middlewares.ProxyMiddleware': 100,
#}
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        ''
        # Set the location of the proxy selected randomly from list of proxies
        proxy_pool = ['127.0.0.1:8118']
        request.meta['proxy'] = "http://%s" % random.choice(proxy_pool)
    
        # Use the following lines if your proxy requires authentication
        #proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
