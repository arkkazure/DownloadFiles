# test_google.py
import csv
import pytest
import time
import os
import re
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Global Vars
download_base_directory = 'D:\\POCs\\DownloadFiles\\OutPutFiles\\'
input_dataFile = '../InputData/IData1.csv'



def read_test_data_from_csv():
    test_data = []
    with open(input_dataFile, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)  # skip header row
        for row in data:
            test_data.append(row)
    return test_data



@pytest.mark.parametrize("TestID, URL, Resource", read_test_data_from_csv())
def test_download_files(TestID, URL, Resource):
 # Set the download directory path
    
    download_directory = download_base_directory + TestID
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

    #chrome_options.add_argument('--headless')
    # Create the WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)
   
    #driver = webdriver.Chrome(options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)

    driver.get(URL)
    
    #wait = WebDriverWait(driver, 10)
    #linkw = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '.txt')]")))
    #time.sleep(2)
    links = driver.find_elements(By.XPATH, "//a[contains(text(), '.txt')]")
    log_info=""
    if len(links) == 0:
        log_info = log_info+TestID+","+get_time_stamp()+",No Attachments Found"
    else:
        
        for link in links:
            link_text = link.text
            print (f"Test ID : {TestID}  -- Link text: {link_text}")
            log_info
            link.click()
            #time.sleep(2)
            if wait_for_file(link_text, download_directory , 30 ):
                log_info = log_info+ TestID+","+get_time_stamp()+",Sucessful Download,"+link_text+"\n"
            else:
                log_info = log_info+ TestID+","+get_time_stamp()+",Failed to Download,"+link_text+"\n"   
   
    #print (TestID)
    # Close the browser
    driver.quit()
    write_to_file("..\\Logs\\"+TestID+".txt", log_info)


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


def write_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def get_time_stamp():
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp_str



@pytest.fixture(scope="session", autouse=True)
def combine_logs(request):
    yield
    print("Combined Logs:")
    get_combined_txt_content("../Logs", "Log.csv")
    

def get_combined_txt_content(folder_path, output_file):
    combined_content = ""

    # Get a list of all .txt files in the folder
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    # Iterate over each .txt file
    for file_path in txt_files:
        with open(file_path, "r") as file:
            content = file.read()
            combined_content += content + "\n"  # Concatenate the content of each file

    # Remove blank lines
    combined_content = "\n".join(line for line in combined_content.split("\n") if line.strip())

    # Construct the output file's full path
    output_path = os.path.join(folder_path, output_file)

    # Write the combined content to the output file
    with open(output_path, "w") as file:
        file.write(combined_content)