import cx_Oracle as oracle

# from oracle_config import *

ip = "172.20.200.16"

host = "khdb-scan.kdahit.com"

port = 1521

service_name = "newdb.kdahit.com"

instance_name = "NEWDB"

# ora_db = oracle.connect("appluser","appluser",dsn_tns)

# cursor = ora_db.cursor()


# host = 'khdb-scan'

# port = 1521

# service_name = "newdb.kdahit.com"

# instance_name = "NEWDB"

# dsn_tns = oracle.makedsn(ip,port,instance_name)

# ora_db = oracle.connect("ibaehis","ib123",dsn_tns)

# cursor = ora_db.cursor()


#   'oracle': {
#     'ENGINE': 'django.db.backends.oracle',
#     'NAME': 'NEWDB:1521/newdb.kdahit.com',
#     'NAME': ('(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=khdb-scan)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=newdb.kdahit.com)))'),
#     'USER': 'ibaehis',
#     'PASSWORD': 'ib123',


class Ora:
    def __init__(self):
        self.dsn_tns = oracle.makedsn(host, port, service_name=service_name)
        self.ora_db = oracle.connect("ibaehis", "ib123", self.dsn_tns)
        self.cursor = self.ora_db.cursor()

    def status_update(self):

        if self.ora_db:
            return "You have connected to the Database"

        else:
            return "Unable to connect to the database! Please contact the IT Department"

    # def __del__(self):
    # self.cursor.close()
    # self.ora_db.close()

    def check_users(self, pr_num, passw):

        sql_qurey = """
        

        SELECT a.APPL_USER_ID, a.APPL_USER_NAME Username,app_password.decrypt(a.APPL_USER_PASSWORD) Password  FROM sm_appl_user a   
        where  a.APPL_USER_ID= :user_id
        and  app_password.decrypt(a.APPL_USER_PASSWORD)=  :user_pass

        
        """

        self.cursor.execute(sql_qurey, [pr_num, passw])
        user_pass = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return user_pass

    def get_package_with_price(self, facility_code):
        package_with_price_qurey = f""" 
        
        Select A.OPERATING_FACILITY_ID,A.PACKAGE_CODE,A.SHORT_DESC,A.LONG_DESC,A.EFF_FROM_DATE,A.EFF_TO_DATE,
        A.OP_YN,A.EM_YN,A.IP_YN,A.DC_YN,B.BLNG_CLASS_CODE,A.PKG_VALID_DAYS,
        B.FACTOR_RATE
        from 
        BL_PACKAGE A,
        BL_PACKAGE_BASE_PRICE B
        WHERE A.OPERATING_FACILITY_ID in ({facility_code})
        AND A.PACKAGE_CODE=B.PACKAGE_CODE

      
"""

        self.cursor.execute(package_with_price_qurey)
        data = self.cursor.fetchall()

        column_name = [i[0] for i in self.cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_discharge_census_revised(self, from_date, to_date):

        discharge_census_revised_qurey = """
            
            
        SELECT a.FACILITY_ID,  a.patient_id,b.PATIENT_NAME,a.DISCHARGE_DATE_TIME,E.LONG_DESC,a.episode_id
        FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f,mp_country g
        WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID 
        and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
        and g.country_code=b.nationality_code
        AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE 
        and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null
        AND a.DISCHARGE_DATE_TIME between :from_date and to_date(:to_date)+1
        and a.FACILITY_ID = 'RH'
        ORDER BY A.ASSIGN_CARE_LOCN_CODE


        """

        self.cursor.execute(discharge_census_revised_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_health_checkup(self, from_date, to_date):

        health_checkup_qurey = """
            
            
        select A.PATIENT_ID,c.patient_name name,get_age(c.date_of_birth,SYSDATE)  Age,c.sex,A.PACKAGE_CODE code,
        B.LONG_DESC Pack_Name,A.EFF_FROM_DATE,A.EFF_TO_DATE,A.PACKAGE_AMT Pack_Amt,
        a.status,a.blng_class_code Class,a.BILL_DOC_NUM
        from BL_PACKAGE_SUB_HDR a, bl_package b,mp_patient c
        where A.PACKAGE_CODE = B.PACKAGE_CODE
        and A.PATIENT_ID = C.PATIENT_ID and a.status in ('C')
        and A.EFF_FROM_DATE between :from_date and to_date(:to_date)+1
        and a.blng_class_code = 'OP'
        and a.OPERATING_FACILITY_ID='RH'
        order by eff_from_Date



        """

        self.cursor.execute(health_checkup_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_pharmacy_report(self, from_date, to_date):

        pharmacy_report_qurey = """
            
            
        select a.episode_id ,a.doc_type_code,a.added_by_id,a.bill_amt, a.doc_num, a.cash_counter_code,a.doc_date
        from BL_BILL_HDR a
        where a.doc_type_code = 'RHOPBL'
        and a.added_date >= :from_date
        AND a.added_date < to_date(:to_date)+1
        and a.cash_counter_code in ('RH00','RH01')


        """

        self.cursor.execute(pharmacy_report_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_card_report(self, from_date, to_date):

        card_report_qurey = """
            
            
        select  TO_CHAR (d.doc_date, 'DD/MM/YY') dat         ,TO_CHAR (d.doc_date, 'HH24:MI:SS') tim
        ,d.doc_type_code||'/'||d.doc_number rec_doc_no          ,d.patient_id UHID
        ,a.SHORT_NAME patient_name          ,d.customer_code          ,c.payer_name
        ,d.doc_amt amount       
        ,d.recpt_type_code          ,d.recpt_nature_code          ,d.recpt_refund_ind
        ,c.slmt_type_code          ,c.slmt_doc_ref_desc "Chq No./Card No."
        ,c.slmt_doc_remarks          ,d.NARRATION          ,c.cash_slmt_flag          ,d.cash_counter_code
        ,d.added_by_id          ,c.cancelled_ind          ,c.bank_code          ,c.bank_branch
        ,d.bill_doc_type_code||'/'||d.bill_doc_number bill_no          ,d.episode_id
        ,c.APPROVAL_REF_NO,c.RCPT_RFND_ID_NO TID
        FROM bl_receipt_refund_dtl c, bl_receipt_refund_hdr d,mp_patient_mast a    ,BL_SLMT_TYPE e 
        WHERE  c.operating_facility_id = 'RH'
        AND d.doc_date >= :from_date
        AND d.doc_date < to_date(:to_date)+1
        AND c.doc_type_code = d.doc_type_code--
        AND c.doc_number = d.doc_number--
        and( d.RECPT_REFUND_IND='R' or
        (d.RECPT_REFUND_IND='F' and d.recpt_nature_code='BI'))
        and c.SLMT_TYPE_CODE=e.SLMT_TYPE_CODE
        and e.CASH_SLMT_FLAG='A'
        and d.patient_id = a.patient_id--
        AND NOT EXISTS (
        SELECT 1
        FROM bl_cancelled_bounced_trx f
        WHERE f.doc_type_code = d.doc_type_code
        AND f.doc_number = d.doc_number
        AND f.cancelled_date  >= :from_date
        AND NVL (d.cancelled_ind, 'N') = 'Y'
        AND f.cancelled_date  < to_date(:to_date)+1)
        union all  
        select  TO_CHAR (f.cancelled_date, 'DD/MM/YY') dat         ,TO_CHAR (f.cancelled_date, 'HH24:MI:SS') tim
        ,d.doc_type_code||'/'||d.doc_number rec_doc_no          ,d.patient_id UHID
        ,a.SHORT_NAME patient_name          ,d.customer_code          ,c.payer_name
        ,-1*d.doc_amt amount       
        ,d.recpt_type_code          ,d.recpt_nature_code          ,d.recpt_refund_ind
        ,c.slmt_type_code          ,c.slmt_doc_ref_desc "Chq No./Card No."
        ,c.slmt_doc_remarks          ,d.NARRATION          ,c.cash_slmt_flag          ,d.cash_counter_code
        ,d.added_by_id          ,c.cancelled_ind          ,c.bank_code          ,c.bank_branch
        ,d.bill_doc_type_code||'/'||d.bill_doc_number bill_no          ,d.episode_id
        ,c.APPROVAL_REF_NO,c.RCPT_RFND_ID_NO TID
        FROM bl_receipt_refund_dtl c, bl_receipt_refund_hdr d,mp_patient_mast a  ,bl_cancelled_bounced_trx f ,BL_SLMT_TYPE e 
        WHERE  c.operating_facility_id = 'RH'
        AND c.doc_type_code = d.doc_type_code--
        AND c.doc_number = d.doc_number--
        and d.patient_id = a.patient_id--
        and( d.RECPT_REFUND_IND='R' or
        (d.RECPT_REFUND_IND='F' and d.recpt_nature_code='BI'))
        and c.SLMT_TYPE_CODE=e.SLMT_TYPE_CODE
        and e.CASH_SLMT_FLAG='A'
        and f.doc_type_code = d.doc_type_code
        AND f.doc_number = d.doc_number
        AND f.cancelled_date  >= :from_date
        AND f.cancelled_date  < to_date(:to_date)+1
        AND trunc(f.cancelled_date)  > trunc(d.doc_date)
        AND NVL (d.cancelled_ind, 'N') = 'Y'




        """

        self.cursor.execute(card_report_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_doctor_fee_package(self, from_date, to_date):

        doctor_fee_package_qurey = """
            
                select a.operating_facility_id, a.patient_id, b.patient_name, a.episode_id, a.service_date,blcommonproc.get_blng_class_code_desc(a.blng_class_code,'en') billing_class,
                    a.blng_srv_code Service_code,      a.service_desc,      blcommonproc.get_practitioner_name  (a.physician_id,  'en'   ) doctor_name,   sum(a.Gross_amt) Gross_amt
                    ,sum(a.Net_amt) net_amount,    sum(a.Doctor_share) Doctor_share, a.PACKAGE_CODE,a.LONG_DESC
                from    
                    (    SELECT   a.operating_facility_id,a.patient_id,a.episode_id, a.episode_type,
                            TO_CHAR (a.service_date, 'DD/MM/RRRR') Service_date,
                            decode(d.RATE_ENTRY_BY_USER_FLAG,'R',d.long_desc,nvl(a.serv_item_desc,d.long_desc)) service_desc,
                            decode(d.RATE_ENTRY_BY_USER_FLAG,'R',a.blng_serv_code,NVL (a.serv_item_code, a.blng_serv_code)) blng_srv_code,
                            a.physician_id,a.blng_serv_code, d.serv_classification_code, 
                            d.serv_grp_code,a.blng_class_code,
                            SUM (NVL (a.org_gross_charge_amt, 0)) Gross_amt,
                            SUM(NVL(a.org_net_charge_amt,0)) Net_amt,
                        SUM(a.org_net_charge_amt * nvl(bl_get_dr_fee_percentage(a.operating_facility_id, a.physician_id, a.episode_type, a.blng_serv_code, d.serv_grp_code, d.serv_classification_code),0)/100) DOCTOR_SHARE
                        , e.PACKAGE_CODE,p.LONG_DESC
                            FROM bl_patient_charges_folio a,
                                bl_blng_serv d,BL_PACKAGE_ENCOUNTER_DTLS e,
                                bl_package p
                            WHERE a.blng_serv_code = d.blng_serv_code
                            and a.EPISODE_ID= e.ENCOUNTER_ID(+)
                            and a.PACKAGE_SEQ_NO = e.PACKAGE_SEQ_NO(+)
                            and e.PACKAGE_CODE=p.PACKAGE_CODE(+)
                            and p.OPERATING_FACILITY_ID(+) = 'RH'
                            AND a.trx_status IS NULL
                            AND a.bill_doc_num is not null
                            AND (('A' !='A' and a.episode_type = 'A')
                                or ('A' ='A' and a.episode_type =a.episode_type)) 
                            AND a.operating_facility_id = 'RH'
                            AND a.bill_doc_date >= :from_date
                            AND a.bill_doc_date <= to_date(:to_date)+1
                            AND a.episode_type IN ('O', 'E', 'R')
                            AND d.comm_doctor_service_yn = 'Y'
                        GROUP BY a.operating_facility_id,
                                a.patient_id,
                                a.episode_id,
                                a.episode_type,
                                a.service_date,
                                d.long_desc,d.RATE_ENTRY_BY_USER_FLAG,
                                a.physician_id,a.serv_item_code,a.serv_item_desc,
                                a.blng_serv_code, a.blng_class_code,d.serv_classification_code, d.serv_grp_code,a.PACKAGE_SERVICE_CODE, e.PACKAGE_CODE,p.LONG_DESC
                            HAVING SUM (NVL (a.org_gross_charge_amt, 0)) <> 0
                        UNION ALL
                        SELECT   a.operating_facility_id,a.patient_id,a.episode_id,a.episode_type,
                                TO_CHAR (a.service_date, 'DD/MM/RRRR') service_date,
                                decode(d.RATE_ENTRY_BY_USER_FLAG,'R',d.long_desc,nvl(a.serv_item_desc,d.long_desc)) service_desc,
                                decode(d.RATE_ENTRY_BY_USER_FLAG,'R',a.blng_serv_code,NVL (a.serv_item_code, a.blng_serv_code)) blng_srv_code,
                                a.physician_id,a.blng_serv_code, d.serv_classification_code, 
                                d.serv_grp_code,a.blng_class_code,
                                SUM (NVL (a.org_gross_charge_amt, 0)) Gross_amt,
                                SUM(NVL(a.org_net_charge_amt,0)) Net_amt,
                                sum((CASE 
                                WHEN a.org_net_charge_amt * nvl(bl_get_dr_fee_percentage(a.operating_facility_id, a.physician_id, a.episode_type, a.blng_serv_code, d.serv_grp_code, d.serv_classification_code),0)/100 > a.org_gross_charge_amt then a.org_net_charge_amt 
                                ELSE
                                    a.org_net_charge_amt * nvl(bl_get_dr_fee_percentage(a.operating_facility_id, a.physician_id, a.episode_type, a.blng_serv_code, d.serv_grp_code, d.serv_classification_code),0)/100
                                END)) Doctor_share, e.PACKAGE_CODE,p.LONG_DESC
                            FROM bl_patient_charges_folio a,
                                bl_blng_serv d,BL_PACKAGE_ENCOUNTER_DTLS e,
                                bl_package p
                            WHERE a.blng_serv_code = d.blng_serv_code
                            and a.EPISODE_ID= e.ENCOUNTER_ID(+)
                            and a.PACKAGE_SEQ_NO = e.PACKAGE_SEQ_NO(+)
                            and e.PACKAGE_CODE=p.PACKAGE_CODE(+)
                            and p.OPERATING_FACILITY_ID(+) = 'RH'
                            AND a.trx_status IS NULL
                            --AND a.bill_doc_num is not null--Commented by Rajesh kumar Modi as on 05.03.2014 for Issue IN47098
                            AND (('A' !='A' and a.episode_type = 'A')
                            or ('A' ='A' and a.episode_type =a.episode_type)) 
                            AND a.operating_facility_id = 'RH'
                            AND a.service_date >= :from_date
                            AND a.service_date <= to_date(:to_date)+1
                            AND a.episode_type IN ('I', 'D')
                                        AND d.comm_doctor_service_yn = 'Y'
                        GROUP BY a.operating_facility_id,
                                a.patient_id,
                                a.episode_id,
                                a.episode_type,
                                a.service_date,
                                d.long_desc,d.RATE_ENTRY_BY_USER_FLAG,
                                a.physician_id,a.serv_item_code,a.serv_item_desc,
                                a.blng_serv_code,a.blng_class_code, d.serv_classification_code, d.serv_grp_code,a.PACKAGE_SERVICE_CODE, e.PACKAGE_CODE,p.LONG_DESC
                            HAVING SUM (NVL (a.org_gross_charge_amt, 0)) <> 0) a, mp_patient b
                where a.patient_id=b.patient_id
                GROUP BY operating_facility_id,A.patient_id,
                        patient_name,
                        episode_id,
                        service_date,a.Gross_amt,a.Net_amt,
                        blcommonproc.get_blng_class_code_desc(a.blng_class_code,'en'),
                        a.service_desc,a.blng_srv_code,
                    blcommonproc.get_practitioner_name
                    (a.physician_id,
                    'en'
                    ) , a.PACKAGE_CODE,a.LONG_DESC
                HAVING  sum(a.doctor_share) <> 0
                ORDER BY  blcommonproc.get_practitioner_name
                    (a.physician_id,
                    'en'
                    )  ASC










        """

        self.cursor.execute(doctor_fee_package_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_op_pharmacy_gst(self, from_date, to_date):

        op_pharmacy_gst_qurey = """
            
        Select a.trx_status,a.episode_type,a.bill_doc_date,a.bill_doc_type_code, a.bill_doc_num,a.patient_id, a.serv_item_code, a.serv_item_desc, a.item_unit_cost, a.base_rate, a.serv_qty, a.batch_id, a.org_gross_charge_amt, a.org_disc_amt,a.org_net_charge_amt,
        a.act_gross_amt, a.addl_charge_amt_in_charge, a.blng_grp_id, b.rule_code, a.standard_base_rate,c.patient_Name
        from
        bl_patient_charges_folio a, bl_pat_chrg_folio_addl_charge b, mp_Patient c
        where
        A.operating_facility_id='RH' and a.operating_facility_id=b.operating_facility_id and a.patient_id=c.patient_id and a.episode_type='R' and B.rule_code like 'GS%' and A.trx_doc_ref=b.trx_doc_ref and a.trx_doc_ref_line_num=b.trx_doc_ref_line_num and
        a.trx_doc_ref_seq_num=b.trx_doc_ref_seq_num and 
        TRUNC(a.trx_date) between :from_date and to_date(:to_date)+1



        """

        self.cursor.execute(op_pharmacy_gst_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_vaccine_report(self, from_date, to_date):

        vaccine_report_qurey = """
            
                SELECT a.operating_facility_id, a.trx_status, a.episode_type,a.bill_doc_date, a.bill_doc_type_code, a.bill_doc_num,
                a.bill_doc_type_code || a.bill_doc_num "BILL NUM", a.patient_id,d.patient_name patnamemast, a.serv_item_code, a.serv_item_desc,
                a.base_rate, a.serv_qty, a.batch_id foliobatch, a.org_gross_charge_amt, a.org_disc_amt, a.org_net_charge_amt,
                a.act_gross_amt, a.addl_charge_amt_in_charge, b.sale_category_code, c.long_desc, a.blng_grp_id, e.primary_key_main,
                f.patient_name patnamesalhdr, g.item_code, g.batch_id saldtlbatch, g.barcode_id, h.hsn_no, null,null,null,
                i.gross_amt, i.serv_disc_amt,i.man_disc_amt, i.overall_disc_amt disc, i.bill_amt, i.bill_prv_doc_number, i.bill_prv_doc_type_code, l.SLMT_TYPE_CODE,i.added_at_ws_no
            FROM bl_patient_charges_folio a,   bl_st_item b,        bl_st_item_sale_catg_hdr c,
                mp_patient d,     bl_patient_charges_interface e,          st_sal_hdr f,
                st_sal_dtl_exp g,          mm_item h,          bl_bill_hdr i,bl_patient_ledger l
            WHERE a.episode_type IN ('R') and f.STORE_CODE = 'RHCOV' AND  g.ITEM_CODE in ('2000062754','2000062855','2000063457','2000063655') and 
            NVL (a.trx_status, 'X') <> 'C' AND NVL (a.bill_doc_type_code, 'z') <> 'z' 
            AND a.TRX_DATE  between :from_date and to_date(:to_date)+1
            AND a.patient_id = e.patient_id AND a.trx_doc_ref = e.trx_doc_ref 
            AND a.trx_doc_ref_line_num = e.trx_doc_ref_line_num AND a.serv_item_code = b.item_code AND b.sale_category_code = c.sale_category_code 
            AND a.patient_id = d.patient_id AND a.patient_id = f.patient_id AND f.doc_type_code || '-' || f.doc_no = e.primary_key_main  
            AND a.serv_item_code = g.item_code AND SUBSTR (a.batch_id, 9, (INSTR (a.batch_id, ';', 9) - 9)) = g.batch_id AND f.doc_no = g.doc_no 
            AND f.doc_type_code = g.doc_type_code AND h.item_code = b.item_code AND i.doc_type_code = a.bill_doc_type_code 
            AND i.patient_id = a.patient_id AND i.doc_num = a.bill_doc_num AND i.episode_type = a.episode_type
            and i.DOC_TYPE_CODE = l.ALL_DOC_TYPE_CODE(+) and i.DOC_NUM = l.ALL_DOC_NUM(+)
        union
        SELECT a.operating_facility_id, a.trx_status, a.episode_type, a.bill_doc_date, a.bill_doc_type_code, a.bill_doc_num,
                a.bill_doc_type_code || a.bill_doc_num "BILL NUM", a.patient_id,      d.patient_name patnamemast, a.serv_item_code, a.serv_item_desc,
                a.base_rate, a.serv_qty, a.batch_id foliobatch,    a.org_gross_charge_amt, a.org_disc_amt, a.org_net_charge_amt,
                a.act_gross_amt, a.addl_charge_amt_in_charge, b.sale_category_code,          c.long_desc, a.blng_grp_id, e.primary_key_main, 
                null, g.item_code, g.batch_id saldtlbatch,null, h.hsn_no, g.sal_doc_type_code, g.sal_doc_no, e.source_doc_ref_for_ret, 
                i.gross_amt, i.serv_disc_amt,i.man_disc_amt, i.overall_disc_amt disc, i.bill_amt, i.bill_prv_doc_number, i.bill_prv_doc_type_code,l.SLMT_TYPE_CODE, i.added_at_ws_no
            FROM bl_patient_charges_folio a,   bl_st_item b,      bl_st_item_sale_catg_hdr c,
                mp_patient d, bl_patient_charges_interface e, st_sal_ret_hdr f,          st_sal_ret_dtl_exp g,
                mm_item h,          bl_bill_hdr i,bl_patient_ledger l
                    WHERE a.episode_type IN ('R') and f.STORE_CODE = 'RHCOV' AND g.ITEM_CODE in ('2000062754','2000062855','2000063457','2000063655') AND NVL (a.trx_status, 'X') <> 'C'
            AND NVL (a.bill_doc_type_code, 'z') <> 'z'  AND a.TRX_DATE  between :from_date and to_date(:to_date)+1
            AND a.patient_id = e.patient_id      AND a.trx_doc_ref = e.trx_doc_ref      AND a.trx_doc_ref_line_num = e.trx_doc_ref_line_num
            AND a.serv_item_code = b.item_code  AND b.sale_category_code = c.sale_category_code AND a.patient_id = d.patient_id AND a.patient_id = f.patient_id
            AND f.doc_type_code || '-' || f.doc_no = e.primary_key_main AND a.serv_item_code = g.item_code AND f.doc_no = g.doc_no
            AND f.doc_type_code = g.doc_type_code      AND SUBSTR (a.batch_id, 9, (INSTR (a.batch_id, ';', 9) - 9)) = g.batch_id AND h.item_code = b.item_code
            AND i.doc_type_code = a.bill_doc_type_code  AND i.patient_id = a.patient_id  AND i.doc_num = a.bill_doc_num AND i.episode_type = a.episode_type
            and i.DOC_TYPE_CODE = l.ALL_DOC_TYPE_CODE(+) and i.DOC_NUM = l.ALL_DOC_NUM(+)



        """

        self.cursor.execute(vaccine_report_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_admissions_with_address(self, from_date, to_date):

        admissions_with_address_qurey = """
                
                
            SELECT
            a.patient_id,b.PATIENT_NAME,b.REGN_DATE,get_age(b.date_of_birth,SYSDATE) Age,b.SEX Sex,TRUNC(a.VISIT_ADM_DATE_TIME) Admission_Date,A.ASSIGN_CARE_LOCN_CODE, 
            A.ASSIGN_BED_CLASS_CODE,E.LONG_DESC,a.ASSIGN_BED_NUM Bed_Num,c.PRACTITIONER_NAME Treating_Doctor,d.LONG_DESC Speciality,A.ASSIGN_BED_CLASS_CODE, f.BLNG_GRP_ID,f.cust_code,f.remark
            ,m.long_name,f.NON_INS_BLNG_GRP_ID,b.ALT_ID3_NO PAN,a.ADDED_BY_ID,a.ADDED_AT_WS_NO,b.form_60_yn,A.episode_id,a.FACILITY_ID,
            H.ADDR1_LINE1,H.ADDR1_LINE2,H.ADDR1_LINE3,
            --H.POSTAL1_CODE,
            t.LONG_DESC Town, g.LONG_DESC Area,
            P.LONG_DESC Pincode,
            i.long_name 
            FROM 
            pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f 
            ,mp_country m,mp_pat_addresses H,mp_postal_code p,
            ar_customer i,
            mp_res_town t, mp_res_area g
            WHERE 
            a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID 
            and a.FACILITY_ID ='RH'
            and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
            AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE 
            and m.COUNTRY_CODE=b.NATIONALITY_CODE
            and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null
            AND a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
            and a.FACILITY_ID = 'RH'
            AND H.PATIENT_ID=A.PATIENT_ID
            AND h.POSTAL1_CODE = p.POSTAL_CODE(+) 
            and f.cust_code=i.cust_code(+)
            and h.RES_TOWN1_CODE =t.RES_TOWN_CODE(+)  and h.RES_AREA1_CODE = g.RES_AREA_CODE(+)
            ORDER BY A.ASSIGN_CARE_LOCN_CODE


            """

        self.cursor.execute(admissions_with_address_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_admissions_report(self, from_date, to_date, facility_code):

        admissions_report_qurey = f"""
                
                
        SELECT a.patient_id,b.PATIENT_NAME,b.REGN_DATE,get_age(b.date_of_birth,SYSDATE) Age,b.SEX Sex,TRUNC(a.VISIT_ADM_DATE_TIME) Admission_Date,A.ASSIGN_CARE_LOCN_CODE, 
        A.ASSIGN_BED_CLASS_CODE,E.LONG_DESC,a.ASSIGN_BED_NUM Bed_Num,c.PRACTITIONER_NAME Treating_Doctor,c.PRACTITIONER_ID,d.LONG_DESC Speciality,A.ASSIGN_BED_CLASS_CODE, f.BLNG_GRP_ID,f.cust_code,f.remark
        ,m.long_name,f.NON_INS_BLNG_GRP_ID,b.ALT_ID3_NO PAN,a.ADDED_BY_ID,a.ADDED_AT_WS_NO,b.form_60_yn,A.episode_id,a.FACILITY_ID
        FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f 
        ,mp_country m
        WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID 
        and a.FACILITY_ID in ({facility_code}) 
        and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
        AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE 
        and m.COUNTRY_CODE=b.NATIONALITY_CODE
        and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null
        AND a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
        and a.FACILITY_ID in ({facility_code}) 
        ORDER BY A.ASSIGN_CARE_LOCN_CODE




            """

        self.cursor.execute(admissions_report_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_admissions_referal(self, from_date, to_date):

        admissions_referal_qurey = """
                
                
        SELECT a.FACILITY_ID , a.patient_id,b.PATIENT_NAME,a.VISIT_ADM_DATE_TIME Admission_Date,E.LONG_DESC,a.episode_id
        FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f,mp_country m
        WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID 
        and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
        AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE 
        and m.COUNTRY_CODE=b.NATIONALITY_CODE
        and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null
        AND a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
        and a.FACILITY_ID = 'RH'
        ORDER BY A.ASSIGN_CARE_LOCN_CODE



            """

        self.cursor.execute(admissions_referal_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_cathlab_report(self, from_date, to_date):

        cathlab_report_qurey = """
                
                
        select a.PERFORMING_FACILITY_ID, a.PATIENT_ID,trunc(a.ORD_DATE_TIME),trunc(a.regn_date_time),a.order_id,
        b.order_catalog_code,b.catalog_desc,b.ORDER_LINE_STATUS,b.ADDED_DATE,b.MODIFIED_BY_ID
        from or_order a,or_order_line b
        where 
        a.order_id = b.order_id and a.order_category = 'TR' and a.order_type_code in ('CATH','PRCH') 
        and b.order_Catalog_code not in ('PRSN000040','PRSN000003','PRAF000012','PRAF000013','PRAF000014','PRCH000001','PRCH000002','PRCH000003','PRSN000006','PRSN000087','PRSN000106','PRSN000107','PRSN000132','PRSN000120','PRSN000104','PRUG000001','PRUG000002','PRUG000003','PRUG000004','PRSN000094','PRSN000001','PRSN000042','PRSN000108','PRBI000001','PRSN000131','PRSN000005','PRSN000128','PRSN000127','PRSN000149','PRSN000150','PRSN000043','PRSN000125','OPGN000253')
        and b.order_line_status = 'RG'
        --and a.patient_id = 'KH1000299325'
        and a.regn_date_time between :from_date and to_date(:to_date)+1--order by trunc(a.regn_date_time)
        and a.PERFORMING_FACILITY_ID='RH'
        order by a.patient_id



            """

        self.cursor.execute(cathlab_report_qurey, [from_date, to_date])
        data = self.cursor.fetchall()

        # only print head
        column_name = [i[0] for i in self.cursor.description]

        # column info
        # for x in self.cursor.description:
        #     print(x)

        if self.cursor:
            self.cursor.close()

        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_daily_revenue_reports(self, revenue_data_rh):
        daily_revenue_reports_qurey = f""" 

        Select * from {revenue_data_rh} order by amount desc 

"""

        self.cursor.execute(
            daily_revenue_reports_qurey,
        )
        data = self.cursor.fetchall()

        column_name = [i[0] for i in self.cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_surgery_report(self, facility_code, from_date, to_date):
        surgery_report_query = f""" 

        select a.CHARGE_DATE_TIME,a.patient_id,a.SERV_ITEM_DESC,a.CHARGE_NET_AMT,b.patient_name,c.long_desc,d.PRACTITIONER_ID,d.PRACTITIONER_NAME,a.episode_id
        from bl_patient_charges_interface a, mp_patient b, bl_blng_serv c, am_practitioner d
        where a.patient_id = b.patient_id and
        a.BLNG_SERV_CODE = c.BLNG_SERV_CODE and
        a.PHYSICIAN_ID = d.PRACTITIONER_ID and
        a.SEC_KEY_MODULE_ID = 'OT'and
        A.CHARGE_NET_AMT !=0 and
        a.OPERATING_FACILITY_ID in ({facility_code}) 
        and a.CHARGE_DATE_TIME between :from_date and to_date(:to_date)+1

"""
        self.cursor.execute(
            surgery_report_query,
            [from_date, to_date],
        )
        data = self.cursor.fetchall()

        column_name = [i[0] for i in self.cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    # clinical admin

    def get_admission_report_for_nursing(self, facility_code, from_date, to_date):
        admission_report_for_nursing_query = f""" 





"""
        self.cursor.execute(
            admission_report_for_nursing_query,
            [from_date, to_date],
        )
        data = self.cursor.fetchall()

        column_name = [i[0] for i in self.cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    # marketing

    def get_rh_admission_report_2(self, facility_code, from_date, to_date):
        rh_admission_report_2_query = f""" 


        SELECT a.patient_id,b.PATIENT_NAME,b.REGN_DATE,get_age(b.date_of_birth,SYSDATE) Age,
        b.SEX Sex,TRUNC(a.VISIT_ADM_DATE_TIME) Admission_Date,a.VISIT_ADM_DATE_TIME ,A.ASSIGN_CARE_LOCN_CODE, 
        A.ASSIGN_BED_CLASS_CODE,a.ASSIGN_BED_NUM Bed_Num,c.PRACTITIONER_NAME Treating_Doctor,
        d.LONG_DESC Speciality,A.ASSIGN_BED_CLASS_CODE, f.BLNG_GRP_ID,f.cust_code,f.remark
        ,m.long_name,f.NON_INS_BLNG_GRP_ID,b.ALT_ID3_NO PAN,a.ADDED_BY_ID,a.ADDED_AT_WS_NO,f.TOT_BUS_GEN_AMT,
        b.form_60_yn,A.episode_id,a.FACILITY_ID,a.REFERRAL_ID,n.FROM_PRACT_NAME,n.FROM_PRACT_ID,o.PRACTITIONER_NAME,
        t.LONG_DESC Town, g.LONG_DESC Area,p.LONG_DESC Pincode ,f.cust_code,i.long_name 
        FROM
        pr_encounter a, mp_patient b,am_practitioner c,am_speciality d--,ip_bed_class e
        ,bl_episode_fin_dtls f ,mp_country m,pr_referral_register n,am_practitioner o,mp_res_town t,mp_postal_code p, mp_res_area g, mp_pat_addresses h, 
        ar_customer i
        WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID and a.PATIENT_ID = h.PATIENT_ID  
        and n.REFERRAL_ID(+) = a.REFERRAL_ID and a.FACILITY_ID in ({facility_code})  and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
        AND a.patient_class = 'IP' AND a.SPECIALTY_CODE = d.SPECIALITY_CODE and m.COUNTRY_CODE=b.NATIONALITY_CODE
        and h.RES_TOWN1_CODE =t.RES_TOWN_CODE(+) and  h.POSTAL1_CODE = p.POSTAL_CODE(+) and h.RES_AREA1_CODE = g.RES_AREA_CODE(+)
        and  n.FROM_PRACT_ID = o.PRACTITIONER_ID (+)--and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE 
        and a.cancel_reason_code is null AND a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
        and a.FACILITY_ID in ({facility_code}) 
        and f.cust_code=i.cust_code(+)
        ORDER BY A.ASSIGN_CARE_LOCN_CODE

"""
        self.cursor.execute(
            rh_admission_report_2_query,
            [from_date, to_date],
        )
        data = self.cursor.fetchall()

        column_name = [i[0] for i in self.cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def get_rh_discharge_report_2(self, facility_code, from_date, to_date):
        rh_discharge_report_2_query = f""" 


        SELECT a.FACILITY_ID , a.patient_id,b.PATIENT_NAME,a.VISIT_ADM_DATE_TIME Admission_Date,E.LONG_DESC
        FROM pr_encounter a, mp_patient b,am_practitioner c,am_speciality d,ip_bed_class e,bl_episode_fin_dtls f,mp_country m
        WHERE a.PATIENT_ID=b.PATIENT_ID AND a.ATTEND_PRACTITIONER_ID =c.PRACTITIONER_ID 
        and  a.PATIENT_ID=f.PATIENT_ID and A.episode_id = f.episode_id
        AND a.patient_class = 'IP'  AND a.SPECIALTY_CODE = d.SPECIALITY_CODE 
        and m.COUNTRY_CODE=b.NATIONALITY_CODE
        and A.ASSIGN_BED_CLASS_CODE = E.BED_CLASS_CODE and a.cancel_reason_code is null
        AND a.VISIT_ADM_DATE_TIME between :from_date and to_date(:to_date)+1
        and a.FACILITY_ID in ({facility_code})
        ORDER BY A.ASSIGN_CARE_LOCN_CODE




"""
        self.cursor.execute(
            rh_discharge_report_2_query,
            [from_date, to_date],
        )
        data = self.cursor.fetchall()

        column_name = [i[0] for i in self.cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name


if __name__ == "__main__":
    a = Ora()
    # b = a.get_online_consultation_report('01-Mar-2022','03-Apr-2022')
    b = a.get_employee_covid_test_report(
        "KH",
        "13-Aug-2022",
        "13-Aug-2022",
    )

    print(b)

    for x in b:
        print(x)
