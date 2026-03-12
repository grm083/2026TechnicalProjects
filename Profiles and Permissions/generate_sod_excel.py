#!/usr/bin/env python3
"""Generate SoD Permission Set Specification Excel workbook."""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ── Style constants ──────────────────────────────────────────────────────────
HEADER_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
SUBHEADER_FONT = Font(name="Calibri", bold=True, size=11)
CONFLICT_FILL = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")
RETAIN_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
NEW_FILL = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
REPLACE_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
CONSOLIDATE_FILL = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


def style_header_row(ws, row, max_col):
    for col in range(1, max_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = THIN_BORDER


def style_data_row(ws, row, max_col, fill=None):
    for col in range(1, max_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.alignment = WRAP
        cell.border = THIN_BORDER
        cell.font = Font(name="Calibri", size=10)
        if fill:
            cell.fill = fill


def auto_width(ws, min_width=12, max_width=50):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        lengths = []
        for cell in col:
            if cell.value:
                lines = str(cell.value).split("\n")
                lengths.append(max(len(line) for line in lines))
        width = min(max(lengths + [min_width]) + 2, max_width)
        ws.column_dimensions[col_letter].width = width


# ── Data ─────────────────────────────────────────────────────────────────────

PERMISSION_SETS = [
    # (ID, Name, Feature Area, Duty, SoD Conflicts, Existing PS, Action, Objects, Key Fields)
    ("A1", "PS_Quote_Price_Accessibility", "Quote / CPQ",
     "Modify price-related fields on Quotes and Quote Lines",
     "A2 (Cost Accessibility)",
     "Price_Accessibility_Permission_Set", "RETAIN",
     "SBQQ__Quote__c, SBQQ__QuoteLine__c",
     "PriceIncrement1-4, PricePrice1-4, PriceUpTo1-4, PriceMinQuantity, PriceUOM, SBQQ__ListPrice__c, SBQQ__PricingMethod__c, Price_Override_Description/Reason"),

    ("A2", "PS_Quote_Cost_Accessibility", "Quote / CPQ",
     "Modify cost-related fields on Quotes and Quote Lines",
     "A1 (Price Accessibility)",
     "Cost_Accessibility_Permission_Set", "RETAIN",
     "SBQQ__Quote__c, SBQQ__QuoteLine__c",
     "CostIncrement1-4, CostPrice1-4, CostUpTo1-4, CostMinQuantity, CostModelType, SBQQ__UnitCost__c, Cost_Override_Description/Reason, Vendor__c, Vendor_Commit_Date__c"),

    ("A3", "PS_Quote_Lifecycle_Management", "Quote / CPQ",
     "Create, edit, manage quotes through lifecycle (excludes price/cost/approval fields)",
     "A5 (Quote Approval)",
     "QuoteOrdersUser", "REPLACE",
     "SBQQ__Quote__c (CRED), SBQQ__QuoteLine__c (CRED), SBQQ__ConfigurationAttribute__c, SBQQ__ProductFeature__c, SBQQ__ProductOption__c, Quote_Line_History_Tracking__c",
     "Status, Integration_Status, Assigned_To, SFDC_Team, Genesys fields, Customer_Request_Date, Duration, Schedule_or_On_Call, Priority, Project, Next_Action fields"),

    ("A4", "PS_Quote_Read_Only", "Quote / CPQ",
     "View-only access to all quote and quote line data including price and cost",
     "None",
     "CPQReadOnly", "RETAIN",
     "SBQQ__Quote__c (R), SBQQ__QuoteLine__c (R), Quote_Line_History_Tracking__c (R)",
     "All fields readable, none editable"),

    ("A5", "PS_Quote_Approval", "Quote / CPQ",
     "Approve or decline quotes; record decisions in Approval Log",
     "A3 (Quote Lifecycle)",
     "None", "NEW",
     "SBQQ__Quote__c (E), Approval_Log__c (CE)",
     "Action_Type, Action_Reason, Manual_Approval_Action, Approve_NTE_Amount, Pending_Information, Special_Handling, Approval_Log Status/Comments/Decision"),

    ("A6", "PS_Quote_MAS_Integration", "Quote / CPQ",
     "Manage MAS integration fields on quote lines",
     "None",
     "MAS_Permissionset", "RETAIN",
     "SBQQ__QuoteLine__c (E)",
     "21 MAS fields: ByPassMASServiceChange, MASAccount, MASBox, MASDelivery, MASNewTicket, MASOpsRouting, MASRemoval, MAS_Swapout, VCRCode"),

    ("B1", "PS_Case_Intake", "Case Management",
     "Create new cases and populate initial intake data",
     "None",
     "None", "NEW",
     "Case (CRE), SBS_Case_Asset__c (CRE)",
     "Case_Type, Case_Sub_Type, Case_Reason, Subject, Description, Contact, Location, Client, Supplier, Emergency, Service_Date, Equipment/Material fields, Day-of-week fields, Offsite address fields"),

    ("B2", "PS_Case_Lifecycle_Management", "Case Management",
     "Progress cases through status, milestones, approval workflows, and closure (excludes financial/SLA)",
     "B3 (Case Financial)",
     "None", "NEW",
     "Case (E), Comment__c (CE)",
     "Status, Case_Sub_Status, Approval_Status, Current_Milestone, Close_Case_Reason, isApproved/Rejected, Case_Comments, PSI_Comments, Authorization fields"),

    ("B3", "PS_Case_Financial", "Case Management",
     "Modify billing, pricing, PO, and charge-related fields on cases",
     "B2 (Case Lifecycle)",
     "None", "NEW",
     "Case (E — field-level)",
     "PurchaseOrder_Number, PurchaseOrder_Required, PO_Override_Reason, Invoice_Number, Disputed_Amount, Chargeable, SalesMeet_Price, No_Price, Price_Quote_Identifier, bale_wire cost fields"),

    ("B4", "PS_Case_SLA_Override", "Case Management",
     "Override SLA dates and service date calculations (supervisor-only)",
     "B1/B2 (Case agent duties)",
     "None", "NEW",
     "Case (E — field-level)",
     "SLA_Service_Date, SLA_Service_Date_Time, SLA_Override_Reason, SLA_Override_Comment, SLA_Violation, Proposed_Service_Date"),

    ("B5", "PS_Case_Read_Only", "Case Management",
     "View-only access to all case data including financial and SLA",
     "None",
     "None", "NEW",
     "Case (R), SBS_Case_Asset__c (R), Comment__c (R)",
     "All fields readable, none editable"),

    ("C1", "PS_Task_Assignment", "Task Management",
     "Create, assign, and reassign tasks",
     "C2 (in audit-sensitive workflows)",
     "None", "NEW",
     "Task (CRE)",
     "OwnerId, Subject, Description, Priority, ActivityDate, WhatId, WhoId, Status, Type"),

    ("C2", "PS_Task_Completion", "Task Management",
     "Complete tasks — set outcomes, results, close",
     "C1 (in audit-sensitive workflows)",
     "None", "NEW",
     "Task (E)",
     "Status (Completed/Closed), CompletedDateTime, CallDisposition, CallDurationInSeconds, Outcome fields"),

    ("C3", "PS_Task_Read_Only", "Task Management",
     "View-only access to all task data",
     "None",
     "None", "NEW",
     "Task (R)",
     "All fields readable, none editable"),

    ("D1", "PS_WorkOrder_Creation", "Work Order",
     "Create and edit work orders and line items (excludes cost fields)",
     "None",
     "None", "NEW",
     "WorkOrder (CRE), WorkOrderLineItem (CRE)",
     "Subject, Description, Status, Priority, Dates, Account/Contact/Asset/Case, Acorn fields, Instructions, Location/Equipment/Material fields"),

    ("D2", "PS_WorkOrder_Cost_Management", "Work Order",
     "Modify cost and financial fields on Work Orders and Line Items",
     "D3 (WO Scheduling)",
     "None", "NEW",
     "WorkOrder (E), WorkOrderLineItem (E) — field-level",
     "Vendor cost fields, service charge fields, billing fields, unit cost, total cost, charge type"),

    ("D3", "PS_WorkOrder_Scheduling", "Work Order",
     "Manage service dates, scheduling, and vendor assignment",
     "D2 (WO Cost Management)",
     "None", "NEW",
     "WorkOrder (E — field-level)",
     "Service_Date, Original_Expected_Date, Proposed_Service_Date, Start/End dates, ETA fields, Vendor assignment, Schedule_or_On_Call, Recurrence"),

    ("D4", "PS_WorkOrder_Read_Only", "Work Order",
     "View-only access to all work order data",
     "None",
     "None", "NEW",
     "WorkOrder (R), WorkOrderLineItem (R)",
     "All fields readable, none editable"),

    ("E1", "PS_Asset_View", "Asset Management",
     "Read-only access to asset records with display capabilities",
     "None",
     "None", "NEW",
     "Asset (R), SBS_Case_Asset__c (R)",
     "All fields readable, none editable"),

    ("E2", "PS_Asset_Financial", "Asset Management",
     "Modify financial fields on assets — cost, discount, pricing",
     "E4 (Asset Configuration)",
     "None", "NEW",
     "Asset (E — field-level)",
     "SBQQ discount/pricing fields, cost fields, billing model, contract pricing, markup"),

    ("E3", "PS_Asset_Availability_Tool", "Asset Management",
     "Execute Asset Availability (AAV) stand-alone tool",
     "None",
     "AAV_Availability_Stand_Alone_Tool + Asset_Availability_User_Permission_Set", "CONSOLIDATE",
     "AAV_Asset_Availability__c (CREDVA/MA)",
     "All 15 AAV fields; Custom Permission: AAV_Asset_Availability_User"),

    ("E4", "PS_Asset_Configuration", "Asset Management",
     "Modify equipment type, container, material, and service config on assets",
     "E2 (Asset Financial)",
     "None", "NEW",
     "Asset (E — field-level)",
     "Equipment type/size/style, Container fields, Material type/code, Product family, Service day fields, Recurrence, Location/site"),

    ("F1", "PS_Pricing_Request_Execution", "Pricing Engine",
     "Create and process pricing requests through full workflow including API",
     "F3 (STP Administration)",
     "Pricing_Access", "RETAIN",
     "Pricing_Request__c (CRE, ViewAll)",
     "70+ fields: cost/price pairs (Haul, Pickup, Disposal, Extra_Pickup), service config, vendor info"),

    ("F2", "PS_Pricing_Request_Read_Only", "Pricing Engine",
     "View-only access to pricing request data",
     "None",
     "Pricing_Read_Only", "RETAIN",
     "Pricing_Request__c (R, ViewAll)",
     "12 key fields readable, none editable"),

    ("F3", "PS_STP_Administration", "Pricing Engine",
     "Configure STP eligibility criteria and manage exception logs",
     "F1 (Pricing Execution)",
     "STP_Administration", "RETAIN",
     "STP_Criteria__c (CREDVA/MA), ExceptionLog__c (R, ViewAll)",
     "22 STP criteria fields: vendor/customer eligibility, equipment rules, market type, frequency, duration"),

    ("G1", "PS_Business_Rule_Administration", "Business Rules & Approvals",
     "Create and manage business rules, NTE rules, notification rules",
     "G3 (Approval Decision)",
     "Business_Rule_Notification", "REFACTOR",
     "Business_Rule__c (CRED), Categorization__c (CRED), Department__c (CRED), Entitlement (CRED)",
     "All 43 Business_Rule__c fields; Custom Perms: BR_Notification, Clone_Button_Visibility"),

    ("G2", "PS_Service_Approver_Configuration", "Business Rules & Approvals",
     "Configure who the approvers are per business rule",
     "G3 (Approval Decision)",
     "SBS_Account_Management (partial)", "REFACTOR",
     "Service_Approver__c (CRED), Out_of_Office__c (CRED)",
     "All 31 Service_Approver fields, all 11 Out_of_Office fields"),

    ("G3", "PS_Approval_Decision", "Business Rules & Approvals",
     "Make approval decisions: approve, reject, request info",
     "G1 (Rule Admin), G2 (Approver Config)",
     "None", "NEW",
     "Approval_Log__c (CRE)",
     "Status, Approval_Comments, Decision_Date_Time, Actual_Approver, Actual_Approver_Contact/Email/Origin/Title"),

    ("G4", "PS_NTE_Approval", "Business Rules & Approvals",
     "Approve Not-To-Exceed amounts on quotes (financial approval)",
     "None",
     "None", "NEW",
     "SBQQ__Quote__c (E — field-level)",
     "Approve_NTE_Amount, is_NTE_Quote"),

    ("G5", "PS_Business_Rule_Read_Only", "Business Rules & Approvals",
     "View-only access to business rules, approvers, and approval logs",
     "None",
     "None", "NEW",
     "Business_Rule__c (R), Service_Approver__c (R), Approval_Log__c (R), Out_of_Office__c (R)",
     "All fields readable, none editable"),

    ("H1", "PS_Account_Management", "Account & Contact",
     "Edit general account data — names, addresses, location codes, market areas",
     "H2 (Account Financial Config)",
     "None", "NEW",
     "Account (E), Account_Title__c (CE)",
     "Customer_ID, Customer_Code, Company_Category, Business_Type, Status, Market_Area, Location_Type, Division, address/phone/email fields"),

    ("H2", "PS_Account_Financial_Configuration", "Account & Contact",
     "Modify billing model, PO requirements, payment terms on accounts",
     "H1 (Account Management)",
     "None", "NEW",
     "Account (E — field-level)",
     "Billing_Model, Billing_Schedule, Billing_Window, Invoice_Method, PO_Required, Federal_Tax_Id, Payment_Terms"),

    ("H3", "PS_Contact_Management", "Account & Contact",
     "Create and edit contacts; manage contact-to-account relationships",
     "H4 (Contact Merge)",
     "Contact_Notification_Maintenance", "ABSORB",
     "Contact (CRE), Contact_Notification_Preference__c (CRE)",
     "ANI, Contact_Status, phone/email, Preferred_Language/Method, Text_Notifications_Opt_In, Account_Title, Account_Department, Location"),

    ("H4", "PS_Contact_Merge", "Account & Contact",
     "Delete and merge duplicate contact records (destructive operation)",
     "H3 (Contact Management)",
     "Merge_Access_for_Non_Admin_Users", "RETAIN",
     "Contact (EDVA/MA), DuplicateRecordSet (R, ViewAll)",
     "Full contact access for merge operations"),

    ("H5", "PS_Notification_Preferences", "Account & Contact",
     "Manage account-level notification preferences",
     "None",
     "Account_Notification_Maintenance", "RETAIN",
     "Account_Notification_Preference__c (CRE)",
     "All notification preference fields"),

    ("I1", "PS_Genesys_Routing_View", "Genesys / CTI",
     "View Genesys routing records and integration status",
     "None",
     "None", "NEW",
     "Genesys_Routing__c (R)",
     "All 42 fields readable, none editable"),

    ("I2", "PS_Genesys_Routing_Control", "Genesys / CTI",
     "Create and manage Genesys routing records and task routing config",
     "None",
     "Task_Genesys_Routing_Permission", "RETAIN",
     "Genesys_Routing__c (CRE), Task_Genesys_Routing_Control__c (CREDVA/MA)",
     "All Genesys fields, Primary_Segment, Service_Flag, Stop_Routing, Task_Type"),

    ("J1", "PS_Communication_Send", "Communication & Email",
     "Send emails, manage email messages, create communication records",
     "None",
     "None", "NEW",
     "Communication_Channel__c (CRE), EmailMessage (CRE)",
     "All 9 Communication_Channel fields, email fields; User Perms: EmailSingle, DistributeFromPersWksp"),

    ("J2", "PS_Communication_Read_Only", "Communication & Email",
     "View communication history, email messages, and channel records",
     "None",
     "None", "NEW",
     "Communication_Channel__c (R), EmailMessage (R)",
     "All fields readable, none editable"),

    ("K2", "PS_Report_Creator", "Reporting & Dashboards",
     "Create and customize reports and dashboards",
     "None",
     "Reports_and_Dashboards_Super_User", "RETAIN",
     "N/A",
     "User Perms: CreateCustomizeDashboards, CreateCustomizeReports, RunReports, ViewPublicDashboards/Reports"),

    ("K3", "PS_Report_Administrator", "Reporting & Dashboards",
     "Full report/dashboard administration including folder management",
     "K2 (Report Creator) in publishing-restricted roles",
     "Reports_and_Dashboards_Administrator", "RETAIN",
     "N/A",
     "User Perms: All K2 perms + CreateDashboardFolders, CreateReportFolders, EditMyDashboards/Reports, ManageDashbdsInPubFolders, ManageReportsInPubFolders"),

    ("L1", "PS_Knowledge_Management", "Administration",
     "Create, edit, and publish knowledge articles",
     "None",
     "Knowledge_Manager_User", "RETAIN",
     "Knowledge__kav (CRED)",
     "User Perms: ArchiveArticles, EditKnowledge, PublishArticles, ViewArchivedArticles, ViewDraftArticles"),

    ("L2", "PS_Project_Services", "Administration",
     "Manage project codes and project-level business rules",
     "None",
     "Project_Services_Project_Management", "RETAIN",
     "Project_Code__c (CRE), Business_Rule__c (CRE)",
     "All Project_Code and business rule fields"),

    ("L3", "PS_Governance_Team", "Administration",
     "Override read-only restrictions for governance updates",
     "None",
     "Governance_Team", "RETAIN",
     "N/A",
     "Custom Perms: Goverance_Team_Access, Unspecified_Contact_Edit"),

    ("L4", "PS_Flow_Management", "Administration",
     "Manage and execute flows with elevated permissions",
     "None",
     "Manage_Flows", "RETAIN",
     "N/A",
     "User Perms: ManageInteraction, RunFlow, ViewRoles, ViewSetup"),

    ("L5", "PS_Market_Area_Alerts_Admin", "Administration",
     "Configure market area alert settings",
     "None",
     "MAA_Admin_Panel_Team", "RETAIN",
     "MAA_Admin_Settings__c (RE)",
     "Custom Perm: MAA_Admin_Panel"),

    ("L6", "PS_Customer_Service_Reporting", "Administration",
     "Customer service supervisor reporting and dashboard access",
     "None",
     "Customer_Service_Reporting_User", "RETAIN",
     "N/A",
     "User Perms: CreateCustomizeReports, CreateReportFolders, ManageCustomReportTypes, ScheduleReports"),

    ("L7", "PS_Escalation_Maintenance", "Administration",
     "Manage vendor escalation contacts and categories",
     "None",
     "Escalation_Maintenance_Permissions", "RETAIN",
     "Category__c (CR)",
     "Escalation contact fields"),

    ("L8", "PS_Launch_FAST", "Administration",
     "LAUNCH/FAST activity log and project tracking",
     "None",
     "Launch_Fast", "RETAIN",
     "FAST_Activity_Log__c (CREDVA/MA)",
     "All FAST activity log fields"),

    ("L9", "PS_Digital_Transformation_Tracking", "Administration",
     "Time tracking for digital transformation projects",
     "None",
     "Digital_Transformation_Time_Tacking", "RETAIN",
     "Digital_Transformation_Time_Tracking__c (CRE)",
     "All time tracking fields"),

    ("L10", "PS_Premium_Delivery_Management", "Administration",
     "Manage premium delivery service enrollment on accounts",
     "None",
     "Manage_Premium_Deliveries", "RETAIN",
     "Account (E — field-level)",
     "Enrolled_in_Premium_Delivery_Service"),

    ("L11", "PS_View_Setup", "Administration",
     "View-only access to org setup and configuration",
     "None",
     "View_Setup_and_Configuration", "RETAIN",
     "N/A",
     "User Perms: ViewRoles, ViewSetup"),

    ("L12", "PS_Modify_All_Data", "Administration",
     "Full administrative data modification — system admin only",
     "None",
     "Modify_All_Data", "RETAIN",
     "N/A",
     "User Perm: ModifyAllData"),

    ("L13", "PS_Password_Never_Expires", "Administration",
     "Integration/API user password policy",
     "None",
     "Password_Never_Expires", "RETAIN",
     "N/A",
     "User Perm: PasswordNeverExpires"),
]

SOD_CONFLICTS = [
    ("A1", "PS_Quote_Price_Accessibility", "A2", "PS_Quote_Cost_Accessibility", "Margin manipulation — user who controls both price and cost can manipulate margins without oversight"),
    ("A3", "PS_Quote_Lifecycle_Management", "A5", "PS_Quote_Approval", "Self-approval — person who creates/edits a quote should not approve it"),
    ("B2", "PS_Case_Lifecycle_Management", "B3", "PS_Case_Financial", "Unauthorized financial changes on cases by general agents"),
    ("B1/B2", "PS_Case_Intake / Lifecycle", "B4", "PS_Case_SLA_Override", "SLA manipulation by case agent — override authority must be separate"),
    ("D2", "PS_WorkOrder_Cost_Management", "D3", "PS_WorkOrder_Scheduling", "Vendor cost/schedule collusion — cost and schedule duties separated"),
    ("G1", "PS_Business_Rule_Administration", "G3", "PS_Approval_Decision", "Self-approval rule authoring — rule author should not be approver"),
    ("G2", "PS_Service_Approver_Configuration", "G3", "PS_Approval_Decision", "Self-appointment as approver — configuring approvers and being one creates risk"),
    ("F1", "PS_Pricing_Request_Execution", "F3", "PS_STP_Administration", "STP criteria manipulation — setting criteria and executing pricing must be separate"),
    ("H1", "PS_Account_Management", "H2", "PS_Account_Financial_Configuration", "Unauthorized billing configuration — financial config requires separate authority"),
    ("H3", "PS_Contact_Management", "H4", "PS_Contact_Merge", "Uncontrolled data destruction — create/edit and merge/delete require different authority"),
]

PSG_COMPOSITIONS = {
    "PSG_Customer_Service_Agent": [
        ("B1", "PS_Case_Intake", "Core duty: create cases"),
        ("B2", "PS_Case_Lifecycle_Management", "Core duty: manage case progress"),
        ("C1", "PS_Task_Assignment", "Core duty: manage tasks"),
        ("C2", "PS_Task_Completion", "Core duty: complete tasks"),
        ("A4", "PS_Quote_Read_Only", "View quotes but not edit"),
        ("D4", "PS_WorkOrder_Read_Only", "View work orders"),
        ("E1", "PS_Asset_View", "View assets"),
        ("G5", "PS_Business_Rule_Read_Only", "View rules"),
        ("I1", "PS_Genesys_Routing_View", "View routing"),
        ("J1", "PS_Communication_Send", "Send emails to customers"),
        ("H3", "PS_Contact_Management", "Manage contacts on cases"),
    ],
    "PSG_Customer_Service_Lead": [
        ("B1", "PS_Case_Intake", "Inherited from Agent"),
        ("B2", "PS_Case_Lifecycle_Management", "Inherited from Agent"),
        ("B4", "PS_Case_SLA_Override", "Supervisor: override SLA"),
        ("C1", "PS_Task_Assignment", "Inherited from Agent"),
        ("C2", "PS_Task_Completion", "Inherited from Agent"),
        ("A4", "PS_Quote_Read_Only", "Inherited from Agent"),
        ("D4", "PS_WorkOrder_Read_Only", "Inherited from Agent"),
        ("E1", "PS_Asset_View", "Inherited from Agent"),
        ("G3", "PS_Approval_Decision", "Supervisor: approve/reject"),
        ("G5", "PS_Business_Rule_Read_Only", "Inherited from Agent"),
        ("I1", "PS_Genesys_Routing_View", "Inherited from Agent"),
        ("J1", "PS_Communication_Send", "Inherited from Agent"),
        ("H3", "PS_Contact_Management", "Inherited from Agent"),
        ("K2", "PS_Report_Creator", "Create team reports"),
    ],
    "PSG_SSM_Agent": [
        ("B1", "PS_Case_Intake", "Create cases"),
        ("B2", "PS_Case_Lifecycle_Management", "Manage cases"),
        ("B3", "PS_Case_Financial", "SSM handles financial fields"),
        ("C1", "PS_Task_Assignment", "Manage tasks"),
        ("C2", "PS_Task_Completion", "Complete tasks"),
        ("A3", "PS_Quote_Lifecycle_Management", "Create and manage quotes"),
        ("A2", "PS_Quote_Cost_Accessibility", "SSM manages cost (NOT price)"),
        ("D1", "PS_WorkOrder_Creation", "Create work orders"),
        ("E1", "PS_Asset_View", "View assets"),
        ("F1", "PS_Pricing_Request_Execution", "Execute pricing requests"),
        ("G5", "PS_Business_Rule_Read_Only", "View rules"),
        ("I2", "PS_Genesys_Routing_Control", "Manage routing"),
        ("J1", "PS_Communication_Send", "Send emails"),
        ("H3", "PS_Contact_Management", "Manage contacts"),
    ],
    "PSG_Sales_Agent": [
        ("A3", "PS_Quote_Lifecycle_Management", "Create and manage quotes"),
        ("A1", "PS_Quote_Price_Accessibility", "Sales manages price (NOT cost)"),
        ("A4", "PS_Quote_Read_Only", "View all quote data"),
        ("B5", "PS_Case_Read_Only", "View cases"),
        ("E1", "PS_Asset_View", "View assets"),
        ("F2", "PS_Pricing_Request_Read_Only", "View pricing requests"),
        ("H1", "PS_Account_Management", "Manage accounts"),
    ],
    "PSG_Vendor_Relations": [
        ("D1", "PS_WorkOrder_Creation", "Create work orders"),
        ("D2", "PS_WorkOrder_Cost_Management", "Manage vendor costs"),
        ("D3", "PS_WorkOrder_Scheduling", "Schedule vendor services"),
        ("A2", "PS_Quote_Cost_Accessibility", "Manage cost side of quotes"),
        ("B5", "PS_Case_Read_Only", "View cases"),
        ("E4", "PS_Asset_Configuration", "Configure assets"),
        ("F1", "PS_Pricing_Request_Execution", "Execute pricing"),
        ("L7", "PS_Escalation_Maintenance", "Manage vendor escalations"),
        ("J1", "PS_Communication_Send", "Communicate with vendors"),
    ],
    "PSG_Compliance": [
        ("B5", "PS_Case_Read_Only", "Audit cases"),
        ("A4", "PS_Quote_Read_Only", "Audit quotes"),
        ("D4", "PS_WorkOrder_Read_Only", "Audit work orders"),
        ("G5", "PS_Business_Rule_Read_Only", "Audit rules"),
        ("F2", "PS_Pricing_Request_Read_Only", "Audit pricing"),
        ("K2", "PS_Report_Creator", "Create compliance reports"),
        ("L11", "PS_View_Setup", "View configuration"),
    ],
    "PSG_Business_Rule_Administrator": [
        ("G1", "PS_Business_Rule_Administration", "Configure rules"),
        ("G2", "PS_Service_Approver_Configuration", "Configure approvers"),
        ("L2", "PS_Project_Services", "Manage project codes"),
        ("B5", "PS_Case_Read_Only", "Context for rule creation"),
        ("A4", "PS_Quote_Read_Only", "Context for rule creation"),
    ],
    "PSG_IT_Support": [
        ("F3", "PS_STP_Administration", "Configure STP criteria"),
        ("I2", "PS_Genesys_Routing_Control", "Manage routing config"),
        ("L1", "PS_Knowledge_Management", "Manage knowledge base"),
        ("L4", "PS_Flow_Management", "Manage flows"),
        ("L5", "PS_Market_Area_Alerts_Admin", "Configure alerts"),
        ("L11", "PS_View_Setup", "View configuration"),
        ("K3", "PS_Report_Administrator", "Manage reporting infrastructure"),
    ],
}

MIGRATION = [
    ("Price_Accessibility_Permission_Set", "RETAIN", "A1 — PS_Quote_Price_Accessibility"),
    ("Cost_Accessibility_Permission_Set", "RETAIN", "A2 — PS_Quote_Cost_Accessibility"),
    ("CPQReadOnly", "RETAIN", "A4 — PS_Quote_Read_Only"),
    ("QuoteOrdersUser", "REPLACE", "A3 — PS_Quote_Lifecycle (split out financial fields)"),
    ("MAS_Permissionset", "RETAIN", "A6 — PS_Quote_MAS_Integration"),
    ("Pricing_Access", "RETAIN", "F1 — PS_Pricing_Request_Execution"),
    ("Pricing_Read_Only", "RETAIN", "F2 — PS_Pricing_Request_Read_Only"),
    ("STP_Administration", "RETAIN", "F3 — PS_STP_Administration"),
    ("Business_Rule_Notification", "REFACTOR", "G1 + G2 (split rule admin from approver config)"),
    ("SBS_Account_Management", "REFACTOR", "G1 + G2 (absorb into rule admin/approver config)"),
    ("Project_Services_Project_Management", "RETAIN", "L2 — PS_Project_Services"),
    ("Governance_Team", "RETAIN", "L3 — PS_Governance_Team"),
    ("Task_Genesys_Routing_Permission", "RETAIN", "I2 — PS_Genesys_Routing_Control"),
    ("AAV_Availability_Stand_Alone_Tool", "CONSOLIDATE", "E3 — PS_Asset_Availability_Tool"),
    ("Asset_Availability_User_Permission_Set", "CONSOLIDATE", "E3 — PS_Asset_Availability_Tool"),
    ("Reports_and_Dashboards_Administrator", "RETAIN", "K3 — PS_Report_Administrator"),
    ("Reports_and_Dashboards_Super_User", "RETAIN", "K2 — PS_Report_Creator"),
    ("Customer_Service_Reporting_User", "RETAIN", "L6 — PS_Customer_Service_Reporting"),
    ("Contact_Notification_Maintenance", "ABSORB", "H3 — PS_Contact_Management"),
    ("Account_Notification_Maintenance", "RETAIN", "H5 — PS_Notification_Preferences"),
    ("Merge_Access_for_Non_Admin_Users", "RETAIN", "H4 — PS_Contact_Merge"),
    ("Manage_Premium_Deliveries", "RETAIN", "L10 — PS_Premium_Delivery_Management"),
    ("Knowledge_Manager_User", "RETAIN", "L1 — PS_Knowledge_Management"),
    ("Manage_Flows", "RETAIN", "L4 — PS_Flow_Management"),
    ("MAA_Admin_Panel_Team", "RETAIN", "L5 — PS_Market_Area_Alerts_Admin"),
    ("Escalation_Maintenance_Permissions", "RETAIN", "L7 — PS_Escalation_Maintenance"),
    ("Launch_Fast", "RETAIN", "L8 — PS_Launch_FAST"),
    ("Digital_Transformation_Time_Tacking", "RETAIN", "L9 — PS_Digital_Transformation_Tracking"),
    ("View_Setup_and_Configuration", "RETAIN", "L11 — PS_View_Setup"),
    ("Modify_All_Data", "RETAIN", "L12 — PS_Modify_All_Data"),
    ("Password_Never_Expires", "RETAIN", "L13 — PS_Password_Never_Expires"),
]

ACTION_FILLS = {
    "RETAIN": RETAIN_FILL,
    "NEW": NEW_FILL,
    "REPLACE": REPLACE_FILL,
    "REFACTOR": REPLACE_FILL,
    "CONSOLIDATE": CONSOLIDATE_FILL,
    "ABSORB": CONSOLIDATE_FILL,
}


def build_workbook():
    wb = openpyxl.Workbook()

    # ── Sheet 1: Permission Set Inventory ────────────────────────────────
    ws = wb.active
    ws.title = "Permission Set Inventory"
    headers = ["ID", "Permission Set Name", "Feature Area", "Duty / Description",
               "SoD Conflicts", "Existing PS", "Action", "Objects (CRUD)", "Key Fields & Permissions"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    style_header_row(ws, 1, len(headers))

    current_area = None
    row = 2
    for ps in PERMISSION_SETS:
        # Insert subheader row for new feature areas
        if ps[2] != current_area:
            current_area = ps[2]
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=len(headers))
            cell = ws.cell(row=row, column=1, value=current_area)
            cell.font = SUBHEADER_FONT
            cell.fill = SUBHEADER_FILL
            cell.alignment = Alignment(horizontal="left", vertical="center")
            for c in range(1, len(headers) + 1):
                ws.cell(row=row, column=c).border = THIN_BORDER
                ws.cell(row=row, column=c).fill = SUBHEADER_FILL
            row += 1

        for col, val in enumerate(ps, 1):
            ws.cell(row=row, column=col, value=val)

        fill = ACTION_FILLS.get(ps[6])
        style_data_row(ws, row, len(headers), fill=None)
        if fill:
            ws.cell(row=row, column=7).fill = fill
        row += 1

    auto_width(ws)
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{row - 1}"
    ws.freeze_panes = "A2"

    # ── Sheet 2: SoD Conflict Matrix ─────────────────────────────────────
    ws2 = wb.create_sheet("SoD Conflict Matrix")
    headers2 = ["PS A — ID", "PS A — Name", "PS B — ID", "PS B — Name", "Risk / Rationale"]
    for col, h in enumerate(headers2, 1):
        ws2.cell(row=1, column=col, value=h)
    style_header_row(ws2, 1, len(headers2))

    for i, conflict in enumerate(SOD_CONFLICTS, 2):
        for col, val in enumerate(conflict, 1):
            ws2.cell(row=i, column=col, value=val)
        style_data_row(ws2, i, len(headers2))
        ws2.cell(row=i, column=1).fill = CONFLICT_FILL
        ws2.cell(row=i, column=3).fill = CONFLICT_FILL

    auto_width(ws2, max_width=60)
    ws2.freeze_panes = "A2"

    # ── Sheet 3: PSG Composition ─────────────────────────────────────────
    ws3 = wb.create_sheet("PSG Composition")
    headers3 = ["PSG Name", "Permission Set ID", "Permission Set Name", "Rationale"]
    for col, h in enumerate(headers3, 1):
        ws3.cell(row=1, column=col, value=h)
    style_header_row(ws3, 1, len(headers3))

    row = 2
    for psg_name, members in PSG_COMPOSITIONS.items():
        for j, (ps_id, ps_name, rationale) in enumerate(members):
            ws3.cell(row=row, column=1, value=psg_name if j == 0 else "")
            ws3.cell(row=row, column=2, value=ps_id)
            ws3.cell(row=row, column=3, value=ps_name)
            ws3.cell(row=row, column=4, value=rationale)
            style_data_row(ws3, row, len(headers3))
            if j == 0:
                ws3.cell(row=row, column=1).font = Font(name="Calibri", bold=True, size=10)
            row += 1
        # blank separator
        row += 1

    auto_width(ws3, max_width=55)
    ws3.freeze_panes = "A2"

    # ── Sheet 4: PSG-to-PS Matrix (cross-reference) ─────────────────────
    ws4 = wb.create_sheet("PSG-PS Cross Reference")

    # Get unique PS IDs in order
    ps_ids = [ps[0] for ps in PERMISSION_SETS]
    psg_names = list(PSG_COMPOSITIONS.keys())

    ws4.cell(row=1, column=1, value="Permission Set \\ PSG →")
    for col, psg in enumerate(psg_names, 2):
        ws4.cell(row=1, column=col, value=psg.replace("PSG_", ""))
    style_header_row(ws4, 1, len(psg_names) + 1)

    for i, ps in enumerate(PERMISSION_SETS, 2):
        ps_id = ps[0]
        ws4.cell(row=i, column=1, value=f"{ps_id} — {ps[1]}")
        ws4.cell(row=i, column=1).font = Font(name="Calibri", size=9)
        ws4.cell(row=i, column=1).border = THIN_BORDER

        for col, psg_name in enumerate(psg_names, 2):
            member_ids = [m[0] for m in PSG_COMPOSITIONS[psg_name]]
            if ps_id in member_ids:
                cell = ws4.cell(row=i, column=col, value="✓")
                cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
            else:
                cell = ws4.cell(row=i, column=col, value="")
            cell.alignment = CENTER
            cell.border = THIN_BORDER
            cell.font = Font(name="Calibri", size=10)

    auto_width(ws4, min_width=14, max_width=40)
    ws4.freeze_panes = "B2"

    # ── Sheet 5: Role Mapping Template ───────────────────────────────────
    ws5 = wb.create_sheet("Role Mapping Template")
    headers5 = ["Current Role / Title", "Department", "Primary PSG",
                "Additional PSGs (if any)", "Additional Individual PSs",
                "Notes / Justification", "Approved By", "Date"]
    for col, h in enumerate(headers5, 1):
        ws5.cell(row=1, column=col, value=h)
    style_header_row(ws5, 1, len(headers5))

    # Pre-populate some example rows
    example_roles = [
        ("Customer Service Representative", "Customer Service", "PSG_Customer_Service_Agent", "", "", "", "", ""),
        ("Customer Service Team Lead", "Customer Service", "PSG_Customer_Service_Lead", "", "", "", "", ""),
        ("SSM Representative", "SSM", "PSG_SSM_Agent", "", "", "", "", ""),
        ("Sales Representative", "Sales", "PSG_Sales_Agent", "", "", "", "", ""),
        ("Vendor Relations Specialist", "Vendor Management", "PSG_Vendor_Relations", "", "", "", "", ""),
        ("Compliance Analyst", "Compliance", "PSG_Compliance", "", "", "", "", ""),
        ("Business Rules Administrator", "Operations", "PSG_Business_Rule_Administrator", "", "", "", "", ""),
        ("IT Support Analyst", "IT", "PSG_IT_Support", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
        ("", "", "", "", "", "", "", ""),
    ]
    for i, role in enumerate(example_roles, 2):
        for col, val in enumerate(role, 1):
            ws5.cell(row=i, column=col, value=val)
        style_data_row(ws5, i, len(headers5))

    auto_width(ws5, max_width=40)
    ws5.freeze_panes = "A2"

    # ── Sheet 6: Migration Path ──────────────────────────────────────────
    ws6 = wb.create_sheet("Migration Path")
    headers6 = ["Existing Permission Set", "Action", "New Permission Set(s)"]
    for col, h in enumerate(headers6, 1):
        ws6.cell(row=1, column=col, value=h)
    style_header_row(ws6, 1, len(headers6))

    for i, (existing, action, new_ps) in enumerate(MIGRATION, 2):
        ws6.cell(row=i, column=1, value=existing)
        ws6.cell(row=i, column=2, value=action)
        ws6.cell(row=i, column=3, value=new_ps)
        fill = ACTION_FILLS.get(action)
        style_data_row(ws6, i, len(headers6))
        if fill:
            ws6.cell(row=i, column=2).fill = fill

    # Add NEW permission sets at the bottom
    new_ps_list = [ps for ps in PERMISSION_SETS if ps[6] == "NEW"]
    row = len(MIGRATION) + 3
    ws6.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    cell = ws6.cell(row=row, column=1, value="NEW Permission Sets to Create")
    cell.font = SUBHEADER_FONT
    cell.fill = SUBHEADER_FILL
    for c in range(1, 4):
        ws6.cell(row=row, column=c).border = THIN_BORDER
        ws6.cell(row=row, column=c).fill = SUBHEADER_FILL
    row += 1

    for ps in new_ps_list:
        ws6.cell(row=row, column=1, value="(none)")
        ws6.cell(row=row, column=2, value="NEW")
        ws6.cell(row=row, column=3, value=f"{ps[0]} — {ps[1]}")
        style_data_row(ws6, row, 3)
        ws6.cell(row=row, column=2).fill = NEW_FILL
        row += 1

    auto_width(ws6, max_width=55)
    ws6.freeze_panes = "A2"

    return wb


if __name__ == "__main__":
    wb = build_workbook()
    output_path = "/home/user/2026TechnicalProjects/Profiles and Permissions/SoD-Permission-Set-Specification.xlsx"
    wb.save(output_path)
    print(f"Excel workbook saved to: {output_path}")
    print(f"Sheets: {wb.sheetnames}")
