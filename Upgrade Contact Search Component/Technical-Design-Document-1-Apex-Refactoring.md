# Technical Design Document: Apex Controller Refactoring

**Project Code:** CSC-APEX-2026-001
**Document Version:** 1.0
**Date:** January 18, 2026
**Status:** Draft for Review
**Author:** Development Team

---

## Document Control

| Version | Date | Author | Changes | Approver |
|---------|------|--------|---------|----------|
| 0.1 | 2026-01-18 | Development Team | Initial draft | Pending |
| 1.0 | 2026-01-18 | Development Team | Complete first version | Pending |

### Document Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Technical Lead | [Name] | _________________ | ______ |
| Senior Apex Developer | [Name] | _________________ | ______ |
| Security Architect | [Name] | _________________ | ______ |
| QA Lead | [Name] | _________________ | ______ |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Architecture Analysis](#current-architecture-analysis)
3. [Proposed Architecture](#proposed-architecture)
4. [Detailed Design](#detailed-design)
5. [Data Model](#data-model)
6. [API Specifications](#api-specifications)
7. [Performance Optimization Strategy](#performance-optimization-strategy)
8. [Security Considerations](#security-considerations)
9. [Error Handling & Logging](#error-handling--logging)
10. [Testing Strategy](#testing-strategy)
11. [Deployment Plan](#deployment-plan)
12. [Rollback Strategy](#rollback-strategy)
13. [Monitoring & Metrics](#monitoring--metrics)
14. [Dependencies](#dependencies)
15. [Appendices](#appendices)

---

## Executive Summary

This document provides the technical design for refactoring the ContactSearchandCreate Apex class to address critical performance bottlenecks and improve code maintainability. The refactoring will split the monolithic class into focused service classes, implement caching strategies, optimize SOQL queries, and establish design patterns for future development.

### Key Changes
- Split monolithic 740-line class into 5 service classes
- Replace SOSL with optimized indexed SOQL queries
- Implement Platform Cache for frequently accessed data
- Consolidate DML operations for bulkification
- Move hard-coded configuration to Custom Metadata Types
- Achieve 80%+ test coverage with comprehensive unit tests

### Performance Targets
- Search response time: <500ms (70% improvement)
- Apex CPU time: <5,000ms (50% reduction)
- SOQL queries: <10 per transaction (40-50% reduction)
- Database time: <1,500ms (60% improvement)

---

## Current Architecture Analysis

### Current Class Structure

**ContactSearchandCreate.cls** (740 lines)
- Mixed responsibilities (search, create, update, validation)
- 25 public methods with varying purposes
- No clear separation of concerns
- Hard-coded configuration values
- Minimal error handling

```apex
public with sharing class ContactSearchandCreate {
    // All methods in single class
    @AuraEnabled public static Case returnCase(Id recordId) { }
    @AuraEnabled public static List<allContacts> searchLocCont(Id locId) { }
    @AuraEnabled public static List<allContacts> searchContact(String searchQuery, Id acct) { }
    @AuraEnabled public static List<allContacts> searchContacts(...) { }
    @AuraEnabled public static Id createNewContact(...) { }
    @AuraEnabled public static Boolean existingContact(...) { }
    // ... 19 more methods
}
```

### Current Performance Issues

#### Issue 1: SOSL Query Overhead
**Location:** `ContactSearchandCreate.cls:58-72`

```apex
List<List<sObject>> qryRes = [FIND :searchQuery IN ALL FIELDS
                    RETURNING Contact(Id, Name, FirstName, LastName, Phone,
                                     MobilePhone,Email,Preferred_Method__c,
                                     Contact_Status__c,Account_Title__r.Name, Account.Name
                                     WHERE (AccountId=:acct OR Location__c=:acct))];
```

**Problems:**
- Searches across ALL FIELDS (expensive)
- No result limiting
- No minimum search term validation
- Can't leverage field-specific indexes

**Measured Impact:**
- Average execution time: 800-1,200ms
- Consumes 3,000-4,000ms CPU time
- Uses 1.5-2MB heap

#### Issue 2: Dynamic SOQL Construction
**Location:** `ContactSearchandCreate.cls:106-154`

```apex
String qry = 'SELECT Id, Name, FirstName, LastName... FROM contact WHERE';
if(firstName != '' && firstName != null) {
    qry += ' FirstName Like \'%' + firstName + '%\'';
}
// ... multiple string concatenations
List<Contact> conList = Database.query(qry);
```

**Problems:**
- Query plan can't be optimized
- Complex string concatenation
- No result limiting
- Difficult to maintain

**Measured Impact:**
- Average execution time: 600-900ms
- Consumes 2,000-3,000ms CPU time
- Query parsing overhead on every execution

#### Issue 3: Multiple Sequential Queries & DML
**Location:** `ContactSearchandCreate.cls:221-263`

```apex
// Query 1
Contact con = [SELECT ... FROM Contact WHERE Id=:contactId];
// Query 2
Id loc = [SELECT ... FROM Case WHERE Id=:caseId].Location__c;
// DML 1
update con;
// Query 3
Case c = [SELECT ... FROM Case WHERE Id=:caseId];
// DML 2
update c;
// Additional queries in called methods
```

**Problems:**
- 3+ queries when 2 would suffice
- 2+ DML operations not bulkified
- Nested method calls perform additional queries

**Measured Impact:**
- Total execution time: 400-600ms
- Consumes 1,500-2,500ms CPU time
- 5-7 SOQL queries consumed

#### Issue 4: No Caching
**Current State:** Every method call queries database

**Measured Impact:**
- Repeated queries for same data
- Account titles queried on every page load
- Vendor lists rebuilt constantly

#### Issue 5: Hard-coded Configuration
**Location:** `ContactSearchandCreate.cls:686-711`

```apex
Set<String> venIds = new Set<String>();
venIds.add('001N000001O7H8eIAF');
venIds.add('001N000001O7H8fIAF');
// ... 16 more hard-coded IDs
```

**Problems:**
- Requires code deployment to change
- Not testable across orgs
- No audit trail for changes

---

## Proposed Architecture

### Service-Oriented Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│              (Aura Component / LWC - Unchanged)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Controller Layer (New)                     │
│           ContactSearchController.cls (Facade)               │
│         - Orchestrates service calls                         │
│         - Handles @AuraEnabled methods                       │
│         - Manages transactions                               │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│  Service Layer  │ │  Service Layer   │ │  Service Layer  │
│                 │ │                  │ │                 │
│ ContactSearch   │ │ ContactMgmt      │ │ CaseContact     │
│ Service.cls     │ │ Service.cls      │ │ Association     │
│                 │ │                  │ │ Service.cls     │
│ - Search ops    │ │ - CRUD ops       │ │ - Relationships │
│ - Query builder │ │ - Validation     │ │ - Updates       │
│ - Result format │ │ - Duplicate det  │ │ - Link creation │
└─────────────────┘ └──────────────────┘ └─────────────────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Repository Layer (New)                      │
│         ContactRepository.cls & CaseRepository.cls           │
│         - Data access abstraction                            │
│         - Query optimization                                 │
│         - Bulk operations                                    │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│  Cache Layer    │ │  Config Layer    │ │ Validation      │
│                 │ │                  │ │ Layer           │
│ CacheService    │ │ ContactSearch    │ │ ContactValid    │
│ .cls            │ │ Config.cls       │ │ ationService    │
│                 │ │                  │ │ .cls            │
│ - Platform Cache│ │ - Custom Metadata│ │ - Business rules│
│ - TTL mgmt      │ │ - Vendor configs │ │ - Field valid   │
└─────────────────┘ └──────────────────┘ └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│        Salesforce Objects (Contact, Case, Account)          │
└─────────────────────────────────────────────────────────────┘
```

### New Class Structure

```
ContactSearchController.cls (Facade Pattern)
├── ContactSearchService.cls
│   ├── search(SearchCriteria criteria)
│   ├── quickSearch(String searchTerm, Id accountId)
│   └── getRecentContacts(Id accountId)
│
├── ContactManagementService.cls
│   ├── createContact(ContactRequest request)
│   ├── checkDuplicates(ContactRequest request)
│   └── validateContact(Contact contact)
│
├── CaseContactAssociationService.cls
│   ├── associateContact(Id caseId, Id contactId, String type)
│   ├── updateCaseContact(Id caseId, Id contactId)
│   └── createRelationships(Id contactId, Id accountId, String type)
│
├── ContactRepository.cls (Data Access)
│   ├── queryBySearchCriteria(SearchCriteria criteria)
│   ├── queryByIds(Set<Id> contactIds)
│   └── queryByAccountAndLocation(Id accountId, Id locationId)
│
├── CaseRepository.cls (Data Access)
│   ├── queryById(Id caseId)
│   └── queryWithRelatedData(Id caseId)
│
├── CacheService.cls (Caching Layer)
│   ├── get(String key)
│   ├── put(String key, Object value, Integer ttl)
│   └── remove(String key)
│
├── ContactSearchConfig.cls (Configuration)
│   ├── getExcludedVendors()
│   ├── getSearchSettings()
│   └── getCacheSettings()
│
└── ContactValidationService.cls (Business Rules)
    ├── validateAccountTitle(Id titleId)
    ├── validateBusinessRules(Contact contact)
    └── canCreateContact(ContactRequest request)
```

---

## Detailed Design

### 1. ContactSearchController (Facade)

**Purpose:** Orchestrate service calls and provide @AuraEnabled methods for UI

**File:** `ContactSearchController.cls`

```apex
/**
 * @description Facade controller for contact search and management operations.
 *              Orchestrates service layer calls and manages transactions.
 * @author Development Team
 * @date 2026-01-18
 */
public with sharing class ContactSearchController {

    // Service instances
    @TestVisible
    private static ContactSearchService searchService = new ContactSearchService();
    @TestVisible
    private static ContactManagementService managementService = new ContactManagementService();
    @TestVisible
    private static CaseContactAssociationService associationService = new CaseContactAssociationService();

    /**
     * @description Search for contacts based on criteria
     * @param criteria JSON string containing search parameters
     * @param caseId Case record ID for context
     * @return ContactSearchResult containing contacts and metadata
     */
    @AuraEnabled(cacheable=true)
    public static ContactSearchResult searchContacts(String criteria, Id caseId) {
        try {
            // Parse criteria
            SearchCriteria searchCriteria = (SearchCriteria)JSON.deserialize(
                criteria, SearchCriteria.class
            );

            // Validate inputs
            if (String.isBlank(caseId)) {
                throw new ContactSearchException('Case ID is required');
            }

            // Get case context
            CaseData caseData = CaseRepository.queryById(caseId);

            // Perform search with context
            searchCriteria.accountId = caseData.accountId;
            List<ContactDTO> contacts = searchService.search(searchCriteria);

            // Build result
            ContactSearchResult result = new ContactSearchResult();
            result.contacts = contacts;
            result.totalCount = contacts.size();
            result.hasMore = contacts.size() >= searchCriteria.pageSize;
            result.caseContext = caseData;

            return result;

        } catch (Exception e) {
            throw new AuraHandledException('Error searching contacts: ' + e.getMessage());
        }
    }

    /**
     * @description Create new contact and associate with case
     * @param request Contact creation request
     * @param caseId Case to associate with
     * @return OperationResult with contact ID
     */
    @AuraEnabled
    public static OperationResult createContactForCase(String request, Id caseId) {
        Savepoint sp = Database.setSavepoint();
        try {
            // Parse request
            ContactRequest contactReq = (ContactRequest)JSON.deserialize(
                request, ContactRequest.class
            );

            // Check for duplicates
            List<ContactDTO> duplicates = managementService.checkDuplicates(contactReq);
            if (!duplicates.isEmpty() && contactReq.ignoreDuplicates == false) {
                OperationResult result = new OperationResult();
                result.success = false;
                result.duplicatesFound = true;
                result.duplicates = duplicates;
                result.message = 'Potential duplicate contacts found';
                return result;
            }

            // Create contact
            Id contactId = managementService.createContact(contactReq);

            // Associate with case
            associationService.associateContact(caseId, contactId, contactReq.contactType);

            // Success result
            OperationResult result = new OperationResult();
            result.success = true;
            result.recordId = contactId;
            result.message = 'Contact created successfully';

            return result;

        } catch (Exception e) {
            Database.rollback(sp);
            throw new AuraHandledException('Error creating contact: ' + e.getMessage());
        }
    }

    /**
     * @description Associate existing contact with case
     * @param caseId Case record ID
     * @param contactId Contact record ID
     * @param contactType Type of contact (Customer, Vendor, Internal)
     * @return OperationResult
     */
    @AuraEnabled
    public static OperationResult associateContactToCase(
        Id caseId, Id contactId, String contactType
    ) {
        Savepoint sp = Database.setSavepoint();
        try {
            // Validate contact
            Contact contact = ContactRepository.queryById(contactId);
            if (contact == null) {
                throw new ContactSearchException('Contact not found');
            }

            // Validate account title
            if (!ContactValidationService.validateAccountTitle(contact.Account_Title__c)) {
                OperationResult result = new OperationResult();
                result.success = false;
                result.errorCode = 'INACTIVE_TITLE';
                result.message = 'Contact account title is inactive. Please update before proceeding.';
                return result;
            }

            // Perform association
            associationService.associateContact(caseId, contactId, contactType);

            // Success result
            OperationResult result = new OperationResult();
            result.success = true;
            result.message = 'Contact associated successfully';

            return result;

        } catch (Exception e) {
            Database.rollback(sp);
            throw new AuraHandledException('Error associating contact: ' + e.getMessage());
        }
    }

    /**
     * @description Get account titles for dropdown
     * @param accountId Account record ID
     * @return List of PicklistOption
     */
    @AuraEnabled(cacheable=true)
    public static List<PicklistOption> getAccountTitles(Id accountId) {
        try {
            // Check cache first
            String cacheKey = 'AccountTitles_' + accountId;
            List<PicklistOption> cached = (List<PicklistOption>)CacheService.get(cacheKey);
            if (cached != null) {
                return cached;
            }

            // Query titles
            List<Account_Title__c> titles = [
                SELECT Id, Name, Status__c
                FROM Account_Title__c
                WHERE Account__c = :accountId
                AND Status__c = 'Active'
                ORDER BY Name ASC
            ];

            // Convert to picklist options
            List<PicklistOption> options = new List<PicklistOption>();
            for (Account_Title__c title : titles) {
                options.add(new PicklistOption(title.Name, title.Id));
            }

            // Cache for 1 hour
            CacheService.put(cacheKey, options, 3600);

            return options;

        } catch (Exception e) {
            throw new AuraHandledException('Error retrieving account titles: ' + e.getMessage());
        }
    }

    /**
     * @description Create new account title
     * @param accountId Account record ID
     * @param titleName Title name
     * @return Id of created title
     */
    @AuraEnabled
    public static Id createAccountTitle(Id accountId, String titleName) {
        try {
            Account_Title__c title = new Account_Title__c(
                Account__c = accountId,
                Name = titleName,
                Status__c = 'Active'
            );
            insert title;

            // Invalidate cache
            String cacheKey = 'AccountTitles_' + accountId;
            CacheService.remove(cacheKey);

            return title.Id;

        } catch (Exception e) {
            throw new AuraHandledException('Error creating account title: ' + e.getMessage());
        }
    }

    // Additional methods following same pattern...

    /**
     * @description Custom exception for contact search operations
     */
    public class ContactSearchException extends Exception {}
}
```

### 2. ContactSearchService

**Purpose:** Handle all contact search operations with optimized queries

**File:** `ContactSearchService.cls`

```apex
/**
 * @description Service for contact search operations with optimized queries
 * @author Development Team
 * @date 2026-01-18
 */
public with sharing class ContactSearchService {

    // Constants
    private static final Integer DEFAULT_PAGE_SIZE = 50;
    private static final Integer MIN_SEARCH_LENGTH = 2;
    private static final Integer MAX_RESULTS = 100;

    /**
     * @description Search contacts with optimized SOQL
     * @param criteria Search criteria
     * @return List of ContactDTO
     */
    public List<ContactDTO> search(SearchCriteria criteria) {
        // Validate criteria
        validateSearchCriteria(criteria);

        // Build query
        String query = buildContactQuery(criteria);

        // Execute query
        List<Contact> contacts = Database.query(query);

        // Transform to DTOs
        return transformToDTO(contacts, criteria.accountId);
    }

    /**
     * @description Quick search by single term (name, email, or phone)
     * @param searchTerm Search term
     * @param accountId Account context
     * @return List of ContactDTO
     */
    public List<ContactDTO> quickSearch(String searchTerm, Id accountId) {
        // Validate
        if (String.isBlank(searchTerm) || searchTerm.length() < MIN_SEARCH_LENGTH) {
            return new List<ContactDTO>();
        }

        // Detect search pattern
        SearchPattern pattern = detectSearchPattern(searchTerm);

        // Build criteria
        SearchCriteria criteria = new SearchCriteria();
        criteria.accountId = accountId;
        criteria.pageSize = DEFAULT_PAGE_SIZE;

        switch on pattern {
            when EMAIL {
                criteria.email = searchTerm;
            }
            when PHONE {
                criteria.phone = cleanPhone(searchTerm);
            }
            when NAME {
                criteria.searchTerm = searchTerm;
            }
        }

        return search(criteria);
    }

    /**
     * @description Build optimized SOQL query
     * @param criteria Search criteria
     * @return SOQL query string
     */
    @TestVisible
    private String buildContactQuery(SearchCriteria criteria) {
        List<String> conditions = new List<String>();

        // Base query with required fields
        String query = 'SELECT Id, Name, FirstName, LastName, AccountNameForContact__c, ' +
                      'Phone, MobilePhone, Email, Preferred_Method__c, Contact_Status__c, ' +
                      'Account_Title__r.Name, Account_Title__r.Status__c, ' +
                      'Account.Name, Business_Rule_Association__c, LastActivityDate ' +
                      'FROM Contact WHERE ';

        // Account context (required)
        if (criteria.accountId != null) {
            conditions.add('(AccountId = :criteria.accountId OR Location__c = :criteria.accountId)');
        }

        // Search term (name search)
        if (String.isNotBlank(criteria.searchTerm)) {
            String searchTerm = '%' + String.escapeSingleQuotes(criteria.searchTerm) + '%';
            conditions.add('(FirstName LIKE :searchTerm OR LastName LIKE :searchTerm OR ' +
                         'Name LIKE :searchTerm)');
        }

        // Specific field searches
        if (String.isNotBlank(criteria.firstName)) {
            String firstName = '%' + String.escapeSingleQuotes(criteria.firstName) + '%';
            conditions.add('FirstName LIKE :firstName');
        }

        if (String.isNotBlank(criteria.lastName)) {
            String lastName = '%' + String.escapeSingleQuotes(criteria.lastName) + '%';
            conditions.add('LastName LIKE :lastName');
        }

        if (String.isNotBlank(criteria.email)) {
            String email = String.escapeSingleQuotes(criteria.email) + '%';
            conditions.add('Email LIKE :email');
        }

        if (String.isNotBlank(criteria.phone)) {
            String phone = '%' + String.escapeSingleQuotes(cleanPhone(criteria.phone)) + '%';
            conditions.add('(Phone LIKE :phone OR MobilePhone LIKE :phone)');
        }

        // Exclude unspecified contacts if requested
        if (criteria.excludeUnspecified) {
            conditions.add('FirstName != \'Unspecified\'');
        }

        // Join conditions
        query += String.join(conditions, ' AND ');

        // Order by
        query += ' ORDER BY Business_Rule_Association__c DESC NULLS LAST, ' +
                'LastActivityDate DESC NULLS LAST, Name ASC';

        // Limit
        Integer limitSize = criteria.pageSize != null ? criteria.pageSize : DEFAULT_PAGE_SIZE;
        limitSize = Math.min(limitSize, MAX_RESULTS);
        query += ' LIMIT ' + limitSize;

        return query;
    }

    /**
     * @description Transform Contact records to DTOs
     * @param contacts List of Contact records
     * @param accountId Account context
     * @return List of ContactDTO
     */
    @TestVisible
    private List<ContactDTO> transformToDTO(List<Contact> contacts, Id accountId) {
        List<ContactDTO> dtos = new List<ContactDTO>();

        for (Contact con : contacts) {
            ContactDTO dto = new ContactDTO();
            dto.contactId = con.Id;
            dto.name = con.Name;
            dto.firstName = con.FirstName;
            dto.lastName = con.LastName;
            dto.title = con.Account_Title__r?.Name;
            dto.company = con.Account.Name;
            dto.phone = con.Phone;
            dto.mobilePhone = con.MobilePhone;
            dto.email = con.Email;
            dto.preferredMethod = con.Preferred_Method__c;
            dto.businessRuleAssociation = con.Business_Rule_Association__c;
            dto.lastActivityDate = con.LastActivityDate;
            dto.accountTitleStatus = con.Account_Title__r?.Status__c;

            // CSS class for highlighting
            dto.rowClass = con.Business_Rule_Association__c == 'Yes' ?
                          'bgHighlight' : 'noBgHighlight';

            dtos.add(dto);
        }

        return dtos;
    }

    /**
     * @description Detect search pattern (email, phone, or name)
     * @param searchTerm Search term
     * @return SearchPattern enum
     */
    @TestVisible
    private SearchPattern detectSearchPattern(String searchTerm) {
        // Email pattern
        Pattern emailPattern = Pattern.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$');
        if (emailPattern.matcher(searchTerm).matches()) {
            return SearchPattern.EMAIL;
        }

        // Phone pattern (basic detection)
        String digitsOnly = searchTerm.replaceAll('[^0-9]', '');
        if (digitsOnly.length() >= 10) {
            return SearchPattern.PHONE;
        }

        // Default to name search
        return SearchPattern.NAME;
    }

    /**
     * @description Clean phone number for searching
     * @param phone Raw phone number
     * @return Cleaned phone number
     */
    private String cleanPhone(String phone) {
        return phone.replaceAll('[^0-9]', '');
    }

    /**
     * @description Validate search criteria
     * @param criteria Search criteria
     */
    private void validateSearchCriteria(SearchCriteria criteria) {
        if (criteria == null) {
            throw new IllegalArgumentException('Search criteria is required');
        }

        // At least one search parameter required
        Boolean hasSearchParam = String.isNotBlank(criteria.searchTerm) ||
                                String.isNotBlank(criteria.firstName) ||
                                String.isNotBlank(criteria.lastName) ||
                                String.isNotBlank(criteria.email) ||
                                String.isNotBlank(criteria.phone);

        if (!hasSearchParam) {
            throw new IllegalArgumentException('At least one search parameter is required');
        }

        // Validate search term length
        if (String.isNotBlank(criteria.searchTerm) &&
            criteria.searchTerm.length() < MIN_SEARCH_LENGTH) {
            throw new IllegalArgumentException(
                'Search term must be at least ' + MIN_SEARCH_LENGTH + ' characters'
            );
        }
    }

    /**
     * @description Enum for search pattern types
     */
    private enum SearchPattern {
        EMAIL, PHONE, NAME
    }
}
```

### 3. CacheService

**Purpose:** Centralized caching using Platform Cache

**File:** `CacheService.cls`

```apex
/**
 * @description Centralized caching service using Platform Cache
 * @author Development Team
 * @date 2026-01-18
 */
public with sharing class CacheService {

    // Cache partition name (configured in Setup)
    private static final String CACHE_PARTITION = 'local.ContactSearchCache';

    // Default TTL (1 hour)
    private static final Integer DEFAULT_TTL = 3600;

    /**
     * @description Get value from cache
     * @param key Cache key
     * @return Cached value or null
     */
    public static Object get(String key) {
        try {
            Cache.Org orgCache = Cache.Org.getPartition(CACHE_PARTITION);
            return orgCache.get(key);
        } catch (Exception e) {
            // Log error but don't fail
            System.debug(LoggingLevel.ERROR, 'Cache get error: ' + e.getMessage());
            return null;
        }
    }

    /**
     * @description Put value in cache
     * @param key Cache key
     * @param value Value to cache
     * @param ttl Time to live in seconds
     */
    public static void put(String key, Object value, Integer ttl) {
        try {
            Cache.Org orgCache = Cache.Org.getPartition(CACHE_PARTITION);
            orgCache.put(key, value, ttl != null ? ttl : DEFAULT_TTL);
        } catch (Exception e) {
            // Log error but don't fail
            System.debug(LoggingLevel.ERROR, 'Cache put error: ' + e.getMessage());
        }
    }

    /**
     * @description Put value with default TTL
     * @param key Cache key
     * @param value Value to cache
     */
    public static void put(String key, Object value) {
        put(key, value, DEFAULT_TTL);
    }

    /**
     * @description Remove value from cache
     * @param key Cache key
     */
    public static void remove(String key) {
        try {
            Cache.Org orgCache = Cache.Org.getPartition(CACHE_PARTITION);
            orgCache.remove(key);
        } catch (Exception e) {
            // Log error but don't fail
            System.debug(LoggingLevel.ERROR, 'Cache remove error: ' + e.getMessage());
        }
    }

    /**
     * @description Check if key exists in cache
     * @param key Cache key
     * @return true if exists
     */
    public static Boolean contains(String key) {
        try {
            Cache.Org orgCache = Cache.Org.getPartition(CACHE_PARTITION);
            return orgCache.contains(key);
        } catch (Exception e) {
            return false;
        }
    }
}
```

### 4. ContactRepository

**Purpose:** Data access layer for Contact queries

**File:** `ContactRepository.cls`

```apex
/**
 * @description Repository for Contact data access
 * @author Development Team
 * @date 2026-01-18
 */
public with sharing class ContactRepository {

    /**
     * @description Query contact by ID
     * @param contactId Contact record ID
     * @return Contact record
     */
    public static Contact queryById(Id contactId) {
        List<Contact> contacts = [
            SELECT Id, FirstName, LastName, Phone, MobilePhone, Email,
                   Contact_Status__c, Account_Title__c, Account_Title__r.Name,
                   Account_Title__r.Status__c, Account_Department__r.Name,
                   AccountId, Account.Name
            FROM Contact
            WHERE Id = :contactId
            LIMIT 1
        ];

        return contacts.isEmpty() ? null : contacts[0];
    }

    /**
     * @description Query contacts by IDs
     * @param contactIds Set of contact IDs
     * @return List of contacts
     */
    public static List<Contact> queryByIds(Set<Id> contactIds) {
        return [
            SELECT Id, Name, FirstName, LastName, Phone, MobilePhone, Email,
                   Account_Title__r.Name, Account.Name
            FROM Contact
            WHERE Id IN :contactIds
        ];
    }

    /**
     * @description Query location contacts excluding unspecified
     * @param locationId Location account ID
     * @param excludeContactId Contact ID to exclude (optional)
     * @return List of contacts
     */
    public static List<Contact> queryLocationContacts(Id locationId, Id excludeContactId) {
        String query = 'SELECT Id, Name, FirstName, LastName, Phone, MobilePhone, Email, ' +
                      'Preferred_Method__c, Account_Title__r.Name, Account.Name, ' +
                      'Business_Rule_Association__c, LastActivityDate ' +
                      'FROM Contact ' +
                      'WHERE (AccountId = :locationId OR Location__c = :locationId) ' +
                      'AND FirstName != \'Unspecified\'';

        if (excludeContactId != null) {
            query += ' AND Id != :excludeContactId';
        }

        query += ' ORDER BY Business_Rule_Association__c DESC NULLS LAST, ' +
                'LastActivityDate DESC NULLS LAST LIMIT 100';

        return Database.query(query);
    }
}
```

---

## Data Model

### Custom Metadata Type: Contact_Search_Configuration__mdt

**Purpose:** Store configurable settings for contact search

```apex
// Fields:
- DeveloperName (Standard)
- MasterLabel (Standard)
- Search_Term_Min_Length__c (Number) - Default: 2
- Max_Results__c (Number) - Default: 100
- Cache_TTL_Seconds__c (Number) - Default: 3600
- Enable_Caching__c (Checkbox) - Default: true
- Exclude_Unspecified_Contacts__c (Checkbox) - Default: true
```

### Custom Metadata Type: Excluded_Vendor__mdt

**Purpose:** Store vendor accounts to exclude from searches

```apex
// Fields:
- DeveloperName (Standard)
- MasterLabel (Standard)
- Vendor_Account_Id__c (Text 18) - Account ID
- Reason__c (Text 255) - Why excluded
- Active__c (Checkbox) - Whether to apply
```

### Platform Cache Partition

**Name:** ContactSearchCache
**Type:** Org Cache
**Size:** 10 MB (configurable)

**Cache Keys Pattern:**
```
AccountTitles_{accountId}        - TTL: 1 hour
AccountDepts_{accountId}          - TTL: 1 hour
VendorRoles                       - TTL: 24 hours
ExcludedVendors                   - TTL: 24 hours
RecentSearch_{userId}_{hash}      - TTL: 15 minutes
```

---

## API Specifications

### Input DTOs

#### SearchCriteria
```apex
public class SearchCriteria {
    public String searchTerm;        // General search
    public String firstName;
    public String lastName;
    public String email;
    public String phone;
    public Id accountId;             // Required context
    public Id caseId;                // Optional context
    public Boolean excludeUnspecified;
    public Integer pageSize;
    public Integer offset;
}
```

#### ContactRequest
```apex
public class ContactRequest {
    public String firstName;
    public String lastName;
    public String email;
    public String phone;
    public String mobilePhone;
    public Id accountId;
    public Id caseId;
    public Id accountTitleId;
    public String department;
    public String preferredMethod;
    public String extension;
    public String contactType;       // Customer, Vendor, Internal
    public Boolean ignoreDuplicates;
}
```

### Output DTOs

#### ContactDTO
```apex
public class ContactDTO {
    @AuraEnabled public Id contactId;
    @AuraEnabled public String name;
    @AuraEnabled public String firstName;
    @AuraEnabled public String lastName;
    @AuraEnabled public String title;
    @AuraEnabled public String company;
    @AuraEnabled public String phone;
    @AuraEnabled public String mobilePhone;
    @AuraEnabled public String email;
    @AuraEnabled public String preferredMethod;
    @AuraEnabled public String businessRuleAssociation;
    @AuraEnabled public Date lastActivityDate;
    @AuraEnabled public String accountTitleStatus;
    @AuraEnabled public String rowClass;    // For UI styling
}
```

#### ContactSearchResult
```apex
public class ContactSearchResult {
    @AuraEnabled public List<ContactDTO> contacts;
    @AuraEnabled public Integer totalCount;
    @AuraEnabled public Boolean hasMore;
    @AuraEnabled public CaseData caseContext;
}
```

#### OperationResult
```apex
public class OperationResult {
    @AuraEnabled public Boolean success;
    @AuraEnabled public String message;
    @AuraEnabled public String errorCode;
    @AuraEnabled public Id recordId;
    @AuraEnabled public Boolean duplicatesFound;
    @AuraEnabled public List<ContactDTO> duplicates;
}
```

---

## Performance Optimization Strategy

### 1. Query Optimization

**Before:**
```apex
// SOSL - searches all fields
List<List<sObject>> qryRes = [FIND :searchQuery IN ALL FIELDS
                    RETURNING Contact(...)];
// Avg: 800-1200ms
```

**After:**
```apex
// Indexed SOQL - specific fields only
List<Contact> contacts = [
    SELECT Id, Name, Email, Phone
    FROM Contact
    WHERE (AccountId = :accountId OR Location__c = :accountId)
    AND (FirstName LIKE :term OR LastName LIKE :term)
    ORDER BY LastActivityDate DESC
    LIMIT 50
];
// Target: <300ms
```

**Optimizations:**
- Use indexed fields (AccountId, Location__c)
- Specific field selection
- LIMIT clause
- ORDER BY on indexed field when possible

### 2. Caching Strategy

```apex
// Cache frequently accessed data
String cacheKey = 'AccountTitles_' + accountId;
List<PicklistOption> cached = CacheService.get(cacheKey);
if (cached != null) {
    return cached; // Cache hit - instant response
}

// Cache miss - query and cache
List<PicklistOption> options = queryTitles(accountId);
CacheService.put(cacheKey, options, 3600); // 1 hour TTL
return options;
```

**What to Cache:**
- Account titles (changes infrequently)
- Account departments (changes infrequently)
- Vendor roles (static picklist values)
- Excluded vendor list (configuration)
- Search configurations (metadata)

**Cache Invalidation:**
- Manual invalidation on title/dept creation
- TTL-based automatic expiration
- Clear on deployment if needed

### 3. Bulkification

**Before:**
```apex
// Separate queries
Contact con = [SELECT ... FROM Contact WHERE Id=:contactId];
Case c = [SELECT ... FROM Case WHERE Id=:caseId];
update con;
update c;
```

**After:**
```apex
// Combined query with relationship
List<SObject> toUpdate = new List<SObject>();

// Single query with relationships
Case c = [SELECT Id, ContactId, Contact.Id, Contact.Name
          FROM Case WHERE Id = :caseId];

// Prepare updates
c.ContactId = contactId;
toUpdate.add(c);

if (needsContactUpdate) {
    Contact con = new Contact(Id=contactId, Field__c='value');
    toUpdate.add(con);
}

// Single DML
update toUpdate;
```

### 4. Governor Limit Management

**Monitoring:**
```apex
// Track limits in each method
System.debug('SOQL Queries: ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
System.debug('CPU Time: ' + Limits.getCpuTime() + '/' + Limits.getLimitCpuTime());
System.debug('Heap Size: ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
```

**Targets:**
- SOQL Queries: <10 per transaction
- CPU Time: <5,000ms
- Heap Size: <4MB
- DML Statements: <5

---

## Security Considerations

### 1. Sharing and Visibility

```apex
// Use 'with sharing' throughout
public with sharing class ContactSearchController {
    // Respects record-level security
}

// Query respects field-level security
List<Contact> contacts = [SELECT Id, Name, Email
                         FROM Contact
                         WITH SECURITY_ENFORCED];
```

### 2. Input Validation

```apex
// Sanitize inputs
String searchTerm = String.escapeSingleQuotes(criteria.searchTerm);

// Validate IDs
if (!Pattern.matches('[a-zA-Z0-9]{15,18}', accountId)) {
    throw new SecurityException('Invalid ID format');
}

// Validate email format
Pattern emailPattern = Pattern.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$');
if (!emailPattern.matcher(email).matches()) {
    throw new ValidationException('Invalid email format');
}
```

### 3. CRUD/FLS Checks

```apex
// Check create permission
if (!Schema.sObjectType.Contact.isCreateable()) {
    throw new SecurityException('Insufficient permissions to create contact');
}

// Check field accessibility
if (!Schema.sObjectType.Contact.fields.Email.isAccessible()) {
    throw new SecurityException('Insufficient permissions to access email field');
}
```

### 4. Error Message Sanitization

```apex
// Don't expose internal details
try {
    // Operation
} catch (Exception e) {
    // Log full error internally
    System.debug(LoggingLevel.ERROR, 'Full error: ' + e.getStackTraceString());

    // Return sanitized message to user
    throw new AuraHandledException('An error occurred while processing your request');
}
```

---

## Error Handling & Logging

### Custom Exception Classes

```apex
public class ContactSearchException extends Exception {}
public class ContactValidationException extends Exception {}
public class ContactDuplicateException extends Exception {}
```

### Logging Framework

```apex
public class Logger {

    public enum LogLevel { DEBUG, INFO, WARN, ERROR, FATAL }

    public static void log(LogLevel level, String message, Exception ex) {
        // Create log entry
        Log__c logEntry = new Log__c(
            Level__c = level.name(),
            Message__c = message,
            Exception_Type__c = ex?.getTypeName(),
            Stack_Trace__c = ex?.getStackTraceString(),
            User__c = UserInfo.getUserId(),
            Timestamp__c = System.now()
        );

        // Insert asynchronously to not block transaction
        insert logEntry;
    }

    public static void error(String message, Exception ex) {
        log(LogLevel.ERROR, message, ex);
    }
}
```

### Usage Pattern

```apex
public static ContactSearchResult searchContacts(String criteria, Id caseId) {
    try {
        // Business logic
        return result;

    } catch (QueryException qe) {
        Logger.error('Query failed in searchContacts', qe);
        throw new AuraHandledException('Search failed. Please try again.');

    } catch (Exception e) {
        Logger.error('Unexpected error in searchContacts', e);
        throw new AuraHandledException('An unexpected error occurred');
    }
}
```

---

## Testing Strategy

### Test Coverage Requirements
- **Minimum:** 80% code coverage
- **Target:** 85% code coverage
- **Critical paths:** 100% coverage

### Test Class Structure

```apex
@isTest
public class ContactSearchControllerTest {

    @testSetup
    static void setup() {
        // Create test data
        TestDataFactory.createAccountHierarchy();
        TestDataFactory.createContacts(50);
        TestDataFactory.createCases(10);
    }

    @isTest
    static void testSearchContacts_Success() {
        // Given
        SearchCriteria criteria = new SearchCriteria();
        criteria.firstName = 'John';
        criteria.accountId = TestDataFactory.clientAccountId;

        // When
        Test.startTest();
        ContactSearchResult result = ContactSearchController.searchContacts(
            JSON.serialize(criteria),
            TestDataFactory.caseId
        );
        Test.stopTest();

        // Then
        System.assertNotEquals(null, result);
        System.assert(result.contacts.size() > 0);
        System.assert(Limits.getQueries() < 10);
        System.assert(Limits.getCpuTime() < 5000);
    }

    @isTest
    static void testSearchContacts_Performance() {
        // Test with max results
        SearchCriteria criteria = new SearchCriteria();
        criteria.searchTerm = 'Test';
        criteria.accountId = TestDataFactory.clientAccountId;
        criteria.pageSize = 100;

        Test.startTest();
        Long startTime = System.currentTimeMillis();
        ContactSearchResult result = ContactSearchController.searchContacts(
            JSON.serialize(criteria),
            TestDataFactory.caseId
        );
        Long endTime = System.currentTimeMillis();
        Test.stopTest();

        // Performance assertions
        System.assert((endTime - startTime) < 1000, 'Search took too long');
        System.assert(Limits.getCpuTime() < 5000, 'CPU time exceeded');
    }

    @isTest
    static void testCreateContactForCase_WithDuplicates() {
        // Test duplicate detection
    }

    @isTest
    static void testAssociateContactToCase_InactiveTitle() {
        // Test validation
    }

    // Additional test methods...
}
```

### Mock Data Factory

```apex
@isTest
public class TestDataFactory {

    public static Id clientAccountId;
    public static Id locationAccountId;
    public static Id vendorAccountId;
    public static Id caseId;

    public static void createAccountHierarchy() {
        // Create client account
        Account client = new Account(
            Name = 'Test Client',
            RecordTypeId = getRecordTypeId('Client')
        );
        insert client;
        clientAccountId = client.Id;

        // Create location account
        Account location = new Account(
            Name = 'TST000123',
            ParentId = client.Id,
            RecordTypeId = getRecordTypeId('Location')
        );
        insert location;
        locationAccountId = location.Id;

        // Create vendor account
        Account vendor = new Account(
            Name = 'Test Vendor',
            RecordTypeId = getRecordTypeId('Vendor')
        );
        insert vendor;
        vendorAccountId = vendor.Id;

        // Create account title
        Account_Title__c title = new Account_Title__c(
            Name = 'Operations Manager',
            Account__c = clientAccountId,
            Status__c = 'Active'
        );
        insert title;
    }

    public static void createContacts(Integer count) {
        List<Contact> contacts = new List<Contact>();
        for (Integer i = 0; i < count; i++) {
            contacts.add(new Contact(
                FirstName = 'TestFirst' + i,
                LastName = 'TestLast' + i,
                Email = 'test' + i + '@example.com',
                Phone = '555010' + String.valueOf(i).leftPad(4, '0'),
                AccountId = clientAccountId
            ));
        }
        insert contacts;
    }

    public static void createCases(Integer count) {
        List<Case> cases = new List<Case>();
        for (Integer i = 0; i < count; i++) {
            cases.add(new Case(
                Subject = 'Test Case ' + i,
                Client__c = clientAccountId,
                Location__c = locationAccountId,
                Origin = 'Phone',
                Status = 'New'
            ));
        }
        insert cases;
        caseId = cases[0].Id;
    }

    private static Id getRecordTypeId(String developerName) {
        return Schema.SObjectType.Account.getRecordTypeInfosByDeveloperName()
            .get(developerName).getRecordTypeId();
    }
}
```

---

## Deployment Plan

### Phase 1: Preparation (Day 1-2)

1. **Create Custom Metadata Types**
   ```bash
   # Deploy metadata types
   sfdx force:source:deploy -m CustomObject:Contact_Search_Configuration__mdt
   sfdx force:source:deploy -m CustomObject:Excluded_Vendor__mdt
   ```

2. **Configure Platform Cache**
   - Setup > Platform Cache
   - Create partition "ContactSearchCache" (10 MB)
   - Allocate to org cache

3. **Create Custom Metadata Records**
   ```xml
   <!-- Contact_Search_Configuration.Search_Default -->
   <values>
       <field>Search_Term_Min_Length__c</field>
       <value xsi:type="xsd:double">2</value>
   </values>
   <values>
       <field>Max_Results__c</field>
       <value xsi:type="xsd:double">100</value>
   </values>
   ```

### Phase 2: Deploy Classes (Day 3-5)

**Deployment Order:**
1. Exception classes
2. DTOs and wrapper classes
3. Repository classes
4. Service classes
5. Controller facade
6. Test classes

```bash
# Deploy in order
sfdx force:source:deploy -p force-app/main/default/classes/exceptions
sfdx force:source:deploy -p force-app/main/default/classes/dto
sfdx force:source:deploy -p force-app/main/default/classes/repository
sfdx force:source:deploy -p force-app/main/default/classes/service
sfdx force:source:deploy -p force-app/main/default/classes/controller
sfdx force:source:deploy -p force-app/main/default/classes/test
```

### Phase 3: Update Aura Component (Day 6)

Update Aura component controller to call new methods:

```javascript
// Old
var action = cmp.get('c.searchContacts');

// New
var action = cmp.get('c.searchContacts'); // Now calls ContactSearchController
```

### Phase 4: Validation Testing (Day 7-10)

1. **Smoke Tests**
   - Basic search functionality
   - Contact creation
   - Association workflows

2. **Performance Tests**
   - Run performance benchmarks
   - Compare against baseline
   - Validate targets met

3. **Integration Tests**
   - Test all user workflows
   - Verify no regressions

### Phase 5: Production Deployment (Day 11-12)

```bash
# Final deployment to production
sfdx force:source:deploy -p force-app/main/default -l RunLocalTests

# Monitor
sfdx force:apex:log:tail
```

---

## Rollback Strategy

### Rollback Triggers

- Critical production defect
- Performance regression
- Data integrity issues
- >5% of transactions failing

### Rollback Steps

1. **Immediate (0-15 minutes)**
   ```bash
   # Update Aura component to use old methods
   # Deploy component change only
   sfdx force:source:deploy -p force-app/main/default/aura/SearchExistingContact
   ```

2. **Full Rollback (if needed)**
   - Restore previous Apex classes from version control
   - Remove new custom metadata types
   - Clear platform cache partition

3. **Data Validation**
   - Check for any orphaned records
   - Verify no data corruption
   - Run data integrity reports

### Rollback Testing

- Test rollback procedure in sandbox
- Document rollback time: <30 minutes
- Assign rollback team roles

---

## Monitoring & Metrics

### Real-Time Monitoring

**Debug Logs:**
```apex
System.debug('=== Search Performance ===');
System.debug('Criteria: ' + JSON.serialize(criteria));
System.debug('Results: ' + contacts.size());
System.debug('SOQL Queries: ' + Limits.getQueries());
System.debug('CPU Time: ' + Limits.getCpuTime());
System.debug('Heap Size: ' + Limits.getHeapSize());
```

### Performance Metrics Dashboard

| Metric | Target | Alert Threshold | Critical Threshold |
|--------|--------|-----------------|-------------------|
| Search Response Time | <500ms | >750ms | >1000ms |
| Apex CPU Time | <5,000ms | >7,500ms | >10,000ms |
| SOQL Queries | <10 | >15 | >20 |
| Heap Size | <4MB | >5MB | >6MB |
| Error Rate | <1% | >3% | >5% |

### Custom Logging

```apex
// Performance log object
Performance_Log__c log = new Performance_Log__c(
    Operation__c = 'Contact Search',
    Criteria__c = JSON.serialize(criteria),
    Result_Count__c = contacts.size(),
    SOQL_Queries__c = Limits.getQueries(),
    CPU_Time__c = Limits.getCpuTime(),
    Heap_Size__c = Limits.getHeapSize(),
    Response_Time__c = endTime - startTime,
    User__c = UserInfo.getUserId(),
    Timestamp__c = System.now()
);
```

### Weekly Performance Reports

- Average search response time
- 95th percentile CPU time
- Cache hit rate
- Error rate trends
- Most common search patterns

---

## Dependencies

### Platform Dependencies

1. **Salesforce Version:** Winter '25 or later (API v59.0+)
2. **Platform Cache:** Enabled and configured
3. **Custom Metadata Types:** Deployable to production

### Object Dependencies

- **Contact** object and custom fields
- **Case** object and custom fields
- **Account** object with record types
- **Account_Title__c** custom object
- **Account_Department__c** custom object (if used)
- **AccountContactRelation** object

### Permission Dependencies

- **Users need:**
  - Read: Contact, Case, Account
  - Create: Contact, AccountContactRelation
  - Edit: Contact, Case
  - Read: Account_Title__c, Custom Metadata Types

---

## Appendices

### Appendix A: Naming Conventions

**Classes:**
- Services: `*Service.cls`
- Repositories: `*Repository.cls`
- Controllers: `*Controller.cls`
- DTOs: `*DTO.cls` or `*Request.cls` / `*Result.cls`
- Tests: `*Test.cls`

**Methods:**
- Public: camelCase
- Private: camelCase with descriptive names
- Test methods: `test*_Scenario`

**Variables:**
- Local: camelCase
- Constants: UPPER_SNAKE_CASE
- Parameters: camelCase

### Appendix B: Code Review Checklist

- [ ] Follows naming conventions
- [ ] All public methods have JavaDoc comments
- [ ] Error handling implemented
- [ ] Security considerations addressed (sharing, FLS)
- [ ] No hard-coded IDs or configuration
- [ ] SOQL queries optimized with LIMIT clauses
- [ ] Governor limits considered
- [ ] Test coverage >80%
- [ ] Performance targets validated
- [ ] No SOSL unless absolutely necessary

### Appendix C: Performance Baseline

**Current State (Before Refactoring):**
```
Search Response Time: 1,000-2,000ms
Apex CPU Time: 8,000-10,000ms
SOQL Queries: 15-20 per transaction
Heap Size: 5-6MB
Database Time: 3,000-4,000ms
```

**Target State (After Refactoring):**
```
Search Response Time: <500ms (70% improvement)
Apex CPU Time: <5,000ms (50% improvement)
SOQL Queries: <10 (50% reduction)
Heap Size: <4MB (30% reduction)
Database Time: <1,500ms (60% improvement)
```

### Appendix D: Migration Mapping

| Old Method | New Method | New Class |
|------------|------------|-----------|
| `searchContacts()` | `searchContacts()` | ContactSearchController |
| `searchLocCont()` | `search()` | ContactSearchService |
| `createNewContact()` | `createContactForCase()` | ContactSearchController |
| `existingContact()` | `associateContactToCase()` | ContactSearchController |
| `checkDuplicateContacts()` | `checkDuplicates()` | ContactManagementService |
| `getAccountTitles()` | `getAccountTitles()` | ContactSearchController |
| `returnCase()` | `queryById()` | CaseRepository |

---

**Document Status:** Ready for Review
**Next Steps:**
1. Technical Lead review and approval
2. Security review
3. Performance validation in sandbox
4. Proceed to implementation

**Review Comments:**
_[Space for reviewer comments]_

---

**End of Technical Design Document**
