# search_page.py
import streamlit as st
import datetime

class SearchPage:
    def display(self):
        st.title("Customer Search Page")
        st.write("Please input the following search criteria (any field is optional):")

        # The following fields are used for searching
        customer_name = st.text_input("Customer Name", key="sp_customer_name")
        use_res_filter = st.checkbox("Filter by Residence Card Expiration Date", key="sp_use_res_filter")
        if use_res_filter:
            res_date = st.date_input("Residence Card Expiration Date", key="sp_res_date")
        else:
            res_date = None
        company_name = st.text_input("Company Name", key="sp_company_name")
        legal_rep = st.text_input("Legal Representative", key="sp_legal_rep")

        # New fields added for searching
        visa_filter = st.checkbox("Filter by Visa Expiration Date", key="sp_use_visa_filter")
        if visa_filter:
            visa_date = st.date_input("Visa Expiration Date", key="sp_visa_date")
        else:
            visa_date = None
        has_dep = st.selectbox("Has Dependents", ["", "yes", "no"], key="sp_has_dep")
        dep_dur = st.selectbox("Dependents' Residence Duration", ["", "same", "different"], key="sp_dep_dur")
        maintenance = st.selectbox("Maintenance Entrusted", ["", "yes", "no", "not sure"], key="sp_maintenance")
        need_final = st.selectbox("Need Final Account", ["", "yes", "no"], key="sp_need_final")
        final_filter = st.checkbox("Filter by Final Account Date", key="sp_use_final_filter")
        if final_filter:
            final_date = st.date_input("Final Account Date", key="sp_final_date")
        else:
            final_date = None
        status_opt = ["", "In Progress", "Approved", "Custom"]
        status = st.selectbox("Current Status", status_opt, key="sp_status")
        custom_status = None
        if status == "Custom":
            custom_status = st.text_input("Custom Status", key="sp_custom_status")
        
        company_addr = st.text_input("Company Address", key="sp_company_addr")
        company_phone = st.text_input("Company Phone", key="sp_company_phone")

        # Buttons for searching and going back
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Search", key="sp_search_btn"):
                records = st.session_state.get("employees", [])
                results = []
                for rec in records:
                    match = True
                    # 基本匹配
                    if customer_name and customer_name.lower() not in rec.get("customer_name", "").lower():
                        match = False
                    if company_name and company_name.lower() not in rec.get("company_name", "").lower():
                        match = False
                    if legal_rep and legal_rep.lower() not in rec.get("legal_representative", "").lower():
                        match = False
                    # 日期匹配
                    if use_res_filter and res_date and rec.get("residence_card_date") != res_date:
                        match = False
                    if visa_filter and visa_date and rec.get("visa_expiration_date") != visa_date:
                        match = False
                    # 选择匹配
                    if has_dep and rec.get("has_dependents") != has_dep:
                        match = False
                    if dep_dur and rec.get("dependents_residence_duration") != dep_dur:
                        match = False
                    if maintenance and rec.get("maintenance_entrusted") != maintenance:
                        match = False
                    if need_final and rec.get("need_final_account") != need_final:
                        match = False
                    if final_filter and final_date and rec.get("final_account_date") != final_date:
                        match = False
                    # 状态匹配
                    if status:
                        if status == "Custom":
                            if custom_status and custom_status.lower() not in rec.get("current_status", "").lower():
                                match = False
                        else:
                            if rec.get("current_status") != status:
                                match = False
                    # 文本匹配
                    if company_addr and company_addr.lower() not in rec.get("company_address", "").lower():
                        match = False
                    if company_phone and company_phone not in rec.get("company_phone", ""):
                        match = False

                    if match:
                        results.append(rec)
                st.session_state.sp_search_results = results
        with col2:
            if st.button("Back", key="sp_back_btn"):
                st.session_state.search_page_active = False
                st.session_state.pop("sp_search_results", None)
                try:
                    st.experimental_rerun()
                except AttributeError:
                    pass

        # 渲染结果
        if "sp_search_results" in st.session_state:
            filtered = st.session_state.sp_search_results
            if filtered:
                st.write("### Search Results:")
                for rec in filtered:
                    md = (
                        f"**Customer Name:** {rec.get('customer_name','')}  \
"
                        f"**Residence Expiry:** {rec.get('residence_card_date','')}  \
"
                        f"**Visa Expiry:** {rec.get('visa_expiration_date','')}  \
"
                        f"**Has Dependents:** {rec.get('has_dependents','')}  \
"
                        f"**Dependents Duration:** {rec.get('dependents_residence_duration','')}  \
"
                        f"**Maintenance Entrusted:** {rec.get('maintenance_entrusted','')}  \
"
                        f"**Need Final Account:** {rec.get('need_final_account','')}  \
"
                        f"**Final Account Date:** {rec.get('final_account_date','')}  \
"
                        f"**Current Status:** {rec.get('current_status','')}  \
"
                        f"**Company Name:** {rec.get('company_name','')}  \
"
                        f"**Legal Representative:** {rec.get('legal_representative','')}  \
"
                        f"**Company Address:** {rec.get('company_address','')}  \
"
                        f"**Company Phone:** {rec.get('company_phone','')}"
                    )
                    st.markdown(md)
                    st.write("---")
            else:
                st.info("No matching records found.")
