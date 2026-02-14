# 🎙️ Voice-Based Form Autofill

A **Streamlit web app** that allows users to **fill forms using their voice**. Speak naturally, and the app transcribes your speech using **OpenAI Whisper**, extracts relevant information, and populates the form fields automatically. Users can review, edit, and re-record individual fields before submission.

---

## **Features**

- Record your details once, and the app populates the form automatically.
- Extracts common form fields:
  - First Name
  - Last Name
  - Email
  - Phone Number (supports spoken digits like "double two")
  - PAN Number
  - Address
- Highlights fields that need review.
- Allows re-recording of individual fields.
- Shows extraction confidence per field.
- Export submissions with timestamp in JSON format.

---

## **Demo**

- Hosted on Streamlit Community Cloud:  
  [https://<your-username>.streamlitapp.com](https://<your-username>.streamlitapp.com)

---

## **Installation & Setup**

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/voice-form-app.git
cd voice-form-app
```
2. **Create virtual enviornment**
```bash
 python -m venv <enviornment_name>
 source <enviornment_name>/bin/activate        # macOS / Linux
 <enviornment_name>\Scripts\activate           # Windows
```
3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Run app locally**
``` bash
streamlit run app.py
```
5. **Usage**
 - Click 🎙 Record your details and speak naturally.
 - The form fields will populate automatically after transcription.
 - Review each field — re-record if necessary.
 - Submit the form to see a JSON output of your submission.


