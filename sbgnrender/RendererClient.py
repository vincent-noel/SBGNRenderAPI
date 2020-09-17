from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import os, sys, tempfile, time, json, shutil

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
            "download.default_directory": directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }
    
    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=d)        

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': directory}}
    driver.execute("send_command", params)
    return driver
    
def _print_console(logs):
    for log in logs:
        print(" ".join(log['message'].split(" ")[2:]))
        
def renderSBGN(url, output_filename, format=None, scale=None, bg=None, max_width=None, max_height=None, quality=None, layout=None, verbose=False):
        
    with tempfile.TemporaryDirectory() as directory:
    #  self.directory = tempfile.mkdtemp()
        driver = _create_driver(directory)
            
        # get request to target the site selenium is active on
        full_url = "file://%s/index.html?url=%s%s%s%s%s%s%s%s" % (
            os.path.dirname(__file__), 
            os.path.join(os.getcwd(), url),
            ("&format=%s" % format) if format is not None else "",
            ("&scale=%s" % scale) if scale is not None else "",
            ("&bg=%s" % bg) if bg is not None else "",
            ("&max_width=%s" % max_width) if max_width is not None else "",
            ("&max_height=%s" % max_height) if max_height is not None else "",
            ("&quality=%s" % quality) if quality is not None else "",
            ("&layout=%s" % layout) if layout is not None else ""
        )
        
        if verbose:
            print("Rendering : %s" % full_url)    
        
        driver.get(full_url)
        
        if verbose:
            _print_console(driver.get_log('browser'))

        wait = WebDriverWait(driver, 60*60*2) # Two hours max should be more than enough
        
        class js_variable_evals_to_true(object):
            def __init__(self, variable):
                self.variable = variable
            def __call__(self, driver):
                try:
                    res = driver.execute_script("return {0};".format(self.variable))
                except Exception as e:
                    print("Driver timeout : %s" % res)
                    return False
                            
                if verbose:
                    print("Driver returned : %s" % res)
                    _print_console(driver.get_log('browser'))
                    
                return res

        wait.until(js_variable_evals_to_true("document.sbgnReady || document.sbgnNotFound || document.sbgnError"))
        
        if verbose:
            _print_console(driver.get_log('browser'))

        if driver.execute_script(" return document.sbgnReady") is True:
            
            # Here we have a problem getting the file on ubuntu where chromedriver is installed via snap
            # In that case, /tmp is remaped to /tmp/snap.chromium/, and I'm not sure how to get the true location. 
            # So I'm trying both
            network_filename = "network.%s" % (format if format is not None else "png")
            while (
                not os.path.exists(os.path.join(directory, network_filename)) 
                and not os.path.exists(os.path.join("/tmp/snap.chromium/tmp", os.path.basename(directory), network_filename))
            ):
                if verbose:
                    print("Downloading ...")
                time.sleep(1)
         
            if os.path.exists(os.path.join(directory, network_filename)):
                shutil.move(os.path.join(directory, network_filename), output_filename)
            elif os.path.exists(os.path.join("/tmp/snap.chromium/tmp", os.path.basename(directory), network_filename)):
                shutil.move(os.path.join("/tmp/snap.chromium/tmp", os.path.basename(directory), network_filename), output_filename)
        else: 
            if driver.execute_script(" return document.sbgnNotFound") is True:
                print("Failed, SBGN not found")

            elif driver.execute_script(" return document.sbgnError") is True:
                print("Failed, something went wrong")

            else:
                print("Failed, and I can't say why")

    
    
