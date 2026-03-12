#!/usr/bin/env python3
"""
Generate SoD-compliant permission set XML metadata files.
Creates the 25 NEW permission sets identified in SoD-Permission-Set-Specification.md.
Existing permission sets that are RETAINED are not touched.
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

OUTPUT_DIR = "/home/user/2026TechnicalProjects/force-app/main/default/permissionsets"


def build_ps_xml(label, description, *, field_perms=None, object_perms=None,
                 class_accesses=None, user_perms=None, custom_perms=None,
                 page_accesses=None, tab_settings=None, custom_metadata=None,
                 license_type=None):
    """Build a PermissionSet XML tree."""
    root = ET.Element("PermissionSet")
    root.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    # classAccesses (alphabetical by class name)
    if class_accesses:
        for cls in sorted(class_accesses):
            ca = ET.SubElement(root, "classAccesses")
            ET.SubElement(ca, "apexClass").text = cls
            ET.SubElement(ca, "enabled").text = "true"

    # customMetadataTypeAccesses
    if custom_metadata:
        for md in sorted(custom_metadata):
            cma = ET.SubElement(root, "customMetadataTypeAccesses")
            ET.SubElement(cma, "enabled").text = "true"
            ET.SubElement(cma, "name").text = md

    # customPermissions
    if custom_perms:
        for cp in sorted(custom_perms):
            cpn = ET.SubElement(root, "customPermissions")
            ET.SubElement(cpn, "enabled").text = "true"
            ET.SubElement(cpn, "name").text = cp

    # description
    ET.SubElement(root, "description").text = description

    # fieldPermissions (alphabetical by field)
    if field_perms:
        for field, editable in sorted(field_perms, key=lambda x: x[0]):
            fp = ET.SubElement(root, "fieldPermissions")
            ET.SubElement(fp, "editable").text = str(editable).lower()
            ET.SubElement(fp, "field").text = field
            ET.SubElement(fp, "readable").text = "true"

    ET.SubElement(root, "hasActivationRequired").text = "false"

    ET.SubElement(root, "label").text = label

    if license_type:
        ET.SubElement(root, "license").text = license_type

    # objectPermissions
    if object_perms:
        for obj in sorted(object_perms, key=lambda x: x["object"]):
            op = ET.SubElement(root, "objectPermissions")
            ET.SubElement(op, "allowCreate").text = str(obj.get("create", False)).lower()
            ET.SubElement(op, "allowDelete").text = str(obj.get("delete", False)).lower()
            ET.SubElement(op, "allowEdit").text = str(obj.get("edit", False)).lower()
            ET.SubElement(op, "allowRead").text = str(obj.get("read", True)).lower()
            ET.SubElement(op, "modifyAllRecords").text = str(obj.get("modifyAll", False)).lower()
            ET.SubElement(op, "object").text = obj["object"]
            ET.SubElement(op, "viewAllRecords").text = str(obj.get("viewAll", False)).lower()

    # pageAccesses
    if page_accesses:
        for page in sorted(page_accesses):
            pa = ET.SubElement(root, "pageAccesses")
            ET.SubElement(pa, "apexPage").text = page
            ET.SubElement(pa, "enabled").text = "true"

    # tabSettings
    if tab_settings:
        for tab, vis in sorted(tab_settings):
            ts = ET.SubElement(root, "tabSettings")
            ET.SubElement(ts, "tab").text = tab
            ET.SubElement(ts, "visibility").text = vis

    # userPermissions
    if user_perms:
        for perm in sorted(user_perms):
            up = ET.SubElement(root, "userPermissions")
            ET.SubElement(up, "enabled").text = "true"
            ET.SubElement(up, "name").text = perm

    return root


def write_xml(root, filename):
    """Write XML tree to file with proper formatting."""
    rough_string = ET.tostring(root, encoding="unicode")
    parsed = minidom.parseString(rough_string)
    pretty = parsed.toprettyxml(indent="    ", encoding=None)
    # Remove the XML declaration that minidom adds (we'll add our own)
    lines = pretty.split("\n")
    lines = [l for l in lines if l.strip() and not l.startswith("<?xml")]
    content = '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(lines) + "\n"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {filename}")


def make_field_perms_edit(obj, fields):
    """Helper: create field permissions with editable=True for a list of fields on one object."""
    return [(f"{obj}.{f}", True) for f in fields]


def make_field_perms_read(obj, fields):
    """Helper: create field permissions with editable=False for a list of fields on one object."""
    return [(f"{obj}.{f}", False) for f in fields]


# ═══════════════════════════════════════════════════════════════════════════════
# PERMISSION SET DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_all():
    print("Generating permission sets...\n")

    # ── A3: Quote Lifecycle Management ────────────────────────────────────
    quote_lifecycle_fields = make_field_perms_edit("SBQQ__Quote__c", [
        "SBQQ__Status__c", "SBQQ__DocumentStatus__c", "Integration_Status__c",
        "QuoteProcuredStatus__c", "STP__c", "STP_Success_Report__c",
        "Resubmit_Flag__c", "DoResyncOutBoundcall__c",
        "AAV_Asset_Availability_Flag__c", "GR_Service_Flag__c",
        "Quote_Only__c", "Emergency_Request__c", "Troubleshoot_Emergency__c",
        # Routing/Assignment
        "Assigned_To__c", "Assing_To_Me_Action__c", "SFDC_Team__c", "SFDC_Team_User__c",
        "Is_Genesys_Required__c", "Genesys_Record_Created__c",
        # General data
        "Customer_Request_Date__c", "Duration__c", "Schedule_or_On_Call__c",
        "Onsite_Contact__c", "Location_Customer_Name__c", "Primary_Segment__c",
        "Priority__c", "Project__c", "ErrorComments__c",
        "Next_Action_Due_Date__c", "Next_Action_Start_Date__c",
        "Case__c", "Case_Type__c", "Case_Sub_Type__c", "Case_Reason__c",
        "Alternate_Description__c", "Alternate_Service_Provided__c",
        "Cancellation_Reason__c", "Case_Comments__c",
        "Acorn_integration_required__c", "Acorn_Integration_Status__c",
        "Show_Flow_Path__c", "Vendor_Commit_Date__c",
    ])

    write_xml(build_ps_xml(
        label="Quote Lifecycle Management",
        description="Create, edit, and manage quotes through their lifecycle. Covers status, routing, assignment, and general data. Excludes price fields (A1), cost fields (A2), and approval authority (A5). SoD: Cannot be combined with PS_Quote_Approval.",
        field_perms=quote_lifecycle_fields,
        object_perms=[
            {"object": "SBQQ__Quote__c", "create": True, "read": True, "edit": True},
            {"object": "SBQQ__QuoteLine__c", "create": True, "read": True, "edit": True},
            {"object": "SBQQ__ConfigurationAttribute__c", "create": True, "read": True, "edit": True, "delete": True},
            {"object": "SBQQ__ProductFeature__c", "create": True, "read": True, "edit": True, "delete": True},
            {"object": "SBQQ__ProductOption__c", "create": True, "read": True, "edit": True, "delete": True},
            {"object": "Quote_Line_History_Tracking__c", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "QuoteCreationHandler", "QuoteLineCreationHandler", "QuoteLineService", "QuoteLineServices",
            "QuoteTriggerHandler", "QuoteTriggerHelper", "QuoteLineTriggerHandler", "QuoteLineTriggerHelper",
            "QuoteSelector", "QuoteLineSelector", "QuoteLineClassificationChanges",
            "QuoteActionsController", "QuoteOnlyController", "QuoteProcurementController",
            "QuoteFavoritesController", "GetQuoteSummary", "ShowQuoteLineHistoryController",
            "AssetQuoteProcurementController", "AlternateServiceController",
            "QuoteOrderTriggerHandler", "RemovalQuoteLineHandler", "QouteValiationHandler",
            "SBQQConfigurationRuleSelector", "SBQQConfigurationRuleService", "SBQQProductOptionSelector",
            "SBQQQuoteService", "AsyncUpdateQuoteFlag", "CalculateQuotePriority",
        ],
    ), "PS_Quote_Lifecycle_Management.permissionset-meta.xml")

    # ── A5: Quote Approval ────────────────────────────────────────────────
    quote_approval_fields = (
        make_field_perms_edit("SBQQ__Quote__c", [
            "Action_Type__c", "Action_Reason__c", "Manual_Approval_Action__c",
            "Approve_NTE_Amount__c", "Pending_Information__c",
            "Special_Handling__c", "Special_Handling_Reason__c", "Special_Handling_Reason_Details__c",
        ]) +
        make_field_perms_edit("Approval_Log__c", [
            "Status__c", "Approval_Comments__c", "Decision_Date_Time__c",
            "Actual_Approver__c", "Actual_Approver_Contact__c", "Actual_Approver_Email__c",
            "Actual_External_Approver_Name__c", "Actual_Approver_Origin__c", "Actual_Approver_Title__c",
        ])
    )

    write_xml(build_ps_xml(
        label="Quote Approval",
        description="Authority to approve or decline quotes and record decisions in the Approval Log. SoD: Cannot be combined with PS_Quote_Lifecycle_Management — the person who creates/edits a quote should not approve it.",
        field_perms=quote_approval_fields,
        object_perms=[
            {"object": "SBQQ__Quote__c", "read": True, "edit": True},
            {"object": "Approval_Log__c", "create": True, "read": True, "edit": True},
        ],
        class_accesses=["QuoteApproval", "QuoteApprovalHandler", "QuoteDecline"],
    ), "PS_Quote_Approval.permissionset-meta.xml")

    # ── B1: Case Intake ───────────────────────────────────────────────────
    case_intake_fields = make_field_perms_edit("Case", [
        "Case_Type__c", "Case_Sub_Type__c", "Case_Reason__c", "Subject", "Description",
        "ContactId", "Site_Contact__c", "Site_Contact_Phone__c", "Email_Address__c",
        "Location__c", "Client__c", "Supplier__c", "AssetId",
        "Emergency__c", "Emergency_Reason__c", "Quote_Only__c",
        "Source_System__c", "Is_From_ScreenPop__c", "FlowToRun__c",
        "Service_Date__c", "Delivery_Date__c", "Service_Start_Date__c", "Service_End_Date__c",
        "Equipment_Size_Code__c", "Equipment_Type_Code__c", "Material_Type__c", "Material__c",
        "Monday__c", "Tuesday__c", "Wednesday__c", "Thursday__c",
        "Friday__c", "Saturday__c", "Sunday__c",
        "Frequency__c", "Occurrence__c", "Occurs__c",
        "Offsite_Address__c", "Offsite_Street_Address__c", "Offsite_City__c",
        "Offsite_State__c", "Offsite_Postal_Code__c",
        "Haul_Away_information__c", "Is_Haul_Away_Service__c",
        "Standard_Portable_Count__c", "Handicapped_Portable_Count__c",
        "Hand_Wash_Station_Type__c",
        "Is_the_compactor_leaking__c", "Is_the_door_closed_and_sealed__c",
        "Does_the_container_have_power__c", "Does_the_container_need_to_be_emptied__c",
        "Site_Survey_Date__c", "Reason_for_site_survey__c", "Survey_Type__c",
        "ContainerPosition__c", "Container_For__c",
        "Instructions_for_the_driver__c", "Special_Instructions__c",
        "Type_of_Delivery__c", "Type_of_Liquid__c",
        "Schedule_or_On_Call__c", "Weekly_Frequency__c", "Scheduled_Frequency__c",
        "Event_Recurrence_Interval__c", "Event_Recurrence_Type_Code__c",
        "Service_Classification__c", "Service_Occurrence_Type_Code__c",
        "Create_AM_and_PM_Pickups__c", "Multiple_Dates__c",
        "Exclude_Holidays__c", "Exclude_Saturdays__c", "Exclude_Sundays__c",
        "Same_Next_Day__c",
        "Work_Order_Instructions__c", "User_Input_Work_Order_Instructions__c",
        "System_Gen_WO_Instructions__c",
        "Is_Multiple_Asset__c", "Is_Multiple_Case_Allowed__c",
        "Is_Multiple_Case_Per_ServiceDT__c", "Is_Multivendor__c",
        "Quantity_Override__c", "Quantity_of_keys_needed__c",
        "Is_With_Lock__c", "Is_With_Wheel__c",
        "Is_Electrical_Workers__c", "Workers_Per_Shift_Count__c",
        "Client_to_meet_the_vendor_driver__c",
        "Bladder_Mount_Location__c",
        "Where_is_the_leak_coming__c",
        "Has_the_issue_been_resolved__c",
        "Temp_Asset_needed__c", "New_Asset__c",
        "Customer_Reference_Number__c", "Reference_Number__c",
        "Priority",
    ])

    write_xml(build_ps_xml(
        label="Case Intake",
        description="Create new cases and populate initial intake data. Entry-point permission for any case-handling role. Covers case creation fields, service configuration, scheduling, equipment/material selection, and site details.",
        field_perms=case_intake_fields,
        object_perms=[
            {"object": "Case", "create": True, "read": True, "edit": True},
            {"object": "SBS_Case_Asset__c", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "CaseController", "CustomCaseCreationCntrlr", "CaseCreation", "CaseUpdateHandler",
            "CaseTriggerHandler", "CaseTriggerHelper", "CaseDetailHelper", "CustomCaseHighlightPanelCntrl",
            "CaseCustomLookUpController", "DuplicateCheckOnCaseController", "GetCaseInformation",
            "ContactSearchandCreate", "ScreenpopController", "Screenpop",
            "HaulAwayService", "BalePickupCaseService", "ETAWindowController",
            "IntakeProcessAuraHandler", "ProgressCaseComponentController",
        ],
        user_perms=["ActivitiesAccess"],
    ), "PS_Case_Intake.permissionset-meta.xml")

    # ── B2: Case Lifecycle Management ─────────────────────────────────────
    case_lifecycle_fields = make_field_perms_edit("Case", [
        "Status", "Case_Sub_Status__c", "Approval_Status__c", "Authorization_Status__c",
        "Current_Milestone__c", "Milestone_Entry_Time__c", "Milestone_Warning_1__c",
        "Close_Case_Reason__c", "Close_Irrelevant_Case__c", "Close_Pickup_Case__c",
        "isApproved__c", "isRejected__c", "isWorkOrderCreated__c",
        "Master_Intake_Complete__c", "VCC_Complete__c", "BackOffice_Case__c",
        "PSI_Override_Reason__c", "PSI_Required__c", "PSI__c",
        "Availability_Checked__c", "Availability_Confirmed__c",
        "CheckReassignment__c", "Last_Agent_ID__c", "Last_Agent_Id_ForTaskAssignment__c",
        # Communication
        "Case_Comments__c", "PSI_Comments__c", "EmailTemplateAdditionalComments__c",
        "Authorization_Notes__c", "Authorization_Channel__c",
        # Flags
        "Is_ByPassWO__c", "Bypass_WO_Duplicate__c", "Is_Clone__c",
        "Is_Info_Task_Created__c", "Is_Monitored__c",
        "Is_MultiCase_TaskBundling__c", "Is_PSI_Required__c",
        "Is_Recreated__c", "Manual_Invocation__c",
        "Send_Autoresoponse__c", "Suppress_Auto_Response__c",
        "Integrate_with_Acorn__c",
        "Acorn_Issue_Id__c", "Acorn_Update_Datetime__c",
    ])

    write_xml(build_ps_xml(
        label="Case Lifecycle Management",
        description="Progress cases through status changes, milestone updates, approval workflows, and closure. Excludes financial fields (B3) and SLA override authority (B4). SoD: Cannot be combined with PS_Case_Financial in roles requiring financial segregation.",
        field_perms=case_lifecycle_fields,
        object_perms=[
            {"object": "Case", "read": True, "edit": True},
        ],
        class_accesses=[
            "CaseUpdateHandler", "CaseApprovalHandler", "CaseHistoryTrackerTriggerHandler",
            "CommentController", "CustomCommentController", "CaseCommentsControllerExtension",
            "CreateCaseHistory", "CloseAcornTicket", "ReopenAcornTicket", "ReassignAcornTicket",
            "ConcatenateTaskDetailForAcorn", "AcornController", "AcornCaseDetailsResource",
            "ValidateTaskToPopMessage", "MultiCaseTaskPopuCntrlr", "CaseDetailCardController",
            "CommunicationChannelViewController", "GetChildCase",
        ],
    ), "PS_Case_Lifecycle_Management.permissionset-meta.xml")

    # ── B3: Case Financial ────────────────────────────────────────────────
    case_financial_fields = make_field_perms_edit("Case", [
        "PurchaseOrder_Number__c", "PurchaseOrder_Required__c", "PurchaseOrder_Override_Reason__c",
        "Override_PO_Create_Task__c",
        "Invoice_Number__c", "Disputed_Amount__c",
        "Chargeable__c", "Is_Haul_Away_Service__c", "Haul_Away_Service_Booked__c",
        "SalesMeet_Price__c", "No_Price__c", "Price_Quote_Identifier__c",
        "Quote_Eligibility_Result__c", "CPQ_New_Service__c",
        "Cost_of_bale_wire_per_unit__c", "Quantity_of_bale_wire_needed_per_cost__c",
        "Documentation_of_cost__c",
        "IsOpportunity_Created__c",
        "Locally_Billed__c",
    ])

    write_xml(build_ps_xml(
        label="Case Financial",
        description="Modify billing, pricing, PO, and charge-related fields on cases. Restricted to roles with financial authority. SoD: Cannot be combined with PS_Case_Lifecycle_Management in roles where financial segregation is required.",
        field_perms=case_financial_fields,
        object_perms=[
            {"object": "Case", "read": True, "edit": True},
        ],
        class_accesses=["BillingService"],
    ), "PS_Case_Financial.permissionset-meta.xml")

    # ── B4: Case SLA Override ─────────────────────────────────────────────
    case_sla_fields = make_field_perms_edit("Case", [
        "SLA_Service_Date__c", "SLA_Service_Date_Time__c", "SLA_Service_DateTime__c",
        "SLA_Date_Text__c",
        "SLA_Override_Reason__c", "SLA_Override_Comment__c", "SLA_Violation__c",
        "Service_Date_from_Local_Time__c",
        "Proposed_Service_Date__c",
    ])

    write_xml(build_ps_xml(
        label="Case SLA Override",
        description="Override SLA dates and service date calculations. Privileged action restricted to supervisors/leads who are not the case owner. SoD: Should not be held by case agents who also have B1/B2.",
        field_perms=case_sla_fields,
        object_perms=[
            {"object": "Case", "read": True, "edit": True},
        ],
        class_accesses=[
            "CaseSLAEntitlementUTIL", "CaseEntitlement", "StartDateManagement",
            "EndDateHandler", "GetSLAInformation",
        ],
    ), "PS_Case_SLA_Override.permissionset-meta.xml")

    # ── B5: Case Read Only ────────────────────────────────────────────────
    write_xml(build_ps_xml(
        label="Case Read Only",
        description="View-only access to all case data including financial and SLA fields. No edit permissions granted.",
        object_perms=[
            {"object": "Case", "read": True},
            {"object": "SBS_Case_Asset__c", "read": True},
        ],
        class_accesses=[
            "CaseDetailHelper", "CustomCaseHighlightPanelCntrl", "CaseDetailCardController",
            "GetCaseInformation", "CommunicationChannelViewController",
        ],
    ), "PS_Case_Read_Only.permissionset-meta.xml")

    # ── C1: Task Assignment ───────────────────────────────────────────────
    write_xml(build_ps_xml(
        label="Task Assignment",
        description="Create, assign, and reassign tasks. Includes setting task owner, team assignment, and initial scheduling. Does not include completion/outcome authority (C2).",
        object_perms=[
            {"object": "Task", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "TaskTriggerHandler", "TaskTriggerHelper",
            "AssignToMeCntrl", "ChangeTaskAssignmentcntrl",
            "TaskRelatedListAura", "TaskTableWrapper", "TaskPopUpMessageController",
            "MultiCaseTaskPopuCntrlr", "CreatePendingInformationTask", "GenTaskController",
            "MyTaskListController", "ServiceIssueTaskController",
            "GetTaskRecursionCheck", "PutTaskRecursionCheck",
        ],
        user_perms=["EditTask", "EditEvent", "ActivitiesAccess"],
    ), "PS_Task_Assignment.permissionset-meta.xml")

    # ── C2: Task Completion ───────────────────────────────────────────────
    write_xml(build_ps_xml(
        label="Task Completion",
        description="Complete tasks by setting outcomes, updating result fields, and closing. Separated from assignment (C1) because in audit-sensitive workflows the assigner should not record the outcome.",
        object_perms=[
            {"object": "Task", "read": True, "edit": True},
        ],
        class_accesses=[
            "AsyncCompleteTask", "AttemptTasksCreationBatch",
            "SendEmailForNotifyCustomerDelayTask",
        ],
    ), "PS_Task_Completion.permissionset-meta.xml")

    # ── C3: Task Read Only ────────────────────────────────────────────────
    write_xml(build_ps_xml(
        label="Task Read Only",
        description="View-only access to all task data. No create or edit permissions.",
        object_perms=[
            {"object": "Task", "read": True},
        ],
        class_accesses=[
            "TaskRelatedListAura", "TaskTableWrapper", "MyTaskListController",
        ],
    ), "PS_Task_Read_Only.permissionset-meta.xml")

    # ── D1: WorkOrder Creation ────────────────────────────────────────────
    wo_general_fields = make_field_perms_edit("WorkOrder", [
        "Account_Number__c", "Acorn_Contact_Id__c", "Acorn_Location_ID__c",
        "Acorn_Issue_Id__c", "Acorn_WO_No__c", "Acorn_WorkOrder_Id__c",
        "Acorn_WorkOrder_Number__c", "Acorn_SID__c", "Acorn_SID_Text__c",
        "Acorn_Update_Datetime__c", "Acorn_Purchase_Order_Number__c",
        "Case_Origin__c", "Case_Reason__c", "Case_Subtype__c", "Case_Type__c",
        "Channel__c", "Client__c", "Company_Category__c",
        "Container_Position__c", "Customer_Interaction_ID__c", "Customer_Location__c",
        "Description__c", "Dispatch_Email__c",
        "Exception_Description__c", "Exception_Reason__c", "IVR_Specific_Exception_Reason__c",
        "Instructions__c", "Integration_Eligible__c", "Integration_Status__c", "Interface_Triggered__c",
        "Latitude__c", "Longitide__c",
        "Onsite_Contact__c", "Onsite_Contact_Phone__c",
        "Profile_Description__c", "Profile_Generator__c", "Profile_Number__c", "Profile_Number_Case__c",
        "Profile_Purchase_Order__c",
        "Status_Case_Subtype__c", "Tonnage__c", "Vehicle_Number__c",
        "Vendor_ID__c", "Vendor_Service_Status__c",
        "WO_Accepted_Rejected_Comments__c", "WO_Quantity__c",
        "Send_Work_Order_to_Vendor__c", "Send_Status__c", "Sent_To__c",
        "AssetMaterial__c", "Asset_Material__c", "Asset_Position__c",
        "Fast_Lane_Ticket__c", "Is_Bypass__c", "Is_Override_Duplicate__c",
        "MAS_Case__c", "MAS_Ticket__c", "Manifest_Number__c",
        "No_Completion_Evidence__c", "No_Route_Evidence__c", "No_Schedule_Evidence__c",
        "PSI__c", "PSI_Bypass_Reason__c",
        "Quote_Order__c", "Rejection_Reason__c",
        "Verify_Service_Task__c", "Vendor_Account_Id__c", "Vendor_Exception_Reason__c",
    ]) + make_field_perms_edit("WorkOrderLineItem", [
        "Asset_Service_Type__c", "Measurement_Unit__c", "Occurrence_Type__c",
        "Quantity_Source__c", "Reason_Code__c", "Reason_Description__c",
        "Reported_Quantity_Source__c", "Service_Quantity__c", "Service_Type__c",
        "Tonnage_Date__c", "Tonnage_User__c", "Tons__c",
        "Acorn_SBID__c", "Acorn_SCOD__c", "Acorn_Update_Datetime__c", "Acorn_WOC__c",
        "SBID_text__c", "SCOD_text__c",
        "Duration__c", "Quantity__c", "Reported_Quantity__c",
        "Purchase_Order_Number__c", "Vendor_Account_Id__c",
        "Event_Tonnage__c", "Is_Quantity_Estimated__c", "PSI_Reading__c",
    ])

    write_xml(build_ps_xml(
        label="WorkOrder Creation",
        description="Create and edit work orders and line items. Covers general WO data, Acorn integration, vendor references, and line item details. Excludes cost/financial fields (D2).",
        field_perms=wo_general_fields,
        object_perms=[
            {"object": "WorkOrder", "create": True, "read": True, "edit": True},
            {"object": "WorkOrderLineItem", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "WorkOrderController", "WorkOrderTriggerHandler", "WorkOrderTriggerHelper",
            "WorkOrderLineItemTriggerHandler", "WorkOrderLineItemTriggerHelper",
            "MultipleWorkorderController", "UpdateWorkOrder", "GetWorkOrderPDFCntrlr",
            "AcornWODetailsController", "WODataWrapper",
        ],
    ), "PS_WorkOrder_Creation.permissionset-meta.xml")

    # ── D2: WorkOrder Cost Management ─────────────────────────────────────
    wo_cost_fields = make_field_perms_edit("WorkOrder", [
        "Dry_Run_Cost__c", "Dry_Run_Cost_NOT_IN_USE__c", "Dry_Run_Cost_in_Currency__c",
        "Dry_Run_Price__c", "Dry_Run_Price_in_Currency__c",
        "Negative_HOC__c", "Marked_as_Dry_Run__c",
        "Dry_Run_Description__c", "Dry_Run_Root_Cause__c",
    ]) + make_field_perms_edit("WorkOrderLineItem", [
        "Cost_Model_Type__c", "Cost_Total_Tax__c", "Cost__c",
        "New_Client_Price__c", "Original_Client_Price__c",
        "Is_Rebate_Pricing_Needed__c", "Is_Rebate_Pricing_Pending__c",
    ])

    write_xml(build_ps_xml(
        label="WorkOrder Cost Management",
        description="Modify cost and financial fields on Work Orders and Line Items. Restricted to vendor relations / financial roles. SoD: Should not be held alongside D3 (Scheduling) in roles where vendor financial and scheduling duties must be separated.",
        field_perms=wo_cost_fields,
        object_perms=[
            {"object": "WorkOrder", "read": True, "edit": True},
            {"object": "WorkOrderLineItem", "read": True, "edit": True},
        ],
        class_accesses=["WorkOrderWebservices", "BillingService"],
    ), "PS_WorkOrder_Cost_Management.permissionset-meta.xml")

    # ── D3: WorkOrder Scheduling ──────────────────────────────────────────
    wo_sched_fields = make_field_perms_edit("WorkOrder", [
        "Service_Date__c", "Original_Expected_Date__c", "Expected_Service_Date__c",
        "Actual_Service_Date__c", "Rescheduled_Date__c",
        "Accept_Date__c", "Decline_Date__c", "Effective_Date__c",
        "Pickup_DateTime__c", "Return_DateTime__c",
        "SLA_Service_Date_Time__c", "Sent_Date_Time__c",
        "Service_Exception_Received_Date_Time__c",
        "Back_Dated_WO__c", "Local_Time__c",
        "Accept_User_Id__c", "Accept_User_name__c",
        "Decline_User__c", "Decline_User_Name__c",
        "Status_Send_Status__c",
    ])

    write_xml(build_ps_xml(
        label="WorkOrder Scheduling",
        description="Manage service dates, scheduling, and vendor assignment on Work Orders. SoD: In vendor management scenarios, may need to be separated from D2 (Cost Management).",
        field_perms=wo_sched_fields,
        object_perms=[
            {"object": "WorkOrder", "read": True, "edit": True},
        ],
        class_accesses=[
            "ServiceSchedulerCtrl", "WorkOrderReportCtrl", "ETAWindowController",
        ],
    ), "PS_WorkOrder_Scheduling.permissionset-meta.xml")

    # ── D4: WorkOrder Read Only ───────────────────────────────────────────
    write_xml(build_ps_xml(
        label="WorkOrder Read Only",
        description="View-only access to all work order and line item data. No create or edit permissions.",
        object_perms=[
            {"object": "WorkOrder", "read": True},
            {"object": "WorkOrderLineItem", "read": True},
        ],
        class_accesses=[
            "AcornWODetailsController", "WODataWrapper", "GetWorkOrderPDFCntrlr",
        ],
    ), "PS_WorkOrder_Read_Only.permissionset-meta.xml")

    # ── E1: Asset View ────────────────────────────────────────────────────
    write_xml(build_ps_xml(
        label="Asset View",
        description="Read-only access to asset records with display capabilities.",
        object_perms=[
            {"object": "Asset", "read": True},
            {"object": "SBS_Case_Asset__c", "read": True},
        ],
        class_accesses=[
            "AssetHeadersForCaseController", "DisplayCaseAssetController", "CaseAssetController",
            "assetCustomTreeGridController", "LocationContainerController",
            "AssetQuerySelector",
        ],
    ), "PS_Asset_View.permissionset-meta.xml")

    # ── E2: Asset Financial ───────────────────────────────────────────────
    asset_fin_fields = make_field_perms_edit("Asset", [
        # Cost fields
        "Cost__c", "Cost_Currency__c", "Cost_Center__c",
        "Cost_Increment_1__c", "Cost_Increment_2__c", "Cost_Increment_3__c", "Cost_Increment_4__c",
        "Cost_Minimum_Quantity__c", "Cost_Model_Type__c",
        "Cost_Price_1__c", "Cost_Price_2__c", "Cost_Price_3__c", "Cost_Price_4__c",
        "Cost_Tax_Inclusive__c", "Cost_Total_Tax__c", "Cost_Unit__c",
        "Cost_UpTo_1__c", "Cost_UpTo_2__c", "Cost_UpTo_3__c", "Cost_UpTo_4__c",
        "Bypass_Cost_Grid__c",
        # Price fields
        "Price__c", "Price_Currency__c",
        "Price_Increment_1__c", "Price_Increment_2__c", "Price_Increment_3__c", "Price_Increment_4__c",
        "Price_Minimum_Quantity__c", "Price_Model_Type__c",
        "Price_Price_1__c", "Price_Price_2__c", "Price_Price_3__c", "Price_Price_4__c",
        "Price_Tax_Inclusive__c", "Price_Total_Tax__c", "Price_Unit__c",
        "Price_UpTo_1__c", "Price_UpTo_2__c", "Price_UpTo_3__c", "Price_UpTo_4__c",
        "EDI_Price_Source__c",
        # SBQQ fields
        "SBQQ__AdditionalDiscountAmount__c", "SBQQ__BillingFrequency__c", "SBQQ__BillingType__c",
        "SBQQ__ChargeType__c", "SBQQ__Discount__c", "SBQQ__DiscountSchedule__c",
        "SBQQ__DiscountScheduleType__c", "SBQQ__DistributorDiscount__c",
        "SBQQ__ListPrice__c", "SBQQ__MarkupAmount__c", "SBQQ__MarkupRate__c",
        "SBQQ__OptionDiscount__c", "SBQQ__OptionDiscountAmount__c",
        "SBQQ__OriginalUnitCost__c", "SBQQ__PartnerDiscount__c",
        "SBQQ__PriceDimension__c", "SBQQ__PricingMethod__c",
        "SBQQ__RegularPrice__c", "SBQQ__RenewalUpliftRate__c",
        "SBQQ__UnitCost__c",
        "Contract_Notes__c",
        "Is_Locally_Billed__c", "Has_InvoiceReadytoBillStatus__c",
    ])

    write_xml(build_ps_xml(
        label="Asset Financial",
        description="Modify financial fields on assets — cost, discount, pricing model, SBQQ billing fields. SoD: Should not overlap with E4 (Configuration) in roles where financial and operational duties are separated.",
        field_perms=asset_fin_fields,
        object_perms=[
            {"object": "Asset", "read": True, "edit": True},
        ],
    ), "PS_Asset_Financial.permissionset-meta.xml")

    # ── E4: Asset Configuration ───────────────────────────────────────────
    asset_config_fields = make_field_perms_edit("Asset", [
        # Equipment/Container/Material
        "Equipment_Type__c", "Equipment_Size__c", "Equipment_Owner__c",
        "Container_Position__c", "Dumpster_Style__c", "Dumpster_Service_Style__c",
        "Material_Type__c", "Material_Grade__c", "Material_Grade_Code__c", "Material_Prompt_ID__c",
        "CPQ_Material__c", "CPQ_Product__c",
        "Service_Type__c", "Category__c",
        "Location__c", "Location_Code__c",
        # Schedule/Recurrence
        "Duration__c", "Frequency__c", "Every__c", "Occurrence__c", "Occurs__c",
        "Schedule_Type__c", "Schedule__c", "Schedule_A_Override__c", "Send_Schedule_A__c",
        "Monday__c", "Monday_AM__c", "Monday_PM__c", "Monday_Frequency__c",
        "Tuesday__c", "Tuesday_AM__c", "Tuesday_PM__c", "Tuesday_Frequency__c",
        "Wednesday__c", "Wednesday_AM__c", "Wednesday_PM__c", "Wednesday_Frequency__c",
        "Thursday__c", "Thursday_AM__c", "Thursday_PM__c", "Thursday_Frequency__c",
        "Friday__c", "Friday_AM__c", "Friday_PM__c", "Friday_Frequency__c",
        "Saturday__c", "Saturday_AM__c", "Saturday_PM__c", "Saturday_Frequency__c",
        "Sunday__c", "Sunday_AM__c", "Sunday_PM__c", "Sunday_Frequency__c",
        "Weekly_Frequency__c", "Monthly_Frequency__c",
        "Month_Relative__c", "Month_Relative_Interval__c",
        "On_Date__c", "On_Day__c", "On_Day1__c", "On_Day2__c", "On_Day3__c",
        "On_the__c", "Of_Day__c", "Of_Every__c", "Of_Every1__c", "Of_Every2__c", "Of_Every3__c",
        "Of_Month__c",
        "Time_of_Day_AM__c", "Time_of_Day_PM__c", "Required_Time_of_Day__c",
        "Exclude_Holidays__c", "Exclude_Saturdays__c", "Exclude_Sundays__c",
        # General config
        "Occurrence_Type__c", "Active__c", "Is_Active__c",
        "Start_Date__c", "End_Date__c", "End_Dated_Asset__c",
        "Generate_Service_Events__c", "Is_Core_Service__c",
        "Is_Hold_Until_Posted__c", "Is_Self_Service__c",
        "GateCode__c", "GL_Code__c", "Restriction__c", "Sensitivity_Code__c",
        "Vendor_Account_Number__c", "Vendor_BU__c", "Vendor_ID__c", "Vendor_Service_Number__c",
        "Supplier__c", "Market_Area__c",
        "Project_Code__c", "Project__c",
        "Quantity__c", "Core_Quantity__c", "Core_Schedule__c",
    ])

    write_xml(build_ps_xml(
        label="Asset Configuration",
        description="Modify equipment type, container details, material codes, service schedule, and location configuration on assets. SoD: Should not overlap with E2 (Financial) in roles where financial and operational duties are separated.",
        field_perms=asset_config_fields,
        object_perms=[
            {"object": "Asset", "read": True, "edit": True},
        ],
        class_accesses=[
            "AssetTriggerHandler", "AssetTriggerHelper", "updateAcornAssetLocation",
            "ProjectCodeTriggerHandler", "ProjectCodeTriggerHelper", "ProjectCodeActiveChecker",
        ],
    ), "PS_Asset_Configuration.permissionset-meta.xml")

    # ── G3: Approval Decision ─────────────────────────────────────────────
    approval_fields = make_field_perms_edit("Approval_Log__c", [
        "Status__c", "Approval_Comments__c", "Decision_Date_Time__c",
        "Actual_Approver__c", "Actual_Approver_Contact__c", "Actual_Approver_Email__c",
        "Actual_External_Approver_Name__c", "Actual_Approver_Origin__c", "Actual_Approver_Title__c",
    ])

    write_xml(build_ps_xml(
        label="Approval Decision",
        description="Make approval decisions — approve, reject, request info. Record the decision in the Approval Log. SoD: Cannot be combined with G1 (Rule Administration) or G2 (Approver Configuration).",
        field_perms=approval_fields,
        object_perms=[
            {"object": "Approval_Log__c", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "CaseApprovalHandler", "QuoteApprovalHandler", "QuoteApproval",
            "QuoteDecline", "UpdateBrApprovalBatch",
        ],
    ), "PS_Approval_Decision.permissionset-meta.xml")

    # ── G4: NTE Approval ──────────────────────────────────────────────────
    nte_fields = make_field_perms_edit("SBQQ__Quote__c", [
        "Approve_NTE_Amount__c", "is_NTE_Quote__c",
    ])

    write_xml(build_ps_xml(
        label="NTE Approval",
        description="Approve Not-To-Exceed (NTE) amounts on quotes. Financial approval authority that should be held by a separate authority from general approval decision-making in high-value scenarios.",
        field_perms=nte_fields,
        object_perms=[
            {"object": "SBQQ__Quote__c", "read": True, "edit": True},
        ],
        class_accesses=[
            "NTEApprovalRuleHelper", "NTEBRRulesModalCtrl", "GetBRQuotePriorityNTECtrl",
        ],
    ), "PS_NTE_Approval.permissionset-meta.xml")

    # ── G5: Business Rule Read Only ───────────────────────────────────────
    write_xml(build_ps_xml(
        label="Business Rule Read Only",
        description="View-only access to business rules, service approvers, approval logs, and out-of-office records. No edit permissions.",
        object_perms=[
            {"object": "Business_Rule__c", "read": True},
            {"object": "Service_Approver__c", "read": True},
            {"object": "Approval_Log__c", "read": True},
            {"object": "Out_of_Office__c", "read": True},
        ],
        class_accesses=[
            "AllRulesModalController", "CaseRulesModalCtrl",
        ],
    ), "PS_Business_Rule_Read_Only.permissionset-meta.xml")

    # ── H1: Account Management ────────────────────────────────────────────
    acct_general_fields = make_field_perms_edit("Account", [
        "Customer_ID__c", "Customer_Code__c", "Customer_Location_Code__c",
        "Common_Name__c", "DBA_Names__c", "Previous_Name__c",
        "Business_Type__c", "Company_Category__c", "Category__c",
        "Status__c", "Market_Area__c", "Market_Area_Override__c", "Market_Area_VID__c",
        "Location_Type__c", "Location_Code__c", "Division__c",
        "Address__c", "Address_Validated__c", "Ignore_Address_Validation__c",
        "County__c", "Geography__c",
        "Phone", "Phone_Extension__c", "Fax", "Email__c",
        "Acorn_Account_Id__c", "Acorn_Company_Status_Id__c", "Acorn_Company_Type_Id__c",
        "Acorn_Location_Code__c", "Acorn_Location_Id__c", "Acorn_Location_Notes__c",
        "Acorn_Parent_Company_Id__c", "Acorn_Update_DT__c",
        "Primary_Segment__c", "Secondary_Segment__c",
        "Brand__c", "Brand_Text__c", "Site",
        "Is_Portal_Customer__c", "Portal_Name__c",
        "Is_Rollup_Client__c", "Centrally_Controlled__c", "Centrally_Serviced__c",
        "Communication_Channel_Preferences__c",
        "Effective_Date__c",
    ]) + make_field_perms_edit("Account_Title__c", [
        # Account_Title__c only has 4 fields - all general
    ])

    write_xml(build_ps_xml(
        label="Account Management",
        description="Edit general account data — names, addresses, location codes, market areas, operational configuration. Excludes financial configuration fields (H2). SoD: Cannot be combined with PS_Account_Financial_Configuration in roles where financial config must be authorized separately.",
        field_perms=acct_general_fields,
        object_perms=[
            {"object": "Account", "read": True, "edit": True},
            {"object": "Account_Title__c", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "AccountContactRelationHandler", "AccountContactRelationHelper",
            "AccountTitleTriggerHandler", "AccountTitleTriggerHelper",
            "AcornCompanyController", "AcornCompanyDetails",
            "AccountTeamMemberUIController", "AccountTeamMemberQueryAction", "HoverOverCardsCntrl",
        ],
    ), "PS_Account_Management.permissionset-meta.xml")

    # ── H2: Account Financial Configuration ───────────────────────────────
    acct_fin_fields = make_field_perms_edit("Account", [
        "Billing_Model__c", "Billing_Schedule__c", "Billing_Window__c", "Billing_Date__c",
        "Invoice_Method__c", "Invoice_Schedule__c",
        "PO_Required__c", "Federal_Tax_Id__c", "Tax_Classification__c",
        "Payment_Terms__c", "Payment_Terms_Type_II__c", "Payment_Methods__c",
        "Deposit_Required__c", "Prepayment_Required__c",
        "Permit_Fee_Required__c",
        "A_R_Balance__c", "GL_Account__c",
        "Bill_Audit_Threshold_Type__c", "Bill_Audit_Threshold_Value__c",
        "Bill_By_Recon__c", "Bill_by_Recon_Effective_Date__c",
        "Require_Billing_Audit__c",
        "Enrolled_in_Premium_Delivery_Service__c",
        "SBQQ__TaxExempt__c",
        "Local_Billing_Allowed__c",
    ])

    write_xml(build_ps_xml(
        label="Account Financial Configuration",
        description="Modify billing model, PO requirements, payment terms, tax settings, and other financial configuration on accounts. SoD: Cannot be combined with PS_Account_Management in roles where financial configuration must be authorized separately.",
        field_perms=acct_fin_fields,
        object_perms=[
            {"object": "Account", "read": True, "edit": True},
        ],
    ), "PS_Account_Financial_Configuration.permissionset-meta.xml")

    # ── I1: Genesys Routing View ──────────────────────────────────────────
    genesys_read_fields = make_field_perms_read("Genesys_Routing__c", [
        "Action__c", "Action_Reason__c", "EmailFrom__c", "EmailSubject__c", "EmailTo__c",
        "Email_Message_Id__c", "Integrate_with_Genesys_Routing__c", "LastAgentId__c",
        "MediaType__c", "Quote__c",
        "SFDCAcctID__c", "SFDCAcctLocation__c", "SFDCAcctLocationTimeZone__c", "SFDCAcctSegment__c",
        "SFDCCaseNumber__c", "SFDCCaseReason__c", "SFDCCaseRefNo__c",
        "SFDCCaseSubCaseType__c", "SFDCCaseType__c",
        "SFDCChildVendorAcctNo__c", "SFDCChildVendorName__c",
        "SFDCContactSegment__c", "SFDCFunction__c",
        "SFDCIsAcctVendor__c", "SFDCIsEmailNew__c",
        "SFDCObjName__c", "SFDCObjRecordID__c", "SFDCObjType__c",
        "SFDCParentVendorAcctNo__c", "SFDCParentVendorName__c",
        "SFDCRecordType__c", "SFDCRouteEndTime__c", "SFDCRoutePriority__c", "SFDCRouteStartTime__c",
        "SFDCServiceFlag__c", "SFDCTaskCaseId__c", "SFDCTaskDescCode__c",
        "SFDCTaskDescription__c", "SFDCTaskDueDateTime__c",
        "SFDCVendorPreferredChannel__c",
        "Send_to_Genesys_Time__c", "Sys_Created_From__c",
    ])

    write_xml(build_ps_xml(
        label="Genesys Routing View",
        description="View Genesys routing records and integration status. Read-only access to all 42 routing fields.",
        field_perms=genesys_read_fields,
        object_perms=[
            {"object": "Genesys_Routing__c", "read": True},
        ],
        class_accesses=[
            "IVRServiceStatusWebService", "IVRServiceStatusWebService_V1",
            "IVRServiceStatusETA", "IVRServiceStatusETA_V1", "IVRUtility",
            "GetIVRCasePrompt", "IVRContainerServices", "IVRExitController",
        ],
    ), "PS_Genesys_Routing_View.permissionset-meta.xml")

    # ── J1: Communication Send ────────────────────────────────────────────
    comm_fields = make_field_perms_edit("Communication_Channel__c", [
        "AccountId__c", "Acorn_Channel_Id__c", "Acorn_Last_Updated_Date__c",
        "Channel_Extension__c", "Channel_Function__c", "Channel_Type__c",
        "Channel_Value__c", "Notes__c", "isActive__c",
    ])

    write_xml(build_ps_xml(
        label="Communication Send",
        description="Send emails, manage email messages, and create communication channel records.",
        field_perms=comm_fields,
        object_perms=[
            {"object": "Communication_Channel__c", "create": True, "read": True, "edit": True},
            {"object": "EmailMessage", "create": True, "read": True, "edit": True},
        ],
        class_accesses=[
            "EmailService", "EmailMessageCreation", "EmailMessageHelper",
            "EmailMessageTriggerHandler", "EmailMessageTriggerHelper", "FetchEmailMessages",
            "InvocableFlowEmail", "NotifyCustomerOfDelayEmailController",
            "NotificationTrackingController", "NotifTrackingWrapper",
            "SendAlert", "SendBusinessRuleData", "SendEmailToWMVendorCtrl",
            "AutoSendEmailToServiceApprovers", "SendErrorNotificationOnJobFailure",
            "ChatTranscriptPdfCtrl",
        ],
        user_perms=["EmailSingle"],
    ), "PS_Communication_Send.permissionset-meta.xml")

    # ── J2: Communication Read Only ───────────────────────────────────────
    comm_read_fields = make_field_perms_read("Communication_Channel__c", [
        "AccountId__c", "Acorn_Channel_Id__c", "Acorn_Last_Updated_Date__c",
        "Channel_Extension__c", "Channel_Function__c", "Channel_Type__c",
        "Channel_Value__c", "Notes__c", "isActive__c",
    ])

    write_xml(build_ps_xml(
        label="Communication Read Only",
        description="View communication history, email messages, and channel records. No send or edit permissions.",
        field_perms=comm_read_fields,
        object_perms=[
            {"object": "Communication_Channel__c", "read": True},
            {"object": "EmailMessage", "read": True},
        ],
        class_accesses=[
            "CommunicationChannelViewController", "FetchEmailMessages",
            "NotificationTrackingController",
        ],
    ), "PS_Communication_Read_Only.permissionset-meta.xml")

    print(f"\nDone! Generated 25 permission set files in:\n  {OUTPUT_DIR}")


if __name__ == "__main__":
    create_all()
