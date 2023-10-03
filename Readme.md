# SimpleGuru

在SG租房时，我想大家一定对某Guru有很多想吐槽的地方，包括但不限于：
- 不能按照房间类型搜索
- Filter功能辣鸡
- 无法进行排序
- 性别/种族歧视
- 隐藏房源数目有上限限制

本项目能够帮助你把某Guru上的搜索结果汇总起来，按照我们设定的标准给房源打分，直接将top-tier房源呈现给我们，大大减少我们浪费在手动浏览上的成本。

## Supporting Platform

本项目暂时只支持 Mac + Safari . 

## Workflow
1. 注册Google Map API，填到config['google_map_key']
2. 去某Guru, 填写你需要的房间信息，搜索，复制结果页的url，填到config['index_url']。
4. Crawl index info
5. Parse the index info
6. Crawl all property info according to the index info
7. Parse the property info
8. Compute augmenting features for all properties.
9. Rank properties, save to the final output file.

## 注意
最短路径使用[Google Map Route API](https://developers.google.com/maps/documentation/routes/transit-route) 获取。你需要申请Google Map API来使用该项目。注册账号后，将key填入config文件中。好消息：有免费额度。