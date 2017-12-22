import xmltodict

class CrawlResponse(object):

    def __init__(self, response, manifest_item):
        if response is None:
            raise Exception('CrawlResponse requires a response object. "None" provided')
        self.__response = response
        self.__xml = xmltodict.parse(response.text)
        self.__xml = xmltodict.parse(test_response)
        self.__manifest_item = manifest_item

    @property
    def manifest_item(self):
        return self.__manifest_item

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, response):
        # self.__xml = xmltodict.parse(response.text)
        self.__xml = xmltodict.parse(test_response)

    @property
    def xml(self):
        return self.__xml

    @property
    def id(self):
        return self.__xml['feed']['yt:channelId']

    @property
    def title(self):
        return self.__xml['feed']['title']

    @property
    def entries(self):
        return self.__xml['feed']['entry']

test_response = '''
<feed 
    xmlns:yt="http://www.youtube.com/xml/schemas/2015" 
    xmlns:media="http://search.yahoo.com/mrss/" 
    xmlns="http://www.w3.org/2005/Atom">
    <link rel="self" href="http://www.youtube.com/feeds/videos.xml?user=StrayFromTheMorale"/>
    <id>yt:channel:UC-MIT1H6OQA9SilY53O8AyQ</id>
    <yt:channelId>UC-MIT1H6OQA9SilY53O8AyQ</yt:channelId>
    <title>NotLogan HighestPrimate</title>
    <link rel="alternate" href="https://www.youtube.com/channel/UC-MIT1H6OQA9SilY53O8AyQ"/>
    <author>
        <name>NotLogan HighestPrimate</name>
        <uri>
https://www.youtube.com/channel/UC-MIT1H6OQA9SilY53O8AyQ
</uri>
    </author>
    <published>2013-03-22T02:39:29+00:00</published>
    <entry>
        <id>yt:video:3q3wcjMEtUM</id>
        <yt:videoId>3q3wcjMEtUM</yt:videoId>
        <yt:channelId>UC-MIT1H6OQA9SilY53O8AyQ</yt:channelId>
        <title>Jim Norton &amp; Sam Roberts - (12-11-2017)</title>
        <link rel="alternate" href="https://www.youtube.com/watch?v=3q3wcjMEtUM"/>
        <author>
            <name>NotLogan HighestPrimate</name>
            <uri>
                https://www.youtube.com/channel/UC-MIT1H6OQA9SilY53O8AyQ
            </uri>
        </author>
        <published>2017-12-12T00:14:38+00:00</published>
        <updated>2017-12-12T00:21:04+00:00</updated>
        <media:group>
            <media:title>Jim Norton &amp; Sam Roberts - (12-11-2017)</media:title>
            <media:content url="https://www.youtube.com/v/4axllc8XSPY?version=3" type="application/x-shockwave-flash" width="640" height="390"/>
            <media:thumbnail url="https://i1.ytimg.com/vi/4axllc8XSPY/hqdefault.jpg" width="480" height="360"/>
            <media:description>
Judd Apatow in studio. (12-11-2017) Follow Me For Channel Updates @ https://twitter.com/LoganGV Follow Jim @ https://twitter.com/jimnorton Jim's Website - http://jimnorton.com Follow Sam @ https://twitter.com/notsam Sam's YouTube - https://youtube.com/notsam Follow The Show @ http://twitter.com/jimandsamshow MP3 Download - http://www54.zippyshare.com/v/uzx4k2ub/file.html If you're having problems with Zippyshare, use a different browser or clear cookies and cache and try again. If an ad pops up when you hit download just exit out of it and click download again. Sometimes it bugs out for people and the ad pops up. It only pops up once and after you exit the ad you can download it. It works every time.
</media:description>
            <media:community>
                <media:starRating count="1" average="5.00" min="1" max="5"/>
                <media:statistics views="63"/>
            </media:community>
        </media:group>
    </entry>
    <entry>
        <id>yt:video:M1qDwf6RHaI</id>
        <yt:videoId>M1qDwf6RHaI</yt:videoId>
        <yt:channelId>UC-MIT1H6OQA9SilY53O8AyQ</yt:channelId>
        <title>(12-08-2017)</title>
        <link rel="alternate" href="https://www.youtube.com/watch?v=M1qDwf6RHaI"/>
        <author>
            <name>NotLogan HighestPrimate</name>
            <uri>
https://www.youtube.com/channel/UC-MIT1H6OQA9SilY53O8AyQ
</uri>
        </author>
        <published>2017-12-10T02:21:48+00:00</published>
        <updated>2017-12-12T00:21:19+00:00</updated>
        <media:group>
            <media:title>(12-08-2017)</media:title>
            <media:content url="https://www.youtube.com/v/c_1HQ6K1lH8?version=3" type="application/x-shockwave-flash" width="640" height="390"/>
            <media:thumbnail url="https://i4.ytimg.com/vi/c_1HQ6K1lH8/hqdefault.jpg" width="480" height="360"/>
            <media:description>
http://theinterrobang.com Finding comedy in everything and everything in comedy. Ron Bennington has been a stand-up comedian and comedy club owner and promoter. He’s also been part of two legendary radio shows, the Ron and Ron Radio Network and the Ron and Fez show. All of that experience comes together for Bennington. Three hours of talk entertainment with nationally known comedians. His co-host is Gail Bennington who has literally grown up in the business of comedy. It’s fun, edgy and covers everything in comedy today. What ESPN is to sports Bennington is to Comedy. Follow Me For Channel Updates @ https://twitter.com/LoganGV Follow The Show @ https://twitter.com/benningtonshow Follow The iBang @ https://twitter.com/theibang MP3 Download - http://www95.zippyshare.com/v/kkjjv0fv/file.html If you're having problems with Zippyshare, use a different browser or clear cookies and cache and try again. If an ad pops up when you hit download just exit out of it and click download again. Sometimes it bugs out for people and the ad pops up. It only pops up once and after you exit the ad you can download it. It works every time.
</media:description>
            <media:community>
                <media:starRating count="27" average="4.85" min="1" max="5"/>
                <media:statistics views="2104"/>
            </media:community>
        </media:group>
    </entry>
    <entry>
        <id>yt:video:iUJ8r4ReHog</id>
        <yt:videoId>iUJ8r4ReHog</yt:videoId>
        <yt:channelId>UC-MIT1H6OQA9SilY53O8AyQ</yt:channelId>
        <title>
Jim Norton &amp; Sam Roberts - Jim Florentine, Layton Benton (12-08-2017)
</title>
        <link rel="alternate" href="https://www.youtube.com/watch?v=iUJ8r4ReHog"/>
        <author>
            <name>NotLogan HighestPrimate</name>
            <uri>
https://www.youtube.com/channel/UC-MIT1H6OQA9SilY53O8AyQ
</uri>
        </author>
        <published>2017-12-09T06:18:26+00:00</published>
        <updated>2017-12-11T23:56:10+00:00</updated>
        <media:group>
            <media:title>
Jim Norton &amp; Sam Roberts - Jim Florentine, Layton Benton (12-08-2017)
</media:title>
            <media:content url="https://www.youtube.com/v/bYHzfmK7CGo?version=3" type="application/x-shockwave-flash" width="640" height="390"/>
            <media:thumbnail url="https://i3.ytimg.com/vi/bYHzfmK7CGo/hqdefault.jpg" width="480" height="360"/>
            <media:description>
Norton is out. Jim Florentine in studio. Layton Benton stops by. (12-08-2017) Follow Me For Channel Updates @ https://twitter.com/LoganGV Follow Jim @ https://twitter.com/jimnorton Jim's Website - http://jimnorton.com Follow Sam @ https://twitter.com/notsam Sam's YouTube - https://youtube.com/notsam Follow The Show @ http://twitter.com/jimandsamshow MP3 Download - http://www55.zippyshare.com/v/JZIZeHGJ/file.html If you're having problems with Zippyshare, use a different browser or clear cookies and cache and try again. If an ad pops up when you hit download just exit out of it and click download again. Sometimes it bugs out for people and the ad pops up. It only pops up once and after you exit the ad you can download it. It works every time.
</media:description>
            <media:community>
                <media:starRating count="27" average="4.26" min="1" max="5"/>
                <media:statistics views="2112"/>
            </media:community>
        </media:group>
    </entry>
</feed>
<!-- # ydl.download(['https://www.youtube.com/watch?v=3q3wcjMEtUM', 'https://www.youtube.com/watch?v=M1qDwf6RHaI', 'https://www.youtube.com/watch?v=iUJ8r4ReHog']) -->
'''