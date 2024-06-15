import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('final.csv')
    df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
    return df

def filter_and_plot(institute, seat_type, gender, quota):
    df = load_data()
    filtered_df = df[(df['Institue'].str.strip() == institute) &
                     (df['Gender'] == gender) &
                     (df['Seat Type'] == seat_type) & 
                     (df['Quota'] == quota)]

    last_rounds = {
        2016: 6,
        2017: 7,
        2018: 7,
        2019: 6,
        2020: 6,
        2021: 6,
        2022: 6,
        2023: 6
    }

    filtered_data = pd.concat([
        filtered_df[(filtered_df['Year'] == year) & (filtered_df['Round'] == last_round)]
        for year, last_round in last_rounds.items()
    ])

    filtered_data = filtered_data.dropna(subset=['Opening Rank'])
    filtered_data = filtered_data.drop_duplicates(subset=['Year', 'Branch'])
    pivot_df = filtered_data.pivot(index='Year', columns='Branch', values='Opening Rank')

    plt.figure(figsize=(14, 10))

    for branch in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[branch], marker='o', linestyle='-', label=branch)

    plt.title(f'Opening Ranks for All Branches in {institute} ({seat_type}, {gender}, {quota}) (2016-2023)')
    plt.xlabel('Year')
    plt.ylabel('Opening Rank')
    plt.legend(title='Branch', bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title("IIIT Opening Ranks Over the Years")

    institutes = [
     
"Atal Bihari Vajpayee Indian Institute of Information Technology & Management Gwalior",
"Indian Institute of Information Technology (IIIT)Kota, Rajasthan",
"Indian Institute of Information Technology Guwahati",
"Indian Institute of Information Technology(IIIT) Kalyani, West Bengal",
"Indian Institute of Information Technology(IIIT) Kilohrad, Sonepat, Haryana",
"Indian Institute of Information Technology(IIIT) Una, Himachal Pradesh",
"Indian Institute of Information Technology (IIIT), Sri City, Chittoor",
"Indian Institute of Information Technology(IIIT), Vadodara, Gujrat",
"Indian Institute of Information Technology, Allahabad",
"Indian Institute of Information Technology, Design & Manufacturing, Kancheepuram",
"Pt. Dwarka Prasad Mishra Indian Institute of Information Technology, Design & Manufacture Jabalpur",
"Indian Institute of Information Technology  Manipur",
"Indian Institute of Information Technology Tiruchirappalli",
"Indian Institute of Information Technology Lucknow",
"Indian Institute of Information Technology(IIIT) Dharwad",
"Indian Institute of Information Technology Design & Manufacturing Kurnool, Andhra Pradesh",
"Indian Institute of Information Technology(IIIT) Kottayam",
"Indian Institute of Information Technology (IIIT) Ranchi",
"Indian Institute of Information Technology (IIIT) Nagpur",
"Indian Institute of Information Technology (IIIT) Pune",
"Indian Institute of Information Technology Bhagalpur",
"Indian Institute of Information Technology Bhopal",
"Indian Institute of Information Technology Surat",
"Indian Institute of Information Technology, Agartala",
"Indian Institute of Information Technology, Vadodara International Campus Diu (IIITVICD)",
"Indian Institute of Information Technology(IIIT), Sri City, Chittoor District, Andra Pradesh",
"Indian Institute of Information Technology Srirangam, Tiruchirappalli",
"Indian Institute of Information Technology(IIIT), Sri City, Chittoor District, Andhra Pradesh"
    ]
    seat_types = ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'EWS (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)']
    genders = ['Gender-Neutral', 'Female-only (including Supernumerary)']
    quotas = ['AI', 'HS', 'OS']

    institute = st.selectbox("Select Institute:", institutes)
    seat_type = st.selectbox("Select Seat Type:", seat_types)
    gender = st.selectbox("Select Gender:", genders)
    quota = st.selectbox("Select Quota:", quotas)

    if st.button("Submit"):
        filter_and_plot(institute, seat_type, gender, quota)

if __name__ == "__main__":
    main()