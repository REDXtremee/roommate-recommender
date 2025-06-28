import streamlit as st
import pandas as pd
import pickle

def roommate(num):
    target = df[df['gender']=='Male']

    target = target.reset_index(drop=True)

    value = 0.5
    stu_index = target[target['scho_num'] == num].index[0]

    new_df = target[
        (target['sgpa'] >= target.loc[stu_index, 'sgpa'] - value) &
        (target['sgpa'] <= target.loc[stu_index, 'sgpa'] + value)
        ]
    new_df = new_df.reset_index(drop=True)

    stu_index = new_df[new_df['scho_num'] == num].index[0]

    x = new_df.iloc[:, 4:]

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler().set_output(transform='pandas')
    x = scaler.fit_transform(x)

    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(x)

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=5, random_state=42)
    x['cluster'] = kmeans.fit_predict(x)

    cluster = x.iloc[stu_index]['cluster']
    cluster_mates = x[x['cluster'] == cluster].index.tolist()
    cluster_mates.remove(stu_index)
    in_cluster_matches = sorted(
        cluster_mates,
        key=lambda x: similarity[stu_index][x],
        reverse=True
    )[:10]

    if len(in_cluster_matches) < 10:
        remaining = 10 - len(in_cluster_matches)
        all_students = list(range(len(new_df)))
        non_cluster = [x for x in all_students if x not in cluster_mates + [stu_index]]
        global_matches = sorted(
            non_cluster,
            key=lambda x: similarity[stu_index][x],
            reverse=True
        )[:remaining]
        in_cluster_matches.extend(global_matches)

    return in_cluster_matches,new_df,similarity,stu_index

def view(matches,df,similarity,stu_index):
    # for i, idx in enumerate(matches, start=1):
    #     # Get student info
    #     if idx in df.index:  # ensure the index exists
    #         student = df.loc[idx]
    #         name = student['name']
    #         scholar = student['scho_num']
    #         branch = student['branch']
    #         similarity_score = similarity[stu_index][idx]
    #
    #         # Display with a card-like block
    #         with st.container():
    #             st.markdown(f"### 🔹 Recommendation {i}")
    #             st.write(f"**Name:** {name}")
    #             st.write(f"**Scholar Number:** {scholar}")
    #             st.write(f"**Branch:** {branch}")
    #             st.write(f"**Similarity Score:** {similarity_score * 100:.2f}%")
    #             st.markdown("---")

    for i, idx in enumerate(matches, start=1):
        if idx in df.index:
            student = df.loc[idx]
            name = student['name']
            scholar = student['scho_num']
            branch = student['branch']
            score = similarity[stu_index][idx] * 100

            with st.expander(f"🔹 Match #{i}: {name} ({branch})", expanded=(i <= 3)):
                col1, col2 = st.columns([1.5, 2])
                with col1:
                    st.write(f"**👤 Name:** {name}")
                    st.write(f"**🎓 Scholar No.:** {scholar}")
                    st.write(f"**🧭 Branch:** {branch}")
                with col2:
                    st.metric(label="💯 Similarity Score", value=f"{score:.2f} %")
                st.markdown("---")

st.set_page_config(
    page_title="Clustered & Compatible",
    # page_icon="🤝",
    # layout="wide"
)
st.title('Clustered & Compatible: Your AI Roommate Guide')
df = pickle.load(open("df_dict.pkl",'rb'))
df = pd.DataFrame(df)
df = df[df['gender']=="Male"]
option = st.selectbox(
    'Enter Your Scholar Number',
    df['scho_num'].values
)

if st.button('Recommend'):
    #
    matches, df, similarity, stu_index = roommate(option)
    view(matches,df,similarity,stu_index)
    st.markdown(
        """
        ---
        🔍 **Disclaimer:**  
        These recommendations are based solely on the input provided by individuals.  
        They **do not reflect any official roommate or hostel allotment**.  
        This tool is only meant to help students explore compatible roommate options with similar preferences and habits.
        """
    )