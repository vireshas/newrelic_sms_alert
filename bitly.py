import urllib
import urllib2
import json
import settings

class Bitly:
    url = "https://api-ssl.bitly.com/v3/shorten"
    access_token = settings.bitly_access_token
    post_params = {
                    "domain" : "bit.ly",
                    "format" : "json",
                    "access_token" : access_token
                  }

    def shorten_url(self, url):
        params = Bitly.post_params.copy()
        params.update({"longUrl": url})
        post_data = urllib.urlencode(params)
        req = urllib2.Request(Bitly.url, post_data)
        response = urllib2.urlopen(req)
        resp = json.load(response)
        print resp
        if resp["data"]:
            return resp["data"]["url"]
        else:
            return ""
