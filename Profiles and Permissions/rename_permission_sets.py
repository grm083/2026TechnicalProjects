#!/usr/bin/env python3
"""
Rename existing permission sets to follow the PS_ naming convention
with more descriptive titles. Creates new files with updated labels
and descriptions. Old files are preserved for reference/destructive changes.
"""

import os
import re
import shutil

PS_DIR = "/home/user/2026TechnicalProjects/force-app/main/default/permissionsets"

# (old_filename, new_filename, new_label, updated_description_or_None)
RENAMES = [
    # ── Genuinely more descriptive renames ──────────────────────────────
    (
        "Price_Accessibility_Permission_Set",
        "PS_Quote_Price_Accessibility",
        "Quote Price Accessibility",
        "Modify price-related fields on Quotes and Quote Lines. SoD: Cannot be combined with PS_Quote_Cost_Accessibility (A2) — a user who controls both price and cost can manipulate margins without oversight.",
    ),
    (
        "Cost_Accessibility_Permission_Set",
        "PS_Quote_Cost_Accessibility",
        "Quote Cost Accessibility",
        "Modify cost-related fields on Quotes and Quote Lines. SoD: Cannot be combined with PS_Quote_Price_Accessibility (A1) — a user who controls both price and cost can manipulate margins without oversight.",
    ),
    (
        "CPQReadOnly",
        "PS_Quote_Read_Only",
        "Quote Read Only",
        "View-only access to all quote and quote line data including price and cost fields. No edit permissions granted.",
    ),
    (
        "MAS_Permissionset",
        "PS_Quote_MAS_Integration",
        "Quote MAS Integration",
        "Manage Material Automated Services (MAS) integration fields on quote lines.",
    ),
    (
        "Pricing_Access",
        "PS_Pricing_Request_Execution",
        "Pricing Request Execution",
        "Create and process pricing requests through the full workflow including API integration. SoD: Cannot be combined with PS_STP_Administration — setting eligibility criteria and executing pricing must be separate.",
    ),
    (
        "Pricing_Read_Only",
        "PS_Pricing_Request_Read_Only",
        "Pricing Request Read Only",
        "View-only access to pricing request data. No create or edit permissions.",
    ),
    (
        "Task_Genesys_Routing_Permission",
        "PS_Genesys_Routing_Control",
        "Genesys Routing Control",
        "Create and manage Genesys routing records and task routing configuration.",
    ),
    (
        "Reports_and_Dashboards_Super_User",
        "PS_Report_Creator",
        "Report Creator",
        "Create and customize reports and dashboards.",
    ),
    (
        "Merge_Access_for_Non_Admin_Users",
        "PS_Contact_Merge",
        "Contact Merge",
        "Delete and merge duplicate contact records. Destructive operation requiring separate authorization. SoD: Must be separate from PS_Contact_Management — creating contacts and merging/deleting them should require different authority.",
    ),
    (
        "Knowledge_Manager_User",
        "PS_Knowledge_Management",
        "Knowledge Management",
        "Create, edit, and publish knowledge articles.",
    ),
    (
        "MAA_Admin_Panel_Team",
        "PS_Market_Area_Alerts_Admin",
        "Market Area Alerts Admin",
        "Configure market area alert settings.",
    ),
    (
        "Digital_Transformation_Time_Tacking",  # Fixes the typo!
        "PS_Digital_Transformation_Tracking",
        "Digital Transformation Tracking",
        "Time tracking for digital transformation projects.",
    ),
    (
        "Account_Notification_Maintenance",
        "PS_Notification_Preferences",
        "Notification Preferences",
        "Manage account-level notification preferences.",
    ),
    (
        "Project_Services_Project_Management",
        "PS_Project_Services",
        "Project Services",
        "Manage project codes and project-level business rules.",
    ),

    # ── Consistency renames (PS_ prefix + minor cleanup) ────────────────
    (
        "Reports_and_Dashboards_Administrator",
        "PS_Report_Administrator",
        "Report Administrator",
        "Full report and dashboard administration including folder management and publishing.",
    ),
    (
        "Customer_Service_Reporting_User",
        "PS_Customer_Service_Reporting",
        "Customer Service Reporting",
        "Customer service supervisor reporting and dashboard access.",
    ),
    (
        "Escalation_Maintenance_Permissions",
        "PS_Escalation_Maintenance",
        "Escalation Maintenance",
        "Manage vendor escalation contacts and categories.",
    ),
    (
        "Manage_Premium_Deliveries",
        "PS_Premium_Delivery_Management",
        "Premium Delivery Management",
        "Manage premium delivery service enrollment on accounts.",
    ),
    (
        "View_Setup_and_Configuration",
        "PS_View_Setup",
        "View Setup",
        "View-only access to org setup and configuration.",
    ),
    (
        "STP_Administration",
        "PS_STP_Administration",
        "STP Administration",
        "Configure STP eligibility criteria and manage exception logs. SoD: Cannot be combined with PS_Pricing_Request_Execution — setting criteria and executing pricing must be separate.",
    ),
    (
        "Governance_Team",
        "PS_Governance_Team",
        "Governance Team",
        None,  # Keep existing description
    ),
    (
        "Manage_Flows",
        "PS_Flow_Management",
        "Flow Management",
        "Manage and execute flows with elevated permissions.",
    ),
    (
        "Launch_Fast",
        "PS_Launch_FAST",
        "Launch FAST",
        None,  # Keep existing description
    ),
    (
        "Modify_All_Data",
        "PS_Modify_All_Data",
        "Modify All Data",
        None,  # Keep existing description
    ),
    (
        "Password_Never_Expires",
        "PS_Password_Never_Expires",
        "Password Never Expires",
        None,  # Keep existing description
    ),

    # ── Refactored: content split into new PS but file gets renamed ──────
    (
        "Business_Rule_Notification",
        "PS_Business_Rule_Administration",
        "Business Rule Administration",
        "Create and manage business rules, NTE rules, notification rules, and approval routing configuration. SoD: Cannot be combined with PS_Approval_Decision — the person who writes the rules should not be the one making approval decisions under those rules.",
    ),
    (
        "SBS_Account_Management",
        "PS_Service_Approver_Configuration",
        "Service Approver Configuration",
        "Configure who the approvers are for each business rule, including NTE amounts, fuzzy matching, and contact/email settings. SoD: Cannot be combined with PS_Approval_Decision — configuring approvers and being an approver creates a self-approval risk.",
    ),

    # ── Consolidated: two files merged into one ──────────────────────────
    # AAV_Availability_Stand_Alone_Tool is the primary (has more content)
    (
        "AAV_Availability_Stand_Alone_Tool",
        "PS_Asset_Availability_Tool",
        "Asset Availability Tool",
        "Execute the Asset Availability (AAV) stand-alone tool. Consolidates former AAV_Availability_Stand_Alone_Tool and Asset_Availability_User_Permission_Set.",
    ),

    # ── Absorbed: Contact_Notification_Maintenance → PS_Contact_Management ──
    (
        "Contact_Notification_Maintenance",
        "PS_Contact_Management",
        "Contact Management",
        "Create and edit contacts, manage contact-to-account relationships, and notification preferences. Absorbs former Contact_Notification_Maintenance.",
    ),
]


def rename_ps(old_name, new_name, new_label, new_description):
    old_file = os.path.join(PS_DIR, f"{old_name}.permissionset-meta.xml")
    new_file = os.path.join(PS_DIR, f"{new_name}.permissionset-meta.xml")

    if not os.path.exists(old_file):
        print(f"  SKIP (not found): {old_name}")
        return False

    if os.path.exists(new_file):
        print(f"  SKIP (already exists): {new_name}")
        return False

    with open(old_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Update the label
    content = re.sub(
        r"<label>.*?</label>",
        f"<label>{new_label}</label>",
        content,
    )

    # Update description if provided
    if new_description:
        if "<description>" in content:
            content = re.sub(
                r"<description>.*?</description>",
                f"<description>{new_description}</description>",
                content,
                flags=re.DOTALL,
            )
        else:
            # Insert description after xmlns line
            content = content.replace(
                "</PermissionSet>",
                f"    <description>{new_description}</description>\n</PermissionSet>",
            )

    with open(new_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  {old_name}")
    print(f"    -> {new_name}  (label: \"{new_label}\")")
    return True


def main():
    print("Renaming permission sets...\n")
    success = 0
    for old_name, new_name, new_label, new_desc in RENAMES:
        if rename_ps(old_name, new_name, new_label, new_desc):
            success += 1

    print(f"\nRenamed {success} of {len(RENAMES)} permission sets.")
    print(f"\nOld files preserved in {PS_DIR}/ for reference.")
    print("For deployment, add old API names to destructiveChanges.xml.")


if __name__ == "__main__":
    main()
