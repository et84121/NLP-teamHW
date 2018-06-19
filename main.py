import json
import ckipws
import re
import os
import tabulate
import nltk
import time


def chronology():
    DataPath = r'meta/{0}-clean.txt'.format(fileName)
    print("[人物事蹟年表]")

    def descriptionFind(name):
        # 搜尋人物所在的段落
        rf = open(DataPath, 'r', encoding='utf8')
        nameFinded = False
        for line in rf.readlines():
            m = re.match(name, line)
            if(m is not None):
                nameFinded = True
            elif(nameFinded is True):
                chronologyList(line)
                return
        print("查無此人")

    def chronologyList(description):
        # 建立年表
        pat = r'\uFF08\d{4}[^\u3002]*'
        yearList = re.findall(pat, description)
        for line in yearList:
            year = line[1:5]
            workpat = r'[^\uFF0C].*'
            nameDescription = re.search(workpat, line[6:]).group()
            print("%s年 : %s" % (year, nameDescription))

    # 主要程式
    name = input("請輸入人名:")
    descriptionFind(name)


def the_number_of_verb():
    """
    計算數據
    計算動詞數量並排序和列表
    """
    verbs = list()
    # 取出所有動詞
    for x in ws_text_tuple:
        for v, pos in x:
            if 'V' in pos:
                verbs.append(v)
    # 計算各動詞數量
    fdist = nltk.FreqDist(verbs)
    #
    count = int(input('輸入 最頻繁x個的動詞的頻率(x 為一數量)\n'))
    print(tabulate.tabulate([[x, y] for x, y in fdist.most_common(count)], [
          '內容', '數量'], tablefmt='pipe'))


def name_show_up():
    """
    計算某名字在該人物段落裡出現的次數
    """
    n = input('輸入要查詢的人名\n')
    if n in name:
        print(n + " 的出現次數為 " + str(ws_s_text.count(n)))


def wordType_and_wordToken():
    """
    計算數據
    計算各人物 word token 和 word type 數量
    """
    num_word_token = list()
    num_word_type = list()
    for x in ws_s_text:
        num_word_token.append(len(x))
        num_word_type.append(len(set(x)))

    tabulate.WIDE_CHARS_MODE = True
    count = int(input('輸入要幾筆資料\n'))
    print(tabulate.tabulate([[name[x], num_word_token[x], num_word_type[x]] for x in range(0, count)], [
          '內容', 'Token', 'Type'], tablefmt='pipe'))


def n_gram():
    """
    計算數據
    計算N-gram數量排行
    """
    n_gram = input('input n-grams 的 n 要多少?\n')
    x = input('要前幾筆的排行\n')
    fdist = nltk.FreqDist(
        [word for people_based_ws_text in ws_s_text for word in people_based_ws_text if len(word) == int(n_gram)])
    print(tabulate.tabulate(
        [[w[0], w[1]] for w in fdist.most_common(int(x))],
        ['內容', '數量'],
        tablefmt='pipe'
    ))


if __name__ == '__main__':
    select = input(
        "你要分析哪篇文章呢？\n1. 社會與文化篇(005-362)  2. 政治與經濟篇(005-370)\n請輸入數字 1 or 2\n")
    fileName = str()
    if select == '1':
        fileName = '社會與文化篇(005-362)'
    elif select == '2':
        fileName = '政治與經濟篇(005-370)'
    raw = open('{0}.txt'.format(fileName), encoding='utf-8', mode='r')

    t_start = time.clock()
    print('\ninfo :正則處理中')

    """
    用正則表達示進行雜訊的清除
    """
    text = re.sub(r"\d \d \d", "=====", raw.read())  # 消頁碼
    text = re.sub(r"\n{2}", "\n", text)  # 消因排版產生的換行
    text = re.sub(r"\n", "", text)  # 消因排版產生的換行
    text = re.sub(r"=====", "\n\n", text)
    text = re.sub(
        r"\d{1,3} [^\u007E_\u5E74_\u6708_\u65E5_\u7248_\uFF5E].*", "", text)  # 消註解
    if fileName == '政治與經濟篇(005-370)':
        text = text.replace('第一章　政府部門', '')
        text = text.replace('第二章　民意機關', '')
        text = text.replace('第三章　政治社會運動', '')
        text = text.replace('第四章　政治受難', '')
        text = text.replace('第五章　農工產業', '')
        text = text.replace('第六章　商業與服務業', '')
    elif fileName == '社會與文化篇(005-362)':
        text = text.replace('第一章　教育學術', '')
        text = text.replace('第二章　文學藝術', '')
        text = text.replace('第三章　大眾文化', '')
        text = text.replace('第四章　醫療衛生', '')
        text = text.replace('第五章　宗教信仰', '')
        text = text.replace('第六章　社會服務', '')

    """
    取出 人名及年份 ex '陳英泰 89（1928.02.18-2010.01.18）'
    """
    names_with_years = re.findall(
        r'\n[^0-9\u5e74\n、]{2,4}[ \d]{0,4}\（[\.0-9]+-[\.0-9]*\）', text, flags=re.U)  # 選取帶年份的人名
    name = list()
    for x in names_with_years:
        name = name + \
            re.findall(r'[^0-9 \（\）\n\.]{2,4}', x, flags=re.U)  # 選取人名

    """
    用取出的人名來進行檔案的切分
    """
    s_text = list()
    for x in range(1, len(names_with_years)):
        s_text.append(text.split(names_with_years[x])[0])
        text = text.split(names_with_years[x])[1]
    s_text.append(text)

    s_text[0] = s_text[0].split(names_with_years[0])[1]

    # 去除多除的換行符
    for x in range(0, len(name)):
        s_text[x] = re.sub(r"\n+", "", s_text[x])

    # 存放清理及分檔後的結果進txt
    text = str()
    with open('meta/{0}-clean.txt'.format(fileName), encoding='utf-8', mode='w') as file:
        for x in range(0, len(name)):
            text += name[x] + "\n"
            text += s_text[x] + "\n\n"
        file.write(text)

    print('info :雜訊去除及檔案切分完成 花了: {0}秒'.format(time.clock() - t_start))

    '''
    分詞 or 讀取已分詞過的結果
    '''
    ws_s_text = list()  # 純文字結果  ex ['蔡英文', '是', ...]
    ws_text_tuple = list()  # 含詞性結果 ex [('蔡英文', 'Nb'), ('是', 'SHI'), ...]
    if (not os.path.isfile('meta/{0}.json'.format(fileName))) or (os.path.getsize('meta/{0}.json'.format(fileName)) == 0):
        print('info :進行分詞中')
        t_start = time.clock()
        with open('meta/{0}.json'.format(fileName), encoding='utf-8', mode='w') as jsonFile:
            WS = ckipws.CKIPWS()  # 呼叫中研院分詞程式
            for i, t in enumerate(s_text):
                tmp = list()
                tmp1 = list()
                for a, b in WS.segment(t, mode=0):
                    tmp.append((a, b))
                    tmp1.append(a)
                ws_text_tuple.append(tmp)
                ws_s_text.append(tmp1)
                print(i, end='\r')
            json.dump(ws_text_tuple, jsonFile)
        print('info :完成分詞 花了: {0}秒'.format(time.clock() - t_start))
    else:
        print('info :讀取舊有已分詞過之檔案')
        with open('meta/{0}.json'.format(fileName), encoding='utf-8', mode='r') as jsonFile:
            ws_text_tuple = json.load(jsonFile)
            for x in ws_text_tuple:
                tmp = list()
                for y, z in x:
                    tmp.append(y)
                ws_s_text.append(tmp)

    """
    存放分詞後結果進文字檔
    """
    with open('meta/{0}-ws.txt'.format(fileName), encoding='utf-8', mode='w') as wsFile:
        text = str()
        for x in range(0, len(name)):
            text += name[x] + "\n"
            text += str(ws_text_tuple[x]) + "\n\n"
        wsFile.write(text)

    """
    選擇要分析的內容
    """
    while True:
        choice = input(
            "\n輸入想要計算的內容(數字)\n" +
            "(1)計算各人物 word token 和 word type 數量\n" +
            "(2)計算N-gram數量排行\n" +
            "(3)計算動詞數量並排序和列表\n" +
            "(4)計算某名字在該人物段落裡出現的次數 \n" +
            "(5)人物事蹟年表\n" +
            "(10)離開程式\n")
        if choice == '1':
            wordType_and_wordToken()
        elif choice == '2':
            n_gram()
        elif choice == '3':
            the_number_of_verb()
        elif choice == '4':
            name_show_up()
        elif choice == '5':
            chronology()
        elif choice == '10':
            break
        else:
            print("Without this option")
