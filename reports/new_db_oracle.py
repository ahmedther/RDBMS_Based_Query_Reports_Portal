import cx_Oracle as newdb_oracle

ip = '172.20.200.16'

host = 'khdb-scan'

port = 1521

service_name = "newdb.kdahit.com"

instance_name = "NEWDB"


#ora_db = newdb_oracle.connect(user="ibaehis", password="ib123", dsn=dsn_tns,
                               #encoding="UTF-8")


class NewDB_Ora:

    def __init__(self):
        self.dsn_tns = newdb_oracle.makedsn("khdb-scan", 1521, service_name="newdb.kdahit.com")
        self.ora_db = newdb_oracle.connect("ibaehis","ib123",self.dsn_tns)
        self.cursor = self.ora_db.cursor()

    def status_update(self):

        if self.ora_db:
            return "You have connected to the Database"

        else:
            return "Unable to connect to the database! Please contact the IT Department" 
      


    def check_users(self,pr_num,passw):
        
        sql_qurey = ('''
        

        SELECT a.APPL_USER_ID, a.APPL_USER_NAME Username,app_password.decrypt(a.APPL_USER_PASSWORD) Password  FROM sm_appl_user a   
        where  a.APPL_USER_ID= :user_id
        and  app_password.decrypt(a.APPL_USER_PASSWORD)=  :user_pass

        
        ''')

        self.cursor.execute(sql_qurey,[pr_num,passw])
        user_pass = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
     

                     
        return user_pass

    def get_stock(self):

        stock_qurey = ('''
        
        
            SELECT DISTINCT A.STORE_CODE, A.ITEM_CODE, B.LONG_DESC, A.BATCH_ID,A.QTY_ON_HAND, A.COMMITTED_QTY FROM ST_ITEM_BATCH A, MM_ITEM B WHERE A.STORE_CODE = 'PS' AND A.ITEM_CODE=B.ITEM_CODE
        
        ''')

        self.cursor.execute(stock_qurey)
        data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return data
    
    
    def get_stock_reports(self):

        stock_reports_query = ('''
        
        
            SELECT a.QTY_ON_HAND, a.COMMITTED_QTY, to_char(NVL (a.QTY_ON_HAND, 0) - NVL (a.COMMITTED_QTY, 0)) AVAIL_Qty,a.STORE_CODE, a.BATCH_ID, a.EXPIRY_DATE_OR_RECEIPT_DATE, a.ITEM_CODE, b.LONG_DESC FROM IBAEHIS.ST_ITEM_BATCH a, MM_ITEM b WHERE  a.ITEM_CODE = b.ITEM_CODE ORDER BY a.STORE_CODE, a.ITEM_CODE,a.EXPIRY_DATE_OR_RECEIPT_DATE
        
        ''')

        self.cursor.execute(stock_reports_query)
        stock_reports_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return stock_reports_data

        

    def get_stock_value(self):

        stock_value_query = ("SELECT a.ITEM_CODE AS ItemCode, a.ITEM_DESC AS Description,a.STORE_CODE AS StoreCode,SUM(a.QTY_ON_HAND) AS QtyOnHand,sum(a.AVAIL_QTY) AS AvailStock,"+
"sum(a.QTY_ON_HAND - a.AVAIL_QTY) AS InTransitStock,d.last_receipt_date AS LastInward, "+
" case when(d.material_group_code = 'KDHMD3') then('Pharma') when(d.material_group_code <> 'KDHMD3') then('surgical') else null end as MaterialCategory"+
" FROM IBAEHIS.ST_BATCH_SEARCH_LANG_VIEW a "+
"left join ST_BATCH_CONTROL b on(a.ITEM_CODE = b.ITEM_CODE and a.BATCH_ID = b.BATCH_ID "+
"and a.EXPIRY_DATE = b.EXPIRY_DATE_OR_RECEIPT_DATE)"+
"left join st_item c on(a.ITEM_CODE = c.ITEM_CODE)"+
"left join mm_item d on(a.item_code = d.item_code)"+
"WHERE(b.SALE_PRICE >= '700' and b.SALE_PRICE <= '799') AND(a.STORE_CODE = 'CP00')"+
"AND(a.ITEM_CODE LIKE '2000%') AND(c.CONSIGNMENT_ITEM_YN = 'N')"+
"GROUP BY a.ITEM_CODE, a.ITEM_DESC,a.STORE_CODE,d.last_receipt_date,d.material_group_code ORDER BY d.material_group_code,a.ITEM_DESC ASC")

        self.cursor.execute(stock_value_query)
        stock_value_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return stock_value_data


    
    def get_bin_location_op_value(self):

        bin_location_op_query = ("SELECT a.ITEM_CODE AS ItemCode, a.ITEM_DESC AS Description,a.STORE_CODE AS StoreCode,SUM(a.QTY_ON_HAND) AS QtyOnHand,sum(a.AVAIL_QTY) AS AvailStock,"+
"sum(a.QTY_ON_HAND - a.AVAIL_QTY) AS InTransitStock,d.last_receipt_date AS LastInward, "+
" case when(d.material_group_code = 'KDHMD3') then('Pharma') when(d.material_group_code <> 'KDHMD3') then('surgical') else null end as MaterialCategory"+
" FROM IBAEHIS.ST_BATCH_SEARCH_LANG_VIEW a "+
"left join ST_BATCH_CONTROL b on(a.ITEM_CODE = b.ITEM_CODE and a.BATCH_ID = b.BATCH_ID "+
"and a.EXPIRY_DATE = b.EXPIRY_DATE_OR_RECEIPT_DATE)"+
"left join st_item c on(a.ITEM_CODE = c.ITEM_CODE)"+
"left join mm_item d on(a.item_code = d.item_code)"+
"WHERE(b.SALE_PRICE >= '700' and b.SALE_PRICE <= '799') AND(a.STORE_CODE = 'CP00')"+
"AND(a.ITEM_CODE LIKE '2000%') AND(c.CONSIGNMENT_ITEM_YN = 'N')"+
"GROUP BY a.ITEM_CODE, a.ITEM_DESC,a.STORE_CODE,d.last_receipt_date,d.material_group_code ORDER BY d.material_group_code,a.ITEM_DESC ASC")

        self.cursor.execute(bin_location_op_query)
        bin_location_op_query_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return bin_location_op_query_data
    

    def get_itemwise_storewise_stock(self):
        itemwise_storewise_stock_query = ("select" +
                    " a.store_code AS STORE," +
                    " a.item_code AS ITEM_CODE,  " +
                    "b.long_desc AS iTEM_NAME," +
                    "a.qty_on_hand AS QOH, "+
                    "ROUND(a.item_value,0) AS VALUE "+
                    " from st_item_store a , " +
                    " mm_item b " +
                    "where (a.item_code = b.item_code) "+
                    "and ((a.qty_on_hand <> 0))" +
                    " order by a.store_code")

        self.cursor.execute(itemwise_storewise_stock_query)
        itemwise_storewise_stock_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return itemwise_storewise_stock_data



    def get_batchwise_stock_report(self):
        batchwise_stock_report_query = ("select " +
                 "a.STORE_CODE  as Store, " +
                 "a.ITEM_CODE as ItemCode,c.LONG_DESC  as ItemName,a.BATCH_ID as Batch,a.EXPIRY_DATE_OR_RECEIPT_DATE as Expiry, " +
                 "a.QTY_ON_HAND as StockQty,b.SERV_COST_AMT as UnitCost,b.PUBLIC_PRICE as MRP from " +
                 "st_item_batch a,bl_st_item_by_tradename b, mm_item c where a.ITEM_CODE = b.ITEM_CODE and a.ITEM_CODE = c.ITEM_CODE " +
                 "and b.ITEM_CODE = c.ITEM_CODE and a.BATCH_ID = b.BATCH_ID and b.EFFECTIVE_TO_DATE is null and b.OPERATING_FACILITY_ID = 'KH' " +
                 "and a.STORE_CODE in (select store_code from mm_store where facility_id = 'KH')" +
                  "order by a.STORE_CODE,a.ITEM_CODE")

        self.cursor.execute(batchwise_stock_report_query)
        batchwise_stock_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return batchwise_stock_report_data

    def get_current_inpatients_report(self):
        get_current_inpatients_report_qurey = ("""
        
        select distinct a.patient_id as Patient_UHID,b.PATIENT_NAME as Patient_Name, a.encounter_id as Encounter_ID,a.bed_num as Bed_No,  
 b.SEX as Sex,round(((sysdate-b.date_of_birth)/365)) as Patient_Age, c.PRACTITIONER_NAME as Attending_Practitioner,d.LONG_DESC Speciality,
a.ADMISSION_DATE_TIME as Admitted_On  
 from ip_open_encounter a,mp_patient b,am_practitioner c,am_speciality d
  where a.facility_id = 'KH' and a.PATIENT_ID=b.PATIENT_ID 
  and a.ATTEND_PRACTITIONER_ID=c.PRACTITIONER_ID 
  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE
  
  """)

        self.cursor.execute(get_current_inpatients_report_qurey)
        get_current_inpatients_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_current_inpatients_report_data


    def get_pharmacy_op_returns(self):
        pharmacy_op_returns_query = ("select distinct * from  GST_DATA_PH_RET  where BILL_DOC_DATE >= ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -30) and OPERATING_FACILITY_ID ='KH' ")

        self.cursor.execute(pharmacy_op_returns_query)
        pharmacy_op_returns_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return pharmacy_op_returns_data
    
    def get_restricted_antimicrobials_consumption_report(self,from_date,to_date):
        getrestricted_antimicrobials_consumption_report_query = ('''
        select distinct a.ADDED_DATE TRN_DATE, b.ITEM_CODE ITEM_CODE, c.DRUG_DESC ITEM_NAME, c.GENERIC_NAME GENERIC_NAME, a.ENCOUNTER_ID ENCOUNTER_ID, 
 a.PATIENT_ID PATIENT_ID, d.PATIENT_NAME PATIENT_NAME,d.SEX ,TRUNC(MONTHS_BETWEEN(sysdate, d.DATE_OF_BIRTH )/12) as Age,  f.ASSIGN_BED_NUM CURR_BED_NO, b.SAL_ITEM_QTY SAL_QTY, b.RET_ITEM_QTY RETURN_QTY, 
 (b.SAL_ITEM_QTY-b.RET_ITEM_QTY) NET_CHARGED, f.VISIT_ADM_DATE_TIME ADMISSION_DATE, f.DISCHARGE_DATE_TIME DISCHARGED_DATE, a.STORE_CODE STORE_CODE, 
 a.DOC_NO DOC_NO,b.DOC_SRL_NO SRL_NO,a.DOC_TYPE_CODE TRN_TYPE,g.PRACTITIONER_NAME,g.PRIMARY_SPECIALITY_CODE  
 from st_sal_hdr a,st_sal_dtl_exp b,PH_DRUG_VW_LANG_VW c,mp_patient d,ip_nursing_unit_bed e,pr_encounter f ,am_practitioner g 
where a.DOC_NO=b.DOC_NO and b.ITEM_CODE=c.DRUG_CODE and d.PATIENT_ID=a.PATIENT_ID and e.OCCUPYING_PATIENT_ID(+)=a.PATIENT_ID 
 and a.DOC_TYPE_CODE=b.DOC_TYPE_CODE and c.PRES_CATG_CODE = '10' and f.ENCOUNTER_ID=a.ENCOUNTER_ID and f.ATTEND_PRACTITIONER_ID=g.PRACTITIONER_ID   
 and a.DOC_TYPE_CODE = 'SAL' and a.FACILITY_ID = 'KH' and a.DOC_DATE between :from_date and :to_date



''')
        self.cursor.execute(getrestricted_antimicrobials_consumption_report_query,[from_date,to_date])
        getrestricted_antimicrobials_consumption_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return getrestricted_antimicrobials_consumption_report_data



    def get_important_antimicrobials_antibiotics_consumption_report(self,drug_code,from_date,to_date,):
        get_important_antimicrobials_antibiotics_consumption_report_query = ('''
        
        select distinct a.ADDED_DATE TRN_DATE, b.ITEM_CODE ITEM_CODE, c.DRUG_DESC ITEM_NAME, c.GENERIC_NAME GENERIC_NAME, a.ENCOUNTER_ID ENCOUNTER_ID,
        a.PATIENT_ID PATIENT_ID,d.PATIENT_NAME PATIENT_NAME,d.SEX ,TRUNC(MONTHS_BETWEEN(sysdate, d.DATE_OF_BIRTH )/12) as Age, f.ASSIGN_BED_NUM CURR_BED_NO ,f.ASSIGN_CARE_LOCN_CODE ORDERING_LOCN,
        h.PRACTITIONER_NAME TREATING_DOC, i.LONG_DESC SPECIALITY, f.REFERRAL_ID REFERRALID, b.SAL_ITEM_QTY SAL_QTY,
        b.RET_ITEM_QTY RETURN_QTY,(b.SAL_ITEM_QTY-b.RET_ITEM_QTY) NET_CHARGED,f.VISIT_ADM_DATE_TIME ADMISSION_DATE,f.DISCHARGE_DATE_TIME DISCHARGED_DATE,
        a.STORE_CODE STORE_CODE,a.DOC_NO DOC_NO,b.DOC_SRL_NO SRL_NO,a.DOC_TYPE_CODE TRN_TYPE
        from st_sal_hdr a,st_sal_dtl_exp b,PH_DRUG_VW_LANG_VW c,mp_patient d,ip_nursing_unit_bed e,pr_encounter f ,PH_DRUG_CATG g, am_practitioner h, AM_SPECIALITY i
        where a.DOC_NO=b.DOC_NO and b.ITEM_CODE=c.DRUG_CODE and d.PATIENT_ID=a.PATIENT_ID and e.OCCUPYING_PATIENT_ID(+)=a.PATIENT_ID
        and a.DOC_TYPE_CODE=b.DOC_TYPE_CODE and f.ATTEND_PRACTITIONER_ID = h.PRACTITIONER_ID and f.SPECIALTY_CODE = i.SPECIALITY_CODE and g.DRUG_CATG_CODE = c.PRES_CATG_CODE and c.PRES_CATG_CODE
        =:drug_code and f.ENCOUNTER_ID=a.ENCOUNTER_ID and a.DOC_TYPE_CODE = 'SAL' and a.FACILITY_ID = 'KH' and a.DOC_DATE between :from_date and :to_date



''')
        self.cursor.execute(get_important_antimicrobials_antibiotics_consumption_report_query,[drug_code,from_date,to_date,])
        get_important_antimicrobials_antibiotics_consumption_report_query_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_important_antimicrobials_antibiotics_consumption_report_query_data

    def get_pharmacy_indent_report(self):

        get_pharmacy_indent_report_qurey = (" select a.PATIENT_ID Pat_ID,a.ENCOUNTER_ID Enc_ID,a.PATIENT_CLASS Pat_Class,a.PAT_CURR_LOCN_CODE Current_Locn,a.ASSIGN_ROOM_NUM Room_No, " +
" a.VISIT_ADM_DATE_TIME Visit_Date_Time,c.ORD_DATE_TIME Order_Date_Time,c.ORDER_CATALOG_CODE Item_Code,c.CATALOG_DESC Item_Desc,c.ORDER_QTY Order_Qty, " +
" d.DISP_QTY Disp_Qty,e.LONG_DESC Order_Status,d.modified_date Dispensed_Date " +
" from pr_encounter a, or_order b, or_order_line c,ph_disp_dtl d,OR_ORDER_STATUS_CODE e " +
" where a.ENCOUNTER_ID = b.ENCOUNTER_ID and b.ORDER_ID=c.ORDER_ID  " +
" and c.ORDER_ID=d.ORDER_ID and c.ORDER_LINE_STATUS=e.ORDER_STATUS_CODE  " +
" and a.PAT_CURR_LOCN_CODE not in ('FL9C','FL9W')and a.facility_id = 'KH'  and a.patient_class = 'IP' and b.order_category = 'PH' " +
" and b.ORD_DATE_TIME between a.VISIT_ADM_DATE_TIME and (a.VISIT_ADM_DATE_TIME+4/24) and trunc(a.visit_adm_date_time) >= trunc(sysdate) " +
" order by d.modified_date desc ")

        self.cursor.execute(get_pharmacy_indent_report_qurey)
        get_pharmacy_indent_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_pharmacy_indent_report_data


    def get_new_admission_indents_report(self):
        get_pharmacy_indent_report_qurey = (" select a.PATIENT_ID Pat_ID, a.PAT_CURR_LOCN_CODE Current_Location,a.ASSIGN_ROOM_NUM Room_No,c.ORDER_CATALOG_CODE Item_Code, " +
" c.CATALOG_DESC Item_Desc,c.ORDER_QTY Order_Qty,c.ORD_DATE_TIME Order_Date_Time " +
" from pr_encounter a, or_order b, or_order_line c,ph_disp_dtl d,OR_ORDER_STATUS_CODE e " +
" where a.ENCOUNTER_ID = b.ENCOUNTER_ID and b.ORDER_ID=c.ORDER_ID and c.ORDER_ID=d.ORDER_ID and c.ORDER_LINE_STATUS=e.ORDER_STATUS_CODE " +
" and a.PAT_CURR_LOCN_CODE not in ('FL9C','FL9W') and a.facility_id =  'KH' and a.patient_class = 'IP' and b.order_category = 'PH'  " +
" and b.ORD_DATE_TIME between a.VISIT_ADM_DATE_TIME and (a.VISIT_ADM_DATE_TIME+4/24) and " +
" trunc(a.visit_adm_date_time) >= sysdate - 2 order by c.ORD_DATE_TIME desc ")

        self.cursor.execute(get_pharmacy_indent_report_qurey)
        get_pharmacy_indent_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_pharmacy_indent_report_data
  


    def get_return_medication_without_return_request_report_value(self,from_date,to_date):
        get_return_medication_without_return_request_report_value_qurey = (''' 
        
        select a.RETURNED_DATE as Returned_DateTime,c.EXP_DISCHARGE_DATE_TIME as Expected_Discharge,c.DISCHARGE_DATE_TIME as Discharge_DateTime,
        b.PATIENT_ID as Patient_ID,f.PATIENT_NAME as Patient_Name,a.DISP_NO Disp_No,a.ITEM_CODE as Item_Code,d.LONG_DESC as Item_Description,g.DRUG_ITEM_YN as Drug,
        a.BATCH_ID as Batch,a.EXPIRY_DATE as Expiry,a.DISP_QTY as DispQty,a.RTN_QTY as RtnQty,e.APPL_USER_NAME as Returned_by,a.MODIFIED_AT_WS_NO as PC_Name
        from ph_retn_medn a,ph_disp_hdr b,pr_encounter c,mm_item d,sm_appl_user e, mp_patient f,st_item g
        where a.DISP_NO=b.DISP_NO and b.ENCOUNTER_ID=c.ENCOUNTER_ID(+) and a.ITEM_CODE=d.ITEM_CODE and b.PATIENT_ID=f.PATIENT_ID and d.ITEM_CODE=g.ITEM_CODE
        and a.DISP_NO not in (select disp_no from ph_ward_return_hdr) and a.MODIFIED_BY_ID=e.APPL_USER_ID and trunc(RETURNED_DATE) between
        :from_date and :to_date
        and b.PATIENT_ID like 'KH100%' order by 1  

''')

        self.cursor.execute(get_return_medication_without_return_request_report_value_qurey,[from_date,to_date])
        get_return_medication_without_return_request_report_value_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_return_medication_without_return_request_report_value_data





    def get_deleted_pharmacy_prescriptions_report(self,from_date,to_date):
        get_deleted_pharmacy_prescriptions_report_qurey = (''' 
        
        select a.order_id as PrescriptionNo, a.patient_id as UHIDNo, c.patient_name as PatientName,
        a.source_code as PatientLocation, a.ORD_DATE_TIME as PrescriptionDate, a.added_by_id as OrderedBy,
        b.order_catalog_code as DrugCodeNo, b.catalog_desc as DrugDescription,e.DRUG_ITEM_YN as DrugYesNo, b.order_qty as PrescribedQty,
        a.modified_at_ws_no as modifiedatstation,d.appl_user_name as FilledByName
        from or_order a , or_order_line b, mp_patient c , sm_appl_user d, st_item e
        where a.order_id in (select order_id from or_order_line_ph where complete_order_reason is not null)
        and a.ORDERING_FACILITY_ID = 'KH' and a.order_id = b.order_id and a.patient_id = c.patient_id and e.ITEM_CODE=b.ORDER_CATALOG_CODE and b.order_catalog_code like '20%'
        and b.modified_by_id = d.appl_user_id and a.ORD_DATE_TIME between :from_date and :to_date order by a.order_id desc

''')

        self.cursor.execute(get_deleted_pharmacy_prescriptions_report_qurey,[from_date,to_date])
        get_deleted_pharmacy_prescriptions_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_deleted_pharmacy_prescriptions_report_data





    def get_pharmacy_direct_sales_report(self,from_date,to_date):
        get_pharmacy_direct_sales_report_qurey = (''' 
        
        select distinct a.ADDED_DATE DOCDATETIME,a.DOC_NO DOCNUM,a.PATIENT_ID PATIENTID,e.PATIENT_NAME PATIENTNAME,b.SAL_ITEM_QTY  ITEMCODE,c.LONG_DESC ITEMNAME, b.BATCH_ID BATCH,b.EXPIRY_DATE_OR_RECEIPT_DATE EXPIRYDATE,
        b.SAL_ITEM_QTY SALEQTY, d.APPL_USER_NAME INITIATEDBY from st_sal_hdr a,st_sal_dtl_exp b,mm_item c,sm_appl_user d,mp_patient e where a.DOC_NO=b.DOC_NO and b.ITEM_CODE=c.ITEM_CODE
        and a.PATIENT_ID=e.PATIENT_ID and a.ADDED_BY_ID=d.APPL_USER_ID and a.STORE_CODE = 'CP00' and a.MODULE_ID = 'ST' and a.FACILITY_ID = 'KH' and a.DOC_DATE between :from_date and :to_date order by a.ADDED_DATE desc

''')

        self.cursor.execute(get_pharmacy_direct_sales_report_qurey,[from_date,to_date])
        get_pharmacy_direct_sales_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_pharmacy_direct_sales_report_data



    def get_pharmacy_charges_and_implant_pending_indent_report(self,from_date,to_date):
        get_pharmacy_charges_and_implant_pending_indent_report_qurey = (''' 
        
       select distinct b.PATIENT_ID PATIENTID,d.PATIENT_NAME PATIENTNAME,a.ORD_DATE_TIME ORDDATETIME,c.APPL_USER_NAME ORDEREDBY,a.ORDER_CATALOG_CODE ITEMCODE,a.CATALOG_DESC ITEMNAME,f.LONG_DESC STATUS,
       a.CAN_DATE_TIME CANCELLEDON,e.PRACTITIONER_NAME CANCELLEDBY,a.CAN_LINE_REASON CANCELREASON from or_order_line a,or_order b,sm_appl_user c,mp_patient d,am_practitioner e,OR_ORDER_STATUS_CODE f
       where a.order_id=b.ORDER_ID and e.PRACTITIONER_ID(+)=a.CAN_PRACT_ID and a.ADDED_BY_ID=c.APPL_USER_ID and d.PATIENT_ID=b.PATIENT_ID and a.ORDER_LINE_STATUS=f.ORDER_STATUS_CODE and a.order_catalog_code in
       (select distinct item_code from mm_item where eff_status = 'E' and long_desc like '%PHARMACY%CHARGES%' or long_desc like '%IMPLANT%PENDING%') and d.ADDED_FACILITY_ID = 'KH'
       and a.ord_date_time between :from_date and :to_date order by a.ord_date_time desc

''')

        self.cursor.execute(get_pharmacy_charges_and_implant_pending_indent_report_qurey,[from_date,to_date])
        get_pharmacy_charges_and_implant_pending_indent_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_pharmacy_charges_and_implant_pending_indent_report_data





    def get_pharmacy_direct_returns_sale_report(self,from_date,to_date):
        get_pharmacy_direct_returns_sale_report_qurey = (''' 
        
       select distinct a.ADDED_DATE DOCDATETIME,a.DOC_NO DOCNUM,a.PATIENT_ID PATIENTID, e.PATIENT_NAME PATIENTNAME,b.ITEM_CODE ITEMCODE,c.LONG_DESC ITEMNAME, b.BATCH_ID BATCH,b.EXPIRY_DATE_OR_RECEIPT_DATE EXPIRYDATE,
       b.ITEM_QTY SALEQTY, d.APPL_USER_NAME INITIATEDBY from st_sal_ret_hdr a,st_sal_ret_dtl_exp b, mm_item c,sm_appl_user d, mp_patient e where a.DOC_NO = b.DOC_NO and b.ITEM_CODE = c.ITEM_CODE and a.PATIENT_ID = e.PATIENT_ID and
       a.ADDED_BY_ID = d.APPL_USER_ID and a.STORE_CODE = 'CP00' and e.ADDED_FACILITY_ID = 'KH' and trunc(a.ADDED_DATE) between :from_date and :to_date

''')

        self.cursor.execute(get_pharmacy_direct_returns_sale_report_qurey,[from_date,to_date])
        get_pharmacy_direct_returns_sale_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_pharmacy_direct_returns_sale_report_data



    def get_consigned_item_detail_report(self,from_date,to_date):
        consigned_item_detail_report_qurey = (''' 
        SELECT ST_SAL_HDR.PATIENT_ID,ST_SAL_HDR.STORE_CODE,ST_SAL_DTL.ADDED_DATE, ST_SAL_DTL.DOC_NO,ST_SAL_DTL.ITEM_CODE,MM_ITEM.LONG_DESC ,ST_SAL_DTL.ITEM_QTY 
 FROM IBAEHIS.ST_SAL_DTL ST_SAL_DTL, IBAEHIS.ST_SAL_HDR ST_SAL_HDR,IBAEHIS.MM_ITEM MM_ITEM,st_item c 
 WHERE (ST_SAL_DTL.ITEM_CODE = MM_ITEM.ITEM_CODE AND ST_SAL_DTL.ITEM_CODE = C.item_code )  AND (ST_SAL_DTL.DOC_NO = ST_SAL_HDR.DOC_NO ) 
 AND ST_SAL_DTL.ADDED_DATE between to_date(:from_date  ,'dd/mm/yyyy hh24:mi:ss') and to_date(:to_date  ,'dd/mm/yyyy hh24:mi:ss')+1
 AND (ST_SAL_DTL.DOC_TYPE_CODE = 'SAL') AND (ST_SAL_HDR.STORE_CODE = 'COT' OR ST_SAL_HDR.STORE_CODE ='OTS' OR ST_SAL_HDR.STORE_CODE ='OTS5') 
 AND (c.consignment_item_yn = 'Y') AND ((ST_SAL_DTL.ITEM_CODE LIKE 'C%') or (ST_SAL_DTL.ITEM_CODE LIKE '2%'))


''')    
    
        self.cursor.execute(consigned_item_detail_report_qurey,[from_date,to_date])
        get_consigned_item_detail_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_consigned_item_detail_report_data




    def get_schedule_h1_drug_report(self,facility_code,from_date,to_date):
        schedule_h1_drug_report_query = (''' 
        
        select distinct c.ITEM_CODE Item_Code, e.PATIENT_CLASS , a.FACILITY_ID FACILITY,a.STORE_CODE Store,a.DOC_DATE Doc_Date, f.APC_NO,nvl(f.PRACTITIONER_NAME,a.PRACTITIONER_NAME) as PRACTITIONER_NAME,a.PATIENT_ID UHID,d.PATIENT_NAME PT_NAME,
        g.ADDR1_LINE1||','||g.ADDR1_LINE2||','||g.ADDR1_LINE3||','||g.ADDR1_LINE4||','||g.RES_TOWN1_CODE||','||g.POSTAL1_CODE ADDRESS,h.LONG_DESC ITEM_NAME,c.BATCH_ID Batch,
        c.EXPIRY_DATE_OR_RECEIPT_DATE Expiry,c.SAL_ITEM_QTY Qty,a.DOC_NO Doc_Num
        from st_sal_hdr a,st_sal_dtl b,st_sal_dtl_exp c,mp_patient d,pr_encounter e,am_practitioner f,MP_PAT_ADDRESSES g, mm_item h
        where a.DOC_NO=b.DOC_NO and a.PATIENT_ID=d.PATIENT_ID and a.PATIENT_ID=g.PATIENT_ID and b.ITEM_CODE=h.ITEM_CODE and a.ENCOUNTER_ID=e.ENCOUNTER_ID(+)
        and e.ATTEND_PRACTITIONER_ID=f.PRACTITIONER_ID(+) and b.DOC_NO=c.DOC_NO and b.ITEM_CODE=c.ITEM_CODE and a.FACILITY_ID = :facility_code
        and a.DOC_DATE between to_date(:from_date,'dd/mm/yyyy hh24:mi:ss') and to_date(:to_date,'dd/mm/yyyy hh24:mi:ss')+1
        and b.ITEM_CODE in ('2000046989','2000054811','2000014232','2000056109','2000012724','2000014122','2000023015','2000054225','2000021515','2000016920','2000019133','2000012723','2000044178',
        '2000013635','2000051089','2000013201','2000012206','2000013318','2000012111','2000013545','2000043798','2000014216','2000014224','2000013246','2000013935','2000037680',
        '2000037679','2000051214','2000023462','2000045386','2000012965','2000013833','2000012979','2000057488','2000011300','2000020745','2000049311','2000020916','2000014123',
        '2000055843','2000039423','2000014215','2000046422','2000052521','2000013937','2000045974','2000013926','2000016697','2000039456','2000017535','2000012265','2000012264',
        '2000035769','2000012205','2000012186','2000012110','2000012147','2000012604','2000012600','2000018058','2000022962','2000022963','2000011503','2000058129','2000011119',
        '2000024355','2000012800','2000018394','2000012801','2000013215','2000012127','2000025022','2000012476','2000013646','2000013097','2000012316','2000012109','2000011109',
        '2000049756','2000055410','2000011299','2000019449','2000013908','2000012207','2000016696','2000012108','2000013965','2000027330','2000050441','2000014121','2000050894',
        '2000058365','2000043104','2000023779','2000049599','2000012107','2000049600','2000013907','2000013973','2000043017','2000045878','2000013945','2000051374','2000013936',
        '2000042514','2000044353','2000060542','2000060547','2000060565','2000060571','2000060572','2000060609','2000060666','2000060667','2000060669','2000061501','2000026461',
        '2000026461','2000026461','2000061789','2000061790','2000011495','2000011495','2000061394','2000025812','2000014067','2000060693','2000014124','2000014124','2000056321',
        '2000056321','2000056321','2000017977','2000017977','2000017970') 

''')
        self.cursor.execute(schedule_h1_drug_report_query,[facility_code,from_date,to_date])
        schedule_h1_drug_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return schedule_h1_drug_report_data
    



    def get_pharmacy_ward_return_requests_with_status_report(self,facility_code,from_date,to_date):
        pharmacy_ward_return_requests_with_status_report_query = (''' 
        
        select a.PATIENT_ID ,d.PATIENT_NAME ,a.ENCOUNTER_ID ,a.DISP_DATE_TIME Dispensed_Dt_Tym,a.DISP_LOCN_CODE Disp_From,a.FROM_LOCN_CODE Returned_from,
        a.RET_TO_DISP_LOCN_CODE Returned_to,a.DISP_NO ,b.ITEM_CODE ,c.LONG_DESC Item_Name,b.STORE_ACKNOWLEDGE_STATUS Status,a.ADDED_DATE Return_On,b.RETURNED_QTY Returned,b.BAL_QTY Balance,
        b.REJ_QTY Rejected from ph_ward_return_hdr a,ph_ward_return_dtl b,mm_item c,mp_patient d
        where a.DISP_NO=b.DISP_NO and a.RET_DOC_NO=b.RET_DOC_NO and a.ORDER_ID=b.ORDER_ID and a.PATIENT_ID=d.PATIENT_ID and b.ITEM_CODE=c.ITEM_CODE
        and a.FACILITY_ID = :facility_code and trunc(a.ADDED_DATE) between to_date(:from_date,'dd/mm/yyyy hh24:mi:ss') and to_date(:to_date,'dd/mm/yyyy hh24:mi:ss')+1

''')
        self.cursor.execute(pharmacy_ward_return_requests_with_status_report_query,[facility_code,from_date,to_date])
        pharmacy_ward_return_requests_with_status_report = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return pharmacy_ward_return_requests_with_status_report


    def get_pharmacy_indent_deliver_summary_report(self):

        stock_qurey = ("select DISTINCT PATIENT_ID AS PatID,count(disp_no) AS IndentsCount,ORD_DATE_TIME  AS OrderDtTym ," +
                " DISPENSED_DATE_TIME AS DispensedDtTym,LOCN_CODE AS IndentLocation,BED_NO  AS BedNo " +
            " from ph_disp_hdr where DISPENSED_DATE_TIME >= '12-Aug-2020' AND PATIENT_ID LIKE 'KH%'" +

" group by PATIENT_ID,DISPENSED_DATE_TIME,LOCN_CODE,BED_NO, ORD_DATE_TIME " +
 "ORDER BY DISPENSED_DATE_TIME DESC ")

        self.cursor.execute(stock_qurey)
        data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return data


    
    def get_new_admission_dispense_report(self):

        get_new_admission_dispense_qurey = ("select c.PATIENT_ID as PatientID,c.LOCN_CODE as PtLocation,c.ORD_DATE_TIME as OrderDateTime , "+
        " a.ASSIGN_BED_NUM as BedNo,c.DISPENSED_DATE_TIME as DispensedDateTime,count(d.DISP_QTY) as Dispensedcount "+
            "from pr_encounter a, or_order b, ph_disp_hdr c,ph_disp_dtl d "+
            "where c.DISP_NO = d.DISP_NO and b.ORDER_ID = c.ORDER_ID and a.PATIENT_ID = b.PATIENT_ID and " +
            "a.ENCOUNTER_ID = b.ENCOUNTER_ID and c.LOCN_CODE not in ('FL9C', 'FL9W') and "+
            "a.facility_id = 'KH' and a.patient_class = 'IP' and b.order_category = 'PH' and "+
            "b.ORD_DATE_TIME between a.VISIT_ADM_DATE_TIME and(a.VISIT_ADM_DATE_TIME+4 / 24) and "+
            "trunc(a.visit_adm_date_time) >= sysdate - 2 "+
            "group by c.PATIENT_ID,c.LOCN_CODE,c.ORD_DATE_TIME,c.DISPENSED_DATE_TIME,a.ASSIGN_BED_NUM "+
            "order by c.DISPENSED_DATE_TIME desc")

        self.cursor.execute(get_new_admission_dispense_qurey)
        get_new_admission_dispense_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_new_admission_dispense_data

    

    def get_pharmacy_op_sale_report_userwise(self,from_date,to_date):
        pharmacy_op_sale_report_userwise_qurey = (''' 
        
       select a.episode_id ,a.doc_type_code,a.added_by_id,a.bill_amt, a.doc_num, a.cash_counter_code,a.doc_date
       from BL_BILL_HDR a
       where a.doc_type_code = 'OPBL'
       and a.cash_counter_code in ('PH1','PH2','PH3','PH4','PH5','PH6','PH7','PH8','PH9')
       and trunc(a.ADDED_DATE) between :from_date and :to_date


''')

        self.cursor.execute(pharmacy_op_sale_report_userwise_qurey,[from_date,to_date])
        pharmacy_op_sale_report_userwise_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return pharmacy_op_sale_report_userwise_data


    def get_pharmacy_consumption_report(self,from_date,to_date):
        get_pharmacy_consumption_re_qurey = (''' 
        
       SELECT ST_SAL_DTL.ADDED_DATE, ST_SAL_DTL.ITEM_QTY, ST_SAL_DTL.ADDED_BY_ID, ST_SAL_DTL.ITEM_CODE ,  
                 ST_SAL_DTL.DOC_NO,ST_SAL_DTL.GROSS_CHARGE_AMT,ST_SAL_DTL.ITEM_COST_VALUE,ST_SAL_DTL.ITEM_QTY,ST_SAL_DTL.ITEM_SAL_VALUE ,  
                 ST_SAL_DTL.ITEM_UNIT_COST,ST_SAL_DTL.ITEM_UNIT_PRICE,ST_SAL_DTL.PAT_GROSS_CHARGE_AMT,ST_SAL_DTL.PAT_NET_AMT,ST_SAL_HDR.STORE_CODE,ST_SAL_HDR.ENCOUNTER_ID,ST_SAL_HDR.PATIENT_ID,MM_ITEM.LONG_DESC  
                 FROM IBAEHIS.ST_SAL_DTL ST_SAL_DTL, IBAEHIS.ST_SAL_HDR ST_SAL_HDR, IBAEHIS.MM_ITEM MM_ITEM  
                  WHERE(ST_SAL_DTL.ITEM_CODE = MM_ITEM.ITEM_CODE)  AND(ST_SAL_DTL.DOC_NO = ST_SAL_HDR.DOC_NO) 
   AND(ST_SAL_DTL.DOC_TYPE_CODE = 'SAL') AND(ST_SAL_HDR.STORE_CODE = 'OP00')  
   AND(ST_SAL_DTL.ITEM_CODE LIKE '2%') 
     and ST_SAL_DTL.ADDED_DATE between :from_date and :to_date


''')

        self.cursor.execute(get_pharmacy_consumption_re_qurey,[from_date,to_date])
        get_pharmacy_consumption_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_pharmacy_consumption_report_data



    def get_food_drug_interaction_report(self,facility_code,from_date,to_date):
        food_drug_interaction_report_qurey = (''' 
        
       select l.ORD_DATE_TIME "Date",e.PATIENT_ID "UHID",e.EPISODE_ID,m.PATIENT_NAME,round(((sysdate-(m.DATE_OF_BIRTH))/365),0) "Age",m.sex,e.ASSIGN_BED_NUM,e.ASSIGN_CARE_LOCN_CODE,
d.DRUG_DESC,n.GENERIC_NAME,d.DRUG_INDICATION "Food-Drug Interation",o.SOURCE_CODE "Ordering location",o.ORD_PRACT_ID,o.ADDED_BY_ID,l.ORDER_QTY,e.VISIT_ADM_DATE_TIME,
e.DISCHARGE_DATE_TIME,e.ADMIT_PRACTITIONER_ID,a.PRACTITIONER_NAME,a.PRIMARY_SPECIALITY_CODE,r.ADDED_BY_ID returned_by,r.ADDED_DATE returned_date,r.RETURNED_QTY,h.RET_TO_DISP_LOCN_CODE
from mp_patient m, or_order o, or_order_line l,or_order_line_ph p,ph_drug d,pr_encounter e,ph_generic_name n,
am_practitioner a,ph_ward_return_dtl r, ph_ward_return_hdr h where 
e.PATIENT_ID = m.PATIENT_ID and o.EPISODE_ID = e.EPISODE_ID and 
o.PATIENT_ID = e.PATIENT_ID and o.ORDER_ID = l.ORDER_ID and o.ORDER_ID = p.ORDER_ID 
and p.GENERIC_ID = n.GENERIC_ID and   l.ORDER_CATALOG_CODE = d.DRUG_CODE and
o.ORDER_ID = h.ORDER_ID(+) and 
e.ADMIT_PRACTITIONER_ID = a.PRACTITIONER_ID and 
o.ORDER_ID = r.ORDER_ID(+) and l.ORD_DATE_TIME between :from_date and :to_date and d.DRUG_INDICATION is not null
and e.FACILITY_ID = :facility_code
      
''')

        self.cursor.execute(food_drug_interaction_report_qurey,[from_date,to_date,facility_code])
        food_drug_interaction_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return food_drug_interaction_report_data

    
    def get_intransite_stock(self):

        get_intransite_stock_qurey = ('''
        
        
            select distinct
            a.STORE_CODE,
            a.ITEM_CODE,
            b.LONG_DESC,
            a.BATCH_ID,
            a.BIN_LOCATION_CODE,
            c.LONG_DESC,
            c.SHORT_DESC,
            a.QTY_ON_HAND,
            a.COMMITTED_QTY
            from st_item_batch a,mm_item b,mm_bin_location c
            where
            a.ITEM_CODE=b.ITEM_CODE and
            a.BIN_LOCATION_CODE=c.BIN_LOCATION_CODE and c.STORE_CODE = 'OP00' and
            a.STORE_CODE = 'OP00' order by a.ITEM_CODE
        ''')

        self.cursor.execute(get_intransite_stock_qurey)
        get_intransite_stock_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_intransite_stock_data
    

    def get_grn_data(self,from_date,to_date):
        get_grn_data_query = ('''
        select distinct a.FACILITY_ID,b.DOC_DATE "GRN Date",b.DOC_NO "HIS Doc No",b.STORE_CODE "Store",b.EXT_DOC_NO "SAP GRN No",b.SUPP_CODE "Vendor Code",d.LONG_NAME "Vendor Name",
a.ITEM_CODE "Item Code",e.LONG_DESC "Item Description",a.ITEM_QTY_NORMAL "GRN Qty",a.RTV_ITEM_QTY_NORMAL "RTV Qty",(a.ITEM_QTY_NORMAL-a.RTV_ITEM_QTY_NORMAL) "Net GRN Qty",
c.BATCH_ID "Batch No",c.EXPIRY_DATE_OR_RECEIPT_DATE "Expiry Date",a.GRN_UNIT_COST_IN_PUR_UOM "Unit Rate",a.ITEM_COST_VALUE "GRN Value"
from st_grn_dtl a,st_grn_hdr b,st_grn_dtl_exp c,ap_supplier d,mm_item e
where a.DOC_NO=b.DOC_NO and a.DOC_TYPE_CODE = b.DOC_TYPE_CODE and a.ITEM_CODE = c.ITEM_CODE and 
a.ITEM_CODE=c.ITEM_CODE and a.DOC_TYPE_CODE = c.DOC_TYPE_CODE and 
a.DOC_NO=c.DOC_NO and a.ITEM_CODE=e.ITEM_CODE and 
d.SUPP_CODE=b.SUPP_CODE and
a.ITEM_CODE like '2000%' and
b.DOC_DATE between :from_date and :to_date
and a.FACILITY_ID in ('KH','AK','RH','GO')
and b.STORE_CODE in ('CP00'  , 'AK00', 'RH00' , 'GO00')
and b.EXT_DOC_NO is not null
order by b.DOC_DATE 



''')
        self.cursor.execute(get_grn_data_query,[from_date,to_date])
        get_grn_data_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_grn_data_data


    def get_drug_duplication_override_report(self,from_date,to_date):
        get_drug_duplication_override_report_query = ('''
        
        select c.patient_id  as PatID,d.patient_name as PatName,b.DUPLICATE_DRUG_OVERRIDE_REASON as DuplicateReason,a.order_catalog_code as IC,
        a.catalog_desc as ItemName,f.generic_name as Generic,a.ord_date_time as OrdDtTym,a.order_qty as Qty
        from or_order_line a,or_order_line_ph b, or_order c, mp_patient d, ph_drug e, ph_generic_name f
        where a.order_id = b.order_id and c.order_id = b.order_id and c.patient_id = d.patient_id
        and b.DUPLICATE_DRUG_OVERRIDE_REASON is not null
        and a.order_catalog_code = e.item_code and e.generic_id = f.generic_id
        and b.modified_date between  :from_date and to_date(:to_date)+1
        and a.added_by_id like 'KH%' order by c.patient_id,f.generic_name 

''')
        self.cursor.execute(get_drug_duplication_override_report_query,[from_date,to_date])
        get_drug_duplication_override_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_drug_duplication_override_report_data

    
    def get_drug_interaction_override_report(self,from_date,to_date):
        get_drug_interaction_override_report_query = ('''
        
        select c.patient_id as PatID,d.patient_name  as PatName,b.INTERACTION_OVERRIDE_REASON  as InteractionOverrideReason,
        a.order_catalog_code as IC,a.catalog_desc  AS ItemName,f.generic_name  as Generic,a.ord_date_time  as OrdDtTym,a.order_qty as Qty
        from or_order_line a,or_order_line_ph b, or_order c, mp_patient d, ph_drug e, ph_generic_name f
        where a.order_id = b.order_id and c.order_id = b.order_id and c.patient_id = d.patient_id
        and b.INTERACTION_OVERRIDE_REASON is not null
        and a.order_catalog_code = e.item_code and e.generic_id = f.generic_id
        and b.modified_date between  :from_date and to_date(:to_date)+1
        and a.added_by_id like 'KH%'
        order by c.patient_id,f.generic_name 

''')
        self.cursor.execute(get_drug_interaction_override_report_query,[from_date,to_date])
        get_drug_interaction_override_report_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_drug_interaction_override_report_data



    def get_credit_outstanding_bill_value(self,facility_code,from_date,to_date):
        get_credit_outstanding_bill_qurey = (''' 
        
       select distinct pack.patient_id,pack.NAME_PREFIX,pack.FIRST_NAME,pack.SECOND_NAME,pack.FAMILY_NAME,
       pack.ADDED_DATE,pack.LONG_DESC,B.LONG_DESC Service_name,a.blng_serv_code,
       a.trx_date,T.PRACTITIONER_NAME,T.primary_speciality_code,a.serv_item_desc,A.ORG_GROSS_CHARGE_AMT from bl_patient_charges_folio a,bl_blng_serv b,am_practitioner t,
       (select E.patient_id,E.EPISODE_ID,M.NAME_PREFIX,M.FIRST_NAME,M.SECOND_NAME,M.FAMILY_NAME,H.ADDED_DATE,P.LONG_DESC  from
       mp_patient M,pr_encounter E,bl_package_sub_hdr h,bl_package p,bl_package_encounter_dtls f
       where e.specialty_code ='EHC'
       and M.PATIENT_ID =E.PATIENT_ID and E.ADDED_FACILITY_ID=:facility_code and H.PACKAGE_CODE=P.PACKAGE_CODE and f.PACKAGE_SEQ_NO = h.PACKAGE_SEQ_NO and f.PACKAGE_CODE = h.PACKAGE_CODE
       and f.PATIENT_ID =h.PATIENT_ID and f.ENCOUNTER_ID = e.EPISODE_ID
       and h.status='C' and p.OPERATING_FACILITY_ID ='KH' and h.added_date between :from_date and :to_date)pack
       where pack.patient_id=a.patient_id and NVL(trx_STATUS,'X')<>'C'and a.trx_date >pack.added_date and A.BLNG_SERV_CODE =B.BLNG_SERV_CODE(+)
       and A.PHYSICIAN_ID=T.PRACTITIONER_ID(+)
       and a.blng_Serv_code not in ('HSPK000001') and  a.OPERATING_FACILITY_ID=:facility_code
        and pack.added_date between :from_date and :to_date



''')

        self.cursor.execute(get_credit_outstanding_bill_qurey,[facility_code,from_date,to_date])
        get_credit_outstanding_bill_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_credit_outstanding_bill_data


    def get_tpa_letter(self,facility_code,from_date,to_date):
        get_tpa_letter_qurey = (''' 
        
       SELECT distinct a.patient_id,b.PATIENT_NAME,TRUNC(a.DISCHARGE_DATE_TIME) DISCHARGE_DATE_TIME ,
       h.long_name,f.TOT_BUS_GEN_AMT Total_Amount, i.bill_amt Pay_by_TPA, 
       f.BILL_DOC_NUMBER Bill_Number, to_char(g.policy_number), to_char(g.credit_auth_ref),i.doc_date
       FROM pr_encounter a, mp_patient b,am_practitioner c, am_speciality d,ip_bed_class e, bl_episode_fin_dtls f,
       BL_ENCOUNTER_PAYER_APPROVAL g, AR_CUSTOMER H, BL_Bill_HDR I
       WHERE a.PATIENT_ID = b.PATIENT_ID(+) AND a.ATTEND_PRACTITIONER_ID = c.PRACTITIONER_ID(+) and i.CUST_CODE = h.cust_code(+)
       and a.PATIENT_ID = f.PATIENT_ID(+) and a.episode_id = f.episode_id(+) and f.episode_id = g.episode_id(+) and g.episode_type = 'I'
       and a.patient_id = i.patient_id and a.episode_id = i.episode_id and a.episode_id = g.episode_id
       AND a.SPECIALTY_CODE = d.SPECIALITY_CODE(+) and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE(+) AND a.patient_class = 'IP'
       and a.cancel_reason_code is null and i.BLNG_GRP_ID IN('TPA','GTPA') and i.bill_amt <> 0
       and f.cust_code not in ('50000004', '50000047', '401240', '30000332')
       AND TRUNC(i.doc_date) between :from_date and :to_date
       and f.OPERATING_FACILITY_ID = :facility_code



''')

        self.cursor.execute(get_tpa_letter_qurey,[from_date,to_date,facility_code])
        get_tpa_letter_data = self.cursor.fetchall()


        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_tpa_letter_data


    
    def get_online_consultation_report(self,from_date,to_date):
        get_online_consultation_report_qurey = (''' 
        
       SELECT   TO_CHAR (a.service_date, 'DD/MM/YY') ser_date,TO_CHAR (a.service_date, 'HH24:MI:SS') ser_time, a.blng_serv_code serv_code, c.long_desc serv_desc,DECODE (a.episode_type,'I', 'IP','O', 'OP','E', 'Emergency','R', 'Referral','D', 'Daycare') pat_Type,
       a.patient_id pat_id, b.short_name pat_name, a.upd_net_charge_amt amount, a.episode_id episode_id, a.blng_class_code blng_class_code, a.bed_class_code bed_class_code, a.serv_qty, a.physician_id,p.LONG_DESC
       FROM bl_patient_charges_folio a, mp_patient_mast b,bl_blng_serv c, BL_PACKAGE_ENCOUNTER_DTLS e,bl_package p
       WHERE a.operating_facility_id = 'KH' AND a.patient_id = b.patient_id AND a.blng_serv_code = c.blng_serv_code
       and NVL(A.BILLED_FLAG,'N') = decode(a.episode_type, 'O', 'Y', 'E', 'Y', 'R', 'Y', NVL(A.BILLED_FLAG, 'N'))
       AND a.service_date between :from_date and :to_date  and a.blng_serv_code in ('CNOP000029', 'CNOP000040', 'CNOP000041', 'CNOP000044')
       and a.ENCOUNTER_ID = e.ENCOUNTER_ID(+) and a.PACKAGE_SEQ_NO = e.PACKAGE_SEQ_NO(+) and a.OPERATING_FACILITY_ID = e.OPERATING_FACILITY_ID(+)
       and e.PACKAGE_CODE = p.PACKAGE_CODE(+) and e.OPERATING_FACILITY_ID = p.OPERATING_FACILITY_ID(+)
    


''')

        self.cursor.execute(get_online_consultation_report_qurey,[from_date,to_date])
        get_online_consultation_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_online_consultation_report_data
        


    def get_contract_report(self,facility_code):

        get_contract_report_qurey = ('''
        
        
            select CUST_CODE,LONG_NAME,CUST_GROUP_CODE,IP_YN,OP_YN,VALID_TO,MODIFIED_FACILITY_ID from ar_customer where MODIFIED_FACILITY_ID = :facility_code and VALID_TO is not null  and ADDED_FACILITY_ID =:facility_code order by VALID_TO 
        
        ''')

        self.cursor.execute(get_contract_report_qurey,[facility_code])
        get_contract_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_contract_report_data  
    



    def get_package_contract_report(self,from_date,to_date,facility_code):
        get_package_contract_report_qurey = (''' 
        
       select PACKAGE_CODE,LONG_DESC,EFF_TO_DATE,OP_YN,IP_YN from BL_PACKAGE where EFF_TO_DATE between :from_date and :to_date and OPERATING_FACILITY_ID = :facility_code and EFF_TO_DATE is not null order by EFF_TO_DATE
      


''')

        self.cursor.execute(get_package_contract_report_qurey,[from_date,to_date,facility_code])
        get_package_contract_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_package_contract_report_data



    def get_credit_card_reconciliation_report(self,facility_code,from_date,to_date):
        get_credit_card_reconciliation_report_qurey = (''' 
        
       select  TO_CHAR (d.doc_date, 'DD/MM/YY') dat,TO_CHAR (d.doc_date, 'HH24:MI:SS') tim,d.doc_type_code||'/'||d.doc_number rec_doc_no,d.patient_id UHID,
       a.SHORT_NAME patient_name,d.customer_code,c.payer_name,d.doc_amt amount,d.recpt_type_code,d.recpt_nature_code,d.recpt_refund_ind,
       c.slmt_type_code,c.slmt_doc_ref_desc ChqNo_CardNo,c.slmt_doc_remarks,d.NARRATION,c.cash_slmt_flag,d.cash_counter_code,
       d.added_by_id,c.cancelled_ind,c.bank_code,c.bank_branch,d.bill_doc_type_code||'/'||d.bill_doc_number bill_no,d.episode_id,
       c.APPROVAL_REF_NO,c.RCPT_RFND_ID_NO TID,c.CC_BATCH_NO, c.CC_SALE_DRAFT_NO,c.TERM_ID_NUM,C.RCPT_RFND_ID_NO
       FROM bl_receipt_refund_dtl c, bl_receipt_refund_hdr d,mp_patient_mast a,BL_SLMT_TYPE e
       WHERE  c.operating_facility_id = :facility_code  AND TRUNC (d.doc_date) between :from_date and :to_date
       AND c.doc_type_code = d.doc_type_code
       AND c.doc_number = d.doc_number and( d.RECPT_REFUND_IND='R' or (d.RECPT_REFUND_IND='F' and d.recpt_nature_code='BI'))
       and c.SLMT_TYPE_CODE=e.SLMT_TYPE_CODE and e.CASH_SLMT_FLAG='A'and d.patient_id = a.patient_id
       AND NOT EXISTS ( SELECT 1 FROM bl_cancelled_bounced_trx f WHERE f.doc_type_code = d.doc_type_code AND f.doc_number = d.doc_number
       AND trunc(f.cancelled_date) >= to_date(:from_date,'DD/MM/YYYY')
       AND NVL (d.cancelled_ind, 'N') = 'Y' AND trunc(f.cancelled_date)  < to_date(:to_date,'DD/MM/YYYY')+1)
       union all
       select  TO_CHAR (f.cancelled_date, 'DD/MM/YY') dat,TO_CHAR (f.cancelled_date, 'HH24:MI:SS') tim,d.doc_type_code||'/'||d.doc_number rec_doc_no,d.patient_id UHID,
       a.SHORT_NAME patient_name,d.customer_code,c.payer_name,-1*d.doc_amt amount,d.recpt_type_code,d.recpt_nature_code,d.recpt_refund_ind,
       c.slmt_type_code,c.slmt_doc_ref_desc ChqNo_CardNo,c.slmt_doc_remarks,d.NARRATION,c.cash_slmt_flag,d.cash_counter_code,
       d.added_by_id,c.cancelled_ind,c.bank_code,c.bank_branch ,d.bill_doc_type_code||'/'||d.bill_doc_number bill_no,d.episode_id,c.APPROVAL_REF_NO,
       c.RCPT_RFND_ID_NO TID,c.CC_BATCH_NO, c.CC_SALE_DRAFT_NO,c.TERM_ID_NUM,C.RCPT_RFND_ID_NO
       FROM bl_receipt_refund_dtl c, bl_receipt_refund_hdr d,mp_patient_mast a,bl_cancelled_bounced_trx f ,BL_SLMT_TYPE e
       WHERE  c.operating_facility_id = :facility_code  AND c.doc_type_code = d.doc_type_code AND c.doc_number = d.doc_number
       and d.patient_id = a.patient_id and( d.RECPT_REFUND_IND='R' or (d.RECPT_REFUND_IND='F' and d.recpt_nature_code='BI'))
       and c.SLMT_TYPE_CODE=e.SLMT_TYPE_CODE and e.CASH_SLMT_FLAG='A'and f.doc_type_code = d.doc_type_code AND f.doc_number = d.doc_number
       AND trunc(f.cancelled_date)  >= to_date(:from_date ,'DD/MM/YYYY') AND trunc(f.cancelled_date)  < to_date(:to_date,'DD/MM/YYYY')+1
       AND trunc(f.cancelled_date)  > trunc(d.doc_date) AND NVL (d.cancelled_ind, 'N') = 'Y' 
      


''')

        self.cursor.execute(get_credit_card_reconciliation_report_qurey,[facility_code,from_date,to_date])
        get_credit_card_reconciliation_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_credit_card_reconciliation_report_data



    def get_covid_ot_surgery_details(self,facility_code,from_date,to_date):
        get_covid_ot_surgery_details_qurey = (''' 
        
       select distinct g.patient_id,b.patient_name,get_age(b.date_of_birth,SYSDATE) Age,b.sex,C.ORDER_ID,a.ENCOUNTER_ID COVID_TEST_ENCOUNTER_,g.ENCOUNTER_ID OT_ORDERED_ENCOUNTER,g.ORDER_DATE_TIME OT_ORDER_TIME,C.ORDER_CATALOG_CODE,C.CATALOG_DESC,
       g.pref_surg_date, D.PRACTITIONER_NAME,E.LONG_DESC,g.added_date,dbms_lob.substr(f.ORDER_COMMENT,5000,1),o.ord_date_time,SPEC_REGD_DATE_TIME,
       o.PATIENT_CLASS, t.result_text result
       from ot_pending_order g,mp_patient b, or_order_line c,AM_PRACTITIONER d,AM_SPECIALITY e,or_order_comment f,
       or_order o,OR_ORDER_LINE L,RL_REQUEST_HEADER A,RL_result_text t
       where o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMB000094' and o.ORDER_STATUS = 'CD'
       and t.SPECIMEN_NO(+)=a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and  o.ORDERING_FACILITY_ID= :facility_code
       and g.patient_id = a.patient_id and a.patient_id = b.patient_id and g.order_id = c.order_id
       and g.PHYSICIAN_ID = D.PRACTITIONER_ID and g.order_id = f.order_id(+) and D.PRIMARY_SPECIALITY_CODE = E.SPECIALITY_CODE
       AND trunc(PREF_SURG_DATE)  between :from_date and :to_date
      
''')

        self.cursor.execute(get_covid_ot_surgery_details_qurey,[facility_code,from_date,to_date])
        get_covid_ot_surgery_details_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_covid_ot_surgery_details_data



    def get_gst_data_of_pharmacy(self):

        gst_data_of_pharmacy_qurey = ('''
        
        
            Select * from gst_data_ph
        
        ''')

        self.cursor.execute(gst_data_of_pharmacy_qurey)
        gst_data_of_pharmacy_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return gst_data_of_pharmacy_data
    



    def get_gst_data_of_pharmacy_return(self):

        gst_data_of_pharmacy_return_qurey = ('''
        
        
            Select * from gst_data_ph_ret
        
        ''')

        self.cursor.execute(gst_data_of_pharmacy_return_qurey)
        gst_data_of_pharmacy_return_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return gst_data_of_pharmacy_return_data



    def get_gst_data_of_ip(self):

        gst_data_of_ip_qurey = ('''
        
        
            Select * from gst_data_ip
        
        ''')

        self.cursor.execute(gst_data_of_ip_qurey)
        gst_data_of_ip_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return gst_data_of_ip_data




    def get_gst_data_of_op(self):

        gst_data_of_op_qurey = ('''
        
        
            Select * from gst_data_op
        
        ''')

        self.cursor.execute(gst_data_of_op_qurey)
        gst_data_of_op_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return gst_data_of_op_data

    

    def get_revenue_data_of_sl(self):

        get_revenue_data_of_sl_qurey = ('''
        
        
            select * from revenue_data_sl
        
        ''')

        self.cursor.execute(get_revenue_data_of_sl_qurey)
        get_revenue_data_of_sl_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_revenue_data_of_sl_data

    

    def get_revenue_data_of_sl1(self):

        get_revenue_data_of_sl1_qurey = ('''
        
        
            select * from revenue_data_sl1
        
        ''')

        self.cursor.execute(get_revenue_data_of_sl1_qurey)
        get_revenue_data_of_sl1_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_revenue_data_of_sl1_data
    

    def get_revenue_data_of_sl2(self):

        get_revenue_data_of_sl2_qurey = ('''
        
        
            select * from revenue_data_sl2
        
        ''')

        self.cursor.execute(get_revenue_data_of_sl2_qurey)
        get_revenue_data_of_sl2_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_revenue_data_of_sl2_data

    def get_discharge_with_mis_report(self,facility_code,from_date,to_date):
        discharge_with_mis_report_qurey = (''' 
        
       select a.PATIENT_ID, b.patient_name, a.VISIT_ADM_DATE_TIME Admission_Time, E.LONG_DESC,a.assign_bed_num,   c.DIS_ADV_DATE_TIME DISCHARGE_REQUEST_TIME,c.EXPECTED_DISCHARGE_DATE ,D.BILL_DOC_DATE,a.DISCHARGE_DATE_TIME Bed_Clear_Date_Time,D.BLNG_GRP_ID,  f.PRACTITIONER_NAME Treating_Doctor,g.LONG_DESC Speciality,c.ENCOUNTER_ID,c.added_by_id,h.appl_user_name,i.AUTHORIZED_DATE_TIME  from pr_encounter a, mp_patient b, ip_discharge_advice c, bl_episode_fin_dtls d,ip_bed_class e,am_practitioner f,am_speciality g,sm_appl_user h,CA_ENCNTR_NOTE i  where a.PATIENT_ID=b.PATIENT_ID and a.PATIENT_CLASS = 'IP' and a.ENCOUNTER_ID=c.ENCOUNTER_ID and a.ENCOUNTER_ID=d.EPISODE_ID   and a.ENCOUNTER_ID=i.ENCOUNTER_ID  and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE   and a.ATTEND_PRACTITIONER_ID =f.PRACTITIONER_ID  AND a.SPECIALTY_CODE = g.SPECIALITY_CODE  and c.added_by_id = h.appl_user_id  and i.note_type= 'DIST' and a.FACILITY_ID =:facility_code and DIS_ADV_STATUS = '0'  and trunc(d.bill_doc_date) between :from_date and :to_date  order by BILL_DOC_DATE
                 
      
''')

        self.cursor.execute(discharge_with_mis_report_qurey,[facility_code,from_date,to_date])
        get_covid_ot_surgery_details_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_covid_ot_surgery_details_data


    def get_pre_discharge_report(self,from_date,to_date):
        pre_discharge_report_qurey = (''' 

        select a.PATIENT_ID, b.patient_name, a.VISIT_ADM_DATE_TIME Admission_Time, E.LONG_DESC,a.assign_bed_num,a.ASSIGN_CARE_LOCN_CODE,
        c.DIS_ADV_DATE_TIME DISCHARGE_REQUEST_TIME, c.EXPECTED_DISCHARGE_DATE ,D.BILL_DOC_DATE,a.DISCHARGE_DATE_TIME Bed_Clear_Date_Time, n.LAST_AMENDED_DATE_TIME,n.AUTHORIZED_DATE_TIME, D.BLNG_GRP_ID,
        f.PRACTITIONER_NAME Treating_Doctor, g.LONG_DESC Speciality, c.ENCOUNTER_ID,c.added_by_id,h.appl_user_name,b.ALT_ID2_NO AS PR_NO,
        B.Contact2_no AS Patient_no,b.Contact3_no as Relative_No from pr_encounter a, mp_patient b, ip_discharge_advice c, bl_episode_fin_dtls d, ip_bed_class e, am_practitioner f, am_speciality g, sm_appl_user h, ca_encntr_note n
        where a.PATIENT_ID = b.PATIENT_ID and a.PATIENT_CLASS = 'IP' and a.ENCOUNTER_ID = c.ENCOUNTER_ID and a.ENCOUNTER_ID = d.EPISODE_ID  and n.PATIENT_ID = c.PATIENT_ID and
        n.ENCOUNTER_ID = c.ENCOUNTER_ID
        and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE
        and a.ATTEND_PRACTITIONER_ID = f.PRACTITIONER_ID
        AND a.SPECIALTY_CODE = g.SPECIALITY_CODE
        and c.added_by_id = h.appl_user_id
        and DIS_ADV_STATUS = '1' and a.FACILITY_ID = 'KH'
        and trunc (a.VISIT_ADM_DATE_TIME) between :from_date and :to_date 
        order by BILL_DOC_DATE


''')    
    
        self.cursor.execute(pre_discharge_report_qurey,[from_date,to_date])
        pre_discharge_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return pre_discharge_report_data


    def get_discharge_report_2(self,from_date,to_date):
        discharge_report_2_qurey = (''' 

        select a.PATIENT_ID,b.patient_name,a.VISIT_ADM_DATE_TIME as Admission_Time,
        f.LONG_DESC BED_CLASS,a.ASSIGN_BED_NUM as BED_NUMBER,i.LONG_DESC as BED_LOCATION,p.practitioner_name,
        a.PRE_DIS_INITIATED_DATE_TIME as DRS_DISCHARGE_ADVISE_TIME,c.DIS_ADV_DATE_TIME as Nursing_Predischarge,
        max(e.AUTHORIZED_DATE_TIME) as Discharge_Summary_time,
        D.BILL_DOC_DATE,a.DISCHARGE_DATE_TIME as bedClear,D.BLNG_GRP_ID,
        trunc(a.DISCHARGE_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) || ' dy, ' || mod(trunc((a.DISCHARGE_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) * 24), 24)  || ' hr, ' || mod(trunc((a.DISCHARGE_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) * 1440), 60)  || ' mn, ' || mod(trunc((a.DISCHARGE_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) * 86400), 60)  || ' sc ' as BedClearnctoDschrgeAdvs ,
        trunc(c.DIS_ADV_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) || ' dy, ' || mod(trunc((c.DIS_ADV_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) * 24), 24)  || ' hr, ' || mod(trunc((c.DIS_ADV_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) * 1440), 60)  || ' mn, ' || mod(trunc((c.DIS_ADV_DATE_TIME-a.PRE_DIS_INITIATED_DATE_TIME) * 86400), 60)  || ' sc ' as NrsgPredschrgetoDschrgeIntmtn,
        trunc(D.BILL_DOC_DATE-a.PRE_DIS_INITIATED_DATE_TIME) || ' dy, ' || mod(trunc((D.BILL_DOC_DATE-a.PRE_DIS_INITIATED_DATE_TIME) * 24), 24)  || ' hr, ' || mod(trunc((D.BILL_DOC_DATE-a.PRE_DIS_INITIATED_DATE_TIME) * 1440), 60)  || ' mn, ' || mod(trunc((D.BILL_DOC_DATE-a.PRE_DIS_INITIATED_DATE_TIME) * 86400), 60)  || ' sc ' as FinlBilPdTmtoDrsDschrgAdvcTim,
        trunc(a.DISCHARGE_DATE_TIME-D.BILL_DOC_DATE) || ' dy, ' || mod(trunc((a.DISCHARGE_DATE_TIME-D.BILL_DOC_DATE) * 24), 24)  || ' hr, ' || mod(trunc((a.DISCHARGE_DATE_TIME-D.BILL_DOC_DATE) * 1440), 60)  || ' mn, ' || mod(trunc((a.DISCHARGE_DATE_TIME-D.BILL_DOC_DATE) * 86400), 60)  || ' sc ' as BdClrnctoFinalBilPdTim
        from pr_encounter a, mp_patient b,bl_episode_fin_dtls d, ip_nursing_unit i,am_practitioner p,ip_discharge_advice c,ca_encntr_note e,ip_bed_class f
        where a.PATIENT_ID=b.PATIENT_ID and a.ENCOUNTER_ID=c.ENCOUNTER_ID and d.bill_doc_type_code='IPBL' and a.ASSIGN_CARE_LOCN_CODE = i.NURSING_UNIT_CODE and a.ENCOUNTER_ID=d.EPISODE_ID 
        and a.ADMIT_PRACTITIONER_ID=p.PRACTITIONER_ID and e.ENCOUNTER_ID(+) = c.ENCOUNTER_ID and a.ASSIGN_BED_CLASS_CODE   = f.BED_CLASS_CODE and  trunc(a.DISCHARGE_DATE_TIME) between :from_date and :to_date
        and DIS_ADV_STATUS = '1' group by a.PATIENT_ID, b.patient_name,a.PRE_DIS_INITIATED_DATE_TIME, a.VISIT_ADM_DATE_TIME ,f.LONG_DESC,a.ASSIGN_BED_NUM ,i.LONG_DESC,d.BED_BILL_BED_TYPE_CODE,p.practitioner_name ,c.DIS_ADV_DATE_TIME ,D.BILL_DOC_DATE,a.DISCHARGE_DATE_TIME,D.BLNG_GRP_ID order by 1 desc


''')    
    
        self.cursor.execute(discharge_report_2_qurey,[from_date,to_date])
        discharge_report_2_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return discharge_report_2_data


    def get_revenue_data_of_sl3(self,facility_code,from_date,to_date):
        get_revenue_data_of_sl3_qurey = (''' 
        
       SELECT NULL ser_date, NULL ser_time,
                                       --a.acct_dept_code dept_code, e.long_desc dept_name,
          NULL txn_date, NULL txn_time, NULL serv_code, NULL serv_desc,
          NULL serv_grp_code, NULL serv_grp_desc, NULL physician_id,
          NULL patienttype, NULL patient_id, NULL pat_name,
          NVL (f.amount, 0) amount, NVL (d.amount, 0) disc_amount,
          NVL (o.amount, 0) rounding_amount, 0 addl_chg, NULL episode_id,
          NULL encounter_id, NULL store_code, NULL blng_class_code,
          NULL bed_class_code, f.main_acc1_code gl_code,
          f.dept_code dept_code_rev
     FROM (SELECT   gl.main_acc1_code, gl.dept_code,
                    DECODE (gl.trx_type_code,
                            'F', SUM (gl.distribution_amt),
                            0
                           ) amount
               FROM bl_gl_distribution gl
              WHERE gl.operating_facility_id = :facility_code
                AND gl.trx_date BETWEEN :from_date and :to_date
                AND gl.main_acc1_code = '222410'
                AND gl.trx_type_code = 'F'
           GROUP BY gl.main_acc1_code, gl.dept_code, gl.trx_type_code) f,
          (SELECT   gl.main_acc1_code, gl.dept_code,
                    DECODE (gl.trx_type_code,
                            'D', SUM (gl.distribution_amt),
                            0
                           ) amount
               FROM bl_gl_distribution gl
              WHERE gl.operating_facility_id = :facility_code
                AND gl.trx_date BETWEEN :from_date and :to_date
                AND gl.main_acc1_code = '222410'
                AND gl.trx_type_code = 'D'
           GROUP BY gl.main_acc1_code, gl.dept_code, gl.trx_type_code) d,
          (SELECT   gl.main_acc1_code, gl.dept_code,
                    DECODE (gl.trx_type_code,
                            'O', SUM (gl.distribution_amt),
                            0
                           ) amount
               FROM bl_gl_distribution gl
              WHERE gl.operating_facility_id = :facility_code
                AND gl.trx_date BETWEEN :from_date and :to_date
                AND gl.main_acc1_code = '222410'
                AND gl.trx_type_code = 'O'
           GROUP BY gl.main_acc1_code, gl.dept_code, gl.trx_type_code) o
    WHERE f.main_acc1_code = d.main_acc1_code(+) AND f.main_acc1_code = o.main_acc1_code(+)
   UNION ALL
   SELECT TO_CHAR (a.service_date, 'DD/MM/YY') ser_date,
          TO_CHAR (a.service_date, 'HH24:MI:SS') ser_time,
          
          --a.acct_dept_code dept_code, e.long_desc dept_name,
          TO_CHAR (a.trx_date, 'DD/MM/YY') txn_date,
          TO_CHAR (a.trx_date, 'HH24:MI:SS') txn_time,
          a.blng_serv_code serv_code, c.long_desc serv_desc,
          c.serv_grp_code serv_grp_code, d.long_desc serv_grp_desc,
          a.physician_id physician_id,
          DECODE (a.episode_type,
                  'I', 'IP',
                  'O', 'OP',
                  'E', 'Emergency',
                  'R', 'Referral',
                  'D', 'Daycare'
                 ) patienttype,
          a.patient_id patient_id, b.short_name pat_name,
          (CASE
              WHEN a.episode_type <> 'R'
              AND ((a.addl_charge_amt_in_charge * -1) = gl.distribution_amt)
                 THEN
                     --decode(gl.main_Acc1_code ,140211,(a.addl_charge_amt_in_charge*-1),0)
                     DECODE (gl.main_acc1_code,
                             140211, (a.addl_charge_amt_in_charge * -1),
                             140212, (a.addl_charge_amt_in_charge * -1),
                             140213, (a.addl_charge_amt_in_charge * -1),
                             140214, (a.addl_charge_amt_in_charge * -1),
                             0
                            )
              ELSE DECODE (gl.trx_type_code, 'F', gl.distribution_amt, 0)
           END
          ) amount,
          
          --DECODE(gl.trx_type_code,'F',gl.distribution_amt, 0)amount,
          DECODE (gl.trx_type_code, 'D', gl.distribution_amt, 0) disc_amount,
          DECODE (gl.trx_type_code,
                  'O', gl.distribution_amt,
                  0
                 ) rounding_amt,
          
          -- ADDED ON 30/10/2012
          (CASE
              WHEN a.episode_type = 'R' AND (gl.rule_code LIKE 'RULE%')
                 THEN (a.addl_charge_amt_in_charge)
              WHEN a.episode_type <> 'R' AND (gl.rule_code LIKE 'S%')
                 THEN (a.addl_charge_amt_in_charge)
              WHEN a.episode_type <> 'R'
              AND ((a.addl_charge_amt_in_charge * -1) = gl.distribution_amt)
                 THEN 0
              ELSE 0
           END
          ) addl_chg,
          
          -- 30/10/2012 commented DECODE (a.episode_type,'R', NVL (a.addl_charge_amt_in_charge, 0),0) addl_chg,
          a.episode_id episode_id, a.encounter_id encounter_id,
          a.store_code store_code, a.blng_class_code blng_class_code,
          a.bed_class_code bed_class_code, gl.main_acc1_code gl_code,
          gl.dept_code dept_code_rev
     FROM bl_gl_distribution gl,
          bl_patient_charges_folio a,
          mp_patient_mast b,
          bl_blng_serv c,
          bl_blng_serv_grp d,
          am_dept_lang_vw e
    WHERE a.operating_facility_id = :facility_code
      AND a.patient_id = gl.patient_id
      AND a.patient_id = b.patient_id
      AND a.trx_doc_ref = gl.trx_doc_ref
      AND a.trx_doc_ref_line_num = gl.trx_doc_ref_line_num
      AND a.trx_doc_ref_seq_num = gl.trx_doc_ref_seq_num
      AND gl.trx_date BETWEEN :from_date and :to_date
      AND gl.main_acc1_code <> '222410'
      AND a.blng_serv_code = c.blng_serv_code
      AND c.serv_grp_code = d.serv_grp_code
      AND a.acct_dept_code = e.dept_code(+)
   UNION ALL
   SELECT TO_CHAR (a.doc_date, 'DD/MM/YY') ser_date,
          TO_CHAR (a.doc_date, 'HH24:MI:SS') ser_time,
              --gl.dept_code dept_code, e.long_desc dept_name,
          TO_CHAR (gl.trx_date, 'DD/MM/YY') txn_date,
          TO_CHAR (gl.trx_date, 'HH24:MI:SS') txn_time, NULL serv_code,
          'Discount' serv_desc, NULL serv_grp_code, NULL serv_grp_desc,
          NULL physician_id,
          DECODE (a.episode_type,
                  'I', 'IP',
                  'O', 'OP',
                  'E', 'Emergency',
                  'R', 'Referral',
                  'D', 'Daycare'
                 ) patienttype,
          a.patient_id patient_id, b.short_name pat_name, 0 amount,
          NVL (a.overall_disc_amt, 0) disc_amount, 0 rounding_amt, 0 addl_chg,
          a.episode_id episode_id, a.encounter_id encounter_id, NULL, NULL,
          a.bed_class_code bed_class_code, gl.main_acc1_code gl_code,
          gl.dept_code dept_code_rev
     FROM bl_gl_distribution gl,
          bl_bill_hdr a,
          mp_patient_mast b,
          am_dept_lang_vw e
    WHERE a.operating_facility_id = :facility_code
      AND a.patient_id = gl.patient_id
      AND a.patient_id = b.patient_id
      AND a.doc_date = gl.trx_date
      AND a.doc_type_code = gl.doc_type
      AND a.doc_num = gl.doc_no
      AND a.overall_disc_amt <> 0
      AND gl.trx_date BETWEEN :from_date and :to_date
      --05/07/2012 AND gl.main_acc1_code  in  ('222410','409998','400570','400590','400580','400600','400610','400620','400630','400640','400650','400660','400670','400680')  -- ONLY DISCOUNT
      AND gl.main_acc1_code IN
             ('409998', '400570', '400575', '400590', '400580', '400600',
              '400610', '400620', '400630', '400640', '400650', '400660',
              '400670', '400680')                             -- ONLY DISCOUNT
      AND gl.trx_type_code = 'D'
      AND gl.dept_code = e.dept_code(+)
   UNION ALL
   SELECT TO_CHAR (a.doc_date, 'DD/MM/YY') ser_date,
          TO_CHAR (a.doc_date, 'HH24:MI:SS') ser_time,
          
          --gl.dept_code dept_code, e.long_desc dept_name,
          TO_CHAR (gl.trx_date, 'DD/MM/YY') txn_date,
          TO_CHAR (gl.trx_date, 'HH24:MI:SS') txn_time, NULL serv_code,
          'Rounding off' serv_desc, NULL serv_grp_code, NULL serv_grp_desc,
          NULL physician_id,
          DECODE (a.episode_type,
                  'I', 'IP',
                  'O', 'OP',
                  'E', 'Emergency',
                  'R', 'Referral',
                  'D', 'Daycare'
                 ) patienttype,
          a.patient_id patient_id, b.short_name pat_name, 0 amount,
          0 disc_amount, NVL (a.bill_rounding_amt, 0) rounding_amt,
          0 addl_chg, a.episode_id episode_id, a.encounter_id encounter_id,
          NULL, NULL, a.bed_class_code bed_class_code,
          gl.main_acc1_code gl_code, gl.dept_code dept_code_rev
     FROM bl_gl_distribution gl,
          bl_bill_hdr a,
          mp_patient_mast b,
          am_dept_lang_vw e
    WHERE a.operating_facility_id = :facility_code
      AND a.patient_id = gl.patient_id
      AND a.patient_id = b.patient_id
      AND a.doc_date = gl.trx_date
      AND a.doc_type_code = gl.doc_type
      AND a.doc_num = gl.doc_no
      AND a.bill_rounding_amt <> 0
      AND gl.trx_date BETWEEN :from_date and :to_date
      AND gl.main_acc1_code IN ('401220')                 -- ONLY ROUNDING OFF
      AND gl.trx_type_code = 'O'
      AND gl.dept_code = e.dept_code(+)
      
      
''')

        self.cursor.execute(get_revenue_data_of_sl3_qurey,[facility_code,from_date,to_date])
        get_revenue_data_of_sl3_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_revenue_data_of_sl3_data


    

    def get_needle_prick_injury_report(self,facility_code,from_date,to_date):
        needle_prick_injury_report_qurey = (''' 
        
       SELECT  o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus,l.modified_date stat_change_date,CATALOG_DESC,A.PATIENT_ID,
       Patient_Name as PatientName,map.SEX,trunc((sysdate - map.DATE_OF_BIRTH) / 365, 0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,b.remark
       test_code,t.result_text result, 
       map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,
       F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,
       g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state  FROM or_order o,OR_ORDER_LINE L, RL_REQUEST_HEADER A,RL_result_text t, pr_encounter e,
       bl_episode_fin_dtls b, mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g, MP_RES_TOWN h , MP_RES_AREA i, mp_region j
       WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMB000094' and a.PATIENT_ID = map.PATIENT_ID
       and f.POSTAL1_CODE = g.POSTAL_CODE(+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+)
       and i.REGION_CODE = j.REGION_CODE(+) AND A.PATIENT_ID = F.PATIENT_ID
       and t.SPECIMEN_NO(+) = a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+) = o.ORDER_STATUS
       and o.PATIENT_ID = b.PATIENT_ID and o.episode_id = b.episode_id and   o.ORDERING_FACILITY_ID=:facility_code
       and e.PATIENT_ID = o.PATIENT_ID and e.EPISODE_ID = o.EPISODE_ID AND o.ORD_DATE_TIME BETWEEN :from_date and :to_date        
      
''')

        self.cursor.execute(needle_prick_injury_report_qurey,[facility_code,from_date,to_date])
        needle_prick_injury_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return needle_prick_injury_report_data


    def get_practo_report(self,facility_code,from_date,to_date):
        practo_report_qurey = (''' 
        
       select a.CONTACT_REASON_CODE,c.CONTACT_REASON,PATIENT_NAME,PATIENT_ID,encounter_id,PRACTITIONER_Name,a.ADDED_DATE,a.ADDED_BY_ID,APPT_REMARKS from oa_appt a,am_practitioner p,am_contact_reason c where a.PRACTITIONER_ID = p.PRACTITIONER_ID and a.CONTACT_REASON_CODE=c.CONTACT_REASON_CODE and a.ADDED_FACILITY_ID=:facility_code and a.added_date between :from_date and :to_date 
      
      
''')

        self.cursor.execute(practo_report_qurey,[facility_code,from_date,to_date])
        practo_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return practo_report_data



    def get_unbilled_report(self,facility_code):

        get_unbilled_report_qurey = ('''
        
        
            select a.service_date,a.patient_id,b.patient_name,a.episode_id,a.Blng_grp_id,a.store_code, a.serv_item_code,a.serv_item_desc
 ,a.base_rate,a.serv_qty,a.base_charge_amt,a.org_net_charge_amt,a.trx_status,A.BILL_DOC_NUM from bl_patient_charges_folio a,mp_patient b 
 where prt_grp_hdr_code='PROCE' and episode_type ='O'and nvl(a.bill_doc_num,0)=0 and nvl(a.trx_status,'A')='A'  
 and a.service_date between sysdate-30 and (sysdate-1) + 0.99999
 and a.patient_id =b.patient_id and a.OPERATING_FACILITY_ID=:facility_code

        ''')

        self.cursor.execute(get_unbilled_report_qurey,[facility_code])
        get_unbilled_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_unbilled_report_data  


    def get_unbilled_deposit_report(self,facility_code):

        get_unbilled_deposit_report_qurey = ('''
        
        
            select distinct * from gst_data_ph a where a.BILL_DOC_DATE >= ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -30) and a.OPERATING_FACILITY_ID= :facility_code

        ''')

        self.cursor.execute(get_unbilled_deposit_report_qurey,[facility_code])
        get_unbilled_deposit_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_unbilled_deposit_report_data  



    def get_contact_report(self,facility_code,from_date,to_date):
        get_contact_report_qurey = (''' 
        
       select distinct e.practitioner_name,a.PATIENT_CLASS,a.patient_id,b.patient_name, a.SPECIALTY_CODE,VISIT_ADM_DATE_TIME,B.CONTACT1_NO,B.CONTACT2_NO ,b.EMAIL_ID from pr_encounter a,mp_patient b,am_practitioner e 
       where a.patient_id=b.patient_id 
       AND  A.PATIENT_ID=b.PATIENT_ID and  a.FACILITY_ID=:facility_code
       and a.ATTEND_PRACTITIONER_ID = e.practitioner_id 
       and a.SPECIALTY_CODE in ('EHC','NEPH','NEUR','UROL','SUON','GYNA','GNMD','MDON','ENDO','HPBL')  and  VISIT_ADM_DATE_TIME between :from_date and :to_date 
      
      
''')

        self.cursor.execute(get_contact_report_qurey,[facility_code,from_date,to_date])
        get_contact_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_contact_report_data
    

    def get_employees_antibodies_reactive_report(self,facility_code,from_date,to_date):
        employees_antibodies_reactive_report_qurey = (''' 
        
       SELECT  o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus,l.modified_date stat_change_date,CATALOG_DESC,A.PATIENT_ID,
       Patient_Name as PatientName,map.SEX,trunc((sysdate - map.DATE_OF_BIRTH) / 365, 0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,
       max(t.NUMERIC_RESULT) Numeric,max(t.RESULT_COMMENT_DESC1) text ,map.ALT_ID2_NO, map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,
       F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,
       g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state
       FROM or_order o,OR_ORDER_LINE L, RL_REQUEST_HEADER A,RL_test_result t, pr_encounter e,
       bl_episode_fin_dtls b, mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g, MP_RES_TOWN h , MP_RES_AREA i, mp_region j
       WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMC00223' and a.PATIENT_ID = map.PATIENT_ID
       and f.POSTAL1_CODE = g.POSTAL_CODE(+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+)
       and i.REGION_CODE = j.REGION_CODE(+) AND A.PATIENT_ID = F.PATIENT_ID
       and t.SPECIMEN_NO(+) = a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+) = o.ORDER_STATUS
       and t.TEST_CODE in ('CUTOFFINDE', 'SARC1')
       and b.BLNG_GRP_ID = 'EMPL'
       and o.PATIENT_ID = b.PATIENT_ID and o.episode_id = b.episode_id
       and e.PATIENT_ID = o.PATIENT_ID and e.EPISODE_ID = o.EPISODE_ID
       AND o.ORD_DATE_TIME BETWEEN :from_date and :to_date 
       and o.ORDERING_FACILITY_ID = :facility_code
       group by o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc ,l.modified_date ,CATALOG_DESC,A.PATIENT_ID,
       Patient_Name ,map.SEX,(sysdate - map.DATE_OF_BIRTH) / 365, 0 , o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,map.ALT_ID2_NO,
       map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,
       F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4  ,
       g.LONG_DESC , h.LONG_DESC , i.LONG_DESC , j.LONG_DESC
       having max(t.RESULT_COMMENT_DESC1) = 'Reactive'
      
''')

        self.cursor.execute(employees_antibodies_reactive_report_qurey,[facility_code,from_date,to_date])
        employees_antibodies_reactive_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return employees_antibodies_reactive_report_data
    

    def get_employees_reactive_and_non_pcr_report(self):

        employees_reactive_and_non_pcr_report_qurey = (" SELECT  A.PATIENT_ID,Patient_Name as PatientName,map.SEX,trunc((sysdate-map.DATE_OF_BIRTH)/365,0) age ,map.ALT_ID2_NO,map.EMAIL_ID,map.CONTACT1_NO, " +
" map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO, F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,  " +
" g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state " +
" FROM or_order o,OR_ORDER_LINE L,RL_REQUEST_HEADER A,RL_test_result t,pr_encounter e, " +
" bl_episode_fin_dtls b ,mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,MP_POSTAL_CODE g,MP_RES_TOWN h,MP_RES_AREA i,mp_region j " +
" WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMC00223' and a.PATIENT_ID = map.PATIENT_ID " +
" and f.POSTAL1_CODE = g.POSTAL_CODE (+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+) " +
" and i.REGION_CODE = j.REGION_CODE(+) AND  A.PATIENT_ID=F.PATIENT_ID  " +
" and t.SPECIMEN_NO(+)=a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+)= o.ORDER_STATUS " +
" and t.TEST_CODE in ('CUTOFFINDE', 'SARC1') and b.BLNG_GRP_ID = 'EMPL' and  o.PATIENT_ID=b.PATIENT_ID " +
" and o.episode_id = b.episode_id and e.PATIENT_ID =o.PATIENT_ID and e.EPISODE_ID=o.EPISODE_ID " +
" group by o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc ,l.modified_date ,CATALOG_DESC,A.PATIENT_ID, " +
" Patient_Name ,map.SEX,trunc((sysdate-map.DATE_OF_BIRTH)/365,0) , o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,map.ALT_ID2_NO, " +
" map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,  " +
" F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4,g.LONG_DESC ,h.LONG_DESC ,i.LONG_DESC ,j.LONG_DESC " +
" having max(t.RESULT_COMMENT_DESC1)='Reactive'  " +
" minus " +
" SELECT  A.PATIENT_ID,Patient_Name as PatientName,map.SEX,trunc((sysdate-map.DATE_OF_BIRTH)/365,0) age ,map.ALT_ID2_NO, map.EMAIL_ID,map.CONTACT1_NO, " +
" map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO, F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address , " +
" g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state " +
" FROM or_order o,OR_ORDER_LINE L,RL_REQUEST_HEADER A,RL_result_text t,pr_encounter e ," +
" bl_episode_fin_dtls b ,mp_patient map,or_order_status_code s,MP_PAT_ADDRESSES F ,MP_POSTAL_CODE g,MP_RES_TOWN h ,MP_RES_AREA i,mp_region j " +
" WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMB000094' and a.PATIENT_ID = map.PATIENT_ID " +
" and f.POSTAL1_CODE = g.POSTAL_CODE (+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+) " +
" and i.REGION_CODE = j.REGION_CODE(+) AND  A.PATIENT_ID=F.PATIENT_ID  " +
" and t.SPECIMEN_NO(+)=a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+)= o.ORDER_STATUS " +
" and  o.PATIENT_ID=b.PATIENT_ID and o.episode_id = b.episode_id and e.PATIENT_ID =o.PATIENT_ID and e.EPISODE_ID=o.EPISODE_ID  ")

        self.cursor.execute(employees_reactive_and_non_pcr_report_qurey)
        employees_reactive_and_non_pcr_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return employees_reactive_and_non_pcr_report_data
    

    def get_employee_covid_test_report(self,facility_code,from_date,to_date):
        employee_covid_test_report_qurey = (''' 
        
       SELECT  o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus,l.modified_date stat_change_date,CATALOG_DESC,A.PATIENT_ID,
       Patient_Name as PatientName,map.SEX,trunc((sysdate-map.DATE_OF_BIRTH)/365,0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,b.remark
       test_code,t.result_text result,map.ALT_ID2_NO ,map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,
       F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,g.LONG_DESC postalcode, h.LONG_DESC area,
       i.LONG_DESC town, j.LONG_DESC state  FROM or_order o,OR_ORDER_LINE L,RL_REQUEST_HEADER A,RL_result_text t,pr_encounter e,bl_episode_fin_dtls b,
       mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g,  MP_RES_TOWN h , MP_RES_AREA i, mp_region j
       WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMB000094' and a.PATIENT_ID = map.PATIENT_ID
       and f.POSTAL1_CODE = g.POSTAL_CODE (+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+)
       and i.REGION_CODE = j.REGION_CODE(+) AND  A.PATIENT_ID=F.PATIENT_ID and o.ORDERING_FACILITY_ID=:facility_code
       and t.SPECIMEN_NO(+)=a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+)= o.ORDER_STATUS
       and  o.PATIENT_ID=b.PATIENT_ID and o.episode_id = b.episode_id and b.BLNG_GRP_ID = 'EMPL'
       and e.PATIENT_ID =o.PATIENT_ID and e.EPISODE_ID=o.EPISODE_ID AND o.ORD_DATE_TIME between :from_date and :to_date 
      
''')

        self.cursor.execute(employee_covid_test_report_qurey,[facility_code,from_date,to_date])
        employee_covid_test_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return employee_covid_test_report_data


    def get_bed_location_report(self,facility_code):

        get_bed_location_report_qurey = ('''
        
        
            select o.patient_class,o.ord_date_time,s.long_desc,c.LONG_DESC,l.modified_date stat_change_date,o.patient_id,
            p.patient_name,i.BED_NUM,i.BED_ALLOCATION_DATE_TIME
            from or_order o,mp_patient p,or_order_status_code s,or_order_line l,or_order_catalog c,bl_order_catalog b,rd_section d,ip_open_encounter i
            where o.PATIENT_ID=p.PATIENT_ID and s.ORDER_STATUS_CODE=o.ORDER_STATUS and o.ORDER_TYPE_CODE=d.order_type_code
            and o.ORDER_ID=l.ORDER_ID and l.ORDER_CATALOG_CODE=c.ORDER_CATALOG_CODE and b.ORDER_CATALOG_CODE = c.ORDER_CATALOG_CODE
            and o.ENCOUNTER_ID=i.ENCOUNTER_ID and o.PATIENT_ID=i.PATIENT_ID and o.ORDERING_FACILITY_ID = :facility_code

        ''')

        self.cursor.execute(get_bed_location_report_qurey,[facility_code])
        get_bed_location_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_bed_location_report_data



    def get_home_visit_report(self,facility_code,from_date,to_date):
        home_visit_report_qurey = (''' 
        
       select DISTINCT a.patient_id,a.episode_id,ALL_DOC_TYPE_CODE BILL_TYPE,
       ALL_DOC_NUM Bill_NUM,b.ADDED_BY_ID,A.ADDED_DATE,C.aPPL_USER_NAME,e.VISIT_ADM_TYPE
       from bl_patient_ledger a,bl_bill_hdr b, SM_aPPL_USER C,pr_encounter e
       where b.doc_num = ALL_DOC_NUM  and b.doc_type_code = ALL_DOC_TYPE_CODE
       AND b.ADDED_BY_ID = C.APPL_USER_ID  and a.OPERATING_FACILITY_ID = :facility_code and a.PATIENT_ID =e.PATIENT_ID
       and a.EPISODE_ID = e.EPISODE_ID and a.EPISODE_TYPE = 'O' and e.VISIT_ADM_TYPE = 'HM'
       and  a.patient_id = b.patient_id  AND B.ADDED_DATE between :from_date and to_date(:to_date)+1
      
''')

        self.cursor.execute(home_visit_report_qurey,[facility_code,from_date,to_date])
        home_visit_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return home_visit_report_data


    def get_cco_billing_count_reports(self):

        get_cco_billing_count_reports_qurey = ('''
        
        
            select count(*),added_by_id from bl_bill_hdr where to_date(ADDED_DATE) >= to_date('01/04/2017', 'dd/mm/yyyy') and DOC_TYPE_CODE = 'OPBL' group by added_by_id
        
        ''')

        self.cursor.execute(get_cco_billing_count_reports_qurey)
        get_cco_billing_count_reports_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_cco_billing_count_reports_data

    
    def get_total_number_of_online_consultation_by_doctors(self,facility_code,from_date,to_date):
        total_number_of_online_consultation_by_doctors_qurey = (''' 
        
       SELECT nvl (m.PRACTITIONER_NAME, ' Grand Total :') practitioner_name , count(1) as total
       FROM bl_patient_charges_folio a,mp_patient_mast b,bl_blng_serv c,BL_PACKAGE_ENCOUNTER_DTLS e,bl_package p ,am_practitioner m
       WHERE a.operating_facility_id = :facility_code AND a.patient_id = b.patient_id AND a.blng_serv_code = c.blng_serv_code
       and NVL(A.BILLED_FLAG,'N') = decode(a.episode_type,'O','Y','E','Y','R','Y',NVL(A.BILLED_FLAG,'N'))
       AND a.service_date  between :from_date and :to_date  and e.OPERATING_FACILITY_ID = p.OPERATING_FACILITY_ID(+)
       and a.blng_serv_code in ('CNOP000029','CNOP000040','CNOP000041','CNOP000044') and a.ENCOUNTER_ID=e.ENCOUNTER_ID(+)
       and a.PACKAGE_SEQ_NO = e.PACKAGE_SEQ_NO(+) and a.OPERATING_FACILITY_ID=e.OPERATING_FACILITY_ID(+) and e.PACKAGE_CODE=p.PACKAGE_CODE(+) 
       AND a.PHYSICIAN_ID=m.PRACTITIONER_ID  group by grouping sets((),(m.PRACTITIONER_NAME))
      
''')

        self.cursor.execute(total_number_of_online_consultation_by_doctors_qurey,[facility_code,from_date,to_date])
        total_number_of_online_consultation_by_doctors_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return total_number_of_online_consultation_by_doctors_data


    def get_total_number_of_ip_patients_by_doctors(self,from_date,to_date):
        gettotal_number_of_ip_patients_by_doctors_query = ('''
        
        select nvl (c.PRACTITIONER_NAME, ' Grand Total :')  Doctor,Count(a.patient_id) Total_patient from pr_encounter a, mp_patient b,am_practitioner c,
        am_speciality e  where a.PATIENT_ID=b.PATIENT_ID and  a.SPECIALTY_CODE = e.SPECIALITY_CODE and a.PATIENT_CLASS = 'IP'
        and a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID and a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
        and a.cancel_reason_code is null and a.facility_id = 'KH' group by grouping sets((),(C.PRACTITIONER_NAME))



''')
        self.cursor.execute(gettotal_number_of_ip_patients_by_doctors_query,[from_date,to_date])
        gettotal_number_of_ip_patients_by_doctors_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return gettotal_number_of_ip_patients_by_doctors_data


    def get_total_number_of_op_patients_by_doctors(self,from_date,to_date):
        get_total_number_of_op_patients_by_doctors_query = ('''
        
        select  nvl (c.PRACTITIONER_NAME, ' Grand Total :') Doctor,Count(a.patient_id) Total_patient  from pr_encounter a, mp_patient b,am_practitioner c,am_speciality e
        where a.PATIENT_ID=b.PATIENT_ID and  a.SPECIALTY_CODE = e.SPECIALITY_CODE and a.PATIENT_CLASS in ('OP','EM')
        and a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID and A.VISIT_ADM_TYPE in ('RV','FV','SD','FU','FF')
        and a.ASSIGN_CARE_LOCN_CODE not in ('DIAG') and TRUNC(a.VISIT_ADM_DATE_TIME) between :from_date and :to_date
        and a.cancel_reason_code is null  group by grouping sets((),(C.PRACTITIONER_NAME))


''')
        self.cursor.execute(get_total_number_of_op_patients_by_doctors_query,[from_date,to_date])
        get_total_number_of_op_patients_by_doctors_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_total_number_of_op_patients_by_doctors_data


    
    def get_opd_changes_report(self,facility_code,from_date,to_date):
        opd_changes_report_qurey = (''' 
        
       select to_char(o.appt_slab_from_time,'HH24:MI:SS') from_time , to_char(o.appt_slab_to_time,'HH24:MI:SS')   to_time,o.appt_ref_no,
       o.clinic_code,o.practitioner_id,to_char(o.appt_date,'dd/mm/yyyy') new_Appt_date,to_char(o.appt_date,'dd/mm/yyyy') i_Appt_date,
       to_char(o.appt_date,'Day') appt_day1,o.APPT_TYPE_CODE visit_type_ind,a.PRACTITIONER_NAME,c.LONG_DESC clinic_name,o.patient_id,
       o.patient_name,o.res_tel_no,o.oth_contact_no
       from oa_appt o,am_practitioner a,op_clinic c where o.PRACTITIONER_ID =a.PRACTITIONER_ID(+) and o.CLINIC_CODE=c.CLINIC_CODE(+) 
       and o.appt_date between :from_date and :to_date and o.patient_id is null and oth_contact_no is null and res_TEL_No not like '__________'
       and appt_remarks is null and o.CONTACT_REASON_CODE <> 11 and o.clinic_code <> 'PRAD' and o.FACILITY_ID = :facility_code
      
''')

        self.cursor.execute(opd_changes_report_qurey,[from_date,to_date,facility_code])
        opd_changes_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return opd_changes_report_data



    def get_ehc_conversion_report(self,facility_code,from_date,to_date):
        ehc_conversion_report_qurey = (''' 
        
       select distinct pack.patient_id,pack.NAME_PREFIX,pack.FIRST_NAME,pack.SECOND_NAME,pack.FAMILY_NAME, pack.ADDED_DATE,pack.LONG_DESC,
       B.LONG_DESC Service_name,a.blng_serv_code,a.trx_date,T.PRACTITIONER_NAME,T.primary_speciality_code,a.serv_item_desc,A.ORG_GROSS_CHARGE_AMT
       from bl_patient_charges_folio a,bl_blng_serv b,am_practitioner t,(select E.patient_id,E.EPISODE_ID,M.NAME_PREFIX,M.FIRST_NAME,M.SECOND_NAME,
       M.FAMILY_NAME,H.ADDED_DATE,P.LONG_DESC from mp_patient M,pr_encounter E,bl_package_sub_hdr h,bl_package p,bl_package_encounter_dtls f
       where e.specialty_code ='EHC' and M.PATIENT_ID =E.PATIENT_ID and H.PACKAGE_CODE=P.PACKAGE_CODE and f.PACKAGE_SEQ_NO = h.PACKAGE_SEQ_NO
       and f.PACKAGE_CODE = h.PACKAGE_CODE and f.PATIENT_ID =h.PATIENT_ID and f.ENCOUNTER_ID = e.EPISODE_ID and h.status='C' and p.OPERATING_FACILITY_ID =:facility_code
    and h.added_date between :from_date and :to_date)pack where pack.patient_id=a.patient_id and NVL(trx_STATUS,'X')<>'C'
    and a.trx_date >pack.added_date and A.BLNG_SERV_CODE =B.BLNG_SERV_CODE(+) and A.PHYSICIAN_ID=T.PRACTITIONER_ID(+)
    and a.blng_Serv_code not in ('HSPK000001') and pack.added_date between :from_date and :to_date
''')

        self.cursor.execute(ehc_conversion_report_qurey,[facility_code,from_date,to_date,from_date,to_date])
        ehc_conversion_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return ehc_conversion_report_data



    def get_ehc_package_range_report(self,facility_code,from_date,to_date):
        ehc_package_range_report_qurey = (''' 
        
       select distinct  P.LONG_DESC, H.ADDED_DATE, E.patient_id, M.NAME_PREFIX, M.FIRST_NAME, M.SECOND_NAME, M.FAMILY_NAME, f.CUST_CODE, c.LONG_NAME ,h.PACKAGE_AMT
       from mp_patient M,pr_encounter E,bl_patient_charges_folio f,bl_package_sub_hdr h,bl_package p,ar_customer c
       where e.specialty_code ='EHC' and M.PATIENT_ID =E.PATIENT_ID and E.EPISODE_ID=F.EPISODE_ID and e.FACILITY_ID =:facility_code
       and p.ADDED_FACILITY_ID = 'KH' and F.PACKAGE_SEQ_NO=H.PACKAGE_SEQ_NO and H.PACKAGE_CODE=P.PACKAGE_CODE  and c.cust_code(+) = f.CUST_CODE and h.status='C'
       and h.added_date between :from_date and to_date(:to_date)+1 and p.OP_YN='Y' order by  H.ADDED_DATE 
''')

        self.cursor.execute(ehc_package_range_report_qurey,[facility_code,from_date,to_date])
        ehc_package_range_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return ehc_package_range_report_data



    def get_error_report(self,from_date,to_date):
        get_error_report_query = ('''
        
        SELECT a.patient_id,b.PATIENT_NAME,b.REGN_DATE,get_age(b.date_of_birth,SYSDATE) Age,b.SEX Gender,a.VISIT_ADM_DATE_TIME Admission_Date,
        A.ASSIGN_CARE_LOCN_CODE,A.ASSIGN_BED_CLASS_CODE,E.LONG_DESC,a.ASSIGN_BED_NUM Bed_Num,c.PRACTITIONER_NAME Treating_Doctor,d.LONG_DESC Speciality,
        A.ASSIGN_BED_CLASS_CODE, f.BLNG_GRP_ID,f.cust_code,f.remark,m.long_name,f.NON_INS_BLNG_GRP_ID,b.ALT_ID2_NO prno,f.TOT_UNADJ_DEP_AMT deposit,
        p.LONG_DESC postal_code FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f ,mp_country m,
        mp_pat_addresses k,mp_postal_code p WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID and a.patient_id=k.patient_id(+)
        and k.POSTAL2_CODE = p.POSTAL_CODE(+) and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id AND a.patient_class = 'IP'
        AND a.SPECIALTY_CODE = d.SPECIALITY_CODE and m.COUNTRY_CODE=b.NATIONALITY_CODE and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE
        and a.cancel_reason_code is null AND a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1 and a.ADDED_FACILITY_ID = 'KH' ORDER BY A.ASSIGN_CARE_LOCN_CODE


''')
        self.cursor.execute(get_error_report_query,[from_date,to_date])
        get_error_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_error_report_data


    def get_gipsa_report(self):

        gipsa_report_qurey = ('''
        
        
            select a.order_id,d.NURSING_DOC_COMP_TIME,b.order_catalog_code,b.catalog_desc, f.LONG_DESC,
            a.patient_id,c.patient_name, c.DATE_OF_BIRTH, c.SEX,g.PRACTITIONER_NAME,k.BLNG_GRP_ID,k.NON_INS_BLNG_GRP_ID,k.CUST_CODE,l.PACKAGE_SEQ_NO,  l.PACKAGE_CODE,n.LONG_DESC
            from or_order a , or_order_line b , mp_patient c , OT_POST_OPER_HDR d , OT_OPER_MAST e, OT_OPER_TYPE f, am_practitioner g,ip_open_encounter i,
            bl_episode_fin_dtls k,bl_package_sub_hdr l,bl_package_encounter_dtls m,bl_package n
            where a.order_id = d.order_id and b.order_id = d.order_id and b.order_catalog_code =e.ORDER_CATALOG_CODE and e.OPER_TYPE_CODE = f.OPER_TYPE
            and a.order_id = b.order_id and a.order_category = 'OT' and  b.order_line_status = 'CD' and a.patient_id = c.patient_id and c.PATIENT_ID = i.PATIENT_ID
            and d.surgeon_code = g.PRACTITIONER_ID(+) and i.ENCOUNTER_ID =d.ENCOUNTER_ID and k.ENCOUNTER_ID = i.ENCOUNTER_ID and k.PATIENT_ID = i.PATIENT_ID and
            i.PATIENT_ID=m.PATIENT_ID(+) and i.ENCOUNTER_ID=m.ENCOUNTER_ID(+) and l.PATIENT_ID(+)=m.PATIENT_ID and l.PACKAGE_SEQ_NO(+)=m.PACKAGE_SEQ_NO and
            l.PACKAGE_CODE=n.PACKAGE_CODE(+)

        ''')

        self.cursor.execute(gipsa_report_qurey)
        gipsa_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return gipsa_report_data
    


    def get_precision_patient_opd_and_online_consultation_list_report(self,from_date,to_date):
        get_precision_patient_opd_and_online_consultation_list_report_query = ('''
        
        select distinct m.patient_id,m.patient_NAME,a.SERV_ITEM_DESC,a.trx_date,m.CONTACT1_NO,m.CONTACT2_NO ,m.EMAIL_ID,
        g.addr1_line1 || ' ' || g.addr1_line2 || ' ' || g.addr1_line3 || ' ' || g.addr1_line4 Address
        from bl_patient_charges_folio a,bl_blng_serv b,mp_patient M,MP_PAT_ADDRESSES g
        where a.patient_id=m.patient_id and m.patient_id=g.patient_id and a.OPERATING_FACILITY_ID = 'KH'
        and NVL(trx_STATUS,'X')<>'C' and A.BLNG_SERV_CODE =B.BLNG_SERV_CODE(+) and a.blng_Serv_code = 'CNOP000047' and a.trx_date between :from_date and :to_date


''')
        self.cursor.execute(get_precision_patient_opd_and_online_consultation_list_report_query,[from_date,to_date])
        get_precision_patient_opd_and_online_consultation_list_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_precision_patient_opd_and_online_consultation_list_report_data



    def get_appointment_details_by_call_center_report(self,from_date,to_date):
        get_appointment_details_by_call_center_report_query = ('''
        
        select APPT_date,a.APPT_REF_NO,a.CLINIC_CODE,b.PRACTITIONER_NAME,a.APPT_SLAB_FROM_TIME,a.APPT_SLAB_TO_TIME,a.PATIENT_ID,a.PATIENT_NAME,a.RES_TEL_NO,
        a.OTH_CONTACT_NO,a.OVERBOOKED_YN,a.APPT_REMARKS,a.NO_OF_SLOTS,a.REASON_FOR_TRANSFER,a.FORCED_APPT_YN,a.TRANSFERRED_APPT_YN,a.ADDED_BY_ID,a.MODIFIED_BY_ID
        from OA_APPT a,AM_PRACTITIONER b,sm_appl_user c where a.PRACTITIONER_ID = b.PRACTITIONER_ID and a.ADDED_BY_ID = c.APPL_USER_ID and a.MODIFIED_BY_ID = c.APPL_USER_ID
        and to_date(APPT_DATE) between :from_date and :to_date and a.FACILITY_ID = 'KH' 


''')
        self.cursor.execute(get_appointment_details_by_call_center_report_query,[from_date,to_date])
        get_appointment_details_by_call_center_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_appointment_details_by_call_center_report_data



    def get_trf_report(self,from_date,to_date):
        get_trf_report_query = ('''
        
        select PATIENT_ID,PATIENT_NAME,GENDER,FROM_NURSING_UNIT_SHORT_DESC,FROM_BED_NO,PRACTITIONER_NAME,TFR_REQ_DATE_TIME,NURSING_UNIT_SHORT_DESC,TFR_REQ_STATUS_DESC from IP_TRANSFER_REQUEST_VW where TFR_REQ_TYPE ='RT' AND TFR_REQ_DATE_TIME between to_date(:from_date) and to_date(:to_date) ORDER BY TFR_REQ_DATE_TIME DESC


''')
        self.cursor.execute(get_trf_report_query,[from_date,to_date])
        get_trf_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_trf_report_data



    def get_current_inpatients_clinical_admin(self):

        current_inpatients_clinical_admin_qurey = ('''
        
        
            select a.PATIENT_ID, b.patient_name, a.ADMISSION_DATE_TIME Admission_Time, E.LONG_DESC,a.BED_NUM ,c.DIS_ADV_DATE_TIME DISCHARGE_REQUEST_TIME,c.EXPECTED_DISCHARGE_DATE ,n.LAST_AMENDED_DATE_TIME,
            n.AUTHORIZED_DATE_TIME,D.BILL_DOC_DATE,d.DISCHARGE_DATE_TIME Bed_Clear_Date_Time, D.BLNG_GRP_ID,b.ALT_ID2_NO AS PR_NO ,
            f.PRACTITIONER_NAME Treating_Doctor, g.LONG_DESC Speciality, c.ENCOUNTER_ID,c.added_by_id ,
            h.appl_user_name ,a.NURSING_UNIT_CODE,B.Contact2_no AS Patient_no,b.Contact3_no as Relative_No
            from ip_open_encounter a, mp_patient b, ip_discharge_advice c ,
            bl_episode_fin_dtls d, ip_bed_class e, am_practitioner f, am_speciality g, sm_appl_user h, ca_encntr_note n
             where a.PATIENT_ID = b.PATIENT_ID and 
            a.ENCOUNTER_ID = c.ENCOUNTER_ID and 
            a.ENCOUNTER_ID = d.EPISODE_ID and 
            n.PATIENT_ID = c.PATIENT_ID and 
            n.ENCOUNTER_ID = c.ENCOUNTER_ID and 
            A.BED_CLASS_CODE = E.BED_CLASS_CODE 
            and a.ATTEND_PRACTITIONER_ID = f.PRACTITIONER_ID 
            AND a.SPECIALTY_CODE = g.SPECIALITY_CODE 
            and a.FACILITY_ID = 'KH'
            and c.added_by_id = h.appl_user_id 
            order by BILL_DOC_DATE
        ''')

        self.cursor.execute(current_inpatients_clinical_admin_qurey)
        current_inpatients_clinical_admin = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return current_inpatients_clinical_admin


    def get_check_patient_registration_date(self,uhid):

        check_patient_registration_date_qurey = ('''
        
        Select PATIENT_ID, REGN_DATE,ADDED_DATE from MP_PATIENT where PATIENT_ID =:uhid


        ''')

        self.cursor.execute(check_patient_registration_date_qurey,[uhid])
        check_patient_registration_date = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return check_patient_registration_date

    


    def get_covid_pcr(self,facility_code,from_date,to_date):
        covid_pcr_qurey = (''' 
        
     SELECT  o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus,l.modified_date stat_change_date,CATALOG_DESC,A.PATIENT_ID,
Patient_Name as PatientName,map.SEX,trunc((sysdate - map.DATE_OF_BIRTH) / 365, 0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,b.remark 
     test_code,t.result_text result , map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,  
 F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,   
 g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state  FROM or_order o,OR_ORDER_LINE L, RL_REQUEST_HEADER A,RL_result_text t, pr_encounter e, 
bl_episode_fin_dtls b, mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g, MP_RES_TOWN h , MP_RES_AREA i, mp_region j 
WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMB000094' and a.PATIENT_ID = map.PATIENT_ID 
 and f.POSTAL1_CODE = g.POSTAL_CODE(+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+) 
 and i.REGION_CODE = j.REGION_CODE(+) AND A.PATIENT_ID = F.PATIENT_ID 
and t.SPECIMEN_NO(+) = a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+) = o.ORDER_STATUS 
and o.PATIENT_ID = b.PATIENT_ID and o.episode_id = b.episode_id 
and e.PATIENT_ID = o.PATIENT_ID and e.EPISODE_ID = o.EPISODE_ID and  o.ORDERING_FACILITY_ID=:facility_code AND o.ORD_DATE_TIME BETWEEN :from_date and :to_date
      
''')

        self.cursor.execute(covid_pcr_qurey,[facility_code,from_date,to_date])
        covid_pcr_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return covid_pcr_data


    def get_covid_2(self,from_date,to_date):
        covid_2_qurey = (''' 
        
                select o.patient_id,p.patient_name,o.PATIENT_CLASS,  o.ord_date_time,o.order_id,l.ORDER_LINE_NUM,
                c.LONG_DESC,s.long_desc orderstatus, l.modified_date stat_change_date,
                p.EMAIL_ID,p.CONTACT1_NO,p.CONTACT2_NO,p.CONTACT3_NO,p.CONTACT4_NO 
                 from or_order o, mp_patient p,or_order_status_code s, or_order_line l,or_order_catalog c where 
                o.PATIENT_ID = p.PATIENT_ID(+)and s.ORDER_STATUS_CODE(+) = o.ORDER_STATUS 
                 and o.ORDER_ID = l.ORDER_ID(+)and l.ORDER_CATALOG_CODE = c.ORDER_CATALOG_CODE(+)
                and L.ORDER_CATALOG_CODE in('LMMB000094', 'LMMC000227') AND o.ORD_DATE_TIME BETWEEN :from_date and :to_date
      
''')

        self.cursor.execute(covid_2_qurey,[from_date,to_date])
        covid_2_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return covid_2_data
    



    def get_covid_antibodies(self,facility_code,from_date,to_date):
        covid_antibodies_qurey = (''' 
        
    SELECT  o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus, l.modified_date stat_change_date, CATALOG_DESC, A.PATIENT_ID,
Patient_Name as PatientName,map.SEX,trunc((sysdate - map.DATE_OF_BIRTH) / 365, 0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code 
,max(t.NUMERIC_RESULT) Numeric,max(t.RESULT_COMMENT_DESC1) text ,map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO, 
 F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,
 g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state 
  FROM or_order o,OR_ORDER_LINE L, RL_REQUEST_HEADER A,RL_test_result t, pr_encounter e, 
bl_episode_fin_dtls b, mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g, MP_RES_TOWN h , MP_RES_AREA i, mp_region j 
WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMC00223' and a.PATIENT_ID = map.PATIENT_ID 
 and f.POSTAL1_CODE = g.POSTAL_CODE(+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+) 
 and i.REGION_CODE = j.REGION_CODE(+) AND A.PATIENT_ID = F.PATIENT_ID 
and t.SPECIMEN_NO(+) = a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+) = o.ORDER_STATUS 
and t.TEST_CODE in ('CUTOFFINDE', 'SARC1') and  o.ORDERING_FACILITY_ID=:facility_code
and o.PATIENT_ID = b.PATIENT_ID and o.episode_id = b.episode_id 
and e.PATIENT_ID = o.PATIENT_ID and e.EPISODE_ID = o.EPISODE_ID AND o.ORD_DATE_TIME BETWEEN :from_date and :to_daye 
group by o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc ,l.modified_date ,CATALOG_DESC,A.PATIENT_ID, 
Patient_Name ,map.SEX,trunc((sysdate - map.DATE_OF_BIRTH) / 365, 0) , o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code 
   ,map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,  
 F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4  , 
 g.LONG_DESC , h.LONG_DESC , i.LONG_DESC , j.LONG_DESC

''')

        self.cursor.execute(covid_antibodies_qurey,[facility_code,from_date,to_date])
        covid_antibodies_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return covid_antibodies_data



    def get_covid_antigen(self,facility_code,from_date,to_date):
        covid_antigen_qurey = (''' 
        
    SELECT   o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus,l.modified_date stat_change_date,CATALOG_DESC,A.PATIENT_ID,
    Patient_Name PatientName,map.SEX,trunc((sysdate - map.DATE_OF_BIRTH) / 365, 0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,
    t.RESULT_COMMENT_DESC1 text, map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO,F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,
    g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state   FROM 
    or_order o,OR_ORDER_LINE L, RL_REQUEST_HEADER A,RL_test_result t, pr_encounter e,
    bl_episode_fin_dtls b, mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g, MP_RES_TOWN h , MP_RES_AREA i, mp_region j
    WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMC000224' and a.PATIENT_ID = map.PATIENT_ID
    and f.POSTAL1_CODE = g.POSTAL_CODE(+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+)
    and i.REGION_CODE = j.REGION_CODE(+) AND A.PATIENT_ID = F.PATIENT_ID
    and t.SPECIMEN_NO(+) = a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+) = o.ORDER_STATUS
    and t.TEST_CODE in ('COVIDAG') and  o.ORDERING_FACILITY_ID=:facility_code
    and o.PATIENT_ID = b.PATIENT_ID and o.episode_id = b.episode_id
    and e.PATIENT_ID = o.PATIENT_ID and e.EPISODE_ID = o.EPISODE_ID AND o.ORD_DATE_TIME BETWEEN :from_date and :to_date

''')

        self.cursor.execute(covid_antigen_qurey,[facility_code,from_date,to_date])
        covid_antigen_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return covid_antigen_data


    def get_cbnaat_test_data(self,facility_code,from_date,to_date):
        cbnaat_test_data_qurey = (''' 
        
    SELECT  o.ord_date_time,SPEC_REGD_DATE_TIME,s.long_desc orderstatus,l.modified_date stat_change_date,CATALOG_DESC,A.PATIENT_ID, 
    Patient_Name as PatientName,map.SEX,trunc((sysdate-map.DATE_OF_BIRTH)/365,0) age, o.PATIENT_CLASS,b.BLNG_GRP_ID,b.cust_code,b.remark 
    test_code,t.result_text result,map.EMAIL_ID,map.CONTACT1_NO,map.CONTACT2_NO,map.CONTACT3_NO,map.CONTACT4_NO, 
    F.addr1_line1 || ' ' || F.addr1_line2 || ' ' || F.addr1_line3 || ' ' || F.addr1_line4 Address ,g.LONG_DESC postalcode, h.LONG_DESC area, i.LONG_DESC town, j.LONG_DESC state 
    FROM or_order o,OR_ORDER_LINE L,RL_REQUEST_HEADER A,RL_result_text t,pr_encounter e, 
    bl_episode_fin_dtls b ,mp_patient map,or_order_status_code s, MP_PAT_ADDRESSES F ,  MP_POSTAL_CODE g,  MP_RES_TOWN h , MP_RES_AREA i, mp_region j  
    WHERE o.ORDER_ID = A.ORDER_ID AND L.ORDER_CATALOG_CODE = 'LMMC000227' and a.PATIENT_ID = map.PATIENT_ID 
    and f.POSTAL1_CODE = g.POSTAL_CODE (+) and g.RES_TOWN_CODE = h.RES_TOWN_CODE(+) and h.RES_AREA_CODE = i.RES_AREA_CODE(+) 
    and i.REGION_CODE = j.REGION_CODE(+) AND  A.PATIENT_ID=F.PATIENT_ID and  o.PATIENT_ID=b.PATIENT_ID and o.episode_id = b.episode_id  
    and t.SPECIMEN_NO(+)=a.SPECIMEN_NO AND o.ORDER_ID = l.ORDER_ID and s.ORDER_STATUS_CODE(+)= o.ORDER_STATUS and o.ADDED_FACILITY_ID=:facility_code
    and e.PATIENT_ID =o.PATIENT_ID and e.EPISODE_ID=o.EPISODE_ID AND o.ORD_DATE_TIME BETWEEN :from_date and :to_date

''')

        self.cursor.execute(cbnaat_test_data_qurey,[facility_code,from_date,to_date])
        cbnaat_test_data_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return cbnaat_test_data_data


    def get_lab_tat_report(self,facility_code,from_date,to_date,dept_name):
        lab_tat_report_qurey = (''' 
        
    SELECT distinct a.PATIENT_ID UHID,a.specimen_no SpecNo,a.SPECIMEN_TYPE_CODE SpecType,a.SOURCE_CODE Locn,l.PRIORITY Priority,e.LONG_NAME Section, 
q.GROUP_TEST_CODE GrpTest,q.TEST_CODE TestCode,d.LONG_DESC TestName,q.INSTRUMENT_CODE MachineName,l.ORD_DATE_TIME OrdDateTime, 
a.SPEC_COLLTD_DATE_TIME CollDate,a.SPEC_REGD_DATE_TIME RegDate,a.VERIFIED_DATE AckDate,q.RELEASED_DATE FirstRelease, 
trunc(24*mod(q.RELEASED_DATE-a.SPEC_REGD_DATE_TIME,1)) || 'Hrs '||  
trunc( mod(mod(q.RELEASED_DATE-a.SPEC_REGD_DATE_TIME,1)*24,1)*60 ) || 'Mins ' || 
trunc(mod(mod(mod(q.RELEASED_DATE-a.SPEC_REGD_DATE_TIME,1)*24,1)*60,1)*60 ) || 'Secs ' FirstReleaseDiff, 
q.REVIEWED_DATE FinalRelease, trunc(24*mod(q.REVIEWED_DATE-a.SPEC_REGD_DATE_TIME,1)) || 'Hrs '||  
trunc( mod(mod(q.REVIEWED_DATE-a.SPEC_REGD_DATE_TIME,1)*24,1)*60 ) || 'Mins ' || 
trunc(mod(mod(mod(q.REVIEWED_DATE-a.SPEC_REGD_DATE_TIME,1)*24,1)*60,1)*60 ) || 'Secs ' FinalReleasediff 
,q.NORMAL_REVIEWED_BY Reviewdby,p.APPL_USER_NAME   
FROM OR_ORDER_LINE L,RL_REQUEST_HEADER A,or_order_catalog b, rl_test_code d,rl_test_result q,rl_section_code e,sm_APPL_USER p 
WHERE d.SECTION_CODE=e.SECTION_CODE and a.SPECIMEN_NO=q.SPECIMEN_NO and L.ORDER_ID(+) = A.ORDER_ID and l.ORDER_CATALOG_CODE=b.ORDER_CATALOG_CODE 
and  b.CONTR_MSR_PANEL_ID = d.TEST_CODE and L.ORDER_CATEGORY = 'LB' AND p.APPL_USER_ID(+)=q.NORMAL_REVIEWED_BY 
and l.ORD_DATE_TIME between :from_date and :to_date  and a.OPERATING_FACILITY_ID = :facility_code and e.LONG_NAME = :dept_name

''')

        self.cursor.execute(lab_tat_report_qurey,[from_date,to_date,facility_code,dept_name])
        lab_tat_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return lab_tat_report_data

    
    def get_histopath_fixation_data(self,year_input,from_date,to_date):
        histopath_fixation_data_qurey = (''' 
        
  SELECT A.SPECIMEN_NO as Specimen_No,a.CATEGORY_YEAR as Yr,a.CATEGORY_CODE as Cat_Code,a.CATEGORY_NUMBER as Cat_No,c.TEST_CODE as Test_Code, 
d.LONG_DESC as Test_Name,b.SPECIMEN_DESC as Specimen_Type,e.RESULT_COMMENT_DESC1 as Fixation_Time,a.SPEC_COLLTD_DATE_TIME as Collectn_Dt, 
a.SPEC_RECD_DATE_TIME as Reg_Dt,a.RELEASED_DATE as Release_Dt,a.RELEASED_BY_ID as Who_Released 
FROM RL_REQUEST_HEADER A, rl_specimen_type_code b, RL_REQUEST_detail c, rl_test_code d, rl_test_result e 
WHERE a.SPECIMEN_NO=c.SPECIMEN_NO and c.TEST_CODE=d.TEST_CODE and a.SPECIMEN_NO = e.SPECIMEN_NO and a.SPECIMEN_TYPE_CODE=b.SPECIMEN_TYPE_CODE 
and c.OPERATING_FACILITY_ID = 'KH' and A.RELEASED_DATE IS NOT NULL 
and CATEGORY_YEAR = :year_input and A.SPEC_COLLTD_DATE_TIME between :from_date and to_date(:to_date)+1
and e.RESULT_COMMENT_DESC1 IS NOT NULL ORDER BY A.SPEC_COLLTD_DATE_TIME 

''')

        self.cursor.execute(histopath_fixation_data_qurey,[year_input,from_date,to_date])
        histopath_fixation_data_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return histopath_fixation_data_data

    
    def get_slide_label_data(self):

        slide_label_data_qurey = ('''
        
        
                  select a.SPEC_REGD_DATE_TIME as REGDDATE,
                substr(a.CATEGORY_YEAR, -2) || a.CATEGORY_CODE || '-' || a.CATEGORY_NUMBER as CatNo,
                a.PATIENT_ID as PatID,
                b.PATIENT_NAME as PatientName,TO_CHAR(b.DATE_OF_BIRTH, 'YYYY-MM-DD') as DOB,b.SEX,
                substr(a.CATEGORY_YEAR, -2) || a.CATEGORY_CODE || '-' || a.CATEGORY_NUMBER || ';' || a.PATIENT_ID || ';' || b.SEX as BarcodedataSingleSection 
                 from rl_request_header a, mp_patient b where a.PATIENT_ID = b.PATIENT_ID and a.CATEGORY_YEAR >= '2020' and a.CATEGORY_CODE = 'H'
                order by a.SPEC_REGD_DATE_TIME desc
        ''')

        self.cursor.execute(slide_label_data_qurey)
        slide_label_data_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return slide_label_data_data


    def get_contract_effective_date_report(self,facility_code,from_date,to_date):
        contract_effective_date_report_qurey = (''' 
        
        select CUST_CODE,LONG_NAME,CUST_GROUP_CODE,IP_YN,OP_YN,VALID_TO,MODIFIED_FACILITY_ID from ar_customer where MODIFIED_FACILITY_ID =:facility_code and VALID_TO is not null  and ADDED_FACILITY_ID = :facility_code and VALID_TO between :from_date and :to_date order by VALID_TO DESC

''')

        self.cursor.execute(contract_effective_date_report_qurey,[facility_code,facility_code,from_date,to_date])
        contract_effective_date_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return contract_effective_date_report_data



    def get_admission_report(self,from_date,to_date):
        admission_report_qurey = (''' 
        
                             select a.PATIENT_ID,b.patient_name, m.long_name,b.email_id,b.contact1_no,b.contact2_no,b.contact3_no,b.email_id as EMAIL_ID2,
                            j.ADDR1_LINE1,j.ADDR1_LINE2,j.ADDR1_LINE3,j.ADDR1_LINE4 ,p1.long_desc City_Area, r1.long_desc district,
                            o1.long_desc State, q1.LONG_DESC postal_code, k.LONG_NAME COUNTRY, n.ADDR2_LINE1,n.ADDR2_LINE2,n.ADDR2_LINE3,n.ADDR2_LINE4,p.long_desc City_Area, r.long_desc district,
                             o.long_desc State, q.LONG_DESC postal_code, l.LONG_NAME as Country,sex,b.mar_status_code,a.VISIT_ADM_DATE_TIME Admission_date, a.DISCHARGE_DATE_TIME,c.PRACTITIONER_NAME Doctor, A.ADDED_BY_ID, 
                            a.ASSIGN_BED_CLASS_CODE,a.episode_id, b.REGN_DATE,get_age(b.date_of_birth, SYSDATE) Age,a.ASSIGN_BED_NUM Bed_Num, d.LONG_DESC Speciality 
                             from pr_encounter a,mp_patient b, am_practitioner c,bl_episode_fin_dtls f, mp_country m,mp_pat_addresses j, mp_country k,mp_country l, mp_pat_addresses n,am_speciality d, 
                             mp_region o, mp_res_town p, mp_postal_code q , mp_res_area r, mp_region o1, mp_res_town p1, mp_postal_code q1 , mp_res_area r1 
                            where a.PATIENT_ID = b.PATIENT_ID and a.PATIENT_ID = f.PATIENT_ID and A.episode_id = f.episode_id and m.COUNTRY_CODE = b.NATIONALITY_CODE 
                             AND a.SPECIALTY_CODE = d.SPECIALITY_CODE and j.PATIENT_ID = b.PATIENT_ID and n.PATIENT_ID = b.PATIENT_ID and j.COUNTRY1_CODE = k.COUNTRY_CODE(+) 
                             and n.COUNTRY2_CODE = l.COUNTRY_CODE(+)   and a.PATIENT_CLASS = 'IP' and a.ATTEND_PRACTITIONER_ID = c.PRACTITIONER_ID 
                            and n.res_town1_code = p.res_town_code(+) and n.res_area1_code = r.res_area_code(+) and n.region1_code = o.region_code(+) 
                            and n.postal1_code = q.POSTAL_CODE(+) and j.res_town1_code = p1.res_town_code(+) and j.res_area1_code = r1.res_area_code(+) and j.region1_code = o1.region_code(+)
                            and j.postal1_code = q1.POSTAL_CODE(+)
                            and trunc(a.VISIT_ADM_DATE_TIME) between :from_date and :to_date
                            and a.facility_id in ('AK', 'KH', 'DF', 'GO', 'RH', 'SL')
                            and a.cancel_reason_code is null  order by a.VISIT_ADM_DATE_TIME
                            
                             
      
''')

        self.cursor.execute(admission_report_qurey,[from_date,to_date])
        admission_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return admission_report_data
    


    def get_patient_discharge_report(self,from_date,to_date):
        patient_discharge_report_qurey = (''' 
        
select a.PATIENT_ID,b.patient_name, m.long_name,b.email_id,b.contact1_no,b.contact2_no,b.contact3_no,b.email_id as EMAIL_ID2, 
j.ADDR1_LINE1,j.ADDR1_LINE2,j.ADDR1_LINE3,j.ADDR1_LINE4 ,j.POSTAL1_CODE,k.LONG_NAME,n.ADDR2_LINE1,n.ADDR2_LINE2,n.ADDR2_LINE3,n.ADDR2_LINE4,n.POSTAL2_CODE, 
l.LONG_NAME as LONG_NAME4,sex,b.mar_status_code,a.VISIT_ADM_DATE_TIME Admission_date,a.DISCHARGE_DATE_TIME,c.PRACTITIONER_NAME Doctor,A.ADDED_BY_ID, 
a.ASSIGN_BED_CLASS_CODE,a.episode_id, b.REGN_DATE,get_age(b.date_of_birth,SYSDATE) Age,a.ASSIGN_BED_NUM Bed_Num,d.LONG_DESC Speciality  
from pr_encounter a, mp_patient b,am_practitioner c,bl_episode_fin_dtls f,mp_country m, 
mp_pat_addresses j,mp_country k,mp_country l,mp_pat_addresses n,am_speciality d 
where a.PATIENT_ID=b.PATIENT_ID and  a.PATIENT_ID=f.PATIENT_ID   
and A.episode_id = f.episode_id and m.COUNTRY_CODE=b.NATIONALITY_CODE  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE  
and j.PATIENT_ID = b.PATIENT_ID and n.PATIENT_ID = b.PATIENT_ID and j.COUNTRY1_CODE=k.COUNTRY_CODE(+) 
and n.COUNTRY2_CODE=l.COUNTRY_CODE(+) and a.PATIENT_CLASS = 'IP' and a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID  
and a.DISCHARGE_DATE_TIME between :from_date and to_date(:to_date)+1 and a.cancel_reason_code is null and a.facility_id in ('AK','KH','DF','GO','RH','SL')  order by a.DISCHARGE_DATE_TIME 
                            
                             
      
''')

        self.cursor.execute(patient_discharge_report_qurey,[from_date,to_date])
        patient_discharge_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return patient_discharge_report_data
    


    def get_credit_letter_report(self,from_date,to_date):
        credit_letter_report_qurey = (''' 
        
select a.PATIENT_ID, b.patient_name,G.LONG_NAME ,a.VISIT_ADM_DATE_TIME Admission_date, a.DISCHARGE_DATE_TIME,c.PRACTITIONER_NAME Doctor, a.REFERRAL_ID,e.LONG_DESC Department, F.BLNG_GRP_ID,F.CUST_CODE 
from pr_encounter a, mp_patient b,am_practitioner c,am_speciality e,bl_episode_fin_dtls f,ar_customer g 
where a.PATIENT_ID=b.PATIENT_ID and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id and  F.CUST_CODE = G.CUST_CODE 
and a.FACILITY_ID in ('AK','KH','DF','GO','RH','SL') and a.SPECIALTY_CODE = e.SPECIALITY_CODE and f.blng_grp_id = 'TPA'  
and  a.PATIENT_CLASS = 'IP' and a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID  and a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
and a.cancel_reason_code is null  order by a.VISIT_ADM_DATE_TIME 
                            
                             
      
''')

        self.cursor.execute(credit_letter_report_qurey,[from_date,to_date])
        credit_letter_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return credit_letter_report_data

    

    def get_corporate_ip_report(self,from_date,to_date):
        corporate_ip_report_qurey = (''' 
        
SELECT a.patient_id,b.PATIENT_NAME,a.VISIT_ADM_DATE_TIME Admission_Date,a.ASSIGN_BED_NUM Bed_Num,d.LONG_DESC Speciality,E.LONG_DESC,c.PRACTITIONER_NAME Treating_Doctor,f.BLNG_GRP_ID,f.cust_code,f.remark
FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f ,mp_country m 
WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID and  a.FACILITY_ID in ('AK','KH','DF','GO','RH','SL') 
and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE  
and m.COUNTRY_CODE=b.NATIONALITY_CODE and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null 
AND a.VISIT_ADM_DATE_TIME  between :from_date and to_date(:to_date)+1
order by a.VISIT_ADM_DATE_TIME
                            
                             
      
''')

        self.cursor.execute(corporate_ip_report_qurey,[from_date,to_date])
        corporate_ip_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return corporate_ip_report_data



    def get_opd_consultation_report(self,from_date,to_date):
        opd_consultation_report_qurey = (''' 
        
SELECT a.patient_id,b.patient_name,TO_CHAR (a.service_date, 'DD/MM/YY') serv_date,a.blng_serv_code serv_code,c.long_desc serv_desc,a.Serv_qty,a.upd_net_charge_amt,a.EPISODE_TYPE,a.service_date,physician_id
FROM bl_patient_charges_folio a,mp_patient b,bl_blng_serv c,bl_blng_serv_grp d,am_dept_lang_vw e WHERE a.operating_facility_id in ('AK','KH','DF','GO','RH','SL')
AND a.blng_serv_code = c.blng_serv_code AND a.patient_id = b.patient_id AND c.serv_grp_code = d.serv_grp_code
AND a.acct_dept_code = e.dept_code and NVL(A.BILLED_FLAG,'N') = decode(a.episode_type,'O','Y','E','Y','R','Y',NVL(A.BILLED_FLAG,'N'))
AND e.language_id = 'en' AND a.service_date >= TO_DATE (:from_date) AND a.service_date < TO_DATE (:to_date)+1
and A.UPD_NET_CHARGE_AMT !=0 and a.blng_serv_code like ('CNOP%')
                            
                             
      
''')

        self.cursor.execute(opd_consultation_report_qurey,[from_date,to_date])
        opd_consultation_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return opd_consultation_report_data

    


    def get_emergency_casualty_report(self,from_date,to_date):
        emergency_casualty_report_qurey = (''' 
        
select a.patient_id, b.patient_name,TO_CHAR(a.service_date, 'DD/MM/YY') serv_date,a.blng_serv_code serv_code, c.long_desc serv_desc, a.Serv_qty, a.upd_net_charge_amt,a.EPISODE_TYPE,a.service_date
FROM bl_patient_charges_folio a,mp_patient b,bl_blng_serv c,bl_blng_serv_grp d,am_dept_lang_vw e
WHERE a.operating_facility_id in ('AK','KH','DF','GO','RH','SL') AND a.blng_serv_code = c.blng_serv_code AND a.patient_id = b.patient_id
AND c.serv_grp_code = d.serv_grp_code AND a.acct_dept_code = e.dept_code
and NVL(A.BILLED_FLAG,'N') = decode(a.episode_type,'O','Y','E','Y','R','Y',NVL(A.BILLED_FLAG,'N'))
AND e.language_id = 'en' AND a.service_date between :from_date and to_date(:to_date)+1
and A.UPD_NET_CHARGE_AMT !=0 and a.blng_serv_code in ('OPGN000017')
                            
                             
      
''')

        self.cursor.execute(emergency_casualty_report_qurey,[from_date,to_date])
        emergency_casualty_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return emergency_casualty_report_data



    def get_new_registration_report(self,city_input,from_date,to_date):
        new_registration_report_qurey = (''' 
        
select b.patient_id,b.regn_date,b.patient_name,b.email_id,b.contact2_no,j.ADDR1_TYPE,j.addr1_line1 || ' ' || j.addr1_line2 || ' ' || j.addr1_line3 || ' ' || j.addr1_line4 Address, j.POSTAL1_CODE as Postal_Code ,
k.LONG_NAME as Country from mp_patient b,mp_pat_addresses j,mp_country k
where j.PATIENT_ID = b.PATIENT_ID and j.COUNTRY1_CODE=k.COUNTRY_CODE
and b.regn_date  between :from_date and to_date(:to_date)+1   
and b.ADDED_FACILITY_ID in ('AK','KH','DF','GO','RH','SL')
and (upper(addr1_line1) like '%'||:city_input||'%' or 
upper(addr1_line2) like '%'||:city_input||'%' or upper(addr1_line3) 
like '%'||:city_input||'%' or upper(addr1_line4) like '%'||:city_input||'%' )

''')

        self.cursor.execute(new_registration_report_qurey,[from_date,to_date,city_input])
        new_registration_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return new_registration_report_data


    def get_hospital_tariff_report(self,facility_code,from_date,to_date):
        hospital_tariff_report_qurey = (''' 
        
select a.blng_serv_code ,b.long_desc,c.long_desc SERVICE_GROUP,d.long_desc SERVICE_CLASSIFICATION ,a.CUST_PC_CODE, 
a.blng_class_code,b.PRT_GRP_HDR_CODE ,a.valid_from , a.valid_to , a.ip_rate , a.op_rate 
from bl_serv_cust_pc_price a, bl_blng_serv b,BL_BLNG_SERV_GRP c,BL_SERV_CLASSIFICATION d 
where a.BLNG_SERV_CODE = b.BLNG_SERV_CODE and valid_to is null and a.BLNG_CLASS_CODE not in ('ER','EX','LD') 
and b.SERV_GRP_CODE not in ('CO','PH','AI','AP','BL','BS','BW','CL','DR','DS','DY','GC','GL','GW','HV','IA', 
'IE','IJ','IM','IP','IS','IT','IU','IV','LA','LE','LG','LP','LS','LY','ME','NA','ND','NJ','NK','NL','NO','NS','NV', 
'NW','OB','OM','PE','PL','PN','RL','SB','SC','SL','ST','SV','SW','SY','VA','VB','VC','VL','XY') 
and CUST_PC_CODE = :facility_code AND a.valid_from between :from_date and to_date(:to_date)+1 
and b.serv_grp_code = c.serv_grp_code  and b.SERV_CLASSIFICATION_CODE = d.SERV_CLASSIFICATION_CODE and b.status is null order by CUST_PC_CODE

''')

        self.cursor.execute(hospital_tariff_report_qurey,[facility_code,from_date,to_date])
        hospital_tariff_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return hospital_tariff_report_data


    def get_international_patient_report(self,from_date,to_date):
        international_patient_report_qurey = (''' 
        
select a.PATIENT_ID,b.patient_name,m.long_name,b.DATE_OF_BIRTH,a.VISIT_ADM_DATE_TIME Admission_date,a.DISCHARGE_DATE_TIME,a.SPECIALTY_CODE,c.PRACTITIONER_NAME Doctor, A.ADDED_BY_ID,
b.CONTACT2_NO, b.EMAIL_ID,l.ADDR1_LINE1, l.ADDR1_LINE2,l.ADDR1_LINE3,l.ADDR1_LINE4
from pr_encounter a, mp_patient b,am_practitioner c,bl_episode_fin_dtls f,mp_country m, MP_PAT_ADDRESSES l
where a.PATIENT_ID=b.PATIENT_ID and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id and m.COUNTRY_CODE=b.NATIONALITY_CODE
and f.blng_grp_id = 'FOR1' and a.PATIENT_CLASS = 'OP' and a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID and b.PATIENT_ID = l.PATIENT_ID
and a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1 
and a.cancel_reason_code is null order by a.VISIT_ADM_DATE_TIME               
                             
      
''')

        self.cursor.execute(international_patient_report_qurey,[from_date,to_date])
        international_patient_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return international_patient_report_data


    def get_tpa_query(self,from_date,to_date):
        tpa_query_qurey = (''' 
        
SELECT a.patient_id,b.PATIENT_NAME,a.VISIT_ADM_DATE_TIME Admission_Date, E.LONG_DESC,
a.ASSIGN_BED_NUM Bed_Num,c.PRACTITIONER_NAME Treating_Doctor,d.LONG_DESC Speciality,f.BLNG_GRP_ID,f.cust_code,f.remark
 FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f,mp_country m
 WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID
 and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
 AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE
 and m.COUNTRY_CODE=b.NATIONALITY_CODE
 and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null
 AND  a.VISIT_ADM_DATE_TIME BETWEEN :from_date and to_date(:to_date)+1
order by a.VISIT_ADM_DATE_TIME        
                             
      
''')

        self.cursor.execute(tpa_query_qurey,[from_date,to_date])
        tpa_query_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return tpa_query_data


    def get_new_admission_report(self,from_date,to_date):
        new_admission_report_qurey = (''' 
        
select a.PATIENT_ID,b.patient_name,a.VISIT_ADM_DATE_TIME Admission_date,a.DISCHARGE_DATE_TIME,a.REFERRAL_ID,  c.PRACTITIONER_NAME Doctor,e.LONG_DESC Department,F.BLNG_GRP_ID,F.CUST_CODE,G.LONG_NAME  from pr_encounter a, mp_patient b,am_practitioner c,am_speciality e,bl_episode_fin_dtls f,ar_customer g  where a.PATIENT_ID=b.PATIENT_ID and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id and  F.CUST_CODE = G.CUST_CODE and a.SPECIALTY_CODE = e.SPECIALITY_CODE and f.blng_grp_id = 'TPA' and  a.PATIENT_CLASS = 'IP' and a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID
AND  a.VISIT_ADM_DATE_TIME BETWEEN :from_date and to_date(:to_date)+1 
and a.cancel_reason_code is null  order by a.VISIT_ADM_DATE_TIME 
                             
      
''')

        self.cursor.execute(new_admission_report_qurey,[from_date,to_date])
        new_admission_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return new_admission_report_data



    

    def get_discharge_billing_report(self,from_date,to_date):
        discharge_billing_report_qurey = (''' 
        
select a.FACILITY_ID,a.patient_id,a.encounter_id,initcap(short_name),alternate_id3_num,dis_adv_date_time,
a.added_by_id,c.appl_user_name from ip_discharge_advice a,mp_patient_mast b,sm_appl_user_vw c 
where a.dis_adv_status='0' and a.patient_id = b.patient_id and a.added_by_id = c.appl_user_id 
and c.language_id='en' and a.FACILITY_ID  ='KH' and a.DIS_ADV_DATE_TIME between :from_date and :to_date
order by dis_adv_date_time
                             
      
''')

        self.cursor.execute(discharge_billing_report_qurey,[from_date,to_date])
        discharge_billing_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return discharge_billing_report_data

    



    def get_discharge_billing_report_without_date_range(self):

        discharge_billing_report_without_date_range_query = ('''
        
        
            select a.FACILITY_ID,a.patient_id,a.encounter_id,initcap(short_name),alternate_id3_num,dis_adv_date_time,a.added_by_id,c.appl_user_name from ip_discharge_advice a,mp_patient_mast b,sm_appl_user_vw c where a.dis_adv_status='0' and a.patient_id = b.patient_id and a.added_by_id = c.appl_user_id and c.language_id='en' and a.FACILITY_ID  ='KH' and trunc(a.DIS_ADV_DATE_TIME) = trunc(sysdate) order by dis_adv_date_time
        
        ''')

        self.cursor.execute(discharge_billing_report_without_date_range_query)
        discharge_billing_report_without_date_range_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return discharge_billing_report_without_date_range_data




    def get_discharge_billing_user(self):

        discharge_billing_user_query = ('''
        
        
           select a.PATIENT_ID,a.ENCOUNTER_ID,initcap(short_name),DIS_ADV_DATE_TIME,a.ADDED_BY_ID ,c.APPL_USER_NAME
           from ip_discharge_advice a,mp_patient_mast b, sm_appl_user_vw c   where A.DIS_ADV_STATUS='0'
           and a.patient_id = b.patient_id and a.added_by_id = c.APPL_USER_ID and c.language_id ='en'
           order by DIS_ADV_DATE_TIME  
            

        ''')

        self.cursor.execute(discharge_billing_user_query)
        discharge_billing_user_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return discharge_billing_user_data




    def get_discount_report(self,from_date,to_date):
        discount_report_qurey = (''' 
        
                                SELECT distinct b.patient_name,a.PATIENT_ID,a.episode_id,a.PATIENT_CLASS,d.DOC_TYPE_CODE,
                                d.DOC_NUM Bill_Num, c.PRACTITIONER_NAME Doctor, round(d.BILL_HOSP_TOT_AMT) as Totalbill,
                                round(d.serv_disc_amt) servicediscount,round(D.MAN_DISC_AMT),round(d.OVERALL_DISC_AMT) 
                                  as overall_discount,round(d.DEPOSIT_ADJ_AMT) advance, round(d.BILL_AMT),round(d.BILL_TOT_OUTST_AMT) as TPA_DUE_Amount,
                                round(d.bill_paid_amt) CASH_CC, round(d.TOT_REFUND_AMT)Refund, d.modified_by_id as 
                                 Prepared_by,D.DOC_TYPE_CODE,D.DOC_NUM,d.doc_date,d.BLNG_GRP_ID,d.CUST_CODE,
                                d.REASON_CODE,e.DISC_REASON_CODE,d.BILL_DISC_DATE,d.BILL_DISC_BY_ID,d.BILL_DISC_AUTH_BY_ID,f.REMARK 
                                  FROM pr_encounter a, mp_patient b,am_practitioner c, bl_bill_hdr d,
                                 bl_patient_charges_folio e, bl_episode_fin_dtls f 
                                   WHERE a.PATIENT_ID = b.PATIENT_ID AND a.patient_id = d.patient_id AND 
                                a.Episode_id = d.EPISODE_ID AND a.ATTEND_PRACTITIONER_ID = c.PRACTITIONER_ID and
                                 f.EPISODE_ID = d.EPISODE_ID and f.PATIENT_ID = d.PATIENT_ID 
                                 and d.DOC_NUM = e.BILL_DOC_NUM(+)
                                 and d.DOC_TYPE_CODE = e.BILL_DOC_TYPE_CODE(+)
                                 AND E.DISC_REASON_CODE IS NOT NULL
                                 AND D.SERV_DISC_AMT > 0
                                 and d.bill_status IS NULL
                                 and D.DOC_DATE between :from_date and to_date(:to_date) + 1
                                union 
                                SELECT b.patient_name,a.PATIENT_ID,a.episode_id,a.PATIENT_CLASS,d.DOC_TYPE_CODE,d.DOC_NUM Bill_Num, 
                                c.PRACTITIONER_NAME Doctor, round(d.BILL_HOSP_TOT_AMT) Total_bill,
                                round(d.serv_disc_amt) servicediscount,round( D.MAN_DISC_AMT),round(d.OVERALL_DISC_AMT)
                                 overall_discount,round(d.DEPOSIT_ADJ_AMT) advance, round(d.BILL_AMT),round(d.BILL_TOT_OUTST_AMT)
                                 TPA_DUE_Amount,round(d.bill_paid_amt) CASH_CC, round(d.TOT_REFUND_AMT) Refund, d.modified_by_id
                                as Prepared_by,D.DOC_TYPE_CODE,D.DOC_NUM,d.doc_date,d.BLNG_GRP_ID,d.CUST_CODE,
                                d.REASON_CODE,null,d.BILL_DISC_DATE,d.BILL_DISC_BY_ID,d.BILL_DISC_AUTH_BY_ID,f.REMARK 
                                 FROM pr_encounter a, mp_patient b,am_practitioner c, bl_bill_hdr d,bl_episode_fin_dtls f 
                                 WHERE a.PATIENT_ID = b.PATIENT_ID AND a.patient_id = d.patient_id AND 
                                 f.EPISODE_ID = d.EPISODE_ID and f.PATIENT_ID = d.PATIENT_ID and 
                                 a.Episode_id = d.EPISODE_ID AND a.ATTEND_PRACTITIONER_ID = c.PRACTITIONER_ID 
                                 and d.bill_status IS NULL
                                 and D.DOC_DATE between :from_date and to_date(:to_date) + 1
                                 
                                   ''')

        self.cursor.execute(discount_report_qurey,[from_date,to_date])
        discount_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return discount_report_data


    def get_refund_report(self,from_date,to_date):
        refund_report_qurey = (''' 
        
                select a.patient_id,c.patient_name,B.SLMT_TYPE_CODE,E.LONG_DESC,round(A.DOC_AMT) as DOC_AMT,A.DOC_DATE,A.DOC_TYPE_CODE,
                A.DOC_NUMBER,A.BILL_DOC_TYPE_CODE,A.BILL_DOC_NUMBER,A.NARRATION,
                b.MODIFIED_BY_ID,a.CANCELLED_IND
                from bl_receipt_refund_hdr a, bl_receipt_refund_dtl b,mp_patient c, mp_pat_addresses d,BL_SLMT_TYPE E
                where A.PATIENT_ID = B.PATIENT_ID
                and A.PATIENT_ID = c.patient_id and a.patient_id = d.patient_id
                and B.SLMT_TYPE_CODE in ('SD', 'ED', 'CH', 'DN', 'BC', 'BF', 'CA', 'CF', 'T1', 'T2') and A.BILL_DOC_NUMBER is not null
                and A.DOC_AMT <= -1
                and b.SLMT_TYPE_CODE = E.SLMT_TYPE_CODE
                and A.DOC_TYPE_CODE = B.DOC_TYPE_CODE and A.DOC_NUMBER = B.DOC_NUMBER
                and A.DOC_DATE between :from_date and to_date(:to_date)+1 
                                 
                                   ''')

        self.cursor.execute(refund_report_qurey,[from_date,to_date])
        refund_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return refund_report_data


    def get_refund_report(self,from_date,to_date):
        refund_report_qurey = (''' 
        
                select a.patient_id,c.patient_name,B.SLMT_TYPE_CODE,E.LONG_DESC,round(A.DOC_AMT) as DOC_AMT,A.DOC_DATE,A.DOC_TYPE_CODE,
                A.DOC_NUMBER,A.BILL_DOC_TYPE_CODE,A.BILL_DOC_NUMBER,A.NARRATION,
                b.MODIFIED_BY_ID,a.CANCELLED_IND
                from bl_receipt_refund_hdr a, bl_receipt_refund_dtl b,mp_patient c, mp_pat_addresses d,BL_SLMT_TYPE E
                where A.PATIENT_ID = B.PATIENT_ID
                and A.PATIENT_ID = c.patient_id and a.patient_id = d.patient_id
                and B.SLMT_TYPE_CODE in ('SD', 'ED', 'CH', 'DN', 'BC', 'BF', 'CA', 'CF', 'T1', 'T2') and A.BILL_DOC_NUMBER is not null
                and A.DOC_AMT <= -1
                and b.SLMT_TYPE_CODE = E.SLMT_TYPE_CODE
                and A.DOC_TYPE_CODE = B.DOC_TYPE_CODE and A.DOC_NUMBER = B.DOC_NUMBER
                and A.DOC_DATE between :from_date and to_date(:to_date)+1 
                                 
                                   ''')

        self.cursor.execute(refund_report_qurey,[from_date,to_date])
        refund_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return refund_report_data
    


    def get_ehc_operation_report(self,facility_code,from_date,to_date):
        ehc_operation_report_qurey = (''' 
        
select distinct pack.patient_id,pack.NAME_PREFIX,pack.FIRST_NAME,pack.SECOND_NAME,pack.FAMILY_NAME,
TO_CHAR (pack.ADDED_DATE,'DD-Mon-YYYY'),pack.LONG_DESC,B.LONG_DESC Service_name,a.blng_serv_code, 
a.trx_date,T.PRACTITIONER_NAME,T.primary_speciality_code,a.serv_item_desc,A.ORG_GROSS_CHARGE_AMT from bl_patient_charges_folio a,bl_blng_serv b,am_practitioner t, 
(select E.patient_id,E.EPISODE_ID,M.NAME_PREFIX,M.FIRST_NAME,M.SECOND_NAME,M.FAMILY_NAME,H.ADDED_DATE,P.LONG_DESC  from  
mp_patient M,pr_encounter E,bl_package_sub_hdr h,bl_package p,bl_package_encounter_dtls f  
where e.specialty_code ='EHC' 
and M.PATIENT_ID =E.PATIENT_ID and E.ADDED_FACILITY_ID=:facility_code and H.PACKAGE_CODE=P.PACKAGE_CODE and f.PACKAGE_SEQ_NO = h.PACKAGE_SEQ_NO and f.PACKAGE_CODE = h.PACKAGE_CODE 
and f.PATIENT_ID =h.PATIENT_ID and f.ENCOUNTER_ID = e.EPISODE_ID  
and h.status='C' and p.OPERATING_FACILITY_ID ='KH' and h.added_date between :from_date and :to_date )pack 
where pack.patient_id=a.patient_id and NVL(trx_STATUS,'X')<>'C'and a.trx_date >pack.added_date and A.BLNG_SERV_CODE =B.BLNG_SERV_CODE(+) 
and A.PHYSICIAN_ID=T.PRACTITIONER_ID(+) 
and a.blng_Serv_code not in ('HSPK000001') and  a.OPERATING_FACILITY_ID=:facility_code 
and pack.added_date between :from_date and :to_date 


''')

        self.cursor.execute(ehc_operation_report_qurey,[facility_code,from_date,to_date])
        ehc_operation_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return ehc_operation_report_data



    def get_ehc_operation_report_2(self,facility_code,from_date,to_date):
        ehc_operation_report_2_qurey = (''' 
        
 select distinct  P.LONG_DESC, H.ADDED_DATE, E.patient_id, M.NAME_PREFIX, M.FIRST_NAME, M.SECOND_NAME, 
 M.FAMILY_NAME, f.CUST_CODE, c.LONG_NAME ,f.BILL_DOC_DATE 
 from mp_patient M,pr_encounter E,bl_patient_charges_folio f,bl_package_sub_hdr h,bl_package p,ar_customer c  
 where e.specialty_code ='EHC' and M.PATIENT_ID =E.PATIENT_ID and E.EPISODE_ID=F.EPISODE_ID and e.FACILITY_ID =:facility_code 
 and p.ADDED_FACILITY_ID = :facility_code and F.PACKAGE_SEQ_NO=H.PACKAGE_SEQ_NO and H.PACKAGE_CODE=P.PACKAGE_CODE and c.cust_code(+) = f.CUST_CODE 
  and h.status='C' and h.added_date between :from_date and to_date(:to_date)+1  and p.OP_YN='Y' order by  H.ADDED_DATE

''')

        self.cursor.execute(ehc_operation_report_2_qurey,[facility_code,facility_code,from_date,to_date])
        ehc_operation_report_2_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return ehc_operation_report_2_data




    def get_oncology_drugs_report(self,facility_code,from_date,to_date):
        oncology_drugs_report_qurey = (''' 
        
SELECT distinct d.long_desc,a.ADDED_DATE,a.ADDED_FACILITY_ID,a.DOC_NO,a.DOC_SRL_NO,a.DOC_TYPE_CODE, 
a.ITEM_CODE,c.long_desc,(a.SAL_ITEM_QTY-a.RET_ITEM_QTY) SAL_ITEM_QTY,b.encounter_id,b.patient_id,e.PATIENT_NAME, a.ADDED_AT_WS_NO,a.ADDED_BY_ID 
FROM ST_SAL_DTL_EXP  a ,ST_SAL_HDR b , mm_item c,MM_STORE d, mp_patient e 
where (a.doc_no = b.doc_no) and (a.item_code = c.item_code) and (a.store_code = d.store_code) and (a.SAL_ITEM_QTY-a.RET_ITEM_QTY) > 0  
and  a.added_facility_id = :facility_code AND b.ADDED_FACILITY_ID = :facility_code and  b.PATIENT_ID=e.PATIENT_ID and 
a.item_code in ('2000045213','2000045761','2000043187','2000048184','2000049844','2000047877','2000047579','2000051797', 
 '2000038532','2000043071','2000058396','2000024382','2000051697','2000047878','2000023973','2000058197','2000019952','2000053939', 
'2000055419','2000051706','2000029792','2000052924','2000059375','2000017355','2000023833','2000024381','2000056129','2000023975', 
'2000038531','2000052744','2000060598','2000059374','2000019945','2000052743','2000058729','2000051550','2000059506','2000018369','2000047003')  
and a.ADDED_DATE between  :from_date and to_date(:to_date)+1 order by a.added_date


''')

        self.cursor.execute(oncology_drugs_report_qurey,[facility_code,facility_code,from_date,to_date])
        oncology_drugs_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return oncology_drugs_report_data




    def get_radiology_tat_report(self,from_date,to_date):
        get_radiology_tat_report_query = ('''
        
select distinct TO_CHAR (r.EXAM_DATE_TIME , 'DD/MM/YY') ser_date,TO_CHAR (r.EXAM_DATE_TIME, 'HH24:MI:SS') ser_time, 
         r.EXAM_CODE serv_code, c.long_desc serv_desc,l.ORDER_QTY,
         DECODE (o.patient_class ,'IP', 'IP','OP', 'OP','EM', 'Emergency','R', 'Referral','D', 'Daycare') pat_Type,
         r.patient_id pat_id, b.short_name pat_name, o.patient_class,o.ord_date_time,r.START_TIME,r.END_TIME
from or_order o,rd_exam_view_requested r,mp_patient_mast b,         bl_blng_serv c,or_order_line l
where r.order_id=o.order_id and o.ORDER_TYPE_CODE in (select order_type_code from rd_section)
--and o.ord_date_time between '1-Aug-2015' and '07-Aug-2015' 
and r.END_TIME is NOT NULL
and o.ORDERING_FACILITY_ID = 'KH'
and r.ORDER_ID =l.ORDER_ID
and r.ORDER_LINE_NO = l.ORDER_LINE_NUM
     AND r.patient_id = b.patient_id
     AND r.EXAM_CODE = c.blng_serv_code
     and NVL(o.BILL_YN,'N') = decode(o.PATIENT_CLASS ,'OP','Y','EM','Y','R','Y',NVL(o.BILL_YN,'N'))
     AND r.EXAM_DATE_TIME between :from_date and :to_date
 

''')
        self.cursor.execute(get_radiology_tat_report_query,[from_date,to_date])
        get_radiology_tat_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_radiology_tat_report_data


    def get_ot_scheduling_list_report(self):
        get_ot_scheduling_list_report_query = ('''
        
select a.patient_id,b.patient_name,get_age(b.date_of_birth,SYSDATE) Age,b.sex,C.ORDER_ID,C.ORDER_CATALOG_CODE,C.CATALOG_DESC, 
a.pref_surg_date, D.PRACTITIONER_NAME,E.LONG_DESC,a.added_date,dbms_lob.substr(f.ORDER_COMMENT,5000,1) 
from ot_pending_order a,mp_patient b, or_order_line c,AM_PRACTITIONER d,AM_SPECIALITY e,or_order_comment f  
where a.patient_id = b.patient_id and a.order_id = c.order_id and A.PHYSICIAN_ID = D.PRACTITIONER_ID and a.order_id = f.order_id(+) 
and D.PRIMARY_SPECIALITY_CODE = E.SPECIALITY_CODE and PREF_SURG_DATE = to_date(sysdate)+1

''')
        self.cursor.execute(get_ot_scheduling_list_report_query)
        get_ot_scheduling_list_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_ot_scheduling_list_report_data



    def get_non_package_covid_patient_report(self):
        non_package_covid_patient_report_query = ('''
        
select distinct E.patient_id,E.ENCOUNTER_ID ,M.NAME_PREFIX,M.FIRST_NAME,M.SECOND_NAME,M.FAMILY_NAME,E.NURSING_UNIT_CODE,E.BED_TYPE_CODE,E.ADMISSION_DATE_TIME,E.BED_CLASS_CODE,
E.BED_NUM from mp_patient M, ip_open_encounter E,IP_aDT_trn I where M.PATIENT_ID = E.PATIENT_ID AND I.ENCOUNTER_ID = E.ENCOUNTER_ID(+) AND I.PATIENT_ID = E.PATIENT_ID(+)
and(I.TO_BED_NO in ('5018', '5018A', '5019', '5019A', '5020', '5020A', '5021', '5021A', '5022', '5022A', '5023', '5023A', '5024', '5024A',
'13001', '13001A', '13002', '13002A', '13002B', '13002C', '13002D', '13002E', '13002F', '13003', '13003A', '13004', '13004A', '13005', '13005A', '13006', '13006A', '13007', '13007A',
'13008', '13008A', '13009', '13009A', '13010', '13010A', '13011', '13011A', '13012', '13012A', '13013', '13013A', '13014', '13014A', '13015', '13015A', '13016', '13016A', '13083', '13083A', '13084',
'13084A', '13085', '13085A', '13086', '13086A', '13087', '13087A', '13088', '13088A', '13089', '13089A', '13090', '13090A', '13091', '13091A', '13092', '13092A', '13093', '13093A', '13094', '13094A',
'13095', '13095A', '13096', '13096A', '13097', '13097A', '13098', '13098A', '13098B', '13098C', '13098D', '13098E', '13098F')
or I.FR_BED_NO in (
'13001', '13001A', '13002', '13002A', '13002B',
'13002C', '13002D', '13002E', '13002F', '13003', '13003A', '13004', '13004A', '13005', '13005A', '13006', '13006A', '13007', '13007A', '13008', '13008A', '13009', '13009A', '13010', '13010A', '13011',
'13011A', '13012', '13012A', '13013', '13013A', '13014', '13014A', '13015', '13015A', '13016', '13016A', '13083', '13083A', '13084', '13084A', '13085', '13085A', '13086', '13086A', '13087',
'13087A', '13088', '13088A', '13089', '13089A', '13090', '13090A', '13091', '13091A', '13092', '13092A', '13093', '13093A', '13094', '13094A', '13095', '13095A', '13096', '13096A', '13097', '13097A', 
'13098', '13098A', '13098B', '13098C', '13098D', '13098E', '13098F', '5018', '5018A', '5019', '5019A', '5020', '5020A', '5021', '5021A', '5022', '5022A', '5023', '5023A', '5024', '5024A')) and e.ADMISSION_DATE_TIME >= '19-Apr-2021' minus 
select distinct E.patient_id,E.ENCOUNTER_ID ,c.NAME_PREFIX,c.FIRST_NAME,c.SECOND_NAME,c.FAMILY_NAME,E.NURSING_UNIT_CODE,E.BED_TYPE_CODE,E.ADMISSION_DATE_TIME,E.BED_CLASS_CODE, 
E.BED_NUM from BL_PACKAGE_SUB_HDR d, bl_package b,mp_patient c, ip_open_encounter E,bl_package_encounter_dtls f, IP_aDT_trn I where d.PACKAGE_CODE = B.PACKAGE_CODE 
and c.PATIENT_ID = e.PATIENT_ID and f.PACKAGE_SEQ_NO = d.PACKAGE_SEQ_NO and f.PACKAGE_CODE = d.PACKAGE_CODE AND I.ENCOUNTER_ID = E.ENCOUNTER_ID AND I.PATIENT_ID = E.PATIENT_ID 
and f.PATIENT_ID = d.PATIENT_ID and f.ENCOUNTER_ID = e.ENCOUNTER_ID and d.PATIENT_ID = C.PATIENT_ID and b.PACKAGE_CODE = 'COVID19' and e.FACILITY_ID = 'KH' 
and e.ADMISSION_DATE_TIME >= '19-Apr-2021'

''')
        self.cursor.execute(non_package_covid_patient_report_query)
        non_package_covid_patient_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return non_package_covid_patient_report_data


    def get_patient_registration_report(self,from_date,to_date):
        get_patient_registration_report_query = ('''
        
SELECT b.NAME_PREFIX,b.FIRST_NAME,b.FAMILY_NAME,b.SEX Gender,b.PAT_CAT_CODE, get_age(b.date_of_birth,SYSDATE) Age ,b.date_of_birth, 
m.LONG_DESC nationality, k.ADDR1_LINE1,k.ADDR1_LINE2,k.ADDR1_LINE3,k.ADDR1_LINE4 ,p.LONG_DESC postal_code, m.long_name country, 
b.email_id,b.CONTACT2_NO,r.CONTACT1_Name,r.CONTACT1_RELATION,r.CONTACT1_MOB_TEL_NO,b.ADDED_BY_ID,C.aPPL_USER_NAME ADDED_BY_NAME, 
b.patient_id,b.PATIENT_NAME,b.REGN_DATE 
FROM mp_patient b, mp_country m,mp_pat_addresses k, mp_postal_code p,mp_pat_rel_contacts r, SM_aPPL_USER C 
WHERE b.patient_id = k.patient_id(+) 
and b.ADDED_BY_ID = c.APPL_USER_ID(+) 
and k.POSTAL2_CODE = p.POSTAL_CODE(+) 
and m.COUNTRY_CODE = b.NATIONALITY_CODE 
and b.patient_id = r.patient_id(+) 
and nvl(r.CONTACT1_ROLE,'NEXT')= 'NEXT' 
and b.REGN_DATE between :from_date and to_date(:to_date)+1


''')
        self.cursor.execute(get_patient_registration_report_query,[from_date,to_date])
        get_patient_registration_report_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
                 
        return get_patient_registration_report_data











if __name__ == "__main__":
    a = NewDB_Ora()
    #b = a.get_tpa_letter('KH','05-Apr-2022','05-Apr-2022')
    b = a.get_contract_report('KH')
    
    print(b)

    for x in b:
        print(x)