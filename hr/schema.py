# from ninja import Schema

from ninja import Schema

class UserSchema(Schema):
    
    username:str
    email:str
    password:str
    





from ninja import Schema

class EmailOTPSchema(Schema):
    subject: str
    recipients: str
    message: str

class OTPValidationSchema(Schema):
    username: str
    otp: str
