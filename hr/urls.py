from django.urls import path, include
from .views import *
from hr.api import api
from rest_framework import routers


app_name = "hr"


urlpatterns = [
    path('api/',api.urls),
    path("attendance", attendanceView, name='attendanceView'),
    
    path("leaveApplication",leaveApplication,name='leaveApplication'),
    path("Leave/leaveHistory",leaveHistory,name='leaveHistory'),
    path("Leave/leaveEdit",leaveEdit,name='leaveEdit'),
    
    path("bankdetails",bankApplication,name='bankApplication'),
    path("BankDetails/bankdetailshistory",bankHistory,name='bankHistory'),
    path("BankDetails/bankdetailsupdate",bankEdit,name='bankEdit'),
    
    path("labour",labour,name='labour'),
    path("LabourContract/labourContracthistory",labourContracthistory,name="labourContracthistory"),
    path("LabourContract/labourContractupdate",labourContractupdate,name="labourContractupdate"),
    
    path("profile", profile, name='profile'),
    path("Profile/edit_profile", editProfile, name='editProfile'),
    path("Profile/changePassword", changePassword, name='changePassword'),
    
    path("visitngCard", visitngCard, name='visitngCard'),
    path("Visiting/visitngCardHistory", visitngCardHistory, name='visitngCardHistory'),
    path("Visiting/visitingCardEdit", visitingCardEdit, name='visitingCardEdit'),
    
    path("EmployeeId", EmployeeId, name='EmployeeId'),

    path("documentforlabourcard",documentforlabourcard,name="documentforlabourcard"),
    path("LabourCardDocument/documentforlabourcardhistory",documentforlabourcardhistory,name="documentforlabourcardhistory"),
    path("LabourCardDocument/documentforlabourcardupdate",documentforlabourcardupdate,name="documentforlabourcardupdate"),
    
    
    path("EmployeeResumption",EmpResumption,name="EmpResumption"),
    path("EmpResumption/EmployeeResumptionHistory",EmpResumptionhistory,name="EmpResumptionhistory"),
    path("EmpResumption/EmployeeResumptionUpdate",EmpResumptionupdate,name="documentforlabourcardupdate"),
    
    
    
    path("EmployeeReimbursement",EmpReimbursement,name="EmpReimbursement"),
    path("EmpReimbursement/ReimbursementHistory",EmpReimbursementhistory,name="EmpReimbursementhistory"),
    path("EmpReimbursement/ReimbursementUpdte",EmpReimbursementupdate,name="EmpReimbursementupdate"),
    
    path("BusinessTrip",BusinessTrip,name='BusinessTrip'),
    path("BusinesstripApplication/BusinessTripHistory",business_trip_history,name='business_trip_history'),
    path("BusinesstripApplication/BusinessTripEdit",business_trip_edit,name='business_trip_edit'),
    
    path("documentforVisa",DocumentVisa,name="DocumentVisa"),
    path("DocumentVisa/documentforvisahistory",documentforvisahistory,name="documentforvisahistory"),
    path("DocumentVisa/documentforvisacardupdate",documentforvisacardupdate,name="documentforvisacardupdate"),
    
    
    path("medicalreimbursement",MedicalReimbursement,name="MedicalReimbursement"),
    path("MedicalReimbursement/medicalreimbursementhistory",medicalreimbursementhistory,name="medicalreimbursementhistory"),
    path("MedicalReimbursement/medicalreimbursementupdate",medicalreimbursementupdate,name="medicalreimbursementupdate"),
    
    
    path("EmployeeTravel",EmployeeTravel,name='EmployeeTravel'),
    path("EmployeeTravel/EmployeeTravelHistory",EmployeeTravelHistory,name='EmployeeTravelHistory'),
    path("EmployeeTravel/EmployeeTravelEdit",EmployeeTravelEdit,name='EmployeeTravelEdit'),
    
    path("EmpException",EmpException,name="EmpException"),
    path("EmployeeException/EmpExceptionHistory",EmpExceptionHistory,name="EmpExceptionHistory"),
    path("EmployeeException/EmpExceptionUpdate",EmpExceptionUpdate,name="EmpExceptionUpdate"),
    
    
    path("documentforpassport", documentforpassport, name='documentforpassport'),
    path("documentforpassport/documentforpassporthistory", documentforpassporthistory, name='documentforpassporthistory'),
    path("documentforpassport/documentforpassportupdate", documentforpassportupdate, name='documentforpassportupdate'),
    
]
