import requests
import re
import urllib
import time
import os
import logging



class GoogleSearchCrawler:



        def __init__(self):
            # create dump folder if it doesn't exists
            if not os.path.exists('results'):
                os.mkdir('results')

        def parse_result(self,html):
            hits = 0

            urls = []

            # each result item is inside <h3> tag
            pats_h3 = re.findall(r'<h3 class="r[\s\w]*?">.+?</h3>', html)

            for pat_h3 in pats_h3:
                pat_h3=urllib.unquote(pat_h3)
                # get result item url
                pat_href=re.findall(r'href=".*?(http.+?)(\&amp|"|\+)',pat_h3)
                if pat_href:
                    # url / href value
                    url=pat_href[0][0]
                    url=urllib.unquote(url)
        #            print url
                    # article date inside <span class="r nsa>
                    urls.append({'url':url})
                    hits=hits+1

            # each result item date is inside <span class="f nsa">
            pats_span = re.findall(r'<span class="f[\s\w]*?">(.+?)<',html)
            idx = 0
            for pat_span in pats_span:
        #        print pat_span
                pat_span_date=re.findall(r'([\d]+ [\w]+ [\d]+)', pat_span)
                if pat_span_date:
                    urls[idx]['date']=pat_span_date[0]
                else:
                    urls[idx]['date']=pat_span

                idx=idx+1


            print "Found", hits

            return urls, hits


        def google_search(self,target_domain, query_string):

            url = "https://www.google.com.sg/search"
            query = query_string
            if target_domain:
                query = 'site:' + target_domain + ' ' + query_string
            output_file=file('results/' + urllib.quote(query) + '.csv','w')
            start = 0
            while True:

                querystring = {"num":"100",
                               "start":str(start),
                               "sclient":"psy-ab",
                               "source":"hp",
                               "tbs":"sbd:1,cdr:1,cd_min:1/1/2015,cd_max:2/27/2017",
                               "tbm":"nws",
                               "q":query,
                               }

                headers = {
                    'cache-control': "no-cache",
                    'postman-token': "613b8671-9549-5556-af0b-609c6b4d4aeb"
                    }

            #    print querystring
                response = requests.request("GET", url, headers=headers, params=querystring)
                result,hits=self.parse_result(response.text)

                if hits > 0:
                    for item in result:
                        output_file.write(item['url'].encode('utf-8')
                                          + ',' + item['date'].encode('utf-8'))
                        output_file.write('\n')

                if hits < 100:
                    break

                start = start + 100

                time.sleep(10)

            output_file.close()

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    googlesearch = GoogleSearchCrawler()
    sites = ["channelnewsasia.com","straitstimes.com","stomp.com.sg","todayonline.com"]
    keywords_1 = ["computer","computerized","computerised","cyber","digital","electronic","high-tech","information technology","internet","networked","technology"]
    keywords_2 = ["elderly","senior citizen","old man","old lady","old guy"]
    for site in sites:
        for keyword1 in keywords_1:
            for keyword2 in keywords_2:
                q =  keyword1 + " crime "+keyword2
                logging.info(q)
                googlesearch.google_search(site,q)
    #`googlesearch.google_search('channelnewsasia.com', 'internet crime + elderly')

