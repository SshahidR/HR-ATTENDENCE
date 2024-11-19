from django.shortcuts import render

# Create your views here.
def attendanceView(request):
    return render(request, "hr/attendance.html")

def leaveApplication(request):
    return render(request, "hr/Leave/leaveApplication.html")

def leaveHistory(request):
    return render(request, "hr/Leave/leaveHistory.html")

def leaveEdit(request):
    return render(request, "hr/Leave/leaveEdit.html")

def bankApplication(request):
    return render(request, "hr/BankDetails/bankdetails.html")

def bankHistory(request):
    return render(request, "hr/BankDetails/bankdetailshistory.html")

def bankEdit(request):
    return render(request, "hr/BankDetails/bankdetailsupdate.html")


def labour(request):
    return render(request, "hr/LabourContract/labour.html")

def labourContracthistory(request):
    return render(request,"hr/LabourContract/labourContracthistory.html")

def labourContractupdate(request):
    return render (request,"hr/LabourContract/labourContractupdate.html")



def visitngCard(request):
    return render(request, "hr/Visiting/visitngCard.html")


def visitngCardHistory(request):
    return render(request, "hr/Visiting/visitngCardHistory.html")

def visitingCardEdit(request):
    return render(request, "hr/Visiting/visitingCardEdit.html")


def EmployeeId(request):
    return render(request, "hr/EmpId/EmployeeId.html")

def documentforlabourcard(request):
    return render(request,"hr/LabourCardDocument/documentforlabourcard.html")

def documentforlabourcardhistory(request):
    return render(request,"hr/LabourCardDocument/documentforlabourcardhistory.html")

def documentforlabourcardupdate(request):
    return render(request,"hr/LabourCardDocument/documentforlabourcardupdate.html")



def EmpResumption(request):
    return render(request,"hr/EmpResumption/EmployeeResumption.html")

def EmpResumptionhistory(request):
    return render(request,"hr/EmpResumption/EmployeeResumptionHistory.html")

def EmpResumptionupdate(request):
    return render(request,"hr/EmpResumption/EmployeeResumptionUpdate.html")


def EmpReimbursement(request):
    return render(request,"hr/EmpReimbursement/EmployeeReimbursement.html")

def EmpReimbursementhistory(request):
    return render(request,"hr/EmpReimbursement/ReimbursementHistory.html")

def EmpReimbursementupdate(request):
    return render(request,"hr/EmpReimbursement/ReimbursementUpdte.html")

def BusinessTrip(request):
    return render(request, "hr/BusinesstripApplication/BusinessTrip.html")

def business_trip_history(request):
    return render(request, "hr/BusinesstripApplication/BusinessTripHistory.html")

def business_trip_edit(request):
    return render(request, "hr/BusinesstripApplication/BusinessTripEdit.html")

def DocumentVisa(request):
    return render(request,"hr/DocumentVisa/documentforVisa.html")

def documentforvisahistory(request):
    return render(request,"hr/DocumentVisa/documentforvisahistory.html")

def documentforvisacardupdate(request):
    return render(request,"hr/DocumentVisa/documentforvisacardupdate.html")


def MedicalReimbursement(request):
    return render(request,"hr/MedicalReimbursement/medicalreimbursement.html")

def medicalreimbursementhistory(request):
    return render(request,"hr/MedicalReimbursement/medicalreimbursementhistory.html")

def medicalreimbursementupdate(request):
    return render(request,"hr/MedicalReimbursement/medicalreimbursementupdate.html")




def EmployeeTravel(request):
    return render(request, "hr/EmployeeTravel/EmployeeTravel.html")

def EmployeeTravelHistory(request):
    return render(request, "hr/EmployeeTravel/EmployeeTravelHistory.html")

def EmployeeTravelEdit(request):
    return render(request, "hr/EmployeeTravel/EmployeeTravelEdit.html")


def EmpException(request):
    return render(request,"hr/EmployeeException/EmpException.html")
def EmpExceptionHistory(request):
    return render(request,"hr/EmployeeException/EmpExceptionHistory.html")
def EmpExceptionUpdate(request):
    return render(request,"hr/EmployeeException/EmpExceptionUpdate.html")

def profile(request):
    return render(request, "hr/Profile/profile.html")

def editProfile(request):
    return render(request, "hr/Profile/edit_profile.html")


def changePassword(request):
    return render(request, "hr/Profile/change_password.html")



def documentforpassport(request):
    return render(request, "hr/documentforpassport/documentforpassport.html")

def documentforpassporthistory(request):
    return render(request, "hr/documentforpassport/documentforpassporthistory.html")

def documentforpassportupdate(request):
    return render(request, "hr/documentforpassport/documentforpassportupdate.html")




import os

file_path = os.path.join('media', 'stored_upload', 'FARHANA BADUBHAI.vcf')
if os.path.exists(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        print(f"File size: {len(file_content)} bytes")
        print(file_content)
else:
    print("File not found")
