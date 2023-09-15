import json

from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from pathlib import Path

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


CALC_URL = 'https://duffmanns.github.io/calc-test/calculator/app/index.html'

def getBrowserInstance():

    options = webdriver.ChromeOptions()

    options.add_argument('--ignore-certificate-errors')
    #options.add_argument("--incognito")
    #options.add_argument('--headless')
    options.add_argument("--start-maximized")

    driver =  webdriver.Chrome( service=Service(), options=options)

    return driver
    
def findOperator(ch):
    match ch:
        case "+":
            return "add"
        case "-":
            return "subtract"
        case "*":
            return "multiply"
        case "/":
            return "divide"
        case _:
            return "Unknown operator"

def calcIt(input_data_file):
    try:
        driver = getBrowserInstance()
        start_at_idx = 0

        #load equations from file
        with open(input_data_file) as data_file:    
            calc_data = json.load(data_file)
        data_file.close()    

        for index, calc in enumerate(calc_data[start_at_idx:]):
            driver.get(CALC_URL)
            equation = calc['equation']
            expectedResult = calc['result']

            print ('Equation #: ' + str(index+1))
            print('equation: ' + equation)
            print('expectedResult: ' + expectedResult)
            
            for ch in equation: #parse each char in the equation
                if (ch.isnumeric()):
                    element = driver.find_element(By.CSS_SELECTOR, "input[value='" + ch + "']")
                else:
                    operator = findOperator(ch)
                    element = driver.find_element(By.ID, operator)

                element.click()

                
            #equation is entered, now click equals to get the result
            driver.find_element(By.ID, "equals").click()

            #assert the result
            actualResult = driver.find_element(By.ID, "display")
            print("actualResult: " + actualResult.text)
            assert actualResult.text == expectedResult, "Fail: " + actualResult.text + " does not match expected result: " + expectedResult
          
        driver.close() #close the newly opened tab
        driver.quit()

    except Exception as e:
        print('calcIt: ' + repr(e))

calcIt('data/input_data.json')
