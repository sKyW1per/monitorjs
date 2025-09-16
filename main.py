import json
import requests

#REMOTEURL = "https://www.superdrug.com/main.ccd1eb1f1fa95c4d.js"
REMOTEURL= "https://api.superdrug.com/api/v2/api-docs"
NAME_FORMER = "former.json"
DISCORDWEBHOOK = "https://discord.com/api/webhooks/1417594008116658367/MArk0d1TzNv5CI1l64ysZjSuCfdC6iTVveNnUKTZQodqgpzt-RGcQxit52WgalvKP70j" 


def getfile(REMOTEURL):
    headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"139\", \"Not;A=Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-GB,en;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i", "Connection": "keep-alive"}
    proxies = {
        "http": "http://127.0.0.1:8080",
        "http": "https://127.0.0.1:8080"
    }
    try:
        r = requests.get(REMOTEURL, timeout=90, headers=headers, proxies=proxies)
        r.raise_for_status()
        print(f"Status code: {r.status_code}")
        return json.loads(r.text)
    except requests.Timeout as e:
        print("Request timed out after 90 seconds.")
        print(f"Details: {e}")
        return False
    except requests.ConnectionError:
        print("Connection error. Unable to reach the server.")
        return False
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return False
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def getformerfile(fname):
    try:
        f = open(fname, "rt")
        jdata = f.readline()
        f.close()
        jparsed = json.loads(jdata) 
        return jparsed
    
    except FileNotFoundError:
        print(str(fname)+" not found")
        return False


def overwritefile(fname, data_new):
    try:
        with open(fname, "w+") as f:
            f.write("test") 
        return fname
    except FileNotFoundError:
        print(str(fname)+" not found or maybe a write acces problem")
        return False


def compare(webhook, data_new, data_old):
    print(webhook)
    #f = open(data_old, "rt")
    #jdata = f.readline()
    #f.close()

    
    for d in data_new["paths"]:
        if d not in data_old["paths"]:
            print(d)
            # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
            data = {
                "content" : d,
                "username" : "Spidey Bot1"
            }
            result = requests.post(DISCORDWEBHOOK, json = data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)
            else:
                print(f"Payload delivered successfully, code {result.status_code}.")
    print("end run apidocs")


def main():
    data_new = getfile(REMOTEURL)
    data_old = getformerfile(NAME_FORMER)
    if data_new != False:
        compare(DISCORDWEBHOOK, data_new, data_old)

    #for d in data:
    #    print(d)
    
    #for d in data["components"]:
    #    print(d)

    #for d in data["info"]:
    #    print(d)

    #TODO: Overwrite file here
    #overwritefile(NAME_FORMER, data_new)

if (__name__ == '__main__'):
    exit_code = main()
    exit(exit_code)
