from whyis.test.test_case import TestCase as WhyisTestCase

from base64 import b64encode

from rdflib import *

import json

import nanopub

import autonomic

files = { 
    'L168_S3_Luo_2013' : '''<http://nanomine.org/nmr/xml/L168_S3_Luo_2013.xml> a <http://nanomine.org/ns/NanomineXMLFile>,
        <http://schema.org/DataDownload>,
        <https://www.iana.org/assignments/media-types/text/xml>;
    <http://vocab.rpi.edu/whyis/hasContent> "data:text/xml;charset=UTF-8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPFBvbHltZXJOYW5vY29tcG9zaXRlPjxJRD5MMTAyX1MzX0h1XzIwMDc8L0lEPjxDb250cm9sX0lEPkwxMDJfUzFfSHVfMjAwNzwvQ29udHJvbF9JRD48REFUQV9TT1VSQ0U+PENpdGF0aW9uPjxDb21tb25GaWVsZHM+PENpdGF0aW9uVHlwZT5yZXNlYXJjaCBhcnRpY2xlPC9DaXRhdGlvblR5cGU+PFB1YmxpY2F0aW9uPkpvdXJuYWwgb2YgdGhlIEV1cm9wZWFuIENlcmFtaWMgU29jaWV0eTwvUHVibGljYXRpb24+PFRpdGxlPkRpZWxlY3RyaWMgcHJvcGVydGllcyBvZiBCU1QvcG9seW1lciBjb21wb3NpdGU8L1RpdGxlPjxBdXRob3I+SHUsIFRhbzwvQXV0aG9yPjxBdXRob3I+SnV1dGksIEphcmk8L0F1dGhvcj48QXV0aG9yPkphbnR1bmVuLCBIZWxpPC9BdXRob3I+PEF1dGhvcj5WaWxrbWFuLCBUYWlzdG88L0F1dGhvcj48S2V5d29yZD5Db21wb3NpdGVzPC9LZXl3b3JkPjxLZXl3b3JkPkRpZWxlY3RyaWMgcHJvcGVydGllczwvS2V5d29yZD48S2V5d29yZD5NaWNyb3N0cnVjdHVyZS1maW5hbDwvS2V5d29yZD48S2V5d29yZD5CU1QtQ09DPC9LZXl3b3JkPjxQdWJsaXNoZXI+RWxzZXZpZXI8L1B1Ymxpc2hlcj48UHVibGljYXRpb25ZZWFyPjIwMDc8L1B1YmxpY2F0aW9uWWVhcj48RE9JPjEwLjEwMTYvai5qZXVyY2VyYW1zb2MuMjAwNy4wMi4wODI8L0RPST48Vm9sdW1lPjI3PC9Wb2x1bWU+PFVSTD5odHRwczovL3d3dy5zY2llbmNlZGlyZWN0LmNvbS9zY2llbmNlL2FydGljbGUvcGlpL1MwOTU1MjIxOTA3MDAxMjUyP3ZpYSUzRGlodWI8L1VSTD48TGFuZ3VhZ2U+RW5nbGlzaDwvTGFuZ3VhZ2U+PExvY2F0aW9uPk1pY3JvZWxlY3Ryb25pY3MgYW5kIE1hdGVyaWFscyBQaHlzaWNzIExhYm9yYXRvcmllcywgRU1QQVJUIFJlc2VhcmNoIEdyb3VwIG9mIEluZm90ZWNoIE91bHUsIFAuTy4gQm94IDQ1MDAsIEZJTi05MDAxNCBVbml2ZXJzaXR5IG9mIE91bHUsIEZpbmxhbmQ8L0xvY2F0aW9uPjxEYXRlT2ZDaXRhdGlvbj4yMDE1LTA3LTI0PC9EYXRlT2ZDaXRhdGlvbj48L0NvbW1vbkZpZWxkcz48Q2l0YXRpb25UeXBlPjxKb3VybmFsPjxJU1NOPjA5NTUtMjIxOTwvSVNTTj48SXNzdWU+MTMtMTU8L0lzc3VlPjwvSm91cm5hbD48L0NpdGF0aW9uVHlwZT48L0NpdGF0aW9uPjwvREFUQV9TT1VSQ0U+PE1BVEVSSUFMUz48TWF0cml4PjxNYXRyaXhDb21wb25lbnQ+PENoZW1pY2FsTmFtZT5jeWNsbyBvbGVmaW4gY29wb2x5bWVyPC9DaGVtaWNhbE5hbWU+PEFiYnJldmlhdGlvbj5DT0M8L0FiYnJldmlhdGlvbj48UG9seW1lclR5cGU+Y29wb2x5bWVyPC9Qb2x5bWVyVHlwZT48TWFudWZhY3R1cmVyT3JTb3VyY2VOYW1lPlRpY29uYSBHbWJILCBHZXJtYW55PC9NYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+PFRyYWRlTmFtZT5Ub3BhcyA4MDA3Uy0wNDwvVHJhZGVOYW1lPjxEZW5zaXR5Pjx2YWx1ZT4xLjAyPC92YWx1ZT48dW5pdD5nL2NtXjM8L3VuaXQ+PC9EZW5zaXR5PjwvTWF0cml4Q29tcG9uZW50PjwvTWF0cml4PjxGaWxsZXI+PEZpbGxlckNvbXBvbmVudD48Q2hlbWljYWxOYW1lPmJhcml1bSBzdHJvbnRpdW0gdGl0YW5hdGU8L0NoZW1pY2FsTmFtZT48QWJicmV2aWF0aW9uPkJTVDwvQWJicmV2aWF0aW9uPjxNYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+U2lnbWHigJNBbGRyaWNoIENoZW1pZSBHbWJILCBHZXJtYW55PC9NYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+PERlbnNpdHk+PHZhbHVlPjQuOTwvdmFsdWU+PHVuaXQ+Zy9jbV4zPC91bml0PjwvRGVuc2l0eT48U3BoZXJpY2FsUGFydGljbGVEaWFtZXRlcj48ZGVzY3JpcHRpb24+bGVzcyB0aGFuIDIwMCBubTwvZGVzY3JpcHRpb24+PHZhbHVlPjIwMDwvdmFsdWU+PHVuaXQ+bm08L3VuaXQ+PC9TcGhlcmljYWxQYXJ0aWNsZURpYW1ldGVyPjwvRmlsbGVyQ29tcG9uZW50PjxGaWxsZXJDb21wb3NpdGlvbj48RnJhY3Rpb24+PHZvbHVtZT4wLjA1PC92b2x1bWU+PC9GcmFjdGlvbj48L0ZpbGxlckNvbXBvc2l0aW9uPjxEZXNjcmlwdGlvbj5CYTAuNVNyMC41VGlPMzwvRGVzY3JpcHRpb24+PC9GaWxsZXI+PC9NQVRFUklBTFM+PFBST0NFU1NJTkc+PE1lbHRNaXhpbmc+PENob29zZVBhcmFtZXRlcj48TWl4aW5nPjxNaXhlcj5Ub3JxdWUgUmhlb21ldGVyPC9NaXhlcj48UlBNPjxkZXNjcmlwdGlvbj4zMi02NCBycG08L2Rlc2NyaXB0aW9uPjx2YWx1ZT40ODwvdmFsdWU+PHVuaXQ+cnBtPC91bml0PjwvUlBNPjxUaW1lPjx2YWx1ZT4xNTwvdmFsdWU+PHVuaXQ+bWludXRlczwvdW5pdD48dW5jZXJ0YWludHk+PHR5cGU+YWJzb2x1dGU8L3R5cGU+PHZhbHVlPjU8L3ZhbHVlPjwvdW5jZXJ0YWludHk+PC9UaW1lPjxUZW1wZXJhdHVyZT48dmFsdWU+MjMwPC92YWx1ZT48dW5pdD5DZWxzaXVzPC91bml0PjwvVGVtcGVyYXR1cmU+PC9NaXhpbmc+PC9DaG9vc2VQYXJhbWV0ZXI+PENob29zZVBhcmFtZXRlcj48TW9sZGluZz48TW9sZGluZ01vZGU+aG90LXByZXNzaW5nPC9Nb2xkaW5nTW9kZT48TW9sZGluZ0luZm8+PFRlbXBlcmF0dXJlPjx2YWx1ZT4yMDA8L3ZhbHVlPjx1bml0PkNlbHNpdXM8L3VuaXQ+PC9UZW1wZXJhdHVyZT48L01vbGRpbmdJbmZvPjwvTW9sZGluZz48L0Nob29zZVBhcmFtZXRlcj48L01lbHRNaXhpbmc+PC9QUk9DRVNTSU5HPjxDSEFSQUNURVJJWkFUSU9OPjxTY2FubmluZ19FbGVjdHJvbl9NaWNyb3Njb3B5PjxFcXVpcG1lbnRVc2VkPkpFT0wgSlNNLTY0MDA8L0VxdWlwbWVudFVzZWQ+PC9TY2FubmluZ19FbGVjdHJvbl9NaWNyb3Njb3B5PjxEaWVsZWN0cmljX2FuZF9JbXBlZGFuY2VfU3BlY3Ryb3Njb3B5X0FuYWx5c2lzPjxFcXVpcG1lbnQ+QWdpbGVudCBFNDk5MUE8L0VxdWlwbWVudD48L0RpZWxlY3RyaWNfYW5kX0ltcGVkYW5jZV9TcGVjdHJvc2NvcHlfQW5hbHlzaXM+PFhSYXlfRGlmZnJhY3Rpb25fYW5kX1NjYXR0ZXJpbmc+PEVxdWlwbWVudD5TaWVtZW5zIEQ1MDAwPC9FcXVpcG1lbnQ+PC9YUmF5X0RpZmZyYWN0aW9uX2FuZF9TY2F0dGVyaW5nPjwvQ0hBUkFDVEVSSVpBVElPTj48UFJPUEVSVElFUz48RWxlY3RyaWNhbD48QUNfRGllbGVjdHJpY0Rpc3BlcnNpb24+PERpZWxlY3RyaWNfUmVhbF9QZXJtaXR0aXZpdHk+PGRlc2NyaXB0aW9uPlJlbGF0aXZlIHBlcm1pdHRpdml0eSBhdCAxR0h6PC9kZXNjcmlwdGlvbj48dmFsdWU+Mi45PC92YWx1ZT48L0RpZWxlY3RyaWNfUmVhbF9QZXJtaXR0aXZpdHk+PERpZWxlY3RyaWNfTG9zc19UYW5nZW50PjxkZXNjcmlwdGlvbj5Mb3NzIFRhbmdlbnQgYXQgMSBHSHo8L2Rlc2NyaXB0aW9uPjx2YWx1ZT41ZS0wNTwvdmFsdWU+PC9EaWVsZWN0cmljX0xvc3NfVGFuZ2VudD48L0FDX0RpZWxlY3RyaWNEaXNwZXJzaW9uPjwvRWxlY3RyaWNhbD48L1BST1BFUlRJRVM+PC9Qb2x5bWVyTmFub2NvbXBvc2l0ZT4=" .'''
}

class XMLIngestTest(WhyisTestCase):

    def test_L168_S3_Luo_2013(self):
        self.login(*self.create_user("user@example.com","password"))
        upload = files['L168_S3_Luo_2013']
        
        response = self.client.post("/pub", data=upload, content_type="text/turtle",follow_redirects=True)
        self.assertEquals(response.status,'201 CREATED')

        xml_content = self.client.get("/about",query_string={'uri':'http://nanomine.org/nmr/xml/L163_S4_Luo_2013.xml'}).data
        print("the xml content ", xml_content)
        
        response = self.client.post("/pub", data=open('/apps/nanomine-graph/setl/xml_ingest.setl.ttl','rb').read(), content_type="text/turtle", follow_redirects=True)
        self.assertEquals(response.status, '201 CREATED')
         
#        xml_content = self.client.get("/about",query_string={'uri':'http://nanomine.org/nmr/xml/L102_S3_Hu_2007.xml'}).data
 #       print("the xml content ", xml_content)

        setlmaker = autonomic.SETLMaker()

        results = self.run_agent(setlmaker)
        self.assertTrue(len(results)>0)

        setlr = autonomic.SETLr()

        print(len(self.app.db))
        for setlr_np in results:
            print("\nThe setlr_np is : ", setlr_np)
            setlr_results = self.run_agent(setlr, nanopublication=setlr_np)

        nanocomposites = list(self.app.db.subjects(RDF.type,URIRef("http://nanomine.org/ns/PolymerNanocomposite")))
        print(nanocomposites, len(self.app.db))
        self.assertEquals(len(nanocomposites),1)

