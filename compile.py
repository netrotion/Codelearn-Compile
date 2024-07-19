from os                     import path, listdir, system, name, remove
from crawl_api.wrap_api     import config
from run_test               import runcase
from time                   import sleep
from shutil                 import get_terminal_size

def pc(text,space = 0,is_fire=False):
    columns, _ = get_terminal_size()
    if columns < 40:
        system('clear') if name == 'posix' else system('cls')
        print(">>Change windows size and restart the programs!")
        raise SystemExit
    padding = (columns - len(text)) // 2 
    return " " *(padding-space) + text


BANNER = "\n".join([
pc(" __   __   __   ___       ___       __           __   __         __          ___ "),
pc("/  ` /  \ |  \ |__  |    |__   /\  |__) |\ |    /  ` /  \  |\/| |__) | |    |__  "),
pc("\__, \__/ |__/ |___ |___ |___ /~~\ |  \ | \|    \__, \__/  |  | |    | |___ |___ "),
pc("                                                       author : Le Viet Hung     "),
pc("            a programs that can compile your training on codelearn.io            "),
])



class run:
    def __init__(self):
        self.base_url = "https://codelearn.io/training/"

    def banner(self):
        system("cls") if name == "nt" else system("clear")
        print(pc(BANNER) + "\n")
        return
    
    def list_files(self):
        self.banner()
        files       = sorted([f for f in listdir() if path.isfile(f)])
        num_files   = len(files)

        print("[+] # DANH SÁCH PYTHON SCRIPTS #\n")
        
        for i, file in enumerate(files):
            print(f"[{i+1}] >> {file}")
        print("[DL] >> Delete Logs")

        print("\n")

        try:
            choice = input(f"[~] CHỌN FILE CẦN CHẠY : ")
            if choice.isnumeric():
                choice = int(choice)
                if 1 <= choice <= num_files:
                    
                    selected_file = path.abspath(files[choice-1])
                    if selected_file == __file__:
                        print("[!] Cannot compile main scripts")
                        sleep(0.7)
                        return self.list_files()
                    
                    elif ".py" != selected_file[-3:]:
                        print(f"[!] Cannot compile {selected_file.split('.')[-1]} files")
                        sleep(0.7)
                        return self.list_files()
                    
                    return selected_file
                else:
                    print(f"Số bạn chọn phải nằm trong khoảng từ 1 đến {num_files}")
                    sleep(0.7)
                    return self.list_files()
                
            elif choice.lower() == "dl":
                files = listdir()
                for file in files:
                    if file.endswith('.txt'):
                        try:
                            remove(file)
                            print(f"Đã xóa file: {file}")
                        except Exception as e:
                            print(f"Lỗi khi xóa file {file}: {e}")
                sleep(0.7)
                return self.list_files()
            
            else:
                raise ValueError
            
        except ValueError:
            print("\"Int\" value type only")
            sleep(0.7)
            return self.list_files()
    def re_configuration(self, data):
        func_content = False
        response = []
        data = data.split("\n")
        for i in data:
            if i[0:4] != "def ":
                if func_content:
                    if i[0].isnumeric() or i[0].isalpha():
                        func_content = False
                        continue
                    response.append(i)
                continue
            
            elif i[0:4] == "def ":
                func_content = True
                response.append(i)
                continue
        return "\n".join(response)

    def remove_hash(self, data):
        response = []
        data = data.split("\n")
        for i in range(len(data)):
            if len(data[i]) == 0:
                continue
            strg = data[i].replace("\\t", "").replace(" ", "")
            try:
                if strg[0] == "#":
                    continue
            except:
                continue
            response.append(data[i])
        
        return "\n".join(response)
    
    def add_hash(self, data, author, train_url):
        base_response = [
            f"# AUTHOR : {author}",
            f"# LINK : {train_url}"
        ]
        data = data.split("\n")
        base_response += data
        return "\n".join(base_response)
    
    def runs(self, path = None):
        
        def check_valid(url):
            if self.base_url not in url:
                return False
            if url.count("/") != 4:
                return False
            
            id = url.split("/")[-1]
            try:
                id = int(id)
                return True
            except:
                return False
            
        self.banner()
        if path == None:
            path = self.list_files()
        read_data = open(path, "r", encoding="utf-8").read()
        
        if self.base_url not in read_data:
            
            print(f"[+] Không tìm thấy link trong files \"{path}\", vui lòng nhập link bài tập tại đây")
            base_url = input("[~] LINK : ")
            
            if not check_valid(base_url):
                print("[!] Link không đúng định dạng, vui lòng nhập lại!")
                sleep(0.7)
                return self.runs(path)
            
            dataset = config(base_url).get_case()
            
        else:
            id      = read_data.split(self.base_url)[1].split("\n")[0]
            dataset = config(f"{self.base_url}{id}").get_case()

        func_name   = dataset[-1]["funcname"].lower()
        if func_name not in read_data.lower():
            print("[+] Function không trùng khớp!!")
            open(path, "w", encoding="utf-8").write(read_data.replace(self.base_url, ""))
            sleep(0.7)
            return self.runs(path)
        
        clone               = read_data.lower()    
        indx                = clone.index(func_name)
        read_data_function  = read_data[indx: indx + len(func_name)]
        read_data           = read_data.replace(read_data_function, func_name)
        based_case          = []

        for i in dataset:
            if "author" in i:
                break
            based_case += [[",".join(i["input"]),i["output"]]]
        
        open(path, "w", encoding="utf-8").write(self.add_hash(self.re_configuration(self.remove_hash(read_data)), dataset[-1]["author"], dataset[-1]["train_link"]))
        read_data = open(path, "r", encoding="utf-8").read()

        runcase(based_case, read_data, func_name).run()
        
        try:
            print("[Ctrl + C to Exited]")
            input("[Enter to continue compile the programs]")
            return exec(open(__file__, "r", encoding="utf-8").read(), globals())
        except KeyboardInterrupt:
            self.banner()
            return
        
if __name__ == "__main__":
    run().runs()