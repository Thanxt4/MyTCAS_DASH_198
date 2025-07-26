from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# สร้าง WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# คำค้นหาที่ต้องการ
search_terms = ['วิศวกรรมคอมพิวเตอร์', 'วิศวกรรมปัญญาประดิษฐ์',]

# เตรียม list สำหรับเก็บข้อมูล
data = []

# เปิดเว็บ
driver.get("https://course.mytcas.com/")

for term in search_terms:
    # รอช่องค้นหา
    search_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/input")))
    search_input.clear()

    # พิมพ์ทีละตัวแบบช้า ๆ
    for char in term:
        search_input.send_keys(char)
        time.sleep(0.1)

    search_input.send_keys(Keys.ENTER)
    time.sleep(2)

    try:
        # หาผลลัพธ์ใน div[2]/div[2]
        results_container = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[2]/div[2]")))
        links = results_container.find_elements(By.TAG_NAME, "a")
        urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        # เข้าไปในแต่ละลิงก์และดึงข้อมูล
        for url in urls:
            driver.get(url)

            try:
                # ดึงชื่อหลักสูตร
                title = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/main/div[2]/div/span/span/a")
                )).text

                # ดึงชื่อมหาวิทยาลัยหรือสถาบัน
                institute = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/main/div[2]/ul/li[1]/dl/dd[5]")
                )).text

                # เก็บข้อมูล
                data.append({
                    "สถาบัน": title,
                    "ชื่อหลักสูตร": term,
                    "ค่าใช้จ่าย": institute,
                    "ลิงก์": url
                })

            except Exception as e:
                print(f"❌ ไม่สามารถดึงข้อมูลจาก {url}: {e}")

            time.sleep(1)

    except Exception as e:
        print(f"❌ ไม่พบผลลัพธ์สำหรับคำว่า '{term}': {e}")

    # กลับไปหน้าแรกเพื่อค้นหาคำถัดไป
    driver.get("https://course.mytcas.com/")
    time.sleep(2)

# ปิด WebDriver
driver.quit()

# แปลงเป็น DataFrame และบันทึกเป็น CSV
df = pd.DataFrame(data)
df.to_csv("mytcas_courses.csv", index=False, encoding='utf-8-sig')

print("\n✅ บันทึกข้อมูลลงไฟล์ 'mytcas_courses.csv' เรียบร้อยแล้ว!")
