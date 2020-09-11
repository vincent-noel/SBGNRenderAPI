from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os, sys, tempfile, time, requests, json, shutil


class RendererClient:
    
    def __init__(self, server="localhost", port=8081):
        
        self.server = server
        self.port = port
        self.driver = None
        self.directory = tempfile.mkdtemp()
        
        self._create_driver()
        if not self.check_status():
            self.close()
            raise ConnectionError("The rendering server %s:%d could not be reached" % (self.server, self.port))
            
        
    def _create_driver(self):
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
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
        self.driver = webdriver.Chrome(options=chrome_options)        

        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.directory}}
        self.driver.execute("send_command", params)

    def check_status(self):
        try:
            res = requests.get("http://%s:%d/status" % (self.server, self.port)).json()
            return res['status']

        except requests.exceptions.ConnectionError as e:
            return False
            
    def render(self, url, output_filename):
                
        # get request to target the site selenium is active on
        print("Rendering : http://%s:%d/?url=%s" % (self.server, self.port, url))
        self.driver.get("http://%s:%d/?url=%s" % (self.server, self.port, url))
        
        wait = WebDriverWait(self.driver, 60*60*2) # Two hours max should be more than enough
        
        class js_variable_evals_to_true(object):
            def __init__(self, variable):
                self.variable = variable
            def __call__(self, driver):
                res = driver.execute_script("return {0};".format(self.variable))
                return res
        print("Started waiting...")
        wait.until(js_variable_evals_to_true("document.sbgnReady || document.sbgnInvalid || document.sbgnNotFound || document.sbgnError"))
        
        print("Returned from wait")
        
        if self.driver.execute_script(" return document.sbgnReady") is True:
            
            while not os.path.exists(os.path.join(self.directory, "truc.png")):
                print("Downloading...")
                time.sleep(1)

            shutil.move(os.path.join(self.directory, "truc.png"), output_filename)
        
        else: 
            if self.driver.execute_script(" return document.sbgnInvalid") is True:
                print("Failed, invalid SBGN")
            elif self.driver.execute_script(" return document.sbgnNotFound") is True:
                print("Failed, SBGN not found")
            elif self.driver.execute_script(" return document.sbgnError") is True:
                print("Failed, something went wrong")
            else:
                print("Failed, and I can't say why")
        
    def close(self):
        
        os.rmdir(self.directory) 
        
        
        
 