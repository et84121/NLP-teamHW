from ctypes import CDLL,c_wchar_p,cast

class CKIPWS:
    ckipws = None
    def __init__(self,main_dll = 'CKIPWS.dll', py_dll = 'PY_CKIPWS.dll', ini = 'ws.ini'):
        c_main_dll = c_wchar_p(main_dll)
        c_ini = c_wchar_p(ini)
        self.ckipws = CDLL(py_dll)
        self.ckipws.Initial(c_main_dll,c_ini)

    def segment(self,inputStr, mode = 0):
        Result = ''
        try:
            CResult = self.ckipws.Segment(inputStr)
            CResult = cast(CResult,c_wchar_p)
            Result = CResult.value
        except:
            pass
        finally:
            if mode == 0:
                WSResult = []
                Result = Result.split()
                for res in Result:
                    re = res.strip()
                    re = res[0:len(res)-1]
                    temp = re.split(u'(')
                    word = temp[0]
                    pos = temp[1]
                    WSResult.append((word,pos))
                #[('蔡英文', 'Nb'), ('是', 'SHI'), ...]
                return WSResult
            elif mode == 1:
                WSResult = []
                Result = Result.split()
                for res in Result:
                    re = res.strip()
                    re = res[0:len(res)-1]
                    temp = re.split(u'(')
                    word = temp[0]
                    pos = temp[1]
                    WSResult.append((word))
                #[('蔡英文'), ('是'), ...]
                return WSResult
            else:
                #蔡英文(Nb)　是(SHI)　中華民國(Nc)...
                return Result

    