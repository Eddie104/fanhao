#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
根据已有的番号json文件从网络上扒取图片
'''

__author__ = "32968210@qq.com"

import json, os, requests

def mkDir(path):
	if not os.path.exists(path):
		os.mkdir(path)
	return path

def downloadImg(url, imgPath):
	print(u"开始下载图片:%s" % url)
	if os.path.exists(imgPath):
		print(u"跳过已存在图片:%s" % imgPath)
	else:
		if url != "":			
			try:
				r = requests.get(url, stream = True)
			except Exception, e:
				print e
				return
			with open(imgPath, 'wb') as f:
				for chunk in r.iter_content(chunk_size = 1024): 
					if chunk:
						f.write(chunk)
						f.flush()
		else:
			print(u"图片%s的url为空" % imgPath)

def createVideo(code, videoData):
	# "ABBA-108":[
	# 	{"group":"ABBA"}, 
	# 	{"ratings":"0"}, 
	# 	{"artists":["堀口奈津美", "白川ゆり", "星杏奈", "伊織涼子", "五十嵐まき", "安部千秋", "岩下愛"]}, 
	# 	{"title":"元○○熟女"}, 
	# 	{"genre":["熟女", "人妻", "ベスト・総集編", "4時間以上作品"]}, 
	# 	{"runing_time":"240分钟"}, 
	# 	{"publisher":"センタービレッジ"},
	# 	{"publication_date":"2012-02-23"}, 
	# 	{"description":"バレリーナ、レースクィーン、水泳インストラクターなど、様々な経歴をもつ熟女が大集合！美尻をくねらせ淫らに喘ぐ元雑誌モデルの奥さまや、エステティシャンの技で男優を腰砕けにする奥さまをはじめ、華麗なキャリアの熟女10人が乱れまくる！"}, 
	# 	{"cover_s":"http://pics.dmm.co.jp/mono/movie/adult/h_086abba108/h_086abba108ps.jpg"}, 
	# 	{"cover_l":"http://pics.dmm.co.jp/mono/movie/adult/h_086abba108/h_086abba108pl.jpg"}, 
	# 	{"scrots":[""]}, 
	# 	{"google_cache_dmm_url":"http://webcache.googleusercontent.com/search?q=cache:_7NGeb7sJJIJ:www.dmm.co.jp/mono/dvd/-/detail/%3D/cid%3Dh_086abba108"}
	# ]
	print(u"创建文件夹:%s" % code)
	mkDir("video/%s" % code)
	jsonText = "{\n"
	for data in videoData:
		if "cover_s" in data:
			downloadImg(data["cover_s"], "video/%s/%ss.jpg" % (code, code))
		elif "cover_l" in data:
			downloadImg(data["cover_l"], "video/%s/%sl.jpg" % (code, code))
		elif "artists" in data:
			jsonText += "\"actress\":["
			for a in data["artists"]:
				jsonText += "\"%s\"," % a
			jsonText += "],\n"
		elif "title" in data:
			jsonText += "\"title\":\"%s\",\n" % data["title"]
		elif "genre" in data:
			jsonText += "\"classType\":["
			for c in data["genre"]:
				jsonText += "\"%s\"," % c
			jsonText += "],\n"
		elif "publication_date" in data:
			jsonText += "\"date\":\"%s\",\n" % data["publication_date"]
	jsonText += "}"
	f = open("video/%s/%s.json" % (code, code), "wb")
	f.write(jsonText.encode("utf-8"))
	f.close()

if __name__ == '__main__':
	# 读取存贮着大量番号的json文件
	f = open("test.json")
	jsonText = f.read()
	f.close()

	jsonText = json.loads(jsonText)
	for k, v in jsonText.items():
		createVideo(k, v)

	print(u"搞定")