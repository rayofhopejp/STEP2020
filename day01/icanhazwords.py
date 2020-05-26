#treat QU as Q
point_list=[1,1,2,1,1,2,1,2,1,3,3,2,2,1,1,2,3,1,1,1,1,2,2,3,2,3]

def count_characters(words):
    dic={}
    for word in words:
        cnt=[0]*26
        for c in word:
            cnt[ord(c)-ord('a')]+=1
            if c=='q':
                cnt[ord('u')-ord('a')]-=1
        dic[word]=cnt
    return dic

def main(words,letters,char_count_dict):
    char_count=[letters.count(chr(ord('a')+i)) for i in range(26)]
    max_point=0
    max_word=""
    for k,v in char_count_dict.items():
        point=1
        for i in range(26):
            if v[i]>char_count[i]:
                break
            if v[i]>0:
                point+=v[i]*point_list[i]
            if i==26-1:
                if point**2>max_point:
                    max_point=point**2
                    max_word=k
    return max_point,max_word

from selenium import webdriver
from time import sleep
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_letters(driver):
    letters=[]
    WebDriverWait(driver,50).until(EC.presence_of_element_located((By.XPATH, "//div[@class='letter p1']")))
    driver.implicitly_wait(0.1)
    for i in range(1,4):
        elems = driver.find_elements_by_xpath("//div[@class='letter p"+str(i)+"']")
        for elem in elems:
            if elem.text.lower()=="qu":
                letters.append('q')
            else:
                letters.append(elem.text.lower())
    return letters

def submit_answer(driver,answer):
    WebDriverWait(driver,50).until(EC.presence_of_element_located((By.XPATH, "//input[@id='MoveField']")))
    if answer=="":
        print('PASS')
        driver.find_element_by_xpath("//input[@value='PASS']").click()
    else:
        driver.find_element_by_xpath("//input[@id='MoveField']").send_keys(answer)
        driver.find_element_by_xpath("//input[@value='Submit']").click()

def submit_score(driver):
    WebDriverWait(driver,50).until(EC.presence_of_element_located((By.XPATH, "//input[@name='NickName']")))
    driver.find_element_by_xpath("//input[@name='NickName']").send_keys("-")
    driver.find_element_by_xpath("//input[@id='AgentRobot']").click()
    driver.find_element_by_xpath("//input[@name='Name']").send_keys("-")
    driver.find_element_by_xpath("//input[@name='Email']").send_keys("-")
    #Githubs
    driver.find_element_by_xpath("//input[@name='URL']").send_keys("-")
    driver.find_element_by_xpath("//input[@type='submit']").click()

if __name__ == '__main__':
    #make dictionary
    path="./dictionary.words"
    f=open(path)
    words=[line.strip().lower() for line in f.readlines()]
    char_count_dict=count_characters(words)

    URL="https://icanhazwordz.appspot.com/"
    driver_path="./chromedriver"
    driver=webdriver.Chrome(driver_path)
    
    #recore highschore at highscore.txt
    hsf=open("highscore.txt","r")
    total_score=0
    goal_score=int(hsf.read().strip())
    print("goal score is",goal_score)
    hsf.close()

    while 1:
        driver.get(URL)
        total_score=0
        for i in range(10):
            letters=get_letters(driver)
            score,word=main(words,letters,char_count_dict)
            print(word,score,total_score) 
            total_score += score
            submit_answer(driver,word)
            dt_now = datetime.datetime.now()
        print("total score is",total_score,dt_now)
        if total_score>goal_score:
            submit_score(driver)
            hsf=open("highscore.txt","w")
            hsf.write(str(total_score))
            hsf.close()
            goal_score=total_score
            print("RECORDED!")
            
      
    f.close()
    driver.close()
    driver.quit()

    
