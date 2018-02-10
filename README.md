指定した@～～～がfavしたツイを見て、そこに画像があればひっぱります

1.twitterkey.jsonにツイAPI利用の必要事項いれます
さんこう　http://phiary.me/twitter-api-key-get-how-to/
2.gtng.pyの13行目くらいからの設定

save_path = os.path.abspath("./savedir/")

#save_pathの下にアニメじゃないファイル移動先掘ってね
animejanaipath = "animejanai"

twitterkey_jsonfilepath = "./twitterkey.json"
image_number = 0
#多く指定すると画像も多くなるけどあんまり多いとツイAPIが一時的に利用不能になるかもしれないやつ
get_pages = 3
count = 60

3.2のもうちょい下に
        "screen_name": "",
        があるので、ここを適当なツイID（＠ぬき）をいれます

4.カレントをgtng.pyのとこにうつして python gtng.py
  3で指定したツイIDのfavツイの画像を引っ張ってきます。
  なので絵描きさんとかを狙い撃ちすると効率がいいです


  何の効率だ


todo ツイID指定をコマンドラインかtxtファイルかどっちかからの指定にします。収集の数とかも
todo 1ファイルゲットのあいまにスリープいれよう
todo 









おおもと

http://prpr.hatenablog.jp/entry/2015/05/12/Python3%E3%81%A7%E3%81%B5%E3%81%81%E3%81%BC%E3%81%A3%E3%81%9F%E3%83%84%E3%82%A4%E3%83%BC%E3%83%88%E3%81%AB%E6%B7%BB%E4%BB%98%E3%81%95%E3%82%8C%E3%81%9F%E7%94%BB%E5%83%8F%E3%82%92%E4%B8%80%E6%8B%AC%E3%83%80

