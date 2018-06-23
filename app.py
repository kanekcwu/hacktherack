from flask import Flask, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
import numpy as np
import pandas as pd

data = pd.read_csv('Output.csv')
prod_counts_dict = OrderedDict(data['Prod Name (Chi)'].value_counts()[:300])

prod_tags_dict = {'ASAHIWONDA極濃黑啡400毫升': ['coffee', 'black', 'asahiwonda'],
 'BIC-XP2電子打火機': ['lighter', 'bic', 'xp2'],
 'BIC圖案火機': ['lighter', 'bic'],
 'C&C提子口味碳酸飲品500毫升': ['c&c',
  'grape',
  'cold',
  'energy',
  'drink',
  'energy_drink'],
 'COCOWAY 100% 椰子水350毫升': ['coconut', 'juice', 'cocoway'],
 'COOL 清涼水 500毫升樽裝': ['water', 'cool', 'bottle'],
 'COOL 清涼水 750毫升樽裝': ['water', 'cool', 'bottle'],
 'DRY 薄荷 萬寶路': ['dry', 'cigarette', 'marlboro', 'mint'],
 'E-ZONE': ['magazine', 'technology'],
 'I MONEY': ['magazine', 'finance'],
 'IF 100% 椰青水 350毫升': ['if', 'coconut', 'juice'],
 'K 1664 白啤酒500毫升罐裝': ['K1664', 'beer', '500ml', 'cold'],
 'M3 健牌': ['cigarette', 'Kent', 'white'],
 'MEVIUS 薄荷晶選 5毫克': ['mint', 'menthol'],
 'MX 萬寶路': ['cigarette', 'red'],
 'POKKA四洲咖啡': ['pokka', 'hot', 'cold', 'coffee'],
 'QB夾心飛碟(阿華田脆脆)': ['crunchy', 'ahwata', 'qb', 'sandwich', 'cold'],
 'QB火腿芝士夾心飛碟': ['sandwich', 'ham', 'cheese', 'qb', 'cold'],
 'QB肉鬆夾心飛碟': ['qb', 'floss', 'sandwich', 'cold'],
 'SPLASH紫冰萬寶路': ['splash', 'marlboro'],
 'TVB週刊': ['tvb', 'magazine'],
 'U MAGAZINE': ['u', 'magazine'],
 '三得利.C.C.檸檬飲料500毫升': ['cc', 'lemon', 'juice', 'cold', 'lemon_juice'],
 '中華硬盒廿支裝': ['cigarette', 'china'],
 '丹麥條-熟包(FD)': ['bun', 'denmark', 'bread'],
 '伊藤園綠茶500毫升': ['green', 'tea', 'japanese'],
 '信報': ['newspaper', 'news'],
 '健力士黑啤罐裝': ['black', 'beer', 'cold'],
 '健達朱古力4條裝50克': ['chocolate', 'milk', 'chocolate_bar'],
 '健達繽紛樂朱古力2條裝43克': ['chocolate bar', 'kinder', 'milk', 'chocolate'],
 '健達繽紛樂白朱古力2條裝39克': ['chocolate bar', 'chocolate', 'milk', 'kinder', 'white'],
 '健達繽紛樂黑朱古力2條裝43克': ['kinder', 'black', 'chocolate', 'milk'],
 '利賓納原味500亳升樽裝': ['purple', 'cold', 'ribena'],
 '加系可口可樂膳食纖維(無糖)500毫升': ['black',
  'cold',
  'healthy',
  'coke',
  'sugar-less',
  'white'],
 '十字牌純．凝酪120克': ['yoga', 'white', 'cross'],
 '十字牌高鈣低脂牛奶236毫升盒裝': ['milk',
  'trappist dairy',
  'box',
  'low-fat',
  'hi-cal',
  'cold',
  'hot',
  'fresh'],
 '十字牌高鈣脫脂牛奶飲品236毫升': ['milk',
  'trappist dairy',
  'box',
  'no fat',
  'high calcium',
  'cold',
  'hot',
  'fresh'],
 '十字牌鮮奶 946毫升  盒庄': ['milk', 'trappist dairy', 'box', 'cold', 'hot', 'fresh'],
 '十字牌鮮奶236毫升盒裝': ['milk', 'trappist dairy', 'box', 'cold', 'hot', 'fresh'],
 '印尼撈麵': ['noodle', ''],
 '可口可樂 192毫升細樽庄': ['cola'],
 '可口可樂 330毫升罐裝': ['cola', 'cold', 'red', 'black'],
 '可口可樂 500毫升樽裝': ['cola', 'cold', 'red', 'black'],
 '可口可樂888毫升膠樽裝': ['cola'],
 '吞拿魚粟米蘑菇包(FD)-熟包': ['bread', 'fishball', 'corn', 'mushroom'],
 '咖喱魚蛋10粒': ['fishball', 'yellow', 'curry'],
 '喜力KING CAN罐裝': ['heineken', 'king', 'can', 'green', 'cold'],
 '嘉士伯啤酒罐裝': ['beer', 'cold'],
 '嘉士伯大罐裝500毫升': ['beer', 'carlsberg', 'cold', 'green'],
 '嘉頓切邊三文治方飽': ['garden', 'sandwich', 'bread'],
 '嘉頓小平方飽': ['garden', 'bread'],
 '嘉頓朱古力忌廉檳': ['garden', 'chocolate'],
 '嘉頓朱古力瑞士卷': ['garden', 'chocolate'],
 '嘉頓朱古力雪芳蛋糕': ['garden', 'chocolate'],
 '嘉頓檸檬瑞士卷': ['garden', 'lemon'],
 '嘉頓檸檬雪芳蛋糕': ['garden', 'lemon'],
 '嘉頓櫻桃提子孖寶蛋糕': ['garden'],
 '嘉頓芒果瑞士卷': ['garden', 'mango', 'spring', 'roll'],
 '嘉頓花生忌廉檳': ['garden', 'peanut', 'cream'],
 '嘉頓花生瑞士卷': ['garden', 'peanut', 'swiss', 'roll'],
 '大發鱈魚絲8克': ['snack', 'plastic package', 'orange', 'blue', 'fish'],
 '天藍萬事發硬盒': ['cigarette', 'blue'],
 '媽咪雞汁伊麵60克': ['snack', 'noodle', 'orange'],
 '子母天然純牧原味牛奶225毫升': ['white', 'milk', 'dutch lady', 'cold'],
 '子母天然純牧朱古力牛奶225毫升': ['brown', 'milk', 'dutch lady', 'cold'],
 '寶礦力 500毫升樽裝': ['blue', 'pocari', 'energy', 'energy_drink', 'drink', 'cold'],
 '寶礦力水特樽裝900毫升': ['pocari', 'water', 'bottle', 'cold'],
 '專業馬訊-排位版': ['horse', 'position', 'gambling'],
 '專業馬訊-賠率版': ['horse', 'odds', 'gambling'],
 '屈臣氏加礦蒸餾水800毫升樽裝': ['watsons', 'water', 'bottle', 'cold'],
 '屈臣氏蒸餾水 430毫升樽庄': ['green', 'water', 'cold', 'waston'],
 '屈臣氏蒸餾水 800毫升樽庄': ['green', 'water', 'cold', 'waston'],
 '屈臣氏蒸餾水1.25公升樽庄': ['watsons', 'water', 'bottle', 'cold'],
 '屈臣氏蒸餾水280毫升樽庄': ['watsons', 'water', 'bottle', 'cold'],
 '屈臣氏蜂蜜水玫瑰花味400毫升': ['watsons', 'sweet', 'rose', 'bottle', 'cold'],
 '得寶抗菌倍護濕紙巾': ['tempo', 'blue', 'tissue', 'wet'],
 '得寶迷你紙巾(冰爽薄荷味) 單包裝': ['mint',
  'cold',
  'plastic package',
  'tissue',
  'tempo',
  'blue'],
 '得寶迷你紙巾(原味)單包裝': ['plastic package', 'tissue', 'tempo', 'blue', 'mini'],
 '得寶迷你紙巾(茉莉花味)單包裝': ['plastic package',
  'tissue',
  'tempo',
  'blue',
  'jasmine',
  'mini'],
 '得寶迷你紙巾(蘋果木香味)單包裝': ['apple', 'tempo', 'tissue', 'mini', 'plastic package'],
 '成報': ['news', 'newspaper'],
 '明報': ['newspaper', 'news'],
 '明報周刊': ['magazine', 'news'],
 '易極無糖薄荷糖34克裝-強勁薄荷味': ['mint', 'strong'],
 '易極薄荷珠薄荷檸檬味45克': ['mint'],
 '星島日報每份': ['newspaper', 'news'],
 '景田礦泉水570毫升': ['water', 'cold'],
 '朝日啤酒(大)500毫升罐裝': ['beer'],
 '東周刊': [],
 '東方新地': ['magazine'],
 '東方日報每份': ['newspaper', 'news'],
 '板町烏龍茶 800毫升': ['brown', 'oolong', 'tea', 'healthy'],
 '果蔬生活100甘筍混合汁280毫升樽': ['red', 'healthy'],
 '水動樂等滲補水飲品500毫升樽裝': ['sport', 'healthy'],
 '法國EVIAN礦泉水0.5公升樽裝': ['water', 'franch', 'evian'],
 '津路烏龍茶 900毫升  樽庄 (12)': ['brown', 'tea', 'cold', 'oolong', 'healthy'],
 '津路烏龍茶500毫升樽庄': ['brown', 'tea', 'cold', 'oolong', 'healthy'],
 '海苔肉鬆卷-熟包(FD)': ['bread', 'green'],
 '淳茶大紅袍 烏龍茶 500 毫升膠樽': ['brown', 'healthy', 'cold', 'hot'],
 '淳茶大紅袍 烏龍茶 920 毫升膠樽': ['brown', 'healthy', 'cold', 'hot'],
 '淳茶綠茶 銀毫茉莉 500 毫升膠樽': ['brown', 'healthy', 'cold', 'hot'],
 '淳茶綠茶 銀毫茉莉 920 毫升膠樽': ['brown', 'healthy', 'cold', 'hot'],
 '淳茶舍日式綠茶飲料(無糖) 920毫升膠樽裝': ['green', 'healthy', 'cold', 'hot'],
 '淳茶舍消茶普洱茶500毫升': ['brown', 'healthy', 'cold', 'hot'],
 '淳茶舍錫蘭紅茶(無糖)500毫升': ['red', 'healthy', 'cold', 'hot'],
 '清熱酷綠涼茶350毫升樽裝': ['green', 'healthy', 'cold', 'hot'],
 '清熱酷草本檸檬350毫升樽裝': ['lemon', 'healthy', 'cold', 'hot'],
 '火腿芝士軟包(FD)-熟包': ['bread', 'cheese', 'hot'],
 '燒賣10粒': ['dimsum', 'hot'],
 '燒賣5粒': ['dimsum', 'hot'],
 '燕京純生啤酒巨罐500毫升': ['brown', 'beer', 'cold'],
 '爆姝藍 威豪': ['cigarette', 'blue'],
 '爆珠紅 威豪': ['cigarette', 'red'],
 '爽浪SUPER無糖香口珠18粒袋庄': ['mint', 'green', 'blue'],
 '爽浪SUPER無糖香口珠清甜薄荷味10粒': ['mint', 'green', 'blue'],
 '爽浪無糖香口珠 10粒 條庄': ['mint', 'green', 'blue'],
 '爽浪無糖香口珠20粒袋庄': ['mint', 'green', 'blue'],
 '牛奶公司鮮奶盒裝    946ML': ['milk', 'white'],
 '特纖幼 卡碧': [],
 '獅威啤酒4罐裝': [],
 '獅威啤酒罐裝': ['gold', 'beer', 'cold', ''],
 '獅威大罐裝500毫升': ['gold', 'beer', 'cold'],
 '玉泉忌廉 500毫升樽裝': ['cream', 'soda', 'cold', 'soft', 'drink', 'green'],
 '珍寶珠': [],
 '珍珍三文魚壽司味薯片52.5克': ['chips', 'salmon', 'Green', 'jacknjill'],
 '珍珍章魚小丸子薯片52.5克': ['chips', 'octopus', 'jacknjill', 'brown', 'yellow'],
 '理的口罩(大)-包 18CM X 9CM': ['mask', 'large', 'health'],
 '生力 KING CAN 500毫升罐裝': ['beer', 'can', 'san', 'yellow', 'cold'],
 '生力啤酒 330毫升罐裝': ['beer', 'can', 'san', 'yellow', 'cold'],
 '白健 1 MG 健牌': ['kent', 'blue', 'cigarette'],
 '白金 萬寶路': ['cigarette', 'gold', 'marlboro'],
 '白銀 萬寶路': ['cigarette', 'silver', 'marlboro'],
 '百福高鈣低糖鮮豆漿 236 毫升盒裝': ['white', 'hi-cal', 'soy', 'cold'],
 '百福鮮豆漿 236 毫升盒裝': ['white', 'soy', 'cold'],
 '皇牌鮮奶球(FD)-熟包': ['hot', 'milk', 'bun'],
 '益力多5支裝': ['healthy', 'bottle', 'yakult'],
 '益達曬駱駝清甜薄荷8粒庄無糖香口珠': ['white', 'sugar free', 'chewing cum', 'extra'],
 '硬盒 萬寶路': ['cigarette', 'box', 'marlboro'],
 '硬盒芙蓉王(金)': ['cigarette', 'box'],
 '硬盒萬事發一毫克': ['cigarette', 'box', 'blue'],
 '硬盒萬事發薄荷晶選1毫克': ['cigarette', 'box', 'blue', 'mint'],
 '硬盒萬事發薄荷晶選8毫克': ['cigarette', 'box', 'blue', 'mint'],
 '紅牛強態飲品罐裝': ['red bull', 'blue', 'red', 'can', 'energy'],
 '紅牛能量飲料355ML': ['red bull', 'blue', 'red', 'can', 'energy'],
 '純雞蛋蛋糕': ['egg', 'cake', 'yellow'],
 '紫薄1 健牌': ['cigarette', 'kent', 'blue'],
 '經濟日報每份': ['newspaper', 'news'],
 '綠 LUCKY': ['white', 'green', 'lucky', 'cigarette'],
 '維他低糖朱古力牛奶250毫升紙包': ['vita', 'chocolate', 'milk', 'healthy', 'brown'],
 '維他低糖檸檬茶375毫升紙包裝': ['vita', 'lemon', 'tea', 'healthy', 'yello', 'brown'],
 '維他奶 375毫升紙包庄': ['vita', 'milk', 'white'],
 '維他奶250毫升紙包': ['vita', 'milk', 'white'],
 '維他奶低糖豆奶375毫升紙包庄': ['vita', 'healthy', 'milk', 'white'],
 '維他奶低糖麥精豆奶375毫升紙包庄': ['vita', 'healthy', 'soy', 'bean', 'brown'],
 '維他奶山水低糖鮮豆漿236毫升盒裝': ['vita', 'heathy', 'milk', 'brown', 'soy'],
 '維他奶山水低糖黑豆漿236毫升盒裝': ['vita', 'milk', 'soy', 'healthy', 'black'],
 '維他奶山水豆漿236毫升盒裝': ['vita', 'soy', 'milk', 'white'],
 '維他奶朱古力荳奶375毫升包庄': ['vita', 'milk', 'chocolate', 'soy', 'brown'],
 '維他奶豆奶480毫升膠樽裝': ['vita', 'milk', 'bottle', 'white'],
 '維他日式桃茶500毫升': ['vita', 'japan', 'peach', 'tea', 'brown'],
 '維他朱古力奶250毫升紙包': ['vita',
  'chocolate',
  'milk',
  'chocolate_milk',
  'cold',
  'hot',
  'brown'],
 '維他朱古力牛奶 236 毫升盒裝': ['vita', 'chocolate', 'milk', 'brown'],
 '維他檸檬茶 250毫升紙包裝': ['vita', 'lemon', 'tea', 'brown'],
 '維他檸檬茶375毫升紙包裝': ['vita',
  'lemon',
  'tea',
  'lemon_tea',
  'cold',
  'yellow',
  'brown'],
 '維他檸檬茶飲品500毫升膠樽裝': ['vita',
  'lemon',
  'tea',
  'lemon_tea',
  'cold',
  'bottle',
  'yellow',
  'brown'],
 '維他港式奶茶250毫升': ['vita', 'hongkong', 'milk', 'tea', 'brown'],
 '維他港式奶茶375毫升': ['vita', 'hongkong', 'milk', 'tea', 'brown'],
 '維他港式奶茶樽裝480毫升': ['vita', 'hongkong', 'milk', 'bottle', 'white'],
 '維他無糖香片茶飲品500毫升膠樽裝': ['vita', 'healthy', 'tea', 'Scented', 'brown'],
 '維他純蒸溜水700毫升樽裝': ['vita', 'water', 'bottle'],
 '維他芒果汁飲品375毫升包庄': ['vita', 'mango', 'juice', 'yellow'],
 '維他菊花茶 375毫升紙包裝': ['vita', 'Chryysamthemum', 'tea', 'yellow'],
 '維他菊花茶500毫升樽裝': ['vita', 'Chryysamthemum', 'tea', 'bottle', 'yellow'],
 '維他蒸餾水 430毫升膠樽裝': ['vita', 'water', 'bottle'],
 '維他蜜糖檸檬茶500毫升樽裝': ['vita', 'lemon', 'tea', 'holly', 'bottle', 'brown'],
 '維他蜜糖菊花茶500毫升樽裝': ['vita', 'holly', 'Chryysamthemum', 'tea', 'brown'],
 '維他蜜糖菊花茶飲品375毫升紙包裝': ['vita', 'holly', 'Chryysamthemum', 'tea', 'brown'],
 '維他鈣思寶大豆高鈣原味375毫升': ['vita', 'milk', 'bean', 'high-cal', 'white'],
 '維他鈣思寶大豆高鈣燕麥味375毫升': ['vita', 'milk', 'bean', 'high-cal', 'brown'],
 '維他鈣思寶杏仁高鈣375毫升': ['vita', 'milk', 'nut', 'high-cal', 'white'],
 '維他錫蘭檸檬茶飲品375毫升紙包庄': ['vita',
  'lemon',
  'tea',
  'lemon_tea',
  'cold',
  'yellow',
  'brown'],
 '維他高鈣低脂朱古力奶236毫升盒裝': ['vita',
  'milk',
  'high-cal',
  'low-fat',
  'chocolate',
  'brown'],
 '維他高鈣低脂牛奶236毫升盒裝': ['vita', 'milk', 'high-cal', 'low-fat', 'white'],
 '維他高鈣牛奶飲品236毫升盒裝': ['vita', 'milk', 'white', 'high-cal'],
 '維記原味乳酪飲品220克': ['vita', 'yogurt', 'white'],
 '維記朱古力低脂牛奶225毫升樽裝': ['vita', 'chocolate', 'low-fat', 'milk', 'bottle'],
 '維記特濃朱古力低脂牛奶飲品236毫升盒裝': ['vita', 'chocolate', 'low-fat', 'milk', 'brown'],
 '維記雪米米茲-雲呢拿': ['vita', 'white', 'mochi', 'ice-cream', 'vanilla'],
 '維記雪米米茲-香芋': ['vita', 'mochi', 'ice-cream', 'purple'],
 '維記高鈣低脂奶946毫升': ['vita', 'high-cal', 'low-fat', 'milk'],
 '維記高鈣低脂牛奶225毫升樽裝': ['vita', 'high-cal', 'low-fat', 'milk', 'bottle', 'white'],
 '維記高鈣低脂牛奶236毫升盒裝': ['green', 'milk', 'hi-cal', 'low-fat'],
 '維記高鈣脫脂牛奶236毫升盒裝': ['vita', 'high-cal', 'low-fat', 'milk', 'white'],
 '維記鮮奶225毫升樽裝': ['red', 'milk'],
 '維記鮮奶236毫升盒裝': ['red', 'milk'],
 '維記鮮牛奶946毫升': ['milk'],
 '總督': ['viceroy', 'cigarette', 'red'],
 '美果蘋果紅茶430毫升': ['telford', 'apple', 'red', 'tea', 'cold'],
 '美果蜜桃紅茶430毫升': ['telford', 'pink', 'peach', 'tea', 'cold'],
 '美粒果橙汁飲品420毫升樽裝': ['orange', 'orange_juice', 'bottle'],
 '美粒果蘆薈粒青提子汁飲品420毫升樽裝': ['minute maid', 'aloe', 'grape', 'green', 'cold'],
 '聖安娜香蕉毛巾蛋糕': ['sthonore', 'banana', 'cake', 'yellow', 'cold'],
 '能得利黑加侖子軟糖52.5克條庄': ['frutips', 'sweet', 'candy', 'grape', 'black', 'purple'],
 '腸粉4條': ['roll', 'white', 'hot'],
 '菜肉包-新': ['dim sum', 'hot', 'bun'],
 '萬事發碧絲夢': ['cigarettes', 'pianissimo', 'pink'],
 '萬事發綠沙龍': ['cigarettes', 'pianissimo', 'green'],
 '葡萄適300毫升樽裝': ['lucozade', 'energy', 'cold', 'orange'],
 '葡萄適EXTRA夏日果300亳升樽庄': ['lucozade', 'energy', 'summer', 'cold', 'orange'],
 '葡萄適SPORT香橙味運動飲品500毫升': ['lucozade', 'energy', 'cold', 'orange'],
 '葡萄適純橙薏米300毫升樽裝': ['lucozade', 'bottle', 'energy', 'energy_drink'],
 '蒜香芝士撈麵': ['noodle', 'cheese', 'yellow', 'garlic'],
 '薄荷 萬寶路': ['marlboro', 'mint', 'white'],
 '薄荷白 萬寶路': ['marlboro', 'mint', 'cigarette', 'white', 'green'],
 '藍冰啤330毫升罐庄': ['blue', 'ice', 'blue_ice', 'beer', 'cold'],
 '藍冰啤KING CAN 500毫升罐裝': ['cold', 'ice', 'beer'],
 '藍冰啤酒330毫升4罐裝': ['cold', 'beer', 'ice'],
 '藍妹4罐庄': ['bluegirlbeer', 'blue', 'beer'],
 '藍妹KING CAN500毫升罐裝': ['bluegirlbeer', 'blue', 'beer', 'cold'],
 '藍妹啤酒大樽裝': ['bluegirlbeer', 'blue', 'beer', 'cold'],
 '藍駱駝硬盒': ['cigarette', 'blue'],
 '蘋果日報': ['newspaper', 'news'],
 '蜜汁叉燒包-熟包': ['dim sum', 'white', 'hot'],
 '解渴誌沛力特800毫升': ['drink', 'energy', 'white'],
 '超軟三文治-日式白汁碎蛋三文治': ['sandwich', 'cold', 'white'],
 '超軟三文治-日式白汁碎蛋火腿三文治': ['sandwich', 'cold', 'white'],
 '超軟三文治-海鹽白汁吞拿魚三文治': ['sandwich', 'cold', 'white'],
 '超軟三文治-煙肉蘑菇芝士三文治': ['sandwich', 'cold', 'white'],
 '道地柑桔檸檬500毫升樽裝': ['tao ti', 'tea', 'lemon', 'yellow'],
 '道地極品玄米茶500毫升樽裝': ['tao ti', 'tea', 'green', 'bottle'],
 '道地極品解綠茶500ML': ['tao ti', 'tea', 'green', 'bottle'],
 '道地極品解茶500ML': ['tao ti', 'tea', 'green', 'bottle'],
 '道地蘋果綠茶 500毫升樽裝': ['tao ti', 'tea', 'green', 'bottle'],
 '道地蜂蜜綠茶 500毫升膠樽庄': ['tao ti', 'tea', 'green', 'bottle'],
 '醇滑嘉士伯啤酒500毫升巨罐裝': ['carlsberg', 'beer', 'can', 'yellow'],
 '金牌嘉士伯罐裝': ['carlsberg', 'beer', 'can', 'yellow'],
 '阿波羅MAGIC CONE- 雲呢拿': ['apollo', 'ice-cream', 'vanilla', 'cold'],
 '阿波羅MAGIC CONE-朱古力': ['appolo', 'ice-cream', 'chocolate'],
 '阿波羅MONAKA-朱古力': ['appolo', 'ice-cream', 'chocolate'],
 '阿波羅MONAKA-雲呢拿': ['appolo', 'ice cream', 'vanillina', 'vanilla', 'white'],
 '阿波羅PARI甜筒 - 曲奇妙趣': ['appolo', 'ice-cream', 'cookie', 'black'],
 '陽光檸檬茶 375毫升紙包庄': ['green', 'yellow', 'lemon', 'tea', 'lemon_tea', 'cold'],
 '陽光蜜瓜豆奶 375毫升紙包庄': ['green', 'vite', 'soy', 'milk', 'soy_milk', 'cold'],
 '雀巢MEGA雪糕批-曲奇妙趣': ['nest', 'pie', 'ice-cream', 'cookie', 'black'],
 '雀巢MEGA雪糕批-薄荷朱古力': ['nest', 'mint', 'chocolate', 'ice-cream', 'pie'],
 '雀巢MEGA雪糕批-雲呢拿朱古力扭紋': ['nest', 'chocolate', 'vanillina', 'brown', 'vanilla'],
 '雀巢咖啡濃香焙煎咖啡250毫升': ['coffee', 'energy', 'brown', 'nest'],
 '雀巢歐陸奶滑咖啡250毫升罐裝': ['coffee', 'energy', 'brown', 'nest', 'milk'],
 '雀巢牛奶公司脫脂牛奶 236毫升盒裝': ['low-fat', 'milk', 'white', 'cold'],
 '雀巢牛奶公司高鈣低脂牛奶236毫升盒裝': ['healthy', 'hi-cal', 'low fat', 'milk', 'white'],
 '雀巢牛奶公司鮮奶236毫升盒裝': ['white', 'milk', 'cold'],
 '雀巢甜筒-朱古力': ['ice-cream', 'cold', 'chocolate', 'black'],
 '雀巢甜筒-芒果支庄': ['orange', 'sweet', 'cold', 'mango'],
 '雀巢甜筒-草莓味': ['ice-cream', 'cold', 'red', 'strawberry'],
 '雀巢甜筒-雲呢拿': ['nest', 'vanilla', 'ice-cream', 'cold', 'white'],
 '雀巢甜筒-香芋味': ['nest', 'purpel', 'ice-cream'],
 '雀巢絲滑牛奶咖啡268毫升樽裝': ['nest', 'milk', 'coffee', 'energy', 'drink'],
 '雀巢茉香柚子綠茶480毫升': ['nest', 'tea', 'cold', 'bottle'],
 '雀巢茶品冰極檸檬茶480毫升膠樽裝': ['blue',
  'nest',
  'ice',
  'lemon',
  'lemon_tea',
  'mint',
  'bottle'],
 '雀巢茶品檸檬茶480毫升樽庄': ['yellow', 'nest', 'lemon', 'tea', 'lemon_tea', 'bottle'],
 '雀巢超級大腳板雪條': ['nest', 'ice-cream', 'chocolate', 'brown'],
 '雀巢雪條-紅豆樂': ['bean', 'red', 'ice-cream', 'nest'],
 '雀巢雪糕杯 -雲呢拿': ['vanilla', 'ice-cream', 'nest', 'cold', 'white'],
 '雀巢雪糕杯-朱古力': ['nest', 'ice-cream', 'cold', 'chocolate'],
 '雀巢雪糕杯-芋頭': ['nest', 'ice-cream', 'purple'],
 '雀巢雪糕杯-芒果': ['nest', 'ice-cream', 'mango', 'yellow'],
 '雀巢香滑咖啡250毫升罐裝': ['brown',
  'nest',
  'coffee',
  'energy',
  'enegry_drink',
  'bottle'],
 '雀巢香濃咖啡250毫升罐庄': ['nest', 'coffee', 'brown', 'energy', 'drink'],
 '雙爆珠 萬寶路': ['black', 'cigarette', 'marlboro'],
 '雙黑薄荷 萬寶路': ['mint', 'black', 'cigarette', 'marlboro'],
 '雞尾包': ['bread', 'chicke', 'tale'],
 '雪碧 500毫升樽裝': ['sprite', 'cold', 'drink', 'soft', 'green', 'white'],
 '零系可口可樂330毫升罐裝': ['zero', 'coke', 'can', 'black', 'red'],
 '零系可口可樂500毫升膠樽裝': ['brown', 'coke', 'red', 'bottle'],
 '零系水動樂水分及電解質補充飲品': ['cold', 'sport', 'drink', 'white', 'blue', 'sweet'],
 '青島啤酒 330 毫升 4細罐裝': ['cold', 'beer', 'can', 'green', 'tsingtao', 'small'],
 '青島啤酒 330 毫升 細罐': ['cold', 'beer', 'can', 'green', 'tsingtao', 'small'],
 '青島啤酒 500 毫升 大罐': ['cold', 'beer', 'can', 'green', 'tsingtao', 'large'],
 '青島純生 500 毫升 大罐': ['yellow', 'tsingtao', 'beer', 'cold'],
 '韋恩杯裝藍山調合冰釀咖啡240毫升': ['cold', 'ice', 'coffee', 'wayne', 'cup', 'brown'],
 '韋恩特濃咖啡X2 320毫升罐': ['wayne', 'expresso', 'coffee', 'can', 'brown'],
 '韓國蜜瓜冰棒': ['cold', 'yellow', 'mellon', 'korea'],
 '風薄荷 萬寶路': ['mint', 'red', 'cigarette', 'marlboro'],
 '風藍萬事發硬盒': ['blue', 'cigarette'],
 '飛想3種茶底檸檬茶原味480毫升': ['brown', 'lemmon', 'cold', 'bottle'],
 '飛雪礦泉水 1.5公升樽裝': ['water', 'bottle', 'cold'],
 '飛雪礦泉水 500毫升膠樽庄': ['blue', 'water', 'cold'],
 '飛雪礦泉水 770毫升樽裝': ['blue', 'water', 'cold'],
 '馬拉糕-新': ['cake', 'sweet', 'brown'],
 '魚蛋燒賣雙拼10粒': ['hot', 'fishball', 'dim sum', 'snack'],
 '鴻福堂夏枯草500毫升樽裝': ['green',
  'bottle',
  'chinese',
  'medicine',
  'healthy',
  'black'],
 '鴻福堂雞骨草樽裝500毫升': ['prayer-beads', 'juice', 'healthy'],
 '麒麟一番巨罐裝啤酒500毫升': ['beer', 'japan', 'cold'],
 '麥提莎牛奶朱古力盒60克': ['red', 'brown', 'milk', 'chocolate'],
 '麥精維他奶 250毫升紙包庄': ['vita', 'brown', 'soy', 'bean'],
 '麥精維他奶375毫升紙包庄': ['vita', 'soy', 'soy_milk', 'soy_bean'],
 '黑冰 1 萬寶路': ['black',
  'ice',
  'black_ice',
  'cigarette',
  'marlboro',
  'blast',
  'ice_blast',
  '1',
  'one'],
 '黑冰 5 萬寶路': ['black',
  'ice',
  'black_ice',
  'cigarette',
  'marlboro',
  'blast',
  'ice_blast',
  '5',
  'five'],
 '黑冰 8 萬寶路': ['black',
  'ice',
  'black_ice',
  'cigarette',
  'marlboro',
  'blast',
  'ice_blast',
  '8',
  'eight'],
 '黑薄荷 萬寶路': ['black',
  'ice',
  'black_ice',
  'cigarette',
  'marlboro',
  'mint',
  'menthol']}

train_data = []
for prod in prod_counts_dict:
    train_data.append(' '.join(prod_tags_dict[prod]))

train_labels = []
for prod, count in prod_counts_dict.items():
    train_labels.append(count)

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])

text_clf = text_clf.fit(train_data, train_labels)


app = Flask(__name__)

@app.route("/<tag_text>")
def get_category(tag_text):
    prediction = text_clf.predict([tag_text])[0]
    return jsonify({'predicted_monthly_sales': int(prediction)})

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5678)
