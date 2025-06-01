import streamlit as st
import pandas as pd
import pickle
import os

APPLICATION_MODES = [
    {"label": "1st phase - general contingent", "value": 1},
    {"label": "Ordinance No. 612/93", "value": 2},
    {"label": "1st phase - special contingent (Azores Island)", "value": 5},
    {"label": "Holders of other higher courses", "value": 7},
    {"label": "Ordinance No. 854-B/99", "value": 10},
    {"label": "International student (bachelor)", "value": 15},
    {"label": "1st phase - special contingent (Madeira Island)", "value": 16},
    {"label": "2nd phase - general contingent", "value": 17},
    {"label": "3rd phase - general contingent", "value": 18},
    {"label": "Ordinance No. 533-A/99 (Different Plan)", "value": 26},
    {"label": "Ordinance No. 533-A/99 (Other Institution)", "value": 27},
    {"label": "Over 23 years old", "value": 39},
    {"label": "Transfer", "value": 42},
    {"label": "Change of course", "value": 43},
    {"label": "Technological specialization diploma holders", "value": 44},
    {"label": "Change of institution/course", "value": 51},
    {"label": "Short cycle diploma holders", "value": 53},
    {"label": "Change of institution/course (International)", "value": 57},
]

COURSES = [
    {"label": "Biofuel Production Technologies", "value": 33},
    {"label": "Animation and Multimedia Design", "value": 171},
    {"label": "Social Service (Evening)", "value": 8014},
    {"label": "Agronomy", "value": 9003},
    {"label": "Communication Design", "value": 9070},
    {"label": "Veterinary Nursing", "value": 9085},
    {"label": "Informatics Engineering", "value": 9119},
    {"label": "Equinculture", "value": 9130},
    {"label": "Management", "value": 9147},
    {"label": "Social Service", "value": 9238},
    {"label": "Tourism", "value": 9254},
    {"label": "Nursing", "value": 9500},
    {"label": "Oral Hygiene", "value": 9556},
    {"label": "Advertising & Marketing Management", "value": 9670},
    {"label": "Journalism and Communication", "value": 9773},
    {"label": "Basic Education", "value": 9853},
    {"label": "Management (Evening)", "value": 9991},
]

# Load model
@st.cache_resource
def load_model():
    model_path = 'model/model.pkl'
    if not os.path.exists(model_path):
        st.error("Model file not found!")
        return None
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def predict_dropout(model, input_data):
    df_input = pd.DataFrame([input_data])
    prediction = model.predict(df_input)
    return prediction[0]

# Mapping untuk dropdown label → angka
gender_map = {"Female": 0, "Male": 1}
yesno_map = {"No": 0, "Yes": 1}

def main():
    st.title("🎓 Student Dropout Prediction")
    st.markdown("Masukkan data mahasiswa untuk memprediksi kemungkinan dropout atau lulus.")

    st.header("📝 Input Data Mahasiswa")

    selected_app_mode = st.selectbox("Jalur Masuk", options=APPLICATION_MODES, format_func=lambda x: x["label"])
    application_mode = selected_app_mode["value"]
    selected_course = st.selectbox("Program Studi", options=COURSES, format_func=lambda x: x["label"])
    course = selected_course["value"]
    prev_grade = st.number_input('📚 Nilai Pendidikan Sebelumnya (0-200)', min_value=0.0, max_value=200.0, value=142.0)
    mother_edu = st.selectbox("🎓 Pendidikan Ibu", [1, 2, 3])
    father_edu = st.selectbox("🎓 Pendidikan Ayah", [3, 4, 5])
    mother_job = st.selectbox("👩‍💼 Pekerjaan Ibu", [1, 2, 3])
    father_job = st.selectbox("👨‍💼 Pekerjaan Ayah", [1, 2, 3])
    admission_grade = st.number_input('📝 Nilai Masuk (0-200)', min_value=0.0, max_value=200.0, value=142.5)
    displaced = st.selectbox('🚨 Pengungsi / Pindahan?', options=list(yesno_map.keys()))
    gender = st.selectbox('👤 Jenis Kelamin', options=list(gender_map.keys()))
    scholarship = st.selectbox('🎓 Penerima Beasiswa?', options=list(yesno_map.keys()))
    age = st.number_input('📅 Usia Saat Masuk Kuliah (min 10)', min_value=10, max_value=100, value=19)

    units1_enrolled = st.number_input('📘 Jumlah Mata Kuliah 1st Sem (Diambil)', min_value=0, max_value=50, value=6)
    units1_eval = st.number_input('📗 Jumlah Mata Kuliah 1st Sem (Dievaluasi)', min_value=0, max_value=50, value=6)
    units1_approved = st.number_input('✅ Jumlah Mata Kuliah 1st Sem (Lulus)', min_value=0, max_value=50, value=6)
    grade1 = st.number_input('1st Sem Grade (0-20)', min_value=0.0, max_value=20.0, value=12.0)

    units2_enrolled = st.number_input('📘 Jumlah Mata Kuliah 2nd Sem (Diambil)', min_value=0, max_value=50, value=6)
    units2_eval = st.number_input('📗 Jumlah Mata Kuliah 2nd Sem (Dievaluasi)', min_value=0, max_value=50, value=6)
    units2_approved = st.number_input('✅ Jumlah Mata Kuliah 2nd Sem (Lulus)', min_value=0, max_value=50, value=6)
    grade2 = st.number_input('2nd Sem Grade (0-20)', min_value=0.0, max_value=20.0, value=12.0)

    unemployment = st.number_input('📉 Tingkat Pengangguran (%)', min_value=0.0, max_value=100.0, value=13.9)
    inflation = st.number_input('💸 Tingkat Inflasi (%)', min_value=-50.0, max_value=50.0, value=-0.3)
    gdp = st.number_input('📊 Pertumbuhan GDP (%)', min_value=-50.0, max_value=50.0, value=0.79)

    ratio1 = st.number_input('📈 Rasio Kelulusan 1st Sem (0-1)', min_value=0.0, max_value=1.0, value=1.0)
    ratio2 = st.number_input('📈 Rasio Kelulusan 2nd Sem (0-1)', min_value=0.0, max_value=1.0, value=1.0)

    if st.button("🔍 Predict Dropout"):
        model = load_model()
        if model is None:
            st.stop()

        # Mapping label → nilai numerik

        input_features = {
            'Application_mode': application_mode,
            'Course': course,
            'Previous_qualification_grade': prev_grade,
            'Mothers_qualification': mother_edu,
            'Fathers_qualification': father_edu,
            'Mothers_occupation': mother_job,
            'Fathers_occupation': father_job,
            'Admission_grade': admission_grade,
            'Displaced': yesno_map[displaced],
            'Gender': gender_map[gender],
            'Scholarship_holder': yesno_map[scholarship],
            'Age_at_enrollment': age,
            'Curricular_units_1st_sem_enrolled': units1_enrolled,
            'Curricular_units_1st_sem_evaluations': units1_eval,
            'Curricular_units_1st_sem_approved': units1_approved,
            'Curricular_units_1st_sem_grade': grade1,
            'Curricular_units_2nd_sem_enrolled': units2_enrolled,
            'Curricular_units_2nd_sem_evaluations': units2_eval,
            'Curricular_units_2nd_sem_approved': units2_approved,
            'Curricular_units_2nd_sem_grade': grade2,

            'Unemployment_rate': unemployment,
            'Inflation_rate': inflation,
            'GDP': gdp,
            'Ratio_approved_1st_sem': ratio1,
            'Ratio_approved_2nd_sem': ratio2
        }
        result = predict_dropout(model, input_features)

        if result == 1:
            st.success("✅ Prediksi: Mahasiswa kemungkinan **LULUS**.")
        else:
            st.warning("⚠️ Prediksi: Mahasiswa kemungkinan **DROPOUT**.")

if __name__ == "__main__":
    main()
