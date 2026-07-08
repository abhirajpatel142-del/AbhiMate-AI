zimport os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "abhimate-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/abhimate.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

