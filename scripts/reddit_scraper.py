#!/usr/bin/env python3

""" NOTES:
https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
http://chromedriver.chromium.org/getting-started/getting-started
https://selenium-python.readthedocs.io/waits.html

USAGE:
pipenv --python=3
pipenv shell
pip install --upgrade -r requirements.txt && python scraper.py
"""

import json
import os
import re
import sys
import time

import youtube_dl
from selenium import webdriver

script_dir = os.path.dirname(os.path.realpath(__file__))
#start_url = "https://m.reddit.com/r/watchpeopledie/top?t=all"
#download_dir = os.path.join(script_dir, "wpd_downloads", "")
start_url = "https://m.reddit.com/r/aww/top?t=all"
download_dir = os.path.join(script_dir, "aww_downloads", "")
checkpoint_path = os.path.join(download_dir, "checkpoint.json")
chrome_driver = os.path.join(script_dir, "chromedriver.exe")
wait_time = 3
score_padding = 6  # support only for 'k' unit numbers
chrome_arguments = [
    "--window-size=360x640",
    "--user-agent='Mozilla/5.0 (Linux; Android 6.0.1; SM-G900V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'"
]
filtered_filename_regex = "(_| |\"|:|\\||\\?|\\*|<|>|/|\\\\)"
max_filename_length = 120
ydl_opts = {'format': "bestvideo+bestaudio/best"}

def process_popups(driver):
    popup_css_elements = [
        "button.quarantineinterstitial__button",
        "button.nsfwinterstitial__button",
        "span.xpromopopup__actionbutton"
    ]
    for popup_css in popup_css_elements:
        try:
            popup_element = driver.find_element_by_css_selector(popup_css)
            popup_element.click()
            print(f"Clicked: {popup_css}")
            time.sleep(wait_time)
        except Exception as e: pass

def navigate_interstitial(driver, navigate, *args):
    print(f"Navigating: {navigate.__name__}")
    navigate(*args)
    time.sleep(wait_time)
    process_popups(driver)
    return driver.current_url

def process_posts(driver):
    print(f"Scraping for posts")
    processed_posts = []
    posts = driver.find_elements_by_css_selector("article.post.size-compact")
    for post in posts:
        thread_link = post.find_element_by_css_selector("a.postheader__post-title-line").get_attribute("href")
        raw_score = post.find_element_by_css_selector("div.votingbox__score").text
        raw_title = post.find_element_by_css_selector("a.postheader__post-title-line").text
        processed_posts += [{
            'id': re.search("/comments/(.+?)/", thread_link).group(1),
            'score': raw_score if raw_score[-1] != "k" else str(int(float(raw_score[ :-1]) * 1000)).rjust(6, "0"),
            'media_link': post.find_element_by_css_selector("a.postheader__author-link").get_attribute("href"),
            'title': re.sub(filtered_filename_regex, "", raw_title.title())[ :max_filename_length]
        }]
    return processed_posts

def unwanted_post(post):
    # TODO: additional media_link processing like image download
    downloaded_ids = [re.search("_(.+?)_", downloaded_file).group(1) for downloaded_file in os.listdir(download_dir) if re.search("_(.+?)_", downloaded_file) != None]
    if post['id'] in downloaded_ids:
        print(f"Already downloaded post with id: {post['id']}")
        return True
    return False

def download_post(post):
    if unwanted_post(post): return
    with youtube_dl.YoutubeDL({'outtmpl': f"{download_dir}{post['score']}_{post['id']}_{post['title']}.%(ext)s", **ydl_opts}) as ydl:
        ydl.download([post['media_link']])

def driver_closed(driver):
    try:
        driver.title
        return False
    except:
        return True

def download_posts(posts, driver):
    failed_posts = []
    for post in posts:
        if driver_closed(driver):  # Stop downloading whenever driver gets closed
            print(f"Downloading stopped because driver was closed: {driver}")
            break
        print(f"Downloading post: {post}")
        try: download_post(post)
        except Exception as e:
            print(f"Failure in downloading post: {e}")
            failed_posts += [post]
    return failed_posts

def process_and_download_and_store_to(driver, stored_posts, failed_posts):
    new_stored_posts = process_posts(driver)
    new_failed_posts = download_posts(new_stored_posts, driver)
    stored_posts.extend(new_stored_posts)
    failed_posts.extend(new_failed_posts)

if __name__ == '__main__':
    if not os.path.exists(download_dir): os.makedirs(download_dir)
    if input("Load from checkpoint file (y)?: ") == "y":
        with open(checkpoint_path, 'r') as checkpoint_file:  # TODO: try locals().update(checkpoint_json)
            checkpoint_json = json.load(checkpoint_file)
            (last_url, failed_posts, stored_posts) = (checkpoint_json['last_url'], checkpoint_json['failed_posts'], checkpoint_json['unique_posts'])  # unique_posts != stored_posts
        print("Start running stuff!")
        import code; code.interact(local={**locals(), **globals()})
    (last_url, failed_posts, stored_posts) = (None, [], [])
    try:
        print("Started webscraping - close the opened window to interrupt.")
        chrome_options = webdriver.chrome.options.Options()
        for arg in chrome_arguments: chrome_options.add_argument(arg)
        with webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver) as driver:
            last_url = navigate_interstitial(driver, driver.get, start_url)
            process_and_download_and_store_to(driver, stored_posts, failed_posts)
            while True:
                last_url = navigate_interstitial(driver, driver.find_element_by_css_selector("a.paginationbuttons__button.m-next").click)
                process_and_download_and_store_to(driver, stored_posts, failed_posts)
    except Exception as e: print(f"Failure webscraping: {e}")
    unique_posts = list({post['id']: post for post in stored_posts}.values())
    with open(os.path.join(download_dir, "checkpoint.json"), 'w') as checkpoint_file:
        checkpoint_file.write(json.dumps({'last_url': last_url, 'failed_posts': failed_posts, 'unique_posts': unique_posts}, indent=4))
        print(f"Successfully checkpoint file written: {checkpoint_file}")    
