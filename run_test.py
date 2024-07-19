from time import time
import sys
import os
class runcase:
    def __init__(self, case, code, funcname):
        self.original_stdout = sys.stdout
        self.devnull = open(os.devnull, 'w')
        self.case = case
        self.code = code
        self.funcname = funcname

    def run(self):
        files = self.funcname + ".txt"
        try:
            open(files, "w", encoding="utf-8").write("")
        except:pass

        for i in range(len(self.case)):
            self.run_test(self.case[i], i)

        self.devnull.close()    
        return 

    def run_test(self, case, id):
        
        time_start      = time()
        files           = self.funcname + ".txt"
        file_log        = self.funcname + "_log.txt"
        BASE_CODE       = f"""

def write_logs(output, content, method):
    with open(output, method, encoding = "utf-8") as f:
        f.write(content)
    return

{self.code}

try:
    response = {self.funcname}({case[0]})
    response = "Tham số : {case[0]} | Kết quả chạy : " + str(response) + " | Kết quả mẫu : {case[1].replace('"', "'")}\\n" 
    write_logs("{files}", response, "a")
except Exception as e:
    content = "Error {files} : " + str(e)
    write_logs("{file_log}", content, "w")
"""
        try:
            sys.stdout = self.devnull
            exec(BASE_CODE, globals())
            
        finally:
            sys.stdout = self.original_stdout
        return print(f"[Case id : {id}] RUNNING DONE | time : {(str(time() - time_start) + '0'*5)[:5]}")