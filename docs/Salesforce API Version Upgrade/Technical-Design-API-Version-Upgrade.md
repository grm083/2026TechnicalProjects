# Technical Design Document: Salesforce API Version Upgrade to 65.0

**Document Type:** Technical Design Document
**Project:** API Version Standardization and Upgrade Initiative
**Target API Version:** 65.0 (Winter '26)
**Document Version:** 1.0
**Date:** 2026-01-17
**Author:** George Martin, Salesforce Technical Architect
**Status:** Ready for Development

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Technical Scope](#2-technical-scope)
3. [Complete Component Inventory](#3-complete-component-inventory)
4. [Technical Requirements](#4-technical-requirements)
5. [Implementation Instructions](#5-implementation-instructions)
6. [Testing Requirements](#6-testing-requirements)
7. [Dependencies and Prerequisites](#7-dependencies-and-prerequisites)
8. [Rollback Strategy](#8-rollback-strategy)

---

## 1. Executive Summary

### 1.1 Purpose

This technical design document provides complete specifications for upgrading all Salesforce metadata components from their current API versions to API version 65.0 (Winter '26). This document is developer-ready and contains all necessary information to execute the upgrade.

### 1.2 Scope Overview

| Component Type | Total Count | Needs Update | Current Version Range | Target Version |
|----------------|-------------|--------------|----------------------|----------------|
| **Apex Classes** | 699 | 699 (100%) | 38.0 - 64.0 | 65.0 |
| **Lightning Web Components** | 42 | 42 (100%) | 47.0 - 63.0 | 65.0 |
| **Aura Components** | 206 | 206 (100%) | 45.0 - 62.0 | 65.0 |
| **Flows** | 99 | 99 (100%) | 49.0 - 64.0 | 65.0 |
| **TOTAL** | **1,046** | **1,046 (100%)** | **38.0 - 64.0** | **65.0** |

### 1.3 Critical Technical Changes in API 65.0

#### Breaking Change 1: SOAP login() Deprecated
- **Impact:** SOAP `login()` method is NO LONGER AVAILABLE in API 65.0
- **Affected Components:** Web services using SOAP authentication
- **Action Required:** Migrate to OAuth 2.0 or external authentication before Summer '27
- **Classes to Review:**
  - `ANIMatchWebservices.cls`
  - `IVRServiceStatusWebService.cls`
  - `WorkOrderWebservices.cls`

#### Breaking Change 2: Access Modifiers Required
- **Impact:** `abstract` and `override` methods MUST have explicit access modifiers
- **Action Required:** Add `protected`, `public`, or `global` keywords
- **Example:**
  ```apex
  // INVALID in API 65.0
  abstract class BaseClass {
      abstract void processData(); // ERROR: Missing access modifier
  }

  // VALID in API 65.0
  abstract class BaseClass {
      protected abstract void processData(); // Correct
  }
  ```

#### Breaking Change 3: Flow Record References
- **Impact:** Flows must use ID fields properly in record references
- **Affected:** All 99 flows need verification
- **Action Required:** Review and test all flows after upgrade

---

## 2. Technical Scope

### 2.1 Environment Requirements

**Development Environment:**
- Salesforce CLI (latest version)
- VS Code with Salesforce Extensions
- Git for version control
- Node.js (v14 or higher)

**Org Requirements:**
- Full Sandbox with production data clone
- API version must be set to 65.0 in `sfdx-project.json`

### 2.2 Update Strategy

**Approach:** Phased incremental update by component type and priority

**Priority Order:**
1. **Phase 1:** Critical Apex classes (API 38.0)
2. **Phase 2:** Trigger handlers and core infrastructure (API 45.0)
3. **Phase 3:** Remaining Apex classes
4. **Phase 4:** Lightning Web Components
5. **Phase 5:** Aura Components
6. **Phase 6:** Flows

---

## 3. Complete Component Inventory

### 3.1 Apex Classes Inventory (699 Classes)

#### 3.1.1 API Version 38.0 (4 Classes) - CRITICAL PRIORITY

| Class Name | Current Version | File Path | Action Required |
|------------|----------------|-----------|-----------------|
| AccountContactRelationHandler.cls | 38.0 | `/force-app/main/default/classes/AccountContactRelationHandler.cls` | Update to 65.0, scan for abstract/override methods |
| AccountContactRelationHelper.cls | 38.0 | `/force-app/main/default/classes/AccountContactRelationHelper.cls` | Update to 65.0, scan for abstract/override methods |
| GetEvaluatedContactId.cls | 38.0 | `/force-app/main/default/classes/GetEvaluatedContactId.cls` | Update to 65.0, scan for abstract/override methods |
| GetSLAInformation.cls | 38.0 | `/force-app/main/default/classes/GetSLAInformation.cls` | Update to 65.0, scan for abstract/override methods |

#### 3.1.2 API Version 45.0 (136 Classes) - HIGH PRIORITY

| Class Name | Current Version | File Path | Type |
|------------|----------------|-----------|------|
| ANIMatchWebservices.cls | 45.0 | `/force-app/main/default/classes/ANIMatchWebservices.cls` | SOAP Web Service - REVIEW |
| ANIMatchWebservicesTest.cls | 45.0 | `/force-app/main/default/classes/ANIMatchWebservicesTest.cls` | Test Class |
| AccountTitleTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/AccountTitleTriggerHandler.cls` | Trigger Handler |
| AccountTitleTriggerHelper.cls | 45.0 | `/force-app/main/default/classes/AccountTitleTriggerHelper.cls` | Trigger Helper |
| AccountTitleTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/AccountTitleTriggerHelperTest.cls` | Test Class |
| AcornCaseDetailsResource.cls | 45.0 | `/force-app/main/default/classes/AcornCaseDetailsResource.cls` | REST Resource |
| AcornCaseDetailsResourceTest.cls | 45.0 | `/force-app/main/default/classes/AcornCaseDetailsResourceTest.cls` | Test Class |
| AcornCompanyController.cls | 45.0 | `/force-app/main/default/classes/AcornCompanyController.cls` | Controller |
| AcornCompanyControllerTest.cls | 45.0 | `/force-app/main/default/classes/AcornCompanyControllerTest.cls` | Test Class |
| AcornCompanyDetails.cls | 45.0 | `/force-app/main/default/classes/AcornCompanyDetails.cls` | Helper |
| AcornCompanyDetailsTest.cls | 45.0 | `/force-app/main/default/classes/AcornCompanyDetailsTest.cls` | Test Class |
| AcornController.cls | 45.0 | `/force-app/main/default/classes/AcornController.cls` | Controller |
| AcornControllerTest.cls | 45.0 | `/force-app/main/default/classes/AcornControllerTest.cls` | Test Class |
| AssetHeadersForCaseController.cls | 45.0 | `/force-app/main/default/classes/AssetHeadersForCaseController.cls` | Controller |
| AssetHeadersForCaseControllerTest.cls | 45.0 | `/force-app/main/default/classes/AssetHeadersForCaseControllerTest.cls` | Test Class |
| AvoidProcessBuilder.cls | 45.0 | `/force-app/main/default/classes/AvoidProcessBuilder.cls` | Utility |
| AvoidProcessBuilderTest.cls | 45.0 | `/force-app/main/default/classes/AvoidProcessBuilderTest.cls` | Test Class |
| BatchToDeleteCase.cls | 45.0 | `/force-app/main/default/classes/BatchToDeleteCase.cls` | Batch Class |
| BatchToDeleteCaseTest.cls | 45.0 | `/force-app/main/default/classes/BatchToDeleteCaseTest.cls` | Test Class |
| BatchToUpdateUsersGroupId.cls | 45.0 | `/force-app/main/default/classes/BatchToUpdateUsersGroupId.cls` | Batch Class |
| BatchToUpdateUsersGroupIdScheduler.cls | 45.0 | `/force-app/main/default/classes/BatchToUpdateUsersGroupIdScheduler.cls` | Scheduler |
| BatchUpdateBusinessRules.cls | 45.0 | `/force-app/main/default/classes/BatchUpdateBusinessRules.cls` | Batch Class |
| BatchUpdateBusinessRulesTest.cls | 45.0 | `/force-app/main/default/classes/BatchUpdateBusinessRulesTest.cls` | Test Class |
| BooleanStringConverter.cls | 45.0 | `/force-app/main/default/classes/BooleanStringConverter.cls` | Utility |
| BooleanStringConverterTest.cls | 45.0 | `/force-app/main/default/classes/BooleanStringConverterTest.cls` | Test Class |
| BusinessRuleTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/BusinessRuleTriggerHandler.cls` | Trigger Handler |
| BusinessRuleTriggerHelper.cls | 45.0 | `/force-app/main/default/classes/BusinessRuleTriggerHelper.cls` | Trigger Helper |
| BusinessRuleTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/BusinessRuleTriggerHelperTest.cls` | Test Class |
| CaseApprovalHandlerTest.cls | 45.0 | `/force-app/main/default/classes/CaseApprovalHandlerTest.cls` | Test Class |
| CaseAssetController.cls | 45.0 | `/force-app/main/default/classes/CaseAssetController.cls` | Controller |
| CaseAssetControllerTest.cls | 45.0 | `/force-app/main/default/classes/CaseAssetControllerTest.cls` | Test Class |
| CaseAssetTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/CaseAssetTriggerHandler.cls` | Trigger Handler |
| CaseAssetTriggerHelper.cls | 45.0 | `/force-app/main/default/classes/CaseAssetTriggerHelper.cls` | Trigger Helper |
| CaseAssetTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/CaseAssetTriggerHelperTest.cls` | Test Class |
| CaseAttachUploadCntrlr.cls | 45.0 | `/force-app/main/default/classes/CaseAttachUploadCntrlr.cls` | Controller |
| CaseAttachUploadCntrlrTest.cls | 45.0 | `/force-app/main/default/classes/CaseAttachUploadCntrlrTest.cls` | Test Class |
| CaseController.cls | 45.0 | `/force-app/main/default/classes/CaseController.cls` | Controller |
| CaseControllerTest.cls | 45.0 | `/force-app/main/default/classes/CaseControllerTest.cls` | Test Class |
| CaseDetailHelper.cls | 45.0 | `/force-app/main/default/classes/CaseDetailHelper.cls` | Helper |
| CaseDetailHelperTest.cls | 45.0 | `/force-app/main/default/classes/CaseDetailHelperTest.cls` | Test Class |
| CaseTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/CaseTriggerHandler.cls` | Trigger Handler - CRITICAL |
| ChangeTaskAssignmentcntrl.cls | 45.0 | `/force-app/main/default/classes/ChangeTaskAssignmentcntrl.cls` | Controller |
| ChangeTaskAssignmentcntrlTest.cls | 45.0 | `/force-app/main/default/classes/ChangeTaskAssignmentcntrlTest.cls` | Test Class |
| CloseAcornTicket.cls | 45.0 | `/force-app/main/default/classes/CloseAcornTicket.cls` | Service Class |
| CloseAcornTicketTest.cls | 45.0 | `/force-app/main/default/classes/CloseAcornTicketTest.cls` | Test Class |
| ConcatenateTaskDetailForAcorn.cls | 45.0 | `/force-app/main/default/classes/ConcatenateTaskDetailForAcorn.cls` | Utility |
| ConcatenateTaskDetailForAcornTest.cls | 45.0 | `/force-app/main/default/classes/ConcatenateTaskDetailForAcornTest.cls` | Test Class |
| Constant_Util.cls | 45.0 | `/force-app/main/default/classes/Constant_Util.cls` | Utility |
| ContactSearchandCreate.cls | 45.0 | `/force-app/main/default/classes/ContactSearchandCreate.cls` | Service Class |
| ContactSearchandCreateTest.cls | 45.0 | `/force-app/main/default/classes/ContactSearchandCreateTest.cls` | Test Class |
| ContactTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/ContactTriggerHandler.cls` | Trigger Handler |
| ContactTriggerHelper.cls | 45.0 | `/force-app/main/default/classes/ContactTriggerHelper.cls` | Trigger Helper |
| ContactTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/ContactTriggerHelperTest.cls` | Test Class |
| CustomCaseCreationCntrlr.cls | 45.0 | `/force-app/main/default/classes/CustomCaseCreationCntrlr.cls` | Controller |
| CustomCaseCreationCntrlrTest.cls | 45.0 | `/force-app/main/default/classes/CustomCaseCreationCntrlrTest.cls` | Test Class |
| CustomCaseHighlightPanelCntrlTest.cls | 45.0 | `/force-app/main/default/classes/CustomCaseHighlightPanelCntrlTest.cls` | Test Class |
| DuplicateCheckOnCaseController.cls | 45.0 | `/force-app/main/default/classes/DuplicateCheckOnCaseController.cls` | Controller |
| DuplicateCheckOnCaseControllerTest.cls | 45.0 | `/force-app/main/default/classes/DuplicateCheckOnCaseControllerTest.cls` | Test Class |
| ETAWindowController.cls | 45.0 | `/force-app/main/default/classes/ETAWindowController.cls` | Controller |
| ETAWindowControllerTest.cls | 45.0 | `/force-app/main/default/classes/ETAWindowControllerTest.cls` | Test Class |
| EmailMessageHelper.cls | 45.0 | `/force-app/main/default/classes/EmailMessageHelper.cls` | Helper |
| EmailMessageHelperTest.cls | 45.0 | `/force-app/main/default/classes/EmailMessageHelperTest.cls` | Test Class |
| EmailMessageTest.cls | 45.0 | `/force-app/main/default/classes/EmailMessageTest.cls` | Test Class |
| EmailMessageTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/EmailMessageTriggerHandler.cls` | Trigger Handler |
| FeedCommentTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/FeedCommentTriggerHandler.cls` | Trigger Handler |
| FeedCommentTriggerHelper.cls | 45.0 | `/force-app/main/default/classes/FeedCommentTriggerHelper.cls` | Trigger Helper |
| FeedCommentTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/FeedCommentTriggerHelperTest.cls` | Test Class |
| GenTaskController.cls | 45.0 | `/force-app/main/default/classes/GenTaskController.cls` | Controller |
| GetBusinessDelayTime.cls | 45.0 | `/force-app/main/default/classes/GetBusinessDelayTime.cls` | Utility |
| GetBusinessDelayTimeTest.cls | 45.0 | `/force-app/main/default/classes/GetBusinessDelayTimeTest.cls` | Test Class |
| GetCaseInformation.cls | 45.0 | `/force-app/main/default/classes/GetCaseInformation.cls` | Service Class |
| GetCaseInformationTest.cls | 45.0 | `/force-app/main/default/classes/GetCaseInformationTest.cls` | Test Class |
| GetServiceApprover.cls | 45.0 | `/force-app/main/default/classes/GetServiceApprover.cls` | Service Class |
| GetServiceApproverTest.cls | 45.0 | `/force-app/main/default/classes/GetServiceApproverTest.cls` | Test Class |
| GetSobjectRecordTypeId.cls | 45.0 | `/force-app/main/default/classes/GetSobjectRecordTypeId.cls` | Utility |
| GetSobjectRecordTypeIdTest.cls | 45.0 | `/force-app/main/default/classes/GetSobjectRecordTypeIdTest.cls` | Test Class |
| GetUsername.cls | 45.0 | `/force-app/main/default/classes/GetUsername.cls` | Utility |
| GetUserNameTest.cls | 45.0 | `/force-app/main/default/classes/GetUserNameTest.cls` | Test Class |
| GetWorkOrderPDFCntrlr.cls | 45.0 | `/force-app/main/default/classes/GetWorkOrderPDFCntrlr.cls` | Controller |
| GetWorkOrderPDFCntrlrTest.cls | 45.0 | `/force-app/main/default/classes/GetWorkOrderPDFCntrlrTest.cls` | Test Class |
| IntegrationHandlerUtil.cls | 45.0 | `/force-app/main/default/classes/IntegrationHandlerUtil.cls` | Utility |
| LightningTableController.cls | 45.0 | `/force-app/main/default/classes/LightningTableController.cls` | Controller |
| LightningTableControllerTest.cls | 45.0 | `/force-app/main/default/classes/LightningTableControllerTest.cls` | Test Class |
| Logger.cls | 45.0 | `/force-app/main/default/classes/Logger.cls` | Utility - CRITICAL |
| LoggerTest.cls | 45.0 | `/force-app/main/default/classes/LoggerTest.cls` | Test Class |
| MultipleWorkorderController.cls | 45.0 | `/force-app/main/default/classes/MultipleWorkorderController.cls` | Controller |
| MultipleWorkorderControllerTest.cls | 45.0 | `/force-app/main/default/classes/MultipleWorkorderControllerTest.cls` | Test Class |
| MyOpenCaseListController.cls | 45.0 | `/force-app/main/default/classes/MyOpenCaseListController.cls` | Controller |
| MyOpenCaseListControllerTest.cls | 45.0 | `/force-app/main/default/classes/MyOpenCaseListControllerTest.cls` | Test Class |
| MyTaskListControllerTest.cls | 45.0 | `/force-app/main/default/classes/MyTaskListControllerTest.cls` | Test Class |
| ProgressCaseComponentController.cls | 45.0 | `/force-app/main/default/classes/ProgressCaseComponentController.cls` | Controller |
| ProgressCaseComponentControllerTest.cls | 45.0 | `/force-app/main/default/classes/ProgressCaseComponentControllerTest.cls` | Test Class |
| RESTHelper.cls | 45.0 | `/force-app/main/default/classes/RESTHelper.cls` | Utility |
| RecurrsiveTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/RecurrsiveTriggerHandler.cls` | Utility |
| RedNoteController.cls | 45.0 | `/force-app/main/default/classes/RedNoteController.cls` | Controller |
| RedNoteControllerTest.cls | 45.0 | `/force-app/main/default/classes/RedNoteControllerTest.cls` | Test Class |
| Screenpop.cls | 45.0 | `/force-app/main/default/classes/Screenpop.cls` | Service Class |
| ScreenpopController.cls | 45.0 | `/force-app/main/default/classes/ScreenpopController.cls` | Controller |
| ScreenpopEmulatorController.cls | 45.0 | `/force-app/main/default/classes/ScreenpopEmulatorController.cls` | Controller |
| SendEmailToServiceApproversCntrlr.cls | 45.0 | `/force-app/main/default/classes/SendEmailToServiceApproversCntrlr.cls` | Controller |
| SendEmailToServiceApproversCntrlrTest.cls | 45.0 | `/force-app/main/default/classes/SendEmailToServiceApproversCntrlrTest.cls` | Test Class |
| SendErrorNotificationOnJobFailure.cls | 45.0 | `/force-app/main/default/classes/SendErrorNotificationOnJobFailure.cls` | Utility |
| ServiceApproverHandler.cls | 45.0 | `/force-app/main/default/classes/ServiceApproverHandler.cls` | Handler |
| ServiceApproverHelper.cls | 45.0 | `/force-app/main/default/classes/ServiceApproverHelper.cls` | Helper |
| ServiceApproverHelperTest.cls | 45.0 | `/force-app/main/default/classes/ServiceApproverHelperTest.cls` | Test Class |
| ServicesDataWrapper.cls | 45.0 | `/force-app/main/default/classes/ServicesDataWrapper.cls` | Wrapper |
| SplitStringToListCntrlr.cls | 45.0 | `/force-app/main/default/classes/SplitStringToListCntrlr.cls` | Controller |
| SplitStringToListCntrlrTest.cls | 45.0 | `/force-app/main/default/classes/SplitStringToListCntrlrTest.cls` | Test Class |
| StatusWrapper.cls | 45.0 | `/force-app/main/default/classes/StatusWrapper.cls` | Wrapper |
| TaskRelatedListAura.cls | 45.0 | `/force-app/main/default/classes/TaskRelatedListAura.cls` | Controller |
| TaskRelatedListAuraTest.cls | 45.0 | `/force-app/main/default/classes/TaskRelatedListAuraTest.cls` | Test Class |
| TaskTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/TaskTriggerHandler.cls` | Trigger Handler - CRITICAL |
| TaskTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/TaskTriggerHelperTest.cls` | Test Class |
| TestDataFactory.cls | 45.0 | `/force-app/main/default/classes/TestDataFactory.cls` | Test Utility - CRITICAL |
| TestDataFactoryTest.cls | 45.0 | `/force-app/main/default/classes/TestDataFactoryTest.cls` | Test Class |
| TestScreenpop.cls | 45.0 | `/force-app/main/default/classes/TestScreenpop.cls` | Test Class |
| TestScreenpopController.cls | 45.0 | `/force-app/main/default/classes/TestScreenpopController.cls` | Test Class |
| TestScreenpopEmulatorController.cls | 45.0 | `/force-app/main/default/classes/TestScreenpopEmulatorController.cls` | Test Class |
| TrackingPattern.cls | 45.0 | `/force-app/main/default/classes/TrackingPattern.cls` | Service Class |
| TrackingPatternTest.cls | 45.0 | `/force-app/main/default/classes/TrackingPatternTest.cls` | Test Class |
| UpdateWorkOrder.cls | 45.0 | `/force-app/main/default/classes/UpdateWorkOrder.cls` | Service Class |
| UpdateWorkOrderTest.cls | 45.0 | `/force-app/main/default/classes/UpdateWorkOrderTest.cls` | Test Class |
| UserGroupUpdateBatchesTest.cls | 45.0 | `/force-app/main/default/classes/UserGroupUpdateBatchesTest.cls` | Test Class |
| UserTriggerHandler.cls | 45.0 | `/force-app/main/default/classes/UserTriggerHandler.cls` | Trigger Handler |
| UserTriggerHelper.cls | 45.0 | `/force-app/main/default/classes/UserTriggerHelper.cls` | Trigger Helper |
| UserTriggerHelperTest.cls | 45.0 | `/force-app/main/default/classes/UserTriggerHelperTest.cls` | Test Class |
| WODataWrapper.cls | 45.0 | `/force-app/main/default/classes/WODataWrapper.cls` | Wrapper |
| WorkOrderWebservices.cls | 45.0 | `/force-app/main/default/classes/WorkOrderWebservices.cls` | SOAP Web Service - REVIEW |
| WorkOrderWebservicesTest.cls | 45.0 | `/force-app/main/default/classes/WorkOrderWebservicesTest.cls` | Test Class |
| changeRecordTypeController.cls | 45.0 | `/force-app/main/default/classes/changeRecordTypeController.cls` | Controller |
| changeRecordTypeControllerTest.cls | 45.0 | `/force-app/main/default/classes/changeRecordTypeControllerTest.cls` | Test Class |
| dynamicCardController.cls | 45.0 | `/force-app/main/default/classes/dynamicCardController.cls` | Controller |
| dynamicCardControllerTest.cls | 45.0 | `/force-app/main/default/classes/dynamicCardControllerTest.cls` | Test Class |
| genTaskControllerTest.cls | 45.0 | `/force-app/main/default/classes/genTaskControllerTest.cls` | Test Class |
| subStatusPathController.cls | 45.0 | `/force-app/main/default/classes/subStatusPathController.cls` | Controller |
| subStatusPathControllerTest.cls | 45.0 | `/force-app/main/default/classes/subStatusPathControllerTest.cls` | Test Class |

**Note:** Complete listing of remaining 559 Apex classes (API versions 46.0-64.0) available in spreadsheet format at: `/docs/apex-class-inventory-complete.csv`

#### 3.1.3 API Version Distribution Summary

| API Version | Class Count | Priority | Effort Estimate (Hours) |
|-------------|-------------|----------|------------------------|
| 38.0 | 4 | Critical | 4 |
| 45.0 | 136 | High | 150 |
| 46.0 | 83 | High | 90 |
| 47.0 | 31 | Medium | 35 |
| 48.0 | 48 | Medium | 50 |
| 49.0 | 20 | Medium | 22 |
| 50.0 | 16 | Medium | 18 |
| 51.0 | 39 | Medium | 42 |
| 52.0 | 44 | Medium | 48 |
| 53.0 | 7 | Low | 8 |
| 54.0 | 13 | Low | 14 |
| 55.0 | 34 | Low | 36 |
| 56.0 | 18 | Low | 20 |
| 57.0 | 36 | Low | 38 |
| 58.0 | 42 | Low | 44 |
| 59.0 | 23 | Low | 24 |
| 60.0 | 28 | Low | 30 |
| 61.0 | 20 | Low | 22 |
| 62.0 | 20 | Low | 22 |
| 63.0 | 18 | Low | 20 |
| 64.0 | 19 | Low | 20 |
| **TOTAL** | **699** | - | **757 hours** |

### 3.2 Lightning Web Components Inventory (42 Components)

| Component Name | Current API | File Path | Priority |
|----------------|------------|-----------|----------|
| assetHoverCard | 47.0 | `/force-app/main/default/lwc/assetHoverCard` | High |
| changeRTCard | 47.0 | `/force-app/main/default/lwc/changeRTCard` | High |
| populateCaseSubType | 47.0 | `/force-app/main/default/lwc/populateCaseSubType` | High |
| multiAssetCaseCard | 48.0 | `/force-app/main/default/lwc/multiAssetCaseCard` | High |
| pricingOutputScreen | 48.0 | `/force-app/main/default/lwc/pricingOutputScreen` | High |
| pricingRequestInput | 48.0 | `/force-app/main/default/lwc/pricingRequestInput` | High |
| pubsub | 48.0 | `/force-app/main/default/lwc/pubsub` | Critical - Shared Utility |
| acornWODetails | 51.0 | `/force-app/main/default/lwc/acornWODetails` | Medium |
| quoteOrderComp | 51.0 | `/force-app/main/default/lwc/quoteOrderComp` | Medium |
| changeRecordTypeCard | 52.0 | `/force-app/main/default/lwc/changeRecordTypeCard` | Medium |
| chatNowTranscript | 52.0 | `/force-app/main/default/lwc/chatNowTranscript` | Medium |
| customCaseComment | 52.0 | `/force-app/main/default/lwc/customCaseComment` | Medium |
| hoverCard | 52.0 | `/force-app/main/default/lwc/hoverCard` | Medium |
| quoteDetailsComp | 52.0 | `/force-app/main/default/lwc/quoteDetailsComp` | Medium |
| quoteSummaryComp | 52.0 | `/force-app/main/default/lwc/quoteSummaryComp` | Medium |
| wasteStreamComp | 52.0 | `/force-app/main/default/lwc/wasteStreamComp` | Medium |
| emailMessageInput | 55.0 | `/force-app/main/default/lwc/emailMessageInput` | Medium |
| quotelineDetailsComp | 55.0 | `/force-app/main/default/lwc/quotelineDetailsComp` | Medium |
| aavCustomDatePicker | 56.0 | `/force-app/main/default/lwc/aavCustomDatePicker` | Medium |
| allRulesModal | 56.0 | `/force-app/main/default/lwc/allRulesModal` | Medium |
| caseRulesModal | 56.0 | `/force-app/main/default/lwc/caseRulesModal` | Medium |
| aavAlternateContainers | 57.0 | `/force-app/main/default/lwc/aavAlternateContainers` | Low |
| aavAppInputPanel | 57.0 | `/force-app/main/default/lwc/aavAppInputPanel` | Low |
| aavAppOutputPanel | 57.0 | `/force-app/main/default/lwc/aavAppOutputPanel` | Low |
| aavUtilityMethods | 57.0 | `/force-app/main/default/lwc/aavUtilityMethods` | Medium - Shared Utility |
| maintainVendorEscalationCom | 57.0 | `/force-app/main/default/lwc/maintainVendorEscalationCom` | Low |
| maintainVendorEscalationContact | 57.0 | `/force-app/main/default/lwc/maintainVendorEscalationContact` | Low |
| reusableCustomDropdownWithSearchLwc | 57.0 | `/force-app/main/default/lwc/reusableCustomDropdownWithSearchLwc` | Medium - Shared Utility |
| sendAlert | 57.0 | `/force-app/main/default/lwc/sendAlert` | Low |
| updatePortal | 57.0 | `/force-app/main/default/lwc/updatePortal` | Low |
| viewComments | 57.0 | `/force-app/main/default/lwc/viewComments` | Low |
| aavAppOutputDeliverySection | 58.0 | `/force-app/main/default/lwc/aavAppOutputDeliverySection` | Low |
| aavAppOutputOutageSection | 58.0 | `/force-app/main/default/lwc/aavAppOutputOutageSection` | Low |
| aavAppOutputServiceSection | 58.0 | `/force-app/main/default/lwc/aavAppOutputServiceSection` | Low |
| aavDeliveryDatesUI | 58.0 | `/force-app/main/default/lwc/aavDeliveryDatesUI` | Low |
| aavReusablePagination | 58.0 | `/force-app/main/default/lwc/aavReusablePagination` | Medium - Shared Utility |
| addNTERulesSA | 58.0 | `/force-app/main/default/lwc/addNTERulesSA` | Low |
| businessNotificationCmp | 58.0 | `/force-app/main/default/lwc/businessNotificationCmp` | Low |
| ntebRulesModal | 58.0 | `/force-app/main/default/lwc/ntebRulesModal` | Low |
| alertCard | 63.0 | `/force-app/main/default/lwc/alertCard` | Low |
| multiVendorPricingResponse | 63.0 | `/force-app/main/default/lwc/multiVendorPricingResponse` | Low |
| pricingMultiVendorOutputScreen | 63.0 | `/force-app/main/default/lwc/pricingMultiVendorOutputScreen` | Low |

**Total Effort Estimate for LWC:** 50 hours

### 3.3 Aura Components Inventory (206 Components)

**Note:** Due to length, the complete Aura component inventory is available in the analysis report. Key statistics:

| API Version | Component Count | Priority |
|-------------|----------------|----------|
| 45.0 | 52 | High |
| 46.0 | 34 | High |
| 47.0 | 18 | Medium |
| 48.0 | 27 | Medium |
| 49.0-62.0 | 75 | Low |

**Critical Aura Components (High Usage):**
- `CaseAssetComponent` (45.0)
- `CaseCreationComponent` (45.0)
- `ShowTeamsOpenTask` (45.0)
- `CustomAppPageTemplate` (45.0)
- `QuoteOverview` (46.0)

**Total Effort Estimate for Aura:** 80 hours

### 3.4 Flows Inventory (99 Flows)

#### 3.4.1 Critical Flows (High Usage) - API 49.0

| Flow Name | Current API | File Path | Business Process |
|-----------|------------|-----------|------------------|
| Business_Rule_Selection | 49.0 | `/force-app/main/default/flows/Business_Rule_Selection.flow-meta.xml` | Business Rule Engine |
| Task_Framework_Process_To_Create_Case | 49.0 | `/force-app/main/default/flows/Task_Framework_Process_To_Create_Case.flow-meta.xml` | Task Creation Framework |
| Case_Update_Process | 49.0 | `/force-app/main/default/flows/Case_Update_Process.flow-meta.xml` | Case Management |
| Task_Assignment | 49.0 | `/force-app/main/default/flows/Task_Assignment.flow-meta.xml` | Task Management |
| Approval_Log | 49.0 | `/force-app/main/default/flows/Approval_Log.flow-meta.xml` | Approval Process |
| Create_Business_Task_Notification | 49.0 | `/force-app/main/default/flows/Create_Business_Task_Notification.flow-meta.xml` | Notifications |
| Email_to_Case | 49.0 | `/force-app/main/default/flows/Email_to_Case.flow-meta.xml` | Email Processing |
| New_Service_Framework | 49.0 | `/force-app/main/default/flows/New_Service_Framework.flow-meta.xml` | Service Creation |
| Actions_for_the_Work_Order | 49.0 | `/force-app/main/default/flows/Actions_for_the_Work_Order.flow-meta.xml` | Work Order Processing |
| Recreate_Work_Order | 49.0 | `/force-app/main/default/flows/Recreate_Work_Order.flow-meta.xml` | Work Order Management |

#### 3.4.2 Flow Distribution Summary

| API Version | Flow Count | Priority | Requires Record Reference Review |
|-------------|-----------|----------|----------------------------------|
| 49.0 | 60 | High | Yes - All 60 flows |
| 51.0 | 2 | Medium | Yes |
| 52.0 | 1 | Medium | Yes |
| 53.0 | 1 | Medium | Yes |
| 54.0 | 1 | Medium | Yes |
| 55.0 | 7 | Medium | Yes |
| 56.0 | 2 | Low | Yes |
| 57.0 | 1 | Low | Yes |
| 58.0 | 1 | Low | Yes |
| 60.0 | 6 | Low | Yes |
| 61.0 | 2 | Low | Yes |
| 62.0 | 3 | Low | Yes |
| 63.0 | 10 | Low | Yes |
| 64.0 | 2 | Low | Yes |

**Total Effort Estimate for Flows:** 120 hours (includes testing)

---

## 4. Technical Requirements

### 4.1 Metadata File Update Requirements

#### 4.1.1 Apex Classes

**File Pattern:** `<ClassName>.cls-meta.xml`

**Required Change:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>65.0</apiVersion>
    <status>Active</status>
</ApexClass>
```

**Update Process:**
1. Locate metadata file: `force-app/main/default/classes/<ClassName>.cls-meta.xml`
2. Change `<apiVersion>` value from current version to `65.0`
3. Save file
4. Scan corresponding `.cls` file for abstract/override methods
5. Add explicit access modifiers if needed

#### 4.1.2 Lightning Web Components

**File Pattern:** `<ComponentName>.js-meta.xml`

**Required Change:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>65.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
    </targets>
</LightningComponentBundle>
```

**Update Process:**
1. Locate metadata file: `force-app/main/default/lwc/<componentName>/<componentName>.js-meta.xml`
2. Change `<apiVersion>` value to `65.0`
3. Save file
4. No code changes required unless deprecated features are used

#### 4.1.3 Aura Components

**File Pattern:** Various (`.cmp-meta.xml`, `.app-meta.xml`, `.evt-meta.xml`, etc.)

**Required Change:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<AuraDefinitionBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>65.0</apiVersion>
    <description>Component Description</description>
</AuraDefinitionBundle>
```

**Update Process:**
1. Locate metadata file: `force-app/main/default/aura/<ComponentName>/<ComponentName>.<extension>-meta.xml`
2. Change `<apiVersion>` value to `65.0`
3. Save file

#### 4.1.4 Flows

**File Pattern:** `<FlowName>.flow-meta.xml`

**Required Change:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>65.0</apiVersion>
    <!-- rest of flow definition -->
</Flow>
```

**Update Process:**
1. Locate flow file: `force-app/main/default/flows/<FlowName>.flow-meta.xml`
2. Change `<apiVersion>` value to `65.0`
3. Review record references for ID field usage
4. Save file
5. Test flow in sandbox

### 4.2 Code Modification Requirements

#### 4.2.1 Abstract Methods - Access Modifiers

**Scan Required:** All Apex classes must be scanned for abstract methods

**Search Pattern:**
```
abstract\s+(?!protected|public|global)\s+(void|[A-Z]\w*)
```

**Invalid Pattern (API 65.0):**
```apex
abstract class MyBaseClass {
    abstract void process(); // ERROR: Missing access modifier
    abstract String getName(); // ERROR: Missing access modifier
}
```

**Valid Pattern (API 65.0):**
```apex
abstract class MyBaseClass {
    protected abstract void process(); // CORRECT
    public abstract String getName(); // CORRECT
    global abstract void globalProcess(); // CORRECT
}
```

**Action Items:**
1. Run regex search across all `.cls` files
2. Identify methods missing access modifiers
3. Add appropriate access modifier (use `protected` for internal inheritance, `public` for package-level, `global` for managed packages)

#### 4.2.2 Override Methods - Access Modifiers

**Search Pattern:**
```
override\s+(?!protected|public|global)\s+(void|[A-Z]\w*)
```

**Invalid Pattern (API 65.0):**
```apex
public class MyChildClass extends MyBaseClass {
    override void process() { // ERROR: Missing access modifier
        // implementation
    }
}
```

**Valid Pattern (API 65.0):**
```apex
public class MyChildClass extends MyBaseClass {
    protected override void process() { // CORRECT
        // implementation
    }
}
```

#### 4.2.3 SOAP Web Services - Authentication Review

**Classes Requiring Review:**
- `ANIMatchWebservices.cls`
- `IVRServiceStatusWebService.cls`
- `WorkOrderWebservices.cls`

**Search for SOAP login() usage:**
```apex
Soap.login()
```

**Migration Path:**
1. Identify all SOAP login() calls
2. Replace with OAuth 2.0 authentication
3. Update integration documentation
4. Test with external systems

### 4.3 Automated Update Scripts

#### 4.3.1 Bulk Metadata Update Script

**Script:** `scripts/update-api-versions.sh`

```bash
#!/bin/bash
# Update API versions for all metadata files

TARGET_VERSION="65.0"

echo "Updating Apex Classes to API $TARGET_VERSION..."
find force-app/main/default/classes -name "*-meta.xml" -exec sed -i "s/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>$TARGET_VERSION<\/apiVersion>/g" {} \;

echo "Updating LWC Components to API $TARGET_VERSION..."
find force-app/main/default/lwc -name "*-meta.xml" -exec sed -i "s/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>$TARGET_VERSION<\/apiVersion>/g" {} \;

echo "Updating Aura Components to API $TARGET_VERSION..."
find force-app/main/default/aura -name "*-meta.xml" -exec sed -i "s/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>$TARGET_VERSION<\/apiVersion>/g" {} \;

echo "Updating Flows to API $TARGET_VERSION..."
find force-app/main/default/flows -name "*.flow-meta.xml" -exec sed -i "s/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>$TARGET_VERSION<\/apiVersion>/g" {} \;

echo "API version update complete!"
echo "Next steps:"
echo "1. Review changes with: git diff"
echo "2. Scan for abstract/override methods"
echo "3. Run tests: sfdx force:apex:test:run --codecoverage"
echo "4. Deploy to sandbox: sfdx force:source:deploy"
```

**Usage:**
```bash
chmod +x scripts/update-api-versions.sh
./scripts/update-api-versions.sh
```

#### 4.3.2 Abstract/Override Method Scanner

**Script:** `scripts/scan-access-modifiers.sh`

```bash
#!/bin/bash
# Scan for abstract and override methods missing access modifiers

echo "Scanning for abstract methods without access modifiers..."
grep -rn "abstract\s\+\(void\|[A-Z]\w*\)" force-app/main/default/classes/*.cls | grep -v "protected\|public\|global" > /tmp/abstract-issues.txt

echo "Scanning for override methods without access modifiers..."
grep -rn "override\s\+\(void\|[A-Z]\w*\)" force-app/main/default/classes/*.cls | grep -v "protected\|public\|global" > /tmp/override-issues.txt

echo "Results:"
echo "Abstract method issues: $(wc -l < /tmp/abstract-issues.txt) found"
echo "Override method issues: $(wc -l < /tmp/override-issues.txt) found"
echo ""
echo "Details saved to:"
echo "  /tmp/abstract-issues.txt"
echo "  /tmp/override-issues.txt"
```

---

## 5. Implementation Instructions

### 5.1 Phase 1: Critical Apex Classes (API 38.0) - Week 1

**Objective:** Update 4 classes from API 38.0 to 65.0

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/api-upgrade-phase1-critical
   ```

2. **Update Metadata Files**
   ```bash
   # Update AccountContactRelationHandler
   cd force-app/main/default/classes
   sed -i 's/<apiVersion>38.0<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' AccountContactRelationHandler.cls-meta.xml
   sed -i 's/<apiVersion>38.0<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' AccountContactRelationHelper.cls-meta.xml
   sed -i 's/<apiVersion>38.0<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' GetEvaluatedContactId.cls-meta.xml
   sed -i 's/<apiVersion>38.0<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' GetSLAInformation.cls-meta.xml
   ```

3. **Scan for Code Issues**
   ```bash
   # Check for abstract/override methods
   grep -n "abstract\|override" AccountContactRelationHandler.cls
   grep -n "abstract\|override" AccountContactRelationHelper.cls
   grep -n "abstract\|override" GetEvaluatedContactId.cls
   grep -n "abstract\|override" GetSLAInformation.cls
   ```

4. **Fix Access Modifiers (if found)**
   - Open each class in VS Code
   - Add explicit access modifiers to abstract/override methods
   - Save changes

5. **Deploy to Sandbox**
   ```bash
   cd /home/user/2026TechnicalProjects
   sfdx force:source:deploy --sourcepath force-app/main/default/classes/AccountContactRelationHandler.cls* --testlevel NoTestRun --targetusername <sandbox-alias>
   # Repeat for other 3 classes
   ```

6. **Run Tests**
   ```bash
   sfdx force:apex:test:run --classnames AccountContactRelationHandlerTest --codecoverage --resultformat human --targetusername <sandbox-alias>
   # Check for test failures
   ```

7. **Commit Changes**
   ```bash
   git add force-app/main/default/classes/AccountContactRelation*
   git add force-app/main/default/classes/GetEvaluatedContactId*
   git add force-app/main/default/classes/GetSLAInformation*
   git commit -m "Phase 1: Update critical classes from API 38.0 to 65.0"
   git push origin feature/api-upgrade-phase1-critical
   ```

**Expected Results:**
- 4 classes updated to API 65.0
- All tests passing
- No compilation errors

### 5.2 Phase 2: Trigger Handlers (API 45.0) - Weeks 2-3

**Objective:** Update core trigger handlers from API 45.0 to 65.0

**Critical Trigger Handlers:**
1. CaseTriggerHandler.cls
2. BusinessRuleTriggerHandler.cls
3. ContactTriggerHandler.cls
4. TaskTriggerHandler.cls
5. AssetTriggerHandler.cls
6. WorkOrderTriggerHandler.cls
7. EmailMessageTriggerHandler.cls
8. CaseAssetTriggerHandler.cls
9. AccountTitleTriggerHandler.cls
10. UserTriggerHandler.cls

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/api-upgrade-phase2-triggers
   ```

2. **Update Trigger Handlers (Batch)**
   ```bash
   cd force-app/main/default/classes

   # Update all trigger handlers
   for file in *TriggerHandler.cls-meta.xml; do
     if grep -q "<apiVersion>45.0</apiVersion>" "$file"; then
       sed -i 's/<apiVersion>45.0<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' "$file"
       echo "Updated: $file"
     fi
   done

   # Update all trigger helpers
   for file in *TriggerHelper.cls-meta.xml; do
     if grep -q "<apiVersion>45.0</apiVersion>" "$file"; then
       sed -i 's/<apiVersion>45.0<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' "$file"
       echo "Updated: $file"
     fi
   done
   ```

3. **Scan for Abstract/Override Methods**
   ```bash
   # Create scan results
   ./scripts/scan-access-modifiers.sh

   # Review results
   cat /tmp/abstract-issues.txt
   cat /tmp/override-issues.txt
   ```

4. **Fix Code Issues**
   - Open each file with issues in VS Code
   - Add access modifiers as needed
   - Save changes

5. **Deploy and Test**
   ```bash
   # Deploy trigger handlers
   sfdx force:source:deploy --sourcepath force-app/main/default/classes/*TriggerHandler.cls* --testlevel RunLocalTests --targetusername <sandbox-alias>

   # Monitor deployment
   sfdx force:source:deploy:report --targetusername <sandbox-alias>
   ```

6. **Verify Tests Pass**
   ```bash
   sfdx force:apex:test:run --testlevel RunLocalTests --codecoverage --resultformat human --targetusername <sandbox-alias>
   ```

7. **Commit Changes**
   ```bash
   git add force-app/main/default/classes/*TriggerHandler*
   git add force-app/main/default/classes/*TriggerHelper*
   git commit -m "Phase 2: Update trigger handlers from API 45.0 to 65.0"
   git push origin feature/api-upgrade-phase2-triggers
   ```

### 5.3 Phase 3: Remaining Apex Classes - Weeks 4-10

**Objective:** Update remaining 559 Apex classes systematically

**Approach:** Batch update by API version (50-75 classes per week)

**Weekly Schedule:**

| Week | API Versions | Class Count | Focus Area |
|------|--------------|-------------|------------|
| 4 | 45.0 (batch 1) | 70 classes | Controllers |
| 5 | 45.0 (batch 2) | 66 classes | Test Classes |
| 6 | 46.0 | 83 classes | Batch Jobs & Utilities |
| 7 | 47.0, 48.0 | 79 classes | Helpers & Wrappers |
| 8 | 49.0-52.0 | 119 classes | Service Classes |
| 9 | 53.0-58.0 | 133 classes | Mixed |
| 10 | 59.0-64.0 | 138 classes | Recent Classes |

**Weekly Process:**

1. **Monday:** Identify classes for the week
2. **Tuesday:** Batch update metadata files
3. **Wednesday:** Scan and fix code issues
4. **Thursday:** Deploy to sandbox and run tests
5. **Friday:** Fix test failures and commit

**Batch Update Template:**
```bash
# Week X Script
WEEK_NUM=4
API_VERSION="45.0"
BATCH_NUM=1

git checkout -b feature/api-upgrade-week${WEEK_NUM}-batch${BATCH_NUM}

# Update metadata
find force-app/main/default/classes -name "*-meta.xml" -exec grep -l "<apiVersion>$API_VERSION</apiVersion>" {} \; | head -70 | xargs sed -i 's/<apiVersion>'$API_VERSION'<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g'

# Verify changes
git diff --stat

# Scan for issues
./scripts/scan-access-modifiers.sh

# Deploy
sfdx force:source:deploy --sourcepath force-app/main/default/classes --testlevel RunLocalTests

# Commit
git commit -am "Week $WEEK_NUM: Update batch $BATCH_NUM to API 65.0"
git push origin feature/api-upgrade-week${WEEK_NUM}-batch${BATCH_NUM}
```

### 5.4 Phase 4: Lightning Web Components - Week 11

**Objective:** Update all 42 LWC components

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/api-upgrade-phase4-lwc
   ```

2. **Batch Update All LWC**
   ```bash
   find force-app/main/default/lwc -name "*-meta.xml" -exec sed -i 's/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' {} \;
   ```

3. **Verify Critical Shared Components**
   - Test `pubsub` (event bus utility)
   - Test `aavUtilityMethods` (shared utility)
   - Test `reusableCustomDropdownWithSearchLwc` (shared component)
   - Test `aavReusablePagination` (shared component)

4. **Visual Regression Testing**
   - Open each Lightning page in sandbox
   - Verify component rendering
   - Test component interactions
   - Check console for errors

5. **Deploy and Test**
   ```bash
   sfdx force:source:deploy --sourcepath force-app/main/default/lwc --testlevel NoTestRun
   ```

6. **Commit Changes**
   ```bash
   git add force-app/main/default/lwc
   git commit -m "Phase 4: Update all LWC components to API 65.0"
   git push origin feature/api-upgrade-phase4-lwc
   ```

### 5.5 Phase 5: Aura Components - Weeks 12-14

**Objective:** Update all 206 Aura components

**Note:** Aura is in maintenance mode. Prioritize high-usage components.

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/api-upgrade-phase5-aura
   ```

2. **Batch Update All Aura Components**
   ```bash
   find force-app/main/default/aura -name "*-meta.xml" -exec sed -i 's/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' {} \;
   ```

3. **Test High-Priority Components First**
   - CaseAssetComponent
   - CaseCreationComponent
   - ShowTeamsOpenTask
   - CustomAppPageTemplate
   - QuoteOverview

4. **Deploy in Batches (50 components per batch)**
   ```bash
   # Batch 1: API 45.0 components
   sfdx force:source:deploy --sourcepath force-app/main/default/aura/CaseAssetComponent,force-app/main/default/aura/CaseCreationComponent,... --testlevel NoTestRun
   ```

5. **Visual Testing**
   - Open Aura applications in sandbox
   - Test component rendering
   - Verify event handling

6. **Commit Changes**
   ```bash
   git add force-app/main/default/aura
   git commit -m "Phase 5: Update all Aura components to API 65.0"
   git push origin feature/api-upgrade-phase5-aura
   ```

### 5.6 Phase 6: Flows - Weeks 15-16

**Objective:** Update all 99 flows and verify record references

**Critical Action:** Review ALL flows for record reference issues (API 65.0 requirement)

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/api-upgrade-phase6-flows
   ```

2. **Batch Update All Flows**
   ```bash
   find force-app/main/default/flows -name "*.flow-meta.xml" -exec sed -i 's/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' {} \;
   ```

3. **Critical Flow Testing (Manual)**

   Test each of these flows in sandbox:
   - Business_Rule_Selection
   - Task_Framework_Process_To_Create_Case
   - Case_Update_Process
   - Task_Assignment
   - Approval_Log
   - Email_to_Case
   - New_Service_Framework
   - Actions_for_the_Work_Order
   - Recreate_Work_Order
   - Work_Order_Creation

4. **Record Reference Verification**

   For EACH flow:
   - Open in Flow Builder
   - Check "Get Records" elements
   - Verify record variables use ID fields correctly
   - Save and activate

5. **Deploy Flows**
   ```bash
   # Deploy in batches (20 flows per batch)
   sfdx force:source:deploy --sourcepath force-app/main/default/flows --testlevel NoTestRun
   ```

6. **Integration Testing**
   - Test case creation flows
   - Test task assignment flows
   - Test approval flows
   - Test work order flows
   - Test business rule flows

7. **Commit Changes**
   ```bash
   git add force-app/main/default/flows
   git commit -m "Phase 6: Update all flows to API 65.0 and verify record references"
   git push origin feature/api-upgrade-phase6-flows
   ```

### 5.7 Final Integration and Production Deployment - Weeks 17-18

**Week 17: Final Sandbox Validation**

1. **Merge All Branches**
   ```bash
   git checkout main
   git merge feature/api-upgrade-phase1-critical
   git merge feature/api-upgrade-phase2-triggers
   git merge feature/api-upgrade-phase3-apex
   git merge feature/api-upgrade-phase4-lwc
   git merge feature/api-upgrade-phase5-aura
   git merge feature/api-upgrade-phase6-flows
   ```

2. **Deploy Complete Package to Full Sandbox**
   ```bash
   sfdx force:source:deploy --manifest manifest/package.xml --testlevel RunLocalTests --targetusername fullsandbox
   ```

3. **Run Complete Test Suite**
   ```bash
   sfdx force:apex:test:run --testlevel RunAllTestsInOrg --codecoverage --resultformat human
   ```

4. **User Acceptance Testing**
   - Execute UAT test cases (see QA document)
   - Get stakeholder sign-off

**Week 18: Production Deployment**

1. **Schedule Maintenance Window**
   - Notify all users
   - Freeze code changes
   - Back up production

2. **Pre-Deployment Checklist**
   - [ ] All tests passing in sandbox (>85% coverage)
   - [ ] UAT sign-off received
   - [ ] Rollback plan documented
   - [ ] Deployment runbook reviewed
   - [ ] Team on standby for issues

3. **Production Deployment**
   ```bash
   sfdx force:source:deploy --manifest manifest/package.xml --testlevel RunLocalTests --targetusername production --wait 60
   ```

4. **Post-Deployment Verification**
   - [ ] Check deployment logs
   - [ ] Run smoke tests
   - [ ] Verify critical flows
   - [ ] Check integration endpoints
   - [ ] Monitor error logs for 2 hours

5. **Post-Deployment Monitoring (48 hours)**
   - Monitor debug logs
   - Track user-reported issues
   - Verify batch jobs run successfully
   - Check external integrations

---

## 6. Testing Requirements

### 6.1 Unit Testing

**Requirement:** Maintain >85% code coverage

**Process:**

1. **Pre-Update Baseline**
   ```bash
   sfdx force:apex:test:run --testlevel RunLocalTests --codecoverage --resultformat json > pre-update-coverage.json
   ```

2. **Post-Update Validation**
   ```bash
   sfdx force:apex:test:run --testlevel RunLocalTests --codecoverage --resultformat json > post-update-coverage.json
   ```

3. **Compare Coverage**
   - Coverage must not decrease
   - All existing tests must pass
   - Fix any failing tests immediately

### 6.2 Integration Testing

**Critical Integration Points:**

1. **Genesys CTI Integration**
   - Test inbound call handling
   - Verify task creation from platform events
   - Check ANI matching functionality

2. **Acorn Field Service Integration**
   - Test work order creation
   - Verify status updates
   - Check REST API endpoints

3. **IVR Service Status**
   - Test SOAP web service calls (critical - SOAP login deprecated)
   - Verify service status lookups
   - Check authentication method

4. **Quote-to-Cash (SBQQ)**
   - Test quote creation flows
   - Verify pricing calculations
   - Check multi-vendor pricing

### 6.3 Regression Testing

See separate QA Test Case Scenario Document for complete regression test suite.

**High-Level Areas:**

1. **Case Management**
   - Case creation
   - Case updates
   - Case assignment
   - Case closure

2. **Task Management**
   - Task framework
   - Task assignment
   - Task completion

3. **Work Order Processing**
   - Work order creation
   - Work order updates
   - Work order completion

4. **Business Rules Engine**
   - Business rule evaluation
   - Business rule triggers

5. **Approval Processes**
   - Approval workflows
   - Approval logging

6. **Email Processing**
   - Email to case
   - Email notifications

---

## 7. Dependencies and Prerequisites

### 7.1 Technical Dependencies

**Required Tools:**
- Salesforce CLI (sfdx) - version 7.180.0 or higher
- VS Code with Salesforce Extensions
- Git version 2.30 or higher
- Node.js v14 or higher
- bash shell (for scripts)

**Org Requirements:**
- Full sandbox with production data
- API version 65.0 enabled
- All packages and managed packages updated to API 65.0 compatible versions

### 7.2 Access Requirements

**Required Permissions:**
- Modify All Data
- Author Apex
- Customize Application
- Manage Flows
- Deploy metadata

**Required Org Access:**
- Development sandbox (for development)
- Full sandbox (for UAT)
- Production org (for deployment)

### 7.3 Pre-Requisites

**Before Starting:**

1. **Verify Third-Party Package Compatibility**
   - Check all AppExchange packages support API 65.0
   - Update packages if necessary
   - Document package versions

2. **Back Up Production**
   - Create full org backup
   - Export all metadata
   - Document current API versions

3. **Create Baseline Test Results**
   - Run all tests in production
   - Document current test coverage
   - Capture current performance metrics

4. **Review Breaking Changes**
   - Read Winter '26 release notes
   - Identify potential impacts
   - Plan mitigation strategies

### 7.4 External Dependencies

**Integration Partners:**
- Notify Genesys team of API upgrade timeline
- Coordinate with Acorn for endpoint testing
- Alert IVR team of SOAP authentication changes

---

## 8. Rollback Strategy

### 8.1 Rollback Decision Criteria

**Trigger Rollback if:**
- Test coverage drops below 75%
- Critical business process fails
- Integration with external system breaks
- More than 5% of users report issues
- Performance degradation >20%

### 8.2 Rollback Procedure

**Step 1: Stop Deployment**
```bash
sfdx force:mdapi:deploy:cancel --targetusername production
```

**Step 2: Deploy Previous Version**
```bash
# Use pre-upgrade backup
sfdx force:source:deploy --manifest backup/pre-upgrade-package.xml --testlevel NoTestRun --targetusername production
```

**Step 3: Verify Rollback**
```bash
sfdx force:apex:test:run --testlevel RunLocalTests
```

**Step 4: Notify Stakeholders**
- Send rollback notification
- Document issues encountered
- Schedule post-mortem

### 8.3 Rollback Limitations

**Cannot Rollback:**
- Manual data changes made post-deployment
- User-created records
- Custom metadata updated by users

**Mitigation:**
- Use change sets for gradual rollout
- Deploy to partial sandboxes first
- Monitor closely for first 48 hours

---

## 9. Success Criteria

**Project Completion Criteria:**

- [ ] All 1,046 components updated to API 65.0
- [ ] All Apex tests passing (>85% coverage)
- [ ] All integration tests passing
- [ ] Zero critical business process failures
- [ ] UAT sign-off received
- [ ] Production deployment successful
- [ ] 48-hour monitoring period completed without major issues

---

## 10. Appendix

### 10.1 Quick Reference Commands

```bash
# Check current API versions
grep -r "<apiVersion>" force-app/main/default --include="*-meta.xml" | sort -u

# Update specific component type
find force-app/main/default/classes -name "*-meta.xml" -exec sed -i 's/<apiVersion>[0-9.]*<\/apiVersion>/<apiVersion>65.0<\/apiVersion>/g' {} \;

# Run tests
sfdx force:apex:test:run --testlevel RunLocalTests --codecoverage

# Deploy to org
sfdx force:source:deploy --sourcepath force-app/main/default --testlevel RunLocalTests

# Check deployment status
sfdx force:source:deploy:report

# View debug logs
sfdx force:apex:log:tail
```

### 10.2 Troubleshooting Guide

**Issue:** Compilation errors after updating class

**Solution:**
1. Check for missing access modifiers on abstract/override methods
2. Verify SOAP authentication methods updated
3. Check for deprecated features in release notes

**Issue:** Tests failing after update

**Solution:**
1. Review test class for hard-coded API version references
2. Update test data to match new behavior
3. Check for flow-related test failures (record references)

**Issue:** Flow fails after update

**Solution:**
1. Open flow in Flow Builder
2. Check "Get Records" elements for proper ID field usage
3. Re-save and activate flow

### 10.3 Support Contacts

**Technical Lead:** George Martin - [email]
**Salesforce Admin:** [Name] - [email]
**QA Lead:** [Name] - [email]
**Project Manager:** [Name] - [email]

---

**END OF TECHNICAL DESIGN DOCUMENT**

**Document Control:**
- Version: 1.0
- Last Updated: 2026-01-17
- Next Review: Upon phase completion
- Classification: Internal Use Only
