from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os, sys, tempfile, time, requests, json, shutil

def _create_driver(directory):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox') # Allow root to run
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument("--allow-file-access-from-files") 
    chrome_options.add_argument("--disabled-web-security")
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": ".",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    # chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('--disable-software-rasterizer')

    # initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
    driver = webdriver.Chrome(options=chrome_options)        

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': directory}}
    driver.execute("send_command", params)
    return driver
    
        
def renderSBGN(url, output_filename):
        
    with tempfile.TemporaryDirectory() as directory:
    #  self.directory = tempfile.mkdtemp()
        driver = _create_driver(directory)
            
        # get request to target the site selenium is active on
        full_url = "file://%s/index.html?url=%s&bg=#fff" % (os.path.dirname(os.path.dirname(__file__)), url)
        print("Rendering : %s" % full_url)
        driver.get(full_url)
        
        wait = WebDriverWait(driver, 60*60*2) # Two hours max should be more than enough
        
        class js_variable_evals_to_true(object):
            def __init__(self, variable):
                self.variable = variable
            def __call__(self, driver):
                res = driver.execute_script("return {0};".format(self.variable))
                return res

        wait.until(js_variable_evals_to_true("document.sbgnReady || document.sbgnNotFound || document.sbgnError"))
        
        if driver.execute_script(" return document.sbgnReady") is True:
            
            while not os.path.exists(os.path.join(directory, "truc.png")):
                time.sleep(1)

            shutil.move(os.path.join(directory, "truc.png"), output_filename)
        
        else: 
            if driver.execute_script(" return document.sbgnNotFound") is True:
                print("Failed, SBGN not found")

            elif driver.execute_script(" return document.sbgnError") is True:
                print("Failed, something went wrong")

            else:
                print("Failed, and I can't say why")

    
    
