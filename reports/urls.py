from django.urls import path
from . import views

urlpatterns = [

    path('',views.login_page,name="login"),              #login Page
    path('landing_page/',views.landing_page, name="landing_page"),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('base/',views.base, name = "base"),          #base HTml pAge
    path('signupuser/',views.signupuser, name="signupuser"),
    path('stock/',views.stock, name='stock'),
    path('stock_report/',views.stock_report, name="stock_report"),
    path('stock_value/',views.stock_value, name="stock_value"),
    path('bin_location_op/',views.bin_location_op, name="bin_location_op"),
    path('itemwise_storewise_stock/',views.itemwise_storewise_stock, name="itemwise_storewise_stock"),
    path('batchwise_stock_report/',views.batchwise_stock_report, name="batchwise_stock_report"),
    path('pharmacy_op_returns/',views.pharmacy_op_returns, name="pharmacy_op_returns"),
    path('restricted_antimicrobials_consumption_report/',views.restricted_antimicrobials_consumption_report, name="restricted_antimicrobials_consumption_report"),
    path('important_antimicrobials_antibiotics_consumption_report/',views.important_antimicrobials_antibiotics_consumption_report, name="important_antimicrobials_antibiotics_consumption_report"),
    path('pharmacy_indent_report/',views.pharmacy_indent_report, name="pharmacy_indent_report"),
    path('new_admission_indents_report/',views.new_admission_indents_report, name="new_admission_indents_report"),
    path('return_medication_without_return_request_report/',views.return_medication_without_return_request_report, name="return_medication_without_return_request_report"),
    path('deleted_pharmacy_prescriptions_report/',views.deleted_pharmacy_prescriptions_report, name="deleted_pharmacy_prescriptions_report"),
    path('pharmacy_direct_sales_report/',views.pharmacy_direct_sales_report, name="pharmacy_direct_sales_report"),
    path('intransites_unf_sal/',views.intransites_unf_sal, name="intransites_unf_sal"),
    path('intransites_confirm_pending/',views.intransites_confirm_pending, name="intransites_confirm_pending"),
    path('non_billable_consumption/',views.non_billable_consumption, name="non_billable_consumption"),
    path('non_billable_consumption1/',views.non_billable_consumption1, name="non_billable_consumption1"),
    path('pharmacy_charges_and_implant_pending_indent_report/',views.pharmacy_charges_and_implant_pending_indent_report, name="pharmacy_charges_and_implant_pending_indent_report"),
    path('pharmacy_direct_returns_sale_report/',views.pharmacy_direct_returns_sale_report, name="pharmacy_direct_returns_sale_report"),
    path('current_inpatients_report/',views.current_inpatients_report, name="current_inpatients_report"),
    path('consigned_item_detail_report/',views.consigned_item_detail_report, name="consigned_item_detail_report"),
    path('schedule_h1_drug_report/',views.schedule_h1_drug_report, name="schedule_h1_drug_report"),
    path('pharmacy_ward_return_requests_with_status_report/',views.pharmacy_ward_return_requests_with_status_report, name="pharmacy_ward_return_requests_with_status_report"),
    path('pharmacy_indent_deliver_summary_report/',views.pharmacy_indent_deliver_summary_report, name="pharmacy_indent_deliver_summary_report"),
    path('intransites_stk_tfr_acknowledgement_pending/',views.intransites_stk_tfr_acknowledgement_pending, name="intransites_stk_tfr_acknowledgement_pending"),
    path('folley_and_central_line/',views.folley_and_central_line, name="folley_and_central_line"),
    path('angiography_kit/',views.angiography_kit, name="angiography_kit"),
    path('new_admission_dispense_report/',views.new_admission_dispense_report, name="new_admission_dispense_report"),
    path('pharmacy_op_sale_report_userwise/',views.pharmacy_op_sale_report_userwise, name="pharmacy_op_sale_report_userwise"),
    path('pharmacy_consumption_report/',views.pharmacy_consumption_report, name="pharmacy_consumption_report"),
    path('food_drug_interaction_report/',views.food_drug_interaction_report, name="food_drug_interaction_report"),
    path('intransite_stock/',views.intransite_stock, name="intransite_stock"),
    path('grn_data/',views.grn_data, name="grn_data"),
    path('drug_duplication_override_report/',views.drug_duplication_override_report, name="drug_duplication_override_report"),
    path('drug_interaction_override_report/',views.drug_interaction_override_report, name="drug_interaction_override_report"),
    path('sale_consumption_report/',views.sale_consumption_report, name="sale_consumption_report"),
    path('sale_consumption_report1/',views.sale_consumption_report1, name="sale_consumption_report1"),
    path('predischarge_medication/',views.predischarge_medication, name="predischarge_medication"),
    path('predischarge_initiate/',views.predischarge_initiate, name="predischarge_initiate"),
    path('intransites_unf_sal_ret/',views.intransites_unf_sal_ret, name="intransites_unf_sal_ret"),
    path('intransites_unf_stk_tfr/',views.intransites_unf_stk_tfr, name="intransites_unf_stk_tfr"),
    path('intransites_acknowledgement_pending_iss/',views.intransites_acknowledgement_pending_iss, name="intransites_acknowledgement_pending_iss"),
    path('intransites_acknowledgement_pending_iss_rt/',views.intransites_acknowledgement_pending_iss_rt, name="intransites_acknowledgement_pending_iss_rt"),
    


    path('credit_outstanding_bill/',views.credit_outstanding_bill, name="credit_outstanding_bill"),
    path('tpa_letter/',views.tpa_letter, name="tpa_letter"),
    path('online_consultation_report/',views.online_consultation_report, name="online_consultation_report"),
    path('contract_report/',views.contract_report, name="contract_report"),
    path('package_contract_report/',views.package_contract_report, name="package_contract_report"),
    path('credit_card_reconciliation_report/',views.credit_card_reconciliation_report, name="credit_card_reconciliation_report"),
    path('covid_ot_surgery_details/',views.covid_ot_surgery_details, name="covid_ot_surgery_details"),
    path('gst_data_of_pharmacy/',views.gst_data_of_pharmacy, name="gst_data_of_pharmacy"),
    path('gst_data_of_pharmacy_return/',views.gst_data_of_pharmacy_return, name="gst_data_of_pharmacy_return"),
    path('gst_data_of_ip/',views.gst_data_of_ip, name="gst_data_of_ip"),
    path('gst_data_of_op/',views.gst_data_of_op, name="gst_data_of_op"),
    path('revenue_data_of_sl/',views.revenue_data_of_sl, name="revenue_data_of_sl"),
    path('revenue_data_of_sl1/',views.revenue_data_of_sl1, name="revenue_data_of_sl1"),
    path('revenue_data_of_sl2/',views.revenue_data_of_sl2, name="revenue_data_of_sl2"),
    path('revenue_data_of_sl3/',views.revenue_data_of_sl3, name="revenue_data_of_sl3"),





    path('pre_discharge_report/',views.pre_discharge_report, name="pre_discharge_report"),
    path('pre_discharge_report_2/',views.pre_discharge_report_2, name="pre_discharge_report_2"),
    path('discharge_report_2/',views.discharge_report_2, name="discharge_report_2"),
    path('discharge_with_mis_report/',views.discharge_with_mis_report, name="discharge_with_mis_report"),
    path('needle_prick_injury_report/',views.needle_prick_injury_report, name="needle_prick_injury_report"),
    path('practo_report/',views.practo_report, name="practo_report"),
    path('unbilled_report/',views.unbilled_report, name="unbilled_report"),
    path('unbilled_deposit_report/',views.unbilled_deposit_report, name="unbilled_deposit_report"),
    path('contact_report/',views.contact_report, name="contact_report"),
    path('employees_antibodies_reactive_report/',views.employees_antibodies_reactive_report, name="employees_antibodies_reactive_report"),
    path('employees_reactive_and_non_pcr_report/',views.employees_reactive_and_non_pcr_report, name="employees_reactive_and_non_pcr_report"),
    path('employee_covid_test_report/',views.employee_covid_test_report, name="employee_covid_test_report"),
    path('bed_location_report/',views.bed_location_report, name="bed_location_report"),
    path('home_visit_report/',views.home_visit_report, name="home_visit_report"),
    path('cco_billing_count_report/',views.cco_billing_count_report, name="cco_billing_count_report"),
    path('total_number_of_online_consultation_by_doctors/',views.total_number_of_online_consultation_by_doctors, name="total_number_of_online_consultation_by_doctors"),
    path('total_number_of_ip_patients_by_doctors/',views.total_number_of_ip_patients_by_doctors, name="total_number_of_ip_patients_by_doctors"),
    path('total_number_of_op_patients_by_doctors/',views.total_number_of_op_patients_by_doctors, name="total_number_of_op_patients_by_doctors"),
    path('opd_changes_report/',views.opd_changes_report, name="opd_changes_report"),
    path('ehc_conversion_report/',views.ehc_conversion_report, name="ehc_conversion_report"),
    path('ehc_package_range_report/',views.ehc_package_range_report, name="ehc_package_range_report"),
    path('error_report/',views.error_report, name="error_report"),
    path('ot_query_report/',views.ot_query_report, name="ot_query_report"),
    path('outreach_cancer_hospital/',views.outreach_cancer_hospital, name="outreach_cancer_hospital"),
    path('gipsa_report/',views.gipsa_report, name="gipsa_report"),
    path('precision_patient_opd_and_online_consultation_list_report/',views.precision_patient_opd_and_online_consultation_list_report, name="precision_patient_opd_and_online_consultation_list_report"),
    path('appointment_details_by_call_center_report/',views.appointment_details_by_call_center_report, name="appointment_details_by_call_center_report"),
    path('trf_report/',views.trf_report, name="trf_report"),
    path('current_inpatients_clinical_admin/',views.current_inpatients_clinical_admin, name="current_inpatients_clinical_admin"),
    path('check_patient_registration_date/',views.check_patient_registration_date, name="check_patient_registration_date"),
    path('patient_registration_report/',views.patient_registration_report, name="patient_registration_report"),
    path('current_inpatients_employee_and_dependants/',views.current_inpatients_employee_and_dependants, name="current_inpatients_employee_and_dependants"),
     path('treatment_sheet_data/',views.treatment_sheet_data, name="treatment_sheet_data"),

    
    
    
    
    path('covid_pcr/',views.covid_pcr, name="covid_pcr"),
    path('covid_2/',views.covid_2, name="covid_2"),
    path('covid_antibodies/',views.covid_antibodies, name="covid_antibodies"),
    path('covid_antigen/',views.covid_antigen, name="covid_antigen"),
    path('cbnaat_test_data/',views.cbnaat_test_data, name="cbnaat_test_data"),
    path('lab_tat_report/',views.lab_tat_report, name="lab_tat_report"),
    path('histopath_fixation_data/',views.histopath_fixation_data, name="histopath_fixation_data"),
    path('slide_label_data/',views.slide_label_data, name="slide_label_data"),




    path('contract_effective_date_report/',views.contract_effective_date_report, name="contract_effective_date_report"),
    path('admission_report/',views.admission_report, name="admission_report"),
    path('patient_discharge_report/',views.patient_discharge_report, name="patient_discharge_report"),
    path('credit_letter_report/',views.credit_letter_report, name="credit_letter_report"),
    path('corporate_ip_report/',views.corporate_ip_report, name="corporate_ip_report"),
    path('opd_consultation_report/',views.opd_consultation_report, name="opd_consultation_report"),
    path('emergency_casualty_report/',views.emergency_casualty_report, name="emergency_casualty_report"),
    path('new_registration_report/',views.new_registration_report, name="new_registration_report"),
    path('hospital_tariff_report/',views.hospital_tariff_report, name="hospital_tariff_report"),
    path('international_patient_report/',views.international_patient_report, name="international_patient_report"),
    path('tpa_query/',views.tpa_query, name="tpa_query"),
    path('new_admission_report/',views.new_admission_report, name="new_admission_report"),


    
    path('discharge_billing_report/',views.discharge_billing_report, name="discharge_billing_report"),
    path('discharge_billing_report_without_date_range/',views.discharge_billing_report_without_date_range, name="discharge_billing_report_without_date_range"),
    path('discharge_billing_user/',views.discharge_billing_user, name="discharge_billing_user"),
    path('discount_report/',views.discount_report, name="discount_report"),
    path('refund_report/',views.refund_report, name="refund_report"),
    path('non_medical_equipment_report/',views.non_medical_equipment_report, name="non_medical_equipment_report"),
    

    path('ehc_operation_report/',views.ehc_operation_report, name="ehc_operation_report"),
    path('ehc_operation_report_2/',views.ehc_operation_report_2, name="ehc_operation_report_2"),

    path('oncology_drugs_report/',views.oncology_drugs_report, name="oncology_drugs_report"),

    path('radiology_tat_report/',views.radiology_tat_report, name="radiology_tat_report"),

    path('ot_scheduling_list_report/',views.ot_scheduling_list_report, name="ot_scheduling_list_report"),
    path('non_package_covid_patient_report/',views.non_package_covid_patient_report, name="non_package_covid_patient_report"),
    
    
]

