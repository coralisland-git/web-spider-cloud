# from __future__ import unicode_literals
import scrapy
import json
import os
import scrapy
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
from selenium import webdriver
from lxml import html
import time
import pdb

import time

class waterwell_original(scrapy.Spider):

	name = 'waterwell_original'

	domain = 'https://secure.in.gov/'

	history = []

	header = {

		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

		"Accept-Encoding":"gzip, deflate, br",

		"Content-Type":"application/x-www-form-urlencoded",

		"Upgrade-Insecure-Requests":"1",

		"Origin":"https://secure.in.gov",

		"Referer":"https://secure.in.gov/apps/dnr/dowos/WaterWell.aspx",

		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
	}

	def __init__(self):
		pass
	
	def start_requests(self):

		init_url  = 'https://secure.in.gov/apps/dnr/dowos/WaterWell.aspx'

		formdata = {

			"__EVENTTARGET":'',

			"__EVENTARGUMENT":'',

			"__LASTFOCUS":'',

			"__VIEWSTATEGENERATOR":"E4F44E51",

			"__SCROLLPOSITIONX":"0",

			"__SCROLLPOSITIONY":"240.90908813476562",

			"mstr$cphUserItems$ddlQSearch":"County",

			"mstr$cphUserItems$ddlQCounty":"1",

			"mstr$cphUserItems$txtMaxNumRows":"30000",

			"mstr$cphUserItems$btnSearchGo":"Search",

			"mstr$cphUserItems$txtAddrNum":'',

			"mstr$cphUserItems$ddlAddrDirection":"0",

			"mstr$cphUserItems$txtAddrName":'',

			"mstr$cphUserItems$txtAddrZip":'',

			"mstr$cphUserItems$txtAddrMaxRows":"30000",

			"__VIEWSTATE":"/wEPDwULLTE5Mzc2MjIwODcPZBYCZg9kFgICAw9kFgQCBQ9kFgQCAQ9kFgICBQ8QZGQWAGQCAw9kFgYCCw88KwANAQAPFgYeB1Zpc2libGVoHgtfIURhdGFCb3VuZGceC18hSXRlbUNvdW50ZmRkAg0PDxYCHwBoZGQCDw8PFgIfAGhkZAIJD2QWBAIBD2QWCgIFDxBkZBYBAgFkAgkPDxYCHwBoZGQCCw8QDxYIHg1EYXRhVGV4dEZpZWxkBQ1zdHJDb3VudHlOYW1lHg5EYXRhVmFsdWVGaWVsZAUNaW50Q291bnR5Tm1ich8BZx8AZ2QQFVwFQWRhbXMFQWxsZW4LQmFydGhvbG9tZXcGQmVudG9uCUJsYWNrZm9yZAVCb29uZQVCcm93bgdDYXJyb2xsBENhc3MFQ2xhcmsEQ2xheQdDbGludG9uCENyYXdmb3JkB0Rhdmllc3MIRGVhcmJvcm4HRGVjYXR1cgZEZUthbGIIRGVsYXdhcmUGRHVib2lzB0Vsa2hhcnQHRmF5ZXR0ZQVGbG95ZAhGb3VudGFpbghGcmFua2xpbgZGdWx0b24GR2lic29uBUdyYW50BkdyZWVuZQhIYW1pbHRvbgdIYW5jb2NrCEhhcnJpc29uCUhlbmRyaWNrcwVIZW5yeQZIb3dhcmQKSHVudGluZ3RvbgdKYWNrc29uBkphc3BlcgNKYXkJSmVmZmVyc29uCEplbm5pbmdzB0pvaG5zb24ES25veAlLb3NjaXVza28ITGFHcmFuZ2UETGFrZQdMYVBvcnRlCExhd3JlbmNlB01hZGlzb24GTWFyaW9uCE1hcnNoYWxsBk1hcnRpbgVNaWFtaQZNb25yb2UKTW9udGdvbWVyeQZNb3JnYW4GTmV3dG9uBU5vYmxlBE9oaW8GT3JhbmdlBE93ZW4FUGFya2UFUGVycnkEUGlrZQZQb3J0ZXIFUG9zZXkHUHVsYXNraQZQdXRuYW0IUmFuZG9scGgGUmlwbGV5BFJ1c2gKU3QuIEpvc2VwaAVTY290dAZTaGVsYnkHU3BlbmNlcgZTdGFya2UHU3RldWJlbghTdWxsaXZhbgtTd2l0emVybGFuZApUaXBwZWNhbm9lBlRpcHRvbgVVbmlvbgtWYW5kZXJidXJnaApWZXJtaWxsaW9uBFZpZ28GV2FiYXNoBldhcnJlbgdXYXJyaWNrCldhc2hpbmd0b24FV2F5bmUFV2VsbHMFV2hpdGUHV2hpdGxleRVcATEBMgEzATQBNQE2ATcBOAE5AjEwAjExAjEyAjEzAjE0AjE1AjE2AjE3AjE4AjE5AjIwAjIxAjIyAjIzAjI0AjI1AjI2AjI3AjI4AjI5AjMwAjMxAjMyAjMzAjM0AjM1AjM2AjM3AjM4AjM5AjQwAjQxAjQyAjQzAjQ0AjQ1AjQ2AjQ3AjQ4AjQ5AjUwAjUxAjUyAjUzAjU0AjU1AjU2AjU3AjU4AjU5AjYwAjYxAjYyAjYzAjY0AjY1AjY2AjY3AjY4AjY5AjcwAjcxAjcyAjczAjc0Ajc1Ajc2Ajc3Ajc4Ajc5AjgwAjgxAjgyAjgzAjg0Ajg1Ajg2Ajg3Ajg4Ajg5AjkwAjkxAjkyFCsDXGdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCDQ8QDxYGHwMFEXN0clF1YWRyYW5nbGVOYW1lHwQFEXN0clF1YWRyYW5nbGVObWJyHwFnZBAVxwUPQWJlcmRlZW4sIElOLUtZBUFjdG9uBUFkYW1zEUFkYW1zdmlsbGUsIE1JLUlOBUFrcm9uBUFsYW1vBkFsYmlvbgpBbGV4YW5kcmlhDEFsZm9yZHN2aWxsZQxBbGxlbnMgQ3JlZWsGQWxwaW5lDEFsdG9uLCBLWS1JTgxBbWJpYSwgSUwtSU4FQW1ib3kOQW5kZXJzb24gTm9ydGgOQW5kZXJzb24gU291dGgHQW5kcmV3cwtBbmdvbGEgRWFzdAtBbmdvbGEgV2VzdAVBbm9rYQdBcmNhZGlhBkFyY29sYQVBcmdvcwVBcm5leQZBc2hsZXkGQXR0aWNhBkF0d29vZAZBdWJ1cm4HQXVndXN0YQ1BdXJvcmEsIElOLUtZBkF6YWxpYQxCYXJnZXJzdmlsbGUOQmFydGxldHRzdmlsbGUJQmFzcyBMYWtlCkJhdGVzdmlsbGULQmVhbmJsb3Nzb20LQmVhciBCcmFuY2gKQmVja3MgTWlsbAxCZWRmb3JkIEVhc3QMQmVkZm9yZCBXZXN0C0JlZWNoIEdyb3ZlE0JlZWNoZXIgRWFzdCwgSUwtSU4RQmVlY2h3b29kLCAgSU4tS1kIQmVsbG1vcmUHQmVsbW9udApCZW5uaW5ndG9uBUJlcm5lEEJldGhsZWhlbSwgSU4tS1kIQmlja25lbGwGQmlwcHVzCEJpcmRzZXllD0Jpc21hcmNrLCBJTC1JTgZCbGFpbmUHQmxvY2hlcgpCbG9vbWZpZWxkC0Jsb29taW5ndG9uCEJsdWZmdG9uCUJvZ2dzdG93bglCb29udmlsbGUGQm9yZGVuB0Jvc3dlbGwHQm91cmJvbgtCcmFuY2h2aWxsZQtCcmF6aWwgRWFzdAtCcmF6aWwgV2VzdAZCcmVtZW4KQnJpZGdlcG9ydAdCcmlzdG9sB0JyaXN0b3cUQnJvbnNvbiBTb3V0aCwgTUktSU4JQnJvb2tzdG9uDEJyb29rc3RvbiBOVwxCcm9va3N0b24gU1cKQnJvb2t2aWxsZQpCcm93bnNidXJnCkJyb3duc3Rvd24LQnJvd25zdmlsbGUIQnVja3Rvd24HQnVmZmFsbwtCdW5rZXIgSGlsbAZCdXJrZXQKQnVybGluZ3Rvbg1CdXJuZXR0c3ZpbGxlD0J1cnIgT2FrLCBNSS1JTgdCdXJyb3dzEkJ1dGxlciBFYXN0LCBJTi1PSAtCdXRsZXIgV2VzdAtCdXRsZXJ2aWxsZQ1DYWJvcm4sIElOLUtZEUNhbGlmb3JuaWEsIE1JLUlOE0NhbHVtZXQgQ2l0eSwgSUwtSU4OQ2FtYnJpZGdlIENpdHkNQ2FtZGVuLCBNSS1JTg1DYW1wYmVsbHNidXJnBkNhbmFhbhBDYW5uZWx0b24sIElOLUtZCENhcmxpc2xlBkNhcmxvcwZDYXJtZWwRQ2Fycm9sbHRvbiwgS1ktSU4IQ2FydGhhZ2UIQ2F0YXJhY3QGQ2F0bGluC0NlZGFyIEdyb3ZlCkNlZGFydmlsbGUMQ2VudGVyIFBvaW50EkNoYXJsZXN0b3duLCBJTi1LWQpDaGF0dGVydG9uCkNoZXN0ZXJ0b24OQ2hlc3RudXQgUmlkZ2UIQ2hyaXNuZXkKQ2h1cnVidXNjbwpDbGFya3NidXJnCUNsYXkgQ2l0eQdDbGF5dG9uC0NsZWFyIENyZWVrFENsZWFyIExha2UsIElOLU9ILU1JCENsZXJtb250CUNsZXZlbGFuZAxDbGlmdHkgRmFsbHMHQ2xpbnRvbg1DbGludG9uIEZhbGxzCkNsb3ZlcmRhbGURQ2xvdmVycG9ydCwgS1ktSU4HQ2x5bWVycwlDb2FsIENpdHkLQ29hdGVzdmlsbGUGQ29sZmF4FUNvbGxlZ2UgQ29ybmVyLCBPSC1JTg1Db2x1bWJpYSBDaXR5CENvbHVtYnVzDENvbm5lcnN2aWxsZRJDb25zdGFudGluZSwgTUktSU4EQ29wZQdDb3J1bm5hDENvcnlkb24gRWFzdAxDb3J5ZG9uIFdlc3QNQ29zbW9zLCBJTi1PSAlDb3Zpbmd0b24IQ3JhbmRhbGwOQ3Jhd2ZvcmRzdmlsbGUMQ3Jvc3MgUGxhaW5zDUNyb3RoZXJzdmlsbGULQ3Jvd24gUG9pbnQGQ3VsdmVyCkN1bWJlcmxhbmQFQ3V6Y28JQ3ludGhpYW5hBERhbGUERGFuYQhEYW52aWxsZRJEYW52aWxsZSBORSwgSUwtSU4SRGFudmlsbGUgU0UsIElMLUlOCkRhcmxpbmd0b24NRGFycm93LCBJTC1JTghEYXlsaWdodBBEZSBHb25pYSBTcHJpbmdzB0RlY2F0dXINRGVja2VyLCBJTC1JTgpEZWVkc3ZpbGxlCkRlZXIgQ3JlZWsJRGVlcmZpZWxkBkRlbHBoaQdEZW1vdHRlBkRlbmhhbQ9EZW5uaXNvbiwgSUwtSU4GRGVwYXV3BkRlcHV0eQxEZXJieSwgSU4tS1kJRGlsbHNib3JvDERpeG9uLCBJTi1PSAhEb21lc3RpYwlEb25hbGRzb24ORG9ub3ZhbiwgSUwtSW4GRHVib2lzBkR1Z2dlcgpEdW5lIEFjcmVzCER1bnJlaXRoC0R5ZXIsIElMLUlOFUUgTW91bnQgQ2FybWVsLCBJTC1JTglFYXJsIFBhcmsFRWF0b24JRWRpbmJ1cmdoC0Vkb24sIElOLU9IEkVkd2FyZHNidXJnLCBNSS1JTgNFZ2UJRWxiZXJmZWxkDUVsaXphYmV0aHRvd24HRWxraGFydAtFbGtpbnN2aWxsZQZFbHdvb2QIRW1pbmVuY2ULRW1tYSwgSUwtSU4HRW5nbGlzaAxFbmdsaXNoIExha2UERW5vcwVFcHNvbRBFdmFuc3ZpbGxlIE5vcnRoFkV2YW5zdmlsbGUgU291dGgsSU4tS1kHRXZlcnRvbglGYWlyIE9ha3MQRmFpcmJhbmtzLCBJTC1JThBGYWlyaGF2ZW4sIE9ILUlOCUZhaXJtb3VudAhGYWxtb3V0aAhGYXJtbGFuZAdGYXlldHRlB0Zpc2hlcnMFRmxvcmEPRmxvcmVuY2UsIElOLUtZC0ZvbHNvbXZpbGxlB0ZvcmFrZXILRm9yZXN0IEhpbGwQRm9ydCBLbm94LCBJTi1LWRRGb3J0IFJlY292ZXJ5LCBJTi1PSA9Gb3J0IFdheW5lIEVhc3QPRm9ydCBXYXluZSBXZXN0DUZvdW50YWluIENpdHkMRm91bnRhaW50b3duBkZvd2xlcgxGcmFuY2VzdmlsbGUJRnJhbmNpc2NvCUZyYW5rZm9ydAhGcmFua2xpbghGcmFua3Rvbg5GcmVkZXJpY2tzYnVyZwdGcmVlZG9tC0ZyZW5jaCBMaWNrCUZyaXRjaHRvbgVGdWxkYQZGdWx0b24NR2FsaWVuLCBNSS1JTglHYWx2ZXN0b24HR2FycmV0dARHYXJ5CEdhcyBDaXR5Bkdhc3RvbgdHYXRjaGVsBkdlbmV2YQpHZW9yZ2V0b3duB0dlb3JnaWEHR2lmZm9yZAZHaWxtYW4IR2xlbmRhbGUIR29vZGxhbmQGR29zaGVuB0dvc3BvcnQHR3JhYmlsbAdHcmFtbWVyC0dyYXNzIENyZWVrEEdyYXl2aWxsZSwgSUwtSU4KR3JlZW5icmllcgtHcmVlbmNhc3RsZQpHcmVlbmZpZWxkC0dyZWVucyBGb3JrCkdyZWVuc2J1cmcJR3JlZW50b3duCUdyZWVud29vZAhHdWlsZm9yZApIYWdlcnN0b3duBEhhbGwISGFtaWx0b24GSGFtbGV0BUhhbm5hC0hhcmRpbnNidXJnD0hhcnJpc29uLCBPSC1JThJIYXJ0Zm9yZCBDaXR5IEVhc3QSSGFydGZvcmQgQ2l0eSBXZXN0CkhhcnRzdmlsbGUJSGF1YnN0YWR0BkhheWRlbglIYXplbHJpZ2cSSGVhdGhzdmlsbGUsIElMLUlOBkhlYnJvbhBIZW5kZXJzb24sIEtZLUlOCkhlbnJ5dmlsbGURSGlja3N2aWxsZSwgSU4tT0gISGlnaGxhbmQHSGlsbGhhbQpIaWxsaXNidXJnCUhpbGxzYm9ybwlIaW5kdXN0YW4ISG9hZ2xhbmQHSG9sbGFuZAZIb2x0b24QSG9vdmVuLCBPSC1JTi1LWQRIb3BlDkh1bXJpY2ssIElMLUlOCkh1bnRlcnRvd24LSHVudGluZ2J1cmcKSHVudGluZ3RvbgVIdXJvbhJIdXRzb252aWxsZSwgSUwtSU4NSHV0dG9uLCBJTC1JTgZIeW1lcmEISWRhdmlsbGUWSWxsaWFuYSBIZWlnaHRzLCBJTC1JTg5JbmRpYW4gU3ByaW5ncxFJbmRpYW5hcG9saXMgRWFzdBFJbmRpYW5hcG9saXMgV2VzdAdJbmdhbGxzBklud29vZARJb25hE0phY2tzb24gUGFyaywgSUwtSU4LSmFja3NvbmJ1cmcKSmFzb252aWxsZQZKYXNwZXIVSmVmZmVyc29udmlsbGUsIElOLUtZCkpvbmVzdmlsbGUGS2Fzc29uEEtlZW5zYnVyZywgSUwtSU4HS2VtcHRvbgxLZW5kYWxsdmlsbGUES2VudAhLZW50bGFuZAdLZXdhbm5hEUtpbmRlcmhvb2ssIE1JLUlOB0tpbmdtYW4RS2luZ3Nmb3JkIEhlaWdodHMHS2lya2xpbgtLaXJrcGF0cmljaxNLbGluZ2VyIExha2UsIE1JLUlOC0tuaWdodHN0b3duCUtub3ggRWFzdAlLbm94IFdlc3QLS29rb21vIEVhc3QLS29rb21vIFdlc3QGS29sZWVuEUtvc21vc2RhbGUsIElOLUtZB0tvc3N1dGgFS291dHMFS3VydHoJTGEgQ3Jvc3NlC0xhIEZvbnRhaW5lEExhIEdyYW5nZSwgS1ktSU4GTGEgUGF6DUxhIFBvcnRlIEVhc3QNTGEgUG9ydGUgV2VzdA5MYWNvbmlhLCBJTi1LWQZMYWRvZ2EOTGFmYXlldHRlIEVhc3QOTGFmYXlldHRlIFdlc3QITGFncmFuZ2UFTGFncm8TTGFrZSBDYWx1bWV0LCBJTC1JTgxMYWtlIFdhd2FzZWUJTGFrZXZpbGxlEUxhbmVzdmlsbGUsIElOLUtZBUxhcGVsBExhdWQWTGF3cmVuY2VidXJnLCBLWS1JTi1PSBJMZWF2ZW53b3J0aCwgSU4tS1kHTGViYW5vbghMZWVzYnVyZxBMZWVzdmlsbGUsIElMLUlOBUxlcm95BUxld2lzC0xld2lzIENyZWVrEExld2lzcG9ydCwgS1ktSU4KTGV3aXN2aWxsZQdMaWJlcnR5DkxpYmVydHkgQ2VudGVyCExpZ29uaWVyBkxpbmRlbgpMaW5uIEdyb3ZlBkxpbnRvbgtMaXR0bGUgWW9yawdMaXZvbmlhBkxpenRvbgpMb2dhbnNwb3J0CUxvb2dvb3RlZQZMb3JhbmUWTG91aXN2aWxsZSBXZXN0LCBLWS1JTgZMb3dlbGwHTHVjZXJuZQZMeWRpY2sETHlubglMeW5udmlsbGUFTHlvbnMETWFjeRNNYWRpc29uIEVhc3QsIEtZLUlOE01hZGlzb24gV2VzdCwgSU4tS1kITWFqZW5pY2EHTWFuaWxsYQlNYW5zZmllbGQGTWFwbGVzCE1hcmlldHRhBk1hcmlvbgZNYXJrbGUMTWFydGluc3ZpbGxlEE1hdHRpbmdseSwgS1ktSU4QTWF1Y2twb3J0LCBJTi1LWQ1NYXVuaWUsIElMLUlOCE1heHZpbGxlBE1heXMHTWF5d29vZAxNY0NvcmRzdmlsbGUKTWNDb3lzYnVyZwVNZWNjYQ1NZWNoYW5pY3NidXJnC01lZGFyeXZpbGxlBk1lZG9yYQdNZWxsb3R0B01lbnRvbmUMTWVyb20sIElMLUlOB01lcnJpYW0ITWV0YW1vcmEFTWlhbWkSTWljaGlnYW4gQ2l0eSBFYXN0Ek1pY2hpZ2FuIENpdHkgV2VzdAxNaWNoaWdhbnRvd24KTWlkZGxlYnVyeQpNaWRkbGV0b3duBU1pbGFuB01pbGZvcmQLTWlsbGVyc2J1cmcKTWlsbGhvdXNlbghNaWxsdG93bgZNaWxyb3kITWl0Y2hlbGwHTW9kZXN0bwVNb2RvYwVNb25nbwVNb25vbghNb25vbiBORQtNb25yb2UgQ2l0eQlNb250ZXp1bWEKTW9udGdvbWVyeRBNb250aWNlbGxvIE5vcnRoEE1vbnRpY2VsbG8gU291dGgKTW9udHBlbGllchBNb29yZXN2aWxsZSBFYXN0EE1vb3Jlc3ZpbGxlIFdlc3QKTW9yZ2FudG93bgdNb3JvY2NvCk1vcnJpc3Rvd24QTW90dHZpbGxlLCBNSS1JTglNb3VudCBBeXITTW91bnQgQ2FybWVsLCBJTC1JTgpNb3VudCBFdG5hDE1vdW50IEdpbGJvYQ5Nb3VudCBQbGVhc2FudBNNb3VudCBWZXJub24sIElOLUtZCE11bGJlcnJ5C011bmNpZSBFYXN0C011bmNpZSBXZXN0DU5hcHBhbmVlIEVhc3QNTmFwcGFuZWUgV2VzdAlOYXNodmlsbGURTmV3IEFsYmFueSwgSU4tS1kUTmV3IEFtc3RlcmRhbSwgS1ktSU4OTmV3IEJlbGxzdmlsbGUWTmV3IEJ1ZmZhbG8gRWFzdCxNSS1JThZOZXcgQnVmZmFsbyBXZXN0LE1JLUlODE5ldyBDYXJsaXNsZQ9OZXcgQ2FzdGxlIEVhc3QPTmV3IENhc3RsZSBXZXN0Ek5ldyBDb3J5ZG9uLCBJTi1PSA1OZXcgRmFpcmZpZWxkCk5ldyBHb3NoZW4STmV3IEhhcm1vbnksIElOLUlMCk5ldyBNYXJrZXQQTmV3IFBhcmlzLCBPSC1JTglOZXcgUG9pbnQITmV3IFJvc3MJTmV3IFNhbGVtDk5ldyBXYXNoaW5ndG9uD05ld2J1cmdoLCBJTi1LWQdOZXdwb3J0EU5pbGVzIEVhc3QsIE1JLUlOEU5pbGVzIFdlc3QsIE1JLUlOB05pbmV2ZWgLTm9ibGVzdmlsbGUGTm9ybWFuDE5vcnRoIEp1ZHNvbg9Ob3J0aCBKdWRzb24gU0UNTm9ydGggTGliZXJ0eRZOb3J0aCBNYW5jaGVzdGVyIE5vcnRoFk5vcnRoIE1hbmNoZXN0ZXIgU291dGgLTm9ydGggU2FsZW0MTm9ydGggVmVybm9uDU5vcnRoIFdlYnN0ZXIMT2FrbGFuZCBDaXR5B09ha3Rvd24ET2RvbgtPZ2RlbiBEdW5lcwtPbGl2ZXIgTGFrZQVPbWVnYQZPbndhcmQHT29saXRpYwZPcmxhbmQFT3JtYXMHT3NjZW9sYQZPc2dvb2QGT3NzaWFuBk90aXNjbwlPdHRlcmJlaW4GT3R3ZWxsC093ZW4sIEtZLUlOFU93ZW5zYm9ybyBFYXN0LCBJTi1LWRVPd2Vuc2Jvcm8gV2VzdCwgSU4tS1kJT3dlbnNidXJnCk93ZW5zdmlsbGUGUGFsbWVyB1BhbG15cmEFUGFvbGkHUGFyYWdvbgRQYXJyBlBhdG9rYQxQYXRyaWNrc2J1cmcOUGF0cmlvdCwgSU4tS1kJUGVuZGxldG9uCVBlbm52aWxsZQZQZW9yaWELUGVycnlzdmlsbGUIUGVyc2hpbmcEUGVydQpQZXRlcnNidXJnCVBldHJvbGV1bQlQaWVyY2V0b24LUGllcmNldmlsbGUHUGltZW50bwxQaW5lIFZpbGxhZ2UKUGxhaW5maWVsZApQbGFpbnZpbGxlCFBseW1vdXRoA1BvZQxQb2ludCBJc2FiZWwGUG9sYW5kB1BvcnRhZ2UIUG9ydGxhbmQKUG9zZXl2aWxsZQZQcmVibGUJUHJpbmNldG9uB1B5cm1vbnQGUXVpbmN5DVJheXMgQ3Jvc3NpbmcGUmVka2V5C1JlZWQsIEtZLUlOClJlZWxzdmlsbGUMUmVpbHksIE9ILUlOCVJlbWluZ3RvbgpSZW5zc2VsYWVyCFJleHZpbGxlDVJpY2hsYW5kIENpdHkIUmljaG1vbmQKUmljaHZhbGxleQpSaWRnZXZpbGxlBlJpcGxleRFSaXNpbmcgU3VuLCBJTi1LWQlSaXZlcndvb2QJUm9hY2hkYWxlBVJvYW5uCVJvY2hlc3RlchFSb2NrIEhhdmVuLCBLWS1JTg9Sb2NrcG9ydCwgSU4tS1kJUm9ja3ZpbGxlBFJvbGwLUm9tZSwgSU4tS1kGUm9tbmV5CFJvc2VkYWxlB1Jvc3N0b24JUm9zc3ZpbGxlC1JvdW5kIEdyb3ZlCVJ1c2h2aWxsZQRSdXNrDFJ1c3NlbGx2aWxsZRNSdXNzZWxsdmlsbGUsIElMLUlOC1J1c3NpYXZpbGxlB1J1dGxhbmQNU2FpbnQgQW50aG9ueRRTYWludCBCZXJuaWNlLCBJTi1JTAlTYWludCBKb2UNU2FpbnQgTWVpbnJhZAVTYWxlbQtTYWxpbmUgQ2l0eQtTYW4gSmFjaW50bwpTYW4gUGllcnJlCFNhbmRib3JuClNhbmR5IEhvb2sOU2FuZm9yZCwgSUwtSU4LU2FudGEgQ2xhdXMJU2NobmVpZGVyCFNjb3RsYW5kEFNjb3R0bGFuZCwgSUwtSU4KU2NvdHRzYnVyZwpTZWVseXZpbGxlBlNlcnZpYQdTZXltb3VyC1NoYW5ub25kYWxlCFNoZWxidXJuBlNoZWxieQtTaGVsYnl2aWxsZQ5TaGVsZG9uLCBJTC1JTghTaGVyaWRhbgtTaGlwc2hld2FuYQdTaGlybGV5BlNob2FscwtTaWx2ZXIgTGFrZQdTbWVkbGV5D1NtaXRoIE1pbGxzLCBLWQhTb2xpdHVkZQlTb2xzYmVycnkIU29tZXJzZXQPU291dGggQmVuZCBFYXN0D1NvdXRoIEJlbmQgV2VzdAxTb3V0aCBCb3N0b24SU291dGggV2hpdGxleSBFYXN0ElNvdXRoIFdoaXRsZXkgV2VzdAZTcGFkZXMSU3BhcnRhbmJ1cmcsIElOLU9IBVNwZWVkB1NwZW5jZXILU3ByaW5ndmlsbGUWU3QuIEZyYW5jaXN2aWxsZSxJTC1JTghTdC4gSm9obghTdGFuZm9yZAlTdGFyIENpdHkIU3RhdW50b24JU3RpbGx3ZWxsEFN0b2NrbGFuZCwgSUwtSU4JU3RvY2t3ZWxsC1N0b25lIEJsdWZmBVN0b3J5BVN0cm9oDlN0dXJnaXMsIE1JLUlOCFN1bGxpdmFuD1N1bHBodXIgU3ByaW5ncwZTdW5tYW4IU3dlZXRzZXIKU3dpdHogQ2l0eQNUYWIHVGFtcGljbwdUYXN3ZWxsEFRlbGwgQ2l0eSwgSU4tS1kJVGVtcGxldG9uDFRlbXBsZXRvbiBORQtUZXJyZSBIYXV0ZQlUaG9ybnRvd24RVGhyZWUgT2FrcywgTUktSU4GVGlwdG9uBlRvcGVrYQlUcmFmYWxnYXIJVHVubmVsdG9uC1R3ZWx2ZSBNaWxlBVVuaW9uEVVuaW9uIENpdHksIElOLU9ICVVuaW9uZGFsZRBVbmlvbnRvd24sIElOLUtZClVuaW9udmlsbGUHVmFsZWVuZQhWYWxsb25pYQpWYWxwYXJhaXNvCVZhbiBCdXJlbgtWZWVkZXJzYnVyZwZWZWxwZW4GVmVybm9uClZlcnNhaWxsZXMSVmV2YXkgTm9ydGgsIElOLUtZElZldmF5IFNvdXRoLCBJTi1LWRBWaW5jZW5uZXMsIElOLUlMBVZvbGdhBldhYmFzaBZXYWJhc2ggSXNsYW5kLEtZLUlMLUlOBldhZGVuYQpXYWRlc3ZpbGxlCFdha2FydXNhB1dhbGRyb24JV2Fsa2VydG9uB1dhbGxhY2UHV2FuYXRhaAZXYXJyZW4GV2Fyc2F3Cldhc2hpbmd0b24IV2F0ZXJsb28MV2F5bWFuc3ZpbGxlCVdheW5ldG93bhRXZXN0IEZyYW5rbGluLCBJTi1LWQxXZXN0IExlYmFub24RV2VzdCBVbmlvbiwgSUwtSU4JV2VzdGZpZWxkCVdlc3Rwb2ludAhXZXN0cG9ydAlXZXN0dmlsbGUKV2hlYXRmaWVsZAlXaGVhdGxhbmQIV2hlZWxpbmcIV2hpdGNvbWIJV2hpdGVoYWxsEVdoaXRld2F0ZXIsIElOLU9IB1doaXRpbmcIV2lsbGlhbXMMV2lsbGlhbXNwb3J0CVdpbGxzaGlyZQ1XaWxzb24sIEtZLUlOB1dpbmFtYWMKV2luY2hlc3RlcghXaW5kZmFsbAdXaW5nYXRlB1dpbnNsb3cHV29sY290dAxXb2xjb3R0dmlsbGUVV29vZGJ1cm4gTm9ydGgsIElOLU9IFVdvb2RidXJuIFNvdXRoLCBJTi1PSAtXcmVuLCBJTi1PSAVXeWF0dBFZYW5rZWV0b3duLCBJTi1LWQZZZW9tYW4NWW91bmcgQW1lcmljYQpaYW5lc3ZpbGxlClppb25zdmlsbGUVxwUHMzgwODQ4OAczOTA4NTY4BzM5MDg1NDUHNDEwODU3OAc0MTA4NjExBzM5MDg3ODEHNDEwODU0NAc0MDA4NTM2BzM4MDg2NTgHMzkwODYxNAczOTA4NTUyBzM4MDg2MTQHNDAwODc0NQc0MDA4NTU4BzQwMDg1MjYHNDAwODUxNgc0MDA4NTc1BzQxMDg0NjgHNDEwODU2MQc0MDA4NjYzBzQwMDg2MjEHNDEwODUxMwc0MTA4NjIyBzM5MDg2MjgHNDEwODU1MQc0MDA4NzMyBzQxMDg1MzgHNDEwODUzMQczODA4NzMyBzM5MDg0MTgHMzkwODUxNwczOTA4NjUyBzM4MDg2ODQHNDEwODYyNQczOTA4NTMyBzM5MDg2MzIHMzgwODU4MQczODA4NjUyBzM4MDg2NzQHMzgwODY3NQczOTA4NjYxBzQxMDg3MzUHMzgwODYyNAczOTA4NzcxBzM5MDg2MjMHMzgwODU3Mgc0MDA4NDY4BzM4MDg1NTQHMzgwODc3Mwc0MDA4NTg1BzM4MDg2MzYHNDAwODczNQc0MDA4NTQxBzM4MDg1NjYHMzkwODYxOAczOTA4NjI1BzQwMDg1NjIHMzkwODU1OAczODA4NzEzBzM4MDg1NDgHNDAwODc1NAc0MTA4NjMxBzM4MDg2MjUHMzkwODc1MQczOTA4NzUyBzQxMDg2NDIHMzkwODY2Mwc0MTA4NTY3BzM4MDg2MjYHNDEwODU3Mgc0MDA4NjU3BzQwMDg2NjgHNDAwODY1OAczOTA4NTQxBzM5MDg2NzQHMzgwODY4MQczOTA4NTYxBzM4MDg3ODMHNDAwODY4Ngc0MDA4NjYxBzQxMDg1MjgHNDAwODY0NAc0MDA4Njc1BzQxMDg1NzMHNDAwODY2NQc0MTA4NDQ3BzQxMDg0NDgHMzkwODUxNQczNzA4Nzg3BzQxMDg0NzgHNDEwODc1NQczOTA4NTcyBzQxMDg0NzcHMzgwODY2MwczODA4NTczBzM3MDg2ODYHMzgwODc4NAc0MDA4NTExBzM5MDg2ODIHMzgwODU2MgczOTA4NTY1BzM5MDg2NDcHMzkwODc2MgczOTA4NDM4BzQxMDg1MjEHMzkwODc0MQczODA4NTQ2BzQwMDg3NDIHNDEwODc1MQczODA4NTg3BzM4MDg3MTEHNDEwODUyMwczOTA4NTQzBzM5MDg3MzEHMzkwODY2NQczOTA4NjE1BzQxMDg0NjcHMzkwODY3MwczOTA4NTc2BzM4MDg1NzQHMzkwODc2NAczOTA4NjY4BzM5MDg2NTcHMzcwODY3Ngc0MDA4NjY0BzM5MDg3MjEHMzkwODY2Ngc0MDA4NjI2BzM5MDg0NTcHNDEwODUyNAczOTA4NTI4BzM5MDg1NjIHNDEwODU3NgczOTA4NjQzBzQxMDg1NDIHMzgwODYyMQczODA4NjIyBzQwMDg0MzcHNDAwODcyNAczODA4NjMxBzQwMDg2MTgHMzgwODU4MgczODA4NTc3BzQxMDg3NDMHNDEwODYyNAczOTA4NTc4BzM4MDg2NDYHMzgwODcyNgczODA4NjI4BzM5MDg3NzQHMzkwODY3NQc0MDA4NzI1BzQwMDg3MTUHNDAwODYxNwc0MDA4NzY1BzM4MDg3MTQHMzgwODcxMgc0MDA4NDc4BzM4MDg3NTUHNDAwODY4MQc0MDA4NjU0BzQwMDg0MzgHNDAwODY1Ngc0MTA4NzIyBzQxMDg2MjYHMzkwODc0NQczODA4NjMyBzM4MDg1NzYHMzgwODYxNQczOTA4NTExBzQwMDg0ODcHNDAwODU1MQc0MTA4NjM0BzQwMDg3ODUHMzgwODY0NwczOTA4NzEzBzQxMDg3NjEHMzkwODU3NAc0MTA4NzQ1BzM4MDg3NDYHNDAwODc2NAc0MDA4NTMzBzM5MDg1MzgHNDEwODQ1Nwc0MTA4NjcxBzQxMDg1MzMHMzgwODcyNAczOTA4NTI3BzQxMDg1NjgHMzkwODYxMwc0MDA4NTM3BzM5MDg2NTYHMzcwODg4MQczODA4NjM0BzQxMDg2MzcHNDEwODcxNAczODA4NzcxBzM4MDg3MTUHMzcwODc4NQczOTA4NTUxBzQxMDg3MTMHMzkwODcyNQczOTA4NDY3BzQwMDg1NDYHMzkwODU2Mwc0MDA4NTIyBzM5MDg2ODQHMzkwODY4MQc0MDA4NjU1BzM4MDg0NzgHMzgwODcyMgc0MTA4NTU4BzM5MDg1MzUHMzcwODU4OAc0MDA4NDQ3BzQxMDg1MTEHNDEwODUxMgczOTA4NDg4BzM5MDg1NjcHNDAwODc1Mwc0MDA4Njg4BzM4MDg3MzQHNDAwODYzNQczOTA4NjQxBzQwMDg1MjcHMzgwODY0MgczOTA4NjI3BzM4MDg2NTUHMzgwODc2NAczODA4NjE3BzQwMDg2ODMHNDEwODY3NAc0MDA4NjUyBzQxMDg1MzIHNDEwODc1Mwc0MDA4NTQ1BzQwMDg1MzUHMzgwODYxNgc0MDA4NDU4BzM4MDg1MzgHMzgwODY2NQc0MTA4NzExBzQwMDg1MjUHMzgwODc1MQc0MDA4NzczBzQxMDg1NTcHMzkwODYzNgc0MTA4NDI4BzM5MDg1MjYHNDAwODY4NAczODA4NzM4BzM4MDg2NDUHMzkwODY2NwczOTA4NTc3BzM5MDg1ODEHMzkwODUzNAc0MDA4NTQ4BzM5MDg2NTEHMzkwODQyOAczOTA4NTgyBzM5MDg2NTUHNDEwODQ1OAc0MTA4NjQ1BzQxMDg2NDcHMzgwODY0MwczOTA4NDM3BzQwMDg1NDMHNDAwODU0NAczOTA4NTM2BzM4MDg3MjUHMzgwODU4Ngc0MDA4NjE1BzM4MDg3ODUHNDEwODczMgczNzA4Nzc1BzM4MDg1NTcHNDEwODQzNwc0MTA4NzU0BzM4MDg2NTYHNDAwODYzMwc0MDA4NzEyBzM5MDg2MzQHNDAwODQ4OAczODA4NzIxBzM5MDg1MTQHMzkwODQyNwczOTA4NTM3BzM5MDg3ODUHNDEwODUyMgczODA4NjM4BzQwMDg1ODQHMzgwODY2NgczOTA4NzE2BzM5MDg3MzUHMzkwODcyMwc0MDA4Njc2BzQxMDg3MjUHMzgwODY3NwczOTA4NjcxBzM5MDg2NzIHMzkwODU4Nwc0MTA4NjMyBzM4MDg3NTQHNDEwODc3NQczOTA4NTcxBzM5MDg3MjIHMzgwODY0OAczODA4NTM2BzM5MDg1MTgHMzgwODcxNgczODA4NzM3BzQwMDg2MzIHNDEwODU0MwczODA4NTY1BzQwMDg3NzQHNDEwODYxNAc0MTA4NTcxBzM5MDg3ODMHNDEwODY0Ngc0MDA4NjIzBzQwMDg2MjcHNDEwODU3NQczOTA4NTc1BzQxMDg2MzUHNDEwODYzNgc0MDA4NjQxBzQwMDg2NDIHMzgwODY4NwczODA4NTE4BzM4MDg2NjEHNDEwODczMQczODA4NjgyBzQxMDg2MzgHNDAwODU2NgczODA4NTQ0BzQxMDg2NDMHNDEwODY1Ngc0MTA4NjU3BzM4MDg2MTEHMzkwODY4Nwc0MDA4NjQ3BzQwMDg2NDgHNDEwODU2NAc0MDA4NTc2BzQxMDg3NjUHNDEwODU0Ngc0MTA4NjUzBzM4MDg1MjgHNDAwODUxNwc0MTA4NTE0BzM5MDg0MTcHMzgwODYyMwc0MDA4NjE0BzQxMDg1MzcHNDEwODcxNQc0MTA4NzMzBzM5MDg3MzMHMzkwODU0NwczNzA4Njg4BzM5MDg1NzMHMzkwODQ2OAc0MDA4NTYzBzQxMDg1NDUHNDAwODYyOAc0MDA4NTYxBzM5MDg3MTIHMzgwODU2OAczODA4NjUzBzM5MDg2ODUHNDAwODY3MwczODA4NjY4BzQxMDg1MjUHMzgwODUyNwc0MTA4NzM0BzQwMDg2NzQHNDEwODY2NAc0MDA4NDE4BzM4MDg3MjMHMzgwODc4MQc0MDA4NjgyBzM4MDg1NjMHMzgwODU2NAc0MDA4NTc0BzM5MDg1NTUHMzkwODc2MQc0MTA4NDE4BzM5MDg1NDgHNDAwODU1Ngc0MDA4NTczBzM5MDg2NDQHMzcwODY3NQczODA4NjEyBzM4MDg4MTEHNDAwODUyMQczOTA4NTY0BzM5MDg2NjIHMzkwODU4OAc0MDA4NzgxBzM5MDg3NjMHNDAwODYyNAc0MTA4NjE4BzM4MDg2NzIHNDAwODcyMgc0MTA4NjIxBzM5MDg3MTUHNDEwODUzNAczOTA4NTQyBzQwMDg2NTEHNDEwODY2Nwc0MTA4NjY4BzQwMDg2MzQHNDEwODU2Ngc0MDA4NTE1BzM5MDg1MTIHNDEwODU0Nwc0MTA4NTU2BzM5MDg1MjQHMzgwODYzMwczOTA4NTQ0BzM4MDg2NjQHMzkwODYzNQc0MDA4NTEyBzQxMDg1NjMHNDAwODY3OAc0MDA4Njg3BzM4MDg3NTMHMzkwODc3MwczODA4NzYxBzQwMDg2NzcHNDAwODY2Nwc0MDA4NTUzBzM5MDg2NTMHMzkwODY1NAczOTA4NjMzBzQwMDg3ODQHMzkwODU2Ngc0MTA4NTc3BzQwMDg3ODMHMzgwODc0Nwc0MDA4NTY1BzQwMDg3NjIHNDAwODUxMwczNzA4Nzg4BzQwMDg2MzYHNDAwODUyMwc0MDA4NTI0BzQxMDg1NDgHNDEwODY0MQczOTA4NjIyBzM4MDg1MzcHMzgwODYxMwczOTA4NjIxBzQxMDg2NzYHNDEwODY3Nwc0MTA4NjY1BzM5MDg1ODMHMzkwODU4NAc0MDA4NDU3BzM5MDg0NTgHMzkwODc1NAczODA4NzI4BzM5MDg2ODgHMzkwODQ3NwczOTA4NTMzBzM5MDg2ODYHMzkwODU1MwczODA4NTU1BzM3MDg3ODQHMzkwODc4NAc0MTA4NjcyBzQxMDg2NzMHMzkwODYzMQc0MDA4NjExBzM4MDg2ODMHNDEwODYyNwc0MTA4NjE3BzQxMDg2NTQHNDEwODUxNwc0MDA4NTg3BzM5MDg2NzYHMzkwODUxNgc0MTA4NTM2BzM4MDg3MzMHMzgwODc3NAczODA4Njc4BzQxMDg3NjIHNDEwODU1NAc0MDA4NTI4BzQwMDg2NjIHMzgwODY4NQc0MTA4NTYyBzQxMDg1MzUHNDEwODY2MQczOTA4NTIzBzQwMDg1ODIHMzgwODU1Ngc0MDA4NzQxBzM4MDg3NDEHMzgwODU0NQczNzA4NzcxBzM3MDg3NzIHMzgwODY4NgczODA4NzM2BzQxMDg3NDIHMzgwODY0MQczODA4NjU0BzM5MDg2NDUHNDEwODcxMgczODA4NzQ1BzM5MDg2MzgHMzgwODQ3NwczOTA4NTg2BzQwMDg1NDIHNDAwODU2OAc0MDA4NzE0BzQxMDg2MTMHNDAwODY3MQczODA4NzQzBzQwMDg1NTIHNDEwODUyNgczOTA4NTIyBzM5MDg3MzQHNDAwODc0MwczOTA4NjY0BzM4MDg3NzIHNDEwODYzMwc0MDA4NTgxBzQwMDg1NDcHMzkwODY0OAc0MTA4NzUyBzQwMDg0NDgHMzgwODcyNwc0MDA4NTcxBzM4MDg3MzUHNDAwODY0NgczOTA4NjQ2BzM5MDg1NTYHNDAwODUzMgczNzA4NzczBzM5MDg2NTgHMzkwODQ0Nwc0MDA4NzcyBzQwMDg3ODIHMzgwODU4MwczNzA4NzgyBzM5MDg0NzgHNDAwODU3OAc0MDA4NTMxBzQxMDg2MTYHMzgwODQ4Nwc0MDA4NTE4BzM5MDg2NzcHNDAwODU4OAc0MTA4NjEyBzM3MDg2ODEHMzcwODc4MQczOTA4NzcyBzQwMDg1NTQHMzcwODY4NQc0MDA4NjM4BzM5MDg3NTMHNDAwODYxMwc0MDA4NjQ1BzQwMDg3NTEHMzkwODU1NAczODA4NjU3BzM5MDg2NzgHMzgwODc3NQc0MDA4NjQzBzQxMDg2MjMHMzgwODYzNwczOTA4NzY1BzQxMDg0MzgHMzgwODYyNwczODA4NjUxBzM5MDg3MzIHMzgwODU4NAc0MTA4NjI4BzM4MDg3ODIHMzgwODc1MgczOTA4NzU1BzM4MDg2MTgHNDEwODcyNAczODA4Njg4BzM5MDg3NzUHMzgwODU2NwczOTA4NzQzBzQwMDg1ODYHMzgwODU4OAc0MDA4NjE2BzM5MDg3MjQHNDEwODcyMwczOTA4NTU3BzQwMDg3NzUHNDAwODYyMgc0MTA4NTY1BzM5MDg1ODUHMzgwODY2Nwc0MTA4NTE4BzM4MDg2NjIHMzcwODc3NwczODA4NzE4BzM5MDg2MTcHNDAwODU2Nwc0MTA4NjYyBzQxMDg2NjMHMzgwODU1OAc0MTA4NTE1BzQxMDg1MTYHMzkwODUzMQc0MDA4NDE3BzM4MDg1NDcHMzkwODYzNwc0MTA4NjY2BzM4MDg3NTYHNDEwODc0NAczOTA4NjE2BzQwMDg2ODUHMzkwODc0Mgc0MTA4NjU1BzQwMDg3NTUHNDAwODYzNwc0MDA4NzIzBzM5MDg2MTIHNDEwODU1Mgc0MTA4NTc0BzM5MDg3MTQHNDAwODUxNAczOTA4NTIxBzQwMDg1NTcHMzkwODcxMQc0MDA4NzQ0BzM4MDg1NzgHMzgwODYzNQczNzA4Njg3BzQwMDg3NTIHNDAwODc2MQczOTA4NzQ0BzQwMDg2MjUHNDEwODY3NQc0MDA4NjMxBzQxMDg1NTUHMzkwODY0MgczODA4NjczBzQwMDg2NzIHMzgwODc0NAc0MDA4NDI3BzQwMDg1NzIHMzcwODc3OAczOTA4NjI0BzM4MDg2NDQHMzgwODY3MQc0MTA4NzQxBzQwMDg1NTUHNDAwODcxMwczODA4NzMxBzM4MDg1ODUHMzkwODUxMwczODA4NTcxBzM4MDg1NjEHMzgwODc2NQczODA4NTc1BzQwMDg1NzcHMzcwODg3MQc0MDA4NzYzBzM4MDg3MTcHNDEwODY1MQczOTA4NTQ2BzQxMDg2NDQHMzkwODc4Mgc0MTA4NjQ4BzQwMDg1NjQHNDEwODUyNwczODA4NzYyBzQxMDg1NDEHMzkwODYxMQc0MDA4NzExBzM3MDg3ODYHNDAwODczNAczOTA4NzI2BzQwMDg2MTIHNDAwODczMQczOTA4NTI1BzQxMDg2NTgHNDEwODcyMQczODA4NzYzBzQwMDg1MzQHMzkwODQ0OAczOTA4NjI2BzM5MDg0ODcHNDEwODc2NAczODA4Njc2BzQwMDg3MzMHNDAwODQ2NwczNzA4Nzc2BzQxMDg2MTUHNDAwODQyOAc0MDA4NTM4BzQwMDg3MjEHMzgwODc0Mgc0MDA4NzcxBzQxMDg1NTMHNDEwODQyNwc0MTA4NDE3BzQwMDg0NzcHNDEwODY1MgczNzA4NzgzBzQwMDg2NjYHNDAwODY1Mwc0MDA4NTgzBzM5MDg2ODMUKwPHBWdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBZmQCEw8PZBYCHgdvbmNsaWNrBRNyZXR1cm4gc2hvd19idXN5KCk7ZAIDD2QWAgIJDxBkEBUJAARFYXN0BU5vcnRoCU5vcnRoZWFzdAlOb3J0aHdlc3QFU291dGgJU291dGhlYXN0CVNvdXRod2VzdARXZXN0FQkBMAIxMQE4AjEzAjE0ATkCMTYCMTcCMTIUKwMJZ2dnZ2dnZ2dnZGQYAQUabXN0ciRjcGhNYWluQm9keSRndlJlc3VsdHMPPCsACgEIZmTYtCSOdLq6FEsEwFQRA0XlmzGBAA=="
		
		}

		yield scrapy.FormRequest(url=init_url, callback=self.parse, headers=self.header, method="post", formdata=formdata, dont_filter=True) 

	def parse(self, response):

		loc_list =response.xpath('//table//tr//a/@href').extract()

		for loc in loc_list[0:1]:

			argument = loc.split(',')[1][1:-2]

			url = "https://secure.in.gov/apps/dnr/dowos/WaterWell.aspx"

			formdata = {

				"__EVENTTARGET":"mstr$cphMainBody$gvResults",

				"__EVENTARGUMENT":argument,

				"__LASTFOCUS":"",

				"__VIEWSTATEGENERATOR":"E4F44E51",

				"__SCROLLPOSITIONX":"0",

				"mstr$cphUserItems$ddlQSearch":"County",

				"mstr$cphMainBodyUserItems$ddlQCounty":"1",

				"mstr$cphUserItems$txtMaxNumRows":"30000",

				
				"mstr$cphUserItems$txtAddrNum":"",
				
				"mstr$cphUserItems$ddlAddrDirection":"0",
				
				"mstr$cphUserItems$txtAddrName":"",
				
				"mstr$cphUserItems$txtAddrZip":"",
				
				"mstr$cphUserItems$txtAddrMaxRows":"250",

				"__SCROLLPOSITIONY":"96.36363220214844",
				
			
			}

			yield scrapy.FormRequest(url=url, callback=self.parse_temp, headers=self.header, method="post", formdata=formdata, dont_filter=True )
			# yield scrapy.FormRequest(url=url, callback=self.parse_detail, headers=self.header, method="post", formdata=formdata, dont_filter=True )


	def parse_temp(self, response):

		yield scrapy.Request(url="https://secure.in.gov/apps/dnr/dowos/Detail.aspx", callback=self.parse_detail, dont_filter=True)


	def parse_detail(self, response):

		item = ChainItem()

		item['reference_number'] = self.validate(''.join(response.xpath('//span[@id="lblRefNum"]//text()').extract()))

		item['driving_dircetion_to_well'] = self.validate(''.join(response.xpath('//span[@id="lblDriving"]//text()').extract()))

		item['date_completed'] = self.validate(''.join(response.xpath('//span[@id="lblDateCompleted"]//text()').extract()))

		item['well_use'] = self.validate(''.join(response.xpath('//span[@id="lblWellUse"]//text()').extract()))

		item['drilling_method'] = self.validate(''.join(response.xpath('//span[@id="lblWellDrillMethod"]//text()').extract()))

		item['pump_type'] = self.validate(''.join(response.xpath('//span[@id="lblWellPumpType"]//text()').extract()))

		item['depth'] = self.validate(''.join(response.xpath('//span[@id="lblWellDepth"]//text()').extract()))

		item['pump_setting_depth'] = self.validate(''.join(response.xpath('//span[@id="lblWellPumpDepth"]//text()').extract()))

		item['water_quality'] = self.validate(''.join(response.xpath('//span[@id="lblWellQuality"]//text()').extract()))

		item['casing_length'] = self.validate(''.join(response.xpath('//span[@id="lblCasingLength"]//text()').extract()))

		item['casing_mateiral'] = self.validate(''.join(response.xpath('//span[@id="lblCasingMaterial"]//text()').extract()))

		item['casing_diameter'] = self.validate(''.join(response.xpath('//span[@id="lblCasingDia"]//text()').extract()))

		item['screen_length'] = self.validate(''.join(response.xpath('//span[@id="lblScreenLength"]//text()').extract()))

		item['screen_material'] = self.validate(''.join(response.xpath('//span[@id="lblScreenMaterial"]//text()').extract()))

		item['screen_diameter'] = self.validate(''.join(response.xpath('//span[@id="lblScreenDia"]//text()').extract()))

		item['slot_size']  = self.validate(''.join(response.xpath('//span[@id="lblScreenSlot"]//text()').extract()))

		item['type_of_test'] = self.validate(''.join(response.xpath('//span[@id="lblTypeTest"]//text()').extract()))

		item['test_rate'] = self.validate(''.join(response.xpath('//span[@id="lblTestRate"]//text()').extract()))

		item['bail_test_rate'] = self.validate(''.join(response.xpath('//span[@id="lblBailTestRate"]//text()').extract()))

		item['drawdown'] = self.validate(''.join(response.xpath('//span[@id="lblDrawdown"]//text()').extract()))

		item['static_water_level'] = self.validate(''.join(response.xpath('//span[@id="lblStaticLevel"]//text()').extract()))

		item['bailer_drawdown'] = self.validate(''.join(response.xpath('//span[@id="lblBailerDrawdown"]//text()').extract()))

		item['material'] = self.validate(''.join(response.xpath('//span[@id="lblGroutMaterial"]//text()').extract()))

		item['depth_2'] = self.validate(''.join(response.xpath('//span[@id="lblSealDepth"]//text()').extract()))

		item['installation_method'] = self.validate(''.join(response.xpath('//span[@id="lblSealMethod"]//text()').extract()))

		item['number_of_bags_used'] = self.validate(''.join(response.xpath('//span[@id="lblGroutBags"]//text()').extract()))

		item['sealing_material'] = self.validate(''.join(response.xpath('//span[@id="lblSealMaterial"]//text()').extract()))

		item['well_abandonment_depth'] = self.validate(''.join(response.xpath('//span[@id="lblSealDepth"]//text()').extract()))

		item['installation_method_2'] = self.validate(''.join(response.xpath('//span[@id="lblSealMethod"]//text()').extract()))

		item['number_of_bags_used_2'] = self.validate(''.join(response.xpath('//span[@id="lblSealBags"]//text()').extract()))

		item['county'] = self.validate(''.join(response.xpath('//span[@id="lblCounty"]//text()').extract()))

		item['township'] = self.validate(''.join(response.xpath('//span[@id="lblTownship"]//text()').extract()))

		item['range'] = self.validate(''.join(response.xpath('//span[@id="lblRange"]//text()').extract()))

		item['section'] = self.validate(''.join(response.xpath('//span[@id="lblSection"]//text()').extract()))

		item['topo_map'] = self.validate(''.join(response.xpath('//span[@id="lblTopoMap"]//text()').extract()))

		item['grant'] = self.validate(''.join(response.xpath('//span[@id="lblGrant"]//text()').extract()))

		item['field_located_by'] = self.validate(''.join(response.xpath('//span[@id="lblFieldBy"]//text()').extract()))

		item['field_located_on'] = self.validate(''.join(response.xpath('//span[@id="lblFieldOn"]//text()').extract()))

		item['courthouse_location_by'] = self.validate(''.join(response.xpath('//span[@id="lblCourthouseBy"]//text()').extract()))

		item['courthouse_location_on'] = self.validate(''.join(response.xpath('//span[@id="lblCourthouseOn"]//text()').extract()))

		item['location_accepted_verification_by'] = self.validate(''.join(response.xpath('//span[@id="lblVerificationBy"]//text()').extract()))

		item['location_accepted_verification_on'] = self.validate(''.join(response.xpath('//span[@id="lblVerificationOn"]//text()').extract()))

		item['subdivision_name'] = self.validate(''.join(response.xpath('//span[@id="lblSubdivision"]//text()').extract()))

		item['lot_number'] = self.validate(''.join(response.xpath('//span[@id="lblLotNum"]//text()').extract()))

		item['ft_w_of_el'] = self.validate(''.join(response.xpath('//span[@id="lblWofE"]//text()').extract()))

		item['ft_n_of_sl'] = self.validate(''.join(response.xpath('//span[@id="lblNofS"]//text()').extract()))

		item['ft_e_of_wl'] = self.validate(''.join(response.xpath('//span[@id="lblEofW"]//text()').extract()))

		item['ft_s_of_nl'] = self.validate(''.join(response.xpath('//span[@id="lblSofN"]//text()').extract()))

		item['ground_elevation'] = self.validate(''.join(response.xpath('//span[@id="lblGroundElev"]//text()').extract()))

		item['depth_of_bedrock'] = self.validate(''.join(response.xpath('//span[@id="lblBedrockDepth"]//text()').extract()))

		item['bedrock_elevation'] = self.validate(''.join(response.xpath('//span[@id="lblBedrockElev"]//text()').extract()))

		item['aquifer_elevation'] = self.validate(''.join(response.xpath('//span[@id="lblAquiferElev"]//text()').extract()))

		item['utm_easting'] = self.validate(''.join(response.xpath('//span[@id="lblUTMEast"]//text()').extract()))

		item['utm_northing'] = self.validate(''.join(response.xpath('//span[@id="lblUTMNorth"]//text()').extract()))

		if item['reference_number'] not in self.history:
			self.history.append(item['reference_number'])
			yield item
		# pdb.set_trace()

	# validate value for eliminate space, wordwrap, etc 

	def validate(self, item):

		try:

			return item.strip().replace('\n', '').replace('\t','').replace('\r', '')

		except:

			pass

	# select items which are not blank from the list

	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp