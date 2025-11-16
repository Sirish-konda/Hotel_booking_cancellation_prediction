# Hotel_booking_cancellation_prediction
End-to-end ML project predicting hotel booking cancellations with Streamlit deployment, featuring data cleaning, model tuning, and F1-based performance evaluation.
## 📘 Overview
This project predicts whether a hotel booking will be canceled using **machine learning**.  
Cancellations impact hotel revenue, staffing, and resource planning.  
By analyzing key factors such as **lead time**, **deposit type**, **customer type**, and **special requests**, this model provides data-driven insights to help hotels reduce losses and improve operations.

The trained model is deployed through an interactive **Streamlit web app**, where users can enter booking details and instantly receive a cancellation prediction with probability.

---

## 🚀 Features
- Complete **data preprocessing** and cleaning  
- **Feature engineering** and selection for optimal performance  
- Multiple models compared using **F1-score**, **Precision**, **Recall**, and **ROC-AUC**  
- Focus on **F1-score** to balance class imbalance  
- **Streamlit app deployment** for real-time predictions  
- Interpretable results with key feature importance analysis  

---

## 🧠 Tech Stack
- Python 🐍  
- Pandas, NumPy, Scikit-learn  
- Matplotlib, Seaborn  
- Streamlit  
- Joblib  

---

## 📊 Model Evaluation
The **Random Forest** model achieved the best balance of accuracy and generalization:  
- **Accuracy:** ~84%  
- **F1-score:** ~0.79  
- **ROC-AUC:** ~0.91  

These results indicate strong predictive power and reliability in identifying potential cancellations.

---

## 💻 Streamlit App
Users can access the model through a simple web interface built with Streamlit.  
The app allows users to:
1. Input booking details (lead time, deposit type, guests, etc.)  
2. View the **predicted probability of cancellation**  
3. See whether the booking is **Likely to Show** or **Likely Cancelled**.  
