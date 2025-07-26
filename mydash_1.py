import pandas as pd
import dash
from dash import dcc, html, dash_table
import plotly.express as px

# โหลดข้อมูล
df = pd.read_excel("mytcas_courses_per_term.xlsx")

# สร้างคอลัมน์ตัวเลขจาก "ค่าใช้จ่ายต่อเทอม (บาท)"
df["ค่าใช้จ่าย (num)"] = pd.to_numeric(
    df["ค่าใช้จ่ายต่อเทอม (บาท)"].replace(r"[^\d]", "", regex=True),
    errors="coerce"
)

# แปลงเป็นข้อความสำหรับตาราง เช่น "25,000 บาท"
df["ค่าใช้จ่าย (ข้อความ)"] = df["ค่าใช้จ่าย (num)"].apply(
    lambda x: f"{int(x):,} บาท" if pd.notna(x) else "ไม่ระบุ"
)

# กราฟแท่ง: ค่าใช้จ่ายเฉลี่ยต่อเทอม แยกตามสถาบัน
bar_fig = px.bar(
    df.groupby("สถาบัน", as_index=False)["ค่าใช้จ่าย (num)"].mean().dropna(),
    x="สถาบัน",
    y="ค่าใช้จ่าย (num)",
    title="ค่าใช้จ่ายเฉลี่ยต่อเทอม (แยกตามสถาบัน)",
    labels={"ค่าใช้จ่าย (num)": "ค่าใช้จ่ายเฉลี่ย (บาท)"},
    color="สถาบัน",
    text_auto=".2s"
)

# ปรับขนาดกราฟให้ใหญ่ขึ้น
bar_fig.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="#fff",
    title_font_size=28,        # ขนาดชื่อกราฟใหญ่ขึ้น
    font=dict(size=8),        # ขนาดตัวหนังสือในกราฟ
    height=700,                # ความสูงของกราฟ
    width=1200,                # ความกว้างของกราฟ
    margin=dict(l=80, r=80, t=80, b=120)
)

# สร้าง Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("📊 Dashboard หลักสูตร TCAS", style={"textAlign": "center"}),

    dcc.Graph(figure=bar_fig),

    html.H3("📄 ข้อมูลหลักสูตร", style={"textAlign": "left"}),

    dash_table.DataTable(
        data=df[["สถาบัน", "ชื่อหลักสูตร", "ค่าใช้จ่าย", "ลิงก์", "ค่าใช้จ่าย (ข้อความ)"]]
            .rename(columns={"ค่าใช้จ่าย (ข้อความ)": "ค่าใช้จ่ายต่อเทอม (บาท)"})
            .to_dict("records"),
        columns=[
            {"name": col, "id": col}
            for col in ["สถาบัน", "ชื่อหลักสูตร", "ค่าใช้จ่าย", "ลิงก์", "ค่าใช้จ่ายต่อเทอม (บาท)"]
        ],
        style_cell={
            "textAlign": "left",
            "fontFamily": "Tahoma",
            "whiteSpace": "normal",
            "height": "auto",
            "padding": "8px"
        },
        style_header={
            "backgroundColor": "#f0f0f0",
            "fontWeight": "bold"
        },
        style_table={"overflowX": "auto"},
        page_size=15,
    )
])

if __name__ == '__main__':
    app.run(debug=True)
