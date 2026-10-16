# #6. WEB APP QUAN LY DIEM SINH VIEN

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="📚",
    layout="wide"
)

# Tao tieu de
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.caption("Ứng dụng quản lý và tra cứu điểm sinh viên")

# Tao du lieu
data = {
    "Ho_ten": [
        "Nguyen Van An",
        "Tran Thi Binh",
        "Le Van Cuong",
        "Pham Thi Dung",
        "Hoang Van Em",
        "Vu Thi Giang",
        "Do Van Hung",
        "Bui Thi Lan",
        "Dang Van Minh",
        "Ngo Thi Nhung"
    ],
    "Chuyen_can": [9, 8, 10, 7, 6, 9, 5, 8, 7, 10],
    "Giua_ky": [8, 7, 9, 6, 5, 8, 4, 7, 6, 9],
    "Cuoi_ky": [9, 8, 8, 7, 4, 9, 5, 6, 7, 10]
}

df = pd.DataFrame(data)

# Tinh diem tong ket
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# Xep loai
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Thong ke
diem_tb = df["Tong_ket"].mean()
sv_cao = df.loc[df["Tong_ket"].idxmax()]
sv_thap = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = int((df["Tong_ket"] >= 5).sum())

# Hien thi bang diem
st.subheader("1. Bảng điểm sinh viên")

bang = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang,
    use_container_width=True,
    hide_index=True
)

# Hien thi thong ke
st.subheader("2. Thống kê")

c1, c2, c3 = st.columns(3)

c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")
c3.metric("Tổng sinh viên", len(df))

st.write(
    f"**Điểm cao nhất:** {sv_cao['Ho_ten']} "
    f"({sv_cao['Tong_ket']:.2f})"
)

st.write(
    f"**Điểm thấp nhất:** {sv_thap['Ho_ten']} "
    f"({sv_thap['Tong_ket']:.2f})"
)

# Tra cuu sinh vien
st.subheader("3. Tra cứu sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df.loc[df["Ho_ten"] == ten_sv].iloc[0]

st.write(f"**Họ tên:** {sv['Ho_ten']}")

a, b, c, d = st.columns(4)

a.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
b.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
c.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
d.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")

st.info(f"Xếp loại: {sv['Xep_loai']}")

# Ve bieu do
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 5))

colors = [
    "#2E86DE" if diem >= 5 else "#E74C3C"
    for diem in df["Tong_ket"]
]

ax.bar(df["Ho_ten"], df["Tong_ket"], color=colors)
ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Thong tin nguoi tao
st.divider()
st.caption("ten: [GiaBảo] | MSSV: [04]")
