import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('final.csv')
    df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
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

    filtered_data = filtered_data.dropna(subset=['Closing Rank'])
    filtered_data = filtered_data.drop_duplicates(subset=['Year', 'Branch'])
    pivot_df = filtered_data.pivot(index='Year', columns='Branch', values='Closing Rank')

    plt.figure(figsize=(14, 10))

    for branch in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[branch], marker='o', linestyle='-', label=branch)

    plt.title(f'Closing Ranks for All Branches in {institute} ({seat_type}, {gender}, {quota}) (2016-2023)')
    plt.xlabel('Year')
    plt.ylabel('Closing Rank')
    plt.legend(title='Branch', bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title("GFTI's Closing Ranks Over the Years")

    institutes = [
        "Assam University, Silchar",
        "Birla Institute of Technology, Mesra,  Ranchi",
        "Gurukula Kangri Vishwavidyalaya, Haridwar",
        "Indian Institute of Carpet Technology,  Bhadohi",
        "Institute of Infrastructure, Technology, Research and Management-Ahmedabad",
        
        "J.K. Institute of Applied Physics & Technology, Department of Electronics & Communication, University of Allahabad- Allahabad",
        "National Institute of Electronics and Information Technology, Aurangabad (Maharashtra)",
        "National Institute of Advanced Manufacturing Technology, Ranchi",
        "Sant Longowal Institute of Engineering and Technology",
        "Mizoram University, Aizawl",
        "School of Engineering, Tezpur University, Napaam, Tezpur",
        "School of Planning & Architecture, Bhopal",
        "School of Planning & Architecture, New Delhi",
        "Shri Mata Vaishno Devi University, Katra, Jammu & Kashmir",
        "International Institute of Information Technology, Naya Raipur",
        "University of Hyderabad",
       
        "Jawaharlal Nehru University, Delhi",
        "International Institute of Information Technology, Bhubaneswar",
        "Central institute of Technology Kokrajar, Assam",
        "Puducherry Technological University, Puducherry",
        "Ghani Khan Choudhary Institute of Engineering and Technology, Malda, West Bengal",
        "Central University of Rajasthan, Rajasthan",
        "National Institute of Food Technology Entrepreneurship and Management, Kundli",
        "National Institute of Food Technology Entrepreneurship and Management, Thanjavur",
        "North Eastern Regional Institute of Science and Technology, Nirjuli-791109 (Itanagar),Arunachal Pradesh",
        "Indian Institute of Handloom Technology(IIHT), Varanasi",
        "Chhattisgarh Swami Vivekanada Technical University, Bhilai (CSVTU Bhilai)",
        "Institute of Chemical Technology, Mumbai: Indian Oil Odisha Campus, Bhubaneswar",
        "North-Eastern Hill University, Shillong",
          "Central University of Jammu",
            "Institute of Engineering and Technology, Dr. H. S. Gour University. Sagar (A Central University)",
              "Central University of Haryana",
                "Birla Institute of Technology, Deoghar Off-Campus",
                  "Birla Institute of Technology, Patna Off-Campus",
                    "Indian Institute of Handloom Technology, Salem",
                                              "CU Jharkhand",

        
        
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
