import json
import os
import subprocess
import sys
import time
from getpass import getpass
from threading import Thread
from flask import Flask

from flask import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mode = sys.argv[1] if len(sys.argv) > 1 else 'put'
if mode == 'put':
    username = sys.argv[2] if len(sys.argv) > 2 else input("Username: ")
    password = sys.argv[3] if len(sys.argv) > 3 else getpass()
scrape = bool(sys.argv[4]) if len(sys.argv) > 4 else False
src_path = os.path.abspath(os.path.dirname(sys.argv[0]))
chrome_driver_path = os.path.join(src_path, "chromedriver.exe")
chrome_args = "--headless --log-level=1"
db_path = os.path.join(os.path.expanduser("~"), "cp_dump.json")
url = 'https://www.facebook.com/groups/140214169783476/?sorting_setting=CHRONOLOGICAL'
text_filter = lambda s: "pasture" in s.lower() or "5th" in s.lower() or "mango" in s.lower() or "net park" in s.lower()
poll_time = 10
timeout = 10

epoch_to_local = lambda t: time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(t))
app = Flask(__name__)

@app.route('/')
def hello():
    with open(db_path, 'r') as file_dump: posts_data = json.load(file_dump)
    mode = request.args.get('mode', default='dump')
    if mode == 'dump':
        dump_str = ""
        for (post_id, data) in sorted(posts_data.items(), key=lambda tup: tup[0]):
            mark = "\u2588 " if text_filter(data['text']) else ""
            dump_str += f"{data['timestamp']}:\t{mark}{data['text']}" + "\n<br />"
        return dump_str
    elif mode == 'fdump':
        fdump_str = ""
        for (post_id, data) in sorted(posts_data.items(), key=lambda tup: tup[0]):
            mark = "\u2588 " if text_filter(data['text']) else ""
            if not mark: continue
            fdump_str += f"{data['timestamp']}:\t{mark}{data['text']}" + "\n<br />"
        return fdump_str
    else:
        return json.dumps(posts_data)

def selenium_post_generator(do_scrape=False):
    print(f"do_scrape: {do_scrape}")
    try:
        chrome_options = Options()
        for arg in chrome_args.split(" "): chrome_options.add_argument(arg)
        posts_data = {}
        with webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options) as driver:
            driver.get(url)
            user_field = driver.find_element_by_name('email')
            pass_field = driver.find_element_by_name('pass')
            login_button = driver.find_element_by_name('login')
            user_field.send_keys(username)
            pass_field.send_keys(password)
            login_button.click()
            while(True):
                if do_scrape:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                else:
                    driver.get(url)
                html = driver.find_element_by_tag_name('html')
                posts = WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'userContentWrapper')))
                for post in posts:
                    try:
                        epoch = int(post.find_element_by_css_selector('abbr._5ptz.timestamp.livetimestamp').get_property('dataset')['utime'])
                        text = post.text[ :post.text.index("\nLike\n")].replace("\n", " ")
                        posts_data[epoch] = {
                            'text': text,
                            'timestamp': epoch_to_local(epoch),
                        }
                    except BaseException as e: print(e)
                yield posts_data
                time.sleep(poll_time)
    except BaseException as e: print(e)

def curl_post_generator():
    try:
        while True:
            get_value = subprocess.run("curl https://saepius.serveo.net?mode=json", capture_output=True).stdout.decode('utf-8', errors='ignore')
            posts_data = json.loads(get_value)
            yield posts_data
            time.sleep(poll_time)
    except BaseException as e: print(e)

def beep(beeps=4):
    for _ in range(beeps):
        print("\a" * 2)
        time.sleep(1)

def display_posts(posts_data, remembered_posts):
    print('|||\n' * 100 + f" === {epoch_to_local(time.time())} === ")
    for (post_id, data) in sorted(posts_data.items(), key=lambda tup: tup[0]):
        mark = "\u2588 " if text_filter(data['text']) else ""
        print(f"{data['timestamp']}:\t{mark}{data['text']}")
        if mark and post_id not in remembered_posts: beep()
        remembered_posts += [post_id]

def append_to_db(new_posts):
    try:
        with open(db_path, 'r') as file_dump: old_posts = json.load(file_dump)
    except BaseException as e:
        print(e)
        old_posts = {}
    posts = {**old_posts, **new_posts}
    with open(db_path, 'w') as file_dump: json.dump(posts, file_dump, indent=4)
    print(f"db file written to: {db_path}")

def put_main():
    Thread(target=app.run, kwargs={'port': 3000}, daemon=True).start()
    Thread(target=subprocess.run, args=("bash -c 'while (true) do sleep 1 && ssh -R saepius.serveo.net:80:localhost:3000 serveo.net; done;'", ), daemon=True).start()
    remembered_posts = []
    for new_posts in selenium_post_generator(scrape):
        display_posts(new_posts, remembered_posts)
        append_to_db(new_posts)

def get_main():
    remembered_posts = []
    for new_posts in curl_post_generator():
        if len(remembered_posts) == 0:
            remembered_posts = list(new_posts.keys())
        display_posts(new_posts, remembered_posts)

if __name__ == '__main__':
    {
        'put': put_main,
        'get': get_main,
    }[mode]()
