import pandas as pd
import time
import datetime
import csv
import os
import sys
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
from keys import YOUR_MAIL_ADDRESS, YOUR_PASSWORD



# __name__はこのモジュールの名前
logger = logging.getLogger(__name__)


BASE_URL = 'https://www.instagram.com'

login_url = 'https://www.instagram.com/accounts/login/'

query = '<query>'

logging.basicConfig(filename=query + '.log', level=logging.INFO)



options = Options()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1280,1024')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--no-sandbox')
#options.add_argument('--load-images=false')
options.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/67.0.3396.87 Safari/537.36')
driver = webdriver.Chrome(executable_path='/home/<USERNAME>/local/bin/chromedriver', chrome_options=options)

block_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "block.PNG")
block2_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "block2.PNG")



def setup(url):
    # <input class="_2hvTZ pexuQ zyHYP" id="f18dc2723b94ad8" aria-label="Phone number, username, or email" aria-required="true" autocapitalize="off" autocorrect="off" maxlength="75" name="username" type="text" value="">
    # <input class="_2hvTZ pexuQ zyHYP" id="f29b4461abba218" aria-label="Phone number, username, or email" aria-required="true" autocapitalize="off" autocorrect="off" maxlength="75" name="username" type="text" value="" aria-describedby="slfErrorAlert">
    #driver.save_screenshot(block_png)
    while True:
        try:
            driver.get(url)
            driver.maximize_window()
            name_btn = WebDriverWait(driver, 15).until(
                #EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div/div[1]/input'))
                EC.presence_of_element_located((By.NAME,'username'))
            )
        except NoSuchElementException:
                print(f'\n{traceback.format_exc()}')
                continue
        else:
            break
    name_btn.send_keys(MAIL_ADDRESS)
    
    # <input class="_2hvTZ pexuQ zyHYP" id="f134fe797fdcfe" aria-label="パスワード" aria-required="true" autocapitalize="off" autocorrect="off" name="password" type="password" value="">'
    while True:
        try:
            pw_btn = WebDriverWait(driver, 15).until(
                #EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/div[1]/input'))
                EC.presence_of_element_located((By.NAME,'password'))
            )
        except NoSuchElementException:
            print(f'\n{traceback.format_exc()}')
            continue
        else:
            break
    pw_btn.send_keys(PASSWORD)
    
    # <button class="_5f5mN       jIbKX KUBKM     pm766    " disabled="">Log in</button>
    while True:
        try:
            input_btn = WebDriverWait(driver, 15).until(
                #EC.presence_of_element_located((By.XPATH,'//form[@class="HmktE"]/span[@class="-Qhn2 _1OSdk"]/button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'))
                EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button'))
            )
            driver.save_screenshot(block_png)
        except:
            continue
        else:
            break
    input_btn.click()
    time.sleep(random.randint(20,24))
    # https://www.instagram.com/#reactivated
    driver.save_screenshot(block_png)
    c_url =  driver.current_url

    return c_url

def input_query(url, query):
    while True:
        try:
            driver.get(url)
            driver.maximize_window()
            input_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
            )
        except NoSuchElementException:
            print(f'\n{traceback.format_exc()}')
            continue
        else:
            break
    input_btn.send_keys(query)
    while True:
        try:
            tag_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]'))
            )
        except NoSuchElementException:
            print(f'\n{traceback.format_exc()}')
            continue
        else:
            break
    tag_btn.click()

    driver.implicitly_wait(10)
    l_url = driver.current_url

    return l_url


def get_post_urls(url):
    urls = []
    while True:
        try:
            driver.get(url)
        except:
            continue
        else:
            break
    driver.maximize_window()
    driver.implicitly_wait(15)
    # <div style="flex-direction: column; padding-bottom: 0px; padding-top: 0px;">
    html_source = driver.page_source
    soup= BeautifulSoup(html_source, 'html.parser')

    driver.save_screenshot(block_png)
    article = soup.find('article', class_="qxft6")
    top_block = article.find('div', class_="EZdmt")
    #_top_block = top_block.find('div').find('div')
    _top_block = top_block.find_all('div')[1]
    # <div class="Nnq7C weEfm">
    top_image_blocks = _top_block.find_all('div', class_="Nnq7C weEfm")
    #print(len(top_image_blocks))
    for top_image_block in top_image_blocks:
        #import pdb; pdb.set_trace()
        #_top_image_blocks = top_image_block.find_all('div', class_="v1Nh3 kIKUG  _bz0w")
        top_image_blocks_hrefs = top_image_block.find_all('div', class_="v1Nh3 kIKUG _bz0w")
        for top_image_blocks_href in top_image_blocks_hrefs:
            try:
                # <a href=
                #import pdb; pdb.set_trace()
                href = top_image_blocks_href.find('a').get('href')
                if urljoin(BASE_URL, href) not in urls:
                    urls.append(urljoin(BASE_URL, href))
                    driver.save_screenshot(block2_png)
                    #print('・・・ LINE 174 >>>', urls)
            except:
                pass
            #print('・・・ LINE 177  No URLs!・・・')
    
    #print("・・・ LINE 179 ・・・ getting URLs's conts is >>>", len(urls))
    #print('・・・ LINE 179 >>>', urls)

    main_block = article.find_all('div')[5]
    main_block_style = main_block.find('div', style="flex-direction: column; padding-bottom: 0px; padding-top: 0px;")
    #import pdb; pdb.set_trace()
    _main_blocks = main_block_style.find_all('div', class_="Nnq7C weEfm")
    #print(len(_main_blocks))
    for _main_block in _main_blocks:
        main_blocks_hrefs = _main_block.find_all('div', class_="v1Nh3 kIKUG  _bz0w")
        for main_blocks_href in main_blocks_hrefs:
            try:
                href = main_blocks_href.find('a').get('href')
                if urljoin(BASE_URL, href) not in urls:
                    urls.append(urljoin(BASE_URL, href))
                    driver.save_screenshot(block2_png)
                #print('・・・ LINE 193 >>>', urls)
                time.sleep(random.randint(3,6))
            except:
                pass
            #print('・・・ LINE 197  No URLs!・・・')
        
        #print("・・・ LINE 199 ・・・ getting URLs's conts is >>>", len(urls))
        print('・・・ LINE 199 >>>', urls)
            
    return urls

def get_acct_page(url):
    while True:
        try:
            driver.get(url)
            driver.maximize_window()
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a'))
            )
        except NoSuchElementException:
            print(f'\n{traceback.format_exc()}')
            continue
        else:
            break
    # userpage_url
    userpage_url = username.get_attribute('href')

    return userpage_url

def get_user_post_urls(url):
    urls = []
    while True:
        try:
            driver.get(url)
        except:
            continue
        else:
            break
    driver.maximize_window()
    driver.implicitly_wait(15)
    html_source = driver.page_source
    soup= BeautifulSoup(html_source, 'html.parser')

    driver.save_screenshot(block_png)
    # <div class="Nnq7C weEfm">
    # # <div class="v1Nh3 kIKUG  _bz0w">
    # # # <a href="/p/BlD082Xn1-e/?taken-by=hirono.qoo">
    #import pdb; pdb.set_trace()
    main_blocks = soup.find_all('div', class_="Nnq7C weEfm")
    for main_block in main_blocks:
        _main_blocks = main_block.find_all('div', class_="v1Nh3 kIKUG _bz0w")
        for _main_block in _main_blocks:
            user_post_href = _main_block.find('a').get('href')
            if urljoin(BASE_URL, user_post_href) not in urls:
                urls.append(urljoin(BASE_URL, user_post_href))
                driver.save_screenshot(block2_png)
    
    #print('・・・ LINE 252 >>>', urls)
            
    return urls

def scrape(url, tag):
    """
    searching_tag
    username
    posting_conts
    followers
    following
    text
    hashtag
    likes
    posting_date
    posting_datetime
    date
    datetime
    userpage_url
    posting_url

    """
    
    data = {}
    notFound = []
    while True:
        try:
            driver.get(url)
            driver.maximize_window()
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a'))
            )
        except NoSuchElementException:
            print(f'\n{traceback.format_exc()}')
            continue
        else:
            break

    driver.save_screenshot(block_png)

    
    # 初期化
    for r in  ['searching_tag','username', 'posting_conts', 'followers', 'following', 'text', 'hashtag', 'likes', 'posting_date','posting_datetime','date', 'datetime', 'userpage_url','posting_url']:
        data[r] = None
    
    
    # posting url
    posting_url = driver.current_url
    data['posting_url'] = posting_url

    # searching_tag
    data['searching_tag'] = tag
    print('【searching_tag】', data['searching_tag'])

    # username
    # <a class="FPmhX notranslate nJAzx" title="lunastella4_foodie" href="/lunastella4_foodie/">lunastella4_foodie</a>
    try:
        #data['username'] = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a').text
        data['username'] = username.text
    except Exception:
        notFound.append('username')
    print('【username】', data['username'])

    # user's & others' text
    # hashtag
    # <a class="" href="/explore/tags/<QUERY>/">#<QUERY></a>
    try:
        tmp = driver.find_element_by_xpath("//a[contains(text(), data['username'])]/following-sibling::span").text
        #import pdb; pdb.set_trace()
        data['text'] = tmp.replace(' ', '').strip()
        m_tags = re.findall('#.*', tmp)
        if m_tags:
            tags = ''
            for m_tag in m_tags:
                if m_tag:
                    #import pdb; pdb.set_trace()
                    _m_tag = m_tag.replace(' ', '').strip()
                else:
                    _m_tag = m_tag
                tags += _m_tag
                tags += ' '
            data['hashtag'] = tags
        else:
            notFound.append('hashtag')
    except Exception:
        notFound.append('text')
    print('【text】', data['text'])
    print('【hashtag】', data['hashtag'])

    # likes
    try:
        tmp = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/a/span').text
        data['likes']  = tmp.replace(',', '')
    except Exception:
        notFound.append('likes')
    print('【likes】', data['likes'])

    # posting_datetime, posting_date
    try:
        # <time class="_1o9PC Nzb55" datetime="2018-07-09T15:41:44.000Z" title="Jul 10, 2018">12 hours ago</time>
        tmp = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[2]/a/time')
        _tmp = tmp.get_attribute('datetime')
        m_datetime = re.search('\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}', _tmp)[0]
        if m_datetime:
            #import pdb; pdb.set_trace()
            data['posting_datetime'] = m_datetime.replace('T', ' ')
            m_time = re.search('\d{4}-\d{1,2}-\d{1,2}', m_datetime)[0]
            if m_time:
                data['posting_date'] = m_time
            else:
                notFound.append('posting_date')
        else:
            notFound.append('posting_datetime')

    except Exception:
        notFound.append('posting_datetime')
        notFound.append('posting_date')
    print('【posting_datetime】', data['posting_datetime'])
    print('【posting_date】', data['posting_date'])
    

    # date
    data['date'] = datetime.datetime.now().strftime('%Y-%m-%d')

    if len(notFound)!=0:
        pass
    
    # datetime
    data['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if len(notFound)!=0:
        pass

    ####################################################################################
    ######## From here, posting User's Page ############################################
    ####################################################################################

    # userpage_url
    # posting_conts
    # followers
    # following
    try:
        # userpage_url
        userpage_url = username.get_attribute('href')
        data['userpage_url'] = userpage_url
        while True:
            try:
                driver.get(userpage_url)
                driver.maximize_window()
                posting_conts = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'))
                )
            except NoSuchElementException:
                print(f'\n{traceback.format_exc()}')
                continue
            else:
                break
        
        # posting_conts
        try:
            tmp = posting_conts.text
            data['posting_conts'] = tmp.replace(',', '')
        except Exception:
            notFound.append('posting_conts')

        # followers
        # <span class="g47SY " title="636,427">636k</span>
        try:
            tmp = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
            try:
                _tmp = tmp.get_attribute('title')
                data['followers'] = _tmp.replace(',', '')
            except:
                data['followers'] = tmp.text
        except Exception:
            notFound.append('followers')

        # following
        try:
            tmp = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
            data['following'] = tmp.replace(',', '')
        except Exception:
            notFound.append('following')

    except Exception:
        notFound.append('userpage_url')
    print('【userpage_url】', data['userpage_url'])
    print('【posting_conts】', data['posting_conts'])
    print('【followers】', data['followers'])
    print('【following】', data['following'])

    return data


if __name__ == '__main__':
    datas = []
    start = time.time()

    check_url = setup(login_url)
    print(check_url)
    first_list_url = input_query(check_url, query)
    print('■', first_list_url)
    current_url = first_list_url
    print('■■', current_url)

    urls = []
    sleep_conts = 1
    while True:
        if sleep_conts <= 1:
            urls.extend(get_post_urls(current_url))
            urls_conts = len(urls)
            print(str(sleep_conts) + 'th get_urls() >>>', len(urls))
            # 9th urls by get_urls()
            time.sleep(random.randint(3,6))
            sleep_conts = sleep_conts + 1
        else:
            break
    print(urls)

    current_urls = []

    for post_url in urls:
        current_urls.extend(get_acct_page(post_url))
    
    for current_url in current_urls:
        user_post_urls = []
        sleep_conts = 1
        while True:
            if sleep_conts <= 1:
                user_post_urls.extend(get_user_post_urls(current_url))
                user_post_urls_conts = len(user_post_urls)
                print(str(sleep_conts) + 'th get_user_post_urls() >>>', len(user_post_urls))
                time.sleep(random.randint(3,6))
                sleep_conts = sleep_conts + 1
            else:
                break
    
    crawl_number = 1
    print(user_post_urls)
    user_post_urls_conts = len(user_post_urls)
    print('・・・', str(user_post_urls_conts) + 'th postpages!')
    for user_post_url in user_post_urls:
        print('・・・・', user_post_url)
        datas.append(scrape(user_post_url, query))
        time.sleep(random.randint(3,8))
        print('【' , str(crawl_number) + '/'+ str(user_post_urls_conts), '】',  user_post_url)
        crawl_number = crawl_number + 1
    
    
    column_order =  ['searching_tag','username', 'posting_conts', 'followers', 'following', 'text', 'hashtag', 'likes', 'posting_date','posting_datetime','date', 'datetime', 'userpage_url','posting_url']
    if len(datas)!=0:
        df = pd.DataFrame(datas)
        df.to_csv('insta_scraper_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.csv', sep=',',encoding='UTF-8',index=False, quoting=csv.QUOTE_ALL, columns=column_order)
        df.to_csv('insta_scraper_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.tsv', sep='\t',encoding='UTF-8',index=False, quoting=csv.QUOTE_ALL, columns=column_order)
    

    end = time.time()
    print("process {0} ms".format((end - start) * 1000))
    sys.exit()
    
driver.quit()