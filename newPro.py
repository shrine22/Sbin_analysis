import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns  # For heatmap
import numpy as np  # For gradient color computation

# Apply custom CSS for black background and white text
st.markdown(
    """
    <style>
    /* Set the app background to dark */
    .stApp {
        background-color: #1E1E2F; /* Dark purple-gray */
        color: #EAEAEA; /* Light gray for text */
    }
    /* Main container styling */
    .block-container {
        font-family: Arial, sans-serif;
        background-color: #2A2A3D; /* Slightly lighter dark gray for contrast */
        padding: 2rem;
        border-radius: 10px; /* Smooth corners for better design */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Subtle shadow */
    }
    /* Hyperlinks */
    a {
        color: #1DB954; /* Vibrant green for links */
        text-decoration: none;
    }
    a:hover {
        color: #0D7377; /* Teal for hover effect */
        text-decoration: underline;
    }
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF; /* Bright white for headings */
    }
    /* Tables and dataframes */
    .dataframe {
        background-color: #1E1E2F; /* Match background */
        color: #EAEAEA; /* Light gray text */
    }
    /* Warnings and messages */
    .stAlert {
        background-color: #3A3A4F; /* Muted gray-blue for alerts */
        color: #FFD700; /* Golden text for warnings */
        border-left: 5px solid #E74C3C; /* Red accent for importance */
    }
    /* Buttons */
    .stButton > button {
        background-color: #1DB954; /* Vibrant green for buttons */
        color: #FFFFFF; /* White text */
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #0D7377; /* Teal hover effect */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the data
df = pd.read_csv("SBIN_New_Data.csv")  # Ensure the CSV is in the same directory or provide the full path

# Ensure the 'Date' column is a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar for user input
st.sidebar.title("SBIN Stock Analysis")
year = st.sidebar.slider("Select Year", 2000, 2024, 2024)  # Adjust the range as needed
selected_insight = st.sidebar.selectbox(
    "Select Insight",
    [
        "Daily Price Range",
        "Stock Performance Trend",
        "Volume Over Time",
        "Top N Days by Closing Price",
        "Correlation Between High, Low, and Volume",
    ],
)

st.title("Real-Time SBIN Stock Data Insights")

# Filter data by year
df['Year'] = df['Date'].dt.year
filtered_df = df[df['Year'] == year]

if filtered_df.empty:
    st.warning("No data available for the selected year.")
else:
    # Real-time graph options
    if selected_insight == "Daily Price Range":
        st.subheader("Daily Price Range (High - Low)")
        filtered_df['Daily Price Range'] = filtered_df['High'] - filtered_df['Low']
        fig = px.line(
            filtered_df,
            x='Date',
            y='Daily Price Range',
            title='Daily Price Range Over Time',
            labels={'Daily Price Range': 'Price Range', 'Date': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Conclusion")
        st.write(
            "Days with higher price ranges indicate higher volatility, which could signify trading opportunities or market uncertainty. "
            "This information is valuable for day traders who rely on volatility to make quick profits. However, prolonged high volatility may also suggest market instability, warranting caution."
        )

    elif selected_insight == "Stock Performance Trend":
        st.subheader("Stock Performance Trend (Closing Price)")
        fig = px.line(
            filtered_df,
            x='Date',
            y='Close',
            title='Stock Performance Trend (Closing Price)',
            labels={'Close': 'Closing Price', 'Date': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Conclusion")
        st.write(
            "The trend of closing prices provides insights into the overall market sentiment and stock performance during the selected year. "
            "A consistent uptrend could signal investor confidence, while frequent fluctuations may indicate uncertain market conditions."
        )

    elif selected_insight == "Volume Over Time":
        st.subheader("Trading Volume Over Time")
        fig = px.bar(
            filtered_df,
            x='Date',
            y='Volume',
            title='Trading Volume Over Time',
            labels={'Volume': 'Volume', 'Date': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Conclusion")
        st.write(
            "Spikes in trading volume often coincide with significant market events, such as announcements or news related to the stock. "
            "High volume suggests increased investor interest, which can lead to either rapid price appreciation or depreciation depending on the sentiment."
        )

    elif selected_insight == "Top N Days by Closing Price":
        st.subheader(f"Top 5 Days by Closing Price in {year}")
        top_days = filtered_df.nlargest(5, 'Close')
        st.dataframe(top_days[['Date', 'Close']])

        # Plot using Matplotlib with a gradient of blue shades
        colors = plt.cm.Purples(np.linspace(0.5, 1, len(top_days)))  # Purple gradient
        plt.figure(figsize=(10, 6))
        plt.bar(top_days['Date'].dt.strftime('%Y-%m-%d'), top_days['Close'], color=colors)
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title("Top 5 Closing Prices")
        st.pyplot(plt)

        st.markdown("### Conclusion")
        st.write(
            "The top-performing days indicate peak market performance, which may be linked to positive news or market sentiment. "
            "Such days highlight periods of high investor confidence and can serve as reference points for future technical analysis or trend identification."
        )

    elif selected_insight == "Correlation Between High, Low, and Volume":
        st.subheader("Correlation Between High, Low, and Volume")
        if not filtered_df.empty:
            correlation_matrix = filtered_df[['High', 'Low', 'Volume']].corr()
            st.write("Correlation Matrix:")
            st.dataframe(correlation_matrix)

            # Plotting correlation heatmap using seaborn
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title("Correlation Heatmap")
            st.pyplot(plt)

            st.markdown("### Conclusion")
            st.write(
                "Strong correlations indicate the interdependence between price and volume metrics, helping investors understand market behavior. "
                "For example, a high correlation between volume and price changes could suggest that significant trading activity influences market movements. "
            )
        else:
            st.warning("No data available for the selected year.")
