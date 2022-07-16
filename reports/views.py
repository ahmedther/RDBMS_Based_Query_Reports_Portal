from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import FileResponse


from .connections import Oracle
from .oracle_config import Ora
from .decorators import unauthenticated_user, allowed_users
from .forms import DateForm,DateTimeForm
from .models import IAACR, FacilityDropdown
from .new_db_oracle import NewDB_Ora
from .supports import date_formater,excel_generator



# Create your views here.

@unauthenticated_user
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'reports/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return render(request, 'reports/index.html', {'success':'You Have Successfuly Signed Up','success1':'Please enter your User ID and Password to Sign In'})
            
            except IntegrityError:
                return render(request, 'reports/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
            
            except ValueError:
                return render(request, 'reports/signupuser.html', {'form':UserCreationForm(), 'error':'Please Enter a Valid Username and Password'})
        else:
            return render(request, 'reports/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


@unauthenticated_user
def login_page(request):

    if request.method == 'GET':
        return render(request, 'reports/login_page.html')
    
    else:
        
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        global user_name
        user_name = request.POST['username']
        
        if user is None:
            return render(request,'reports/login_page.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return render(request,'reports/index.html', {'user_name':request.user.username})
            

@login_required(login_url='login')
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


@login_required(login_url='login')
def landing_page(request):

    if request.method == 'GET':
        return render(request,'reports/index.html', {'user_name':request.user.username})
    
     
    
            


    

@login_required(login_url='login')
def base(request):
    # Pharmacy Based permissions
    pharmacy_permission = request.user.groups.filter(name="Pharmacy")
    stock_permission = request.user.groups.filter(name="Pharmacy - Stock")
    stock_report_permission = request.user.groups.filter(name="Pharmacy - Stock Report")
    stock_value_permission = request.user.groups.filter(name="Pharmacy - Stock Value")
    bin_location_op_permission = request.user.groups.filter(name="Pharmacy - Bin Location OP")
    itemwise_storewise_stock_permission = request.user.groups.filter(name="Pharmacy - Itemwise Storewise Stock Value")
    batchwise_stock_report_permission = request.user.groups.filter(name="Pharmacy - Batch Wise Stock Report")
    pharmacy_op_returns_permission = request.user.groups.filter(name="Pharmacy - Pharmacy OP Returns")
    restricted_antimicrobials_consumption_report_permission = request.user.groups.filter(name="Pharmacy - Restricted Antimicrobials Consumption Report")
    important_antimicrobials_antibiotics_consumption_report_permission = request.user.groups.filter(name="Pharmacy - Important Antimicrobials / Antibiotics Consumption Report")
    pharmacy_indent_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Indent Report")
    new_admission_indents_report_permission = request.user.groups.filter(name="Pharmacy - New Admission’s Indents Report")
    return_medication_without_return_request_report_permission = request.user.groups.filter(name="Pharmacy - Return Medication Without Return Request Report")
    deleted_pharmacy_prescriptions_report_permission = request.user.groups.filter(name="Pharmacy - Deleted Pharmacy Prescriptions Report")
    pharmacy_direct_sales_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Direct Sales Report")
    intransites_unf_sal_permission = request.user.groups.filter(name="Pharmacy - Intransites Unf Sal")
    intransites_confirm_pending_permission = request.user.groups.filter(name="Pharmacy - Intransites Confirm Pending")
    non_billable_consumption_permission = request.user.groups.filter(name="Pharmacy - Non Billable Consumption")
    non_billable_consumption1_permission = request.user.groups.filter(name="Pharmacy - Non Billable Consumption 1")
    pharmacy_charges_and_implant_pending_indent_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Charges & Implant Pending Indent Report")
    pharmacy_direct_returns_sale_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Direct Returns Sale Report")
    current_inpatients_report_permission = request.user.groups.filter(name="Pharmacy - Current Inpatients Reports")
    consigned_item_detail_report_permission = request.user.groups.filter(name="Pharmacy - Consigned Item Detail Report")
    schedule_h1_drug_report_permission = request.user.groups.filter(name="Pharmacy - Schedule H1 Drug Report")
    pharmacy_ward_return_requests_with_status_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Ward Return Requests with Status Report")
    pharmacy_indent_deliver_summary_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Indent Deliver Summary Report")
    intransites_stk_tfr_acknowledgement_pending_permission = request.user.groups.filter(name="Pharmacy - Intransites Stk Tfr Acknowledgement Pending Report")
    folley_and_central_line_permission = request.user.groups.filter(name="Pharmacy - Folley and Central Line")
    angiography_kit_permission = request.user.groups.filter(name="Pharmacy - Angiography Kit")
    new_admission_dispense_report_permission = request.user.groups.filter(name="Pharmacy - New Admission Dispense Report")
    pharmacy_op_sale_report_userwise_permission = request.user.groups.filter(name="Pharmacy - Pharmacy OP Sale Report Userwise")
    pharmacy_consumption_report_permission = request.user.groups.filter(name="Pharmacy - Pharmacy Consumption Report")
    food_drug_interaction_report_permission = request.user.groups.filter(name="Pharmacy - Food-Drug Interaction Report")
    intransite_stock_permission = request.user.groups.filter(name="Pharmacy - Intransite Stock")
    grn_data_permission = request.user.groups.filter(name="Pharmacy - GRN Data")
    drug_duplication_override_report_permission = request.user.groups.filter(name="Pharmacy - Drug Duplication Override Report")
    drug_interaction_override_report_permission = request.user.groups.filter(name="Pharmacy - Drug Interaction Override Report")
    sale_consumption_report_permission = request.user.groups.filter(name="Pharmacy - Sale Consumption Report")
    sale_consumption_report1_permission = request.user.groups.filter(name="Pharmacy - Sale Consumption Report 1")
    predischarge_medication_permission = request.user.groups.filter(name="Pharmacy - Predischarge Medication")
    predischarge_initiate_permission = request.user.groups.filter(name="Pharmacy - Predischarge Initiate")
    intransites_unf_sal_ret_permission = request.user.groups.filter(name="Pharmacy - Intransites Unf Sal Ret")
    intransites_unf_stk_tfr_permission = request.user.groups.filter(name="Pharmacy - Intransites Unf Stk Tfr")
    intransites_acknowledgement_pending_iss_permission = request.user.groups.filter(name="Pharmacy - Intransites Acknowledgement Pending ISS")
    intransites_acknowledgement_pending_iss_rt_permission = request.user.groups.filter(name="Pharmacy - Intransites Acknowledgement Pending ISS RT")

    # Finance Based Permissions
    finance_permission = request.user.groups.filter(name="Finance")
    credit_outstanding_bill_permission = request.user.groups.filter(name="Finance - Credit Bill Outstanding")
    tpa_letter_permission = request.user.groups.filter(name="Finance - TPA Letter")
    online_consultation_report_permission = request.user.groups.filter(name="Finance - Online Consultation Report")
    contract_report_permission = request.user.groups.filter(name="Finance - Contract Reports")
    package_contract_report_permission = request.user.groups.filter(name="Finance - Package Contract Report")
    credit_card_reconciliation_report_permission = request.user.groups.filter(name="Finance - Credit Card Reconciliation Report")
    covid_ot_surgery_details_permission = request.user.groups.filter(name="Finance - Covid OT Surgery Details")
    gst_data_of_pharmacy_permission = request.user.groups.filter(name="Finance - GST Data of Pharmacy")
    gst_data_of_pharmacy_return_permission = request.user.groups.filter(name="Finance - GST Data of Pharmacy Return")
    gst_data_of_ip_permission = request.user.groups.filter(name="Finance - GST Data of IP")
    gst_data_of_op_permission = request.user.groups.filter(name="Finance - GST Data of OP")
    revenue_data_of_sl_permission = request.user.groups.filter(name="Finance - Revenue Data of SL")
    revenue_data_of_sl1_permission = request.user.groups.filter(name="Finance - Revenue Data of SL 1")
    revenue_data_of_sl2_permission = request.user.groups.filter(name="Finance - Revenue Data of SL 2")
    revenue_data_of_sl3_permission = request.user.groups.filter(name="Finance - Revenue Data of SL 3")
    

    # Clinical Administration Based Permissions
    clinical_administration_permission = request.user.groups.filter(name="Clinical Administration")
    discharge_report_2_permission = request.user.groups.filter(name="Clinical Administration - Discharge Report 2")
    pre_discharge_report_permission = request.user.groups.filter(name="Clinical Administration - Pre Discharge Report")
    pre_discharge_report_2_permission = request.user.groups.filter(name="Clinical Administration - Pre Discharge Report 2")
    discharge_with_mis_report_permission = request.user.groups.filter(name="Clinical Administration - Discharge With MIS Report")
    needle_prick_injury_report_permission = request.user.groups.filter(name="Clinical Administration - Needle Prick Injury Report")
    practo_report_permission = request.user.groups.filter(name="Clinical Administration - Practo Report")
    unbilled_report_permission = request.user.groups.filter(name="Clinical Administration - Unbilled Report")
    unbilled_deposit_report_permission = request.user.groups.filter(name="Clinical Administration - Unbilled Deposit Report")
    contact_report_permission = request.user.groups.filter(name="Clinical Administration - Contact Report")
    employees_antibodies_reactive_report_permission = request.user.groups.filter(name="Clinical Administration - Employees Antibodies Reactive Report")
    employees_reactive_and_non_pcr_report_permission = request.user.groups.filter(name="Clinical Administration - Employee Reactive and Non PCR Report")
    employee_covid_test_report_permission = request.user.groups.filter(name="Clinical Administration - Employee Covid Test Report")
    bed_location_report_permission = request.user.groups.filter(name="Clinical Administration - Bed Location Report")
    home_visit_report_permission = request.user.groups.filter(name="Clinical Administration - Home Visit Report")
    cco_billing_count_report_permission = request.user.groups.filter(name="Clinical Administration - CCO Billing Count Report")
    total_number_of_online_consultation_by_doctors_permission = request.user.groups.filter(name="Clinical Administration - Total Number of Online Consultation by Doctors")
    total_number_of_ip_patients_by_doctors_permission = request.user.groups.filter(name="Clinical Administration - Total Number of IP Patients by Doctors")
    total_number_of_op_patients_by_doctors_permission = request.user.groups.filter(name="Clinical Administration - Total Number of OP Patients by Doctors")
    opd_changes_report_permission = request.user.groups.filter(name="Clinical Administration - OPD Changes Report")
    ehc_conversion_report_permission = request.user.groups.filter(name="Clinical Administration - EHC Conversion Report")
    ehc_package_range_report_permission = request.user.groups.filter(name="Clinical Administration - EHC Package Range Report")
    error_report_permission = request.user.groups.filter(name="Clinical Administration - Error Report")
    ot_query_report_permission = request.user.groups.filter(name="Clinical Administration - OT Query Report")
    outreach_cancer_hospital_permission = request.user.groups.filter(name="Clinical Administration - Outreach Cancer Hospital")
    gipsa_report_permission = request.user.groups.filter(name="Clinical Administration - GIPSA Report")
    precision_patient_opd_and_online_consultation_list_report_permission = request.user.groups.filter(name="Clinical Administration - Precision Patient OPD & Online Consultation List Report") 
    appointment_details_by_call_center_report_permission = request.user.groups.filter(name="Clinical Administration - Appointment Details By Call Center Report") 
    trf_report_permission = request.user.groups.filter(name="Clinical Administration - TRF Report")
    current_inpatients_clinical_admin_permission = request.user.groups.filter(name="Clinical Administration - Current Inpatients(Clinical Admin)")
    check_patient_registration_date_permission = request.user.groups.filter(name="Clinical Administration - Check Patient Registration Date")
    covid_antigen_permission = request.user.groups.filter(name="Clinical Administration - Covid Antigen")
    current_inpatients_employee_and_dependants_permission = request.user.groups.filter(name="Clinical Administration - Current Inpatients Employee and Dependants")
    treatment_sheet_data_permission = request.user.groups.filter(name="Clinical Administration - Treatment Sheet Data")
    patient_registration_report_permission = request.user.groups.filter(name="Clinical Administration - Patient Registration Report")
    




    #Lab Baed Permissions
    lab_permission = request.user.groups.filter(name="Lab")
    covid_pcr_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - Covid PCR")
    covid_2_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - Covid 2")
    covid_antibodies_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - Covid Antibodies")
    cbnaat_test_data_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - CBNAAT Test Data")
    lab_tat_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - LAB TAT Report")
    histopath_fixation_data_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - Histopath Fixation Data")
    slide_label_data_permission = request.user.groups.filter(name="Miscellaneous Reports - Lab - Slide Label Data")




    # Marketing Based Permissions
    marketing_permission = request.user.groups.filter(name="Marketing")
    contract_effective_date_report_permission = request.user.groups.filter(name="Marketing - Contract Effective Date Report")
    admission_report_permission = request.user.groups.filter(name="Marketing - Admission Reports")
    patient_discharge_report_permission = request.user.groups.filter(name="Marketing - Patient Discharge Report")
    credit_letter_report_permission = request.user.groups.filter(name="Marketing - Credit Letter Report")
    corporate_ip_report_permission = request.user.groups.filter(name="Marketing - Corporate IP Report")
    opd_consultation_report_permission = request.user.groups.filter(name="Marketing - OPD Consultation Report")
    emergency_casualty_report_permission = request.user.groups.filter(name="Marketing - Emergency Casualty Report")
    new_registration_report_permission = request.user.groups.filter(name="Marketing - New Registration Report")
    hospital_tariff_report_permission = request.user.groups.filter(name="Marketing - Hospital Tariff Report")
    international_patient_report_permission = request.user.groups.filter(name="Marketing - International Patient Report")
    tpa_query_permission = request.user.groups.filter(name="Marketing - TPA Query")
    new_admission_report_permission = request.user.groups.filter(name="Marketing - New Admission Report")



    # Miscellaneous_Reports
    miscellaneous_reports_permission = request.user.groups.filter(name="Miscellaneous Reports")
    ot_scheduling_list_report_permission = request.user.groups.filter(name="Miscellaneous Reports - OT Scheduling List Report")
    non_package_covid_patient_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Non Package Covid Patient Report")
    
    #Billing
    billing_permission = request.user.groups.filter(name="Billing")
    discharge_billing_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Billing - Discharge Billing Report")
    discharge_billing_report_without_date_range_permission = request.user.groups.filter(name="Miscellaneous Reports - Billing - Discharge Billing Report Without Date Range")
    discharge_billing_user_permission = request.user.groups.filter(name="Miscellaneous Reports - Billing - Discharge Billing User")
    discount_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Billing - Discount Report")
    refund_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Billing - Refund Report")
    non_medical_equipment_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Billing - Non Medical Equipment Report")
    #EHC
    ehc_permission = request.user.groups.filter(name="EHC")
    ehc_operation_report_permission = request.user.groups.filter(name="Miscellaneous Reports - EHC - EHC Operation Report")
    ehc_operation_report_2_permission = request.user.groups.filter(name="Miscellaneous Reports - EHC - EHC Operation Report 2")
    #Sales
    sales_permission = request.user.groups.filter(name="Sales")
    oncology_drugs_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Sales - Oncology Drugs Report")
    #Radiology
    radiology_permission = request.user.groups.filter(name="Radiology")
    radiology_tat_report_permission = request.user.groups.filter(name="Miscellaneous Reports - Radiology - Radiology TAT Report")


    


    return render(request,'reports/base.html', {
        #Pharmacy Permission Dictionary
        'user_name':request.user.username,
        "pharmacy_permission":pharmacy_permission,
        "stock_permission" : stock_permission,
        "stock_report_permission":stock_report_permission,
        "stock_value_permission":stock_value_permission,
        "bin_location_op_permission":bin_location_op_permission,
        "itemwise_storewise_stock_permission":itemwise_storewise_stock_permission,
        "batchwise_stock_report_permission":batchwise_stock_report_permission,
        "pharmacy_op_returns_permission":pharmacy_op_returns_permission,
        "restricted_antimicrobials_consumption_report_permission":restricted_antimicrobials_consumption_report_permission,
        "important_antimicrobials_antibiotics_consumption_report_permission":important_antimicrobials_antibiotics_consumption_report_permission,
        "pharmacy_indent_report_permission":pharmacy_indent_report_permission,
        "new_admission_indents_report_permission":new_admission_indents_report_permission,
        "return_medication_without_return_request_report_permission":return_medication_without_return_request_report_permission,
        "deleted_pharmacy_prescriptions_report_permission":deleted_pharmacy_prescriptions_report_permission,
        "pharmacy_direct_sales_report_permission":pharmacy_direct_sales_report_permission,
        "intransites_unf_sal_permission":intransites_unf_sal_permission,
        "intransites_confirm_pending_permission":intransites_confirm_pending_permission,
        "non_billable_consumption_permission": non_billable_consumption_permission,
        "non_billable_consumption1_permission": non_billable_consumption1_permission,
        "pharmacy_charges_and_implant_pending_indent_report_permission":pharmacy_charges_and_implant_pending_indent_report_permission,
        "pharmacy_direct_returns_sale_report_permission":pharmacy_direct_returns_sale_report_permission,
        "current_inpatients_report_permission":current_inpatients_report_permission,
        "consigned_item_detail_report_permission":consigned_item_detail_report_permission,
        "schedule_h1_drug_report_permission":schedule_h1_drug_report_permission,
        "pharmacy_ward_return_requests_with_status_report_permission":pharmacy_ward_return_requests_with_status_report_permission,
        "pharmacy_indent_deliver_summary_report_permission":pharmacy_indent_deliver_summary_report_permission,
        "intransites_stk_tfr_acknowledgement_pending_permission":intransites_stk_tfr_acknowledgement_pending_permission,
        "folley_and_central_line_permission":folley_and_central_line_permission,
        "angiography_kit_permission":angiography_kit_permission,
        "new_admission_dispense_report_permission":new_admission_dispense_report_permission,
        "pharmacy_op_sale_report_userwise_permission":pharmacy_op_sale_report_userwise_permission,
        "credit_card_reconciliation_report_permission":credit_card_reconciliation_report_permission,
        "pharmacy_consumption_report_permission":pharmacy_consumption_report_permission,
        "food_drug_interaction_report_permission":food_drug_interaction_report_permission,
        "intransite_stock_permission":intransite_stock_permission,
        "grn_data_permission":grn_data_permission,
        "drug_duplication_override_report_permission":drug_duplication_override_report_permission,
        "drug_interaction_override_report_permission":drug_interaction_override_report_permission,
        "sale_consumption_report_permission":sale_consumption_report_permission,
        "sale_consumption_report1_permission":sale_consumption_report1_permission,
        "predischarge_medication_permission":predischarge_medication_permission,
        "predischarge_initiate_permission":predischarge_initiate_permission,
        "intransites_unf_sal_ret_permission":intransites_unf_sal_ret_permission,
        "intransites_unf_stk_tfr_permission":intransites_unf_stk_tfr_permission,
        "intransites_acknowledgement_pending_iss_permission":intransites_acknowledgement_pending_iss_permission,
        "intransites_acknowledgement_pending_iss_rt_permission":intransites_acknowledgement_pending_iss_rt_permission,


        #Finance Permission Dictionary
        "finance_permission":finance_permission,
        "credit_outstanding_bill_permission":credit_outstanding_bill_permission,
        "tpa_letter_permission":tpa_letter_permission,
        "online_consultation_report_permission":online_consultation_report_permission,
        "contract_report_permission":contract_report_permission,
        "package_contract_report_permission":package_contract_report_permission,
        "covid_ot_surgery_details_permission":covid_ot_surgery_details_permission,
        "gst_data_of_pharmacy_permission":gst_data_of_pharmacy_permission,
        "gst_data_of_pharmacy_return_permission":gst_data_of_pharmacy_return_permission,
        "gst_data_of_ip_permission":gst_data_of_ip_permission,
        "gst_data_of_op_permission":gst_data_of_op_permission,
        "revenue_data_of_sl_permission":revenue_data_of_sl_permission,
        "revenue_data_of_sl1_permission":revenue_data_of_sl1_permission,
        "revenue_data_of_sl2_permission":revenue_data_of_sl2_permission,
        "revenue_data_of_sl3_permission":revenue_data_of_sl3_permission,

        

        # Clinical Administration Based Permissions
        "clinical_administration_permission":clinical_administration_permission,
        "discharge_report_2_permission":discharge_report_2_permission,
        "pre_discharge_report_permission":pre_discharge_report_permission,
        "pre_discharge_report_2_permission":pre_discharge_report_2_permission,
        "discharge_with_mis_report_permission":discharge_with_mis_report_permission,
        "needle_prick_injury_report_permission":needle_prick_injury_report_permission,
        "practo_report_permission":practo_report_permission,
        "unbilled_report_permission":unbilled_report_permission,
        "unbilled_deposit_report_permission":unbilled_deposit_report_permission,
        "contact_report_permission":contact_report_permission,
        "employees_antibodies_reactive_report_permission":employees_antibodies_reactive_report_permission,
        "employees_reactive_and_non_pcr_report_permission":employees_reactive_and_non_pcr_report_permission,
        "employee_covid_test_report_permission":employee_covid_test_report_permission,
        "bed_location_report_permission":bed_location_report_permission,
        "home_visit_report_permission":home_visit_report_permission,
        "cco_billing_count_report_permission":cco_billing_count_report_permission,
        "total_number_of_online_consultation_by_doctors_permission":total_number_of_online_consultation_by_doctors_permission,
        "total_number_of_ip_patients_by_doctors_permission":total_number_of_ip_patients_by_doctors_permission,
        "total_number_of_op_patients_by_doctors_permission":total_number_of_op_patients_by_doctors_permission,
        "opd_changes_report_permission":opd_changes_report_permission,
        "ehc_conversion_report_permission":ehc_conversion_report_permission,
        "ehc_package_range_report_permission":ehc_package_range_report_permission,
        "error_report_permission":error_report_permission,
        "ot_query_report_permission":ot_query_report_permission,
        "outreach_cancer_hospital_permission":outreach_cancer_hospital_permission,
        "gipsa_report_permission":gipsa_report_permission,
        "precision_patient_opd_and_online_consultation_list_report_permission":precision_patient_opd_and_online_consultation_list_report_permission,
        "appointment_details_by_call_center_report_permission":appointment_details_by_call_center_report_permission,
        "trf_report_permission":trf_report_permission,
        "current_inpatients_clinical_admin_permission":current_inpatients_clinical_admin_permission,
        "check_patient_registration_date_permission":check_patient_registration_date_permission,
        "patient_registration_report_permission":patient_registration_report_permission,
        "current_inpatients_employee_and_dependants_permission":current_inpatients_employee_and_dependants_permission,
        "treatment_sheet_data_permission":treatment_sheet_data_permission,


        # Marketing
        "marketing_permission":marketing_permission,
        "contract_effective_date_report_permission":contract_effective_date_report_permission,
        "patient_discharge_report_permission":patient_discharge_report_permission,
        "admission_report_permission":admission_report_permission,
        "credit_letter_report_permission":credit_letter_report_permission,
        "corporate_ip_report_permission":corporate_ip_report_permission,
        "opd_consultation_report_permission":opd_consultation_report_permission,
        "emergency_casualty_report_permission":emergency_casualty_report_permission,
        "new_registration_report_permission":new_registration_report_permission,
        "hospital_tariff_report_permission":hospital_tariff_report_permission,
        "international_patient_report_permission":international_patient_report_permission,
        "tpa_query_permission":tpa_query_permission,
        "new_admission_report_permission":new_admission_report_permission,


        # Miscellaneous_Reports
        "miscellaneous_reports_permission":miscellaneous_reports_permission,
        #Billing
        "billing_permission":billing_permission,
        "discharge_billing_report_permission":discharge_billing_report_permission,
        "discharge_billing_report_without_date_range_permission":discharge_billing_report_without_date_range_permission,
        "discharge_billing_user_permission":discharge_billing_user_permission,
        "discount_report_permission":discount_report_permission,
        "refund_report_permission":refund_report_permission,
        "non_medical_equipment_report_permission":non_medical_equipment_report_permission,
        # Lab
        "lab_permission":lab_permission,
        "covid_antibodies_permission":covid_antibodies_permission,
        "covid_pcr_permission":covid_pcr_permission,
        "covid_2_permission":covid_2_permission,
        "covid_antigen_permission":covid_antigen_permission,
        "cbnaat_test_data_permission":cbnaat_test_data_permission,
        "lab_tat_report_permission":lab_tat_report_permission,
        "histopath_fixation_data_permission":histopath_fixation_data_permission,
        "slide_label_data_permission":slide_label_data_permission,
        #EHC
        "ehc_permission":ehc_permission,
        "ehc_operation_report_permission":ehc_operation_report_permission,
        "ehc_operation_report_2_permission":ehc_operation_report_2_permission,
        #Sales
        "sales_permission":sales_permission,
        "oncology_drugs_report_permission":oncology_drugs_report_permission,
        #Radiology
        "radiology_permission":radiology_permission,
        "radiology_tat_report_permission":radiology_tat_report_permission,
        #---
        "ot_scheduling_list_report_permission":ot_scheduling_list_report_permission,
        "non_package_covid_patient_report_permission":non_package_covid_patient_report_permission,

        })
    

@login_required(login_url='login')
@allowed_users('Pharmacy - Stock')
def stock(request):

    if request.method == 'GET':
        return render(request,'reports/stock.html', {'user_name':request.user.username, "page_name" : "Stock"})
    
     
    elif request.method == 'POST':
        db =  Ora()
        stock_data, stock_column = db.get_stock()
        excel_file_path = excel_generator(page_name="Stock", column=stock_column,data=stock_data)

        if not stock_data:
            return render(request,'reports/stock.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/stock.html', {'stock_data':stock_data, 'user_name':request.user.username})
            
    
            
        

@login_required(login_url='login')
@allowed_users('Pharmacy - Stock Report')
def stock_report(request):

    if request.method == 'GET':
        return render(request,'reports/stock_report.html', {'user_name':request.user.username, "page_name" : "Stock Report"})

    
    elif request.method == 'POST':
        db =  Ora()
        stock_report,column_name = db.get_stock_reports()
        excel_file_path = excel_generator(page_name="Stock Report", column=column_name,data=stock_report)

        if not stock_report:
            return render(request,'reports/stock_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/stock_report.html', {'stock_report':stock_report, 'user_name':request.user.username})
        

            
        


@login_required(login_url='login')
@allowed_users('Pharmacy - Stock Value')
def stock_value(request):
    if request.method == 'GET':
        return render(request,'reports/stock_value.html', {'user_name':request.user.username, "page_name" : "Stock Value"})

    
    elif request.method == 'POST':
        db =  Ora()
        stock_value,column_name = db.get_stock_value()
        excel_file_path = excel_generator(page_name="Stock Value",data=stock_value,column=column_name)

        if not stock_value:
            return render(request,'reports/stock_value.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/stock_value.html', {'stock_value':stock_value, 'user_name':request.user.username})
        


@login_required(login_url='login')
@allowed_users('Pharmacy - Bin Location OP')
def bin_location_op(request):

    if request.method == 'GET':
        return render(request,'reports/bin_location_op.html', {'user_name':request.user.username , "page_name" : "Bin Location OP"})

    
    elif request.method == 'POST':
        db =  Ora()
        bin_location_op_value,column_name = db.get_bin_location_op_value()
        excel_file_path = excel_generator(page_name="Bin Location OP",data=bin_location_op_value,column=column_name)

        if not bin_location_op_value:
            return render(request,'reports/bin_location_op.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})
        
        else:         
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/bin_location_op.html', {'bin_location_op_value':bin_location_op_value, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users('Pharmacy - Itemwise Storewise Stock Value')
def itemwise_storewise_stock(request):
    

    if request.method == 'GET':
        return render(request,'reports/itemwise_storewise_stock.html', {'user_name':request.user.username , "page_name" : "Itemwise Storewise Stock Value"})


    elif request.method == 'POST':
        db =  Ora()
        itemwise_storewise_stock_value,column_name = db.get_itemwise_storewise_stock()
        excel_file_path = excel_generator(page_name="Itemwise Storewise Stock Value",data=itemwise_storewise_stock_value,column=column_name)

        if not itemwise_storewise_stock_value:
            return render(request,'reports/itemwise_storewise_stock.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/itemwise_storewise_stock.html', {'itemwise_storewise_stock_value':itemwise_storewise_stock_value, 'user_name':request.user.username})

        


@login_required(login_url='login')
@allowed_users('Pharmacy - Batch Wise Stock Report')
def batchwise_stock_report(request):
    if request.method == 'GET':
        return render(request,'reports/batchwise_stock_report.html', {'user_name':request.user.username , "page_name" : "Batch Wise Stock Report"})
   
     
    elif request.method == 'POST':
        db =  Ora()
        batchwise_stock_report_value,column_name = db.get_batchwise_stock_report()
        excel_file_path = excel_generator(page_name="Batch Wise Stock Report",data=batchwise_stock_report_value,column=column_name)

        if not batchwise_stock_report_value:
            return render(request,'reports/batchwise_stock_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/batchwise_stock_report.html', {'batchwise_stock_report_value':batchwise_stock_report_value, 'user_name':request.user.username})
            
            
        


@login_required(login_url='login')
@allowed_users('Pharmacy - Pharmacy OP Returns')
def pharmacy_op_returns(request):
    if request.method == 'GET':
        return render(request,'reports/pharmacy_op_returns.html', {'user_name':request.user.username , "page_name" : "Pharmacy OP Returns"})
    
    elif request.method == 'POST':
        db =  Ora()
        pharmacy_op_returns_value,column_name = db.get_pharmacy_op_returns()
        excel_file_path = excel_generator(page_name="Pharmacy OP Returns",data=pharmacy_op_returns_value,column=column_name)
        
        if not pharmacy_op_returns_value:
            return render(request,'reports/pharmacy_op_returns.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_op_returns.html', {'pharmacy_op_returns_value':pharmacy_op_returns_value, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users('Pharmacy - Restricted Antimicrobials Consumption Report')
def restricted_antimicrobials_consumption_report(request):
    if request.method == 'GET':
        return render(request,'reports/restricted_antimicrobials_consumption_report.html', {'user_name':request.user.username , "page_name" : "Restricted Antimicrobials Consumption Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        restricted_antimicrobials_consumption_report_value,column_name = db.get_restricted_antimicrobials_consumption_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Restricted Antimicrobials Consumption Report",data=restricted_antimicrobials_consumption_report_value,column=column_name)

        if not restricted_antimicrobials_consumption_report_value:
            return render(request,'reports/restricted_antimicrobials_consumption_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/restricted_antimicrobials_consumption_report.html', {'restricted_antimicrobials_consumption_report_value':restricted_antimicrobials_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users('Pharmacy - Important Antimicrobials / Antibiotics Consumption Report')
def important_antimicrobials_antibiotics_consumption_report(request):
    drugs = IAACR.objects.all()

    if request.method == 'GET':

        

        return render(request,'reports/important_antimicrobials_antibiotics_consumption_report.html', {
            'user_name':request.user.username , 
            "page_name" : "Important Antimicrobials / Antibiotics Consumption Report", 
            'date_form' : DateForm(),
            'drugs' : drugs,
            
            })
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        # Select Function from model
        drug_code = request.POST['drug_dropdown']
        

        db = Ora()
        important_antimicrobials_antibiotics_consumption_report_value,column_name = db.get_important_antimicrobials_antibiotics_consumption_report(drug_code,from_date, to_date)
        excel_file_path = excel_generator(page_name="Important Antimicrobials / Antibiotics Consumption Report",data=important_antimicrobials_antibiotics_consumption_report_value,column=column_name)

        if not important_antimicrobials_antibiotics_consumption_report_value:
            return render(request,'reports/important_antimicrobials_antibiotics_consumption_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'drugs' : drugs})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/important_antimicrobials_antibiotics_consumption_report.html', {'important_antimicrobials_antibiotics_consumption_report':important_antimicrobials_antibiotics_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'drugs' : drugs})



@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Indent Report")
def pharmacy_indent_report(request):

    if request.method == 'GET':
        return render(request,'reports/pharmacy_indent_report.html', {'user_name':request.user.username, "page_name" : "Pharmacy Indent Report"})
    
     
    elif request.method == 'POST':
        db = Ora()
        pharmacy_indent_report_data,column_name = db.get_pharmacy_indent_report()
        excel_file_path = excel_generator(page_name="Pharmacy Indent Report",data=pharmacy_indent_report_data,column=column_name)

        if not pharmacy_indent_report_data:
            return render(request,'reports/pharmacy_indent_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_indent_report.html', {'pharmacy_indent_report_data':pharmacy_indent_report_data, 'user_name':request.user.username})



@login_required(login_url='login')
@allowed_users("Pharmacy - New Admission’s Indents Report")
def new_admission_indents_report(request):

    if request.method == 'GET':
        return render(request,'reports/new_admission_indents_report.html', {'user_name':request.user.username, "page_name" : "New Admission’s Indents Report"})
    
     
    elif request.method == 'POST':
        db = Ora()
        new_admission_indents_report_data,column_name = db.get_new_admission_indents_report()
        excel_file_path = excel_generator(page_name="New Admission’s Indents Report",data=new_admission_indents_report_data,column=column_name)

        if not new_admission_indents_report_data:
            return render(request,'reports/new_admission_indents_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/new_admission_indents_report.html', {'new_admission_indents_report_data':new_admission_indents_report_data, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users("Pharmacy - Return Medication Without Return Request Report")
def return_medication_without_return_request_report(request):
    if request.method == 'GET':
        return render(request,'reports/return_medication_without_return_request_report.html', {'user_name':request.user.username , "page_name" : "Return Medication Without Return Request Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        return_medication_without_return_request_report_value,column_name = db.get_return_medication_without_return_request_report_value(from_date,to_date)
        excel_file_path = excel_generator(page_name="Return Medication Without Return Request Report",data=return_medication_without_return_request_report_value,column=column_name)

        if not return_medication_without_return_request_report_value:
            return render(request,'reports/return_medication_without_return_request_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/return_medication_without_return_request_report.html', {'return_medication_without_return_request_report_value':return_medication_without_return_request_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    


@login_required(login_url='login')
@allowed_users("Pharmacy - Deleted Pharmacy Prescriptions Report")
def deleted_pharmacy_prescriptions_report(request):
    if request.method == 'GET':
        return render(request,'reports/deleted_pharmacy_prescriptions_report.html', {'user_name':request.user.username , "page_name" : "Deleted Pharmacy Prescriptions Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']

        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])

        from_date = from_date + " " + from_time
        to_date = to_date + " " + to_time
        
        db = Ora()
        deleted_pharmacy_prescriptions_report_value, deleted_pharmacy_prescriptions_report_column_name = db.get_deleted_pharmacy_prescriptions_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Deleted Pharmacy Prescriptions Report",data=deleted_pharmacy_prescriptions_report_value,column=deleted_pharmacy_prescriptions_report_column_name)

        if not deleted_pharmacy_prescriptions_report_value:
            return render(request,'reports/deleted_pharmacy_prescriptions_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/deleted_pharmacy_prescriptions_report.html', {'deleted_pharmacy_prescriptions_report_value':deleted_pharmacy_prescriptions_report_value, "deleted_pharmacy_prescriptions_report_column_name":deleted_pharmacy_prescriptions_report_column_name, 'user_name':request.user.username,'date_form' : DateForm()})





@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Direct Returns Sale Report")
def pharmacy_direct_sales_report(request):
    if request.method == 'GET':
        return render(request,'reports/pharmacy_direct_sales_report.html', {'user_name':request.user.username , "page_name" : "Pharmacy Direct Sales Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        pharmacy_direct_sales_report_value,column_name = db.get_pharmacy_direct_sales_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pharmacy Direct Returns Sale Report",data=pharmacy_direct_sales_report_value,column=column_name)

        if not pharmacy_direct_sales_report_value:
            return render(request,'reports/pharmacy_direct_sales_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_direct_sales_report.html', {'pharmacy_direct_sales_report_value':pharmacy_direct_sales_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Pharmacy - Intransites Unf Sal')
def intransites_unf_sal(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_unf_sal.html', {'user_name':request.user.username, "page_name" : "Intransites Unf Sal",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        intransites_unf_sal_data, intransites_unf_sal_column_name = db.get_intransites_unf_sal(from_date,to_date)
        excel_file_path = excel_generator(page_name="Intransites Unf Sal",data=intransites_unf_sal_data,column=intransites_unf_sal_column_name)

        if not intransites_unf_sal_data:
            return render(request,'reports/intransites_unf_sal.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_unf_sal.html', {'intransites_unf_sal_data':intransites_unf_sal_data, "intransites_unf_sal_column_name":intransites_unf_sal_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Unf Sal"})



@login_required(login_url='login')
@allowed_users('Pharmacy - Intransites Confirm Pending')
def intransites_confirm_pending(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_confirm_pending.html', {'user_name':request.user.username, "page_name" : "Intransites Confirm Pending"})
    
     
    elif request.method == 'POST':
        db =  Ora()
        intransites_confirm_pending_data, intransites_confirm_pending_column_name = db.get_intransites_confirm_pending()
        excel_file_path = excel_generator(page_name="Intransites Confirm Pending",data=intransites_confirm_pending_data,column=intransites_confirm_pending_column_name)

        if not intransites_confirm_pending_data:
            return render(request,'reports/intransites_confirm_pending.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_confirm_pending.html', {'intransites_confirm_pending_data':intransites_confirm_pending_data, "intransites_confirm_pending_column_name":intransites_confirm_pending_column_name,'user_name':request.user.username, "page_name" : "Intransites Confirm Pending"})


@login_required(login_url='login')
@allowed_users('Pharmacy - Non Billable Consumption')
def non_billable_consumption(request):

    if request.method == 'GET':
        return render(request,'reports/non_billable_consumption.html', {'user_name':request.user.username, "page_name" : "Non Billable Consumption",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        non_billable_consumption_data, non_billable_consumption_column_name = db.get_non_billable_consumption(from_date,to_date)
        excel_file_path = excel_generator(page_name="Non Billable Consumption",data=non_billable_consumption_data,column=non_billable_consumption_column_name)

        if not non_billable_consumption_data:
            return render(request,'reports/non_billable_consumption.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/non_billable_consumption.html', {'non_billable_consumption_data':non_billable_consumption_data, "non_billable_consumption_column_name":non_billable_consumption_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Non Billable Consumption"})



@login_required(login_url='login')
@allowed_users('Pharmacy - Non Billable Consumption 1')
def non_billable_consumption1(request):

    if request.method == 'GET':
        return render(request,'reports/non_billable_consumption1.html', {'user_name':request.user.username, "page_name" : "Non Billable Consumption 1",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        non_billable_consumption1_data, non_billable_consumption1_column_name = db.get_non_billable_consumption1(from_date,to_date)
        excel_file_path = excel_generator(page_name="Non Billable Consumption 1",data=non_billable_consumption1_data,column=non_billable_consumption1_column_name)

        if not non_billable_consumption1_data:
            return render(request,'reports/non_billable_consumption1.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/non_billable_consumption1.html', {'non_billable_consumption1_data':non_billable_consumption1_data, "non_billable_consumption1_column_name":non_billable_consumption1_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Non Billable Consumption 1"})



@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Charges & Implant Pending Indent Report")
def pharmacy_charges_and_implant_pending_indent_report(request):
    if request.method == 'GET':
        return render(request,'reports/pharmacy_charges_and_implant_pending_indent_report.html', {'user_name':request.user.username , "page_name" : "Pharmacy Charges & Implant Pending Indent Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        pharmacy_charges_and_implant_pending_indent_report_value,column_name = db.get_pharmacy_charges_and_implant_pending_indent_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pharmacy Charges & Implant Pending Indent Report",data=pharmacy_charges_and_implant_pending_indent_report_value,column=column_name)

        if not pharmacy_charges_and_implant_pending_indent_report_value:
            return render(request,'reports/pharmacy_charges_and_implant_pending_indent_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_charges_and_implant_pending_indent_report.html', {'pharmacy_charges_and_implant_pending_indent_report_value':pharmacy_charges_and_implant_pending_indent_report_value, 'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Direct Returns Sale Report")
def pharmacy_direct_returns_sale_report(request):
    if request.method == 'GET':
        return render(request,'reports/pharmacy_direct_returns_sale_report.html', {'user_name':request.user.username , "page_name" : "Pharmacy Direct Returns Sale Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        pharmacy_direct_returns_sale_report_value,column_name = db.get_pharmacy_direct_returns_sale_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pharmacy Direct Returns Sale Report",data=pharmacy_direct_returns_sale_report_value,column=column_name)

        if not pharmacy_direct_returns_sale_report_value:
            return render(request,'reports/pharmacy_direct_returns_sale_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_direct_returns_sale_report.html', {'pharmacy_direct_returns_sale_report_value':pharmacy_direct_returns_sale_report_value, 'user_name':request.user.username,'date_form' : DateForm()})





@login_required(login_url='login')
@allowed_users("Pharmacy - Current Inpatients Reports")
def current_inpatients_report(request):

    if request.method == 'GET':
        return render(request,'reports/current_inpatients_report.html', {'user_name':request.user.username, "page_name" : "Current Inpatients Reports"})
    
     
    elif request.method == 'POST':
        db = Ora()
        current_inpatients_report_value,column_name = db.get_current_inpatients_report()
        excel_file_path = excel_generator(page_name="Current Inpatients Reports",data=current_inpatients_report_value,column=column_name)

        if not current_inpatients_report_value:
            return render(request,'reports/current_inpatients_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/current_inpatients_report.html', {'current_inpatients_report_value':current_inpatients_report_value, 'user_name':request.user.username})



@login_required(login_url='login')
@allowed_users("Pharmacy - Consigned Item Detail Report")
def consigned_item_detail_report(request):
    if request.method == 'GET':
        return render(request,'reports/consigned_item_detail_report.html', {'user_name':request.user.username , "page_name" : "Consigned Item Detail Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        consigned_item_detail_report_value,column_name = db.get_consigned_item_detail_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Consigned Item Detail Report",data=consigned_item_detail_report_value,column=column_name)
        
        if not consigned_item_detail_report_value:
            return render(request,'reports/consigned_item_detail_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/consigned_item_detail_report.html', {'consigned_item_detail_report_value':consigned_item_detail_report_value, 'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users("Pharmacy - Schedule H1 Drug Report")
def schedule_h1_drug_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':

        return render(request,'reports/schedule_h1_drug_report.html', {
            'user_name':request.user.username , 
            "page_name" : "Schedule H1 Drug Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        # Select Function from model
        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/schedule_h1_drug_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        if  facility_code == "ALL":
            db = Ora()
            schedule_h1_drug_report_value,column_name = db.get_schedule_h1_drug_report_all(from_date, to_date)

        else: 
            db = Ora()
            schedule_h1_drug_report_value,column_name = db.get_schedule_h1_drug_report(facility_code,from_date, to_date)
        
        excel_file_path = excel_generator(page_name="Schedule H1 Drug Report",data=schedule_h1_drug_report_value,column=column_name)
        
        if not schedule_h1_drug_report_value:
            return render(request,'reports/schedule_h1_drug_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/schedule_h1_drug_report.html', {'schedule_h1_drug_report_value':schedule_h1_drug_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

    


@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Ward Return Requests with Status Report")
def pharmacy_ward_return_requests_with_status_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':

        

        return render(request,'reports/pharmacy_ward_return_requests_with_status_report.html', {
            'user_name':request.user.username , 
            "page_name" : "Pharmacy Ward Return Requests with Status Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        # Select Function from model
        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/pharmacy_ward_return_requests_with_status_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        

        db = Ora()
        pharmacy_ward_return_requests_with_status_report_value,column_name = db.get_pharmacy_ward_return_requests_with_status_report(facility_code,from_date, to_date)
        excel_file_path = excel_generator(page_name="Pharmacy Ward Return Requests with Status Report",data=pharmacy_ward_return_requests_with_status_report_value,column=column_name)
        
        if not pharmacy_ward_return_requests_with_status_report_value:
            return render(request,'reports/pharmacy_ward_return_requests_with_status_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_ward_return_requests_with_status_report.html', {'pharmacy_ward_return_requests_with_status_report_value':pharmacy_ward_return_requests_with_status_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Indent Deliver Summary Report")
def pharmacy_indent_deliver_summary_report(request):

    if request.method == 'GET':
        return render(request,'reports/pharmacy_indent_deliver_summary_report.html', {'user_name':request.user.username, "page_name" : "Pharmacy Indent Deliver Summary Report"})
    
     
    elif request.method == 'POST':
        db = Ora()
        pharmacy_indent_deliver_summary_report_value,column_name = db.get_pharmacy_indent_deliver_summary_report()
        excel_file_path = excel_generator(page_name="Pharmacy Indent Deliver Summary Report",data=pharmacy_indent_deliver_summary_report_value,column=column_name)

        if not pharmacy_indent_deliver_summary_report_value:
            return render(request,'reports/pharmacy_indent_deliver_summary_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_indent_deliver_summary_report.html', {'pharmacy_indent_deliver_summary_report_value':pharmacy_indent_deliver_summary_report_value, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users("Pharmacy - Intransites Stk Tfr Acknowledgement Pending Report")
def intransites_stk_tfr_acknowledgement_pending(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_stk_tfr_acknowledgement_pending.html', {'user_name':request.user.username, "page_name" : "Intransites Stk Tfr Acknowledgement Pending Report"})
    
     
    elif request.method == 'POST':
        db = Ora()
        intransites_stk_tfr_acknowledgement_pending_value,intransites_stk_tfr_acknowledgement_pending_column_name = db.get_intransites_stk_tfr_acknowledgement_pending()
        excel_file_path = excel_generator(page_name="Intransites Stk Tfr Acknowledgement Pending Report",data=intransites_stk_tfr_acknowledgement_pending_value,column=intransites_stk_tfr_acknowledgement_pending_column_name)

        if not intransites_stk_tfr_acknowledgement_pending_value:
            return render(request,'reports/intransites_stk_tfr_acknowledgement_pending.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_stk_tfr_acknowledgement_pending.html', {'intransites_stk_tfr_acknowledgement_pending_column_name':intransites_stk_tfr_acknowledgement_pending_column_name,'intransites_stk_tfr_acknowledgement_pending_value':intransites_stk_tfr_acknowledgement_pending_value, 'user_name':request.user.username,"page_name" : "Intransites Stk Tfr Acknowledgement Pending Report"})


@login_required(login_url='login')
@allowed_users('Pharmacy - Folley and Central Line')
def folley_and_central_line(request):

    if request.method == 'GET':
        return render(request,'reports/folley_and_central_line.html', {'user_name':request.user.username, "page_name" : "Folley and Central Line",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        folley_and_central_line_data, folley_and_central_line_column_name = db.get_folley_and_central_line(from_date,to_date)
        excel_file_path = excel_generator(page_name="Folley and Central Line",data=folley_and_central_line_data,column=folley_and_central_line_column_name)

        if not folley_and_central_line_data:
            return render(request,'reports/folley_and_central_line.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/folley_and_central_line.html', {'folley_and_central_line_data':folley_and_central_line_data, "folley_and_central_line_column_name":folley_and_central_line_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Folley and Central Line"})



@login_required(login_url='login')
@allowed_users('Pharmacy - Angiography Kit')
def angiography_kit(request):

    if request.method == 'GET':
        return render(request,'reports/angiography_kit.html', {'user_name':request.user.username, "page_name" : "Angiography Kit",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        angiography_kit_data, angiography_kit_column_name = db.get_angiography_kit(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pharmacy - Angiography Kit",data=angiography_kit_data,column=angiography_kit_column_name)

        if not angiography_kit_data:
            return render(request,'reports/angiography_kit.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/angiography_kit.html', {'angiography_kit_data':angiography_kit_data, "angiography_kit_column_name":angiography_kit_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Angiography Kit"})



@login_required(login_url='login')
@allowed_users("Pharmacy - New Admission Dispense Report")
def new_admission_dispense_report(request):

    if request.method == 'GET':
        return render(request,'reports/new_admission_dispense_report.html', {'user_name':request.user.username, "page_name" : "New Admission Dispense Report"})
    
     
    elif request.method == 'POST':
        db = Ora()
        new_admission_dispense_report_data,column_name = db.get_new_admission_dispense_report()
        excel_file_path = excel_generator(page_name="New Admission Dispense Report",data=new_admission_dispense_report_data,column=column_name)

        if not new_admission_dispense_report_data:
            return render(request,'reports/new_admission_dispense_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/new_admission_dispense_report.html', {'new_admission_dispense_report_data':new_admission_dispense_report_data, 'user_name':request.user.username})




@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy OP Sale Report Userwise")
def pharmacy_op_sale_report_userwise(request):
    if request.method == 'GET':
        return render(request,'reports/pharmacy_op_sale_report_userwise.html', {'user_name':request.user.username , "page_name" : "Pharmacy OP Sale Report Userwise", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        pharmacy_op_sale_report_userwise_value,column_name = db.get_pharmacy_op_sale_report_userwise(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pharmacy OP Sale Report Userwise",data=pharmacy_op_sale_report_userwise_value,column=column_name)
        
        if not pharmacy_op_sale_report_userwise_value:
            return render(request,'reports/pharmacy_op_sale_report_userwise.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_op_sale_report_userwise.html', {'pharmacy_op_sale_report_userwise_value':pharmacy_op_sale_report_userwise_value, 'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users("Pharmacy - Pharmacy Consumption Report")
def pharmacy_consumption_report(request):
    if request.method == 'GET':
        return render(request,'reports/pharmacy_consumption_report.html', {'user_name':request.user.username , "page_name" : "Pharmacy Consumption Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        pharmacy_consumption_report_value,column_name = db.get_pharmacy_consumption_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pharmacy Consumption Report",data=pharmacy_consumption_report_value,column=column_name)
        
        if not pharmacy_consumption_report_value:
            return render(request,'reports/pharmacy_consumption_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pharmacy_consumption_report.html', {'pharmacy_consumption_report_value':pharmacy_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users("Pharmacy - Food-Drug Interaction Report")
def food_drug_interaction_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/food_drug_interaction_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Food-Drug Interaction Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/food_drug_interaction_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        food_drug_interaction_report_value,column_name = db.get_food_drug_interaction_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Food-Drug Interaction Report",data=food_drug_interaction_report_value,column=column_name)
        
        if not food_drug_interaction_report_value:
            return render(request,'reports/food_drug_interaction_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/food_drug_interaction_report.html', {'food_drug_interaction_report_value':food_drug_interaction_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})




@login_required(login_url='login')
@allowed_users('Pharmacy - Intransite Stock')
def intransite_stock(request):

    if request.method == 'GET':
        return render(request,'reports/intransite_stock.html', {'user_name':request.user.username, "page_name" : "Intransite Stock"})
    
     
    elif request.method == 'POST':
        db = Ora()
        intransite_stock_data ,column_name = db.get_intransite_stock()
        excel_file_path = excel_generator(page_name="Intransite Stock",data=intransite_stock_data,column=column_name)

        if not intransite_stock_data:
            return render(request,'reports/intransite_stock.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransite_stock.html', {'intransite_stock_data':intransite_stock_data, 'user_name':request.user.username})
            

@login_required(login_url='login')
@allowed_users('Pharmacy - GRN Data')
def grn_data(request):
    if request.method == 'GET':
        return render(request,'reports/grn_data.html', {'user_name':request.user.username , "page_name" : "GRN Data", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        grn_data_value,column_name = db.get_grn_data(from_date,to_date)
        excel_file_path = excel_generator(page_name="GRN Data",data=grn_data_value,column=column_name)
        
        if not grn_data_value:
            return render(request,'reports/grn_data.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/grn_data.html', {'grn_data_value':grn_data_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Pharmacy - Drug Duplication Override Report')
def drug_duplication_override_report(request):
    if request.method == 'GET':
        return render(request,'reports/drug_duplication_override_report.html', {'user_name':request.user.username , "page_name" : "Drug Duplication Override Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        drug_duplication_override_report_value,column_name = db.get_drug_duplication_override_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Drug Duplication Override Report",data=drug_duplication_override_report_value,column=column_name)
        
        if not drug_duplication_override_report_value:
            return render(request,'reports/drug_duplication_override_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/drug_duplication_override_report.html', {'drug_duplication_override_report_value':drug_duplication_override_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Pharmacy - Drug Interaction Override Report')
def drug_interaction_override_report(request):
    if request.method == 'GET':
        return render(request,'reports/drug_interaction_override_report.html', {'user_name':request.user.username , "page_name" : "Drug Interaction Override Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        drug_interaction_override_report_value,column_name = db.get_drug_interaction_override_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Drug Interaction Override Report",data=drug_interaction_override_report_value,column=column_name)
        
        if not drug_interaction_override_report_value:
            return render(request,'reports/drug_interaction_override_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/drug_interaction_override_report.html', {'drug_interaction_override_report_value':drug_interaction_override_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Pharmacy - Sale Consumption Report')
def sale_consumption_report(request):
    if request.method == 'GET':
        return render(request,'reports/sale_consumption_report.html', {'user_name':request.user.username , "page_name" : "Sale Consumption Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        sale_consumption_report_value,column_name = db.get_sale_consumption_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Sale Consumption Report",data=sale_consumption_report_value,column=column_name)
        
        if not sale_consumption_report_value:
            return render(request,'reports/sale_consumption_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/sale_consumption_report.html', {'column_name':column_name,'sale_consumption_report_value':sale_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Pharmacy - Sale Consumption Report 1')
def sale_consumption_report1(request):
    if request.method == 'GET':
        return render(request,'reports/sale_consumption_report1.html', {'user_name':request.user.username , "page_name" : "Sale Consumption Report 1",})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        try :
            month = request.POST['month']
            year = request.POST['year']
        except MultiValueDictKeyError:
            return render(request,'reports/sale_consumption_report1.html', {'error':"😒 Please Enter a Month and a Year",'user_name':request.user.username,})

        
        
        db = Ora()
        sale_consumption_report1_value,column_name = db.get_sale_consumption_report1(month,year)
        excel_file_path = excel_generator(page_name="Sale Consumption Report 1",data=sale_consumption_report1_value,column=column_name)
        
        if not sale_consumption_report1_value:
            return render(request,'reports/sale_consumption_report1.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/sale_consumption_report1.html', {'column_name':column_name,'sale_consumption_report1_value':sale_consumption_report1_value, 'user_name':request.user.username,'date_form' : DateForm()})





@login_required(login_url='login')
@allowed_users('Pharmacy - Predischarge Medication')
def predischarge_medication(request):

    if request.method == 'GET':
        return render(request,'reports/predischarge_medication.html', {'user_name':request.user.username, "page_name" : "Predischarge Medication",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        predischarge_medication_data, predischarge_medication_column_name = db.get_predischarge_medication(from_date,to_date)
        excel_file_path = excel_generator(page_name="Predischarge Medication",data=predischarge_medication_data,column=predischarge_medication_column_name)

        if not predischarge_medication_data:
            return render(request,'reports/predischarge_medication.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/predischarge_medication.html', {'predischarge_medication_data':predischarge_medication_data, "predischarge_medication_column_name":predischarge_medication_column_name,'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users('Pharmacy - Predischarge Initiate')
def predischarge_initiate(request):

    if request.method == 'GET':
        return render(request,'reports/predischarge_initiate.html', {'user_name':request.user.username, "page_name" : "Predischarge Initiate"})
    
     
    elif request.method == 'POST':
        db = Ora()
        predischarge_initiate_data, predischarge_initiate_data_column_name = db.get_predischarge_initiate()
        excel_file_path = excel_generator(page_name="Predischarge Initiate",data=predischarge_initiate_data,column=predischarge_initiate_data_column_name)

        if not predischarge_initiate_data:
            return render(request,'reports/predischarge_initiate.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/predischarge_initiate.html', {'predischarge_initiate_data':predischarge_initiate_data,"predischarge_initiate_data_column_name":predischarge_initiate_data_column_name, 'user_name':request.user.username,"page_name" : "Predischarge Initiate"})
            


@login_required(login_url='login')
@allowed_users('Pharmacy - Intransites Unf Sal Ret')
def intransites_unf_sal_ret(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_unf_sal_ret.html', {'user_name':request.user.username, "page_name" : "Intransites Unf Sal Ret",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        intransites_unf_sal_ret_data, intransites_unf_sal_ret_column_name = db.get_intransites_unf_sal_ret(from_date,to_date)
        excel_file_path = excel_generator(page_name="Intransites Unf Sal Ret",data=intransites_unf_sal_ret_data,column=intransites_unf_sal_ret_column_name)

        if not intransites_unf_sal_ret_data:
            return render(request,'reports/intransites_unf_sal_ret.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_unf_sal_ret.html', {'intransites_unf_sal_ret_data':intransites_unf_sal_ret_data, "intransites_unf_sal_ret_column_name":intransites_unf_sal_ret_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Unf Sal Ret"})



@login_required(login_url='login')
@allowed_users('Pharmacy - Intransites Unf Stk Tfr')
def intransites_unf_stk_tfr(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_unf_stk_tfr.html', {'user_name':request.user.username, "page_name" : "Intransites Unf Stk Tfr",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db =  Ora()
        intransites_unf_stk_tfr_data, intransites_unf_stk_tfr_column_name = db.get_intransites_unf_stk_tfr(from_date,to_date)
        excel_file_path = excel_generator(page_name="Intransites Unf Stk Tfr",data=intransites_unf_stk_tfr_data,column=intransites_unf_stk_tfr_column_name)

        if not intransites_unf_stk_tfr_data:
            return render(request,'reports/intransites_unf_stk_tfr.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_unf_stk_tfr.html', {'intransites_unf_stk_tfr_data':intransites_unf_stk_tfr_data, "intransites_unf_stk_tfr_column_name":intransites_unf_stk_tfr_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Unf Stk Tfr"})




@login_required(login_url='login')
@allowed_users('Pharmacy - Intransites Acknowledgement Pending ISS')
def intransites_acknowledgement_pending_iss(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_acknowledgement_pending_iss.html', {'user_name':request.user.username, "page_name" : "Intransites Acknowledgement Pending ISS",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        db =  Ora()
        intransites_acknowledgement_pending_iss_data, intransites_acknowledgement_pending_iss_column_name = db.get_intransites_acknowledgement_pending_iss()
        excel_file_path = excel_generator(page_name="",data=intransites_acknowledgement_pending_iss_data,column=intransites_acknowledgement_pending_iss_column_name)

        if not intransites_acknowledgement_pending_iss_data:
            return render(request,'reports/intransites_acknowledgement_pending_iss.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_acknowledgement_pending_iss.html', {'intransites_acknowledgement_pending_iss_data':intransites_acknowledgement_pending_iss_data, "intransites_acknowledgement_pending_iss_column_name":intransites_acknowledgement_pending_iss_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Acknowledgement Pending ISS"})


@login_required(login_url='login')
@allowed_users('Pharmacy - Intransites Acknowledgement Pending ISS RT')
def intransites_acknowledgement_pending_iss_rt(request):

    if request.method == 'GET':
        return render(request,'reports/intransites_acknowledgement_pending_iss_rt.html', {'user_name':request.user.username, "page_name" : "Pharmacy - Intransites Acknowledgement Pending ISS RT",'date_form' : DateForm()})
    
     
    elif request.method == 'POST':
        db =  Ora()
        intransites_acknowledgement_pending_iss_rt_data, intransites_acknowledgement_pending_iss_rt_column_name = db.get_intransites_acknowledgement_pending_iss_rt()
        excel_file_path = excel_generator(page_name="Intransites Acknowledgement Pending ISS RT",data=intransites_acknowledgement_pending_iss_rt_data,column=intransites_acknowledgement_pending_iss_rt_column_name)

        if not intransites_acknowledgement_pending_iss_rt_data:
            return render(request,'reports/intransites_acknowledgement_pending_iss_rt.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/intransites_acknowledgement_pending_iss_rt.html', {'intransites_acknowledgement_pending_iss_rt_data':intransites_acknowledgement_pending_iss_rt_data, "intransites_acknowledgement_pending_iss_rt_column_name":intransites_acknowledgement_pending_iss_rt_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Pharmacy - Intransites Acknowledgement Pending ISS RT"})





#Finance Reports




@login_required(login_url='login')
@allowed_users("Finance - Credit Bill Outstanding")
def credit_outstanding_bill(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/credit_outstanding_bill.html', {
            'user_name':request.user.username, 
            "page_name" : "Credit Outstanding Bill", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/credit_outstanding_bill.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        credit_outstanding_bill_value,column_name = db.get_credit_outstanding_bill_value(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Credit Bill Outstanding",data=credit_outstanding_bill_value,column=column_name)
        
        if not credit_outstanding_bill_value:
            return render(request,'reports/credit_outstanding_bill.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/credit_outstanding_bill.html', {'credit_outstanding_bill_value':credit_outstanding_bill_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    

@login_required(login_url='login')
@allowed_users("Finance - TPA Letter")
def tpa_letter(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/tpa_letter.html', {
            'user_name':request.user.username, 
            "page_name" : "TPA Letter", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/tpa_letter.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        tpa_letter_value,column_name = db.get_tpa_letter(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="TPA Letter",data=tpa_letter_value,column=column_name)
        
        if not tpa_letter_value:
            return render(request,'reports/tpa_letter.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/tpa_letter.html', {'tpa_letter_value':tpa_letter_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    



@login_required(login_url='login')
@allowed_users("Finance - Online Consultation Report")
def online_consultation_report(request):
    if request.method == 'GET':
        return render(request,'reports/online_consultation_report.html', {'user_name':request.user.username , "page_name" : "Online Consultation Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        online_consultation_report_value,column_name = db.get_online_consultation_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Online Consultation Report",data=online_consultation_report_value,column=column_name)
        
        if not online_consultation_report_value:
            return render(request,'reports/online_consultation_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/online_consultation_report.html', {'online_consultation_report_value':online_consultation_report_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users('Finance - Contract Reports')
def contract_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/contract_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Contract Reports",
            'facilities' : facility,
            })
    
     
    elif request.method == 'POST':
        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/contract_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        contract_report_data,column_name = db.get_contract_report(facility_code)
        excel_file_path = excel_generator(page_name="Contract Reports",data=contract_report_data,column=column_name)

        if not contract_report_data:
            return render(request,'reports/contract_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'facilities' : facility})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/contract_report.html', {'contract_report_data':contract_report_data, 'user_name':request.user.username,'facilities' : facility})
            

@login_required(login_url='login')
@allowed_users('Clinical Administration - Current Inpatients Employee and Dependants')
def current_inpatients_employee_and_dependants(request):
    if request.method == 'GET':
        return render(request,'reports/current_inpatients_employee_and_dependants.html', {'user_name':request.user.username , "page_name" : "Current Inpatients Employee and Dependants", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        current_inpatients_employee_and_dependants_value,column_name = db.get_current_inpatients_employee_and_dependants(from_date,to_date)
        excel_file_path = excel_generator(page_name="Current Inpatients Employee and Dependants",data=current_inpatients_employee_and_dependants_value,column=column_name)
        
        if not current_inpatients_employee_and_dependants_value:
            return render(request,'reports/current_inpatients_employee_and_dependants.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/current_inpatients_employee_and_dependants.html', {'current_inpatients_employee_and_dependants_value':current_inpatients_employee_and_dependants_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users('Clinical Administration - Treatment Sheet Data')
def treatment_sheet_data(request):

    if request.method == 'GET':
        return render(request,'reports/treatment_sheet_data.html', {'user_name':request.user.username, "page_name" : "Treatment Sheet Data"})
    
     
    elif request.method == 'POST':
        db = Ora()
        treatment_sheet_data_data,column_name = db.get_treatment_sheet_data()
        excel_file_path = excel_generator(page_name="Treatment Sheet Data",data=treatment_sheet_data_data,column=column_name)

        if not treatment_sheet_data_data:
            return render(request,'reports/treatment_sheet_data.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/package_contract_report.html', {'column_name':column_name,'treatment_sheet_data_data':treatment_sheet_data_data, 'user_name':request.user.username,})


@login_required(login_url='login')
@allowed_users("Finance - Package Contract Report")
def package_contract_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/package_contract_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Package Contract Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/package_contract_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        package_contract_report_value,column_name = db.get_package_contract_report(from_date,to_date,facility_code)
        excel_file_path = excel_generator(page_name="Package Contract Report",data=package_contract_report_value,column=column_name)
        
        if not package_contract_report_value:
            return render(request,'reports/package_contract_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/package_contract_report.html', {'package_contract_report_value':package_contract_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    



@login_required(login_url='login')
@allowed_users("Finance - Credit Card Reconciliation Report")
def credit_card_reconciliation_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/credit_card_reconciliation_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Credit Card Reconciliation Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/credit_card_reconciliation_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        credit_card_reconciliation_report_value,column_name = db.get_credit_card_reconciliation_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Credit Card Reconciliation Report",data=credit_card_reconciliation_report_value,column=column_name)
        
        if not credit_card_reconciliation_report_value:
            return render(request,'reports/credit_card_reconciliation_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/credit_card_reconciliation_report.html', {'credit_card_reconciliation_report_value':credit_card_reconciliation_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    



@login_required(login_url='login')
@allowed_users("Finance - Covid OT Surgery Details")
def covid_ot_surgery_details(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/covid_ot_surgery_details.html', {
            'user_name':request.user.username, 
            "page_name" : "Covid OT Surgery Details", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/covid_ot_surgery_details.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        covid_ot_surgery_details_value,column_name = db.get_covid_ot_surgery_details(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Covid OT Surgery Details",data=covid_ot_surgery_details_value,column=column_name)
        
        if not covid_ot_surgery_details_value:
            return render(request,'reports/covid_ot_surgery_details.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/covid_ot_surgery_details.html', {'covid_ot_surgery_details_value':covid_ot_surgery_details_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    


@login_required(login_url='login')
@allowed_users('Finance - GST Data of Pharmacy')
def gst_data_of_pharmacy(request):

    if request.method == 'GET':
        return render(request,'reports/gst_data_of_pharmacy.html', {'user_name':request.user.username, "page_name" : "GST Data of Pharmacy"})
    
     
    elif request.method == 'POST':
        db = Ora()
        gst_data_of_pharmacy_data,column_name = db.get_gst_data_of_pharmacy()
        excel_file_path = excel_generator(page_name="GST Data of Pharmacy",data=gst_data_of_pharmacy_data,column=column_name)

        if not gst_data_of_pharmacy_data:
            return render(request,'reports/gst_data_of_pharmacy.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/gst_data_of_pharmacy.html', {'gst_data_of_pharmacy_data':gst_data_of_pharmacy_data, 'user_name':request.user.username})
            
    


@login_required(login_url='login')
@allowed_users('Finance - GST Data of Pharmacy Return')
def gst_data_of_pharmacy_return(request):

    if request.method == 'GET':
        return render(request,'reports/gst_data_of_pharmacy_return.html', {'user_name':request.user.username, "page_name" : "GST Data of Pharmacy"})
    
     
    elif request.method == 'POST':
        db = Ora()
        gst_data_of_pharmacy_return_data,column_name = db.get_gst_data_of_pharmacy_return()
        excel_file_path = excel_generator(page_name="GST Data of Pharmacy Return",data=gst_data_of_pharmacy_return_data,column=column_name)

        if not gst_data_of_pharmacy_return_data:
            return render(request,'reports/gst_data_of_pharmacy_return.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/gst_data_of_pharmacy_return.html', {'gst_data_of_pharmacy_return_data':gst_data_of_pharmacy_return_data, 'user_name':request.user.username})
            
    


@login_required(login_url='login')
@allowed_users('Finance - GST Data of IP')
def gst_data_of_ip(request):

    if request.method == 'GET':
        return render(request,'reports/gst_data_of_ip.html', {'user_name':request.user.username, "page_name" : "GST Data of IP"})
    
     
    elif request.method == 'POST':
        db = Ora()
        gst_data_of_ip_data,column_name = db.get_gst_data_of_ip()
        excel_file_path = excel_generator(page_name="GST Data of IP",data=gst_data_of_ip_data,column=column_name)

        if not gst_data_of_ip_data:
            return render(request,'reports/gst_data_of_ip.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/gst_data_of_ip.html', {'gst_data_of_ip_data':gst_data_of_ip_data, 'user_name':request.user.username})
            


@login_required(login_url='login')
@allowed_users('Finance - GST Data of OP')
def gst_data_of_op(request):

    if request.method == 'GET':
        return render(request,'reports/gst_data_of_op.html', {'user_name':request.user.username, "page_name" : "GST Data of OP"})
    
     
    elif request.method == 'POST':
        db = Ora()
        gst_data_of_op_data,column_name = db.get_gst_data_of_op()
        excel_file_path = excel_generator(page_name="GST Data of OP",data=gst_data_of_op_data,column=column_name)

        if not gst_data_of_op_data:
            return render(request,'reports/gst_data_of_op.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/gst_data_of_op.html', {'gst_data_of_op_data':gst_data_of_op_data, 'user_name':request.user.username})
            

@login_required(login_url='login')
@allowed_users('Finance - Revenue Data of SL')
def revenue_data_of_sl(request):

    if request.method == 'GET':
        return render(request,'reports/revenue_data_of_sl.html', {'user_name':request.user.username, "page_name" : "Revenue Data of SL"})
    
     
    elif request.method == 'POST':
        db = Ora()
        revenue_data_of_sl_data,column_name = db.get_revenue_data_of_sl()
        excel_file_path = excel_generator(page_name="Revenue Data of SL",data=revenue_data_of_sl_data,column=column_name)

        if not revenue_data_of_sl_data:
            return render(request,'reports/revenue_data_of_sl.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/revenue_data_of_sl.html', {'revenue_data_of_sl_data':revenue_data_of_sl_data, 'user_name':request.user.username})
            


@login_required(login_url='login')
@allowed_users('Finance - Revenue Data of SL 1')
def revenue_data_of_sl1(request):

    if request.method == 'GET':
        return render(request,'reports/revenue_data_of_sl1.html', {'user_name':request.user.username, "page_name" : "Revenue Data of SL 1"})
    
     
    elif request.method == 'POST':
        db = Ora()
        revenue_data_of_sl1_data,column_name = db.get_revenue_data_of_sl1()
        excel_file_path = excel_generator(page_name="Revenue Data of SL 1",data=revenue_data_of_sl1_data,column=column_name)

        if not revenue_data_of_sl1_data:
            return render(request,'reports/revenue_data_of_sl1.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/revenue_data_of_sl1.html', {'revenue_data_of_sl1_data':revenue_data_of_sl1_data, 'user_name':request.user.username})




@login_required(login_url='login')
@allowed_users('Finance - Revenue Data of SL 2')
def revenue_data_of_sl2(request):

    if request.method == 'GET':
        return render(request,'reports/revenue_data_of_sl2.html', {'user_name':request.user.username, "page_name" : "Revenue Data of SL 2"})
    
     
    elif request.method == 'POST':
        db = Ora()
        revenue_data_of_sl2_data,column_name = db.get_revenue_data_of_sl2()
        excel_file_path = excel_generator(page_name="Revenue Data of SL 2",data=revenue_data_of_sl2_data,column=column_name)

        if not revenue_data_of_sl2_data:
            return render(request,'reports/revenue_data_of_sl2.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/revenue_data_of_sl2.html', {'revenue_data_of_sl2_data':revenue_data_of_sl2_data, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users("Finance - Revenue Data of SL 3")
def revenue_data_of_sl3(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/revenue_data_of_sl3.html', {
            'user_name':request.user.username, 
            "page_name" : "Revenue Data of SL 3", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        user = request.user.username
        
       

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/revenue_data_of_sl3.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        restricted = ("KH","RH", "ALL")
        if user=="51005374" and (facility_code in restricted):
            return render(request,'reports/revenue_data_of_sl3.html', {'error':"You are not Authorized to view this Facility! Please select a different Facility.", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        
        db = Ora()
        revenue_data_of_sl3_value,column_name = db.get_revenue_data_of_sl3(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Revenue Data of SL 3",data=revenue_data_of_sl3_value,column=column_name)
        
        if not revenue_data_of_sl3_value:
            return render(request,'reports/revenue_data_of_sl3.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/revenue_data_of_sl3.html', {'revenue_data_of_sl3_value':revenue_data_of_sl3_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})



@login_required(login_url='login')
@allowed_users("Clinical Administration - Pre Discharge Report")
def pre_discharge_report(request):
    if request.method == 'GET':
        return render(request,'reports/pre_discharge_report.html', {'user_name':request.user.username , "page_name" : "Pre Discharge Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])

        
        db = Ora()
        pre_discharge_report_value,column_name = db.get_pre_discharge_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Pre Discharge Report",data=pre_discharge_report_value,column=column_name)
        
        if not pre_discharge_report_value:
            return render(request,'reports/pre_discharge_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pre_discharge_report.html', {'pre_discharge_report_value':pre_discharge_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Clinical Administration - Pre Discharge Report 2')
def pre_discharge_report_2(request):

    if request.method == 'GET':
        return render(request,'reports/pre_discharge_report_2.html', {'user_name':request.user.username, "page_name" : "Pre Discharge Report 2"})
    
     
    elif request.method == 'POST':
        db = Ora()
        pre_discharge_report_2_data,column_name = db.get_pre_discharge_report_2()
        excel_file_path = excel_generator(page_name="Pre Discharge Report 2",data=pre_discharge_report_2_data,column=column_name)

        if not pre_discharge_report_2_data:
            return render(request,'reports/pre_discharge_report_2.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/pre_discharge_report_2.html', {'column_name':column_name,'pre_discharge_report_2_data':pre_discharge_report_2_data, 'user_name':request.user.username,})




@login_required(login_url='login')
@allowed_users("Clinical Administration - Discharge Report 2")
def discharge_report_2(request):
    if request.method == 'GET':
        return render(request,'reports/discharge_report_2.html', {'user_name':request.user.username , "page_name" : "Discharge Report 2", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])

        
        db = Ora()
        discharge_report_2_value,column_name = db.get_discharge_report_2(from_date,to_date)
        excel_file_path = excel_generator(page_name="Discharge Report 2",data=discharge_report_2_value,column=column_name)
        
        if not discharge_report_2_value:
            return render(request,'reports/discharge_report_2.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/discharge_report_2.html', {'discharge_report_2_value':discharge_report_2_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users("Clinical Administration - Discharge With MIS Report")
def discharge_with_mis_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/discharge_with_mis_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Discharge With MIS Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/discharge_with_mis_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        discharge_with_mis_report_value,column_name = db.get_discharge_with_mis_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Discharge With MIS Report",data=discharge_with_mis_report_value,column=column_name)
        
        if not discharge_with_mis_report_value:
            return render(request,'reports/discharge_with_mis_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/discharge_with_mis_report.html', {'discharge_with_mis_report_value':discharge_with_mis_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Clinical Administration - Needle Prick Injury Report")
def needle_prick_injury_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/needle_prick_injury_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Needle Prick Injury Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/needle_prick_injury_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        needle_prick_injury_report_value,column_name = db.get_needle_prick_injury_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Needle Prick Injury Report",data=needle_prick_injury_report_value,column=column_name)
        
        if not needle_prick_injury_report_value:
            return render(request,'reports/needle_prick_injury_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/needle_prick_injury_report.html', {'needle_prick_injury_report_value':needle_prick_injury_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    


@login_required(login_url='login')
@allowed_users("Clinical Administration - Practo Report")
def practo_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/practo_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Practo Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/practo_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        practo_report_value,column_name = db.get_practo_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Practo Report",data=practo_report_value,column=column_name)
        
        if not practo_report_value:
            return render(request,'reports/practo_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/practo_report.html', {'practo_report_value':practo_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})






@login_required(login_url='login')
@allowed_users('Clinical Administration - Unbilled Report')
def unbilled_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/unbilled_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Unbilled Report",
            'facilities' : facility,
            })
    
     
    elif request.method == 'POST':
        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/unbilled_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        unbilled_report_data,column_name = db.get_unbilled_report(facility_code)
        excel_file_path = excel_generator(page_name="Unbilled Report",data=unbilled_report_data,column=column_name)

        if not unbilled_report_data:
            return render(request,'reports/unbilled_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'facilities' : facility})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/unbilled_report.html', {'unbilled_report_data':unbilled_report_data, 'user_name':request.user.username,'facilities' : facility})
            


@login_required(login_url='login')
@allowed_users('Clinical Administration - Unbilled Deposit Report')
def unbilled_deposit_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/unbilled_deposit_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Unbilled Deposit Report",
            'facilities' : facility,
            })
    
     
    elif request.method == 'POST':
        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/unbilled_deposit_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        unbilled_deposit_report_data,column_name = db.get_unbilled_deposit_report(facility_code)
        excel_file_path = excel_generator(page_name="Unbilled Deposit Report",data=unbilled_deposit_report_data,column=column_name)

        if not unbilled_deposit_report_data:
            return render(request,'reports/unbilled_deposit_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'facilities' : facility})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/unbilled_deposit_report.html', {'unbilled_deposit_report_data':unbilled_deposit_report_data, 'user_name':request.user.username,'facilities' : facility})




@login_required(login_url='login')
@allowed_users("Clinical Administration - Contact Report")
def contact_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/contact_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Contact Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/contact_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        contact_report_value,column_name = db.get_contact_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Contact Report",data=contact_report_value,column=column_name)
        
        if not contact_report_value:
            return render(request,'reports/contact_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/contact_report.html', {'contact_report_value':contact_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Clinical Administration - Employees Antibodies Reactive Report")
def employees_antibodies_reactive_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/employees_antibodies_reactive_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Employees Antibodies Reactive Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/employees_antibodies_reactive_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        employees_antibodies_reactive_report_value, column_name = db.get_employees_antibodies_reactive_report(from_date,to_date,facility_code)
        excel_file_path = excel_generator(page_name="Employees Antibodies Reactive Report",data=employees_antibodies_reactive_report_value,column=column_name)
        
        if not employees_antibodies_reactive_report_value:
            return render(request,'reports/employees_antibodies_reactive_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/employees_antibodies_reactive_report.html', {'employees_antibodies_reactive_report_value':employees_antibodies_reactive_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users('Clinical Administration - Employee Reactive and Non PCR Report')
def employees_reactive_and_non_pcr_report(request):

    if request.method == 'GET':
        return render(request,'reports/employees_reactive_and_non_pcr_report.html', {'user_name':request.user.username, "page_name" : "Employee Reactive and Non PCR Report"})

    
    elif request.method == 'POST':
        db = Ora()
        employees_reactive_and_non_pcr_report_value,column_name = db.get_employees_reactive_and_non_pcr_report()
        excel_file_path = excel_generator(page_name="Employee Reactive and Non PCR Report",data=employees_reactive_and_non_pcr_report_value,column=column_name)

        if not employees_reactive_and_non_pcr_report_value:
            return render(request,'reports/employees_reactive_and_non_pcr_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/employees_reactive_and_non_pcr_report.html', {'employees_reactive_and_non_pcr_report_value':employees_reactive_and_non_pcr_report_value, 'user_name':request.user.username})
        

@login_required(login_url='login')
@allowed_users("Clinical Administration - Employee Covid Test Report")
def employee_covid_test_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/employee_covid_test_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Employee Covid Test Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/employee_covid_test_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        employee_covid_test_report_value, column_name = db.get_employee_covid_test_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Employee Covid Test Report",data=employee_covid_test_report_value,column=column_name)
        
        if not employee_covid_test_report_value:
            return render(request,'reports/employee_covid_test_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/employee_covid_test_report.html', {'employee_covid_test_report_value':employee_covid_test_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users('Clinical Administration - Bed Location Report')
def bed_location_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/bed_location_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Bed Location Report",
            'facilities' : facility,
            })
    
     
    elif request.method == 'POST':
        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/bed_location_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        bed_location_report_data, column_name = db.get_bed_location_report(facility_code)
        excel_file_path = excel_generator(page_name="Bed Location Report",data=bed_location_report_data,column=column_name)

        if not bed_location_report_data:
            return render(request,'reports/bed_location_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'facilities' : facility})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/bed_location_report.html', {'bed_location_report_data':bed_location_report_data, 'user_name':request.user.username,'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Clinical Administration - Home Visit Report")
def home_visit_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/home_visit_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Home Visit Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/home_visit_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        home_visit_report_value, column_name = db.get_home_visit_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Home Visit Report",data=home_visit_report_value,column=column_name)
        
        if not home_visit_report_value:
            return render(request,'reports/home_visit_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/home_visit_report.html', {'home_visit_report_value':home_visit_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users('Clinical Administration - CCO Billing Count Report')
def cco_billing_count_report(request):
    

    if request.method == 'GET':
        return render(request,'reports/cco_billing_count_report.html', {'user_name':request.user.username, "page_name" : "CCO Billing Count Report", 'date_form' : DateForm()})

    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        db = Ora()
        cco_billing_count_report_data, cco_billing_count_report_column_name= db.get_cco_billing_count_reports(from_date)
        excel_file_path = excel_generator(page_name="CCO Billing Count Report",data=cco_billing_count_report_data,column=cco_billing_count_report_column_name)

        if not cco_billing_count_report_data:
            return render(request,'reports/cco_billing_count_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/cco_billing_count_report.html', {'cco_billing_count_report_data':cco_billing_count_report_data,"cco_billing_count_report_column_name":cco_billing_count_report_column_name, 'user_name':request.user.username,'date_form' : DateForm()})
    

@login_required(login_url='login')
@allowed_users("Clinical Administration - Total Number of Online Consultation by Doctors")
def total_number_of_online_consultation_by_doctors(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/total_number_of_online_consultation_by_doctors.html', {
            'user_name':request.user.username, 
            "page_name" : "Total Number of Online Consultation by Doctors", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })



    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/total_number_of_online_consultation_by_doctors.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        total_number_of_online_consultation_by_doctors_value, column_name = db.get_total_number_of_online_consultation_by_doctors(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Total Number of Online Consultation by Doctors",data=total_number_of_online_consultation_by_doctors_value,column=column_name)
        
        if not total_number_of_online_consultation_by_doctors_value:
            return render(request,'reports/total_number_of_online_consultation_by_doctors.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/total_number_of_online_consultation_by_doctors.html', {'total_number_of_online_consultation_by_doctors_value':total_number_of_online_consultation_by_doctors_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users('Clinical Administration - Total Number of IP Patients by Doctors')
def total_number_of_ip_patients_by_doctors(request):
    if request.method == 'GET':
        return render(request,'reports/total_number_of_ip_patients_by_doctors.html', {'user_name':request.user.username , "page_name" : "Total Number of IP Patients by Doctors", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        total_number_of_ip_patients_by_doctors_value, column_name = db.get_total_number_of_ip_patients_by_doctors(from_date,to_date)
        excel_file_path = excel_generator(page_name="Total Number of IP Patients by Doctors",data=total_number_of_ip_patients_by_doctors_value,column=column_name)
        
        if not total_number_of_ip_patients_by_doctors_value:
            return render(request,'reports/total_number_of_ip_patients_by_doctors.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/total_number_of_ip_patients_by_doctors.html', {'total_number_of_ip_patients_by_doctors_value':total_number_of_ip_patients_by_doctors_value, 'user_name':request.user.username,'date_form' : DateForm()})
    


@login_required(login_url='login')
@allowed_users('Clinical Administration - Total Number of OP Patients by Doctors')
def total_number_of_op_patients_by_doctors(request):
    if request.method == 'GET':
        return render(request,'reports/total_number_of_op_patients_by_doctors.html', {'user_name':request.user.username , "page_name" : "Total Number of OP Patients by Doctors", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        total_number_of_op_patients_by_doctors_value, column_name = db.get_total_number_of_op_patients_by_doctors(from_date,to_date)
        excel_file_path = excel_generator(page_name="Total Number of OP Patients by Doctors",data=total_number_of_op_patients_by_doctors_value,column=column_name)
        
        if not total_number_of_op_patients_by_doctors_value:
            return render(request,'reports/total_number_of_op_patients_by_doctors.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/total_number_of_op_patients_by_doctors.html', {'total_number_of_op_patients_by_doctors_value':total_number_of_op_patients_by_doctors_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users("Clinical Administration - OPD Changes Report")
def opd_changes_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/opd_changes_report.html', {
            'user_name':request.user.username, 
            "page_name" : "OPD Changes Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })


    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/opd_changes_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        opd_changes_report_value, column_name = db.get_opd_changes_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="OPD Changes Report",data=opd_changes_report_value,column=column_name)
        
        if not opd_changes_report_value:
            return render(request,'reports/opd_changes_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/opd_changes_report.html', {'opd_changes_report_value':opd_changes_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    
    
@login_required(login_url='login')
@allowed_users("Clinical Administration - EHC Conversion Report")
def ehc_conversion_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/ehc_conversion_report.html', {
            'user_name':request.user.username, 
            "page_name" : "EHC Conversion Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })


    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/ehc_conversion_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        ehc_conversion_report_value, column_name = db.get_ehc_conversion_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="EHC Conversion Report",data=ehc_conversion_report_value,column=column_name)
        
        if not ehc_conversion_report_value:
            return render(request,'reports/ehc_conversion_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/ehc_conversion_report.html', {'ehc_conversion_report_value':ehc_conversion_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    



@login_required(login_url='login')
@allowed_users("Clinical Administration - EHC Package Range Report")
def ehc_package_range_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/ehc_package_range_report.html', {
            'user_name':request.user.username, 
            "page_name" : "EHC Package Range Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })


    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/ehc_package_range_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        db = Ora()
        ehc_package_range_report_value, column_name = db.get_ehc_package_range_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="EHC Package Range Report",data=ehc_package_range_report_value,column=column_name)
        
        if not ehc_package_range_report_value:
            return render(request,'reports/ehc_package_range_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/ehc_package_range_report.html', {'ehc_package_range_report_value':ehc_package_range_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
    



@login_required(login_url='login')
@allowed_users('Clinical Administration - Error Report')
def error_report(request):
    if request.method == 'GET':
        return render(request,'reports/error_report.html', {'user_name':request.user.username , "page_name" : "Error Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        error_report_value, column_name = db.get_error_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Error Report",data=error_report_value,column=column_name)
        
        if not error_report_value:
            return render(request,'reports/error_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/error_report.html', {'error_report_value':error_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Clinical Administration - OT Query Report')
def ot_query_report(request):
    if request.method == 'GET':
        return render(request,'reports/ot_query_report.html', {'user_name':request.user.username , "page_name" : "OT Query Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        ot_query_report_value, column_name = db.get_ot_query_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="OT Query Report",data=ot_query_report_value,column=column_name)
        
        if not ot_query_report_value:
            return render(request,'reports/ot_query_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/ot_query_report.html', {'ot_query_report_value':ot_query_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Clinical Administration - Outreach Cancer Hospital')
def outreach_cancer_hospital(request):
    page_name = "Outreach Cancer Hospital"
    if request.method == 'GET':
        
        return render(request,'reports/outreach_cancer_hospital.html', {'user_name':request.user.username , "page_name" : page_name, 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        outreach_cancer_hospital_value, column_name = db.get_outreach_cancer_hospital(from_date,to_date)
        excel_file_path = excel_generator(page_name=page_name,data=outreach_cancer_hospital_value,column=column_name)
        
        if not outreach_cancer_hospital_value:
            return render(request,'reports/outreach_cancer_hospital.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/outreach_cancer_hospital.html', {'column_name':column_name,ot_query_report_value':ot_query_report_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users('Clinical Administration - GIPSA Report')
def gipsa_report(request):

    if request.method == 'GET':
        return render(request,'reports/gipsa_report.html', {'user_name':request.user.username, "page_name" : "GIPSA Report"})
    
     
    elif request.method == 'POST':
        db = Ora()
        gipsa_report_data, column_name = db.get_gipsa_report()
        excel_file_path = excel_generator(page_name="GIPSA Report",data=gipsa_report_data,column=column_name)

        if not gipsa_report_data:
            return render(request,'reports/gipsa_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/gipsa_report.html', {'gipsa_report_data':gipsa_report_data, 'user_name':request.user.username})
            
    

@login_required(login_url='login')
@allowed_users('Clinical Administration - Precision Patient OPD & Online Consultation List Report')
def precision_patient_opd_and_online_consultation_list_report(request):
    if request.method == 'GET':
        return render(request,'reports/precision_patient_opd_and_online_consultation_list_report.html', {'user_name':request.user.username , "page_name" : "Precision Patient OPD & Online Consultation List Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        precision_patient_opd_and_online_consultation_list_report_value, column_name = db.get_precision_patient_opd_and_online_consultation_list_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Precision Patient OPD & Online Consultation List Report",data=precision_patient_opd_and_online_consultation_list_report_value,column=column_name)
        
        if not precision_patient_opd_and_online_consultation_list_report_value:
            return render(request,'reports/precision_patient_opd_and_online_consultation_list_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/precision_patient_opd_and_online_consultation_list_report.html', {'precision_patient_opd_and_online_consultation_list_report_value':precision_patient_opd_and_online_consultation_list_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Clinical Administration - Appointment Details By Call Center Report')
def appointment_details_by_call_center_report(request):
    if request.method == 'GET':
        return render(request,'reports/appointment_details_by_call_center_report.html', {'user_name':request.user.username , "page_name" : "Appointment Details By Call Center Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        appointment_details_by_call_center_report_value, column_name = db.get_appointment_details_by_call_center_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Appointment Details By Call Center Report",data=appointment_details_by_call_center_report_value,column=column_name)
        
        if not appointment_details_by_call_center_report_value:
            return render(request,'reports/appointment_details_by_call_center_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/appointment_details_by_call_center_report.html', {'appointment_details_by_call_center_report_value':appointment_details_by_call_center_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Clinical Administration - TRF Report')
def trf_report(request):
    if request.method == 'GET':
        return render(request,'reports/trf_report.html', {'user_name':request.user.username , "page_name" : "TRF Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        trf_report_value, column_name = db.get_trf_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="TRF Report",data=trf_report_value,column=column_name)
        
        if not trf_report_value:
            return render(request,'reports/trf_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/trf_report.html', {'trf_report_value':trf_report_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users('Clinical Administration - Current Inpatients(Clinical Admin)')
def current_inpatients_clinical_admin(request):

    if request.method == 'GET':
        return render(request,'reports/current_inpatients_clinical_admin.html', {'user_name':request.user.username, "page_name" : "Current Inpatients(Clinical Admin)"})
    
     
    elif request.method == 'POST':
        db =  Ora()
        current_inpatients_clinical_admin_data, column_name = db.get_current_inpatients_clinical_admin()
        excel_file_path = excel_generator(page_name="Current Inpatients(Clinical Admin",data=current_inpatients_clinical_admin_data,column=column_name)

        if not current_inpatients_clinical_admin_data:
            return render(request,'reports/current_inpatients_clinical_admin.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/current_inpatients_clinical_admin.html', {'current_inpatients_clinical_admin_data':current_inpatients_clinical_admin_data, 'user_name':request.user.username})
            
@login_required(login_url='login')
@allowed_users('Clinical Administration - Check Patient Registration Date')
def check_patient_registration_date(request):

    if request.method == 'GET':
        return render(request,'reports/check_patient_registration_date.html', {'user_name':request.user.username, "page_name" : "Check Patient Registration Date"})
    
     
    elif request.method == 'POST':
        uhid = request.POST['uhid'].upper()
        db =  Ora()
        check_patient_registration_date_data, column_name = db.get_check_patient_registration_date(uhid)
        excel_file_path = excel_generator(page_name="Check Patient Registration Date",data=check_patient_registration_date_data,column=column_name)

        if not check_patient_registration_date_data:
            return render(request,'reports/check_patient_registration_date.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/check_patient_registration_date.html', {'check_patient_registration_date_data':check_patient_registration_date_data, 'user_name':request.user.username})
            

@login_required(login_url='login')
@allowed_users('Clinical Administration - Patient Registration Report')
def patient_registration_report(request):
    if request.method == 'GET':
        return render(request,'reports/patient_registration_report.html', {'user_name':request.user.username , "page_name" : "Patient Registration Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        patient_registration_report_value, column_name = db.get_patient_registration_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Patient Registration Report",data=patient_registration_report_value,column=column_name)
        
        if not patient_registration_report_value:
            return render(request,'reports/patient_registration_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/patient_registration_report.html', {'patient_registration_report_value':patient_registration_report_value, 'user_name':request.user.username,'date_form' : DateForm()})






# Lab

@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - Lab - Covid PCR")
def covid_pcr(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/covid_pcr.html', {
            'user_name':request.user.username, 
            "page_name" : "Covid PCR", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/covid_pcr.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        covid_pcr_value, column_name = db.get_covid_pcr(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Covid PCR",data=covid_pcr_value,column=column_name)
        
        if not covid_pcr_value:
            return render(request,'reports/covid_pcr.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/covid_pcr.html', {'covid_pcr_value':covid_pcr_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})



@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Lab - Covid 2')
def covid_2(request):
    if request.method == 'GET':
        return render(request,'reports/covid_2.html', {'user_name':request.user.username , "page_name" : "Covid 2", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        covid_2_value,column_name = db.get_covid_2(from_date,to_date)
        excel_file_path = excel_generator(page_name="Covid 2",data=covid_2_value,column=column_name)
        
        if not covid_2_value:
            return render(request,'reports/covid_2.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/covid_2.html', {'covid_2_value':covid_2_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - Lab - Covid Antibodies")
def covid_antibodies(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/covid_antibodies.html', {
            'user_name':request.user.username, 
            "page_name" : "Covid Antibodies", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/covid_antibodies.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        covid_antibodies_value, column_name = db.get_covid_antibodies(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Covid Antibodies",data=covid_antibodies_value,column=column_name)
        
        if not covid_antibodies_value:
            return render(request,'reports/covid_antibodies.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/covid_antibodies.html', {'covid_antibodies_value':covid_antibodies_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Clinical Administration - Covid Antigen")
def covid_antigen(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/covid_antigen.html', {
            'user_name':request.user.username, 
            "page_name" : "Covid Antigen", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/covid_antigen.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        covid_antigen_value, column_name = db.get_covid_antigen(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Covid Antigen",data=covid_antigen_value,column=column_name)
        
        if not covid_antigen_value:
            return render(request,'reports/covid_antigen.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/covid_antigen.html', {'covid_antigen_value':covid_antigen_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - Lab - CBNAAT Test Data")
def cbnaat_test_data(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/cbnaat_test_data.html', {
            'user_name':request.user.username, 
            "page_name" : "CBNAAT Test Data", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/cbnaat_test_data.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        cbnaat_test_data_value, column_name = db.get_cbnaat_test_data(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="CBNAAT Test Data",data=cbnaat_test_data_value,column=column_name)
        
        if not cbnaat_test_data_value:
            return render(request,'reports/cbnaat_test_data.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/cbnaat_test_data.html', {'cbnaat_test_data_value':cbnaat_test_data_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})



@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - Lab - LAB TAT Report")
def lab_tat_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/lab_tat_report.html', {
            'user_name':request.user.username, 
            "page_name" : "LAB TAT Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        

        try :
            facility_code = request.POST['facility_dropdown']
            dept_name = request.POST['department_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/lab_tat_report.html', {'error':"😒 Please select a facility and the department name from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        lab_tat_report_value, column_name = db.get_lab_tat_report(facility_code,from_date,to_date,dept_name)
        excel_file_path = excel_generator(page_name="LAB TAT Report",data=lab_tat_report_value,column=column_name)
        
        if not lab_tat_report_value:
            return render(request,'reports/lab_tat_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/lab_tat_report.html', {'lab_tat_report_value':lab_tat_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - Lab - Histopath Fixation Data")
def histopath_fixation_data(request):
    if request.method == 'GET':
        return render(request,'reports/histopath_fixation_data.html', {'user_name':request.user.username , "page_name" : "Histopath Fixation Data", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        year_input = request.POST['year_input']
        
        db = Ora()
        histopath_fixation_data_value, column_name = db.get_histopath_fixation_data(year_input,from_date,to_date)
        excel_file_path = excel_generator(page_name="Histopath Fixation Data",data=histopath_fixation_data_value,column=column_name)
        
        if not histopath_fixation_data_value:
            return render(request,'reports/histopath_fixation_data.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/histopath_fixation_data.html', {'histopath_fixation_data_value':histopath_fixation_data_value, 'user_name':request.user.username,'date_form' : DateForm()})
    


@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Lab - Slide Label Data')
def slide_label_data(request):

    if request.method == 'GET':
        return render(request,'reports/slide_label_data.html', {'user_name':request.user.username, "page_name" : "Slide Label Data"})
    
     
    elif request.method == 'POST':
        db =  Ora()
        slide_label_data_data, column_name = db.get_slide_label_data()
        excel_file_path = excel_generator(page_name="Slide Label Data",data=slide_label_data_data,column=column_name)

        if not slide_label_data_data:
            return render(request,'reports/slide_label_data.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/slide_label_data.html', {'slide_label_data_data':slide_label_data_data, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users("Marketing - Contract Effective Date Report")
def contract_effective_date_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/contract_effective_date_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Contract Effective Date Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/contract_effective_date_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        contract_effective_date_report_value, column_name = db.get_contract_effective_date_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Contract Effective Date Report",data=contract_effective_date_report_value,column=column_name)
        
        if not contract_effective_date_report_value:
            return render(request,'reports/contract_effective_date_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/contract_effective_date_report.html', {'contract_effective_date_report_value':contract_effective_date_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users('Marketing - Admission Reports')
def admission_report(request):
    if request.method == 'GET':
        return render(request,'reports/admission_report.html', {'user_name':request.user.username , "page_name" : "Admission Reports", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        admission_report_value, column_name = db.get_admission_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Admission Reports",data=admission_report_value,column=column_name)
        
        if not admission_report_value:
            return render(request,'reports/admission_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/admission_report.html', {'admission_report_value':admission_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Marketing - Patient Discharge Report')
def patient_discharge_report(request):
    if request.method == 'GET':
        return render(request,'reports/patient_discharge_report.html', {'user_name':request.user.username , "page_name" : "Patient Discharge Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        patient_discharge_report_value, column_name = db.get_patient_discharge_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Patient Discharge Report",data=patient_discharge_report_value,column=column_name)
        
        if not patient_discharge_report_value:
            return render(request,'reports/patient_discharge_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/patient_discharge_report.html', {'patient_discharge_report_value':patient_discharge_report_value, 'user_name':request.user.username,'date_form' : DateForm()})



@login_required(login_url='login')
@allowed_users('Marketing - Credit Letter Report')
def credit_letter_report(request):
    if request.method == 'GET':
        return render(request,'reports/credit_letter_report.html', {'user_name':request.user.username , "page_name" : "Credit Letter Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        credit_letter_report_value, column_name = db.get_credit_letter_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Credit Letter Report",data=credit_letter_report_value,column=column_name)
        
        if not credit_letter_report_value:
            return render(request,'reports/credit_letter_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/credit_letter_report.html', {'credit_letter_report_value':credit_letter_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Marketing - Corporate IP Report')
def corporate_ip_report(request):
    if request.method == 'GET':
        return render(request,'reports/corporate_ip_report.html', {'user_name':request.user.username , "page_name" : "Corporate IP Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        corporate_ip_report_value, column_name = db.get_corporate_ip_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Corporate IP Report",data=corporate_ip_report_value,column=column_name)
        
        if not corporate_ip_report_value:
            return render(request,'reports/corporate_ip_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/corporate_ip_report.html', {'corporate_ip_report_value':corporate_ip_report_value, 'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users('Marketing - OPD Consultation Report')
def opd_consultation_report(request):
    if request.method == 'GET':
        return render(request,'reports/opd_consultation_report.html', {'user_name':request.user.username , "page_name" : "OPD Consultation Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        opd_consultation_report_value, column_name = db.get_opd_consultation_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="OPD Consultation Report",data=opd_consultation_report_value,column=column_name)
        
        if not opd_consultation_report_value:
            return render(request,'reports/opd_consultation_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/opd_consultation_report.html', {'opd_consultation_report_value':opd_consultation_report_value, 'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users('Marketing - Emergency Casualty Report')
def emergency_casualty_report(request):
    if request.method == 'GET':
        return render(request,'reports/emergency_casualty_report.html', {'user_name':request.user.username , "page_name" : "Emergency Casualty Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        emergency_casualty_report_value, column_name = db.get_emergency_casualty_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Emergency Casualty Report",data=emergency_casualty_report_value,column=column_name)
        
        if not emergency_casualty_report_value:
            return render(request,'reports/emergency_casualty_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/emergency_casualty_report.html', {'emergency_casualty_report_value':emergency_casualty_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    


@login_required(login_url='login')
@allowed_users("Marketing - New Registration Report")
def new_registration_report(request):
    if request.method == 'GET':
        global facility
        facility = FacilityDropdown.objects.all()

        return render(request,'reports/new_registration_report.html', {
            'user_name':request.user.username , 
            "page_name" : "New Registration Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            })
    
    elif request.method == 'POST':
        print(request.POST)
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        city_input = request.POST['city_input'].upper()
        facility_code = request.POST['facility_dropdown']
        
        db = Ora()
        new_registration_report_value, new_registration_report_column = db.get_new_registration_report(from_date,to_date,facility_code,city_input)
        excel_file_path = excel_generator(page_name="New Registration Report",data=new_registration_report_value,column=new_registration_report_column)
        
        if not new_registration_report_value:
            return render(request,'reports/new_registration_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities':facility,})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/new_registration_report.html', {'new_registration_report_value':new_registration_report_value, "new_registration_report_column":new_registration_report_column,'user_name':request.user.username,'date_form' : DateForm()})




@login_required(login_url='login')
@allowed_users("Marketing - Hospital Tariff Report")
def hospital_tariff_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/hospital_tariff_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Hospital Tariff Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/hospital_tariff_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        hospital_tariff_report_value, column_name = db.get_hospital_tariff_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Hospital Tariff Report",data=hospital_tariff_report_value,column=column_name)
        
        if not hospital_tariff_report_value:
            return render(request,'reports/hospital_tariff_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/hospital_tariff_report.html', {'hospital_tariff_report_value':hospital_tariff_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})



@login_required(login_url='login')
@allowed_users('Marketing - International Patient Report')
def international_patient_report(request):
    if request.method == 'GET':
        return render(request,'reports/international_patient_report.html', {'user_name':request.user.username , "page_name" : "International Patient Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        international_patient_report_value, column_name = db.get_international_patient_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="International Patient Report",data=international_patient_report_value,column=column_name)
        
        if not international_patient_report_value:
            return render(request,'reports/international_patient_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/international_patient_report.html', {'international_patient_report_value':international_patient_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    


@login_required(login_url='login')
@allowed_users('Marketing - TPA Query')
def tpa_query(request):
    if request.method == 'GET':
        return render(request,'reports/tpa_query.html', {'user_name':request.user.username , "page_name" : "TPA Query", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        tpa_query_value, column_name = db.get_tpa_query(from_date,to_date)
        excel_file_path = excel_generator(page_name="TPA Query",data=tpa_query_value,column=column_name)
        
        if not tpa_query_value:
            return render(request,'reports/tpa_query.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/tpa_query.html', {'tpa_query_value':tpa_query_value, 'user_name':request.user.username,'date_form' : DateForm()})
    

@login_required(login_url='login')
@allowed_users('Marketing - New Admission Report')
def new_admission_report(request):
    if request.method == 'GET':
        return render(request,'reports/new_admission_report.html', {'user_name':request.user.username , "page_name" : "New Admission Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        new_admission_report_value, column_name = db.get_new_admission_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="New Admission Report",data=new_admission_report_value,column=column_name)
        
        if not new_admission_report_value:
            return render(request,'reports/new_admission_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/new_admission_report.html', {'new_admission_report_value':new_admission_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    

@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Billing - Discharge Billing Report')
def discharge_billing_report(request):
    if request.method == 'GET':
        return render(request,'reports/discharge_billing_report.html', {'user_name':request.user.username , "page_name" : "Discharge Billing Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        discharge_billing_report_value, column_name = db.get_discharge_billing_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Discharge Billing Report",data=discharge_billing_report_value,column=column_name)
        
        if not discharge_billing_report_value:
            return render(request,'reports/discharge_billing_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/discharge_billing_report.html', {'discharge_billing_report_value':discharge_billing_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    

@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Billing - Discharge Billing Report Without Date Range')
def discharge_billing_report_without_date_range(request):

    if request.method == 'GET':
        return render(request,'reports/discharge_billing_report_without_date_range.html', {'user_name':request.user.username, "page_name" : "Discharge Billing Report Without Date Range"})

    
    elif request.method == 'POST':
        db =  Ora()
        discharge_billing_report_without_date_range_value, column_name = db.get_discharge_billing_report_without_date_range()
        excel_file_path = excel_generator(page_name="Discharge Billing Report Without Date Range",data=discharge_billing_report_without_date_range_value,column=column_name)

        if not discharge_billing_report_without_date_range_value:
            return render(request,'reports/discharge_billing_report_without_date_range.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/discharge_billing_report_without_date_range.html', {'discharge_billing_report_without_date_range_value':discharge_billing_report_without_date_range_value, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Billing - Discharge Billing User')
def discharge_billing_user(request):

    if request.method == 'GET':
        return render(request,'reports/discharge_billing_user.html', {'user_name':request.user.username, "page_name" : "Discharge Billing User"})

    
    elif request.method == 'POST':
        db =  Ora()
        discharge_billing_user_value, column_name = db.get_discharge_billing_user()
        excel_file_path = excel_generator(page_name="Discharge Billing User",data=discharge_billing_user_value,column=column_name)

        if not discharge_billing_user_value:
            return render(request,'reports/discharge_billing_user.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/discharge_billing_user.html', {'discharge_billing_user_value':discharge_billing_user_value, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Billing - Discount Report')
def discount_report(request):
    if request.method == 'GET':
        return render(request,'reports/discount_report.html', {'user_name':request.user.username , "page_name" : "Discount Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        discount_report_value, column_name = db.get_discount_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Discount Report",data=discount_report_value,column=column_name)
        
        if not discount_report_value:
            return render(request,'reports/discount_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/discount_report.html', {'discount_report_value':discount_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    
    

@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Billing - Refund Report')
def refund_report(request):
    if request.method == 'GET':
        return render(request,'reports/refund_report.html', {'user_name':request.user.username , "page_name" : "Refund Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        refund_report_value, column_name = db.get_refund_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Refund Report",data=refund_report_value,column=column_name)
        
        if not refund_report_value:
            return render(request,'reports/refund_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/refund_report.html', {'refund_report_value':refund_report_value, 'user_name':request.user.username,'date_form' : DateForm()})
    

@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Billing - Non Medical Equipment Report')
def non_medical_equipment_report(request):

    if request.method == 'GET':
        return render(request,'reports/non_medical_equipment_report.html', {'user_name':request.user.username, "page_name" : "Non Medical Equipment Report"})
    
     
    elif request.method == 'POST':
        uhid = request.POST['uhid'].upper()
        episode_id = request.POST['episode_id']
        db =  Ora()
        non_medical_equipment_report_data, column_name = db.get_non_medical_equipment_report(uhid,episode_id)
        excel_file_path = excel_generator(page_name="Non Medical Equipment Report",data=non_medical_equipment_report_data,column=column_name)

        if not non_medical_equipment_report_data:
            return render(request,'reports/non_medical_equipment_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/non_medical_equipment_report.html', {'non_medical_equipment_report_data':non_medical_equipment_report_data, 'user_name':request.user.username})
            


@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - EHC - EHC Operation Report")
def ehc_operation_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/ehc_operation_report.html', {
            'user_name':request.user.username, 
            "page_name" : "EHC Operation Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/ehc_operation_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        ehc_operation_report_value, column_name = db.get_ehc_operation_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="EHC Operation Report",data=ehc_operation_report_value,column=column_name)
        
        if not ehc_operation_report_value:
            return render(request,'reports/ehc_operation_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/ehc_operation_report.html', {'ehc_operation_report_value':ehc_operation_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - EHC - EHC Operation Report 2")
def ehc_operation_report_2(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/ehc_operation_report_2.html', {
            'user_name':request.user.username, 
            "page_name" : "EHC Operation Report 2", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/ehc_operation_report_2.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        ehc_operation_report_2_value, column_name = db.get_ehc_operation_report_2(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="EHC Operation Report 2",data=ehc_operation_report_2_value,column=column_name)
        
        if not ehc_operation_report_2_value:
            return render(request,'reports/ehc_operation_report_2.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/ehc_operation_report_2.html', {'ehc_operation_report_2_value':ehc_operation_report_2_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url='login')
@allowed_users("Miscellaneous Reports - Sales - Oncology Drugs Report")
def oncology_drugs_report(request):
    facility = FacilityDropdown.objects.all()

    if request.method == 'GET':
        return render(request,'reports/oncology_drugs_report.html', {
            'user_name':request.user.username, 
            "page_name" : "Oncology Drugs Report", 
            'date_form' : DateForm(),
            'facilities' : facility,
            
            })

    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        

        try :
            facility_code = request.POST['facility_dropdown']
        except MultiValueDictKeyError:
            return render(request,'reports/oncology_drugs_report.html', {'error':"😒 Please Select a facility from the dropdown list",'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})

        db = Ora()
        oncology_drugs_report_value, column_name = db.get_oncology_drugs_report(facility_code,from_date,to_date)
        excel_file_path = excel_generator(page_name="Oncology Drugs Report",data=oncology_drugs_report_value,column=column_name)
        
        if not oncology_drugs_report_value:
            return render(request,'reports/oncology_drugs_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/oncology_drugs_report.html', {'oncology_drugs_report_value':oncology_drugs_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})



@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Radiology - Radiology TAT Report')
def radiology_tat_report(request):
    if request.method == 'GET':
        return render(request,'reports/radiology_tat_report.html', {'user_name':request.user.username , "page_name" : "Radiology TAT Report", 'date_form' : DateForm()})
    
    elif request.method == 'POST':
        #Manually format To Date fro Sql Query
        from_date = date_formater(request.POST['from_date'])
        to_date = date_formater(request.POST['to_date'])
        
        db = Ora()
        radiology_tat_report_value, column_name = db.get_radiology_tat_report(from_date,to_date)
        excel_file_path = excel_generator(page_name="Radiology TAT Report",data=radiology_tat_report_value,column=column_name)
        
        if not radiology_tat_report_value:
            return render(request,'reports/radiology_tat_report.html', {'error':"Sorry!!! No Data Found", 'user_name':request.user.username,'date_form' : DateForm()})
        
        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/radiology_tat_report.html', {'radiology_tat_report_value':radiology_tat_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - OT Scheduling List Report')
def ot_scheduling_list_report(request):

    if request.method == 'GET':
        return render(request,'reports/ot_scheduling_list_report.html', {'user_name':request.user.username, "page_name" : "OT Scheduling List Report"})
    
     
    elif request.method == 'POST':
        db =  Ora()
        ot_scheduling_list_report_data, column_name = db.get_ot_scheduling_list_report()
        excel_file_path = excel_generator(page_name="OT Scheduling List Report",data=ot_scheduling_list_report_data,column=column_name)

        if not ot_scheduling_list_report_data:
            return render(request,'reports/ot_scheduling_list_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/ot_scheduling_list_report.html', {'ot_scheduling_list_report_data':ot_scheduling_list_report_data, 'user_name':request.user.username})


@login_required(login_url='login')
@allowed_users('Miscellaneous Reports - Non Package Covid Patient Report')
def non_package_covid_patient_report(request):

    if request.method == 'GET':
        return render(request,'reports/non_package_covid_patient_report.html', {'user_name':request.user.username, "page_name" : "Non Package Covid Patient Report"})
    
     
    elif request.method == 'POST':
        db =  Ora()
        non_package_covid_patient_report_data, column_name = db.get_non_package_covid_patient_report()
        excel_file_path = excel_generator(page_name="Non Package Covid Patient Report",data=non_package_covid_patient_report_data,column=column_name)

        if not non_package_covid_patient_report_data:
            return render(request,'reports/non_package_covid_patient_report.html', {'error':"Sorry!!! No Data Found" , 'user_name':request.user.username})

        else:
            return FileResponse(open(excel_file_path, 'rb'), content_type='application/vnd.ms-excel')
            #return render(request,'reports/non_package_covid_patient_report.html', {'non_package_covid_patient_report_data':non_package_covid_patient_report_data, 'user_name':request.user.username})


