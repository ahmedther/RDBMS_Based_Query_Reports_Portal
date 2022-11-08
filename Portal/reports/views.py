from multiprocessing import context
import platform
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import FileResponse, HttpResponse

from .oracle_config import Ora
from .decorators import unauthenticated_user, allowed_users
from .forms import DateForm, DateTimeForm
from .models import IAACR, FacilityDropdown, Employee
from .supports import (
    date_formater,
    excel_generator,
    excel_generator_tpa,
    input_validator,
)


# Create your views here.


@unauthenticated_user
def signupuser(request):
    facility = FacilityDropdown.objects.all().order_by("facility_name")
    context = {
        "form": UserCreationForm(),
        "facilities": facility,
    }
    if request.method == "GET":
        return render(request, "reports/signupuser.html", context)
    else:

        facility_code = input_validator(
            request=request,
            context=context,
            error_name="Facility",
            value_in_post="facility_dropdown",
        )
        first_name = input_validator(
            request=request,
            context=context,
            error_name="First Name",
            value_in_post="first_name",
        )
        last_name = input_validator(
            request=request,
            context=context,
            error_name="Last Name",
            value_in_post="last_name",
        )
        pr_number = input_validator(
            request=request,
            context=context,
            error_name="Payroll Number",
            value_in_post="pr_number",
        )
        department = input_validator(
            request=request,
            context=context,
            error_name="Department",
            value_in_post="department",
        )
        username = input_validator(
            request=request,
            context=context,
            error_name="Username",
            value_in_post="username",
        )

        if request.POST["password1"] == request.POST["password2"]:

            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password1"],
                    first_name=first_name,
                    last_name=last_name,
                )
                user.save()
                employe_data = Employee(
                    user=User.objects.get(pk=user.id),
                    department=department,
                    pr_number=pr_number,
                    facility=FacilityDropdown.objects.get(pk=facility_code),
                )
                employe_data.save()

                context["success"] = "You Have Successfuly Signed Up"
                context[
                    "success1"
                ] = "Please enter your User ID and Password to Sign In"

                return render(request, "reports/login_page.html", context)

            except IntegrityError:
                context[
                    "error"
                ] = "That username has already been taken. Please choose a new username"
                return render(request, "reports/signupuser.html", context)

            # except ValueError:
            #     context["error"] = "Please Enter a Valid Username and Password"
            #     return render(request, "reports/signupuser.html", context)
        else:
            context["error"] = "Passwords did not match"
            return render(request, "reports/signupuser.html", context)


@unauthenticated_user
def login_page(request):

    if request.method == "GET":
        return render(request, "reports/login_page.html")

    else:

        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        global user_name
        user_name = request.POST["username"]

        if user is None:
            return render(
                request,
                "reports/login_page.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username and password did not match",
                },
            )
        else:
            login(request, user)
            return render(
                request, "reports/index.html", {"user_name": request.user.username}
            )


@login_required(login_url="login")
def logoutuser(request):

    if request.method == "POST":
        logout(request)
        return redirect("login")


@login_required(login_url="login")
def landing_page(request):

    if request.method == "GET":
        return render(
            request, "reports/index.html", {"user_name": request.user.username}
        )


@login_required(login_url="login")
def kh_nav(request):
    # Pharmacy Based permissions
    pharmacy_permission = request.user.groups.filter(name="Pharmacy")
    stock_permission = request.user.groups.filter(name="Pharmacy - Stock")
    stock_report_permission = request.user.groups.filter(name="Pharmacy - Stock Report")
    stock_value_permission = request.user.groups.filter(name="Pharmacy - Stock Value")
    bin_location_op_permission = request.user.groups.filter(
        name="Pharmacy - Bin Location OP"
    )
    itemwise_storewise_stock_permission = request.user.groups.filter(
        name="Pharmacy - Itemwise Storewise Stock Value"
    )
    batchwise_stock_report_permission = request.user.groups.filter(
        name="Pharmacy - Batch Wise Stock Report"
    )
    pharmacy_op_returns_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy OP Returns"
    )
    restricted_antimicrobials_consumption_report_permission = (
        request.user.groups.filter(
            name="Pharmacy - Restricted Antimicrobials Consumption Report"
        )
    )
    pharmacy_itemwise_sale_report_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy Itemwise Sale Report"
    )
    pharmacy_indent_report_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy Indent Report"
    )
    new_admission_indents_report_permission = request.user.groups.filter(
        name="Pharmacy - New Admission's Indents Report"
    )
    return_medication_without_return_request_report_permission = (
        request.user.groups.filter(
            name="Pharmacy - Return Medication Without Return Request Report"
        )
    )
    deleted_pharmacy_prescriptions_report_permission = request.user.groups.filter(
        name="Pharmacy - Deleted Pharmacy Prescriptions Report"
    )
    pharmacy_direct_sales_report_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy Direct Sales Report"
    )
    intransites_unf_sal_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Unf Sal"
    )
    intransites_confirm_pending_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Confirm Pending"
    )
    non_billable_consumption_permission = request.user.groups.filter(
        name="Pharmacy - Non Billable Consumption"
    )
    non_billable_consumption1_permission = request.user.groups.filter(
        name="Pharmacy - Non Billable Consumption 1"
    )
    item_substitution_report_permission = request.user.groups.filter(
        name="Pharmacy - Item Substitution Report"
    )
    foc_grn_report_permission = request.user.groups.filter(
        name="Pharmacy - FOC GRN Report"
    )
    pharmacy_charges_and_implant_pending_indent_report_permission = (
        request.user.groups.filter(
            name="Pharmacy - Pharmacy Charges & Implant Pending Indent Report"
        )
    )
    pharmacy_direct_returns_sale_report_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy Direct Returns Sale Report"
    )
    current_inpatients_report_permission = request.user.groups.filter(
        name="Pharmacy - Current Inpatients Reports"
    )
    consigned_item_detail_report_permission = request.user.groups.filter(
        name="Pharmacy - Consigned Item Detail Report"
    )
    schedule_h1_drug_report_permission = request.user.groups.filter(
        name="Pharmacy - Schedule H1 Drug Report"
    )
    pharmacy_ward_return_requests_with_status_report_permission = (
        request.user.groups.filter(
            name="Pharmacy - Pharmacy Ward Return Requests with Status Report"
        )
    )
    pharmacy_indent_deliver_summary_report_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy Indent Deliver Summary Report"
    )
    intransites_stk_tfr_acknowledgement_pending_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Stk Tfr Acknowledgement Pending Report"
    )
    folley_and_central_line_permission = request.user.groups.filter(
        name="Pharmacy - Folley and Central Line"
    )
    angiography_kit_permission = request.user.groups.filter(
        name="Pharmacy - Angiography Kit"
    )
    search_indents_by_code_permission = request.user.groups.filter(
        name="Pharmacy - Search Indents By Code"
    )
    new_admission_dispense_report_permission = request.user.groups.filter(
        name="Pharmacy - New Admission Dispense Report"
    )
    pharmacy_op_sale_report_userwise_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy OP Sale Report Userwise"
    )
    pharmacy_consumption_report_permission = request.user.groups.filter(
        name="Pharmacy - Pharmacy Consumption Report"
    )
    food_drug_interaction_report_permission = request.user.groups.filter(
        name="Pharmacy - Food-Drug Interaction Report"
    )
    intransite_stock_permission = request.user.groups.filter(
        name="Pharmacy - Intransite Stock"
    )
    grn_data_permission = request.user.groups.filter(name="Pharmacy - GRN Data")
    drug_duplication_override_report_permission = request.user.groups.filter(
        name="Pharmacy - Drug Duplication Override Report"
    )
    drug_interaction_override_report_permission = request.user.groups.filter(
        name="Pharmacy - Drug Interaction Override Report"
    )
    sale_consumption_report_permission = request.user.groups.filter(
        name="Pharmacy - Sale Consumption Report"
    )
    sale_consumption_report1_permission = request.user.groups.filter(
        name="Pharmacy - Sale Consumption Report 1"
    )
    new_code_creation_permission = request.user.groups.filter(
        name="Pharmacy - New Code Creation"
    )
    tvd_cabg_request_permission = request.user.groups.filter(
        name="Pharmacy - TVD CABG Request"
    )
    stock_amount_wise_permission = request.user.groups.filter(
        name="Pharmacy - Stock Amount-Wise"
    )
    dept_issue_pending_tracker_permission = request.user.groups.filter(
        name="Pharmacy - Dept Issue Pending Tracker"
    )
    patient_indent_count_permission = request.user.groups.filter(
        name="Pharmacy - Patient Indent Count"
    )
    predischarge_medication_permission = request.user.groups.filter(
        name="Pharmacy - Predischarge Medication"
    )
    predischarge_initiate_permission = request.user.groups.filter(
        name="Pharmacy - Predischarge Initiate"
    )
    intransites_unf_sal_ret_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Unf Sal Ret"
    )
    intransites_unf_stk_tfr_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Unf Stk Tfr"
    )
    intransites_acknowledgement_pending_iss_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Acknowledgement Pending ISS"
    )
    intransites_acknowledgement_pending_iss_rt_permission = request.user.groups.filter(
        name="Pharmacy - Intransites Acknowledgement Pending ISS RT"
    )
    narcotic_stock_report_permission = request.user.groups.filter(
        name="Pharmacy - Narcotic Stock Report"
    )
    # Finance Based Permissions
    finance_permission = request.user.groups.filter(name="Finance")
    credit_outstanding_bill_permission = request.user.groups.filter(
        name="Finance - Credit Bill Outstanding"
    )
    tpa_letter_permission = request.user.groups.filter(name="Finance - TPA Letter")
    online_consultation_report_permission = request.user.groups.filter(
        name="Finance - Online Consultation Report"
    )
    contract_report_permission = request.user.groups.filter(
        name="Finance - Contract Reports"
    )
    admission_census_permission = request.user.groups.filter(
        name="Finance - Admission Census"
    )
    card_permission = request.user.groups.filter(name="Finance - Card")

    patientwise_bill_details_permission = request.user.groups.filter(
        name="Finance - Patient-Wise Bill Details"
    )

    package_contract_report_permission = request.user.groups.filter(
        name="Finance - Package Contract Report"
    )
    credit_card_reconciliation_report_permission = request.user.groups.filter(
        name="Finance - Credit Card Reconciliation Report"
    )
    covid_ot_surgery_details_permission = request.user.groups.filter(
        name="Finance - Covid OT Surgery Details"
    )
    gst_data_of_pharmacy_permission = request.user.groups.filter(
        name="Finance - GST Data of Pharmacy"
    )
    cathlab_permission = request.user.groups.filter(name="Finance - Cathlab")
    form_61_permission = request.user.groups.filter(name="Finance - Form 61")
    packages_applied_to_patients_permission = request.user.groups.filter(
        name="Finance - Packages Applied To Patients"
    )
    gst_data_of_pharmacy_return_permission = request.user.groups.filter(
        name="Finance - GST Data of Pharmacy Return"
    )
    gst_data_of_ip_permission = request.user.groups.filter(
        name="Finance - GST Data of IP"
    )
    gst_data_of_op_permission = request.user.groups.filter(
        name="Finance - GST Data of OP"
    )
    ot_permission = request.user.groups.filter(name="Finance - OT")

    discharge_census_permission = request.user.groups.filter(
        name="Finance - Discharge Census"
    )
    gst_ipd_permission = request.user.groups.filter(name="Finance - GST IPD")

    revenue_data_of_sl_permission = request.user.groups.filter(
        name="Finance - Revenue Data of SL"
    )
    revenue_data_of_sl1_permission = request.user.groups.filter(
        name="Finance - Revenue Data of SL 1"
    )
    revenue_data_of_sl2_permission = request.user.groups.filter(
        name="Finance - Revenue Data of SL 2"
    )
    revenue_data_of_sl3_permission = request.user.groups.filter(
        name="Finance - Revenue Data of SL 3"
    )
    revenue_jv_permission = request.user.groups.filter(name="Finance - Revenue JV")
    collection_report_permission = request.user.groups.filter(
        name="Finance - Collection Report"
    )

    # Clinical Administration Based Permissions
    clinical_administration_permission = request.user.groups.filter(
        name="Clinical Administration"
    )
    discharge_report_2_permission = request.user.groups.filter(
        name="Clinical Administration - Discharge Report 2"
    )
    pre_discharge_report_permission = request.user.groups.filter(
        name="Clinical Administration - Pre Discharge Report"
    )
    pre_discharge_report_2_permission = request.user.groups.filter(
        name="Clinical Administration - Pre Discharge Report 2"
    )
    discharge_with_mis_report_permission = request.user.groups.filter(
        name="Clinical Administration - Discharge With MIS Report"
    )
    needle_prick_injury_report_permission = request.user.groups.filter(
        name="Clinical Administration - Needle Prick Injury Report"
    )
    practo_report_permission = request.user.groups.filter(
        name="Clinical Administration - Practo Report"
    )
    unbilled_report_permission = request.user.groups.filter(
        name="Clinical Administration - Unbilled Report"
    )
    unbilled_deposit_report_permission = request.user.groups.filter(
        name="Clinical Administration - Unbilled Deposit Report"
    )
    contact_report_permission = request.user.groups.filter(
        name="Clinical Administration - Contact Report"
    )
    employees_antibodies_reactive_report_permission = request.user.groups.filter(
        name="Clinical Administration - Employees Antibodies Reactive Report"
    )
    employees_reactive_and_non_pcr_report_permission = request.user.groups.filter(
        name="Clinical Administration - Employee Reactive and Non PCR Report"
    )
    employee_covid_test_report_permission = request.user.groups.filter(
        name="Clinical Administration - Employee Covid Test Report"
    )
    bed_location_report_permission = request.user.groups.filter(
        name="Clinical Administration - Bed Location Report"
    )
    home_visit_report_permission = request.user.groups.filter(
        name="Clinical Administration - Home Visit Report"
    )
    cco_billing_count_report_permission = request.user.groups.filter(
        name="Clinical Administration - CCO Billing Count Report"
    )
    total_number_of_online_consultation_by_doctors_permission = request.user.groups.filter(
        name="Clinical Administration - Total Number of Online Consultation by Doctors"
    )
    tpa_current_inpatients_permission = request.user.groups.filter(
        name="Clinical Administration - TPA Current Inpatients"
    )
    tpa_cover_letter_permission = request.user.groups.filter(
        name="Clinical Administration - TPA Cover Letter"
    )
    total_number_of_ip_patients_by_doctors_permission = request.user.groups.filter(
        name="Clinical Administration - Total Number of IP Patients by Doctors"
    )
    total_number_of_op_patients_by_doctors_permission = request.user.groups.filter(
        name="Clinical Administration - Total Number of OP Patients by Doctors"
    )
    opd_changes_report_permission = request.user.groups.filter(
        name="Clinical Administration - OPD Changes Report"
    )
    ehc_conversion_report_permission = request.user.groups.filter(
        name="Clinical Administration - EHC Conversion Report"
    )
    ehc_package_range_report_permission = request.user.groups.filter(
        name="Clinical Administration - EHC Package Range Report"
    )
    error_report_permission = request.user.groups.filter(
        name="Clinical Administration - Error Report"
    )
    ot_query_report_permission = request.user.groups.filter(
        name="Clinical Administration - OT Query Report"
    )
    outreach_cancer_hospital_permission = request.user.groups.filter(
        name="Clinical Administration - Outreach Cancer Hospital"
    )
    gipsa_report_permission = request.user.groups.filter(
        name="Clinical Administration - GIPSA Report"
    )
    precision_patient_opd_and_online_consultation_list_report_permission = request.user.groups.filter(
        name="Clinical Administration - Precision Patient OPD & Online Consultation List Report"
    )
    appointment_details_by_call_center_report_permission = request.user.groups.filter(
        name="Clinical Administration - Appointment Details By Call Center Report"
    )
    trf_report_permission = request.user.groups.filter(
        name="Clinical Administration - TRF Report"
    )
    current_inpatients_clinical_admin_permission = request.user.groups.filter(
        name="Clinical Administration - Current Inpatients(Clinical Admin)"
    )
    check_patient_registration_date_permission = request.user.groups.filter(
        name="Clinical Administration - Check Patient Registration Date"
    )
    opd_consultation_report_with_address_permission = request.user.groups.filter(
        name="Clinical Administration - OPD Consultation Report With Address"
    )

    current_inpatients_employee_and_dependants_permission = request.user.groups.filter(
        name="Clinical Administration - Current Inpatients Employee and Dependants"
    )
    treatment_sheet_data_permission = request.user.groups.filter(
        name="Clinical Administration - Treatment Sheet Data"
    )
    patient_registration_report_permission = request.user.groups.filter(
        name="Clinical Administration - Patient Registration Report"
    )

    # Lab Baed Permissions
    lab_permission = request.user.groups.filter(name="Lab")
    covid_pcr_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - Covid PCR"
    )
    covid_2_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - Covid 2"
    )
    covid_antibodies_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - Covid Antibodies"
    )
    covid_antigen_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - Covid Antibodies"
    )
    cbnaat_test_data_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - CBNAAT Test Data"
    )
    lab_tat_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - LAB TAT Report"
    )
    histopath_fixation_data_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - Histopath Fixation Data"
    )
    slide_label_data_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Lab - Slide Label Data"
    )

    # Marketing Based Permissions
    marketing_permission = request.user.groups.filter(name="Marketing")
    contract_effective_date_report_permission = request.user.groups.filter(
        name="Marketing - Contract Effective Date Report"
    )
    admission_report_permission = request.user.groups.filter(
        name="Marketing - Admission Reports"
    )
    patient_discharge_report_permission = request.user.groups.filter(
        name="Marketing - Patient Discharge Report"
    )
    corporate_discharge_report_permission = request.user.groups.filter(
        name="Marketing - Corporate Discharge Report"
    )
    corporate_discharge_report_with_customer_code_permission = (
        request.user.groups.filter(
            name="Marketing - Corporate Discharge Report With Customer Code"
        )
    )
    credit_letter_report_permission = request.user.groups.filter(
        name="Marketing - Credit Letter Report"
    )
    corporate_ip_report_permission = request.user.groups.filter(
        name="Marketing - Corporate IP Report"
    )
    opd_consultation_report_permission = request.user.groups.filter(
        name="Marketing - OPD Consultation Report"
    )
    emergency_casualty_report_permission = request.user.groups.filter(
        name="Marketing - Emergency Casualty Report"
    )
    new_registration_report_permission = request.user.groups.filter(
        name="Marketing - New Registration Report"
    )
    hospital_tariff_report_permission = request.user.groups.filter(
        name="Marketing - Hospital Tariff Report"
    )
    international_patient_report_permission = request.user.groups.filter(
        name="Marketing - International Patient Report"
    )
    tpa_query_permission = request.user.groups.filter(name="Marketing - TPA Query")
    new_admission_report_permission = request.user.groups.filter(
        name="Marketing - New Admission Report"
    )

    # Miscellaneous_Reports
    miscellaneous_reports_permission = request.user.groups.filter(
        name="Miscellaneous Reports"
    )
    ot_scheduling_list_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - OT Scheduling List Report"
    )
    non_package_covid_patient_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Non Package Covid Patient Report"
    )
    # Microbiology
    microbiology_permission = request.user.groups.filter(name="Microbiology")
    gx_flu_a_flu_b_rsv_permission = request.user.groups.filter(
        name="Microbiology - GX Flu A, Flu B RSV"
    )
    h1n1_detection_by_pcr_permission = request.user.groups.filter(
        name="Microbiology - H1N1 Detection By PCR"
    )
    biofire_respiratory_permission = request.user.groups.filter(
        name="Microbiology - Biofire Respiratory"
    )
    covid_19_report_with_pincode_and_ward_permission = request.user.groups.filter(
        name="Microbiology - COVID 19 Report With Pincode And Ward"
    )
    cbnaat_covid_report_with_pincode_permission = request.user.groups.filter(
        name="Microbiology - CBNAAT COVID Report With Pincode"
    )

    # Billing
    billing_permission = request.user.groups.filter(name="Billing")
    discharge_billing_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Discharge Billing Report"
    )
    discharge_billing_report_without_date_range_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Discharge Billing Report Without Date Range"
    )
    discharge_billing_user_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Discharge Billing User"
    )
    discount_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Discount Report"
    )
    refund_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Refund Report"
    )
    non_medical_equipment_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Non Medical Equipment Report"
    )
    additional_tax_on_package_room_rent_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Additional Tax On Package Room Rent"
    )
    due_deposit_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Billing - Due Deposit Report"
    )
    # EHC
    ehc_permission = request.user.groups.filter(name="EHC")
    ehc_operation_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - EHC - EHC Operation Report"
    )
    ehc_operation_report_2_permission = request.user.groups.filter(
        name="Miscellaneous Reports - EHC - EHC Operation Report 2"
    )
    # Sales
    sales_permission = request.user.groups.filter(name="Sales")
    oncology_drugs_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Sales - Oncology Drugs Report"
    )
    # Radiology
    radiology_permission = request.user.groups.filter(name="Radiology")
    radiology_tat_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Radiology - Radiology TAT Report"
    )
    # Internal Auditor
    internal_auditor_permission = request.user.groups.filter(name="Internal Auditor")
    day_care_report_permission = request.user.groups.filter(
        name="Miscellaneous Reports - Internal Auditor - Day Care Report"
    )
    context = {
        # Facility Identifier
        #
        # User Det
        "user_name": request.user.username,
        # Pharmacy Permission Dictionary
        "pharmacy_permission": pharmacy_permission,
        "stock_permission": stock_permission,
        "stock_report_permission": stock_report_permission,
        "stock_value_permission": stock_value_permission,
        "bin_location_op_permission": bin_location_op_permission,
        "itemwise_storewise_stock_permission": itemwise_storewise_stock_permission,
        "batchwise_stock_report_permission": batchwise_stock_report_permission,
        "pharmacy_op_returns_permission": pharmacy_op_returns_permission,
        "restricted_antimicrobials_consumption_report_permission": restricted_antimicrobials_consumption_report_permission,
        "pharmacy_itemwise_sale_report_permission": pharmacy_itemwise_sale_report_permission,
        "pharmacy_indent_report_permission": pharmacy_indent_report_permission,
        "new_admission_indents_report_permission": new_admission_indents_report_permission,
        "return_medication_without_return_request_report_permission": return_medication_without_return_request_report_permission,
        "deleted_pharmacy_prescriptions_report_permission": deleted_pharmacy_prescriptions_report_permission,
        "pharmacy_direct_sales_report_permission": pharmacy_direct_sales_report_permission,
        "intransites_unf_sal_permission": intransites_unf_sal_permission,
        "intransites_confirm_pending_permission": intransites_confirm_pending_permission,
        "non_billable_consumption_permission": non_billable_consumption_permission,
        "non_billable_consumption1_permission": non_billable_consumption1_permission,
        "item_substitution_report_permission": item_substitution_report_permission,
        "foc_grn_report_permission": foc_grn_report_permission,
        "pharmacy_charges_and_implant_pending_indent_report_permission": pharmacy_charges_and_implant_pending_indent_report_permission,
        "pharmacy_direct_returns_sale_report_permission": pharmacy_direct_returns_sale_report_permission,
        "current_inpatients_report_permission": current_inpatients_report_permission,
        "consigned_item_detail_report_permission": consigned_item_detail_report_permission,
        "schedule_h1_drug_report_permission": schedule_h1_drug_report_permission,
        "pharmacy_ward_return_requests_with_status_report_permission": pharmacy_ward_return_requests_with_status_report_permission,
        "pharmacy_indent_deliver_summary_report_permission": pharmacy_indent_deliver_summary_report_permission,
        "intransites_stk_tfr_acknowledgement_pending_permission": intransites_stk_tfr_acknowledgement_pending_permission,
        "folley_and_central_line_permission": folley_and_central_line_permission,
        "angiography_kit_permission": angiography_kit_permission,
        "search_indents_by_code_permission": search_indents_by_code_permission,
        "new_admission_dispense_report_permission": new_admission_dispense_report_permission,
        "pharmacy_op_sale_report_userwise_permission": pharmacy_op_sale_report_userwise_permission,
        "credit_card_reconciliation_report_permission": credit_card_reconciliation_report_permission,
        "pharmacy_consumption_report_permission": pharmacy_consumption_report_permission,
        "food_drug_interaction_report_permission": food_drug_interaction_report_permission,
        "intransite_stock_permission": intransite_stock_permission,
        "grn_data_permission": grn_data_permission,
        "drug_duplication_override_report_permission": drug_duplication_override_report_permission,
        "drug_interaction_override_report_permission": drug_interaction_override_report_permission,
        "sale_consumption_report_permission": sale_consumption_report_permission,
        "sale_consumption_report1_permission": sale_consumption_report1_permission,
        "new_code_creation_permission": new_code_creation_permission,
        "tvd_cabg_request_permission": tvd_cabg_request_permission,
        "stock_amount_wise_permission": stock_amount_wise_permission,
        "dept_issue_pending_tracker_permission": dept_issue_pending_tracker_permission,
        "patient_indent_count_permission": patient_indent_count_permission,
        "predischarge_medication_permission": predischarge_medication_permission,
        "predischarge_initiate_permission": predischarge_initiate_permission,
        "intransites_unf_sal_ret_permission": intransites_unf_sal_ret_permission,
        "intransites_unf_stk_tfr_permission": intransites_unf_stk_tfr_permission,
        "intransites_acknowledgement_pending_iss_permission": intransites_acknowledgement_pending_iss_permission,
        "intransites_acknowledgement_pending_iss_rt_permission": intransites_acknowledgement_pending_iss_rt_permission,
        "narcotic_stock_report_permission": narcotic_stock_report_permission,
        # Finance Permission Dictionary
        "finance_permission": finance_permission,
        "credit_outstanding_bill_permission": credit_outstanding_bill_permission,
        "tpa_letter_permission": tpa_letter_permission,
        "online_consultation_report_permission": online_consultation_report_permission,
        "contract_report_permission": contract_report_permission,
        "admission_census_permission": admission_census_permission,
        "card_permission": card_permission,
        "patientwise_bill_details_permission": patientwise_bill_details_permission,
        "package_contract_report_permission": package_contract_report_permission,
        "covid_ot_surgery_details_permission": covid_ot_surgery_details_permission,
        "gst_data_of_pharmacy_permission": gst_data_of_pharmacy_permission,
        "cathlab_permission": cathlab_permission,
        "form_61_permission": form_61_permission,
        "packages_applied_to_patients_permission": packages_applied_to_patients_permission,
        "gst_data_of_pharmacy_return_permission": gst_data_of_pharmacy_return_permission,
        "gst_data_of_ip_permission": gst_data_of_ip_permission,
        "gst_data_of_op_permission": gst_data_of_op_permission,
        "ot_permission": ot_permission,
        "discharge_census_permission": discharge_census_permission,
        "gst_ipd_permission": gst_ipd_permission,
        "revenue_data_of_sl_permission": revenue_data_of_sl_permission,
        "revenue_data_of_sl1_permission": revenue_data_of_sl1_permission,
        "revenue_data_of_sl2_permission": revenue_data_of_sl2_permission,
        "revenue_data_of_sl3_permission": revenue_data_of_sl3_permission,
        "revenue_jv_permission": revenue_jv_permission,
        "collection_report_permission": collection_report_permission,
        # Clinical Administration Based Permissions
        "clinical_administration_permission": clinical_administration_permission,
        "discharge_report_2_permission": discharge_report_2_permission,
        "pre_discharge_report_permission": pre_discharge_report_permission,
        "pre_discharge_report_2_permission": pre_discharge_report_2_permission,
        "discharge_with_mis_report_permission": discharge_with_mis_report_permission,
        "needle_prick_injury_report_permission": needle_prick_injury_report_permission,
        "practo_report_permission": practo_report_permission,
        "unbilled_report_permission": unbilled_report_permission,
        "unbilled_deposit_report_permission": unbilled_deposit_report_permission,
        "contact_report_permission": contact_report_permission,
        "employees_antibodies_reactive_report_permission": employees_antibodies_reactive_report_permission,
        "employees_reactive_and_non_pcr_report_permission": employees_reactive_and_non_pcr_report_permission,
        "employee_covid_test_report_permission": employee_covid_test_report_permission,
        "bed_location_report_permission": bed_location_report_permission,
        "home_visit_report_permission": home_visit_report_permission,
        "cco_billing_count_report_permission": cco_billing_count_report_permission,
        "total_number_of_online_consultation_by_doctors_permission": total_number_of_online_consultation_by_doctors_permission,
        "tpa_current_inpatients_permission": tpa_current_inpatients_permission,
        "tpa_cover_letter_permission": tpa_cover_letter_permission,
        "total_number_of_ip_patients_by_doctors_permission": total_number_of_ip_patients_by_doctors_permission,
        "total_number_of_op_patients_by_doctors_permission": total_number_of_op_patients_by_doctors_permission,
        "opd_changes_report_permission": opd_changes_report_permission,
        "ehc_conversion_report_permission": ehc_conversion_report_permission,
        "ehc_package_range_report_permission": ehc_package_range_report_permission,
        "error_report_permission": error_report_permission,
        "ot_query_report_permission": ot_query_report_permission,
        "outreach_cancer_hospital_permission": outreach_cancer_hospital_permission,
        "gipsa_report_permission": gipsa_report_permission,
        "precision_patient_opd_and_online_consultation_list_report_permission": precision_patient_opd_and_online_consultation_list_report_permission,
        "appointment_details_by_call_center_report_permission": appointment_details_by_call_center_report_permission,
        "trf_report_permission": trf_report_permission,
        "current_inpatients_clinical_admin_permission": current_inpatients_clinical_admin_permission,
        "check_patient_registration_date_permission": check_patient_registration_date_permission,
        "opd_consultation_report_with_address_permission": opd_consultation_report_with_address_permission,
        "patient_registration_report_permission": patient_registration_report_permission,
        "current_inpatients_employee_and_dependants_permission": current_inpatients_employee_and_dependants_permission,
        "treatment_sheet_data_permission": treatment_sheet_data_permission,
        # Marketing
        "marketing_permission": marketing_permission,
        "contract_effective_date_report_permission": contract_effective_date_report_permission,
        "patient_discharge_report_permission": patient_discharge_report_permission,
        "corporate_discharge_report_permission": corporate_discharge_report_permission,
        "corporate_discharge_report_with_customer_code_permission": corporate_discharge_report_with_customer_code_permission,
        "admission_report_permission": admission_report_permission,
        "credit_letter_report_permission": credit_letter_report_permission,
        "corporate_ip_report_permission": corporate_ip_report_permission,
        "opd_consultation_report_permission": opd_consultation_report_permission,
        "emergency_casualty_report_permission": emergency_casualty_report_permission,
        "new_registration_report_permission": new_registration_report_permission,
        "hospital_tariff_report_permission": hospital_tariff_report_permission,
        "international_patient_report_permission": international_patient_report_permission,
        "tpa_query_permission": tpa_query_permission,
        "new_admission_report_permission": new_admission_report_permission,
        # Miscellaneous_Reports
        "miscellaneous_reports_permission": miscellaneous_reports_permission,
        # Microbiology
        "microbiology_permission": microbiology_permission,
        "gx_flu_a_flu_b_rsv_permission": gx_flu_a_flu_b_rsv_permission,
        "h1n1_detection_by_pcr_permission": h1n1_detection_by_pcr_permission,
        "biofire_respiratory_permission": biofire_respiratory_permission,
        "covid_19_report_with_pincode_and_ward_permission": covid_19_report_with_pincode_and_ward_permission,
        "cbnaat_covid_report_with_pincode_permission": cbnaat_covid_report_with_pincode_permission,
        # Billing
        "billing_permission": billing_permission,
        "discharge_billing_report_permission": discharge_billing_report_permission,
        "discharge_billing_report_without_date_range_permission": discharge_billing_report_without_date_range_permission,
        "discharge_billing_user_permission": discharge_billing_user_permission,
        "discount_report_permission": discount_report_permission,
        "refund_report_permission": refund_report_permission,
        "non_medical_equipment_report_permission": non_medical_equipment_report_permission,
        "additional_tax_on_package_room_rent_permission": additional_tax_on_package_room_rent_permission,
        "due_deposit_report_permission": due_deposit_report_permission,
        # Lab
        "lab_permission": lab_permission,
        "covid_antibodies_permission": covid_antibodies_permission,
        "covid_pcr_permission": covid_pcr_permission,
        "covid_2_permission": covid_2_permission,
        "covid_antigen_permission": covid_antigen_permission,
        "cbnaat_test_data_permission": cbnaat_test_data_permission,
        "lab_tat_report_permission": lab_tat_report_permission,
        "histopath_fixation_data_permission": histopath_fixation_data_permission,
        "slide_label_data_permission": slide_label_data_permission,
        # EHC
        "ehc_permission": ehc_permission,
        "ehc_operation_report_permission": ehc_operation_report_permission,
        "ehc_operation_report_2_permission": ehc_operation_report_2_permission,
        # Sales
        "sales_permission": sales_permission,
        "oncology_drugs_report_permission": oncology_drugs_report_permission,
        # Radiology
        "radiology_permission": radiology_permission,
        "radiology_tat_report_permission": radiology_tat_report_permission,
        # Internal Auditor
        "internal_auditor_permission": internal_auditor_permission,
        "day_care_report_permission": day_care_report_permission,
        # ---
        "ot_scheduling_list_report_permission": ot_scheduling_list_report_permission,
        "non_package_covid_patient_report_permission": non_package_covid_patient_report_permission,
        # kokilaben Facility in context
    }
    return render(request, "reports/kh_nav.html", context)


@login_required(login_url="login")
@allowed_users("Pharmacy - Stock")
def stock(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Stock",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        stock_data, stock_column = db.get_stock()
        excel_file_path = excel_generator(
            page_name="Stock", column=stock_column, data=stock_data
        )

        if not stock_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'stock_data':stock_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Stock Report")
def stock_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Stock Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        stock_report, column_name = db.get_stock_reports()
        excel_file_path = excel_generator(
            page_name="Stock Report", column=column_name, data=stock_report
        )

        if not stock_report:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'stock_report':stock_report, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Stock Value")
def stock_value(request):
    dropdown_options = []
    db = Ora()
    store_data = db.get_store_code_ST_BATCH_SEARCH_LANG_VIEW()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[2]} - {data[1]}"}
        )

    context = {
        "dropdown_options": dropdown_options,
        "user_name": request.user.username,
        "page_name": "Stock Value",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        store_code = request.POST["dropdown_options"]
        db = Ora()
        stock_value, column_name = db.get_stock_value(store_code)
        excel_file_path = excel_generator(
            page_name="Stock Value", data=stock_value, column=column_name
        )

        if not stock_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'stock_value':stock_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Bin Location OP")
def bin_location_op(request):

    dropdown_options = []
    db = Ora()
    store_data = db.get_store_code_ST_BATCH_SEARCH_LANG_VIEW()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[2]} - {data[1]}"}
        )
    context = {
        "dropdown_options": dropdown_options,
        "user_name": request.user.username,
        "page_name": "Bin Location OP",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        store_code = request.POST["dropdown_options"]
        db = Ora()
        bin_location_op_value, column_name = db.get_bin_location_op_value(store_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=bin_location_op_value,
            column=column_name,
        )

        if not bin_location_op_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'bin_location_op_value':bin_location_op_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Itemwise Storewise Stock Value")
def itemwise_storewise_stock(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Itemwise Storewise Stock Value",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        itemwise_storewise_stock_value, column_name = db.get_itemwise_storewise_stock()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=itemwise_storewise_stock_value,
            column=column_name,
        )

        if not itemwise_storewise_stock_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'itemwise_storewise_stock_value':itemwise_storewise_stock_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Batch Wise Stock Report")
def batchwise_stock_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Batch Wise Stock Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        db = Ora()
        batchwise_stock_report_value, column_name = db.get_batchwise_stock_report(
            facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=batchwise_stock_report_value,
            column=column_name,
        )

        if not batchwise_stock_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'batchwise_stock_report_value':batchwise_stock_report_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy OP Returns")
def pharmacy_op_returns(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy OP Returns",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        pharmacy_op_returns_value, column_name = db.get_pharmacy_op_returns(
            facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_op_returns_value,
            column=column_name,
        )

        if not pharmacy_op_returns_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_op_returns_value':pharmacy_op_returns_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Restricted Antimicrobials Consumption Report")
def restricted_antimicrobials_consumption_report(request):

    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    dropdown_options = []
    db = Ora()
    store_data = db.get_st_sal_hdr()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[1]} - {data[0]}"}
        )

    context = {
        "dropdown_options": dropdown_options,
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Restricted Antimicrobials Consumption Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
            store_code = request.POST["dropdown_options"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            restricted_antimicrobials_consumption_report_value,
            column_name,
        ) = db.get_restricted_antimicrobials_consumption_report(
            from_date, to_date, store_code, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=restricted_antimicrobials_consumption_report_value,
            column=column_name,
        )

        if not restricted_antimicrobials_consumption_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'restricted_antimicrobials_consumption_report_value':restricted_antimicrobials_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Itemwise Sale Report")
def pharmacy_itemwise_sale_report(request):
    dropdown_options = []

    drugs = IAACR.objects.all()
    for drug in drugs:
        dropdown_options.append(
            {"option_value": drug.drug_code, "option_name": drug.drug_name}
        )
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    dropdown_options1 = []
    db = Ora()
    store_data = db.get_DOC_TYPE_CODE_st_sal_hdr()

    for data in store_data:
        dropdown_options1.append(
            {"option_value": data[0], "option_name": f"{data[1]} - {data[0]}"}
        )

    context = {
        "dropdown_options1": dropdown_options1,
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "dropdown_options": dropdown_options,
        "user_name": request.user.username,
        "page_name": "Pharmacy Itemwise Sale Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":

        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        # Select Function from model
        drug_code = request.POST["dropdown_options"]
        store_code = request.POST["dropdown_options1"]

        db = Ora()
        (
            pharmacy_itemwise_sale_report_value,
            column_name,
        ) = db.get_pharmacy_itemwise_sale_report(
            drug_code, from_date, to_date, store_code, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_itemwise_sale_report_value,
            column=column_name,
        )

        if not pharmacy_itemwise_sale_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_itemwise_sale_report':pharmacy_itemwise_sale_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'drugs' : drugs})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Indent Report")
def pharmacy_indent_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Pharmacy Indent Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        pharmacy_indent_report_data, column_name = db.get_pharmacy_indent_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_indent_report_data,
            column=column_name,
        )

        if not pharmacy_indent_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_indent_report_data':pharmacy_indent_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - New Admission's Indents Report")
def new_admission_indents_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "New Admission’s Indents Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            new_admission_indents_report_data,
            column_name,
        ) = db.get_new_admission_indents_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=new_admission_indents_report_data,
            column=column_name,
        )

        if not new_admission_indents_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'new_admission_indents_report_data':new_admission_indents_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Return Medication Without Return Request Report")
def return_medication_without_return_request_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Return Medication Without Return Request Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            return_medication_without_return_request_report_value,
            column_name,
        ) = db.get_return_medication_without_return_request_report_value(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=return_medication_without_return_request_report_value,
            column=column_name,
        )

        if not return_medication_without_return_request_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'return_medication_without_return_request_report_value':return_medication_without_return_request_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Deleted Pharmacy Prescriptions Report")
def deleted_pharmacy_prescriptions_report(request):
    context = {
        "date_template": "date_template",
        "time_template": "time_template",
        "user_name": request.user.username,
        "page_name": "Deleted Pharmacy Prescriptions Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_time = request.POST["from_time"]
        to_time = request.POST["to_time"]

        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        from_date = from_date + " " + from_time
        to_date = to_date + " " + to_time

        db = Ora()
        (
            deleted_pharmacy_prescriptions_report_value,
            deleted_pharmacy_prescriptions_report_column_name,
        ) = db.get_deleted_pharmacy_prescriptions_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=deleted_pharmacy_prescriptions_report_value,
            column=deleted_pharmacy_prescriptions_report_column_name,
        )

        if not deleted_pharmacy_prescriptions_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'deleted_pharmacy_prescriptions_report_value':deleted_pharmacy_prescriptions_report_value, "deleted_pharmacy_prescriptions_report_column_name":deleted_pharmacy_prescriptions_report_column_name, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Direct Sales Report")
def pharmacy_direct_sales_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    dropdown_options = []
    db = Ora()
    store_data, module_id_data = db.get_store_code_st_sal_hdr()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[2]} - {data[1]}"}
        )

    dropdown_options1 = [
        {
            "option_value": module_id_data[0][0],
            "option_name": f"Module Type Pharmacy - {module_id_data[0][0]}",
        },
        {
            "option_value": module_id_data[1][0],
            "option_name": f"Module Type Inventory {module_id_data[1][0]}",
        },
    ]
    context = {
        "dropdown_options": dropdown_options,
        "dropdown_options1": dropdown_options1,
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy Direct Sales Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
            store_code = request.POST["dropdown_options"]
            module_id = request.POST["dropdown_options1"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            pharmacy_direct_sales_report_value,
            column_name,
        ) = db.get_pharmacy_direct_sales_report(
            from_date, to_date, store_code, module_id, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_direct_sales_report_value,
            column=column_name,
        )

        if not pharmacy_direct_sales_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_direct_sales_report_value':pharmacy_direct_sales_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Unf Sal")
def intransites_unf_sal(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Intransites Unf Sal",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            intransites_unf_sal_data,
            intransites_unf_sal_column_name,
        ) = db.get_intransites_unf_sal(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_unf_sal_data,
            column=intransites_unf_sal_column_name,
        )

        if not intransites_unf_sal_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_unf_sal_data':intransites_unf_sal_data, "intransites_unf_sal_column_name":intransites_unf_sal_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Unf Sal"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Confirm Pending")
def intransites_confirm_pending(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Intransites Confirm Pending",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            intransites_confirm_pending_data,
            intransites_confirm_pending_column_name,
        ) = db.get_intransites_confirm_pending()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_confirm_pending_data,
            column=intransites_confirm_pending_column_name,
        )

        if not intransites_confirm_pending_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_confirm_pending_data':intransites_confirm_pending_data, "intransites_confirm_pending_column_name":intransites_confirm_pending_column_name,'user_name':request.user.username, "page_name" : "Intransites Confirm Pending"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Non Billable Consumption")
def non_billable_consumption(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    dropdown_options = []
    db = Ora()
    store_data = db.get_store_code_ST_SAL_DTL()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[1]} - {data[0]}"}
        )

    context = {
        "dropdown_options": dropdown_options,
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Non Billable Consumption",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
            store_code = request.POST["dropdown_options"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            non_billable_consumption_data,
            non_billable_consumption_column_name,
        ) = db.get_non_billable_consumption(
            from_date, to_date, store_code, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=non_billable_consumption_data,
            column=non_billable_consumption_column_name,
        )

        if not non_billable_consumption_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'non_billable_consumption_data':non_billable_consumption_data, "non_billable_consumption_column_name":non_billable_consumption_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Non Billable Consumption"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Non Billable Consumption 1")
def non_billable_consumption1(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Non Billable Consumption 1",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            non_billable_consumption1_data,
            non_billable_consumption1_column_name,
        ) = db.get_non_billable_consumption1(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=non_billable_consumption1_data,
            column=non_billable_consumption1_column_name,
        )

        if not non_billable_consumption1_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'non_billable_consumption1_data':non_billable_consumption1_data, "non_billable_consumption1_column_name":non_billable_consumption1_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Non Billable Consumption 1"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Item Substitution Report")
def item_substitution_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Item Substitution Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        item_substitution_report_value, column_name = db.get_item_substitution_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=item_substitution_report_value,
            column=column_name,
        )

        if not item_substitution_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'item_substitution_report_value':item_substitution_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - FOC GRN Report")
def foc_grn_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "FOC GRN Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query

        db = Ora()
        foc_grn_report_value, column_name = db.get_foc_grn_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=foc_grn_report_value,
            column=column_name,
        )

        if not foc_grn_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'foc_grn_report_value':foc_grn_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Charges & Implant Pending Indent Report")
def pharmacy_charges_and_implant_pending_indent_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy Charges & Implant Pending Indent Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            pharmacy_charges_and_implant_pending_indent_report_value,
            column_name,
        ) = db.get_pharmacy_charges_and_implant_pending_indent_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_charges_and_implant_pending_indent_report_value,
            column=column_name,
        )

        if not pharmacy_charges_and_implant_pending_indent_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_charges_and_implant_pending_indent_report_value':pharmacy_charges_and_implant_pending_indent_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Direct Returns Sale Report")
def pharmacy_direct_returns_sale_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy Direct Returns Sale Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            pharmacy_direct_returns_sale_report_value,
            column_name,
        ) = db.get_pharmacy_direct_returns_sale_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_direct_returns_sale_report_value,
            column=column_name,
        )

        if not pharmacy_direct_returns_sale_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_direct_returns_sale_report_value':pharmacy_direct_returns_sale_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Current Inpatients Reports")
def current_inpatients_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Current Inpatients Reports",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        db = Ora()
        (
            current_inpatients_report_value,
            column_name,
        ) = db.get_current_inpatients_report(facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=current_inpatients_report_value,
            column=column_name,
        )

        if not current_inpatients_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'current_inpatients_report_value':current_inpatients_report_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Consigned Item Detail Report")
def consigned_item_detail_report(request):
    dropdown_options = []
    db = Ora()
    store_data = db.get_store_code_ST_SAL_DTL()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[1]} - {data[0]}"}
        )

    context = {
        "dropdown_options": dropdown_options,
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Consigned Item Detail Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        store_code = request.POST["dropdown_options"]

        db = Ora()
        (
            consigned_item_detail_report_value,
            column_name,
        ) = db.get_consigned_item_detail_report(from_date, to_date, store_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=consigned_item_detail_report_value,
            column=column_name,
        )

        if not consigned_item_detail_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'consigned_item_detail_report_value':consigned_item_detail_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Schedule H1 Drug Report")
def schedule_h1_drug_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "date_template": "date_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Schedule H1 Drug Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":

        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        # Select Function from model
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        schedule_h1_drug_report_value, column_name = db.get_schedule_h1_drug_report(
            facility_code, from_date, to_date
        )

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=schedule_h1_drug_report_value,
            column=column_name,
        )

        if not schedule_h1_drug_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'schedule_h1_drug_report_value':schedule_h1_drug_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Ward Return Requests with Status Report")
def pharmacy_ward_return_requests_with_status_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Pharmacy Ward Return Requests with Status Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":

        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        # Select Function from model
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        db = Ora()
        (
            pharmacy_ward_return_requests_with_status_report_value,
            column_name,
        ) = db.get_pharmacy_ward_return_requests_with_status_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_ward_return_requests_with_status_report_value,
            column=column_name,
        )

        if not pharmacy_ward_return_requests_with_status_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_ward_return_requests_with_status_report_value':pharmacy_ward_return_requests_with_status_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Indent Deliver Summary Report")
def pharmacy_indent_deliver_summary_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy Indent Deliver Summary Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        db = Ora()
        (
            pharmacy_indent_deliver_summary_report_value,
            column_name,
        ) = db.get_pharmacy_indent_deliver_summary_report(facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_indent_deliver_summary_report_value,
            column=column_name,
        )

        if not pharmacy_indent_deliver_summary_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_indent_deliver_summary_report_value':pharmacy_indent_deliver_summary_report_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Stk Tfr Acknowledgement Pending Report")
def intransites_stk_tfr_acknowledgement_pending(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Intransites Stk Tfr Acknowledgement Pending Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        db = Ora()
        (
            intransites_stk_tfr_acknowledgement_pending_value,
            intransites_stk_tfr_acknowledgement_pending_column_name,
        ) = db.get_intransites_stk_tfr_acknowledgement_pending(facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_stk_tfr_acknowledgement_pending_value,
            column=intransites_stk_tfr_acknowledgement_pending_column_name,
        )

        if not intransites_stk_tfr_acknowledgement_pending_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_stk_tfr_acknowledgement_pending_column_name':intransites_stk_tfr_acknowledgement_pending_column_name,'intransites_stk_tfr_acknowledgement_pending_value':intransites_stk_tfr_acknowledgement_pending_value, 'user_name':request.user.username,"page_name" : "Intransites Stk Tfr Acknowledgement Pending Report"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Folley and Central Line")
def folley_and_central_line(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Folley and Central Line",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            folley_and_central_line_data,
            folley_and_central_line_column_name,
        ) = db.get_folley_and_central_line(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=folley_and_central_line_data,
            column=folley_and_central_line_column_name,
        )

        if not folley_and_central_line_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'folley_and_central_line_data':folley_and_central_line_data, "folley_and_central_line_column_name":folley_and_central_line_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Folley and Central Line"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Angiography Kit")
def angiography_kit(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Angiography Kit",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        angiography_kit_data, angiography_kit_column_name = db.get_angiography_kit(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=angiography_kit_data,
            column=angiography_kit_column_name,
        )

        if not angiography_kit_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'angiography_kit_data':angiography_kit_data, "angiography_kit_column_name":angiography_kit_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Angiography Kit"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Search Indents By Code")
def search_indents_by_code(request):
    dropdown_options = [
        {
            "option_value": "CP00",
            "option_name": "CP Pharmacy",
        }
    ]
    context = {
        "dropdown_options": dropdown_options,
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Search Indents By Code",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        location_code = request.POST["dropdown_options"]
        db = Ora()

        (
            search_indents_by_code_data,
            search_indents_by_code_column_name,
        ) = db.get_search_indents_by_code(from_date, location_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=search_indents_by_code_data,
            column=search_indents_by_code_column_name,
        )

        if not search_indents_by_code_data:
            context["error"] = "Sorry!!! No Data Found"
            return (render(request, "reports/one_for_all.html", context),)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'search_indents_by_code_data':search_indents_by_code_data, "search_indents_by_code_column_name":search_indents_by_code_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Angiography Kit"})


@login_required(login_url="login")
@allowed_users("Pharmacy - New Admission Dispense Report")
def new_admission_dispense_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "New Admission Dispense Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            new_admission_dispense_report_data,
            column_name,
        ) = db.get_new_admission_dispense_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=new_admission_dispense_report_data,
            column=column_name,
        )

        if not new_admission_dispense_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'new_admission_dispense_report_data':new_admission_dispense_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy OP Sale Report Userwise")
def pharmacy_op_sale_report_userwise(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    dropdown_options = []
    db = Ora()
    store_data = db.get_doc_type_code_BL_BILL_HDR()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[1]} - {data[0]}"}
        )

    dropdown_options1 = [
        {"option_value": "AK", "option_name": "Cash Counters OF Akola"},
        {"option_value": "GO", "option_name": "Cash Counters OF Gondia"},
        {"option_value": "IN", "option_name": "Cash Counters OF Indore"},
        {"option_value": "AN", "option_name": "KH - AN"},
        {"option_value": "BD", "option_name": "KH - BD"},
        {"option_value": "C", "option_name": "KH - C"},
        {"option_value": "CA", "option_name": "KH - CA"},
        {"option_value": "MZ", "option_name": "KH - MZ"},
        {"option_value": "PH", "option_name": "KH - PH"},
        {"option_value": "RH", "option_name": "Cash Counters OF Navi Mumbai RH"},
        {"option_value": "SL", "option_name": "Cash Counters OF Solapur"},
    ]

    context = {
        "dropdown_options1": dropdown_options1,
        "dropdown_options": dropdown_options,
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy OP Sale Report Userwise",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
            store_code = request.POST["dropdown_options"]
            cash_counter = request.POST["dropdown_options1"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            pharmacy_op_sale_report_userwise_value,
            column_name,
        ) = db.get_pharmacy_op_sale_report_userwise(
            from_date, to_date, store_code, cash_counter, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_op_sale_report_userwise_value,
            column=column_name,
        )

        if not pharmacy_op_sale_report_userwise_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_op_sale_report_userwise_value':pharmacy_op_sale_report_userwise_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Pharmacy Consumption Report")
def pharmacy_consumption_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy Consumption Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            pharmacy_consumption_report_value,
            column_name,
        ) = db.get_pharmacy_consumption_report(from_date, to_date, facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pharmacy_consumption_report_value,
            column=column_name,
        )

        if not pharmacy_consumption_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pharmacy_consumption_report_value':pharmacy_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Food-Drug Interaction Report")
def food_drug_interaction_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Food-Drug Interaction Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            food_drug_interaction_report_value,
            column_name,
        ) = db.get_food_drug_interaction_report(facility_code, from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=food_drug_interaction_report_value,
            column=column_name,
        )

        if not food_drug_interaction_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'food_drug_interaction_report_value':food_drug_interaction_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransite Stock")
def intransite_stock(request):
    dropdown_options = []
    db = Ora()
    store_data = db.get_store_code_st_item_batch()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[2]} - {data[1]}"}
        )

    context = {
        "dropdown_options": dropdown_options,
        "user_name": request.user.username,
        "page_name": "Intransite Stock",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        store_code = request.POST["dropdown_options"]
        db = Ora()
        intransite_stock_data, column_name = db.get_intransite_stock(store_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransite_stock_data,
            column=column_name,
        )

        if not intransite_stock_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransite_stock_data':intransite_stock_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Pharmacy - GRN Data")
def grn_data(request):
    dropdown_options = []
    all_dropdown_options = {"ALL": " "}
    db = Ora()
    store_code = db.get_st_grn_hdr_store_code()
    for data in store_code:
        dropdown_options.append(
            {
                "option_value": f"'{data[0]}'",
                "option_name": f"{data[1]} - {data[2]}",
            }
        )
        all_dropdown_options["ALL"] = all_dropdown_options["ALL"] + f"'{data[0]}',"

    all_dropdown_options["ALL"] = all_dropdown_options["ALL"][:-1]

    dropdown_options.append(
        {
            "option_value": all_dropdown_options["ALL"],
            "option_name": "ALL",
        }
    )

    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facilities": facility,
        "facility_template": "facility_template",
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "GRN Data",
        "date_form": DateForm(),
        "dropdown_options": dropdown_options,
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        store_code_ph = request.POST["dropdown_options"]
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        grn_data_value, column_name = db.get_grn_data(
            from_date, to_date, facility_code, store_code_ph
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=grn_data_value, column=column_name
        )

        if not grn_data_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'grn_data_value':grn_data_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Drug Duplication Override Report")
def drug_duplication_override_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Drug Duplication Override Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            drug_duplication_override_report_value,
            column_name,
        ) = db.get_drug_duplication_override_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=drug_duplication_override_report_value,
            column=column_name,
        )

        if not drug_duplication_override_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'drug_duplication_override_report_value':drug_duplication_override_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Drug Interaction Override Report")
def drug_interaction_override_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Drug Interaction Override Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            drug_interaction_override_report_value,
            column_name,
        ) = db.get_drug_interaction_override_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=drug_interaction_override_report_value,
            column=column_name,
        )

        if not drug_interaction_override_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'drug_interaction_override_report_value':drug_interaction_override_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Sale Consumption Report")
def sale_consumption_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Sale Consumption Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        sale_consumption_report_value, column_name = db.get_sale_consumption_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=sale_consumption_report_value,
            column=column_name,
        )

        if not sale_consumption_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'sale_consumption_report_value':sale_consumption_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Sale Consumption Report 1")
def sale_consumption_report1(request):
    input_tags = {"Month", "Year"}
    context = {
        "input_tags": input_tags,
        "user_name": request.user.username,
        "page_name": "Sale Consumption Report 1",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        try:
            month = request.POST["Month"]
            year = request.POST["Year"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Enter a Month and a Year"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        sale_consumption_report1_value, column_name = db.get_sale_consumption_report1(
            month, year
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=sale_consumption_report1_value,
            column=column_name,
        )

        if not sale_consumption_report1_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'sale_consumption_report1_value':sale_consumption_report1_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - New Code Creation")
def new_code_creation(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "New Code Creation",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            new_code_creation_data,
            new_code_creation_data_column_name,
        ) = db.get_new_code_creation(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=new_code_creation_data,
            column=new_code_creation_data_column_name,
        )

        if not new_code_creation_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {"date_form": DateForm(),'new_code_creation_data':new_code_creation_data,"new_code_creation_data_column_name":new_code_creation_data_column_name, 'user_name':request.user.username,"page_name" : "Predischarge Initiate"})


@login_required(login_url="login")
@allowed_users("Pharmacy - TVD CABG Request")
def tvd_cabg_request(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pharmacy - TVD CABG Request",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            tvd_cabg_request_data,
            tvd_cabg_request_data_column_name,
        ) = db.get_tvd_cabg_request(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=tvd_cabg_request_data,
            column=tvd_cabg_request_data_column_name,
        )

        if not tvd_cabg_request_data:
            context["error"] = ("Sorry!!! No Data Found",)
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {"date_form": DateForm(),'tvd_cabg_request_data':tvd_cabg_request_data,"tvd_cabg_request_data_column_name":new_code_creation_data_column_name, 'user_name':request.user.username,"page_name" : "Predischarge Initiate"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Stock Amount-Wise")
def stock_amount_wise(request):
    dropdown_options = []
    db = Ora()
    store_data = db.get_store_code_ST_BATCH_SEARCH_LANG_VIEW()

    for data in store_data:
        dropdown_options.append(
            {"option_value": data[0], "option_name": f"{data[2]} - {data[1]}"}
        )

    input_tags = {"From Amount", "To Amount"}

    context = {
        "input_tags": input_tags,
        "user_name": request.user.username,
        "page_name": "Stock Amount-Wise",
        "date_form": DateForm(),
        "dropdown_options": dropdown_options,
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":

        from_amount = request.POST["From"]
        to_amount = request.POST["To"]
        store_code = request.POST["dropdown_options"]

        db = Ora()
        (
            stock_amount_wise_data,
            stock_amount_wise_column_name,
        ) = db.get_stock_amount_wise(from_amount, to_amount, store_code)

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=stock_amount_wise_data,
            column=stock_amount_wise_column_name,
        )

        if not stock_amount_wise_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'stock_amount_wise_data':stock_amount_wise_data, "stock_amount_wise_column_name":stock_amount_wise_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Pharmacy - Intransites Acknowledgement Pending ISS RT"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Dept Issue Pending Tracker")
def dept_issue_pending_tracker(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Dept Issue Pending Tracker",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            dept_issue_pending_tracker_data,
            dept_issue_pending_tracker_column_name,
        ) = db.get_dept_issue_pending_tracker(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=dept_issue_pending_tracker_data,
            column=dept_issue_pending_tracker_column_name,
        )

        if not dept_issue_pending_tracker_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'dept_issue_pending_tracker_data':dept_issue_pending_tracker_data, "dept_issue_pending_tracker_column_name":dept_issue_pending_tracker_column_name,'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Patient Indent Count")
def patient_indent_count(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Patient Indent Count",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        patient_indent_count_value, column_name = db.get_patient_indent_count(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=patient_indent_count_value,
            column=column_name,
        )

        if not patient_indent_count_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'patient_indent_count_


@login_required(login_url="login")
@allowed_users("Pharmacy - Predischarge Medication")
def predischarge_medication(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Predischarge Medication",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            predischarge_medication_data,
            predischarge_medication_column_name,
        ) = db.get_predischarge_medication(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=predischarge_medication_data,
            column=predischarge_medication_column_name,
        )

        if not predischarge_medication_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'predischarge_medication_data':predischarge_medication_data, "predischarge_medication_column_name":predischarge_medication_column_name,'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Pharmacy - Predischarge Initiate")
def predischarge_initiate(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Predischarge Initiate",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            predischarge_initiate_data,
            predischarge_initiate_data_column_name,
        ) = db.get_predischarge_initiate()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=predischarge_initiate_data,
            column=predischarge_initiate_data_column_name,
        )

        if not predischarge_initiate_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'predischarge_initiate_data':predischarge_initiate_data,"predischarge_initiate_data_column_name":predischarge_initiate_data_column_name, 'user_name':request.user.username,"page_name" : "Predischarge Initiate"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Unf Sal Ret")
def intransites_unf_sal_ret(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Intransites Unf Sal Ret",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            intransites_unf_sal_ret_data,
            intransites_unf_sal_ret_column_name,
        ) = db.get_intransites_unf_sal_ret(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_unf_sal_ret_data,
            column=intransites_unf_sal_ret_column_name,
        )

        if not intransites_unf_sal_ret_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_unf_sal_ret_data':intransites_unf_sal_ret_data, "intransites_unf_sal_ret_column_name":intransites_unf_sal_ret_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Unf Sal Ret"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Unf Stk Tfr")
def intransites_unf_stk_tfr(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Intransites Unf Stk Tfr",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            intransites_unf_stk_tfr_data,
            intransites_unf_stk_tfr_column_name,
        ) = db.get_intransites_unf_stk_tfr(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_unf_stk_tfr_data,
            column=intransites_unf_stk_tfr_column_name,
        )

        if not intransites_unf_stk_tfr_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_unf_stk_tfr_data':intransites_unf_stk_tfr_data, "intransites_unf_stk_tfr_column_name":intransites_unf_stk_tfr_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Unf Stk Tfr"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Acknowledgement Pending ISS")
def intransites_acknowledgement_pending_iss(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Intransites Acknowledgement Pending ISS",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            intransites_acknowledgement_pending_iss_data,
            intransites_acknowledgement_pending_iss_column_name,
        ) = db.get_intransites_acknowledgement_pending_iss()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_acknowledgement_pending_iss_data,
            column=intransites_acknowledgement_pending_iss_column_name,
        )

        if not intransites_acknowledgement_pending_iss_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_acknowledgement_pending_iss_data':intransites_acknowledgement_pending_iss_data, "intransites_acknowledgement_pending_iss_column_name":intransites_acknowledgement_pending_iss_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Intransites Acknowledgement Pending ISS"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Intransites Acknowledgement Pending ISS RT")
def intransites_acknowledgement_pending_iss_rt(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Pharmacy - Intransites Acknowledgement Pending ISS RT",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            intransites_acknowledgement_pending_iss_rt_data,
            intransites_acknowledgement_pending_iss_rt_column_name,
        ) = db.get_intransites_acknowledgement_pending_iss_rt()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=intransites_acknowledgement_pending_iss_rt_data,
            column=intransites_acknowledgement_pending_iss_rt_column_name,
        )

        if not intransites_acknowledgement_pending_iss_rt_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'intransites_acknowledgement_pending_iss_rt_data':intransites_acknowledgement_pending_iss_rt_data, "intransites_acknowledgement_pending_iss_rt_column_name":intransites_acknowledgement_pending_iss_rt_column_name,'user_name':request.user.username,'date_form' : DateForm(), "page_name" : "Pharmacy - Intransites Acknowledgement Pending ISS RT"})


@login_required(login_url="login")
@allowed_users("Pharmacy - Narcotic Stock Report")
def narcotic_stock_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Narcotic Stock Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            narcotic_stock_report_data,
            narcotic_stock_report_data_column_name,
        ) = db.get_narcotic_stock_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=narcotic_stock_report_data,
            column=narcotic_stock_report_data_column_name,
        )

        if not narcotic_stock_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'narcotic_stock_report_data':narcotic_stock_report_data,"narcotic_stock_report_data_column_name":narcotic_stock_report_data_column_name, 'user_name':request.user.username,"page_name" : "Predischarge Initiate"})


# Finance Reports


@login_required(login_url="login")
@allowed_users("Finance - Credit Bill Outstanding")
def credit_outstanding_bill(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Credit Outstanding Bill",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            credit_outstanding_bill_value,
            column_name,
        ) = db.get_credit_outstanding_bill_value(facility_code, from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=credit_outstanding_bill_value,
            column=column_name,
        )

        if not credit_outstanding_bill_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'credit_outstanding_bill_value':credit_outstanding_bill_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - TPA Letter")
def tpa_letter(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "TPA Letter",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        tpa_letter_value, column_name = db.get_tpa_letter(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=tpa_letter_value, column=column_name
        )

        if not tpa_letter_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'tpa_letter_value':tpa_letter_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Online Consultation Report")
def online_consultation_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Online Consultation Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            online_consultation_report_value,
            column_name,
        ) = db.get_online_consultation_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=online_consultation_report_value,
            column=column_name,
        )

        if not online_consultation_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'online_consultation_report_value':online_consultation_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Finance - Contract Reports")
def contract_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Contract Reports",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        contract_report_data, column_name = db.get_contract_report(facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=contract_report_data,
            column=column_name,
        )

        if not contract_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'contract_report_data':contract_report_data, 'user_name':request.user.username,'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Admission Census")
def admission_census(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Admission Census",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        admission_census_value, column_name = db.get_admission_census(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=admission_census_value,
            column=column_name,
        )

        if not admission_census_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'admission_census_value':admission_census_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Card")
def card(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Card",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/__.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        card_value, column_name = db.get_card(from_date, to_date, facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=card_value,
            column=column_name,
        )

        if not card_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'card_value':card_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Patient-Wise Bill Details")
def patientwise_bill_details(request):
    dropdown_options = [
        {
            "option_value": "('O')",
            "option_name": "Outpatient",
        },
        {
            "option_value": "('E')",
            "option_name": "Emergency",
        },
        {
            "option_value": "('R')",
            "option_name": "External",
        },
        {
            "option_value": "('I')",
            "option_name": "Inpatient",
        },
        {
            "option_value": ("O", "E", "R", "I"),
            "option_name": "All",
        },
    ]

    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    textbox = {"UHID", "Episode ID"}
    context = {
        "textbox": textbox,
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Patient-Wise Bill Details",
        "dropdown_options": dropdown_options,
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
            episode_code = request.POST["dropdown_options"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        # Convert and Split all Episode and UHID with commer separated values and then to tuple example : ('KH1000', 'KH1000')
        episode_id = request.POST["Episode ID"]
        episode_id = tuple(episode_id.split())
        if len(episode_id) == 1:
            episode_id = f"('{episode_id[0]}')"

        uhid = request.POST["UHID"]
        uhid = tuple(uhid.split())
        if len(uhid) == 1:
            uhid = f"('{uhid[0]}')"

        db = Ora()
        (patientwise_bill_details_data, column_name,) = db.get_patientwise_bill_details(
            uhid, episode_id, facility_code, episode_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=patientwise_bill_details_data,
            column=column_name,
        )

        if not patientwise_bill_details_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'patientwise_bill_details_data':patientwise_bill_details_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - Package Contract Report")
def package_contract_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Package Contract Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        package_contract_report_value, column_name = db.get_package_contract_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=package_contract_report_value,
            column=column_name,
        )

        if not package_contract_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'package_contract_report_value':package_contract_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Credit Card Reconciliation Report")
def credit_card_reconciliation_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Credit Card Reconciliation Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            credit_card_reconciliation_report_value,
            column_name,
        ) = db.get_credit_card_reconciliation_report(facility_code, from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=credit_card_reconciliation_report_value,
            column=column_name,
        )

        if not credit_card_reconciliation_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'credit_card_reconciliation_report_value':credit_card_reconciliation_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Covid OT Surgery Details")
def covid_ot_surgery_details(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Covid OT Surgery Details",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        covid_ot_surgery_details_value, column_name = db.get_covid_ot_surgery_details(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=covid_ot_surgery_details_value,
            column=column_name,
        )

        if not covid_ot_surgery_details_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'covid_ot_surgery_details_value':covid_ot_surgery_details_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - GST Data of Pharmacy")
def gst_data_of_pharmacy(request):
    context = {
        "user_name": request.user.username,
        "page_name": "GST Data of Pharmacy",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        gst_data_of_pharmacy_data, column_name = db.get_gst_data_of_pharmacy()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=gst_data_of_pharmacy_data,
            column=column_name,
        )

        if not gst_data_of_pharmacy_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'gst_data_of_pharmacy_data':gst_data_of_pharmacy_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - Cathlab")
def cathlab(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Cathlab",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        cathlab_value, column_name = db.get_cathlab(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=cathlab_value,
            column=column_name,
        )

        if not cathlab_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'cathlab_value':cathlab_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Finance - Form 61")
def form_61(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_template": "facility_template",
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Form 61",
        "date_form": DateForm(),
    }

    if request.method == "GET":

        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        # Select Function from model
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        form_61_value, column_name = db.get_form_61(facility_code, from_date, to_date)

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=form_61_value,
            column=column_name,
        )

        if not form_61_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'form_61_value':form_61_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Packages Applied To Patients")
def packages_applied_to_patients(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_template": "facility_template",
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Packages Applied To Patients",
        "date_form": DateForm(),
    }

    if request.method == "GET":

        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        # Select Function from model
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            packages_applied_to_patients_value,
            column_name,
        ) = db.get_packages_applied_to_patients(facility_code, from_date, to_date)

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=packages_applied_to_patients_value,
            column=column_name,
        )

        if not packages_applied_to_patients_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'packages_applied_to_patients_value':packages_applied_to_patients_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - GST Data of Pharmacy Return")
def gst_data_of_pharmacy_return(request):
    context = {
        "user_name": request.user.username,
        "page_name": "GST Data of Pharmacy Return",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            gst_data_of_pharmacy_return_data,
            column_name,
        ) = db.get_gst_data_of_pharmacy_return()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=gst_data_of_pharmacy_return_data,
            column=column_name,
        )

        if not gst_data_of_pharmacy_return_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'gst_data_of_pharmacy_return_data':gst_data_of_pharmacy_return_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - GST Data of IP")
def gst_data_of_ip(request):
    context = {
        "user_name": request.user.username,
        "page_name": "GST Data of IP",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        gst_data_of_ip_data, column_name = db.get_gst_data_of_ip()
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=gst_data_of_ip_data, column=column_name
        )

        if not gst_data_of_ip_data:
            context["error"] = "Sorry!!! No Data Found"

            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'gst_data_of_ip_data':gst_data_of_ip_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - GST Data of OP")
def gst_data_of_op(request):
    context = {
        "user_name": request.user.username,
        "page_name": "GST Data of OP",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        gst_data_of_op_data, column_name = db.get_gst_data_of_op()
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=gst_data_of_op_data, column=column_name
        )

        if not gst_data_of_op_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'gst_data_of_op_data':gst_data_of_op_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - OT")
def ot(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "OT",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        ot_value, column_name = db.get_ot(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ot_value,
            column=column_name,
        )

        if not ot_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ot_value':ot_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Discharge Census")
def discharge_census(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Discharge Census",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        discharge_census_value, column_name = db.get_discharge_census(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=discharge_census_value,
            column=column_name,
        )

        if not discharge_census_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'discharge_census_value':discharge_census_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - GST IPD")
def gst_ipd(request):
    context = {
        "user_name": request.user.username,
        "page_name": "GST IPD",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":

        db = Ora()
        gst_ipd_value, column_name = db.get_gst_ipd()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=gst_ipd_value,
            column=column_name,
        )

        if not gst_ipd_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/gst_ipd.html', {'gst_ipd_value':gst_ipd_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Revenue Data of SL")
def revenue_data_of_sl(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Revenue Data of SL",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        revenue_data_of_sl_data, column_name = db.get_revenue_data_of_sl()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=revenue_data_of_sl_data,
            column=column_name,
        )

        if not revenue_data_of_sl_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'revenue_data_of_sl_data':revenue_data_of_sl_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - Revenue Data of SL 1")
def revenue_data_of_sl1(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Revenue Data of SL 1",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        revenue_data_of_sl1_data, column_name = db.get_revenue_data_of_sl1()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=revenue_data_of_sl1_data,
            column=column_name,
        )

        if not revenue_data_of_sl1_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'revenue_data_of_sl1_data':revenue_data_of_sl1_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - Revenue Data of SL 2")
def revenue_data_of_sl2(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Revenue Data of SL 2",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        revenue_data_of_sl2_data, column_name = db.get_revenue_data_of_sl2()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=revenue_data_of_sl2_data,
            column=column_name,
        )

        if not revenue_data_of_sl2_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'revenue_data_of_sl2_data':revenue_data_of_sl2_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Finance - Revenue Data of SL 3")
def revenue_data_of_sl3(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Revenue Data of SL 3",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        revenue_data_of_sl3_value, column_name = db.get_revenue_data_of_sl3(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=revenue_data_of_sl3_value,
            column=column_name,
        )

        if not revenue_data_of_sl3_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'revenue_data_of_sl3_value':revenue_data_of_sl3_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Revenue JV")
def revenue_jv(request):
    dropdown_options = [
        {
            "option_value": "revenue_data",
            "option_name": "Revenue Data [0]",
        },
        {
            "option_value": "revenue_data1",
            "option_name": "Revenue Data 1",
        },
        {
            "option_value": "revenue_data2",
            "option_name": "Revenue Data 2",
        },
    ]
    context = {
        "user_name": request.user.username,
        "page_name": "Revenue JV",
        "dropdown_options": dropdown_options,
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            revenue_data = request.POST["dropdown_options"]
        except:
            context["error"] = "Please Select The Dropdown Field"
            return render(request, "reports/one_for_all.html", context)
        db = Ora()
        revenue_jv_value, column_name = db.get_revenue_jv(revenue_data)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=revenue_jv_value,
            column=column_name,
        )

        if not revenue_jv_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'revenue_jv_value':revenue_jv_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Finance - Collection Report")
def collection_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "date_template": "date_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Collection Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":

        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        # Select Function from model
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        collection_report_value, column_name = db.get_collection_report(
            facility_code, from_date, to_date
        )

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=collection_report_value,
            column=column_name,
        )

        if not collection_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'collection_report_value':collection_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Pre Discharge Report")
def pre_discharge_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Pre Discharge Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        pre_discharge_report_value, column_name = db.get_pre_discharge_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pre_discharge_report_value,
            column=column_name,
        )

        if not pre_discharge_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'pre_discharge_report_value':pre_discharge_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Pre Discharge Report 2")
def pre_discharge_report_2(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Pre Discharge Report 2",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        pre_discharge_report_2_data, column_name = db.get_pre_discharge_report_2()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=pre_discharge_report_2_data,
            column=column_name,
        )

        if not pre_discharge_report_2_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'pre_discharge_report_2_data':pre_discharge_report_2_data, 'user_name':request.user.username,})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Discharge Report 2")
def discharge_report_2(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Discharge Report 2",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        discharge_report_2_value, column_name = db.get_discharge_report_2(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=discharge_report_2_value,
            column=column_name,
        )

        if not discharge_report_2_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'discharge_report_2_value':discharge_report_2_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Discharge With MIS Report")
def discharge_with_mis_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Discharge With MIS Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        discharge_with_mis_report_value, column_name = db.get_discharge_with_mis_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=discharge_with_mis_report_value,
            column=column_name,
        )

        if not discharge_with_mis_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'discharge_with_mis_report_value':discharge_with_mis_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Needle Prick Injury Report")
def needle_prick_injury_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Needle Prick Injury Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            needle_prick_injury_report_value,
            column_name,
        ) = db.get_needle_prick_injury_report(facility_code, from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=needle_prick_injury_report_value,
            column=column_name,
        )

        if not needle_prick_injury_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'needle_prick_injury_report_value':needle_prick_injury_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Practo Report")
def practo_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Practo Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        practo_report_value, column_name = db.get_practo_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=practo_report_value, column=column_name
        )

        if not practo_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'practo_report_value':practo_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Unbilled Report")
def unbilled_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Unbilled Report",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        unbilled_report_data, column_name = db.get_unbilled_report(facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=unbilled_report_data,
            column=column_name,
        )

        if not unbilled_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'unbilled_report_data':unbilled_report_data, 'user_name':request.user.username,'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Unbilled Deposit Report")
def unbilled_deposit_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Unbilled Deposit Report",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        unbilled_deposit_report_data, column_name = db.get_unbilled_deposit_report(
            facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=unbilled_deposit_report_data,
            column=column_name,
        )

        if not unbilled_deposit_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'unbilled_deposit_report_data':unbilled_deposit_report_data, 'user_name':request.user.username,'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Contact Report")
def contact_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Contact Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        contact_report_value, column_name = db.get_contact_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=contact_report_value,
            column=column_name,
        )

        if not contact_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'contact_report_value':contact_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Current Inpatients Employee and Dependants")
def current_inpatients_employee_and_dependants(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Current Inpatients Employee and Dependants",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            current_inpatients_employee_and_dependants_value,
            column_name,
        ) = db.get_current_inpatients_employee_and_dependants(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=current_inpatients_employee_and_dependants_value,
            column=column_name,
        )

        if not current_inpatients_employee_and_dependants_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'current_inpatients_employee_and_dependants_value':current_inpatients_employee_and_dependants_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Treatment Sheet Data")
def treatment_sheet_data(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Treatment Sheet Data",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        treatment_sheet_data_data, column_name = db.get_treatment_sheet_data()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=treatment_sheet_data_data,
            column=column_name,
        )

        if not treatment_sheet_data_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                {"error": "Sorry!!! No Data Found", "user_name": request.user.username},
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'treatment_sheet_data_data':treatment_sheet_data_data, 'user_name':request.user.username,})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Employees Antibodies Reactive Report")
def employees_antibodies_reactive_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Employees Antibodies Reactive Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"

        db = Ora()
        (
            employees_antibodies_reactive_report_value,
            column_name,
        ) = db.get_employees_antibodies_reactive_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=employees_antibodies_reactive_report_value,
            column=column_name,
        )

        if not employees_antibodies_reactive_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'employees_antibodies_reactive_report_value':employees_antibodies_reactive_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Employee Reactive and Non PCR Report")
def employees_reactive_and_non_pcr_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Employee Reactive and Non PCR Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            employees_reactive_and_non_pcr_report_value,
            column_name,
        ) = db.get_employees_reactive_and_non_pcr_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=employees_reactive_and_non_pcr_report_value,
            column=column_name,
        )

        if not employees_reactive_and_non_pcr_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'employees_reactive_and_non_pcr_report_value':employees_reactive_and_non_pcr_report_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Employee Covid Test Report")
def employee_covid_test_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Employee Covid Test Report",
        "date_form": DateForm(),
        "facilities": facility,
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            employee_covid_test_report_value,
            column_name,
        ) = db.get_employee_covid_test_report(facility_code, from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=employee_covid_test_report_value,
            column=column_name,
        )

        if not employee_covid_test_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'employee_covid_test_report_value':employee_covid_test_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Bed Location Report")
def bed_location_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Bed Location Report",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        bed_location_report_data, column_name = db.get_bed_location_report(
            facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=bed_location_report_data,
            column=column_name,
        )

        if not bed_location_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)
        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'bed_location_report_data':bed_location_report_data, 'user_name':request.user.username,'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Home Visit Report")
def home_visit_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Home Visit Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        home_visit_report_value, column_name = db.get_home_visit_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=home_visit_report_value,
            column=column_name,
        )

        if not home_visit_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'home_visit_report_value':home_visit_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - CCO Billing Count Report")
def cco_billing_count_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "CCO Billing Count Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        db = Ora()
        (
            cco_billing_count_report_data,
            cco_billing_count_report_column_name,
        ) = db.get_cco_billing_count_reports(from_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=cco_billing_count_report_data,
            column=cco_billing_count_report_column_name,
        )

        if not cco_billing_count_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'cco_billing_count_report_data':cco_billing_count_report_data,"cco_billing_count_report_column_name":cco_billing_count_report_column_name, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users(
    "Clinical Administration - Total Number of Online Consultation by Doctors"
)
def total_number_of_online_consultation_by_doctors(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Total Number of Online Consultation by Doctors",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        db = Ora()
        (
            total_number_of_online_consultation_by_doctors_value,
            column_name,
        ) = db.get_total_number_of_online_consultation_by_doctors(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=total_number_of_online_consultation_by_doctors_value,
            column=column_name,
        )

        if not total_number_of_online_consultation_by_doctors_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'total_number_of_online_consultation_by_doctors_value':total_number_of_online_consultation_by_doctors_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - TPA Current Inpatients")
def tpa_current_inpatients(request):
    context = {
        "user_name": request.user.username,
        "page_name": "TPA Current Inpatients",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        tpa_current_inpatients_data, column_name = db.get_tpa_current_inpatients()
        # excel_file_path = excel_generator(        #     page_name="TPA Current Inpatients",        #     data=tpa_current_inpatients_data,       #     column=column_name,        # )

        if not tpa_current_inpatients_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            pd_dataframe = pd.DataFrame(
                data=tpa_current_inpatients_data, columns=list(column_name)
            )
            return HttpResponse(pd_dataframe.to_html())
            # return FileResponse(            #     open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"            # )
            # context["pd_dataframe"] = pd_dataframe.to_html(header="TPA Current Inpatients")
            # return render(request, "reports/one_for_all.html", context)


@login_required(login_url="login")
@allowed_users("Clinical Administration - TPA Cover Letter")
def tpa_cover_letter(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "TPA Cover Letter",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            tpa_cover_letter_value,
            column_name,
        ) = db.get_tpa_cover_letter(from_date, to_date)
        system_os = platform.system()
        if system_os == "Linux":
            excel_file_path = excel_generator(
                data=tpa_cover_letter_value,
                column=column_name,
                page_name=context["page_name"],
            )
        else:
            excel_file_path = excel_generator_tpa(
                data=tpa_cover_letter_value,
                column=column_name,
                page_name=context["page_name"],
            )

        if not tpa_cover_letter_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'tpa_cover_letter_value':tpa_cover_letter_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Total Number of IP Patients by Doctors")
def total_number_of_ip_patients_by_doctors(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Total Number of IP Patients by Doctors",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            total_number_of_ip_patients_by_doctors_value,
            column_name,
        ) = db.get_total_number_of_ip_patients_by_doctors(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=total_number_of_ip_patients_by_doctors_value,
            column=column_name,
        )

        if not total_number_of_ip_patients_by_doctors_value:
            context["error"] = "Sorry!!! No Data Found"

            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'total_number_of_ip_patients_by_doctors_value':total_number_of_ip_patients_by_doctors_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Total Number of OP Patients by Doctors")
def total_number_of_op_patients_by_doctors(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Total Number of OP Patients by Doctors",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            total_number_of_op_patients_by_doctors_value,
            column_name,
        ) = db.get_total_number_of_op_patients_by_doctors(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=total_number_of_op_patients_by_doctors_value,
            column=column_name,
        )

        if not total_number_of_op_patients_by_doctors_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'total_number_of_op_patients_by_doctors_value':total_number_of_op_patients_by_doctors_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - OPD Changes Report")
def opd_changes_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "OPD Changes Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        opd_changes_report_value, column_name = db.get_opd_changes_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=opd_changes_report_value,
            column=column_name,
        )

        if not opd_changes_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'opd_changes_report_value':opd_changes_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - EHC Conversion Report")
def ehc_conversion_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "EHC Conversion Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        ehc_conversion_report_value, column_name = db.get_ehc_conversion_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ehc_conversion_report_value,
            column=column_name,
        )

        if not ehc_conversion_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ehc_conversion_report_value':ehc_conversion_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - EHC Package Range Report")
def ehc_package_range_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "EHC Package Range Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        ehc_package_range_report_value, column_name = db.get_ehc_package_range_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ehc_package_range_report_value,
            column=column_name,
        )

        if not ehc_package_range_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ehc_package_range_report_value':ehc_package_range_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Error Report")
def error_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Error Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        error_report_value, column_name = db.get_error_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=error_report_value, column=column_name
        )

        if not error_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'error_report_value':error_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - OT Query Report")
def ot_query_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "OT Query Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        ot_query_report_value, column_name = db.get_ot_query_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ot_query_report_value,
            column=column_name,
        )

        if not ot_query_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ot_query_report_value':ot_query_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Outreach Cancer Hospital")
def outreach_cancer_hospital(request):

    context = {
        "date_template": "date_template",
        "page_name": "Outreach Cancer Hospital",
        "user_name": request.user.username,
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        outreach_cancer_hospital_value, column_name = db.get_outreach_cancer_hospital(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=outreach_cancer_hospital_value,
            column=column_name,
        )

        if not outreach_cancer_hospital_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,ot_query_report_value':ot_query_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - GIPSA Report")
def gipsa_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "GIPSA Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        gipsa_report_data, column_name = db.get_gipsa_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=gipsa_report_data, column=column_name
        )

        if not gipsa_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'gipsa_report_data':gipsa_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users(
    "Clinical Administration - Precision Patient OPD & Online Consultation List Report"
)
def precision_patient_opd_and_online_consultation_list_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Precision Patient OPD & Online Consultation List Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            precision_patient_opd_and_online_consultation_list_report_value,
            column_name,
        ) = db.get_precision_patient_opd_and_online_consultation_list_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=precision_patient_opd_and_online_consultation_list_report_value,
            column=column_name,
        )

        if not precision_patient_opd_and_online_consultation_list_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'precision_patient_opd_and_online_consultation_list_report_value':precision_patient_opd_and_online_consultation_list_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Appointment Details By Call Center Report")
def appointment_details_by_call_center_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Appointment Details By Call Center Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            appointment_details_by_call_center_report_value,
            column_name,
        ) = db.get_appointment_details_by_call_center_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=appointment_details_by_call_center_report_value,
            column=column_name,
        )

        if not appointment_details_by_call_center_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'appointment_details_by_call_center_report_value':appointment_details_by_call_center_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - TRF Report")
def trf_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "TRF Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        trf_report_value, column_name = db.get_trf_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=trf_report_value, column=column_name
        )

        if not trf_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'trf_report_value':trf_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Current Inpatients(Clinical Admin)")
def current_inpatients_clinical_admin(request):
    dropdown_options = [
        {
            "option_value": "*",
            "option_name": "ALL",
        },
        {
            "option_value": "CASH",
            "option_name": "TPA",
        },
        {
            "option_value": "dietitian",
            "option_name": "For Dietitians",
        },
    ]

    context = {
        "dropdown_options": dropdown_options,
        "user_name": request.user.username,
        "page_name": "Current Inpatients(Clinical Admin)",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            billing_group = request.POST["dropdown_options"]

        except MultiValueDictKeyError:
            billing_group = "*"

        db = Ora()
        (
            current_inpatients_clinical_admin_data,
            column_name,
        ) = db.get_current_inpatients_clinical_admin(billing_group)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=current_inpatients_clinical_admin_data,
            column=column_name,
        )
        context["column_name"] = column_name

        if not current_inpatients_clinical_admin_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'current_inpatients_clinical_admin_data':current_inpatients_clinical_admin_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Check Patient Registration Date")
def check_patient_registration_date(request):

    input_tags = {"UHID"}
    context = {
        "input_tags": input_tags,
        "user_name": request.user.username,
        "page_name": "Check Patient Registration Date",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        uhid = request.POST["UHID"].upper()
        db = Ora()
        (
            check_patient_registration_date_data,
            column_name,
        ) = db.get_check_patient_registration_date(uhid)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=check_patient_registration_date_data,
            column=column_name,
        )

        if not check_patient_registration_date_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'check_patient_registration_date_data':check_patient_registration_date_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Clinical Administration - OPD Consultation Report With Address")
def opd_consultation_report_with_address(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "OPD Consultation Report With Address",
        "date_form": DateForm(),
        "facilities": facility,
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            opd_consultation_report_with_address_value,
            column_name,
        ) = db.get_opd_consultation_report_with_address(
            facility_code, from_date, to_date
        )

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=opd_consultation_report_with_address_value,
            column=column_name,
        )

        if not opd_consultation_report_with_address_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'opd_consultation_report_with_address_value':opd_consultation_report_with_address_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Clinical Administration - Patient Registration Report")
def patient_registration_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Patient Registration Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            patient_registration_report_value,
            column_name,
        ) = db.get_patient_registration_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=patient_registration_report_value,
            column=column_name,
        )

        if not patient_registration_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'patient_registration_report_value':patient_registration_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Contract Effective Date Report")
def contract_effective_date_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Contract Effective Date Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            contract_effective_date_report_value,
            column_name,
        ) = db.get_contract_effective_date_report(facility_code, from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=contract_effective_date_report_value,
            column=column_name,
        )

        if not contract_effective_date_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'contract_effective_date_report_value':contract_effective_date_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Marketing - Admission Reports")
def admission_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Admission Reports",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        admission_report_value, column_name = db.get_admission_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=admission_report_value,
            column=column_name,
        )

        if not admission_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'facilities' : facility,'admission_report_value':admission_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Patient Discharge Report")
def patient_discharge_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Patient Discharge Report",
        "date_form": DateForm(),
        "date_template": "date_template",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        patient_discharge_report_value, column_name = db.get_patient_discharge_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=patient_discharge_report_value,
            column=column_name,
        )

        if not patient_discharge_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'patient_discharge_report_value':patient_discharge_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Corporate Discharge Report")
def corporate_discharge_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Corporate Discharge Report",
        "date_form": DateForm(),
        "facilities": facility,
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            corporate_discharge_report_value,
            column_name,
        ) = db.get_corporate_discharge_report(facility_code, from_date, to_date)

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=corporate_discharge_report_value,
            column=column_name,
        )

        if not corporate_discharge_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'corporate_discharge_report_value':corporate_discharge_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Corporate Discharge Report With Customer Code")
def corporate_discharge_report_with_customer_code(request):

    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Corporate Discharge Report With Customer Code",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(
            request,
            "reports/one_for_all.html",
            context,
        )

    elif request.method == "POST":

        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            corporate_discharge_report_with_customer_code_value,
            column_name,
        ) = db.get_corporate_discharge_report_with_customer_code(from_date, to_date)

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=corporate_discharge_report_with_customer_code_value,
            column=column_name,
        )

        if not corporate_discharge_report_with_customer_code_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'corporate_discharge_report_with_customer_code_value':corporate_discharge_report_with_customer_code_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Credit Letter Report")
def credit_letter_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Credit Letter Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        credit_letter_report_value, column_name = db.get_credit_letter_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=credit_letter_report_value,
            column=column_name,
        )

        if not credit_letter_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'credit_letter_report_value':credit_letter_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Corporate IP Report")
def corporate_ip_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Corporate IP Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        corporate_ip_report_value, column_name = db.get_corporate_ip_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=corporate_ip_report_value,
            column=column_name,
        )

        if not corporate_ip_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'corporate_ip_report_value':corporate_ip_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - OPD Consultation Report")
def opd_consultation_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "OPD Consultation Report",
        "date_form": DateForm(),
        "facilities": facility,
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        opd_consultation_report_value, column_name = db.get_opd_consultation_report(
            facility_code, from_date, to_date
        )

        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=opd_consultation_report_value,
            column=column_name,
        )

        if not opd_consultation_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'opd_consultation_report_value':opd_consultation_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Emergency Casualty Report")
def emergency_casualty_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Emergency Casualty Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        emergency_casualty_report_value, column_name = db.get_emergency_casualty_report(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=emergency_casualty_report_value,
            column=column_name,
        )

        if not emergency_casualty_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'emergency_casualty_report_value':emergency_casualty_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - New Registration Report")
def new_registration_report(request):
    input_tags = {"City"}
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "input_tags": input_tags,
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "New Registration Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":

        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        city_input = request.POST["City"].upper()
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            new_registration_report_value,
            new_registration_report_column,
        ) = db.get_new_registration_report(
            from_date, to_date, city_input, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=new_registration_report_value,
            column=new_registration_report_column,
        )

        if not new_registration_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'new_registration_report_value':new_registration_report_value, "new_registration_report_column":new_registration_report_column,'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - Hospital Tariff Report")
def hospital_tariff_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Hospital Tariff Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/__.html", context)

        db = Ora()
        hospital_tariff_report_value, column_name = db.get_hospital_tariff_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=hospital_tariff_report_value,
            column=column_name,
        )

        if not hospital_tariff_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'hospital_tariff_report_value':hospital_tariff_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Marketing - International Patient Report")
def international_patient_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "date_form": DateForm(),
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "International Patient Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        (
            international_patient_report_value,
            column_name,
        ) = db.get_international_patient_report(from_date, to_date, facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=international_patient_report_value,
            column=column_name,
        )

        if not international_patient_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'facilities' : facility,'international_patient_report_value':international_patient_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - TPA Query")
def tpa_query(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "TPA Query",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        tpa_query_value, column_name = db.get_tpa_query(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=tpa_query_value, column=column_name
        )

        if not tpa_query_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'tpa_query_value':tpa_query_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Marketing - New Admission Report")
def new_admission_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "New Admission Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        new_admission_report_value, column_name = db.get_new_admission_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=new_admission_report_value,
            column=column_name,
        )

        if not new_admission_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'new_admission_report_value':new_admission_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Discharge Billing Report")
def discharge_billing_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Discharge Billing Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        discharge_billing_report_value, column_name = db.get_discharge_billing_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=discharge_billing_report_value,
            column=column_name,
        )

        if not discharge_billing_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'discharge_billing_report_value':discharge_billing_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users(
    "Miscellaneous Reports - Billing - Discharge Billing Report Without Date Range"
)
def discharge_billing_report_without_date_range(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Discharge Billing Report Without Date Range",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            discharge_billing_report_without_date_range_value,
            column_name,
        ) = db.get_discharge_billing_report_without_date_range()
        # excel_file_path = excel_generator(page_name="Discharge Billing Report Without Date Range", data=discharge_billing_report_without_date_range_value, column=column_name,      )

        if not discharge_billing_report_without_date_range_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(
                request,
                "reports/one_for_all.html",
                context,
            )

        else:
            pd_dataframe = pd.DataFrame(
                data=discharge_billing_report_without_date_range_value,
                columns=list(column_name),
            )
            pd_dataframe["DIS_ADV_DATE_TIME"] = pd.to_datetime(
                pd_dataframe["DIS_ADV_DATE_TIME"], format="%d-%b-%Y %H:%M:%S"
            ).dt.strftime("%d-%b-%Y %H:%M:%S")

            return HttpResponse(pd_dataframe.to_html())
            # return FileResponse(
            #     open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            # )
            # return render(request,'reports/one_for_all.html', {'discharge_billing_report_without_date_range_value':discharge_billing_report_without_date_range_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Discharge Billing User")
def discharge_billing_user(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Discharge Billing User",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        discharge_billing_user_value, column_name = db.get_discharge_billing_user()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=discharge_billing_user_value,
            column=column_name,
        )

        if not discharge_billing_user_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'discharge_billing_user_value':discharge_billing_user_value, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Discount Report")
def discount_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Discount Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        discount_report_value, column_name = db.get_discount_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=discount_report_value,
            column=column_name,
        )

        if not discount_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'discount_report_value':discount_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Refund Report")
def refund_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Refund Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)
        refund_report_value, column_name = db.get_refund_report(
            from_date, to_date, facility_code
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=refund_report_value, column=column_name
        )

        if not refund_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'refund_report_value':refund_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Non Medical Equipment Report")
def non_medical_equipment_report(request):
    input_tags = {"Episode ID", "UHID"}
    context = {
        "user_name": request.user.username,
        "input_tags": input_tags,
        "page_name": "Non Medical Equipment Report",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        uhid = request.POST["UHID"].upper()
        episode_id = request.POST["Episode"]
        db = Ora()
        (
            non_medical_equipment_report_data,
            column_name,
        ) = db.get_non_medical_equipment_report(uhid, episode_id)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=non_medical_equipment_report_data,
            column=column_name,
        )

        if not non_medical_equipment_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {"column_name":column_name,'non_medical_equipment_report_data':non_medical_equipment_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Additional Tax On Package Room Rent")
def additional_tax_on_package_room_rent(request):
    input_tags = {"Episode ID", "UHID"}
    context = {
        "input_tags": input_tags,
        "user_name": request.user.username,
        "page_name": "Additional Tax On Package Room Rent",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        uhid = request.POST["UHID"].upper()
        episode_id = request.POST["Episode"]
        db = Ora()
        (
            additional_tax_on_package_room_rent_data,
            column_name,
        ) = db.get_additional_tax_on_package_room_rent(uhid, episode_id)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=additional_tax_on_package_room_rent_data,
            column=column_name,
        )

        if not additional_tax_on_package_room_rent_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'additional_tax_on_package_room_rent_data':additional_tax_on_package_room_rent_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Billing - Due Deposit Report")
def due_deposit_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Due Deposit Report",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        due_deposit_report_value, column_name = db.get_due_deposit_report(facility_code)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=due_deposit_report_value,
            column=column_name,
        )

        if not due_deposit_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'due_deposit_report_value':due_deposit_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


# Lab


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - Covid PCR")
def covid_pcr(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Covid PCR",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        covid_pcr_value, column_name = db.get_covid_pcr(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=covid_pcr_value, column=column_name
        )

        if not covid_pcr_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'covid_pcr_value':covid_pcr_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - Covid 2")
def covid_2(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Covid 2",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        covid_2_value, column_name = db.get_covid_2(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=covid_2_value, column=column_name
        )

        if not covid_2_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'covid_2_value':covid_2_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - Covid Antibodies")
def covid_antibodies(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Covid Antibodies",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        covid_antibodies_value, column_name = db.get_covid_antibodies(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=covid_antibodies_value,
            column=column_name,
        )

        if not covid_antibodies_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'covid_antibodies_value':covid_antibodies_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - Covid Antibodies")
def covid_antigen(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Covid Antigen",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        covid_antigen_value, column_name = db.get_covid_antigen(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"], data=covid_antigen_value, column=column_name
        )

        if not covid_antigen_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'covid_antigen_value':covid_antigen_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - CBNAAT Test Data")
def cbnaat_test_data(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "CBNAAT Test Data",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        cbnaat_test_data_value, column_name = db.get_cbnaat_test_data(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=cbnaat_test_data_value,
            column=column_name,
        )

        if not cbnaat_test_data_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'cbnaat_test_data_value':cbnaat_test_data_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - LAB TAT Report")
def lab_tat_report(request):
    get_fac = request.user.employee.facility

    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")

    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    dropdown_options = [
        {
            "option_value": "Histopathology & Cytology",
            "option_name": "Histopathology & Cytology",
        },
        {"option_value": "Immunology", "option_name": "Immunology"},
        {"option_value": "Toxicology", "option_name": "Toxicology"},
        {"option_value": "Biochemistry", "option_name": "Biochemistry"},
        {"option_value": "Hematology", "option_name": "Hematology"},
        {"option_value": "Microbiology", "option_name": "Microbiology"},
        {"option_value": "Transfusion Medicine", "option_name": "Transfusion Medicine"},
        {"option_value": "Genetics", "option_name": "Genetics"},
        {"option_value": "Clinical Pathology", "option_name": "Clinical Pathology"},
        {
            "option_value": "Infectious Molecular Biology",
            "option_name": "Infectious Molecular Biology",
        },
        {
            "option_value": "Haematology & Immunohaematology",
            "option_name": "Haematology & Immunohaematology",
        },
        {
            "option_value": "Histocompatibility Lab",
            "option_name": "Histocompatibility Lab",
        },
    ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "dropdown_options": dropdown_options,
        "user_name": request.user.username,
        "page_name": "LAB TAT Report",
        "date_form": DateForm(),
        "facilities": facility,
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
            dept_name = request.POST["dropdown_options"]
        except MultiValueDictKeyError:
            context[
                "error"
            ] = "😒 Please select a facility and the department name from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        lab_tat_report_value, column_name = db.get_lab_tat_report(
            facility_code, from_date, to_date, dept_name
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=lab_tat_report_value,
            column=column_name,
        )

        if not lab_tat_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'lab_tat_report_value':lab_tat_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - Histopath Fixation Data")
def histopath_fixation_data(request):
    input_tags = {"Category Year"}
    context = {
        "input_tags": input_tags,
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Histopath Fixation Data",
        "date_form": DateForm(),
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        year_input = request.POST["Category"]

        db = Ora()
        histopath_fixation_data_value, column_name = db.get_histopath_fixation_data(
            year_input, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=histopath_fixation_data_value,
            column=column_name,
        )

        if not histopath_fixation_data_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'histopath_fixation_data_value':histopath_fixation_data_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Lab - Slide Label Data")
def slide_label_data(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Slide Label Data",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        slide_label_data_data, column_name = db.get_slide_label_data()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=slide_label_data_data,
            column=column_name,
        )

        if not slide_label_data_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'slide_label_data_data':slide_label_data_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - EHC - EHC Operation Report")
def ehc_operation_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "EHC Operation Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        ehc_operation_report_value, column_name = db.get_ehc_operation_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ehc_operation_report_value,
            column=column_name,
        )

        if not ehc_operation_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ehc_operation_report_value':ehc_operation_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - EHC - EHC Operation Report 2")
def ehc_operation_report_2(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "EHC Operation Report 2",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        ehc_operation_report_2_value, column_name = db.get_ehc_operation_report_2(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ehc_operation_report_2_value,
            column=column_name,
        )

        if not ehc_operation_report_2_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ehc_operation_report_2_value':ehc_operation_report_2_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Sales - Oncology Drugs Report")
def oncology_drugs_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "facilities": facility,
        "user_name": request.user.username,
        "page_name": "Oncology Drugs Report",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        oncology_drugs_report_value, column_name = db.get_oncology_drugs_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=oncology_drugs_report_value,
            column=column_name,
        )

        if not oncology_drugs_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'oncology_drugs_report_value':oncology_drugs_report_value, 'user_name':request.user.username,'date_form' : DateForm(),'facilities' : facility})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Radiology - Radiology TAT Report")
def radiology_tat_report(request):
    get_fac = request.user.employee.facility
    if get_fac.facility_name == "ALL":
        facility = FacilityDropdown.objects.values().order_by("facility_name")
    else:
        facility = [
            {
                "facility_name": get_fac.facility_name,
                "facility_code": get_fac.facility_code,
            },
        ]
    context = {
        "date_template": "date_template",
        "facility_template": "facility_template",
        "user_name": request.user.username,
        "page_name": "Radiology TAT Report",
        "date_form": DateForm(),
        "facilities": facility,
    }
    if request.method == "GET":

        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])
        try:
            facility_code = request.POST["facility_dropdown"]
        except MultiValueDictKeyError:
            context["error"] = "😒 Please Select a facility from the dropdown list"
            return render(request, "reports/one_for_all.html", context)

        db = Ora()
        radiology_tat_report_value, column_name = db.get_radiology_tat_report(
            facility_code, from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=radiology_tat_report_value,
            column=column_name,
        )

        if not radiology_tat_report_value:
            context["error"] = " Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'radiology_tat_report_value':radiology_tat_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Internal Auditor - Day Care Report")
def day_care_report(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Day Care Report",
        "date_form": DateForm(),
    }
    if request.method == "GET":

        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        day_care_report_value, column_name = db.get_day_care_report(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=day_care_report_value,
            column=column_name,
        )

        if not day_care_report_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'column_name':column_name,'day_care_report_value':day_care_report_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - OT Scheduling List Report")
def ot_scheduling_list_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "OT Scheduling List Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        ot_scheduling_list_report_data, column_name = db.get_ot_scheduling_list_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=ot_scheduling_list_report_data,
            column=column_name,
        )

        if not ot_scheduling_list_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'ot_scheduling_list_report_data':ot_scheduling_list_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Miscellaneous Reports - Non Package Covid Patient Report")
def non_package_covid_patient_report(request):
    context = {
        "user_name": request.user.username,
        "page_name": "Non Package Covid Patient Report",
    }
    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        db = Ora()
        (
            non_package_covid_patient_report_data,
            column_name,
        ) = db.get_non_package_covid_patient_report()
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=non_package_covid_patient_report_data,
            column=column_name,
        )

        if not non_package_covid_patient_report_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'non_package_covid_patient_report_data':non_package_covid_patient_report_data, 'user_name':request.user.username})


@login_required(login_url="login")
@allowed_users("Microbiology - GX Flu A, Flu B RSV")
def gx_flu_a_flu_b_rsv(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "GX Flu A, Flu B RSV",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        gx_flu_a_flu_b_rsv_value, column_name = db.get_gx_flu_a_flu_b_rsv(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=gx_flu_a_flu_b_rsv_value,
            column=column_name,
        )

        if not gx_flu_a_flu_b_rsv_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'gx_flu_a_flu_b_rsv_value':gx_flu_a_flu_b_rsv_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Microbiology - H1N1 Detection By PCR")
def h1n1_detection_by_pcr(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "H1N1 Detection By PCR",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        h1n1_detection_by_pcr_value, column_name = db.get_h1n1_detection_by_pcr(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=h1n1_detection_by_pcr_value,
            column=column_name,
        )

        if not h1n1_detection_by_pcr_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'h1n1_detection_by_pcr_value':h1n1_detection_by_pcr_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Microbiology - Biofire Respiratory")
def biofire_respiratory(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "Biofire Respiratory",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        biofire_respiratory_value, column_name = db.get_biofire_respiratory(
            from_date, to_date
        )
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=biofire_respiratory_value,
            column=column_name,
        )

        if not biofire_respiratory_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'biofire_respiratory_value':biofire_respiratory_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Microbiology - COVID 19 Report With Pincode And Ward")
def covid_19_report_with_pincode_and_ward(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "COVID 19 Report With Pincode And Ward",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            covid_19_report_with_pincode_and_ward_value,
            column_name,
        ) = db.get_covid_19_report_with_pincode_and_ward(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=covid_19_report_with_pincode_and_ward_value,
            column=column_name,
        )

        if not covid_19_report_with_pincode_and_ward_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'covid_19_report_with_pincode_and_ward_value':covid_19_report_with_pincode_and_ward_value, 'user_name':request.user.username,'date_form' : DateForm()})


@login_required(login_url="login")
@allowed_users("Microbiology - CBNAAT COVID Report With Pincode")
def cbnaat_covid_report_with_pincode(request):
    context = {
        "date_template": "date_template",
        "user_name": request.user.username,
        "page_name": "CBNAAT COVID Report With Pincode",
        "date_form": DateForm(),
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":
        # Manually format To Date fro Sql Query
        from_date = date_formater(request.POST["from_date"])
        to_date = date_formater(request.POST["to_date"])

        db = Ora()
        (
            cbnaat_covid_report_with_pincode_value,
            column_name,
        ) = db.get_cbnaat_covid_report_with_pincode(from_date, to_date)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=cbnaat_covid_report_with_pincode_value,
            column=column_name,
        )

        if not cbnaat_covid_report_with_pincode_value:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'cbnaat_covid_report_with_pincode_value':cbnaat_covid_report_with_pincode_value, 'user_name':request.user.username,'date_form' : DateForm()})


# Run Query Directly
@login_required(login_url="login")
def run_query_directly(request):
    textbox = {"Paste SQL Query here"}
    context = {
        "textbox": textbox,
        "user_name": request.user.username,
        "page_name": "Run Query Directly",
    }

    if request.method == "GET":
        return render(request, "reports/one_for_all.html", context)

    elif request.method == "POST":

        sql_query = request.POST["Paste SQL Query here"]
        db = Ora()
        (
            run_query_directly_data,
            column_name,
        ) = db.get_run_query_directly(sql_query)
        excel_file_path = excel_generator(
            page_name=context["page_name"],
            data=run_query_directly_data,
            column=column_name,
        )

        if not run_query_directly_data:
            context["error"] = "Sorry!!! No Data Found"
            return render(request, "reports/one_for_all.html", context)

        else:
            return FileResponse(
                open(excel_file_path, "rb"), content_type="application/vnd.ms-excel"
            )
            # return render(request,'reports/one_for_all.html', {'run_query_directly_data':run_query_directly_data, 'user_name':request.user.username})
