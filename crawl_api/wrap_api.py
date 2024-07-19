import requests

class config:
    def __init__(self, url) -> None:
        self.headers = {
            'accept'                : 'application/json, text/plain, */*',
            'accept-language'       : 'vi-VN,vi;q=0.9',
            'cache-control'         : 'no-cache',
            'dnt'                   : '1',
            'language'              : 'vn',
            'origin'                : 'https://codelearn.io',
            'pragma'                : 'no-cache',
            'priority'              : 'u=1, i',
            'referer'               : 'https://codelearn.io/',
            'sec-ch-ua'             : '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile'      : '?0',
            'sec-ch-ua-platform'    : '"Windows"',
            'sec-fetch-dest'        : 'empty',
            'sec-fetch-mode'        : 'cors',
            'sec-fetch-site'        : 'same-site',
            'user-agent'            : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        self.url = url
    
    def get_case(self, list_test_case = []):
        id      = self.url.split("/")[-1]
        params  = {
            'activityId'    : id,
            'contextId'     : id,
            'contextType'   : '3',
        }
        
        response    = requests.get(
            url     = 'https://coding.codelearn.io/coding/training/get-code-activity', 
            params  = params, 
            headers = self.headers
        )

        result        = response.json()
        function_name = result["data"]["codeActivity"]["functionName"]
        case_data     = result["data"]["codeActivity"]["listTestCase"]

        for i in case_data:
            if not i["isHidden"]:
                input_params  = i["input"].replace("#", "").split(";")
                while "" in input_params:
                    input_params.pop(input_params.index(""))

                output_params = i["output"]
                list_test_case.append({
                    "input"    : input_params  ,
                    "output"   : output_params ,
                })
        info = {
            "funcname"   : function_name,
            "author"     : result["data"]["codeActivity"]["activity"]["owner"]["userName"],
            "train_link" : "https://codelearn.io/training/" + str(result["data"]["codeActivity"]["activityId"]),  
        }
        list_test_case.append(info)
        return list_test_case
    
#Example : config("https://codelearn.io/training/3234").get_case()
