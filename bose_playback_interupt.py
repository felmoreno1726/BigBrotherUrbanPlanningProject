import requests

data = '<play_info><app_key>CkrAxHSTKAOtl4LyuKwvk33QoyGlj0cC</app_key><url>https://ia802508.us.archive.org/5/items/testmp3testfile/mpthreetest.mp3</url><service>service text</service><reason>reason text</reason><message>message text</message><volume>70</volume></play_info>'

response = requests.post('http://192.168.1.15:8090/speaker', data=data)
