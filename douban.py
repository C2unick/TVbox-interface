#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

host_url = 'https://movie.douban.com/j'
apikey = "?apikey=0ac44ae016490db2204ce0a042db2916"

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "豆瓣"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"剧集": "剧集",
			"电影": "电影",
			"综艺": "综艺",
			"动漫": "动漫",
			"纪录片": "纪录片",
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		url = host_url + '/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=15&page_start=0' 
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		joList = jo.get("subjects")
		lists = []
		for item in joList:
			rating = item['rate']
			lists.append({
				"vod_id": item.get("id", ""),
				"vod_name": item['title'],
				"vod_pic": item['cover'],
				"vod_remarks": rating
			})
		result = {
			'list':lists
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):		
		limit=40
		result = {}
		# if extend:
		# 	sort = extend.pop('sort') if "sort" in extend else "T"
		# 	genres=""
		# 	countries=""
		# 	year_range=""
		# 	sort = extend.pop('sort') if "sort" in extend else "T"
		# 	tags = ",".join(item for item in extend.values())
		# else:
		sort = extend.pop('sort') if "sort" in extend else ""
		genres=""
		countries=""
		year_range=""
		if tid=="电影":
			tag="电影"
		elif tid=="剧集":
			tag="电视剧"
		elif tid=="综艺":
			tag="综艺"
		elif tid=="动漫":
			tag="动漫"
		elif tid=="纪录片":
			tag="纪录片"
		url=host_url +"/new_search_subjects?&range=0,10"+"&sort="+sort+"&genres="+genres+"&countries="+countries+"&year_range"+year_range+"&start="+str((int(pg) - 1) * limit)+"&limit="+str(limit)+"&tags="+tag
		rsp = self.fetch(url,headers=self.header)

		jo = json.loads(rsp.text)
		jolist = jo["data"]

		videos = []
		for vod in jolist:
			rating = vod.get("rate", "")
			pic = vod.get("cover", "")
			videos.append({
				"vod_id": vod.get("id", ""),
				"vod_name": vod['title'],
				"vod_pic": pic,
				"vod_remarks": rating
			})

		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = limit
		result['total'] = 999999
		return result

	def detailContent(self,array):
		pass
	def searchContent(self,key,quick):
		pass
	def playerContent(self,flag,id,vipFlags):
		pass

	config = {
		"player": {},
		"filter": {
           
            "电影":[
                {"key":"类型","name":"类型","value":[{"n":"全部类型","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"动作","v":"动作"},{"n":"科幻","v":"科幻"},{"n":"动画","v":"动画"},{"n":"悬疑","v":"悬疑"},{"n":"犯罪","v":"犯罪"},{"n":"惊悚","v":"惊悚"},{"n":"冒险","v":"冒险"},{"n":"音乐","v":"音乐"},{"n":"历史","v":"历史"},{"n":"奇幻","v":"奇幻"},{"n":"恐怖","v":"恐怖"},{"n":"战争","v":"战争"},{"n":"传记","v":"传记"},{"n":"歌舞","v":"歌舞"},{"n":"武侠","v":"武侠"},{"n":"情色","v":"情色"},{"n":"灾难","v":"灾难"},{"n":"西部","v":"西部"},{"n":"纪录片","v":"纪录片"},{"n":"短片","v":"短片"}]},
                {"key":"地区","name":"地区","value":[{"n":"全部地区","v":""},{"n":"华语","v":"华语"},{"n":"欧美","v":"欧美"},{"n":"韩国","v":"韩国"},{"n":"日本","v":"日本"},{"n":"中国大陆","v":"中国大陆"},{"n":"美国","v":"美国"},{"n":"中国香港","v":"中国香港"},{"n":"中国台湾","v":"中国台湾"},{"n":"英国","v":"英国"},{"n":"法国","v":"法国"},{"n":"德国","v":"德国"},{"n":"意大利","v":"意大利"},{"n":"西班牙","v":"西班牙"},{"n":"印度","v":"印度"},{"n":"泰国","v":"泰国"},{"n":"俄罗斯","v":"俄罗斯"},{"n":"加拿大","v":"加拿大"},{"n":"澳大利亚","v":"澳大利亚"},{"n":"爱尔兰","v":"爱尔兰"},{"n":"瑞典","v":"瑞典"},{"n":"巴西","v":"巴西"},{"n":"丹麦","v":"丹麦"}]},
                {"key":"sort","name":"排序","value":[{"n":"近期热度","v":"T"},{"n":"首映时间","v":"R"},{"n":"高分优先","v":"S"},{"n":"综合","v":"U"}]},
                {"key":"年代","name":"年代","value":[{"n":"全部年代","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2010年代","v":"2010年代"},{"n":"2000年代","v":"2000年代"},{"n":"90年代","v":"90年代"},{"n":"80年代","v":"80年代"},{"n":"70年代","v":"70年代"},{"n":"60年代","v":"60年代"},{"n":"更早","v":"更早"}]}],
            
            "剧集":[
                {"key":"类型","name":"类型","value":[{"n":"不限","v":""},{"n":"电视剧","v":"电视剧"},{"n":"综艺","v":"综艺"}]},
                {"key":"电视剧形式","name":"电视剧形式","value":[{"n":"不限","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"悬疑","v":"悬疑"},{"n":"动画","v":"动画"},{"n":"武侠","v":"武侠"},{"n":"古装","v":"古装"},{"n":"家庭","v":"家庭"},{"n":"犯罪","v":"犯罪"},{"n":"科幻","v":"科幻"},{"n":"恐怖","v":"恐怖"},{"n":"历史","v":"历史"},{"n":"战争","v":"战争"},{"n":"动作","v":"动作"},{"n":"冒险","v":"冒险"},{"n":"传记","v":"传记"},{"n":"剧情","v":"剧情"},{"n":"奇幻","v":"奇幻"},{"n":"惊悚","v":"惊悚"},{"n":"灾难","v":"灾难"},{"n":"歌舞","v":"歌舞"},{"n":"音乐","v":"音乐"}]},
                {"key":"综艺形式","name":"综艺形式","value":[{"n":"不限","v":""},{"n":"真人秀","v":"真人秀"},{"n":"脱口秀","v":"脱口秀"},{"n":"音乐","v":"音乐"},{"n":"歌舞","v":"歌舞"}]},
                {"key":"地区","name":"地区","value":[{"n":"全部地区","v":""},{"n":"华语","v":"华语"},{"n":"欧美","v":"欧美"},{"n":"国外","v":"国外"},{"n":"韩国","v":"韩国"},{"n":"日本","v":"日本"},{"n":"中国大陆","v":"中国大陆"},{"n":"中国香港","v":"中国香港"},{"n":"美国","v":"美国"},{"n":"英国","v":"英国"},{"n":"泰国","v":"泰国"},{"n":"中国台湾","v":"中国台湾"},{"n":"意大利","v":"意大利"},{"n":"法国","v":"法国"},{"n":"德国","v":"德国"},{"n":"西班牙","v":"西班牙"},{"n":"俄罗斯","v":"俄罗斯"},{"n":"瑞典","v":"瑞典"},{"n":"巴西","v":"巴西"},{"n":"丹麦","v":"丹麦"},{"n":"印度","v":"印度"},{"n":"加拿大","v":"加拿大"},{"n":"爱尔兰","v":"爱尔兰"},{"n":"澳大利亚","v":"澳大利亚"}]},
                {"key":"sort","name":"排序","value":[{"n":"近期热度","v":"T"},{"n":"首播时间","v":"R"},{"n":"高分优先","v":"S"},{"n":"综合","v":"U"}]},
                {"key":"年代","name":"年代","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2010年代","v":"2010年代"},{"n":"2000年代","v":"2000年代"},{"n":"90年代","v":"90年代"},{"n":"80年代","v":"80年代"},{"n":"70年代","v":"70年代"},{"n":"60年代","v":"60年代"},{"n":"更早","v":"更早"}]},
                {"key":"平台","name":"平台","value":[{"n":"全部","v":""},{"n":"腾讯视频","v":"腾讯视频"},{"n":"爱奇艺","v":"爱奇艺"},{"n":"优酷","v":"优酷"},{"n":"湖南卫视","v":"湖南卫视"},{"n":"Netflix","v":"Netflix"},{"n":"HBO","v":"HBO"},{"n":"BBC","v":"BBC"},{"n":"NHK","v":"NHK"},{"n":"CBS","v":"CBS"},{"n":"NBC","v":"NBC"},{"n":"tvN","v":"tvN"}]}],
            
			}
	}
	header = {
		"Host": "movie.douban.com",
		"Connection": "Keep-Alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 Edg/109.0.1518.69"
	}

	def localProxy(self,param):
		pass