# Sleep productivity tracker

A simple Streamlit web app to track and visualize your daily sleep hours and productivity levels. The app uses Firebase as a cloud backend to store and retrieve user data securely. It provides personalized suggestions and visual insights to help users reflect on their habits and improve daily performance.

## 🛠 How to Run the Project

1. **Clone the Repository**
   Open a terminal and run:

   ```bash
   git clone https://github.com/your-username/sleep-productivity-tracker.git
   cd sleep-productivity-tracker
   ```

2. **Install Required Libraries**
   Make sure Python is installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Firebase**

   * Go to [Firebase Console](https://console.firebase.google.com/)
   * Create a project → Realtime Database → Get your Firebase config
   * Paste your Firebase config in the `firebaseConfig = { ... }` part inside `tracker.py`

4. **Run the Streamlit App**
   Run this command in terminal:

   ```bash
   streamlit run tracker.py
   ```

5. **Start Using the App**

   * Enter your sleep hours and productivity score
   * View graphs, averages, and suggestions on the dashboard
