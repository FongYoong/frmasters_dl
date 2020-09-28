import dependencies as dp

dp.Install()

import sys
import subprocess
import pickle
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

credentials_file = "session/credentials.txt"
custom_user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
login_url = 'https://frontendmasters.com/login/'
target_url = 'https://frontendmasters.com/courses/webpack-fundamentals/ecmascript-modules-esm/'
login_duration = 120 # seconds
cookies_file = "session/cookies.pkl"
video_resolution = '720' # 360 or 720
output_file = "output/output.mp4"

def QuitSession(message):
    print(message)
    driver.quit() if 'driver' in globals() else None
    sys.exit()

try:
    f = open(credentials_file, "r")
    username, password = (f.readline(), f.readline())
except Exception as e:
    QuitSession("{} not found\n".format(credentials_file))
f.close()

session_url = None

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
opts = Options()
opts.add_argument(custom_user_agent) # Refer to https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-web-driver
driver = webdriver.Chrome("{}/{}".format(dp.folder, dp.chrome_name), desired_capabilities=caps, options=opts)

driver.get(login_url)

try:
    cookies = pickle.load(open(cookies_file, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
except pickle.UnpicklingError as e:
    print("Unpickling Error\n", e)
    pass
except Exception as e:
    print(e)
driver.refresh()

try:
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_css_selector('button[data-callback="onSubmit"]').click()
    try:
        WebDriverWait(driver, login_duration).until(EC.presence_of_element_located((By.CLASS_NAME, 'DashboardHeader')))
        print("Login successful\n")
    except TimeoutException:
        QuitSession("Attempt failed: Login took too long\n")
except:
    print("Restored login session\n")

driver.get(target_url)
cookies = driver.get_cookies()
pickle.dump(cookies, open(cookies_file,"wb"))
if not len([cookie for cookie in cookies if 'CloudFront' in cookie['name']]):
    QuitSession("Attempt failed: No CloudFront key-pair cookies available")
    # Clue: https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver?rq=1

browser_log = driver.get_log('performance')
events = [json.loads(entry['message'])['message'] for entry in browser_log]
events = [event for event in events if 'Network.response' in event['method']]

m3u8_urls = []
for event in events:
    params = event['params']
    if 'response' in params:
        if '.m3u8' in params['response']['url']:
            m3u8_urls.append((params['response']['url']))
if not len(m3u8_urls):
    QuitSession("Attempt failed: No .m3u8 playlist files available")

# Format adheres to the following link: https://www.jokecamp.com/blog/passing-http-headers-to-ffmpeg/
formatted_cookies = r"$'{}\r\n'".format(r"\r\n".join([r"{}:{}".format(cookie['name'],cookie['value']) for cookie in cookies]))
target_m3u8_url = [m3u8 for m3u8 in m3u8_urls if video_resolution in m3u8][0]
# Refer to https://superuser.com/questions/692990/use-ffmpeg-copy-codec-to-combine-ts-files-into-a-single-mp4/693009
ffmpeg_command = '/dependencies/ffmpeg -headers {} -i "{}" -codec copy {}'.format(formatted_cookies, target_m3u8_url, output_file)
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(ffmpeg_process.stdout.readlines())

QuitSession("Attempt successfull!\n")