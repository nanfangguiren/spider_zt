import requests
import hashlib
import sys
import re
import base64
import binascii
import json
import os
import click
from Crypto.Cipher import AES
from http import cookiejar

requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数

class Encrypyed():

    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'

    # 登录加密算法 https://github.com/stkevintan/nw_musicbox
    def encrypted_request(self, text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(
            text, self.nonce), sec_key.decode('utf-8'))
        enc_sec_key = self.rsa_encrpt(sec_key, self.pub_key, self.modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        return data

    def aes_encrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(secKey.encode('utf-8'),
                            AES.MODE_CBC, b'0102030405060708')
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16),
                 int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def create_secret_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]


class Netease():
    def __init__(self, timeout=60, cookie_path='.'):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_request(self, url, params):
        data = self.ep.encrypted_request(params)
        resp = self.session.post(url, data=data, timeout=self.timeout)
        result = resp.json()
        if result['code'] != 200:
            print('post_request error')
        else:
            return result

    def search(self, song_name, limit=10):
        # result = self.search(song_name, search_type=1, limit=limit)

        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        params = {
            's': song_name,
            'type': 1,
            'offset': 0,
            'sub': 'false',
            'limit': limit
        }

        result = self.post_request(url, params)

        if result['result']['songCount'] <= 0:
            print('Song {} not existed.'.format(song_name))
            return
        
        # 获取有用信息
        songs = result['result']['songs']
        song_list = [
            {
                'id': song['id'],
                'name':song['name'],
                'author':'+'.join([a['name'] for a in song['ar']])
            }
            for song in songs
        ]

        # 获取下载链接 url
        ids = [song['id'] for song in song_list]
        urls = self.get_url(ids)
        
        for i, song in enumerate(song_list):
            song['url'] = urls[i]

        return song_list

    def get_url(self, song_ids, bit_rate=320000):
        """
        获得歌曲的下载地址
        :params song_id: 音乐ID<int>.
        :params bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
        :return: 歌曲下载地址
        """

        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        csrf = ''
        params = {
            'ids': song_ids,
            'br': bit_rate,
            'csrf_token': csrf
        }

        result = self.post_request(url, params)
        urls = [song['url'] for song in result['data']]

        if urls is None:
            print('Song not available due to copyright issue.')

        return urls

    def download(self, song, folder):
        url = song['url']
        song_name = song['name']
        author = song['author']

        if not os.path.exists(folder):
            os.makedirs(folder)

        fpath = os.path.join(folder, f'{song_name}_{author}.mp3')

        if sys.platform == 'win32' or sys.platform == 'cygwin':
            valid_name = re.sub(r'[<>:"/\\|?*]', '', song_name)
            if valid_name != song_name:
                print('{} will be saved as: {}.mp3'.format(
                    song_name, valid_name))
                fpath = os.path.join(folder, f'{valid_name}_{author}.mp3')

        if os.path.exists(fpath):
            print(f'{song_name} has exist!')
            return
        
        resp = self.download_session.get(
            url, timeout=self.timeout, stream=True)

        length = int(resp.headers.get('content-length'))
        label = 'Downloading {} {}kb'.format(song_name, int(length/1024))

        with click.progressbar(length=length, label=label) as progressbar:
            with open(fpath, 'wb') as song_file:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        song_file.write(chunk)
                        progressbar.update(1024)




if __name__ == '__main__':
    crawler = Netease()
    songs = crawler.search('青', 5)
    # print(songs)
    for song in songs:
        crawler.download(song, './out/Music')


    # timeout = 60
    # output = 'Musics'
    # quiet = True
    # cookie_path = 'Cookie'
    # netease = Netease(timeout, output, quiet, cookie_path)

    # netease.download_song_by_search('青', 5)


    # music_list_name = 'music_list.txt'
    # # 如果music列表存在, 那么开始下载
    # if os.path.exists(music_list_name):
    #     with open(music_list_name, 'r') as f:
    #         music_list = list(map(lambda x: x.strip(), f.readlines()))
    #     for song_num, song_name in enumerate(music_list):
    #         netease.download_song_by_search(song_name, song_num + 1)
    # else:
    #     print('music_list.txt not exist.')
