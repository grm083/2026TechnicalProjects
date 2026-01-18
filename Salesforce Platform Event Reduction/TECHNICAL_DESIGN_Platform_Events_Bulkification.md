# TECHNICAL DESIGN DOCUMENT
## Salesforce Platform Event Volume Reduction Initiative

---

**Document Title:** Technical Design Document - Platform Event Bulkification

**Project Name:** Salesforce Platform Event Volume Reduction Initiative

**Project Code:** SFDC-PE-2026-001

**Document Version:** 1.0

**Document Date:** January 18, 2026

**Author:** Technical Architecture Team

**Document Status:** Draft - Pending Review

---

## Document Control

| Version | Date | Author | Changes | Reviewer | Status |
|---------|------|--------|---------|----------|--------|
| 0.1 | 2026-01-18 | Technical Architecture Team | Initial draft | Pending | Draft |
| 1.0 | 2026-01-18 | Technical Architecture Team | Complete design | Pending | Draft |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Design Overview](#design-overview)
3. [Current State Architecture](#current-state-architecture)
4. [Future State Architecture](#future-state-architecture)
5. [Detailed Design Specifications](#detailed-design-specifications)
6. [Database Design](#database-design)
7. [Integration Design](#integration-design)
8. [Security Design](#security-design)
9. [Error Handling and Logging](#error-handling-and-logging)
10. [Performance Design](#performance-design)
11. [Testing Strategy](#testing-strategy)
12. [Deployment Plan](#deployment-plan)
13. [Rollback Strategy](#rollback-strategy)
14. [Appendices](#appendices)

---

## Executive Summary

### Purpose

This Technical Design Document provides detailed specifications for refactoring non-bulkified Platform Event publishing patterns in the Salesforce organization. The design addresses critical technical debt that results in excessive Platform Event generation, data loss, and performance degradation.

### Scope

This design covers:
- Refactoring of 6 Apex classes and triggers
- Creation of new PlatformEventPublisher utility framework
- Implementation of monitoring and alerting
- Testing and deployment strategies

### Design Principles

1. **Bulkification First:** All Platform Event publishing must support bulk operations (200 records)
2. **Backward Compatibility:** No breaking changes to event subscribers or payload structures
3. **Error Resilience:** Graceful error handling with comprehensive logging
4. **Performance Optimization:** Minimize CPU time and API consumption
5. **Maintainability:** Clear, documented code following Salesforce best practices
6. **Testability:** 85%+ code coverage with comprehensive test scenarios

### Key Architectural Changes

| Component | Current State | Future State | Impact |
|-----------|---------------|--------------|--------|
| **CasetoQuoteAutomation.trigger** | Processes only first event | Processes all events in batch | Eliminates data loss |
| **PlatformEventProcessor.cls** | RaiseTaskAndGenesysPE accepts single ID | Accepts Set<Id>, publishes in bulk | 99% reduction in API calls |
| **QouteValiationHandler.cls** | Calls event publisher in loop | Collects IDs, publishes after loop | 95% reduction in API calls |
| **AutoSendEmailToServiceApprovers.cls** | Publishes 1 event for N cases | Publishes N events in 1 bulk operation | Complete audit trail |
| **Logger.cls** | saveLog() non-bulkified | Deprecated, use saveLogs() only | Standardized logging |
| **PlatformEventPublisher.cls** | Does not exist | New centralized utility | Reusable framework |

---

## Design Overview

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          TRIGGER LAYER                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐   │
│  │ CasetoQuote      │  │ QuoteTrigger     │  │ Other Triggers     │   │
│  │ Automation       │  │                  │  │                    │   │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────┬─────────┘   │
└───────────┼────────────────────┼─────────────────────────┼─────────────┘
            │                    │                         │
            ▼                    ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        BUSINESS LOGIC LAYER                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │           QouteValiationHandler.cls (REFACTORED)                 │  │
│  │  - Collects quote IDs requiring events                          │  │
│  │  - Calls PlatformEventProcessor AFTER loop                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │        AutoSendEmailToServiceApprovers.cls (REFACTORED)          │  │
│  │  - Publishes event per case in bulk                             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PLATFORM EVENT PUBLISHING LAYER                       │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │         PlatformEventProcessor.cls (REFACTORED)                  │  │
│  │  ┌──────────────────────────────────────────────────────────┐   │  │
│  │  │ RaiseTaskAndGenesysPE(Set<Id> quoteIds)                  │   │  │
│  │  │  - Creates List<Task_and_Genesys_Platform_Event__e>     │   │  │
│  │  │  - Loops through Set<Id> to create events               │   │  │
│  │  │  - Single EventBus.publish() call                        │   │  │
│  │  └──────────────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────────────┐   │  │
│  │  │ RaiseSTPProcessEventPE(Set<Id> quoteIds, Boolean flag)  │   │  │
│  │  │  - Already bulkified (reference pattern)                │   │  │
│  │  └──────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │         PlatformEventPublisher.cls (NEW UTILITY)                 │  │
│  │  - Centralized event publishing framework                        │  │
│  │  - Queuing mechanism for events                                  │  │
│  │  - Bulk publish with error handling                              │  │
│  │  - Convenience methods for common event types                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                Logger.cls (UPDATED)                              │  │
│  │  - saveLog() marked @deprecated                                  │  │
│  │  - saveLogs() enforced as standard                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PLATFORM EVENT BUS                               │
│                      EventBus.publish() API                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Task_and_Genesys_Platform_Event__e                               │  │
│  │ STPProcessEvent__e                                               │  │
│  │ CasetoQuoteAutomation__e                                         │  │
│  │ System_Log_Event__e                                              │  │
│  │ Task_Create_Update_Event__e                                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      EVENT SUBSCRIBER LAYER                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Platform Event Triggers (Subscribers)                           │  │
│  │  - Process events asynchronously                                 │  │
│  │  - Already support bulk processing                               │  │
│  │  - No changes required                                           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Design Strategy

#### Refactoring Approach

**Minimize Risk:**
1. Maintain existing method signatures where possible (overload instead of replace)
2. Preserve event payload structures (no breaking changes)
3. Keep error handling patterns consistent
4. Add comprehensive logging for debugging

**Maximize Impact:**
1. Focus on high-volume event publishers first
2. Create reusable patterns via PlatformEventPublisher utility
3. Implement monitoring to validate improvements
4. Document patterns for future development

#### Backward Compatibility

All changes maintain backward compatibility:
- Event payload structures unchanged
- Event subscribers require no modifications
- Existing method signatures preserved via overloading
- Deprecated methods remain functional (with warnings)

---

## Current State Architecture

### Current State: CasetoQuoteAutomation.trigger

**File:** `force-app/main/default/triggers/CasetoQuoteAutomation.trigger`

**Current Implementation:**
```apex
trigger CasetoQuoteAutomation on CasetoQuoteAutomation__e (after insert) {
    try {
        // ISSUE: Only accesses Trigger.new[0] - first event only!
        String eventType = Trigger.new[0].EventType__c;
        string payload = Trigger.new[0].payload__c;

        List<CaseQuoteAutomation__mdt> caseQuoteAutomationList = [
            SELECT Next_Event__c, Parameter__c
            FROM CaseQuoteAutomation__mdt
            WHERE Action__c = :eventType
        ];

        Map<String, Object> MapOfData = (Map<String, Object>)
            JSON.deserializeUntyped(Trigger.new[0].PayLoad__c);

        // ... process single event ...

        // Publishes single new event
        if(caseQuoteAutomationList[0].Next_Event__c != null && result != null) {
            List<CasetoQuoteAutomation__e> events = new List<CasetoQuoteAutomation__e>();
            CasetoQuoteAutomation__e event = new CasetoQuoteAutomation__e();
            event.EventType__c = caseQuoteAutomationList[0].Next_Event__c;
            event.PayLoad__c = JSON.serialize(result);
            events.add(event);
            List<Database.SaveResult> results = EventBus.publish(events);
        }
    } catch (Exception ex) {
        system.debug(ex.getMessage());
    }
}
```

**Problems:**
1. ❌ Only processes `Trigger.new[0]` (first event)
2. ❌ All subsequent events in batch are silently dropped
3. ❌ No error logging for dropped events
4. ❌ Data loss occurring in production

**Impact:**
- If 50 events published together, only 1 is processed (98% loss)
- Downstream automation incomplete
- Business processes fail silently

---

### Current State: PlatformEventProcessor.RaiseTaskAndGenesysPE

**File:** `force-app/main/default/classes/PlatformEventProcessor.cls`

**Current Implementation:**
```apex
/*
@Method name       : RaiseTaskAndGenesysPE
@Description       : To raise TaskandGenesys Platform event
@Param             : Id quoteId                          ← SINGLE ID!
@Return Type       : Void
*/
public static void RaiseTaskAndGenesysPE(Id quoteId){
    List<Task_and_Genesys_Platform_Event__e> events = new List<Task_and_Genesys_Platform_Event__e>();
    Task_and_Genesys_Platform_Event__e evt = new Task_and_Genesys_Platform_Event__e(Payload__c=quoteId);
    events.add(evt);

    // Publishes immediately - if called in loop, happens N times!
    List<Database.SaveResult> results = EventBus.publish(events);
}
```

**Called From:** `QouteValiationHandler.cls`
```apex
for(SBQQ__Quote__c qt: triggerNew){  // LOOP
    // ... validation logic ...

    if(startDatevalidationMessage != Constant_Util.SUCCESS && startDatevalidationMessage != null) {
        PlatformEventProcessor.RaiseTaskAndGenesysPE(qt.Id);  // CALLED IN LOOP!
        qt.addError(startDatevalidationMessage);
        return true;
    }
}
```

**Problems:**
1. ❌ Method accepts single ID instead of collection
2. ❌ Called inside trigger loop (200 quotes = 200 publish operations)
3. ❌ Each publish operation counts against governor limits
4. ❌ Massive API consumption

**Impact:**
- 200 individual EventBus.publish() calls instead of 1
- High CPU time consumed
- Governor limit risk
- Primary cause of excessive Platform Events

---

### Current State: AutoSendEmailToServiceApprovers

**File:** `force-app/main/default/classes/AutoSendEmailToServiceApprovers.cls`

**Current Implementation:**
```apex
public static void autosendEmail(Set<Id> brlst, Set<Id> cselst, Set<Id> tsklst){
    // ... processes multiple business rules, cases, tasks ...
    // ... sends emails to multiple approvers ...

    if(results.get(0).isSuccess()) {
        // ISSUE: Only publishes ONE event for ALL cases!
        System_Log_Event__e emailEvent = new System_Log_Event__e();
        emailEvent.Message__c = System.Label.ApprovalEmailSuccessMsg;
        emailEvent.Level__c = 'INFO';
        emailEvent.Parent_ID__c = caseId;  // Only ONE caseId
        emailEvent.User_ID__c = UserInfo.getUserId();

        Database.SaveResult result = EventBus.publish(emailEvent);
    }
}
```

**Problems:**
1. ❌ Method accepts multiple case IDs but only publishes 1 event
2. ❌ Only one case is referenced in the log event
3. ❌ Incomplete audit trail (missing 99% of cases)
4. ❌ Compliance risk

**Impact:**
- If 100 approvals processed, only 1 logged
- Audit trail has 99% gaps
- Cannot trace which cases had emails sent
- Compliance and troubleshooting issues

---

### Current State: Logger.saveLog()

**File:** `force-app/main/default/classes/Logger.cls`

**Current Implementation:**
```apex
// Non-bulkified method
public Logger saveLog(Logger.Log l) {
    System_log_event__e event = Logger.log2SystemEvent(l);
    System_Log__c log = Logger.toSObject(l);
    insert log;      // Individual DML
    insert event;    // Individual DML - NOT EventBus.publish!
    return this;
}

// Bulkified method (already exists, properly implemented)
public Logger saveLogs() {
    List<SObject> logsToAdd = new List<SObject>();
    List<SObject> eventsToAdd = new List<SObject>();

    for (Logger.Log l : logCache) {
        logsToAdd.add(Logger.toSObject(l));
        eventsToAdd.add(Logger.log2SystemEvent(l));
    }

    Database.insert(logsToAdd, false);

    if (CREATE_PLATFORM_EVENT) {
        Database.SaveResult[] eventSrList = EventBus.publish(eventsToAdd);  // BULK
    }

    return this;
}
```

**Problems:**
1. ⚠️ Dual API design - both bulkified and non-bulkified methods exist
2. ⚠️ Developers may call wrong method
3. ⚠️ No deprecation warning on non-bulkified method
4. ⚠️ Limited usage (3 classes) but should be standardized

**Impact:**
- If saveLog() called in loop, creates individual events
- Inconsistent logging patterns across codebase
- Technical debt continues to accrue

---

## Future State Architecture

### Future State: CasetoQuoteAutomation.trigger (Refactored)

**Design Goals:**
1. ✅ Process ALL events in Trigger.new (not just first)
2. ✅ Collect new events to publish, then publish in bulk
3. ✅ Add comprehensive error handling and logging
4. ✅ Maintain backward compatibility with event payload

**Refactored Implementation:**
```apex
trigger CasetoQuoteAutomation on CasetoQuoteAutomation__e (after insert) {
    // Collect new events to publish
    List<CasetoQuoteAutomation__e> eventsToPublish = new List<CasetoQuoteAutomation__e>();
    List<String> errorMessages = new List<String>();

    // Process ALL events in batch
    for(CasetoQuoteAutomation__e incomingEvent : Trigger.new) {
        try {
            String eventType = incomingEvent.EventType__c;
            String payload = incomingEvent.payload__c;

            // Query metadata for this event type
            List<CaseQuoteAutomation__mdt> caseQuoteAutomationList = [
                SELECT Next_Event__c, Parameter__c
                FROM CaseQuoteAutomation__mdt
                WHERE Action__c = :eventType
                LIMIT 1
            ];

            if(caseQuoteAutomationList.isEmpty()) {
                errorMessages.add('No metadata found for eventType: ' + eventType);
                continue;
            }

            // Deserialize payload
            Map<String, Object> MapOfData = (Map<String, Object>)
                JSON.deserializeUntyped(incomingEvent.PayLoad__c);

            // Process event based on type
            Object result = processEventByType(eventType, MapOfData, caseQuoteAutomationList[0]);

            // If there's a next event, collect it for bulk publish
            if(caseQuoteAutomationList[0].Next_Event__c != null && result != null) {
                CasetoQuoteAutomation__e newEvent = new CasetoQuoteAutomation__e();
                newEvent.EventType__c = caseQuoteAutomationList[0].Next_Event__c;
                newEvent.PayLoad__c = JSON.serialize(result);
                eventsToPublish.add(newEvent);
            }

        } catch (Exception ex) {
            // Log error but continue processing other events
            errorMessages.add('Error processing event: ' + ex.getMessage() +
                            ' | StackTrace: ' + ex.getStackTraceString());
        }
    }

    // Bulk publish all collected events
    if(!eventsToPublish.isEmpty()) {
        List<Database.SaveResult> results = EventBus.publish(eventsToPublish);

        // Check for publish errors
        for(Integer i = 0; i < results.size(); i++) {
            if(!results[i].isSuccess()) {
                for(Database.Error err : results[i].getErrors()) {
                    errorMessages.add('Failed to publish event: ' + err.getMessage());
                }
            }
        }
    }

    // Log any errors
    if(!errorMessages.isEmpty()) {
        System.debug(LoggingLevel.ERROR, 'CasetoQuoteAutomation errors: ' +
                     String.join(errorMessages, '; '));

        // Optional: Create System_Log_Event__e for errors
        Logger.error('CasetoQuoteAutomation', String.join(errorMessages, '; ')).saveLogs();
    }
}

// Helper method to process event by type (extracted for clarity)
private static Object processEventByType(String eventType, Map<String, Object> data,
                                         CaseQuoteAutomation__mdt metadata) {
    // Implementation of event processing logic
    // (existing logic from current trigger)
    return null; // placeholder
}
```

**Key Changes:**
1. ✅ **Loop through ALL events:** `for(CasetoQuoteAutomation__e incomingEvent : Trigger.new)`
2. ✅ **Collect events:** `eventsToPublish.add(newEvent)` instead of immediate publish
3. ✅ **Bulk publish:** Single `EventBus.publish()` call after loop
4. ✅ **Error handling:** Try-catch per event, continue processing on error
5. ✅ **Error logging:** Comprehensive logging of all errors
6. ✅ **Helper method:** Extract processing logic for testability

**Benefits:**
- Processes all events (0% data loss)
- Single publish operation (vs. N operations)
- Errors don't block other events
- Better debugging with comprehensive logging

---

### Future State: PlatformEventProcessor.RaiseTaskAndGenesysPE (Refactored)

**Design Goals:**
1. ✅ Accept collection of IDs instead of single ID
2. ✅ Create events for all IDs in single operation
3. ✅ Maintain backward compatibility with overloaded method
4. ✅ Add error handling and logging

**Refactored Implementation:**
```apex
/*
@Method name       : RaiseTaskAndGenesysPE (REFACTORED - BULK)
@Description       : To raise TaskandGenesys Platform event in bulk
@Param             : Set<Id> quoteIds - Collection of quote IDs
@Return Type       : Void
*/
public static void RaiseTaskAndGenesysPE(Set<Id> quoteIds){
    if(quoteIds == null || quoteIds.isEmpty()) {
        return; // No IDs to process
    }

    List<Task_and_Genesys_Platform_Event__e> events = new List<Task_and_Genesys_Platform_Event__e>();

    // Create event for EACH quote ID
    for(Id quoteId : quoteIds){
        Task_and_Genesys_Platform_Event__e evt = new Task_and_Genesys_Platform_Event__e();
        evt.Payload__c = quoteId;
        events.add(evt);
    }

    // Single bulk publish operation
    List<Database.SaveResult> results = EventBus.publish(events);

    // Error handling
    for(Integer i = 0; i < results.size(); i++){
        if(!results[i].isSuccess()){
            String errorMsg = 'Failed to publish Task_and_Genesys_Platform_Event__e for quote: ' +
                            events[i].Payload__c;
            for(Database.Error err : results[i].getErrors()){
                errorMsg += ' | Error: ' + err.getMessage();
            }
            System.debug(LoggingLevel.ERROR, errorMsg);

            // Log to System_Log_Event__e
            Logger.error('PlatformEventProcessor.RaiseTaskAndGenesysPE', errorMsg).saveLogs();
        }
    }
}

/*
@Method name       : RaiseTaskAndGenesysPE (OVERLOAD - BACKWARD COMPATIBILITY)
@Description       : Overload for single ID (calls bulk method)
@Param             : Id quoteId - Single quote ID
@Return Type       : Void
@Deprecated        : Use bulk method with Set<Id> instead
*/
@Deprecated
public static void RaiseTaskAndGenesysPE(Id quoteId){
    if(quoteId == null) {
        return;
    }

    // Call bulk method
    Set<Id> quoteIds = new Set<Id>{quoteId};
    RaiseTaskAndGenesysPE(quoteIds);
}
```

**Key Changes:**
1. ✅ **Collection parameter:** `Set<Id> quoteIds` instead of `Id quoteId`
2. ✅ **Bulk event creation:** Loop to create events for all IDs
3. ✅ **Single publish:** One `EventBus.publish()` call
4. ✅ **Error handling:** Check each SaveResult, log failures
5. ✅ **Backward compatibility:** Overloaded method for single ID
6. ✅ **Deprecation warning:** `@Deprecated` annotation

**Benefits:**
- 200 IDs = 1 publish call (vs. 200 calls)
- 99.5% reduction in API consumption
- Backward compatible (existing callers still work)
- Comprehensive error logging

---

### Future State: QouteValiationHandler (Refactored)

**Design Goal:**
Collect quote IDs during validation loop, publish events AFTER loop completes

**Current Pattern (BEFORE):**
```apex
for(SBQQ__Quote__c qt: triggerNew){
    // validation logic...
    PlatformEventProcessor.RaiseTaskAndGenesysPE(qt.Id);  // ❌ IN LOOP
}
```

**Refactored Pattern (AFTER):**
```apex
// Collect IDs that need events
Set<Id> quoteIdsNeedingEvents = new Set<Id>();

for(SBQQ__Quote__c qt: triggerNew){
    // ... validation logic ...

    String startDatevalidationMessage = StartDateManagement.validateStartDateOnNewServiceQuote(
        quoteLines, triggerOldMap
    );

    if(startDatevalidationMessage != Constant_Util.SUCCESS && startDatevalidationMessage != null) {
        // Collect ID instead of publishing immediately
        quoteIdsNeedingEvents.add(qt.Id);
        qt.addError(startDatevalidationMessage);
        return true;
    }
}

// Publish ALL events in one bulk operation AFTER loop
if(!quoteIdsNeedingEvents.isEmpty()) {
    PlatformEventProcessor.RaiseTaskAndGenesysPE(quoteIdsNeedingEvents);
}
```

**Key Changes:**
1. ✅ **Collect IDs:** `quoteIdsNeedingEvents.add(qt.Id)` during loop
2. ✅ **Publish after loop:** Single call after loop completes
3. ✅ **Pass collection:** `RaiseTaskAndGenesysPE(quoteIdsNeedingEvents)`

**Benefits:**
- 95% reduction in publish operations
- Cleaner separation of concerns
- Easier to debug and maintain

---

### Future State: AutoSendEmailToServiceApprovers (Refactored)

**Design Goals:**
1. ✅ Publish one log event PER case (not just one total)
2. ✅ Bulk publish all events together
3. ✅ Complete audit trail

**Refactored Implementation:**
```apex
public static void autosendEmail(Set<Id> brlst, Set<Id> cselst, Set<Id> tsklst){
    // ... existing email sending logic ...

    List<Messaging.SingleEmailMessage> emails = new List<Messaging.SingleEmailMessage>();
    Map<Id, Id> caseIdToEmailMap = new Map<Id, Id>(); // Track which email for which case

    // Build emails (existing logic)
    // ... populate emails list and caseIdToEmailMap ...

    // Send emails
    List<Messaging.SendEmailResult> results = Messaging.sendEmail(emails);

    // Create log event for EACH case (not just one)
    List<System_Log_Event__e> emailEvents = new List<System_Log_Event__e>();

    for(Integer i = 0; i < results.size(); i++) {
        Messaging.SendEmailResult result = results[i];

        if(result.isSuccess()) {
            // Create SUCCESS log event for this case
            Id caseId = getCaseIdForEmail(i, caseIdToEmailMap);

            System_Log_Event__e emailEvent = new System_Log_Event__e();
            emailEvent.Message__c = System.Label.ApprovalEmailSuccessMsg;
            emailEvent.Level__c = 'INFO';
            emailEvent.Parent_ID__c = caseId;
            emailEvent.User_ID__c = UserInfo.getUserId();
            emailEvent.Timestamp__c = System.now();
            emailEvents.add(emailEvent);

        } else {
            // Create ERROR log event for this case
            Id caseId = getCaseIdForEmail(i, caseIdToEmailMap);

            String errorMsg = 'Email send failed: ';
            for(Messaging.SendEmailError err : result.getErrors()) {
                errorMsg += err.getMessage() + '; ';
            }

            System_Log_Event__e emailEvent = new System_Log_Event__e();
            emailEvent.Message__c = errorMsg;
            emailEvent.Level__c = 'ERROR';
            emailEvent.Parent_ID__c = caseId;
            emailEvent.User_ID__c = UserInfo.getUserId();
            emailEvent.Timestamp__c = System.now();
            emailEvents.add(emailEvent);
        }
    }

    // Bulk publish ALL log events
    if(!emailEvents.isEmpty()) {
        List<Database.SaveResult> eventResults = EventBus.publish(emailEvents);

        // Handle event publish failures
        for(Integer i = 0; i < eventResults.size(); i++) {
            if(!eventResults[i].isSuccess()) {
                String logError = 'Failed to publish System_Log_Event__e: ';
                for(Database.Error err : eventResults[i].getErrors()) {
                    logError += err.getMessage() + '; ';
                }
                System.debug(LoggingLevel.ERROR, logError);
            }
        }
    }
}

// Helper method to map email index to case ID
private static Id getCaseIdForEmail(Integer emailIndex, Map<Id, Id> caseIdToEmailMap) {
    // Implementation to retrieve case ID for given email index
    return null; // placeholder
}
```

**Key Changes:**
1. ✅ **Event per case:** Loop through results, create event for EACH case
2. ✅ **Bulk publish:** Single `EventBus.publish()` for all events
3. ✅ **Success and error tracking:** Log both success and failure
4. ✅ **Complete audit trail:** 100% of cases logged

**Benefits:**
- Complete audit trail (from 1% to 100%)
- Compliance requirements met
- Easier troubleshooting
- Still bulkified (1 publish operation)

---

### Future State: Logger.cls (Updated)

**Design Goal:**
Deprecate non-bulkified method, standardize on bulkified pattern

**Updated Implementation:**
```apex
/*
@Method name       : saveLog (NON-BULKIFIED - DEPRECATED)
@Description       : Saves a single log immediately (NOT RECOMMENDED)
@Param             : Logger.Log l
@Return Type       : Logger
@Deprecated        : Use saveLogs() instead for bulkified logging
*/
@Deprecated
public Logger saveLog(Logger.Log l) {
    // Add deprecation warning
    System.debug(LoggingLevel.WARN,
        'DEPRECATED: Logger.saveLog() is deprecated. Use Logger.saveLogs() instead for bulkified logging.'
    );

    // Add log to cache
    logCache.add(l);

    // Call bulkified method
    return saveLogs();
}

/*
@Method name       : saveLogs (BULKIFIED - RECOMMENDED)
@Description       : Saves all cached logs in bulk
@Return Type       : Logger
*/
public Logger saveLogs() {
    if(logCache.isEmpty()) {
        return this;
    }

    List<SObject> logsToAdd = new List<SObject>();
    List<SObject> eventsToAdd = new List<SObject>();

    for (Logger.Log l : logCache) {
        logsToAdd.add(Logger.toSObject(l));
        eventsToAdd.add(Logger.log2SystemEvent(l));
    }

    // Bulk DML operations
    Database.insert(logsToAdd, false);

    if (CREATE_PLATFORM_EVENT) {
        Database.SaveResult[] eventSrList = EventBus.publish(eventsToAdd);

        // Error handling for event publishing
        for(Integer i = 0; i < eventSrList.size(); i++) {
            if(!eventSrList[i].isSuccess()) {
                System.debug(LoggingLevel.ERROR,
                    'Failed to publish System_Log_Event__e: ' + eventSrList[i].getErrors()
                );
            }
        }
    }

    // Clear cache
    logCache.clear();

    return this;
}
```

**Key Changes:**
1. ✅ **@Deprecated annotation:** Marks saveLog() as deprecated
2. ✅ **Runtime warning:** Logs deprecation message when called
3. ✅ **Redirects to bulk method:** saveLog() now calls saveLogs()
4. ✅ **Documentation:** Updated JSDoc comments

**Migration Strategy:**
1. Update all callers to use saveLogs() pattern:
   ```apex
   // BEFORE:
   new Logger().log('Error', 'Message').saveLog();

   // AFTER:
   new Logger().log('Error', 'Message').saveLogs();
   ```

2. Search for all usage of `Logger.saveLog()` and refactor

3. After migration period (3-6 months), remove deprecated method

---

### Future State: PlatformEventPublisher (New Utility)

**Design Goals:**
1. ✅ Centralized event publishing framework
2. ✅ Built-in bulkification
3. ✅ Error handling and logging
4. ✅ Convenience methods for common event types
5. ✅ Reusable across all Platform Events

**New Class Implementation:**
```apex
/**
 * @Description: Centralized utility for publishing Platform Events in bulk
 * @Author: Technical Architecture Team
 * @Date: 2026-01-18
 * @Usage:
 *   // Add events to queue
 *   PlatformEventPublisher.addSystemLogEvent('INFO', 'Message', caseId);
 *   PlatformEventPublisher.addSystemLogEvent('ERROR', 'Error msg', caseId);
 *
 *   // Publish all queued events in bulk
 *   PlatformEventPublisher.publishEvents();
 */
public without sharing class PlatformEventPublisher {

    // Event queue (automatically bulkified)
    private static List<SObject> eventsToPublish = new List<SObject>();

    // Maximum events per publish operation (Salesforce limit: 10,000)
    private static final Integer MAX_EVENTS_PER_PUBLISH = 2000;

    /**
     * Add a generic Platform Event to the queue
     * @param event Platform Event record (any __e object)
     */
    public static void addEvent(SObject event) {
        if(event != null) {
            eventsToPublish.add(event);
        }
    }

    /**
     * Add multiple Platform Events to the queue
     * @param events List of Platform Event records
     */
    public static void addEvents(List<SObject> events) {
        if(events != null && !events.isEmpty()) {
            eventsToPublish.addAll(events);
        }
    }

    /**
     * Publish all queued events in bulk
     * @return List<Database.SaveResult> Results of publish operation
     */
    public static List<Database.SaveResult> publishEvents() {
        if(eventsToPublish.isEmpty()) {
            return new List<Database.SaveResult>();
        }

        List<Database.SaveResult> allResults = new List<Database.SaveResult>();

        // Handle chunking if over max limit
        Integer totalEvents = eventsToPublish.size();
        Integer startIndex = 0;

        while(startIndex < totalEvents) {
            Integer endIndex = Math.min(startIndex + MAX_EVENTS_PER_PUBLISH, totalEvents);
            List<SObject> chunk = new List<SObject>();

            for(Integer i = startIndex; i < endIndex; i++) {
                chunk.add(eventsToPublish[i]);
            }

            // Publish chunk
            List<Database.SaveResult> results = EventBus.publish(chunk);
            allResults.addAll(results);

            // Error handling
            for(Integer i = 0; i < results.size(); i++) {
                if(!results[i].isSuccess()) {
                    String errorMsg = 'Failed to publish Platform Event: ' +
                                    chunk[i].getSObjectType();
                    for(Database.Error err : results[i].getErrors()) {
                        errorMsg += ' | Error: ' + err.getMessage();
                    }
                    System.debug(LoggingLevel.ERROR, errorMsg);
                }
            }

            startIndex = endIndex;
        }

        // Clear queue
        eventsToPublish.clear();

        return allResults;
    }

    /**
     * Get count of queued events (for testing/debugging)
     * @return Integer Number of events in queue
     */
    public static Integer getQueuedEventCount() {
        return eventsToPublish.size();
    }

    /**
     * Clear all queued events without publishing (for error recovery)
     */
    public static void clearQueue() {
        eventsToPublish.clear();
    }

    // ==================== CONVENIENCE METHODS ====================

    /**
     * Add System_Log_Event__e to queue
     * @param level Log level (INFO, WARN, ERROR, DEBUG)
     * @param message Log message
     * @param parentId Related record ID (optional)
     */
    public static void addSystemLogEvent(String level, String message, Id parentId) {
        System_Log_Event__e event = new System_Log_Event__e(
            Level__c = level,
            Message__c = message,
            Parent_ID__c = parentId,
            User_ID__c = UserInfo.getUserId(),
            Timestamp__c = System.now()
        );
        addEvent(event);
    }

    /**
     * Add Task_and_Genesys_Platform_Event__e to queue
     * @param quoteId Quote ID payload
     */
    public static void addTaskAndGenesysEvent(Id quoteId) {
        Task_and_Genesys_Platform_Event__e event = new Task_and_Genesys_Platform_Event__e(
            Payload__c = quoteId
        );
        addEvent(event);
    }

    /**
     * Add multiple Task_and_Genesys_Platform_Event__e to queue
     * @param quoteIds Set of Quote IDs
     */
    public static void addTaskAndGenesysEvents(Set<Id> quoteIds) {
        if(quoteIds == null || quoteIds.isEmpty()) {
            return;
        }

        List<Task_and_Genesys_Platform_Event__e> events =
            new List<Task_and_Genesys_Platform_Event__e>();

        for(Id quoteId : quoteIds) {
            events.add(new Task_and_Genesys_Platform_Event__e(Payload__c = quoteId));
        }

        addEvents(events);
    }

    /**
     * Add STPProcessEvent__e to queue
     * @param quoteId Quote ID payload
     * @param priceOnlyCall Price only flag
     */
    public static void addSTPProcessEvent(Id quoteId, Boolean priceOnlyCall) {
        STPProcessEvent__e event = new STPProcessEvent__e(
            Payload__c = quoteId,
            PriceOnlyCall__c = priceOnlyCall
        );
        addEvent(event);
    }

    /**
     * Add multiple STPProcessEvent__e to queue
     * @param quoteIds Set of Quote IDs
     * @param priceOnlyCall Price only flag
     */
    public static void addSTPProcessEvents(Set<Id> quoteIds, Boolean priceOnlyCall) {
        if(quoteIds == null || quoteIds.isEmpty()) {
            return;
        }

        List<STPProcessEvent__e> events = new List<STPProcessEvent__e>();

        for(Id quoteId : quoteIds) {
            events.add(new STPProcessEvent__e(
                Payload__c = quoteId,
                PriceOnlyCall__c = priceOnlyCall
            ));
        }

        addEvents(events);
    }

    /**
     * Add CasetoQuoteAutomation__e to queue
     * @param eventType Event type from metadata
     * @param payload JSON payload
     */
    public static void addCaseToQuoteEvent(String eventType, String payload) {
        CasetoQuoteAutomation__e event = new CasetoQuoteAutomation__e(
            EventType__c = eventType,
            PayLoad__c = payload
        );
        addEvent(event);
    }

    /**
     * Add Task_Create_Update_Event__e to queue
     * @param caseId Case ID to refresh
     * @param refresh Refresh flag
     */
    public static void addTaskCreateUpdateEvent(Id caseId, Boolean refresh) {
        Task_Create_Update_Event__e event = new Task_Create_Update_Event__e(
            CaseId__c = caseId,
            Refresh__c = refresh
        );
        addEvent(event);
    }
}
```

**Key Features:**
1. ✅ **Queue-based:** Events collected, published in bulk
2. ✅ **Automatic chunking:** Handles >2000 events safely
3. ✅ **Error handling:** Comprehensive logging of failures
4. ✅ **Convenience methods:** Pre-built methods for each event type
5. ✅ **Flexible:** Generic addEvent() for any Platform Event
6. ✅ **Testable:** getQueuedEventCount() for assertions

**Usage Example:**
```apex
// In trigger or handler class
for(SBQQ__Quote__c quote : triggerNew) {
    // Collect events during loop
    PlatformEventPublisher.addTaskAndGenesysEvent(quote.Id);
    PlatformEventPublisher.addSystemLogEvent('INFO', 'Quote validated', quote.Id);
}

// Publish all at once after loop
PlatformEventPublisher.publishEvents();
```

---

## Detailed Design Specifications

### Design Specification 1: CasetoQuoteAutomation.trigger Refactoring

**Objective:** Process all events in batch, eliminate data loss

**Affected Files:**
- `force-app/main/default/triggers/CasetoQuoteAutomation.trigger`

**Changes Required:**

| Component | Current | New | Reason |
|-----------|---------|-----|--------|
| Event access | `Trigger.new[0]` | `for(event : Trigger.new)` | Process all events |
| Event collection | N/A | `List<CasetoQuoteAutomation__e> eventsToPublish` | Collect before publish |
| Publishing | In loop | After loop | Bulkification |
| Error handling | Catch all, log once | Try-catch per event | Isolated failures |

**Pseudocode:**
```
1. Initialize: eventsToPublish = [], errorMessages = []
2. FOR EACH incomingEvent IN Trigger.new:
   a. TRY:
      i. Extract eventType and payload from incomingEvent
      ii. Query metadata for eventType
      iii. IF no metadata: log error, CONTINUE
      iv. Deserialize payload
      v. Process event based on type
      vi. IF nextEvent exists: collect in eventsToPublish
   b. CATCH exception:
      i. Log error to errorMessages
      ii. CONTINUE (don't stop processing)
3. IF eventsToPublish is not empty:
   a. results = EventBus.publish(eventsToPublish)
   b. Check results for errors, add to errorMessages
4. IF errorMessages is not empty:
   a. Log all errors to System.debug
   b. Create System_Log_Event__e
```

**Testing Requirements:**
- Test with 1 event (existing functionality)
- Test with 50 events (bulk processing)
- Test with mix of success and error events
- Test with invalid metadata
- Test with malformed payload
- Verify all events processed
- Verify bulk publish operation

---

### Design Specification 2: PlatformEventProcessor.RaiseTaskAndGenesysPE Refactoring

**Objective:** Accept collection of IDs, publish in bulk, maintain backward compatibility

**Affected Files:**
- `force-app/main/default/classes/PlatformEventProcessor.cls`
- `force-app/main/default/classes/QouteValiationHandler.cls`

**Changes Required:**

| Component | Current | New | Reason |
|-----------|---------|-----|--------|
| Method signature | `RaiseTaskAndGenesysPE(Id)` | `RaiseTaskAndGenesysPE(Set<Id>)` | Bulk interface |
| Backward compat | N/A | Overload with `RaiseTaskAndGenesysPE(Id)` | Don't break callers |
| Event creation | Single event | Loop to create events | Handle multiple IDs |
| Error handling | Minimal | Check each SaveResult | Detect failures |

**Implementation Steps:**

1. **Create new bulk method:**
   ```apex
   public static void RaiseTaskAndGenesysPE(Set<Id> quoteIds) {
       // Implementation as shown in Future State section
   }
   ```

2. **Add overload for backward compatibility:**
   ```apex
   @Deprecated
   public static void RaiseTaskAndGenesysPE(Id quoteId) {
       RaiseTaskAndGenesysPE(new Set<Id>{quoteId});
   }
   ```

3. **Update QouteValiationHandler:**
   - Add `Set<Id> quoteIdsNeedingEvents = new Set<Id>();` before loop
   - Replace `PlatformEventProcessor.RaiseTaskAndGenesysPE(qt.Id);` with `quoteIdsNeedingEvents.add(qt.Id);`
   - After loop: `if(!quoteIdsNeedingEvents.isEmpty()) PlatformEventProcessor.RaiseTaskAndGenesysPE(quoteIdsNeedingEvents);`

**Testing Requirements:**
- Test bulk method with 200 IDs
- Test backward compat method with single ID
- Test with empty Set
- Test with null parameter
- Verify single EventBus.publish() call
- Test error handling
- Integration test with QouteValiationHandler

---

### Design Specification 3: AutoSendEmailToServiceApprovers Refactoring

**Objective:** Publish one event per case, maintain audit trail

**Affected Files:**
- `force-app/main/default/classes/AutoSendEmailToServiceApprovers.cls`

**Changes Required:**

| Component | Current | New | Reason |
|-----------|---------|-----|--------|
| Event creation | 1 event total | 1 event per case | Complete audit trail |
| Event content | Single case ID | Specific case ID per event | Traceability |
| Publishing | Single publish | Single bulk publish | Still bulkified |
| Error tracking | Success only | Success and failure | Complete logging |

**Implementation Steps:**

1. **Track case-to-email mapping:**
   ```apex
   Map<Id, Id> caseIdToEmailMap = new Map<Id, Id>();
   // Populate during email building
   ```

2. **Create events per result:**
   ```apex
   List<System_Log_Event__e> emailEvents = new List<System_Log_Event__e>();
   for(Integer i = 0; i < results.size(); i++) {
       // Create event for each result
   }
   ```

3. **Bulk publish:**
   ```apex
   if(!emailEvents.isEmpty()) {
       EventBus.publish(emailEvents);
   }
   ```

**Testing Requirements:**
- Test with 1 case (baseline)
- Test with 100 cases (bulk)
- Test with mix of success and failure
- Verify event count = case count
- Verify correct case ID in each event
- Verify single publish operation

---

### Design Specification 4: Logger.saveLog() Deprecation

**Objective:** Standardize on bulkified logging pattern

**Affected Files:**
- `force-app/main/default/classes/Logger.cls`
- `force-app/main/default/classes/IntegrationHandlerUtil.cls`
- `force-app/main/default/classes/UpdateQuantityClientPrice.cls`

**Changes Required:**

| Component | Current | New | Reason |
|-----------|---------|-----|--------|
| saveLog() method | Active | @Deprecated | Discourage usage |
| Runtime warning | None | Debug log warning | Alert developers |
| Implementation | Direct DML | Redirect to saveLogs() | Standardize |
| Callers | Use saveLog() | Refactor to saveLogs() | Migration |

**Migration Steps:**

1. **Update Logger.cls:**
   - Add `@Deprecated` annotation
   - Add runtime warning
   - Redirect to saveLogs()

2. **Find all callers:**
   ```bash
   grep -r "\.saveLog()" force-app/main/default/classes/
   ```

3. **Refactor each caller:**
   ```apex
   // BEFORE:
   new Logger().log('Error', 'Message').saveLog();

   // AFTER:
   Logger logger = new Logger();
   logger.log('Error', 'Message');
   // ... collect more logs if needed ...
   logger.saveLogs();
   ```

**Testing Requirements:**
- Test deprecated method still works
- Verify warning appears in logs
- Test refactored callers
- Verify bulkified behavior

---

### Design Specification 5: PlatformEventPublisher Utility Creation

**Objective:** Create reusable bulkified event publishing framework

**Affected Files:**
- `force-app/main/default/classes/PlatformEventPublisher.cls` (NEW)
- `force-app/main/default/classes/PlatformEventPublisher_Test.cls` (NEW)

**Class Structure:**

```
PlatformEventPublisher
├── Private Variables
│   └── eventsToPublish (List<SObject>)
├── Core Methods
│   ├── addEvent(SObject)
│   ├── addEvents(List<SObject>)
│   ├── publishEvents()
│   ├── getQueuedEventCount()
│   └── clearQueue()
└── Convenience Methods
    ├── addSystemLogEvent(...)
    ├── addTaskAndGenesysEvent(...)
    ├── addTaskAndGenesysEvents(...)
    ├── addSTPProcessEvent(...)
    ├── addSTPProcessEvents(...)
    ├── addCaseToQuoteEvent(...)
    └── addTaskCreateUpdateEvent(...)
```

**Key Features:**
- Static methods for easy access
- Automatic queuing
- Chunking for large volumes (>2000 events)
- Comprehensive error handling
- Convenience methods for all Platform Event types

**Testing Requirements:**
- Test addEvent() with various event types
- Test publishEvents() with 1, 100, 3000 events
- Test chunking logic
- Test error handling
- Test convenience methods
- Test clearQueue()
- Test getQueuedEventCount()
- Integration tests with real triggers

---

## Database Design

### Platform Event Definitions

No changes to Platform Event definitions are required. All events maintain their current structure:

#### System_Log_Event__e
```
Fields:
- Level__c (Text) - Log level (INFO, WARN, ERROR, DEBUG)
- Message__c (Text) - Log message
- Parent_ID__c (Text) - Related record ID
- User_ID__c (Text) - User who triggered the log
- Timestamp__c (DateTime) - Log timestamp
```

#### Task_and_Genesys_Platform_Event__e
```
Fields:
- Payload__c (Text) - Quote ID or serialized data
```

#### STPProcessEvent__e
```
Fields:
- Payload__c (Text) - Quote ID
- PriceOnlyCall__c (Checkbox) - Price-only flag
```

#### CasetoQuoteAutomation__e
```
Fields:
- EventType__c (Text) - Event type from metadata
- PayLoad__c (Long Text Area) - JSON payload
```

#### Task_Create_Update_Event__e
```
Fields:
- CaseId__c (Text) - Case ID to refresh
- Refresh__c (Checkbox) - Refresh flag
```

### Custom Metadata Types

No changes to Custom Metadata Types are required.

### Data Migration

No data migration is required - this is a code-only refactoring.

---

## Integration Design

### Integration Points

#### 1. Genesys CTI Integration

**Platform Event:** Task_and_Genesys_Platform_Event__e

**Current Flow:**
```
Quote Validation → RaiseTaskAndGenesysPE() → EventBus → Genesys Subscriber → CTI Routing
```

**Future Flow:**
```
Quote Validation → Collect IDs → RaiseTaskAndGenesysPE(Set<Id>) → EventBus → Genesys Subscriber → CTI Routing
```

**Impact:**
- Event payload structure unchanged (backward compatible)
- Event subscribers unchanged (already handle bulk events)
- Integration endpoint unchanged
- CTI routing logic unchanged

**Testing Requirements:**
- Verify Genesys receives all events
- Verify event order doesn't break routing
- Test with 200 simultaneous events
- Coordinate with Genesys integration team

---

#### 2. Quote-to-Cash (CPQ) Integration

**Platform Event:** STPProcessEvent__e

**Current Flow:**
```
Pricing Request → RaiseSTPProcessEventPE() → EventBus → STP Subscriber → Quote Processing
```

**Future Flow:**
(No changes - already bulkified)

**Impact:**
- None - this pattern is already correct

---

#### 3. Case-to-Quote Automation

**Platform Event:** CasetoQuoteAutomation__e

**Current Flow:**
```
Case Update → Publish Event → Trigger (processes first only) → Next Event
```

**Future Flow:**
```
Case Update → Publish Event → Trigger (processes ALL) → Bulk Publish Next Events
```

**Impact:**
- All events now processed (no data loss)
- Multiple next events published in bulk
- Event chain completes fully

**Testing Requirements:**
- Test full case-to-quote workflow
- Verify all automation steps complete
- Test with 50 concurrent case updates
- Validate quote creation success rate

---

#### 4. Logging Infrastructure

**Platform Event:** System_Log_Event__e

**Current Flow:**
```
Various Sources → Logger.saveLog() / saveLogs() → EventBus → Log Subscriber → System_Log__c
```

**Future Flow:**
```
Various Sources → Logger.saveLogs() (standardized) → EventBus → Log Subscriber → System_Log__c
```

**Impact:**
- Improved consistency
- Complete audit trail
- No functional changes to subscribers

---

### Integration Testing Strategy

1. **Genesys CTI:** Coordinate with integration team, test in isolated sandbox
2. **CPQ:** Validate quote processing, ensure no regression
3. **Case Automation:** End-to-end testing of case-to-quote flow
4. **Logging:** Verify log records created correctly

---

## Security Design

### Security Considerations

#### 1. Sharing Model

**Platform Events:** Platform Events bypass sharing rules (by design)

**Implication:** Event subscribers must enforce sharing/security

**No changes required:** Event subscribers already implement security

---

#### 2. Field-Level Security

**Platform Events:** Do not enforce FLS (by design)

**Implication:** Sensitive data in events visible to subscribers

**No changes required:** Current event payloads already designed appropriately

---

#### 3. CRUD Permissions

**Platform Events:** Require "Create" permission on Platform Event object

**No changes required:** Existing code already has permissions

---

#### 4. Code Security

**Static Analysis:** Run Checkmarx/PMD on all refactored code

**Security Review:** Required for Phase 1 completion

**No Security Concerns Identified:**
- No SOQL injection vectors
- No XSS vulnerabilities
- No sensitive data exposure
- No authentication/authorization bypasses

---

## Error Handling and Logging

### Error Handling Strategy

#### 1. Platform Event Publish Failures

**Strategy:** Check Database.SaveResult, log failures, continue processing

**Implementation:**
```apex
List<Database.SaveResult> results = EventBus.publish(events);

for(Integer i = 0; i < results.size(); i++) {
    if(!results[i].isSuccess()) {
        String errorMsg = 'Failed to publish event: ' + events[i];
        for(Database.Error err : results[i].getErrors()) {
            errorMsg += ' | ' + err.getMessage();
        }
        System.debug(LoggingLevel.ERROR, errorMsg);
        Logger.error('ClassName', errorMsg).saveLogs();
    }
}
```

**Rationale:**
- Individual event failures don't stop processing
- All errors logged for troubleshooting
- System continues operating

---

#### 2. Trigger Execution Errors

**Strategy:** Try-catch per event, continue processing other events

**Implementation:**
```apex
for(Event__e evt : Trigger.new) {
    try {
        // Process event
    } catch(Exception ex) {
        errorMessages.add('Event: ' + evt + ' Error: ' + ex.getMessage());
        continue; // Don't stop processing
    }
}
```

**Rationale:**
- One bad event doesn't break entire batch
- Maximizes throughput
- All errors logged

---

#### 3. Null/Empty Parameter Handling

**Strategy:** Early return with no-op

**Implementation:**
```apex
public static void RaiseTaskAndGenesysPE(Set<Id> quoteIds) {
    if(quoteIds == null || quoteIds.isEmpty()) {
        return; // No-op
    }
    // Process...
}
```

**Rationale:**
- Defensive programming
- Prevents null pointer exceptions
- Clear intent

---

### Logging Standards

#### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| **DEBUG** | Detailed debugging info | 'Processing 200 events' |
| **INFO** | Normal operations | 'Successfully published 200 events' |
| **WARN** | Potential issues | 'DEPRECATED: Use saveLogs() instead' |
| **ERROR** | Failures | 'Failed to publish event: [details]' |

#### Log Format

```apex
System.debug(LoggingLevel.ERROR,
    '[ClassName.methodName] Error message | Details: [details] | StackTrace: [trace]'
);
```

#### System_Log_Event__e Usage

Create log events for:
- ✅ Platform Event publish failures
- ✅ Business-critical errors
- ✅ Integration failures
- ✅ Data validation errors

Do NOT create log events for:
- ❌ Debug-level information
- ❌ Normal processing
- ❌ Validation errors shown to users

---

## Performance Design

### Performance Targets

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| **EventBus.publish() calls** | ~450/hour | <25/hour | Event Monitoring |
| **Trigger execution time** | TBD | <500ms for 200 records | Debug logs |
| **CPU time** | TBD | <5000ms per transaction | Debug logs |
| **Heap size** | TBD | <3MB per transaction | Debug logs |

### Performance Optimization Strategies

#### 1. Bulk Processing

**Strategy:** Process all records together, not individually

**Implementation:**
- Loop to collect IDs/data
- Single operation after loop (publish, DML, etc.)

**Benefit:** 95-99% reduction in operations

---

#### 2. Collection Types

**Strategy:** Use appropriate collection types

| Use Case | Collection Type | Reason |
|----------|----------------|--------|
| Unique IDs | `Set<Id>` | Automatic deduplication |
| Ordered events | `List<SObject>` | Maintain order |
| Key-value lookup | `Map<Id, SObject>` | O(1) lookup |

---

#### 3. Query Optimization

**Strategy:** Query once, reuse data

**Implementation:**
```apex
// GOOD: Query once outside loop
Map<Id, SBQQ__Quote__c> quoteMap = new Map<Id, SBQQ__Quote__c>(
    [SELECT Id, Name FROM SBQQ__Quote__c WHERE Id IN :quoteIds]
);

for(Id quoteId : quoteIds) {
    SBQQ__Quote__c quote = quoteMap.get(quoteId);
    // Use quote data
}

// BAD: Query inside loop
for(Id quoteId : quoteIds) {
    SBQQ__Quote__c quote = [SELECT Id, Name FROM SBQQ__Quote__c WHERE Id = :quoteId];
}
```

---

#### 4. Chunking for Large Volumes

**Strategy:** Process in chunks if exceeding limits

**Implementation:**
```apex
Integer MAX_EVENTS = 2000;
Integer totalEvents = eventsToPublish.size();

for(Integer i = 0; i < totalEvents; i += MAX_EVENTS) {
    Integer endIndex = Math.min(i + MAX_EVENTS, totalEvents);
    List<SObject> chunk = new List<SObject>();
    for(Integer j = i; j < endIndex; j++) {
        chunk.add(eventsToPublish[j]);
    }
    EventBus.publish(chunk);
}
```

**Benefit:** Safely handle >2000 events without limit exceptions

---

### Performance Testing

**Load Test Scenarios:**
1. 1 record (baseline)
2. 200 records (max trigger batch)
3. 2000 records (chunking threshold)
4. 5000 records (multiple chunks)

**Measurements:**
- CPU time per scenario
- Heap size per scenario
- EventBus.publish() call count
- Transaction execution time

**Acceptance Criteria:**
- All scenarios complete successfully
- No governor limit exceptions
- <500ms execution time for 200 records
- <5000ms CPU time per transaction

---

## Testing Strategy

### Test Coverage Requirements

**Minimum Coverage:** 85% on all modified classes

**Target Coverage:** 90%+

### Unit Testing

#### Test Class Structure

For each modified class, create/update test class:

| Class | Test Class |
|-------|------------|
| PlatformEventProcessor | PlatformEventProcessorTest |
| PlatformEventPublisher | PlatformEventPublisher_Test |
| AutoSendEmailToServiceApprovers | AutoSendEmailToServiceApproversTest |
| Logger | LoggerTest |

#### Test Scenarios

**For each method:**
1. ✅ Happy path (normal execution)
2. ✅ Bulk processing (200 records)
3. ✅ Null parameter
4. ✅ Empty collection parameter
5. ✅ Error scenario
6. ✅ Governor limit approach (large volume)

**Example Test: RaiseTaskAndGenesysPE**
```apex
@isTest
public class PlatformEventProcessorTest {

    @isTest
    static void testRaiseTaskAndGenesysPE_SingleId() {
        // Test backward compat method
        Test.startTest();
        PlatformEventProcessor.RaiseTaskAndGenesysPE(fakeQuoteId);
        Test.stopTest();

        // Verify event delivered
        // (Note: Can't query Platform Events, so verify no exceptions)
    }

    @isTest
    static void testRaiseTaskAndGenesysPE_BulkIds() {
        Set<Id> quoteIds = new Set<Id>();
        for(Integer i = 0; i < 200; i++) {
            quoteIds.add(fflib_IDGenerator.generate(SBQQ__Quote__c.SObjectType));
        }

        Test.startTest();
        PlatformEventProcessor.RaiseTaskAndGenesysPE(quoteIds);
        Test.stopTest();

        // Verify no exceptions, event count via Test.getEventBus().getEventDeliveryCount()
    }

    @isTest
    static void testRaiseTaskAndGenesysPE_NullParameter() {
        Test.startTest();
        PlatformEventProcessor.RaiseTaskAndGenesysPE((Set<Id>)null);
        Test.stopTest();

        // Verify graceful handling (no exception)
    }

    @isTest
    static void testRaiseTaskAndGenesysPE_EmptySet() {
        Test.startTest();
        PlatformEventProcessor.RaiseTaskAndGenesysPE(new Set<Id>());
        Test.stopTest();

        // Verify graceful handling (no exception)
    }
}
```

---

### Integration Testing

#### Integration Test Scenarios

1. **End-to-End Quote Validation:**
   - Create 100 quotes
   - Update to trigger validation
   - Verify Task_and_Genesys events published
   - Verify event count = quote count
   - Verify single EventBus.publish() call

2. **End-to-End Case-to-Quote:**
   - Create 50 cases
   - Publish CasetoQuoteAutomation events
   - Verify all 50 events processed
   - Verify quotes created
   - Verify no data loss

3. **End-to-End Approval Email:**
   - Trigger approval workflow for 100 cases
   - Verify emails sent
   - Verify 100 System_Log_Event__e published
   - Verify audit trail complete

4. **Genesys CTI Integration:**
   - Update quotes to trigger CTI routing
   - Verify events reach Genesys
   - Verify CTI routing functions correctly
   - Coordinate with integration team

#### Integration Test Environment

- **Sandbox:** Full copy sandbox with production data
- **Integrations:** Genesys CTI connected
- **Users:** Test with various profiles/permissions
- **Volume:** Test with production-like volumes

---

### Performance Testing

#### Performance Test Plan

1. **Baseline Measurement:**
   - Run current code with 200 records
   - Capture CPU time, heap size, publish count
   - Document as baseline

2. **Post-Fix Measurement:**
   - Run refactored code with 200 records
   - Capture same metrics
   - Compare to baseline

3. **Load Testing:**
   - Test with 1, 10, 100, 200, 500 records
   - Plot performance curves
   - Verify linear scaling

#### Performance Test Tools

- **Developer Console:** Debug logs for detailed metrics
- **Event Monitoring:** API call tracking
- **Custom Dashboard:** Real-time monitoring

---

### User Acceptance Testing (UAT)

#### UAT Scenarios

1. **Quote Validation (Business User):**
   - Create and validate quotes
   - Verify normal functionality
   - Verify no performance degradation

2. **Case Management (CSR):**
   - Process cases end-to-end
   - Verify case-to-quote automation works
   - Verify task creation/routing

3. **Approval Process (Approver):**
   - Receive and respond to approval emails
   - Verify emails received
   - Verify audit trail visible

#### UAT Acceptance Criteria

- ✅ All business processes function normally
- ✅ No user-visible changes (backward compatible)
- ✅ No performance degradation
- ✅ No increase in errors/failures

---

### Regression Testing

#### Regression Test Scope

Test all triggers/classes that:
- Publish Platform Events
- Subscribe to Platform Events
- Use modified classes

#### Regression Test Cases

1. All existing test classes must pass
2. Code coverage must not decrease
3. No new PMD violations
4. No new security vulnerabilities

---

## Deployment Plan

### Deployment Strategy

**Approach:** Phased deployment with rollback capability

**Environments:**
1. DEV Sandbox (development)
2. QA Sandbox (quality assurance)
3. UAT Sandbox (user acceptance testing)
4. PROD (production)

### Deployment Phases

#### Phase 1: DEV Sandbox Deployment (Week 1)

**Activities:**
- Deploy all code changes
- Run unit tests
- Validate test coverage
- Fix any deployment issues

**Success Criteria:**
- Deployment successful
- All tests pass
- 85%+ coverage achieved

---

#### Phase 2: QA Sandbox Deployment (Week 2)

**Activities:**
- Deploy from DEV to QA
- Execute QA test plan
- Performance testing
- Integration testing

**Success Criteria:**
- All QA tests pass
- Performance targets met
- No critical/high defects

---

#### Phase 3: UAT Sandbox Deployment (Week 3)

**Activities:**
- Deploy from QA to UAT
- Business user testing
- End-to-end workflow validation
- Stakeholder demos

**Success Criteria:**
- UAT sign-off received
- No business-critical issues
- User acceptance achieved

---

#### Phase 4: PROD Deployment (Week 5)

**Activities:**
- Final code review
- CAB approval
- Production deployment (maintenance window)
- Post-deployment validation
- 1 week monitoring

**Success Criteria:**
- Deployment successful
- No rollback required
- Metrics confirm improvements
- No production incidents

---

### Deployment Checklist

**Pre-Deployment:**
- [ ] All code peer reviewed
- [ ] All tests passing (85%+ coverage)
- [ ] Security review complete
- [ ] UAT sign-off received
- [ ] CAB approval obtained
- [ ] Deployment runbook prepared
- [ ] Rollback plan tested
- [ ] Stakeholders notified
- [ ] Maintenance window scheduled

**During Deployment:**
- [ ] Backup current code
- [ ] Deploy via Change Set or SFDX
- [ ] Run all tests in production
- [ ] Smoke test critical workflows
- [ ] Verify Platform Event dashboard

**Post-Deployment:**
- [ ] Monitor for 1 hour (critical period)
- [ ] Check error logs
- [ ] Validate metrics (EventBus.publish() count)
- [ ] Confirm no user issues
- [ ] Notify stakeholders of success
- [ ] Begin 1-week monitoring period

---

### Deployment Commands

**Using Salesforce DX:**
```bash
# Validate deployment (check-only)
sfdx force:source:deploy --manifest manifest/package.xml \
  --checkonly --testlevel RunLocalTests --targetusername PROD

# Deploy to production
sfdx force:source:deploy --manifest manifest/package.xml \
  --testlevel RunLocalTests --targetusername PROD

# Quick deploy (after successful validation)
sfdx force:source:deploy --jobid <validation-job-id> --targetusername PROD
```

**Using Change Sets:**
1. Create outbound change set in UAT
2. Upload to PROD
3. Validate in PROD
4. Deploy during maintenance window

---

## Rollback Strategy

### Rollback Triggers

Initiate rollback if:
- ❌ Critical production error occurs
- ❌ Data loss detected
- ❌ Integration failure (Genesys)
- ❌ Performance degradation >50%
- ❌ Governor limit exceptions
- ❌ Business process failure

### Rollback Procedure

**Immediate Rollback (Within 1 hour):**

1. **Notify stakeholders** (5 minutes)
   - Executive sponsor
   - Project team
   - Business users

2. **Execute rollback** (15 minutes)
   ```bash
   # Deploy previous version from backup
   sfdx force:source:deploy --manifest manifest/package-backup.xml \
     --targetusername PROD
   ```

3. **Validate rollback** (15 minutes)
   - Run smoke tests
   - Check critical workflows
   - Verify Platform Events publishing

4. **Monitor** (25 minutes)
   - Check error logs
   - Verify no new issues
   - Confirm stabilization

**Post-Rollback:**
- Root cause analysis (24 hours)
- Fix issue in DEV
- Re-test in QA/UAT
- Plan re-deployment

---

### Rollback Testing

**Test rollback procedure in UAT:**
1. Deploy refactored code
2. Validate works correctly
3. Execute rollback procedure
4. Validate original code works
5. Document rollback time and steps

**Success Criteria:**
- Rollback completes in <30 minutes
- No data loss during rollback
- Original functionality restored

---

## Appendices

### Appendix A: File Inventory

#### Files Modified

| File Path | Type | Changes | Lines Changed |
|-----------|------|---------|---------------|
| `force-app/main/default/triggers/CasetoQuoteAutomation.trigger` | Trigger | Process all events, bulk publish | ~50 |
| `force-app/main/default/classes/PlatformEventProcessor.cls` | Class | Add bulk method, overload | ~30 |
| `force-app/main/default/classes/QouteValiationHandler.cls` | Class | Collect IDs, call bulk method | ~10 |
| `force-app/main/default/classes/AutoSendEmailToServiceApprovers.cls` | Class | Publish per-case events in bulk | ~40 |
| `force-app/main/default/classes/Logger.cls` | Class | Deprecate saveLog() | ~10 |

#### Files Created

| File Path | Type | Purpose | Lines |
|-----------|------|---------|-------|
| `force-app/main/default/classes/PlatformEventPublisher.cls` | Class | Centralized event publishing utility | ~300 |
| `force-app/main/default/classes/PlatformEventPublisher_Test.cls` | Test Class | Test coverage for utility | ~200 |

#### Test Files Updated

| File Path | Changes |
|-----------|---------|
| `PlatformEventProcessorTest.cls` | Add bulk method tests |
| `AutoSendEmailToServiceApproversTest.cls` | Update for per-case events |
| `LoggerTest.cls` | Test deprecated method warning |

---

### Appendix B: Dependencies

#### Internal Dependencies

- Logger class (logging)
- Constant_Util class (constants)
- SystemObjectSelector class (SOQL)
- RecurrsiveTriggerHandler class (recursion control)

#### External Dependencies

- Genesys CTI system (integration)
- Salesforce CPQ (quote processing)
- Email delivery system

---

### Appendix C: Code Review Checklist

**For each code change:**
- [ ] Bulkified (processes 200 records)
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Comments/documentation added
- [ ] Test coverage >85%
- [ ] No SOQL in loops
- [ ] No DML in loops
- [ ] No hard-coded IDs
- [ ] Follows naming conventions
- [ ] Passes PMD/Checkmarx scan

---

### Appendix D: Monitoring and Alerting

#### Metrics to Monitor

**Daily:**
- EventBus.publish() API call count
- Platform Event volume by type
- Event publish failure rate
- Trigger execution time (p50, p95, p99)

**Weekly:**
- Trend analysis
- Comparison to baseline
- Capacity planning

#### Alerts to Configure

| Metric | Threshold | Action |
|--------|-----------|--------|
| EventBus.publish() calls | >100/hour | Email tech lead |
| Event publish failures | >1% | Email tech lead |
| Trigger execution time | >1000ms | Email tech lead |
| Governor limit exceptions | Any | Page on-call |

---

### Appendix E: Glossary

| Term | Definition |
|------|------------|
| **Bulkification** | Design pattern to process multiple records in single operation |
| **Platform Event** | Salesforce event-driven messaging framework (__e suffix) |
| **EventBus** | Salesforce API for publishing Platform Events |
| **Governor Limits** | Salesforce runtime limits (SOQL, DML, CPU, etc.) |
| **Trigger Context** | Variables available in trigger (Trigger.new, Trigger.old, etc.) |
| **SaveResult** | Salesforce object containing DML/event publish result |

---

## Document Approval

**This Technical Design Document must be reviewed and approved before implementation begins.**

| Approver | Title | Signature | Date |
|----------|-------|-----------|------|
| **Technical Lead** | [Name] | _________________ | ________ |
| **Solution Architect** | [Name] | _________________ | ________ |
| **Security Team** | [Name] | _________________ | ________ |
| **QA Lead** | [Name] | _________________ | ________ |
| **Project Manager** | [Name] | _________________ | ________ |

---

**END OF TECHNICAL DESIGN DOCUMENT**

---

## Document Revision History

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 0.1 | 2026-01-18 | Technical Architecture Team | Initial draft | - |
| 1.0 | 2026-01-18 | Technical Architecture Team | Complete design | Pending |

**Next Review Date:** Upon project completion or significant design change

---

*This document is confidential and proprietary. Distribution is limited to project stakeholders and authorized personnel only.*
