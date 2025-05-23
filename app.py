import gradio as gr
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# Prediction function
def predict_loan_approval(ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,
                          Gender, Married, Dependents, Education, Self_Employed, Property_Area):

    # Manual one-hot encoding
    dependents_map = {
        "0": [1, 0, 0, 0],
        "1": [0, 1, 0, 0],
        "2": [0, 0, 1, 0],
        "3+": [0, 0, 0, 1],
    }

    property_area_map = {
        "Rural": [1, 0, 0],
        "Semiurban": [0, 1, 0],
        "Urban": [0, 0, 1],
    }

    # Binary encoding
    Gender = 1.0 if Gender == "Male" else 0.0
    Married = 1.0 if Married == "Yes" else 0.0
    Education = 1.0 if Education == "Graduate" else 0.0
    Self_Employed = 1.0 if Self_Employed == "Yes" else 0.0

    # Combine all features
    features = [
        ApplicantIncome,
        CoapplicantIncome,
        LoanAmount,
        Loan_Amount_Term,
        Credit_History,
        Gender,
        Married,
        *dependents_map[Dependents],
        Education,
        Self_Employed,
        *property_area_map[Property_Area]
    ]

    prediction = model.predict([features])[0]
    return "✅ Approved" if prediction == 1 else "❌ Rejected"

# Create Gradio interface
demo = gr.Interface(
    fn=predict_loan_approval,
    inputs=[
        gr.Number(label="Applicant Income"),
        gr.Number(label="Coapplicant Income"),
        gr.Number(label="Loan Amount"),
        gr.Number(label="Loan Amount Term"),
        gr.Radio([1.0, 0.0], label="Credit History (1 = Good, 0 = Bad)"),
        gr.Radio(["Male", "Female"], label="Gender"),
        gr.Radio(["Yes", "No"], label="Married"),
        gr.Radio(["0", "1", "2", "3+"], label="Dependents"),
        gr.Radio(["Graduate", "Not Graduate"], label="Education"),
        gr.Radio(["Yes", "No"], label="Self Employed"),
        gr.Radio(["Rural", "Semiurban", "Urban"], label="Property Area"),
    ],
    outputs=gr.Text(label="Loan Status"),
    title="Loan Eligibility Predictor",
    description="Enter applicant details to check loan approval status."
)

# Launch the app
if __name__ == "__main__":
    demo.launch()
