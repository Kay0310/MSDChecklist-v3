
import streamlit as st
import pandas as pd
import datetime
import io
from pathlib import Path

st.set_page_config(page_title="근골격계 부담작업 체크리스트", layout="wide")
st.title("📋 근골격계 부담작업 체크리스트 시스템")

# 기본 정보 입력
st.subheader("✅ 기본 정보 입력")
company = st.text_input("회사명")
department = st.text_input("부서명")
work_name = st.text_input("작업명")
unit_work = st.text_input("단위작업명")
writer = st.text_input("작성자")
write_date = st.date_input("작성일자", value=datetime.date.today())
weight = st.text_input("총중량 (Kg)")

# 항목 체크
items = {
    1: "하루 4시간 이상 키보드 또는 마우스를 조작하는 작업",
    2: "2시간 이상 같은 동작을 반복하는 작업",
    3: "팔을 어깨 위로 드는 작업 등",
    4: "목이나 허리를 구부리거나 비트는 작업",
    5: "쪼그리거나 무릎을 굽힌 자세의 작업",
    6: "손가락으로 1kg 이상을 집는 작업",
    7: "한 손으로 4.5kg 이상 드는 작업",
    8: "25kg 이상 물체를 하루 10회 이상 드는 작업",
    9: "10kg 이상 물체를 무릎 아래, 어깨 위 등에서 드는 작업",
    10: "4.5kg 이상 물체를 분당 2회 이상 드는 작업",
    11: "손 또는 무릎으로 반복 충격을 가하는 작업",
    12: "기타 신체에 부담을 주는 작업"
}

responses = []
st.subheader("🧩 부담작업 항목 체크")
for i in range(1, 13):
    st.markdown(f"### {i}호. {items[i]}")
    applicable = st.radio(f"{i}호 해당 여부", ["예", "아니오"], key=f"item_{i}")
    count = st.number_input(f"{i}호 해당 인원 수", min_value=0, step=1, key=f"count_{i}")
    memo1 = st.text_input(f"{i}호 메모 1", key=f"memo1_{i}")
    memo2 = st.text_input(f"{i}호 메모 2", key=f"memo2_{i}")
    responses.append({
        "항목": f"{i}호",
        "해당": applicable,
        "인원": count,
        "메모1": memo1,
        "메모2": memo2
    })

# 작업내용 서술
st.subheader("📝 작업내용 서술")
row_count = st.number_input("행 개수 선택", min_value=1, max_value=10, value=1)
task_descriptions = []
for i in range(row_count):
    text = st.text_area(f"작업내용 {i+1}", key=f"task_{i}")
    task_descriptions.append(text)

# 임시 저장
st.subheader("💾 임시 저장")
if st.button("📥 .xlsx 파일로 임시 저장"):
    df = pd.DataFrame(responses)
    desc_df = pd.DataFrame({"작업내용": task_descriptions})
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="부담작업 체크")
        desc_df.to_excel(writer, index=False, sheet_name="작업내용")
    st.download_button(
        label="📂 temp_작성자명_날짜.xlsx 다운로드",
        data=buffer.getvalue(),
        file_name=f"temp_{writer}_{write_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.info("※ Google Sheets에 저장하려면 Google 계정(Drive 권한)이 필요합니다. 인증 후 사용 가능합니다.")
