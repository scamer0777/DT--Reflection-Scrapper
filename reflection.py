from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
   
    driver.get('https://web.whatsapp.com')

    print("Please scan the QR code to log in. Waiting for 200 seconds...")
    time.sleep(100) 
    messages = []
    name_number_pairs = []

    
    message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-in, div.message-out")

    for message in message_elements:
        number = "Unknown"
        name = "Unknown"
        timestamp = "Unknown"
        message_text = "No message text"

       
        try:
            number = message.find_element(By.CSS_SELECTOR, "span.ahx").text
        except:

            pass

        try:
            name = message.find_element(By.CSS_SELECTOR, "._ahxy.x1iyjqo2.x6ikm8r.x10wlt62.x1n2onr6.xlyipyv").text
        except:
            try:
                name = message.find_element(By.CSS_SELECTOR, "._ahxt.x1ypdohk.xt0b8zv._ao3e").text
            except:
                pass

        try:
            timestamp = message.find_element(By.CSS_SELECTOR, ".x1rg5ohu").text
        except:
            pass

        try:
            message_text = message.find_element(By.CSS_SELECTOR, "._ao3e > span").text
        except:
            pass

       
        if "reflection" in message_text.lower():
            messages.append({"participant": name, "message": message_text, "timestamp": timestamp, "number": number})

           
            if name != "Unknown" or number != "Unknown":
                name_number_pairs.append({"name": name, "number": number})

  
    df_messages = pd.DataFrame(messages)
    df_messages.to_csv('whatsapp_filtered_messages.csv', index=False)

    df_name_number = pd.DataFrame(name_number_pairs)
    df_name_number.to_csv('whatsapp_filtered_names_numbers.csv', index=False)

    print("Filtered messages have been saved to 'whatsapp_filtered_messages.csv'")
    print("Filtered names and numbers have been saved to 'whatsapp_filtered_names_numbers.csv'")

finally:
    driver.quit()
