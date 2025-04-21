# modify_page.py
import streamlit as st
import datetime

class ModifyPage:
    def display(self):
        st.title("Search Portal (Admin / Superadmin)")
        st.write("Please input the following search criteria (any field is optional):")

        # 搜索条件输入框
        customer_name = st.text_input("Customer Name", key="search_customer_name")
        use_date_filter = st.checkbox("Filter by Residence Card Expiration Date", key="search_use_date")
        if use_date_filter:
            residence_card_date = st.date_input("Residence Card Expiration Date", key="search_date")
        else:
            residence_card_date = None
        company_name = st.text_input("Company Name", key="search_company")
        legal_rep = st.text_input("Legal Representative", key="search_legal")

        # Add Customer 按钮
        if st.button("Add Customer", key="add_cust_button"):
            st.session_state.show_add_form = True

        # 新增表单渲染
        if st.session_state.get("show_add_form", False):
            self.render_add_customer()

        # 搜索按钮
        if st.button("Search", key="search_button"):
            records = st.session_state.get("employees", [])
            filtered = []
            for rec in records:
                match = True
                if customer_name and customer_name.lower() not in rec.get("customer_name", "").lower():
                    match = False
                if company_name and company_name.lower() not in rec.get("company_name", "").lower():
                    match = False
                if legal_rep and legal_rep.lower() not in rec.get("legal_representative", "").lower():
                    match = False
                if use_date_filter and residence_card_date is not None and rec.get("residence_card_date") != residence_card_date:
                    match = False
                if match:
                    filtered.append(rec)
            st.session_state.filtered_employees = filtered
            # 重置新增表单
            st.session_state.show_add_form = False

        # 显示搜索结果
        if "filtered_employees" in st.session_state:
            results = st.session_state.filtered_employees
            if results:
                st.write("### Search Results:")
                for idx, rec in enumerate(results):
                    with st.expander(f"Customer: {rec.get('customer_name')}", expanded=True):
                        # Original fields
                        new_name = st.text_input("Customer Name", value=rec.get("customer_name", ""), key=f"edit_name_{idx}")
                        new_date = st.date_input("Residence Card Expiration Date", value=rec.get("residence_card_date", datetime.date.today()), key=f"edit_date_{idx}")
                        new_company = st.text_input("Company Name", value=rec.get("company_name", ""), key=f"edit_company_{idx}")
                        new_legal = st.text_input("Legal Representative", value=rec.get("legal_representative", ""), key=f"edit_legal_{idx}")
                        # New fields
                        new_visa = st.date_input("Visa Expiration Date", value=rec.get("visa_expiration_date", datetime.date.today()), key=f"edit_visa_{idx}")
                        new_has_dep = st.selectbox("Has Dependents", ["yes", "no"], index=0 if rec.get("has_dependents", "yes") == "yes" else 1, key=f"edit_has_dep_{idx}")
                        new_dep_dur = st.selectbox("Dependents' Residence Duration", ["same", "different"], index=0 if rec.get("dependents_residence_duration", "same") == "same" else 1, key=f"edit_dep_dur_{idx}")
                        if new_has_dep == "yes":
                            if new_dep_dur == "different":
                                new_dep_date = st.date_input("Dependents' Expiration Date", value=rec.get("dependent_residence_expiration_date", datetime.date.today()), key=f"edit_dep_date_{idx}")
                            else:
                                new_dep_date = new_visa
                        else:
                            new_dep_date = None
                        new_maint = st.selectbox("Maintenance Entrusted", ["yes", "no", "not sure"], index=["yes", "no", "not sure"].index(rec.get("maintenance_entrusted", "yes")), key=f"edit_maint_{idx}")
                        new_need_final = st.selectbox("Need Final Account", ["yes", "no"], index=0 if rec.get("need_final_account", "yes") == "yes" else 1, key=f"edit_need_final_{idx}")
                        new_final_date = st.date_input("Final Account Date", value=rec.get("final_account_date", datetime.date.today()), key=f"edit_final_date_{idx}")
                        status_opts = ["In Progress", "Approved", "Custom"]
                        default_status = rec.get("current_status", "In Progress")
                        if default_status not in status_opts:
                            default_status = "Custom"
                        new_status_sel = st.selectbox("Current Status", status_opts, index=status_opts.index(default_status), key=f"edit_status_{idx}")
                        if new_status_sel == "Custom":
                            new_status = st.text_input("Custom Status", value=rec.get("current_status", "") if rec.get("current_status") not in ["In Progress", "Approved"] else "", key=f"edit_status_custom_{idx}")
                        else:
                            new_status = new_status_sel
                        new_addr = st.text_input("Company Address", value=rec.get("company_address", ""), key=f"edit_addr_{idx}")
                        new_phone = st.text_input("Company Phone", value=rec.get("company_phone", ""), key=f"edit_phone_{idx}")

                        # Uptate the button
                        if st.button("Update Customer", key=f"update_{idx}"):
                            orig_idx = st.session_state.employees.index(rec)
                            updated = {
                                "customer_name": new_name,
                                "residence_card_date": new_date,
                                "company_name": new_company,
                                "legal_representative": new_legal,
                                "visa_expiration_date": new_visa,
                                "has_dependents": new_has_dep,
                                "dependents_residence_duration": new_dep_dur,
                                "dependent_residence_expiration_date": new_dep_date,
                                "maintenance_entrusted": new_maint,
                                "need_final_account": new_need_final,
                                "final_account_date": new_final_date,
                                "current_status": new_status,
                                "company_address": new_addr,
                                "company_phone": new_phone
                            }
                            st.session_state.employees[orig_idx] = updated
                            st.session_state.filtered_employees[idx] = updated
                            st.success(f"Customer {new_name} updated!")
                        # The delete button
                        if st.button("Delete Customer", key=f"delete_{idx}"):
                            orig_idx = st.session_state.employees.index(rec)
                            st.session_state.employees.pop(orig_idx)
                            st.session_state.filtered_employees.pop(idx)
                            st.success(f"Customer {rec.get('customer_name')} deleted!")
            else:
                st.info("No matching records found.")

        # The back button
        if st.button("Back", key="back_button"):
            st.session_state.pop("filtered_employees", None)
            st.session_state.pop("show_add_form", None)
            try:
                st.experimental_rerun()
            except AttributeError:
                pass

    def render_add_customer(self):
        st.subheader("Add New Customer")
        new_customer_name = st.text_input("Customer Name", key="new_cust_name")
        new_residence_card_date = st.date_input("Residence Card Expiration Date", key="new_cust_date")
        new_company_name = st.text_input("Company Name", key="new_cust_company")
        new_legal_representative = st.text_input("Legal Representative", key="new_cust_legal")
        new_visa = st.date_input("Visa Expiration Date", key="new_cust_visa")
        new_has_dep = st.selectbox("Has Dependents", ["yes", "no"], key="new_cust_has_dep")
        new_dep_dur = st.selectbox("Dependents' Residence Duration", ["same", "different"], key="new_cust_dep_dur")
        if new_has_dep == "yes":
            if new_dep_dur == "different":
                new_dep_date = st.date_input("Dependents' Expiration Date", key="new_cust_dep_date")
            else:
                new_dep_date = new_visa
        else:
            new_dep_date = None
        new_maint = st.selectbox("Maintenance Entrusted", ["yes", "no", "not sure"], key="new_cust_maint")
        new_need_final = st.selectbox("Need Final Account", ["yes", "no"], key="new_cust_need_final")
        new_final_date = st.date_input("Final Account Date", key="new_cust_final_date")
        status_opts = ["In Progress", "Approved", "Custom"]
        new_status_sel = st.selectbox("Current Status", status_opts, key="new_cust_status_sel")
        if new_status_sel == "Custom":
            new_status = st.text_input("Custom Status", key="new_cust_status_custom")
        else:
            new_status = new_status_sel
        new_addr = st.text_input("Company Address", key="new_cust_addr")
        new_phone = st.text_input("Company Phone", key="new_cust_phone")
        if st.button("Save Customer", key="save_cust_button"):
            new_customer = {
                "customer_name": new_customer_name,
                "residence_card_date": new_residence_card_date,
                "company_name": new_company_name,
                "legal_representative": new_legal_representative,
                "visa_expiration_date": new_visa,
                "has_dependents": new_has_dep,
                "dependents_residence_duration": new_dep_dur,
                "dependent_residence_expiration_date": new_dep_date,
                "maintenance_entrusted": new_maint,
                "need_final_account": new_need_final,
                "final_account_date": new_final_date,
                "current_status": new_status,
                "company_address": new_addr,
                "company_phone": new_phone
            }
            st.session_state.employees.append(new_customer)
            st.success(f"New customer {new_customer_name} added!")
            st.session_state.pop("show_add_form", None)
            st.session_state.pop("filtered_employees", None)
            try:
                st.experimental_rerun()
            except AttributeError:
                pass
