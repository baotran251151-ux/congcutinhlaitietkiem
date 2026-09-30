import streamlit as st
st.image("logo.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("Ngân hàng trung ương_kho bạc nhà nước")
st.write("Tính toán theo phương pháp lãi đơn và lãi kép")


# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return "{:,.0f} VNĐ".format(value)


# ==============================
# NHẬP DỮ LIỆU
# ==============================

st.sidebar.header("Thông tin gửi tiết kiệm")

tien_gui = st.sidebar.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0,
    value=100000000,
    step=1000000
)

ky_han = st.sidebar.number_input(
    "Kỳ hạn gửi (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.sidebar.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1
)


loai_lai = st.sidebar.selectbox(
    "Chọn phương thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)


hinh_thuc_nhan = st.sidebar.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# ==============================
# TÍNH TOÁN
# ==============================

if st.button("🧮 Tính toán"):

    # đổi lãi suất năm sang số thập phân
    r = lai_suat / 100

    # số năm gửi
    so_nam = ky_han / 12


    # ------------------------------
    # LÃI ĐƠN
    # ------------------------------
    if loai_lai == "Lãi đơn":

        tong_tien_lai = tien_gui * r * so_nam

        tong_tien = tien_gui + tong_tien_lai


    # ------------------------------
    # LÃI KÉP
    # ------------------------------
    else:

        # nhập lãi theo tháng
        lai_thang = r / 12

        tong_tien = tien_gui * ((1 + lai_thang) ** ky_han)

        tong_tien_lai = tong_tien - tien_gui



    # ==============================
    # TÍNH LÃI ĐỊNH KỲ
    # ==============================

    if hinh_thuc_nhan == "Lãnh lãi hàng tháng":

        so_ky = ky_han

        lai_dinh_ky = tong_tien_lai / so_ky


    elif hinh_thuc_nhan == "Lãnh lãi hàng quý":

        so_ky = ky_han / 3

        lai_dinh_ky = tong_tien_lai / so_ky


    else:

        lai_dinh_ky = tong_tien_lai



    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================

    st.subheader("📊 Kết quả tính toán")


    col1, col2 = st.columns(2)


    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

        st.metric(
            "Tổng tiền lãi",
            format_money(tong_tien_lai)
        )


    with col2:

        st.metric(
            "Tiền gốc ban đầu",
            format_money(tien_gui)
        )

        st.metric(
            "Tổng gốc + lãi",
            format_money(tong_tien)
        )


    # bảng thông tin
    st.divider()

    st.write("### 📌 Thông tin khoản gửi")

    thong_tin = {
        "Số tiền gửi": format_money(tien_gui),
        "Kỳ hạn": f"{ky_han} tháng",
        "Lãi suất": f"{lai_suat}%/năm",
        "Phương thức tính": loai_lai,
        "Hình thức nhận lãi": hinh_thuc_nhan
    }

    for key, value in thong_tin.items():
        st.write(f"**{key}:** {value}")



# ==============================
# CÔNG THỨC
# ==============================

with st.expander("📚 Xem công thức"):

    st.write("""
    **1. Lãi đơn**

    Lãi = Tiền gửi × Lãi suất năm × Số năm gửi


    **2. Lãi kép**

    Tổng tiền = Tiền gửi × (1 + lãi suất tháng)^số tháng


    Trong đó:

    - Lãi suất tháng = Lãi suất năm / 12
    - Tổng tiền lãi = Tổng tiền nhận được - Tiền gốc
    """)
