import os, json, datetime
from pathlib import Path

class JSONManager():

    def __init__(self) -> None:
        self.json = ""

    def load_server(self, server_name:str, user_name:str, return_bool:bool):
        y = os.path.join(os.path.dirname(__file__), "credits")
        os.makedirs(y, exist_ok=True)
        self.path = Path(y + "\\{NAME}.json".format(NAME = server_name))
        if os.path.exists(self.path) and self.path.suffix == '.json':
            try:
                if(os.path.getsize(self.path) == 0):
                    return False
                f = open(self.path, 'r')
                obj = json.load(f)
                self.json = obj
                f.close()   
                if(str(user_name) in obj.keys()):
                    if(return_bool):
                        return True
                    else:
                        return obj[str(user_name)]
                else:
                    if(return_bool):
                        return False
                    else:
                        return "Not Found"
            except Exception as ex:
                print("load from server failed")
                print(ex)
        else:
            print("Error")

        pass

    def save_to_server(self, server_name:str, user_name:str, value:int) -> bool:
        y = os.path.join(os.path.dirname(__file__), "credits")
        os.makedirs(y, exist_ok=True)
        self.path = Path(y + "\\{NAME}.json".format(NAME = server_name))
        try:
            if(os.path.getsize(self.path) == 0):
                f = open(self.path, 'w')
                x = {str(user_name): value}
                json.dump(x, f)
            else:
                f = open(self.path, 'r')
                obj = json.load(f)
                f.close()
                f = open(self.path, 'w').close()
                f = open(self.path, 'w')
                obj[str(user_name)] = value
                json.dump(obj, f)
            f.close()
            return True
        except Exception as ex:
            print("save to server failed")
            print(ex)
        pass

    def daily(self, server_name:str, user_name:str):
        y = os.path.join(os.path.dirname(__file__), "dailies")
        os.makedirs(y, exist_ok=True)
        x = y + "\\{NAME}.json".format(NAME = server_name)
        self.path = Path(x)
        try:
            if(not(os.path.exists(self.path)) or os.path.getsize(self.path) == 0):
                f = open(self.path, 'w')
                x = {str(user_name) : datetime.datetime.now().isoformat()}
                json.dump(x, f)
            else:
                f = open(self.path, 'r')
                obj = json.load(f)
                f.close()
                if(str(user_name) in obj.keys()):
                    newtime = datetime.datetime.now()
                    oldtime = datetime.datetime.fromisoformat(obj[str(user_name)])
                    diff = newtime - oldtime
                    if(diff > datetime.timedelta(hours=24)):
                        f = open(self.path, 'w').close()
                        f = open(self.path, 'w')
                        obj[str(user_name)] = datetime.datetime.now().isoformat()
                        json.dump(obj, f)
                        f.close()
                        return True
                    else:
                        return diff
                else:
                    f = open(self.path, 'w').close()
                    f = open(self.path, 'w')
                    obj[str(user_name)] = datetime.datetime.now().isoformat()
                    json.dump(obj, f)
                    f.close()
                    return True
        except Exception as ex:
            print("daily is failing")
            print(ex)        
    
