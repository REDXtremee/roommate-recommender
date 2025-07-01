🏠 Hostel Roommate Recommender System
This project recommends compatible hostel roommates using clustering and similarity techniques based on user preferences and personality traits collected through a survey. It aims to help students make more informed decisions while choosing or switching roommates.

💡 Overview
The goal was to build a system that recommends suitable hostel partners by analyzing inputs like:

SGPA (academic compatibility)

Social preference

Cleanliness priority

Study habits

Sleep schedule

Visitor frequency

Gender and year

Using K-Means Clustering for grouping similar students and Cosine Similarity to measure pairwise compatibility within clusters, the system suggests the best possible roommate matches.

📊 Data Collection
Data was collected via a Google Form circulated among hostel residents. The form included multiple-choice questions that were later converted into numerical ratings (1-5 scale) for computation. Normalization was applied twice:
While converting qualitative data into ratings.

During preprocessing to standardize feature values.

[https://forms.gle/UDmAntCyGUAdn11u8]

⚙️ Features Used
SGPA (given the highest weight)

Social Preference

Cleanliness

Study Habits

Sleeping Preference

Visitor Frequency

Gender

🔍 Techniques Applied
🧠 K-Means Clustering for grouping similar individuals.

📐 Cosine Similarity for matching within clusters.

📊 Data Normalization for scale standardization.

📈 Matplotlib / Seaborn for visualizing clusters.

🌐 Streamlit for building an interactive web app.

🚀 Live Demo
You can try out the system and view recommendations based on the current dataset here:

🔗 [https://roommate-recommender.streamlit.app]
