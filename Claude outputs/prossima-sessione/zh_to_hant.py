# Converte lavori_lingua_zh.py in lavori_lingua_zh_hant.py (cinese tradizionale, lessico Taiwan)
import os, re
R = os.path.join(os.path.dirname(__file__), '..', '..', 'strumenti')
s = open(os.path.join(R, 'lavori_lingua_zh.py'), encoding='utf-8').read()
FR = [('意大利','義大利'),('视频','影片'),('信息','資訊'),('定制','訂製'),('制作','製作'),('制造','製造'),('干燥','乾燥'),('干净','乾淨'),
      ('回复','回覆'),('重复','重複'),('联系','聯繫'),('标志','標誌'),('茶几','茶@@'),('哪里','哪裡'),('这里','這裡'),('里面','裡面'),('细致','細緻')]
for a,b in FR: s = s.replace(a,b)
SIMP = '与业丝两个为举么书于亚从们价会体余侧储养内写军农决况准几划则办务动区医却历压厨参发变叠台后吗团园围国图场坏块坞墙处备复头实对导将尔尝层帘带干并库应开张录悬户护报择挂据摄摆摇数时显术机杆条来构柜标样楼横欧气汇没浅游满灯灵点独狭环现电画疗着确积称简类红纹组细织绍经结绕给统绪续绿缝罗联脚节获营蓝装见视览计认议讲设访评诉译话详语说请读调谈谢负责货资赏赛车转输边过还这进远连迹选邮采里钢钥铝铬铺销锚镀镂长门闭问间阅队阶陈隐难雾页顶项顺须预频题颜饰馆马齐龛'
TRAD = '與業絲兩個為舉麼書於亞從們價會體餘側儲養內寫軍農決況準幾劃則辦務動區醫卻歷壓廚參發變疊臺後嗎團園圍國圖場壞塊塢牆處備複頭實對導將爾嘗層簾帶乾並庫應開張錄懸戶護報擇掛據攝擺搖數時顯術機桿條來構櫃標樣樓橫歐氣匯沒淺遊滿燈靈點獨狹環現電畫療著確積稱簡類紅紋組細織紹經結繞給統緒續綠縫羅聯腳節獲營藍裝見視覽計認議講設訪評訴譯話詳語說請讀調談謝負責貨資賞賽車轉輸邊過還這進遠連跡選郵採裡鋼鑰鋁鉻鋪銷錨鍍鏤長門閉問間閱隊階陳隱難霧頁頂項順須預頻題顏飾館馬齊龕'
assert len(SIMP) == len(TRAD), (len(SIMP), len(TRAD))
s = s.translate(str.maketrans(SIMP, TRAD)).replace('茶@@', '茶几')
s = s.replace("LANG = 'zh'; HREFLANG = 'zh-Hans'", "LANG = 'zh-hant'; HREFLANG = 'zh-Hant'").replace('zh_CN', 'zh_TW')
s = s.replace('/zh/', '/zh-hant/').replace("'zh/", "'zh-hant/").replace("'zh')", "'zh-hant')")
s = s.replace('簡體中文', '繁體中文').replace('cinese semplificato', 'cinese tradizionale')
open(os.path.join(R, 'lavori_lingua_zh_hant.py'), 'w', encoding='utf-8').write(s)
print('ok')
