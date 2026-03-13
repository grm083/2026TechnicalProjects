# SoD Permission Set Deploy Package

## Contents

```
deploy-package/
├── package.xml                          # Manifest: 54 PS_ permission sets
├── permissionsets/                       # 54 permission set metadata files
│   ├── PS_Account_Financial_Configuration.permissionset-meta.xml
│   ├── PS_Account_Management.permissionset-meta.xml
│   ├── ...
│   └── PS_WorkOrder_Scheduling.permissionset-meta.xml
├── destructive/
│   ├── destructiveChanges.xml           # Removes 30 old-name permission sets
│   └── package.xml                      # Empty manifest (required by SF CLI)
└── README.md
```

## What's Included

**54 permission sets** with the `PS_` naming convention:
- **25 net-new** permission sets (Case, Task, WorkOrder, Asset, Approval, Account, Genesys, Communication)
- **29 renamed** copies of existing permission sets (with updated labels, descriptions, and SoD documentation)

**30 old permission sets** listed in destructiveChanges.xml for removal after verification.

## Deployment

### Step 1: Deploy the new permission sets

```bash
sf project deploy start --source-dir deploy-package
```

Or using the manifest directly:

```bash
sf project deploy start --manifest deploy-package/package.xml --source-dir deploy-package
```

### Step 2: Verify in the target org

1. Confirm all 54 `PS_` permission sets appear in Setup > Permission Sets
2. Spot-check field permissions, object permissions, and Apex class access
3. Verify labels and descriptions are populated

### Step 3 (OPTIONAL): Remove old permission sets

**Only do this after updating all PSG assignments, Apex references, and flow references to use the new `PS_` API names.**

```bash
sf project deploy start --manifest deploy-package/destructive/package.xml --post-destructive-changes deploy-package/destructive/destructiveChanges.xml
```

## Permission Set Summary

| Category | Count | Permission Sets |
|----------|-------|----------------|
| Quote / CPQ | 6 | PS_Quote_Price_Accessibility, PS_Quote_Cost_Accessibility, PS_Quote_Lifecycle_Management, PS_Quote_Read_Only, PS_Quote_Approval, PS_Quote_MAS_Integration |
| Case Management | 5 | PS_Case_Intake, PS_Case_Lifecycle_Management, PS_Case_Financial, PS_Case_SLA_Override, PS_Case_Read_Only |
| Task Management | 3 | PS_Task_Assignment, PS_Task_Completion, PS_Task_Read_Only |
| Work Order | 4 | PS_WorkOrder_Creation, PS_WorkOrder_Cost_Management, PS_WorkOrder_Scheduling, PS_WorkOrder_Read_Only |
| Asset Management | 4 | PS_Asset_View, PS_Asset_Financial, PS_Asset_Availability_Tool, PS_Asset_Configuration |
| Pricing Engine | 3 | PS_Pricing_Request_Execution, PS_Pricing_Request_Read_Only, PS_STP_Administration |
| Business Rules | 5 | PS_Business_Rule_Administration, PS_Service_Approver_Configuration, PS_Approval_Decision, PS_NTE_Approval, PS_Business_Rule_Read_Only |
| Account & Contact | 5 | PS_Account_Management, PS_Account_Financial_Configuration, PS_Contact_Management, PS_Contact_Merge, PS_Notification_Preferences |
| Genesys / CTI | 2 | PS_Genesys_Routing_Control, PS_Genesys_Routing_View |
| Communication | 2 | PS_Communication_Send, PS_Communication_Read_Only |
| Reporting | 3 | PS_Report_Creator, PS_Report_Administrator, PS_Customer_Service_Reporting |
| Administration | 12 | PS_Knowledge_Management, PS_Project_Services, PS_Governance_Team, PS_Flow_Management, PS_Market_Area_Alerts_Admin, PS_Escalation_Maintenance, PS_Launch_FAST, PS_Digital_Transformation_Tracking, PS_Premium_Delivery_Management, PS_View_Setup, PS_Modify_All_Data, PS_Password_Never_Expires |
