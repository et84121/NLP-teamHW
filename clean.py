import json,ckipws,re,os,tabulate,nltk,time

if __name__ == '__main__':
    select = input("你要分析哪篇文章呢？\n1. 社會與文化篇(005-362)  2. 政治與經濟篇(005-370)\n請輸入數字 1 or 2\n")
    fileName = str()
    if select == '1':
        fileName = '社會與文化篇(005-362)'
    elif select == '2':    
        fileName = '政治與經濟篇(005-370)'
    raw = open('{0}.txt'.format(fileName),encoding='utf-8', mode='r')

    t_start = time.clock()
    print('\ninfo :正則處理中')

    """
    用正則表達示進行雜訊的清除
    """
    text = re.sub(r"\d \d \d","=====",raw.read()) #消頁碼
    text = re.sub(r"\n{2}","\n",text) #消因排版產生的換行
    text = re.sub(r"\n","",text) #消因排版產生的換行
    text = re.sub(r"=====","\n\n",text)
    text = re.sub(r"\d{1,3} [^\u007E_\u5E74_\u6708_\u65E5_\u7248_\uFF5E].*","",text) #消註解
    if fileName == '政治與經濟篇(005-370)':
        text=text.replace('第一章　政府部門','')
        text=text.replace('第二章　民意機關','')
        text=text.replace('第三章　政治社會運動','')
        text=text.replace('第四章　政治受難','')
        text=text.replace('第五章　農工產業','')
        text=text.replace('第六章　商業與服務業','')
    elif fileName == '社會與文化篇(005-362)':
        text=text.replace('第一章　教育學術','')
        text=text.replace('第二章　文學藝術','')
        text=text.replace('第三章　大眾文化','')
        text=text.replace('第四章　醫療衛生','')
        text=text.replace('第五章　宗教信仰','')
        text=text.replace('第六章　社會服務','')

    """
    取出 人名及年份 ex '陳英泰 89（1928.02.18-2010.01.18）'
    """
    names_with_years = re.findall(r'\n[^0-9\u5e74\n、]{2,4}[ \d]{0,4}\（[\.0-9]+-[\.0-9]*\）',text, flags=re.U) #選取帶年份的人名
    name = list()
    for x in names_with_years:
        name = name + re.findall(r'[^0-9 \（\）\n\.]{2,4}',x,flags=re.U) #選取人名
    
    """
    用取出的人名來進行檔案的切分
    """
    s_text = list()
    for x in range(1,len(names_with_years)):
        s_text.append(text.split(names_with_years[x])[0]) 
        text = text.split(names_with_years[x])[1]
    s_text.append(text)

    s_text[0] = s_text[0].split(names_with_years[0])[1] 

    # 去除多除的換行符
    for x in range(0,len(name)):
        s_text[x] = re.sub(r"\n+","",s_text[x])

    # 存放清理及分檔後的結果進txt
    text = str()
    with open('{0}-clean.txt'.format(fileName),encoding='utf-8', mode='w') as file:
        for x in range(0,len(name)):
            text += name[x] + "\n"
            text += s_text[x] + "\n\n"
        file.write(text)

    print('info :雜訊去除及檔案切分完成 花了: {0}秒'.format(time.clock()-t_start))


    '''
    分詞 or 讀取已分詞過的結果
    '''
    ws_s_text = list()
    if ( not os.path.isfile('{0}.json'.format(fileName)) ) or ( os.path.getsize('{0}.json'.format(fileName)) == 0 ):
        print('info :進行分詞中')
        t_start = time.clock()
        with open('{0}.json'.format(fileName),encoding='utf-8', mode='w') as jsonFile:
            WS = ckipws.CKIPWS() #呼叫中研院分詞程式
            for i, t in enumerate(s_text):
                ws_s_text.append(WS.segment(t,mode=1))
                print(i, end='\r')
            json.dump(ws_s_text,jsonFile)
        print('info :完成分詞 花了: {0}秒'.format(time.clock()-t_start))
    else:
        print('info :讀取舊有已分詞過之檔案')
        with open('{0}.json'.format(fileName),encoding='utf-8', mode='r') as jsonFile:
            ws_s_text = json.load(jsonFile)

    """
    存放分詞後結果進文字檔
    """
    with open('{0}-ws.txt'.format(fileName),encoding='utf-8', mode='w') as wsFile:
        text = str()
        for x in range(0,len(name)):
            text += name[x] + "\n"
            text += str(ws_s_text[x]) + "\n\n"
        wsFile.write(text)

    """
    計算相關數據
    """
    num_word_token = list()
    num_word_type  = list()
    for x in ws_s_text:
        num_word_token.append(len(x))
        num_word_type.append(len(set(x)))
    
    tabulate.WIDE_CHARS_MODE = True
    print('\n因為console寬度的關系 只展示前10筆資料')
    print(tabulate.tabulate([num_word_token[:10],num_word_type[:10]],name[:10],tablefmt='pipe'))

    n_gram = input('input n-grams 的 n 要多少?\n')
    x = input('要前幾筆的排行\n')
    fdist = nltk.FreqDist([word for people_based_ws_text in ws_s_text for word in people_based_ws_text if len(word) == int(n_gram)])
    print(tabulate.tabulate(
        [[x[1] for x in fdist.most_common(int(x))]],
        [x[0] for x in fdist.most_common(int(x))],
        tablefmt='pipe'
        ))
