# QA Test Case Scenarios: Apex Controller Refactoring

**Project Code:** CSC-APEX-2026-001
**Document Version:** 1.0
**Date:** January 18, 2026
**Status:** Ready for Test Execution
**QA Lead:** [Name]

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-18 | QA Team | Initial test cases |

---

## Table of Contents

1. [Test Strategy Overview](#test-strategy-overview)
2. [Test Environment Setup](#test-environment-setup)
3. [Functional Test Cases](#functional-test-cases)
4. [Performance Test Cases](#performance-test-cases)
5. [Integration Test Cases](#integration-test-cases)
6. [Security Test Cases](#security-test-cases)
7. [Regression Test Cases](#regression-test-cases)
8. [Negative Test Cases](#negative-test-cases)
9. [Data-Driven Test Cases](#data-driven-test-cases)
10. [Test Execution Schedule](#test-execution-schedule)
11. [Test Data Requirements](#test-data-requirements)
12. [Defect Management](#defect-management)

---

## Test Strategy Overview

### Objectives
- Verify 100% functional parity with existing implementation
- Validate performance improvements meet targets
- Ensure no regression in existing functionality
- Confirm security and data integrity
- Achieve 80%+ code coverage

### Test Levels
1. **Unit Testing** - Apex test classes (80%+ coverage)
2. **Integration Testing** - Component interaction tests
3. **Performance Testing** - Response time and resource usage
4. **Security Testing** - Permissions and data access
5. **Regression Testing** - Existing functionality validation

### Success Criteria
- ✓ All P0 test cases pass (100%)
- ✓ 95%+ P1 test cases pass
- ✓ Performance targets met or exceeded
- ✓ Zero critical defects
- ✓ Code coverage ≥80%

### Test Approach
- **Automated:** Apex unit tests (100%)
- **Manual:** Integration and exploratory tests
- **Performance:** Automated scripts with debug logs
- **Security:** Manual verification with security specialist

---

## Test Environment Setup

### Prerequisites
- [x] Full copy sandbox with production data volume
- [x] Refactored Apex classes deployed
- [x] Custom Metadata Types configured
- [x] Platform Cache partition created (10 MB)
- [x] Test data loaded (see Test Data Requirements)
- [x] Debug logs enabled for performance tracking

### Test User Profiles
1. **System Administrator** - Full access for testing
2. **Standard User** - Normal user permissions
3. **Read-Only User** - Limited access testing
4. **External User** - Community user testing

### Test Data Sets
- **Accounts:** 100 (25 Client, 25 Location, 25 Vendor, 25 Mixed)
- **Contacts:** 500 (250 Customer, 150 Vendor, 100 Internal)
- **Cases:** 50 (various types and statuses)
- **Account Titles:** 20 (15 Active, 5 Inactive)
- **Account Contact Relations:** 300

---

## Functional Test Cases

### FC-001: Contact Search - Simple Search by First Name

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.searchContacts |
| **Estimated Time** | 5 minutes |

**Objective:** Verify contact search returns correct results when searching by first name

**Pre-conditions:**
- User has access to SearchExistingContact component
- Test data loaded with contacts: "John Smith", "Jane Doe", "John Johnson"
- Case record associated with Client account

**Test Data:**
- Case ID: {testCaseId}
- Search Criteria: firstName = "John"
- Expected Results: 2 contacts

**Test Steps:**
1. Navigate to Case record page
2. Open SearchExistingContact component
3. Call `searchContacts()` with criteria:
   ```json
   {
     "firstName": "John",
     "accountId": "{clientAccountId}",
     "pageSize": 50
   }
   ```
4. Verify response

**Expected Results:**
- Response contains 2 contact records
- Both contacts have firstName = "John"
- Response time < 500ms
- No errors in debug log
- SOQL queries < 10

**Actual Results:**
_[To be filled during test execution]_

**Status:** [ ] Pass [ ] Fail [ ] Blocked

**Defects:** _[Link to defect if failed]_

---

### FC-002: Contact Search - Email Pattern Detection

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.searchContacts |
| **Estimated Time** | 5 minutes |

**Objective:** Verify email search works correctly

**Pre-conditions:**
- Contact exists with email "john.smith@example.com"

**Test Data:**
- Case ID: {testCaseId}
- Search Criteria: email = "john.smith@example.com"

**Test Steps:**
1. Call `searchContacts()` with email criteria
2. Verify contact returned
3. Check performance metrics

**Expected Results:**
- Exactly 1 contact returned
- Contact email matches search criteria exactly
- Response time < 400ms
- Query uses indexed Email field

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-003: Contact Search - Phone Number Search

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-003 |
| **Priority** | P1 - High |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.searchContacts |

**Objective:** Verify phone number search with various formats

**Test Data:**
- Contact with Phone: (555) 123-4567
- Search variations: "5551234567", "555-123-4567", "(555) 123-4567"

**Test Steps:**
1. Search with format: "5551234567"
2. Verify contact found
3. Search with format: "555-123-4567"
4. Verify contact found
5. Search with format: "(555) 123-4567"
6. Verify contact found

**Expected Results:**
- All three formats return the same contact
- Phone number normalized before search
- Results consistent across formats

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-004: Contact Search - Multi-Field Search

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-004 |
| **Priority** | P1 - High |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.searchContacts |

**Objective:** Verify search works with multiple criteria

**Test Data:**
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "email": "john.smith@example.com",
  "accountId": "{accountId}"
}
```

**Test Steps:**
1. Call searchContacts with all criteria
2. Verify results match ALL criteria (AND logic)
3. Check query construction

**Expected Results:**
- Only contacts matching ALL criteria returned
- Query uses AND logic correctly
- Performance within targets

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-005: Contact Search - Result Limiting

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-005 |
| **Priority** | P1 - High |
| **Test Type** | Functional, Boundary |
| **Component** | ContactSearchController.searchContacts |

**Objective:** Verify search respects pageSize limit

**Test Data:**
- 100 contacts matching search criteria
- pageSize = 50

**Test Steps:**
1. Perform search that would return 100 results
2. Set pageSize to 50
3. Verify only 50 results returned
4. Check hasMore flag

**Expected Results:**
- Exactly 50 results returned
- hasMore = true in response
- Results ordered correctly (BR Association, Last Activity, Name)
- Performance not degraded

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-006: Contact Search - Empty Results

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-006 |
| **Priority** | P1 - High |
| **Test Type** | Functional, Negative |
| **Component** | ContactSearchController.searchContacts |

**Objective:** Verify graceful handling of no results

**Test Data:**
- Search criteria: firstName = "NonExistentName123456"

**Test Steps:**
1. Search with criteria that will return no results
2. Verify response structure
3. Check error handling

**Expected Results:**
- Empty array returned (not null)
- No error thrown
- totalCount = 0
- hasMore = false

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-007: Contact Creation - Standard Customer Contact

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-007 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.createContactForCase |

**Objective:** Verify new customer contact creation

**Test Data:**
```json
{
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "jane.doe@example.com",
  "phone": "5551234567",
  "accountId": "{clientAccountId}",
  "accountTitleId": "{titleId}",
  "department": "Operations",
  "preferredMethod": "Email",
  "contactType": "Customer"
}
```

**Test Steps:**
1. Call createContactForCase with test data
2. Verify contact created in database
3. Verify contact associated to case
4. Verify account relationships created
5. Check all field values

**Expected Results:**
- Contact record created with all fields populated correctly
- Contact.AccountId = clientAccountId
- Case.ContactId updated to new contact
- AccountContactRelation created (Type = Customer)
- OperationResult.success = true
- No duplicate detection triggered
- Transaction completed successfully

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-008: Contact Creation - Duplicate Detection

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-008 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional, Positive |
| **Component** | ContactManagementService.checkDuplicates |

**Objective:** Verify duplicate detection works correctly

**Pre-conditions:**
- Existing contact: John Smith, john.smith@example.com, 5551234567

**Test Data:**
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "email": "john.smith@example.com",
  "phone": "5551234567"
}
```

**Test Steps:**
1. Attempt to create contact with same details
2. Verify duplicate detection triggered
3. Check duplicates returned in response

**Expected Results:**
- OperationResult.success = false
- OperationResult.duplicatesFound = true
- OperationResult.duplicates contains existing contact
- No new contact created
- User can review and choose to proceed

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-009: Contact Association - Existing Contact to Case

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-009 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.associateContactToCase |

**Objective:** Verify existing contact can be associated to case

**Test Data:**
- Existing contact ID: {contactId}
- Case ID: {caseId}
- Contact Type: "Customer"

**Test Steps:**
1. Call associateContactToCase
2. Verify case updated
3. Verify relationships created
4. Check validation rules

**Expected Results:**
- Case.ContactId = contactId
- AccountContactRelation created if needed
- Account title validated (must be Active)
- OperationResult.success = true
- No errors

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-010: Contact Association - Inactive Account Title Validation

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-010 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional, Negative |
| **Component** | ContactValidationService.validateAccountTitle |

**Objective:** Verify inactive account title is rejected

**Pre-conditions:**
- Contact with inactive account title exists

**Test Steps:**
1. Attempt to associate contact with inactive title
2. Verify validation error

**Expected Results:**
- OperationResult.success = false
- OperationResult.errorCode = "INACTIVE_TITLE"
- OperationResult.message = "Contact account title is inactive..."
- Contact NOT associated to case
- User shown clear error message

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-011: Cache Service - Get Account Titles

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-011 |
| **Priority** | P1 - High |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.getAccountTitles |

**Objective:** Verify account titles are cached correctly

**Test Steps:**
1. Call getAccountTitles for accountId (cache miss)
2. Verify database query executed
3. Call getAccountTitles again (cache hit)
4. Verify no database query executed
5. Wait for TTL expiration (3600 seconds)
6. Call again (cache expired)

**Expected Results:**
- First call: Query executed, results cached
- Second call: Results from cache, no query
- Cache key format: "AccountTitles_{accountId}"
- TTL = 3600 seconds (1 hour)
- Cache hit improves response time by 80%

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FC-012: Cache Service - Invalidation on Title Creation

| Field | Value |
|-------|-------|
| **Test Case ID** | FC-012 |
| **Priority** | P1 - High |
| **Test Type** | Functional, Positive |
| **Component** | ContactSearchController.createAccountTitle |

**Objective:** Verify cache is invalidated when new title created

**Test Steps:**
1. Call getAccountTitles (cache titles)
2. Create new account title
3. Call getAccountTitles again
4. Verify new title in results

**Expected Results:**
- Cache invalidated on title creation
- New title appears in subsequent calls
- No stale data served

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Performance Test Cases

### PT-001: Search Response Time - Standard Query

| Field | Value |
|-------|-------|
| **Test Case ID** | PT-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Performance |
| **Component** | ContactSearchController.searchContacts |

**Objective:** Verify search response time meets target

**Test Data:**
- Search criteria with 25 results

**Test Steps:**
1. Enable debug logs
2. Execute search query
3. Measure response time from debug logs
4. Record CPU time, SOQL queries, heap size
5. Repeat 10 times and average

**Performance Targets:**
- Response Time: < 500ms (Target), < 750ms (Acceptable)
- CPU Time: < 5,000ms
- SOQL Queries: < 10
- Heap Size: < 4MB
- Database Time: < 1,500ms

**Expected Results:**
| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| Response Time | < 500ms | ___ ms | [ ] Pass [ ] Fail |
| CPU Time | < 5,000ms | ___ ms | [ ] Pass [ ] Fail |
| SOQL Queries | < 10 | ___ | [ ] Pass [ ] Fail |
| Heap Size | < 4MB | ___ MB | [ ] Pass [ ] Fail |
| DB Time | < 1,500ms | ___ ms | [ ] Pass [ ] Fail |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PT-002: Search Response Time - Large Result Set

| Field | Value |
|-------|-------|
| **Test Case ID** | PT-002 |
| **Priority** | P1 - High |
| **Test Type** | Performance |
| **Component** | ContactSearchController.searchContacts |

**Objective:** Verify performance with maximum results (100)

**Test Data:**
- Search criteria returning 100+ results
- pageSize = 100 (maximum)

**Test Steps:**
1. Execute search returning 100 results
2. Measure all performance metrics
3. Compare against baseline

**Performance Targets:**
- Response Time: < 800ms
- CPU Time: < 6,000ms
- Results properly limited

**Expected Results:**
- Performance degradation < 60% vs. standard query
- All limits respected
- No governor limit issues

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PT-003: Contact Creation Performance

| Field | Value |
|-------|-------|
| **Test Case ID** | PT-003 |
| **Priority** | P1 - High |
| **Test Type** | Performance |
| **Component** | ContactSearchController.createContactForCase |

**Objective:** Verify contact creation performance

**Test Steps:**
1. Create new contact with all fields
2. Measure response time and resource usage
3. Verify DML optimization

**Performance Targets:**
- Response Time: < 1,000ms
- CPU Time: < 4,000ms
- DML Statements: < 5
- SOQL Queries: < 10

**Expected Results:**
- All targets met
- Bulkification patterns used
- No unnecessary queries

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PT-004: Cache Performance - Hit vs Miss

| Field | Value |
|-------|-------|
| **Test Case ID** | PT-004 |
| **Priority** | P1 - High |
| **Test Type** | Performance |
| **Component** | CacheService |

**Objective:** Verify cache performance improvement

**Test Steps:**
1. Measure getAccountTitles (cache miss)
2. Measure getAccountTitles (cache hit)
3. Calculate improvement

**Performance Targets:**
- Cache hit 80% faster than miss
- Cache hit < 50ms response time
- Zero SOQL queries on cache hit

**Expected Results:**
| Scenario | Response Time | SOQL Queries | Status |
|----------|---------------|--------------|--------|
| Cache Miss | ___ ms | 1 | [ ] |
| Cache Hit | ___ ms | 0 | [ ] |
| Improvement | ___% | N/A | [ ] Pass [ ] Fail |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PT-005: Bulk Operations - Multiple Contacts

| Field | Value |
|-------|-------|
| **Test Case ID** | PT-005 |
| **Priority** | P1 - High |
| **Test Type** | Performance |
| **Component** | ContactRepository |

**Objective:** Verify bulkification handles multiple records efficiently

**Test Steps:**
1. Query 50 contacts by IDs
2. Measure performance
3. Verify bulk query used

**Performance Targets:**
- Single SOQL query for all records
- Response time < 300ms
- CPU time < 2,000ms

**Expected Results:**
- Bulk pattern used
- No N+1 query issues
- Efficient resource usage

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PT-006: Performance Regression Test

| Field | Value |
|-------|-------|
| **Test Case ID** | PT-006 |
| **Priority** | P0 - Critical |
| **Test Type** | Performance, Regression |
| **Component** | All |

**Objective:** Verify no performance regression vs. old implementation

**Test Steps:**
1. Execute same queries on old vs. new implementation
2. Compare all metrics
3. Verify improvement

**Performance Targets:**
- Search 70% faster (1,500ms → <500ms)
- CPU time 50% reduction (9,000ms → <5,000ms)
- SOQL queries 40% reduction (17 → <10)

**Expected Results:**
| Metric | Old | New | Improvement | Target | Status |
|--------|-----|-----|-------------|--------|--------|
| Search Time | 1,500ms | ___ ms | ___% | 70% | [ ] |
| CPU Time | 9,000ms | ___ ms | ___% | 50% | [ ] |
| SOQL Queries | 17 | ___ | ___% | 40% | [ ] |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Integration Test Cases

### IT-001: End-to-End Contact Search and Association

| Field | Value |
|-------|-------|
| **Test Case ID** | IT-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Integration |
| **Component** | Full workflow |

**Objective:** Verify complete workflow from search to association

**Test Steps:**
1. User opens contact search component
2. Searches for contact by name
3. Selects contact from results
4. Associates contact to case
5. Verifies case updated
6. Verifies relationships created

**Expected Results:**
- All components work together
- Data flows correctly between services
- Case updated correctly
- Relationships created
- No errors at any step

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### IT-002: Contact Creation with Duplicate Detection Workflow

| Field | Value |
|-------|-------|
| **Test Case ID** | IT-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Integration |
| **Component** | Full workflow |

**Objective:** Verify duplicate detection workflow

**Test Steps:**
1. User attempts to create contact
2. System detects duplicate
3. User reviews duplicate
4. User chooses to use existing contact
5. Contact associated to case

**Expected Results:**
- Duplicate detection works
- User can review duplicates
- User can select existing contact
- No duplicate created
- Transaction completes successfully

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### IT-003: Service Layer Integration

| Field | Value |
|-------|-------|
| **Test Case ID** | IT-003 |
| **Priority** | P1 - High |
| **Test Type** | Integration |
| **Component** | Service layer |

**Objective:** Verify all service classes work together

**Test Steps:**
1. Controller calls SearchService
2. SearchService calls Repository
3. Repository queries database
4. Results flow back through layers
5. Verify each layer's responsibility

**Expected Results:**
- Clean separation of concerns
- Each layer performs its function
- No business logic in controller
- No data access in service
- Proper abstraction maintained

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### IT-004: Cache Service Integration

| Field | Value |
|-------|-------|
| **Test Case ID** | IT-004 |
| **Priority** | P1 - High |
| **Test Type** | Integration |
| **Component** | Cache integration |

**Objective:** Verify cache integrates with all components

**Test Steps:**
1. First call to getAccountTitles (cache miss)
2. Second call (cache hit)
3. Create new title (cache invalidation)
4. Third call (cache miss due to invalidation)
5. Verify cache behavior

**Expected Results:**
- Cache transparently integrated
- Invalidation works correctly
- No stale data served
- Performance improvement visible

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Security Test Cases

### ST-001: Sharing Rules - Record Access

| Field | Value |
|-------|-------|
| **Test Case ID** | ST-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Security |
| **Component** | All with sharing classes |

**Objective:** Verify sharing rules are respected

**Test Steps:**
1. Login as User A (access to Account A only)
2. Search for contacts
3. Verify only contacts from Account A returned
4. Login as User B (no access to Account A)
5. Search for same contacts
6. Verify no results returned

**Expected Results:**
- Sharing rules enforced
- Users only see records they have access to
- WITH SHARING keyword effective
- No data leakage

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### ST-002: Field-Level Security

| Field | Value |
|-------|-------|
| **Test Case ID** | ST-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Security |
| **Component** | All classes |

**Objective:** Verify FLS is respected

**Test Steps:**
1. Remove Email field access from user profile
2. Login as that user
3. Attempt to search by email
4. Verify error or null handling

**Expected Results:**
- FLS respected
- User cannot access restricted fields
- No FLS exceptions thrown
- Graceful degradation

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### ST-003: CRUD Permissions

| Field | Value |
|-------|-------|
| **Test Case ID** | ST-003 |
| **Priority** | P0 - Critical |
| **Test Type** | Security |
| **Component** | ContactManagementService |

**Objective:** Verify CRUD permissions checked

**Test Steps:**
1. Remove Create permission on Contact
2. Attempt to create contact
3. Verify permission check

**Expected Results:**
- Permission checked before operation
- SecurityException thrown if no permission
- Clear error message
- No record created

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### ST-004: SOQL Injection Prevention

| Field | Value |
|-------|-------|
| **Test Case ID** | ST-004 |
| **Priority** | P0 - Critical |
| **Test Type** | Security |
| **Component** | ContactSearchService |

**Objective:** Verify SOQL injection is prevented

**Test Steps:**
1. Attempt search with injection: "Smith' OR '1'='1"
2. Verify proper escaping
3. Verify only legitimate results returned

**Expected Results:**
- String.escapeSingleQuotes() used
- No SOQL injection possible
- Search treats input as literal string
- No unauthorized data accessed

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### ST-005: Data Validation - Email Format

| Field | Value |
|-------|-------|
| **Test Case ID** | ST-005 |
| **Priority** | P1 - High |
| **Test Type** | Security, Validation |
| **Component** | ContactValidationService |

**Objective:** Verify email format validation

**Test Steps:**
1. Attempt to create contact with invalid email: "notanemail"
2. Verify validation error
3. Attempt with valid email
4. Verify acceptance

**Expected Results:**
- Invalid email rejected
- ValidationException thrown
- Valid email accepted
- No XSS or injection via email field

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Regression Test Cases

### RT-001: Existing Aura Component Still Works

| Field | Value |
|-------|-------|
| **Test Case ID** | RT-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Regression |
| **Component** | Backward compatibility |

**Objective:** Verify existing Aura component still functions

**Test Steps:**
1. Open existing SearchExistingContact Aura component
2. Perform search
3. Create contact
4. Associate contact
5. Verify all functions work

**Expected Results:**
- Aura component still works
- Calls new Apex methods correctly
- No breaking changes
- Same behavior as before

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### RT-002: Existing Workflows Not Broken

| Field | Value |
|-------|-------|
| **Test Case ID** | RT-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Regression |
| **Component** | Workflows |

**Objective:** Verify no existing workflows broken

**Test Steps:**
1. Test all Case workflows
2. Test Contact workflows
3. Test Process Builder processes
4. Test Flows
5. Verify all still work

**Expected Results:**
- No workflows broken
- All processes still execute
- All flows still work
- No errors in workflow logs

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### RT-003: API Backward Compatibility

| Field | Value |
|-------|-------|
| **Test Case ID** | RT-003 |
| **Priority** | P0 - Critical |
| **Test Type** | Regression |
| **Component** | API compatibility |

**Objective:** Verify API methods maintain compatibility

**Test Steps:**
1. Call each refactored method
2. Verify parameters accepted
3. Verify return types unchanged
4. Verify behavior identical

**Expected Results:**
- All @AuraEnabled methods available
- Parameters unchanged
- Return types unchanged
- Behavior identical or improved

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Negative Test Cases

### NT-001: Invalid Search Criteria

| Field | Value |
|-------|-------|
| **Test Case ID** | NT-001 |
| **Priority** | P1 - High |
| **Test Type** | Negative |
| **Component** | ContactSearchService |

**Objective:** Verify error handling for invalid input

**Test Cases:**
- Null criteria
- Empty criteria (all fields blank)
- Search term < 2 characters
- Invalid account ID format
- Negative pageSize

**Expected Results:**
- Appropriate exception thrown
- Clear error message
- No database queries executed
- No system errors

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### NT-002: Null Parameter Handling

| Field | Value |
|-------|-------|
| **Test Case ID** | NT-002 |
| **Priority** | P1 - High |
| **Test Type** | Negative |
| **Component** | All controllers |

**Objective:** Verify null parameter handling

**Test Steps:**
1. Call methods with null parameters
2. Verify graceful error handling
3. Verify no NullPointerException

**Expected Results:**
- Parameters validated
- Clear error messages
- No system exceptions
- User-friendly errors

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### NT-003: Governor Limits - Maximum Results

| Field | Value |
|-------|-------|
| **Test Case ID** | NT-003 |
| **Priority** | P1 - High |
| **Test Type** | Negative, Limits |
| **Component** | ContactSearchService |

**Objective:** Verify behavior at governor limits

**Test Steps:**
1. Create scenario with 50,000 contacts
2. Attempt broad search
3. Verify limits respected

**Expected Results:**
- Query limited to configured maximum (100)
- No LimitException thrown
- Results returned successfully
- Performance acceptable

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Data-Driven Test Cases

### DD-001: Search Variations

| Field | Value |
|-------|-------|
| **Test Case ID** | DD-001 |
| **Priority** | P1 - High |
| **Test Type** | Data-Driven |
| **Component** | ContactSearchService |

**Objective:** Test multiple search scenarios

**Test Data:**

| Scenario | First Name | Last Name | Email | Phone | Expected Count |
|----------|-----------|-----------|-------|-------|----------------|
| 1 | John | | | | 5 |
| 2 | | Smith | | | 10 |
| 3 | John | Smith | | | 2 |
| 4 | | | john@example.com | | 1 |
| 5 | | | | 5551234567 | 1 |
| 6 | J% | | | | 15 |

**Test Steps:**
For each scenario:
1. Execute search with given criteria
2. Verify result count matches expected
3. Verify all results match criteria

**Expected Results:**
- All scenarios pass
- Results accurate for each variation
- Performance consistent

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### DD-002: Contact Creation Variations

| Field | Value |
|-------|-------|
| **Test Case ID** | DD-002 |
| **Priority** | P1 - High |
| **Test Type** | Data-Driven |
| **Component** | ContactManagementService |

**Objective:** Test contact creation with various data

**Test Data:**

| Scenario | Type | Has Email | Has Phone | Has Title | Should Succeed |
|----------|------|-----------|-----------|-----------|----------------|
| 1 | Customer | Yes | Yes | Yes | Yes |
| 2 | Customer | Yes | No | Yes | Yes |
| 3 | Customer | No | Yes | Yes | Yes |
| 4 | Customer | No | No | Yes | Yes |
| 5 | Vendor | Yes | Yes | No | Yes |
| 6 | Internal | Yes | No | No | Yes |

**Test Steps:**
For each scenario:
1. Create contact with specified data
2. Verify creation success/failure matches expected
3. Verify required fields enforced

**Expected Results:**
- All scenarios behave as expected
- Validation rules enforced
- Data integrity maintained

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Test Execution Schedule

### Week 1: Unit & Functional Testing
| Day | Test Cases | Owner | Status |
|-----|------------|-------|--------|
| Mon | FC-001 to FC-006 | QA Engineer 1 | [ ] |
| Tue | FC-007 to FC-012 | QA Engineer 1 | [ ] |
| Wed | PT-001 to PT-003 | QA Engineer 2 | [ ] |
| Thu | PT-004 to PT-006 | QA Engineer 2 | [ ] |
| Fri | IT-001 to IT-004 | QA Lead | [ ] |

### Week 2: Security & Regression Testing
| Day | Test Cases | Owner | Status |
|-----|------------|-------|--------|
| Mon | ST-001 to ST-005 | Security Specialist | [ ] |
| Tue | RT-001 to RT-003 | QA Engineer 1 | [ ] |
| Wed | NT-001 to NT-003 | QA Engineer 2 | [ ] |
| Thu | DD-001 to DD-002 | QA Engineer 1 | [ ] |
| Fri | Exploratory Testing | All | [ ] |

### Week 3: Bug Fixes & Retesting
| Day | Activities | Owner | Status |
|-----|------------|-------|--------|
| Mon-Wed | Fix defects | Dev Team | [ ] |
| Thu-Fri | Retest failures | QA Team | [ ] |

---

## Test Data Requirements

### Account Data
```sql
-- 25 Client Accounts
-- 25 Location Accounts (children of Clients)
-- 25 Vendor Accounts
-- 25 Mixed/Other Accounts
```

### Contact Data
```sql
-- 250 Customer Contacts
--   - 50 at Client level
--   - 200 at Location level
--   - Various titles and departments
--   - 10 with "Unspecified" first name
--   - Mix of active and inactive titles

-- 150 Vendor Contacts
--   - Associated with Vendor accounts
--   - Various roles
--   - Mix of email/phone availability

-- 100 Internal Contacts
--   - Account Team Members
--   - Various roles
```

### Case Data
```sql
-- 50 Cases
--   - 20 with Location (Customer contact type)
--   - 15 with Vendor (Vendor contact type)
--   - 10 with neither (Internal contact type)
--   - 5 already with contacts assigned
--   - Various types: Activate, Deactivate, Modify, Service
--   - Various statuses: New, In Progress, Closed
```

### Account Title Data
```sql
-- 20 Account Titles
--   - 15 Active
--   - 5 Inactive
--   - Various names: Operations Manager, Facility Manager, etc.
```

---

## Defect Management

### Defect Severity Levels

**P0 - Critical**
- System crash or data loss
- Security vulnerability
- Core functionality broken
- Blocker for deployment

**P1 - High**
- Major functionality impaired
- No reasonable workaround
- Significant performance degradation
- Affects many users

**P2 - Medium**
- Minor functionality issue
- Workaround available
- Affects few users
- Cosmetic issues

**P3 - Low**
- Enhancement request
- Minor inconvenience
- Affects very few users
- Nice-to-have improvements

### Defect Template

```markdown
**Defect ID:** DEF-[NUMBER]
**Test Case ID:** [TC-ID]
**Severity:** [P0/P1/P2/P3]
**Component:** [Component Name]

**Summary:** [One-line description]

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happened]

**Screenshots/Logs:**
[Attach evidence]

**Environment:**
- Org: [Sandbox name]
- User: [Test user]
- Date/Time: [When occurred]

**Status:** Open/In Progress/Fixed/Closed
**Assigned To:** [Developer name]
**Fix Version:** [Release version]
```

### Exit Criteria

Testing is complete when:
- ✓ All P0 test cases pass (100%)
- ✓ 95%+ P1 test cases pass
- ✓ All P0/P1 defects resolved
- ✓ Performance targets met
- ✓ Security review approved
- ✓ Code coverage ≥80%
- ✓ Regression testing passed
- ✓ Stakeholder sign-off obtained

---

## Test Summary Report Template

```markdown
# Test Summary Report: Apex Controller Refactoring

**Test Period:** [Start Date] - [End Date]
**QA Lead:** [Name]
**Status:** [In Progress/Complete]

## Test Execution Summary

| Category | Total | Executed | Passed | Failed | Blocked | Pass Rate |
|----------|-------|----------|--------|--------|---------|-----------|
| Functional | 12 | 12 | 11 | 1 | 0 | 92% |
| Performance | 6 | 6 | 6 | 0 | 0 | 100% |
| Integration | 4 | 4 | 4 | 0 | 0 | 100% |
| Security | 5 | 5 | 5 | 0 | 0 | 100% |
| Regression | 3 | 3 | 3 | 0 | 0 | 100% |
| Negative | 3 | 3 | 3 | 0 | 0 | 100% |
| Data-Driven | 2 | 2 | 2 | 0 | 0 | 100% |
| **Total** | **35** | **35** | **34** | **1** | **0** | **97%** |

## Performance Metrics

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Search Response Time | <500ms | 380ms | ✓ Pass |
| CPU Time | <5,000ms | 3,200ms | ✓ Pass |
| SOQL Queries | <10 | 7 | ✓ Pass |
| Code Coverage | ≥80% | 85% | ✓ Pass |

## Defects Summary

| Severity | Open | In Progress | Fixed | Total |
|----------|------|-------------|-------|-------|
| P0 | 0 | 0 | 0 | 0 |
| P1 | 0 | 0 | 1 | 1 |
| P2 | 0 | 1 | 2 | 3 |
| P3 | 1 | 0 | 0 | 1 |
| **Total** | **1** | **1** | **3** | **5** |

## Recommendation

[Ready for Production / Needs Additional Testing / Blocked]

**Sign-off:**
- QA Lead: _________________ Date: _______
- Technical Lead: _________________ Date: _______
```

---

**Document Status:** Ready for Test Execution
**Next Steps:** Begin test execution per schedule, log results, report defects

---

**End of QA Test Case Scenarios Document**
