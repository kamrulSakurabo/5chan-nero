from drivers.driver import get_driver
from .models import Post
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from dateutil.parser import parse
from datetime import datetime
import re
import csv

keyword = "S南美容"
path = 'C:\\Users\\k_has\\OneDrive\\デスクトップ\\5chanCsv'


def search_data():
    driver = get_driver()

    url = "https://5ch.search2ch.info/"
    driver.get(url)
    print("URL LOADED")

    start_date = datetime(2023, 6, 1).date()

    # Here's how to get the current date
    current_date = datetime.now().date()
    try:
        # search box
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gsc-i-id1"]')))
        search_box.clear()
        search_box.send_keys(keyword)
        print("fill up the search box")

        # search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="___gcse_0"]/div/div/form/table/tbody/tr/td[2]/button')))
        search_button.click()
        print("Search button is clicked.")

        # select the Date option
        date_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="___gcse_0"]/div/div/div/div[3]/table/tbody/tr/td[2]/div/div[2]/div[1]/div[2]')))
        date_option.click()
        print('Date option opened')

        date_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="___gcse_0"]/div/div/div/div[3]/table/tbody/tr/td[2]/div/div[2]/div[2]/div[2]/div')))
        actions = ActionChains(driver)
        actions.move_to_element(date_select).click(date_select).perform()
        print('Date option Selected')
        sleep(2)

        for p in range(2, 11):
            for i in range(1, 11):
                xpath_str = f'//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div[1]/div/div[1]/div[{i}]/div[1]'
                parent_item = driver.find_element(By.XPATH, xpath_str)

                if keyword in parent_item.text:
                    link = parent_item.find_element(By.XPATH, './div[1]/div/a')

                    link.click()
                    print(f'enter the new item: {i}')

                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        all_link = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="thread"]/div[3]/ul/li[1]/a')))
                        all_link.click()
                        print('Enter the latest all link')

                        articles = driver.find_elements(By.XPATH, '//article[starts-with(@id, "")]')
                        # Reverse the articles for start from bottom of the page
                        articles = articles[::-1]
                        for article in articles:
                            try:
                                date_time_str = article.find_element(By.XPATH, './details/span[1]').text
                                date_str, time_str = date_time_str.split()
                                date_time_str_clean = re.sub(r'\(.*?\)', '', date_str)
                                date_time_str_clean = f"{date_time_str_clean} {time_str}"
                                if re.match(r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{2}", date_time_str_clean):
                                    date_to_check_datetime = parse(date_time_str_clean)
                                    date_to_check = date_to_check_datetime.date()

                                    if start_date <= date_to_check <= current_date:
                                        body = article.find_element(By.XPATH, './section').text
                                        if keyword in body:
                                            print(
                                                f"The date in article is within the specified range: {date_to_check} time is: {time_str}")
                                            print(f"Keyword found in the article")

                                            title = driver.find_element(By.XPATH, '//*[@id="threadtitle"]').text
                                            user_id = article.find_element(By.XPATH, './details/span[2]').text
                                            userID = user_id.replace("ID:", "")
                                            user_name = article.find_element(By.XPATH,
                                                                             './details/summary/span[2]/b').text
                                            url = driver.current_url
                                            print(f"Title: {title}")
                                            print(f"UserID: {userID}")
                                            print(f"UserName: {user_name}")
                                            # print(f"Body: {body_html}")
                                            print(f"text body: {body}")
                                            print(f"Post Date and Time: {date_to_check},{time_str}")
                                            print(f"URL: {url}")

                                            # save to the database

                                            post = Post(
                                                userId=userID,
                                                title=title,
                                                postDate=date_to_check_datetime,
                                                postBody=body,
                                                postUrl=url,
                                                userUrl=url,
                                                otherUrl=url,
                                                keyword=keyword,
                                            )
                                            exists = Post.objects.filter(postBody=post.postBody,
                                                                         postDate=post.postDate).exists()
                                            if not exists:
                                                post.save()
                                                print('Post saved in database.')
                                            else:
                                                print("Post already exists in database, skipping...")

                                        else:
                                            print(f"{keyword} not found in the article")

                                    else:
                                        print(f"記事内の日付が指定された範囲内にありません。: {date_to_check}")
                                        break
                            except ValueError:
                                print(f"Unexpected date-time format in article: {date_time_str}")
                                continue
                            except Exception as e:
                                print(f"Unable to parse date: {date_time_str}. Error: {e}")
                                continue

                            # switch back to original window
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                    except NoSuchElementException:
                        print("The 'All' link was not found for this item")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

            # back to the next page
            next_button_xpath = f'//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div/div[{p}]'
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            next_button.click()
            sleep(2)
            print(f"Go to the next Page: {p}")

    except NoSuchElementException:
        print('Keyword not found')
    except ElementClickInterceptedException:
        print("The 'All' button was not clickable at the moment of finding it")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    keyword_posts = Post.objects.filter(keyword=keyword)
    if keyword_posts.exists():
        write_posts_to_csv(keyword, keyword_posts)
    else:
        print('Not Created file')


def write_posts_to_csv(keyword, posts):
    keyword = keyword
    fieldnames = ['履歴No', 'No', '既読', 'SNSユーザ/ブログタイトル', 'SNSユーザID/ブログサイト', '投稿日/公開日', '公開場所', '本文',
                  'ユーザリンク', '記事リンク', 'その他リンク', '検出日', '問題ワード通知']
    filename = f"{path}\\{keyword}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i, post in enumerate(posts):
            writer.writerow({
                '履歴No': i + 1,
                'No': post.id,
                '既読': post.alreadyRead,
                'SNSユーザ/ブログタイトル': post.title,
                'SNSユーザID/ブログサイト': post.userId,
                '投稿日/公開日': post.postDate.strftime('%Y-%m-%d %H:%M:%S'),
                '公開場所': post.searchPlace,
                '本文': post.postBody,
                'ユーザリンク': post.postUrl,
                '記事リンク': post.userUrl,
                'その他リンク': post.otherUrl,
                '検出日': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                '問題ワード通知': post.wordNotification

            })
