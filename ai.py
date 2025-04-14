import joblib
from time import sleep
import pandas as pd

class DiseasePredictor:
    def __init__(self):
        try:
            self.model = joblib.load('disease_predictor.joblib')
            self.feature_encoders = joblib.load('feature_encoders.joblib')
            self.label_encoder_y = joblib.load('label_encoder_y.joblib')
            print("All files loaded successfully!")
        except FileNotFoundError as e:
            print(f"Error: {e}. Please check the file paths.")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    
    def predict_disease(self, new_data):
        input_df = pd.DataFrame([new_data])
        
        for col, encoder in self.feature_encoders.items():
            if col in input_df.columns:
                input_df[col] = input_df[col].map(lambda x: x if x in encoder.classes_ else 'UNKNOWN')
                input_df[col] = encoder.transform(input_df[col])
        
        prediction = self.model.predict(input_df)
        
        # Simulate loading (optional - you might want to remove this in GUI)
        print("Loading eta: 3s")
        sleep(1)
        print("Loading eta: 2s")
        sleep(1)
        print("Loading eta: 1s")
        sleep(1)
        print("Done")

        return self.label_encoder_y.inverse_transform(prediction)[0]

# This part will only run if the script is executed directly (not when imported)
if __name__ == "__main__":
    predictor = DiseasePredictor()
    
    input_fever = input("Enter Fever (Yes/No): ")
    input_cough = input("Enter Cough (Yes/No): ")
    input_fatigue = input("Enter Fatigue (Yes/No): ")
    input_difficulty_breathing = input("Enter Difficulty Breathing (Yes/No): ")
    input_headache = input("Enter Headache (Yes/No): ")
    input_rash = input("Enter Rash (Yes/No): ")
    input_nausea = input("Enter Nausea (Yes/No): ")
    input_joint_pain = input("Enter Joint Pain (Yes/No): ")
    input_weight_change = input("Enter Weight Change (Yes/No): ")
    input_age = int(input("Enter Age: "))
    input_gender = input("Enter Gender (Male/Female): ")
    input_blood_pressure = input("Enter Blood Pressure (Low/Medium/High): ")
    input_cholesterol_level = input("Enter Cholesterol Level (Low/Medium/High): ")

    new_patient = {
        'Fever': input_fever,
        'Cough': input_cough,
        'Fatigue': input_fatigue,
        'Difficulty Breathing': input_difficulty_breathing,
        'Headache': input_headache,
        'Rash': input_rash,
        'Nausea': input_nausea,
        'Joint Pain': input_joint_pain,
        'Weight Change': input_weight_change,
        'Age': input_age,
        'Gender': input_gender,
        'Blood Pressure': input_blood_pressure,
        'Cholesterol Level': input_cholesterol_level
    }

    print(f"Symptoms and Data Collected: {new_patient}")
    print(f"Predicted Disease: {predictor.predict_disease(new_patient)}")
