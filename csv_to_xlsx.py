import pandas as pd
import re

# อ่านไฟล์ CSV
df = pd.read_csv('mytcas_courses(1).csv', encoding='utf-8-sig')

def fee_per_term_numeric(fee):
    """
    คืนค่าเป็นตัวเลข (int) ต่อเทอม ถ้าเป็น 'ตลอดหลักสูตร' จะหาร 8
    ถ้าไม่ใช่ตัวเลขหรือไม่มีข้อมูล จะคืนค่า None
    """
    if not isinstance(fee, str):
        return None
    # กรณี "ตลอดหลักสูตร"
    if "ตลอดหลักสูตร" in fee:
        match = re.search(r"([\d,]+)", fee)
        if match:
            try:
                num = int(match.group(1).replace(",", ""))
                per_term = int(num / 8)
                return per_term
            except Exception:
                return None
        return None
    # กรณีต่อเทอม/ต่อภาคการศึกษา
    match = re.search(r"([\d,]+)", fee)
    if match:
        try:
            return int(match.group(1).replace(",", ""))
        except Exception:
            return None
    return None

if "ค่าใช้จ่าย" in df.columns:
    df["ค่าใช้จ่ายต่อเทอม (บาท)"] = df["ค่าใช้จ่าย"].apply(fee_per_term_numeric)
    # ลบแถวที่ไม่สามารถแปลงเป็นตัวเลขได้ (NaN)
    df = df.dropna(subset=["ค่าใช้จ่ายต่อเทอม (บาท)"])
else:
    print("ไม่พบคอลัมน์ 'ค่าใช้จ่าย' ในไฟล์ CSV")

# ส่งออกเป็นไฟล์ Excel
df.to_excel('mytcas_courses_per_term.xlsx', index=False)