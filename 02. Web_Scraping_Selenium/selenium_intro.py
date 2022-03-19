# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys

# os.environ['PATH'] += r"C:/Users/sangh/Desktop/Drivers/ChromeDriver"
# driver = webdriver.Chrome()

# ###########################################################################

# # driver.get('https://www.seleniumeasy.com/test/jquery-download-progress-bar-demo.html')
# # driver.implicitly_wait(3) #time.sleep(3)
# # my_element = driver.find_element_by_id('downloadButton')

# # my_element.click()

# # implicity wait applies here
# # my_second_element = driver.find_element_by_id('ierwi')

# # progress_element = driver.find_element_by_class_name('progress-label')
# # print(f"{progress_element.text == 'Completed'}")

# # WebDriverWait(driver, 30).until(
# #     EC.text_to_be_present_in_element(
# #         (By.CLASS_NAME, 'progress-label'),
# #          "Complete!"
# #     )
# # )

# ###########################################################################
# driver.get('https://www.seleniumeasy.com/test/basic-first-form-demo.html')
# driver.implicitly_wait(3)

# try:
#     no_button = driver.find_element_by_class_name('at-cm-no-button')
#     no_button.click()
# except:
#     pass
# sum1 = driver.find_element_by_id('sum1')
# sum2 = driver.find_element_by_id('sum2')

# sum1.send_keys(Keys.NUMPAD1, Keys.NUMPAD5)
# sum2.send_keys(15)

# btn = driver.find_element_by_css_selector("button[onclick="return total()"]")
# btn.click()