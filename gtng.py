# coding:utf-8

from requests_oauthlib import OAuth1Session

import json
import os
import glob
import sys
import urllib
import cv2

oath_key_dict = {}
save_path = os.path.abspath("./savedir/")

#save_pathの下にアニメじゃないファイル移動先掘ってね
animejanaipath = "animejanai"

twitterkey_jsonfilepath = "./twitterkey.json"
image_number = 0
get_pages = 3
count = 60
NOTANIMEPREFIX = ""
NOTANIMESUFFIX = ""

def create_oath_session(jsonfilepath):
    with open(jsonfilepath, 'r') as f:
        json_data = json.load(f)

    oath = OAuth1Session(
        json_data["consumer_key"],
        json_data["consumer_secret"],
        json_data["access_token"],
        json_data["access_token_secret"]
    )
    return oath

def fav_tweets_get(page, jsonfilepath):
    url = "https://api.twitter.com/1.1/favorites/list.json?"
    params = {
        #任意のtwitterID,@以下の文字列
        "screen_name": "rin7914",
        "page": page,
        "count": count,
        "include_entities": 1
    }
    oath = create_oath_session(jsonfilepath)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print("Error code: {0}".format(responce.status_code))
        return None
    tweets = json.loads(responce.text)
    return tweets

def image_saver(tweets):
    global image_number
    for tweet in tweets:
        try:
            image_list = tweet["extended_entities"]["media"]

            for image_dict in image_list:
                url = image_dict["media_url"]
                url_large = url + ":large"
                with open(save_path +"/"+str(image_number) + "_" + os.path.basename(url), 'wb') as f:
                    img = urllib.request.urlopen(url_large, timeout=5).read()
                    f.write(img)
                print("done")
                image_number+=1

        except KeyError:
            print("KeyError:画像を含んでいないツイートです。")
        except:
            print("Unexpected error in imagesaver:", sys.exc_info()[0])

#戻りがtrueならあにめ
def is_animefile(filename, cascade_file = "./lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (24, 24))
    return (len(faces) > 0)

#捨てると必要なものをステそうなのでリネームで対応したい（希望
#pre + filename + suf＝変更後のファイル名です
def rename_file(filename, pre, suf = ""):
    try:
        #何回も同じことやってまううう（todo
        dirname = os.path.dirname(filename)
        if dirname.endswith("\\") is False:
            dirname += "\\"
        renamedfilename = dirname + animejanaipath + "\\" + pre + os.path.basename(filename) + suf
        os.rename(filename, renamedfilename)
    except OSError as oserr:
        print("OSError:ファイル名変更に失敗しました:{0}", oserr)
    except:
        print("Unexpected error in renamefile:", sys.exc_info()[0])


#アニメファイルとそうでないのとの振り分け
#アニメじゃないファイルはrenameするという
def aloc_animefile(save_dir):
    files = glob.glob(save_dir + "/*.jpg")
    files += glob.glob(save_dir + "/*.png")
    for animefilename in files:
        if is_animefile(animefilename) is False:
            rename_file(animefilename, NOTANIMEPREFIX, NOTANIMESUFFIX)

if __name__ == "__main__":
    for i in range(1, get_pages):
        tweets = fav_tweets_get(i, twitterkey_jsonfilepath)
        image_saver(tweets)
    aloc_animefile(save_path)

