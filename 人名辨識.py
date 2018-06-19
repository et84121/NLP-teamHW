import re
import pandas as pd
import jieba


def select_people_name(data):
    pattern = re.compile(r'[王李張劉陳楊黃趙周吳徐孫馬胡朱郭何羅高林]\w{1,2}')
    result = re.findall(pattern, data)
    print(result)

    words = jieba.pseg.cut(str(result))
    clean_result = []
    for word, flag in words:
        print('%s %s' % (word, flag))
        if flag == 'nr':
            word_number = len(word)
            if not word_number == 1:
                clean_result.append(word)
