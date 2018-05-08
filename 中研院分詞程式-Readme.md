* 本試用版發行日: 20180409
* 說明內容版本: 20171208

# Must run under 32bits python env

# 注意事項
- 如果執行時發生問題，可以進行以下步驟，安裝相關文件。
 - 安裝 vcredist_x86_2005.exe 或是 vcredist_x64_2005.exe
- 下列系統目錄請勿隨意異動。
 - Data2\
 - ws.ini


# 單機執行方式

## CKIPWSTester

    CKIPWSTester     ws.ini    test\sample.txt  test\sample.tag
    執行檔           參數檔    輸入檔　　　     輸出檔
    ws.ini:斷詞設定檔
    test/sample.txt: 輸入檔名
    test/sample.tag: 輸出檔名
    

## CKIPWSTesterDir

    CKIPWSTesterDir   ws.ini   input      output
    執行檔           參數檔    輸入目錄　 輸出目錄
    (系統會對 input 目錄下的檔案進行斷詞的作, 並輸出到 output 目錄下)

# API 呼叫方式

## 請參考 CKIPWS.py 內容

    主要是 指定 ini 與 inputStr ，最後呼叫 segment 即可。
    ini = 'ws.ini'
    initial(main_dll, py_dll, ini)
    inputStr = u'蔡英文是中華民國總統,而馬英九為前任總統,新北市市長是朱立倫'
    Result = segment(inputStr)
    print (Result)

    (使用方式 python CKIPWS.py )

# 檔案格式

## 輸入

- 文字檔 (支援 Big-5, UTF16LE帶簽名)

    詞是最小有意義且可以自由使用的語言單位。任何語言處理的系統都必須先能分辨文本中的詞才能進行進一步的處理，例如機器翻譯、語言分析、語言了解、資訊抽取。因此中文自動分詞的工作成了語言處理不可或缺的技術。基本上自動分詞多利用詞典中收錄的詞和文本做比對，找出可能包含的詞，由於存在歧義的切分結果，因此多數的中文分詞程式多討論如何解決分詞歧義的問題，而較少討論如何處理詞典中未收錄的詞出現的問題（新詞如何辨認）。
    

## 輸出 (UTF16LE帶簽名)

    　詞(Na)　是(SHI)　最(Dfa)　小(VH)　有(V_2)　意義(Na)　且(Cbb)　可以(D)　自由(VH)　使用(VC)　的(DE)　語言(Na)　單位(Na)　。(PERIODCATEGORY)
    　任何(Neqa)　語言(Na)　處理(VC)　的(DE)　系統(Na)　都(D)　必須(D)　先(D)　能(D)　分辨(VE)　文本(Nb)　中(Ng)　的(DE)　詞(Na)　才(Da)　能(D)　進行(VC)　進一步(A)　的(DE)　處理(Nv)　，(COMMACATEGORY)
    　例如(P)　機器(Na)　翻譯(Na)　、(PAUSECATEGORY)　語言(Na)　分析(Na)　、(PAUSECATEGORY)　語言(Na)　了解(Nv)　、(PAUSECATEGORY)　資訊(Na)　抽取(VC)　。(PERIODCATEGORY)
    　因此(Cbb)　中文(Na)　自動(VH)　分詞(Na)　的(DE)　工作(Na)　成(VG)　了(Di)　語言(Na)　處理(VC)　不可或缺(A)　的(DE)　技術(Na)　。(PERIODCATEGORY)
    　基本(Na)　上(Ncd)　自動(VH)　分詞(Na)　多(D)　利用(VC)　詞典(Na)　中(Ng)　收錄(VC)　的(DE)　詞(Na)　和(Caa)　文本(Nb)　做(VC)　比對(VC)　，(COMMACATEGORY)
    　找出(VC)　可能(D)　包含(VJ)　的(DE)　詞(Na)　，(COMMACATEGORY)
    　由於(Cbb)　存在(Nv)　歧義(Na)　的(DE)　切分(VC)　結果(Na)　，(COMMACATEGORY)
    　因此(Cbb)　多數(Neqa)　的(DE)　中文(Na)　分詞(Na)　程式(Na)　多(D)　討論(VE)　如何(D)　解決(VC)　分詞(Na)　歧義(Na)　的(DE)　問題(Na)　，(COMMACATEGORY)
    　而(Cbb)　較少(D)　討論(VE)　如何(D)　處理(VC)　詞典(Na)　中(Ng)　未(D)　收錄(VC)　的(DE)　詞(Na)　出現(VH)　的(DE)　問題(Na)　（(PARENTHESISCATEGORY)　新(VH)　詞(Na)　如何(D)　辨認(VC)　）(PARENTHESISCATEGORY)　。(PERIODCATEGORY)

# 可以配合 ConvertZ8.02 轉換成 big5

    可以參考 ConvertZ8.02/ConvertZ_ReadMe.txt
    (指定輸出)
    ConvertZ8.02\convertz /i:ule /o:big5 /f:d test\sample.tag test\sample.big5
    (直接覆寫)
    ConvertZ8.02\convertz /i:ule /o:big5 /f:d test\sample.tag

# 斷詞系統相關論文

## 斷詞系統主體

- Chen, K.J. & S.H. Liu, "Word Identification for Mandarin Chinese Sentences," Proceedings of 14th Coling (1992), pp. 101-107.

## 未知詞處理

- Chen, C. J., M. H. Bai, K. J. Chen, 1997, "Category Guessing for Chinese Unknown Words." Proceedings of the Natural Language Processing Pacific Rim Symposium 1997, pp. 35--40. NLPRS '97 Thailand.
- Chen Keh-Jiann, Ming-Hong Bai, "Unknown Word Detection for Chinese by a Corpus-based Learning Method", International Journal of Computational linguistics and Chinese Language Processing, 1998, Vol.3, #1, pages 27-44.
- Chen Keh-Jiann, Wei-Yun Ma, 2002, "Unknown Word Extraction for Chinese Documents", Proceedings of Coling 2002, pp.169-175.
- Ma, Wei-Yun and Keh-Jiann Chen, 2003, "A Bottom-up Merging Algorithm for Chinese Unknown Word Extraction", Proceedings of ACL, Second SIGHAN Workshop on Chinese Language Processing, pp.31-38.
- Ma, Wei-Yun and Keh-Jiann Chen, 2003, "Introduction to CKIP Chinese Word Segmentation System for the First International Chinese Word Segmentation Bakeoff", Proceedings of ACL, Second SIGHAN Workshop on Chinese Language Processing, pp. 168-171.

## 詞類標記

- Tsai Yu-Fang and Keh-Jiann Chen, 2003, "Reliable and Cost-Effective Pos-Tagging", Proceedings of ROCLING XV, pp161-174.
- Tsai Yu-Fang and Keh-Jiann Chen, 2003, "Context-rule Model for POS Tagging", Proceedings of PACLIC 17, pp146-151.
- Tsai Yu-Fang and Keh-Jiann Chen, 2004, "Reliable and Cost-Effective Pos-Tagging", International Journal of Computational Linguistics & Chinese Language Processing, Vol. 9 #1, pp83-96.