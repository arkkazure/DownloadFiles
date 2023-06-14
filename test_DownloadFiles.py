# test_google.py
import csv
import pytest
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_test_data_from_csv():
    test_data = []
    with open('./InputData/Idata1.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)  # skip header row
        for row in data:
            test_data.append(row)
    return test_data

@pytest.mark.parametrize("TestID, URL, Resource", read_test_data_from_csv())
def test_download_files(TestID, URL, Resource):
 # Set the download directory path
    download_directory = 'D:\\POCs\\DownloadFiles\\OutPutFiles\\' +TestID
    #download_directory = os.path.join(download_directory_base, Test_ID) 
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
    })

    chrome_options.add_argument('--headless')
    # Create the WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)
   
    #driver = webdriver.Chrome(options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)

    driver.get(URL)
    #time.sleep(5)
    wait = WebDriverWait(driver, 10)
    linkw = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '.xml')]")))
    links = driver.find_elements(By.XPATH, "//a[contains(text(), '.xml')]")
    for link in links:
        link_text = link.text
        print (f"link text: {link_text}")
        link.click()
        #time.sleep(2)
        wait_for_file(link_text, download_directory , 30 )

   
    print (TestID)
    # Close the browser
    driver.quit()






def wait_for_file(file_name, directory_path, timeout=120):
    start_time = time.time()
    file_path = os.path.join(directory_path, file_name)
    tmp_file_pattern = re.compile(r'.*\.tmp$')
    unconfirmed_file_pattern = re.compile(r'Unconfirm.*')

    while not os.path.isfile(file_path) or any(tmp_file_pattern.match(f) for f in os.listdir(directory_path)) or any(unconfirmed_file_pattern.match(f) for f in os.listdir(directory_path)):
        if time.time() - start_time >= timeout:
            print(f"Timeout reached. File '{file_name}' not found or .tmp file still present.")
            return False
        time.sleep(1)  # Wait for 1 second before checking again

    print(f"File '{file_name}' found in directory: {directory_path}")
    return True