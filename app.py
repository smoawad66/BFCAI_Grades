import streamlit as st
from calculate_total import hier
from helpers import gpa_scale, get_image

st.set_page_config(
    page_title="Grades Slayer",
    page_icon="icon.jpeg"
)

st.markdown("""
    <style>
.appbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    max-height: 60px;
    background-color: rgba(0.0, 0.0, 0.0, 0.3);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 1rem 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

        input[type="number"] {
        direction: ltr !important;
        text-align: left !important;
    }

    div.stButton > button {
        width: 100%;
        background-color: #262730;
        color: #DDF;
        border: none;
        border-radius: 6px;
        padding: 0.75rem;
        font-size: 20px;
        font-weight: bold;
        box-shadow: none;
        transition: none;
    }

    div.stButton > button:hover {
        background-color: #262730;
        color: #DDF;
    }

    div.stButton > button:focus {
        outline: none;
        box-shadow: none;
    }

    div.stButton > button:active {
        color: #DDF; /* Blue when clicked */
        background-color: #262730;
    }
    * {
        direction: rtl;
    }
    body {
        background-color: white;
        margin: 4rem;
        padding: 4rem;
    }

    .main {
        margin: 4rem;
        corner-radius: 0px;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        font-family: 'Arial', monospace;
        color: white;
    }

    .block-container {
        margin: 4rem;
        corner-radius: 0px;
        width: 100%;
        height: 100%;
        max-width: 800px;
        padding: 2rem;
        background-color: transparent;
        border-radius: 15px;
    }

    h1 {
        text-align: center;
    }
    .logo-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .logo {
        width: 80px;
        height: auto;
    }
    h1 {
        text-align: center;
        color: #fff;
        font-size: 3em;
        margin-bottom: 1rem;
    }
    .metric {
        background: #eaf2fa;
        border-radius: 8px;
        padding: 0.7rem;
        margin-bottom: 0.5rem;
        text-align: right;
        direction: rtl;
    }
    footer {
        text-align: center;
        color: #fff;
        font-size: 0.9em;
        margin-top: 3rem;
    }
        .stMain {
            background-image: linear-gradient(to bottom, #1E5799, #5DA7E2);
        }

        /* Optional: override Streamlit padding/margin if needed */
        .st-emotion-cache-z4kicb.elbt1zu1 {
            background-image: linear-gradient(to bottom, #1E5799, #5DA7E2);
        }
    input[type="text"], input[type="number"], select {
        background-color: #262730 !important;
        color: white !important;
        direction: ltr !important;
        text-align: left !important;
        
    }
    p{
        padding-right: 5px;
        font-size: 30px;     
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="appbar">
    <h1 style="color: #1E5799; text-align: center; font-size: 2.2rem;"></h1>
</div>
""", unsafe_allow_html=True)


st.markdown("<h1>مطرشم الدرجات</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="logo-container">
        <img src="https://mis.bu.edu.eg/benha_new/userdocuments/3682/1375635155439119397364.jpg" class="logo">
        <img src="https://mis.bu.edu.eg/benha_new/Registration/EKP_logo.jpg" class="logo">
        <img src="https://mis.bu.edu.eg/benha_new/Images/DefaultImages/mislogo.png" class="logo">
    </div>
""", unsafe_allow_html=True)

student_id = st.text_input("الرقم القومي:", max_chars=14)

grade_mode = st.radio("تعرف ايه عن السلوك التنظيمي", ["التقدير", "الدرجة"])

if grade_mode == "الدرجة":
    grade_input = st.number_input("الدرجة:", min_value=50.0, max_value=100.0, step=0.5, format="%.1f")
else:
    grade_input = st.selectbox("التقدير:", list(gpa_scale.keys()))

st.markdown("---")
st.subheader("النتيجة")


if st.button("سبمت"):
    if len(student_id) == 14:
        with st.spinner("جاري الأشكلة..."):
            results = hier(student_id, grade_input) 
            if type(results) is tuple:
                num_courses, num_hours, cgpa, total_score, stud_name, img_src = results
                img = get_image(img_src)

                col_left, col_center, col_right = st.columns([1, 2, 1])
                with col_center:
                    st.image(img, width=250)
                    st.markdown(f"""
                        <div style="
                            background-color: #EAF2FA;
                            color: black;
                            text-align: center;
                            width: 250px;
                            padding-top: 10px;
                            padding-bottom: 10px;
                            font-size: 20px;
                            font-weight: bold;
                            border-radius: 6px;
                            margin-bottom: 15px;
                        ">
                            {stud_name}
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div style="color:black" class="metric"><strong>عدد المقررات: </strong> {num_courses}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:black" class="metric"><strong>عدد الساعات: </strong> {num_hours}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div style="color:black" class="metric"><strong>مجموع الدرجات: </strong> {total_score}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:black" class="metric"><strong>تراكمي النقاط: </strong> {cgpa:.10f}</div>', unsafe_allow_html=True)

            else:
                st.error('الرقم القومي غلط' if not results else 'موقع الكلية مقفول دلوقتي')
    elif not student_id:
        st.error('اكتب الرقم القومي')
    else:
        st.error('الرقم القومي لازم يكون 14 رقم')
else:
    st.markdown("")

st.markdown('''<p style="color: #EEE; margin-bottom: 50px; text-align: center;"> عبدالله حبسه + السيد معوض 2026 ©</p>''', unsafe_allow_html=True)