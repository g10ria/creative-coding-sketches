import requests
import os
import time

sounds = [

    "a2", "ba2", "pa2", "ma2", "fa2", "da2", "ta2", "na2", "la2", "ga2", "ka2", "ha2", "za2", "ca2", "sa2", "zha2", "cha2", "sha2",
    "ai2", "bai2", "pai2", "mai2", "dai2", "tai2", "nai2", "lai2", "gai2", "kai2", "hai2", "zai2", "cai2", "sai2", "zhai2", "chai2", "shai2",
    "an2", "ban2", "pan2", "man2", "fan2", "dan2", "tan2", "nan2", "lan2", "gan2", "kan2", "han2", "zan2", "can2", "san2", "zhan2", "chan2", "shan2", "ran2",
    "ang2", "bang2", "pang2", "mang2", "fang2", "dang2", "tang2", "nang2", "lang2", "gang2", "kang2", "hang2", "zang2", "cang2", "sang2", "zhang2", "chang2", "shang2", "rang2",
    "ao2", "bao2", "pao2", "mao2", "dao2", "tao2", "nao2", "lao2", "gao2", "kao2", "hao2", "zao2", "cao2", "sao2", "zhao2", "chao2", "shao2", "rao2",
    "e2", "me2", "de2", "te2", "ne2", "le2", "ge2", "ke2", "he2", "ze2", "ce2", "se2", "zhe2", "che2", "she2", "re2",
    "ei2", "bei2", "pei2", "mei2", "fei2", "dei2", "nei2", "lei2", "gei2", "hei2", "zei2", "zhei2", "shei2",
    "en2", "ben2", "pen2", "men2", "fen2", "nen2", "gen2", "ken2", "hen2", "zen2", "cen2", "sen2", "zhen2", "chen2", "shen2", "ren2",
    "eng2", "beng2", "peng2", "meng2", "feng2", "deng2", "teng2", "neng2", "leng2", "geng2", "keng2", "heng2", "zeng2", "ceng2", "seng2", "zheng2", "cheng2", "sheng2", "reng2",
    "er2", "yi2", "bi2", "pi2", "mi2", "di2", "ti2", "ni2", "li2", "ji2", "qi2", "xi2",
    "ya2", "dia2", "lia2", "jia2", "qia2", "xia2",
    "yan2", "bian2", "pian2", "mian2", "dian2", "tian2", "nian2", "lian2", "jian2", "qian2", "xian2",
    "yang2", "niang2", "liang2", "jiang2", "qiang2", "xiang2",
    "yao2", "biao2", "piao2", "miao2", "diao2", "tiao2", "niao2", "liao2", "jiao2", "qiao2", "xiao2",
    "ye2", "bie2", "pie2", "mie2", "die2", "tie2", "nie2", "lie2", "jie2", "qie2", "xie2",
    "yin2", "bin2", "pin2", "min2", "nin2", "lin2", "jin2", "qin2", "xin2",
    "ying2", "bing2", "ping2", "ming2", "ding2", "ting2", "ning2", "ling2", "jing2", "qing2", "xing2",
    "yong2", "jiong2", "qiong2", "xiong2",
    "you2", "miu2", "diu2", "niu2", "liu2", "jiu2", "qiu2", "xiu2",
    "o2", "bo2", "po2", "mo2", "fo2",
    "dong2", "tong2", "nong2", "long2", "gong2", "kong2", "hong2", "zong2", "cong2", "song2", "zhong2", "chong2", "rong2",
    "ou2", "pou2", "mou2", "fou2", "dou2", "tou2", "lou2", "gou2", "kou2", "hou2", "zou2", "cou2", "sou2", "zhou2", "chou2", "shou2", "rou2",
    "wu2", "bu2", "pu2", "mu2", "fu2", "du2", "tu2", "nu2", "lu2", "gu2", "ku2", "hu2", "zu2", "cu2", "su2", "zhu2", "chu2", "shu2", "ru2",
    "wa2", "gua2", "kua2", "hua2", "zhua2", "shua2",
    "wai2", "guai2", "kuai2", "huai2", "zhuai2", "chuai2", "shuai2",
    "wan2", "duan2", "tuan2", "nuan2", "luan2", "guan2", "kuan2", "huan2", "zuan2", "cuan2", "suan2", "zhuan2", "chuan2", "shuan2", "ruan2",
    "wang2", "guang2", "kuang2", "huang2", "zhuang2", "chuang2", "shuang2",
    "wei2", "dui2", "tui2", "gui2", "kui2", "hui2", "zui2", "cui2", "sui2", "zhui2", "chui2", "shui2", "rui2",
    "wen2", "dun2", "tun2", "lun2", "gun2", "kun2", "hun2", "zun2", "cun2", "sun2", "zhun2", "chun2", "shun2", "run2",
    "weng2", "wo2", "duo2", "tuo2", "nuo2", "luo2", "guo2", "kuo2", "huo2", "zuo2", "cuo2", "suo2", "zhuo2", "chuo2", "shuo2", "ruo2",
    "yu2", "nv2", "lv2", "ju2", "qu2", "xu2",
    "yuan2", "juan2", "quan2", "xuan2",
    "yue2", "nve2", "lve2", "jue2", "que2", "xue2",
    "yun2", "jun2", "qun2", "xun2",

    "a3", "ba3", "pa3", "ma3", "fa3", "da3", "ta3", "na3", "la3", "ga3", "ka3", "ha3", "za3", "ca3", "sa3", "zha3", "cha3", "sha3",
    "ai3", "bai3", "pai3", "mai3", "dai3", "tai3", "nai3", "lai3", "gai3", "kai3", "hai3", "zai3", "cai3", "sai3", "zhai3", "chai3", "shai3",
    "an3", "ban3", "pan3", "man3", "fan3", "dan3", "tan3", "nan3", "lan3", "gan3", "kan3", "han3", "zan3", "can3", "san3", "zhan3", "chan3", "shan3", "ran3",
    "ang3", "bang3", "pang3", "mang3", "fang3", "dang3", "tang3", "nang3", "lang3", "gang3", "kang3", "hang3", "zang3", "cang3", "sang3", "zhang3", "chang3", "shang3", "rang3",
    "ao3", "bao3", "pao3", "mao3", "dao3", "tao3", "nao3", "lao3", "gao3", "kao3", "hao3", "zao3", "cao3", "sao3", "zhao3", "chao3", "shao3", "rao3",
    "e3", "me3", "de3", "te3", "ne3", "le3", "ge3", "ke3", "he3", "ze3", "ce3", "se3", "zhe3", "che3", "she3", "re3",
    "ei3", "bei3", "pei3", "mei3", "fei3", "dei3", "nei3", "lei3", "gei3", "hei3", "zei3", "zhei3", "shei3",
    "en3", "ben3", "pen3", "men3", "fen3", "nen3", "gen3", "ken3", "hen3", "zen3", "cen3", "sen3", "zhen3", "chen3", "shen3", "ren3",
    "eng3", "beng3", "peng3", "meng3", "feng3", "deng3", "teng3", "neng3", "leng3", "geng3", "keng3", "heng3", "zeng3", "ceng3", "seng3", "zheng3", "cheng3", "sheng3", "reng3",
    "er3", "yi3", "bi3", "pi3", "mi3", "di3", "ti3", "ni3", "li3", "ji3", "qi3", "xi3",
    "ya3", "dia3", "lia3", "jia3", "qia3", "xia3",
    "yan3", "bian3", "pian3", "mian3", "dian3", "tian3", "nian3", "lian3", "jian3", "qian3", "xian3",
    "yang3", "niang3", "liang3", "jiang3", "qiang3", "xiang3",
    "yao3", "biao3", "piao3", "miao3", "diao3", "tiao3", "niao3", "liao3", "jiao3", "qiao3", "xiao3",
    "ye3", "bie3", "pie3", "mie3", "die3", "tie3", "nie3", "lie3", "jie3", "qie3", "xie3",
    "yin3", "bin3", "pin3", "min3", "nin3", "lin3", "jin3", "qin3", "xin3",
    "ying3", "bing3", "ping3", "ming3", "ding3", "ting3", "ning3", "ling3", "jing3", "qing3", "xing3",
    "yong3", "jiong3", "qiong3", "xiong3",
    "you3", "miu3", "diu3", "niu3", "liu3", "jiu3", "qiu3", "xiu3",
    "o3", "bo3", "po3", "mo3", "fo3",
    "dong3", "tong3", "nong3", "long3", "gong3", "kong3", "hong3", "zong3", "cong3", "song3", "zhong3", "chong3", "rong3",
    "ou3", "pou3", "mou3", "fou3", "dou3", "tou3", "lou3", "gou3", "kou3", "hou3", "zou3", "cou3", "sou3", "zhou3", "chou3", "shou3", "rou3",
    "wu3", "bu3", "pu3", "mu3", "fu3", "du3", "tu3", "nu3", "lu3", "gu3", "ku3", "hu3", "zu3", "cu3", "su3", "zhu3", "chu3", "shu3", "ru3",
    "wa3", "gua3", "kua3", "hua3", "zhua3", "shua3",
    "wai3", "guai3", "kuai3", "huai3", "zhuai3", "chuai3", "shuai3",
    "wan3", "duan3", "tuan3", "nuan3", "luan3", "guan3", "kuan3", "huan3", "zuan3", "cuan3", "suan3", "zhuan3", "chuan3", "shuan3", "ruan3",
    "wang3", "guang3", "kuang3", "huang3", "zhuang3", "chuang3", "shuang3",
    "wei3", "dui3", "tui3", "gui3", "kui3", "hui3", "zui3", "cui3", "sui3", "zhui3", "chui3", "shui3", "rui3",
    "wen3", "dun3", "tun3", "lun3", "gun3", "kun3", "hun3", "zun3", "cun3", "sun3", "zhun3", "chun3", "shun3", "run3",
    "weng3", "wo3", "duo3", "tuo3", "nuo3", "luo3", "guo3", "kuo3", "huo3", "zuo3", "cuo3", "suo3", "zhuo3", "chuo3", "shuo3", "ruo3",
    "yu3", "nv3", "lv3", "ju3", "qu3", "xu3",
    "yuan3", "juan3", "quan3", "xuan3",
    "yue3", "nve3", "lve3", "jue3", "que3", "xue3",
    "yun3", "jun3", "qun3", "xun3",

    "a4", "ba4", "pa4", "ma4", "fa4", "da4", "ta4", "na4", "la4", "ga4", "ka4", "ha4", "za4", "ca4", "sa4", "zha4", "cha4", "sha4",
    "ai4", "bai4", "pai4", "mai4", "dai4", "tai4", "nai4", "lai4", "gai4", "kai4", "hai4", "zai4", "cai4", "sai4", "zhai4", "chai4", "shai4",
    "an4", "ban4", "pan4", "man4", "fan4", "dan4", "tan4", "nan4", "lan4", "gan4", "kan4", "han4", "zan4", "can4", "san4", "zhan4", "chan4", "shan4", "ran4",
    "ang4", "bang4", "pang4", "mang4", "fang4", "dang4", "tang4", "nang4", "lang4", "gang4", "kang4", "hang4", "zang4", "cang4", "sang4", "zhang4", "chang4", "shang4", "rang4",
    "ao4", "bao4", "pao4", "mao4", "dao4", "tao4", "nao4", "lao4", "gao4", "kao4", "hao4", "zao4", "cao4", "sao4", "zhao4", "chao4", "shao4", "rao4",
    "e4", "me4", "de4", "te4", "ne4", "le4", "ge4", "ke4", "he4", "ze4", "ce4", "se4", "zhe4", "che4", "she4", "re4",
    "ei4", "bei4", "pei4", "mei4", "fei4", "dei4", "nei4", "lei4", "gei4", "hei4", "zei4", "zhei4", "shei4",
    "en4", "ben4", "pen4", "men4", "fen4", "nen4", "gen4", "ken4", "hen4", "zen4", "cen4", "sen4", "zhen4", "chen4", "shen4", "ren4",
    "eng4", "beng4", "peng4", "meng4", "feng4", "deng4", "teng4", "neng4", "leng4", "geng4", "keng4", "heng4", "zeng4", "ceng4", "seng4", "zheng4", "cheng4", "sheng4", "reng4",
    "er4", "yi4", "bi4", "pi4", "mi4", "di4", "ti4", "ni4", "li4", "ji4", "qi4", "xi4",
    "ya4", "dia4", "lia4", "jia4", "qia4", "xia4",
    "yan4", "bian4", "pian4", "mian4", "dian4", "tian4", "nian1", "lian4", "jian4", "qian4", "xian4",
    "yang4", "niang4", "liang4", "jiang4", "qiang4", "xiang4",
    "yao4", "biao4", "piao4", "miao4", "diao4", "tiao4", "niao4", "liao4", "jiao4", "qiao4", "xiao4",
    "ye4", "bie4", "pie4", "mie4", "die4", "tie4", "nie4", "lie4", "jie4", "qie4", "xie4",
    "yin4", "bin4", "pin4", "min4", "nin4", "lin4", "jin4", "qin4", "xin4",
    "ying4", "bing4", "ping4", "ming4", "ding4", "ting4", "ning4", "ling4", "jing4", "qing4", "xing4",
    "yong4", "jiong4", "qiong4", "xiong4",
    "you4", "miu4", "diu4", "niu4", "liu4", "jiu4", "qiu4", "xiu4",
    "o4", "bo4", "po4", "mo4", "fo4",
    "dong4", "tong4", "nong4", "long4", "gong4", "kong4", "hong4", "zong4", "cong4", "song4", "zhong4", "chong4", "rong4",
    "ou4", "pou4", "mou4", "fou4", "dou4", "tou4", "lou4", "gou4", "kou4", "hou4", "zou4", "cou4", "sou4", "zhou4", "chou4", "shou4", "rou4",
    "wu4", "bu4", "pu4", "mu4", "fu4", "du4", "tu4", "nu4", "lu4", "gu4", "ku4", "hu4", "zu4", "cu4", "su4", "zhu4", "chu4", "shu4", "ru4",
    "wa4", "gua4", "kua4", "hua4", "zhua4", "shua4",
    "wai4", "guai4", "kuai4", "huai4", "zhuai4", "chuai4", "shuai4",
    "wan4", "duan4", "tuan4", "nuan4", "luan4", "guan4", "kuan4", "huan4", "zuan4", "cuan4", "suan4", "zhuan4", "chuan4", "shuan4", "ruan4",
    "wang4", "guang4", "kuang4", "huang4", "zhuang4", "chuang4", "shuang4",
    "wei4", "dui4", "tui4", "gui4", "kui4", "hui4", "zui4", "cui4", "sui4", "zhui4", "chui4", "shui4", "rui4",
    "wen4", "dun4", "tun4", "lun4", "gun4", "kun4", "hun4", "zun4", "cun4", "sun4", "zhun4", "chun4", "shun4", "run4",
    "weng4", "wo4", "duo4", "tuo4", "nuo4", "luo4", "guo4", "kuo4", "huo4", "zuo4", "cuo4", "suo4", "zhuo4", "chuo4", "shuo4", "ruo4",
    "yu4", "nv4", "lv4", "ju4", "qu4", "xu4",
    "yuan4", "juan4", "quan4", "xuan4",
    "yue4", "nve4", "lve4", "jue4", "que4", "xue4",
    "yun4", "jun4", "qun4", "xun4"
]

base_url = "https://cdn.yoyochinese.com/audio/pychart/{}.mp3"
download_folder = "yoyo_chinese_audio"

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

print(f"Starting download of {len(sounds)} files...")

for sound in sounds:
    url = base_url.format(sound)
    file_path = os.path.join(download_folder, f"{sound}.mp3")
    
    if os.path.exists(file_path):
        print(f"Skipping: {sound}.mp3 (Already downloaded)")
        continue

    try:
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded: {sound}.mp3")
        else:
            print(f"Failed to find: {sound}.mp3 (Status: {response.status_code})")

        time.sleep(0.5) 
        
    except Exception as e:
        print(f"Error downloading {sound}: {e}")

print("Task complete!")