# QA Test Case Scenarios: As-Is Aura to LWC Migration

**Project Code:** CSC-LWC-ASIS-2026-002
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
3. [Functional Parity Test Cases](#functional-parity-test-cases)
4. [UI/UX Consistency Test Cases](#uiux-consistency-test-cases)
5. [Browser Compatibility Test Cases](#browser-compatibility-test-cases)
6. [Mobile Responsiveness Test Cases](#mobile-responsiveness-test-cases)
7. [Component Communication Test Cases](#component-communication-test-cases)
8. [Jest Unit Test Verification](#jest-unit-test-verification)
9. [Performance Test Cases](#performance-test-cases)
10. [Accessibility Test Cases](#accessibility-test-cases)
11. [Integration Test Cases](#integration-test-cases)
12. [Regression Test Cases](#regression-test-cases)
13. [Test Execution Schedule](#test-execution-schedule)
14. [Defect Management](#defect-management)

---

## Test Strategy Overview

### Objectives
- Verify 100% functional parity with Aura component
- Validate performance improvements (30-40% faster)
- Ensure consistent UI/UX experience
- Confirm browser compatibility
- Validate mobile responsiveness
- Achieve 85%+ Jest test coverage

### Key Testing Principle
**"Like-for-Like" Migration** - Every feature, workflow, and UI element must work identically to the Aura component

### Success Criteria
- ✓ All 40+ functional parity items verified (100%)
- ✓ Performance improvements achieved (30-40% faster load)
- ✓ All supported browsers pass (100%)
- ✓ Mobile devices fully functional
- ✓ Jest coverage ≥85%
- ✓ Zero critical defects
- ✓ User acceptance: >80% prefer or equal to Aura

### Test Approach
- **Automated:** Jest unit tests (85%+ coverage)
- **Manual:** UI/UX verification, exploratory testing
- **Side-by-Side:** Aura vs LWC comparison testing
- **Performance:** Automated scripts with debug logs
- **Browser:** BrowserStack for cross-browser testing

---

## Test Environment Setup

### Prerequisites
- [x] Full copy sandbox with production data
- [x] Phase 1 (Apex Refactoring) deployed and stable
- [x] LWC components deployed
- [x] Lightning pages updated (test pages first)
- [x] Test data loaded
- [x] BrowserStack account configured
- [x] Mobile test devices available

### Test Environments
1. **Aura Reference Environment** - Original component for comparison
2. **LWC Test Environment** - New LWC component
3. **Side-by-Side Environment** - Both components available

### Test Browsers
| Browser | Version | Platform |
|---------|---------|----------|
| Chrome | Latest 2 | Windows, Mac, Linux |
| Firefox | Latest 2 | Windows, Mac |
| Safari | Latest 2 | Mac, iOS |
| Edge | Latest 2 | Windows |

### Test Devices
| Device | OS | Screen Size |
|--------|----|-----------  |
| iPhone 13 | iOS 15+ | 6.1" |
| Samsung Galaxy S21 | Android 11+ | 6.2" |
| iPad Pro | iOS 15+ | 12.9" |
| Windows Desktop | Win 10/11 | 1920x1080 |
| MacBook Pro | macOS | 2560x1600 |

---

## Functional Parity Test Cases

### FP-001: Contact Type Selection - Customer

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactTypeSelector |

**Objective:** Verify Customer contact type selection works identically to Aura

**Pre-conditions:**
- Both Aura and LWC components available in sandbox

**Test Steps:**
1. **Aura Component:**
   - Open SearchExistingContact (Aura)
   - Click "Customer" button
   - Observe behavior

2. **LWC Component:**
   - Open searchExistingContact (LWC)
   - Click "Customer" button
   - Observe behavior

3. **Compare:**
   - Button states
   - UI changes
   - Fields displayed
   - Search behavior

**Expected Results:**
- Button changes to selected state (same visual)
- Other buttons deselected
- Customer search fields displayed
- Location contacts auto-loaded (if location present)
- Behavior identical in both versions

**Comparison Checklist:**
- [ ] Button visual state identical
- [ ] Deselection of other types identical
- [ ] Field display identical
- [ ] Auto-search behavior identical
- [ ] Performance similar or better

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-002: Contact Type Selection - Vendor

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactTypeSelector |

**Objective:** Verify Vendor contact type selection

**Test Steps:**
1. Select "Vendor" in both Aura and LWC
2. Compare behavior

**Expected Results:**
- Vendor search interface displayed
- Vendor list shown (if applicable)
- Single search field displayed
- Identical behavior

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-003: Multi-Field Customer Search

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-003 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactSearchForm |

**Objective:** Verify multi-field search works identically

**Test Data:**
- First Name: "John"
- Last Name: "Smith"
- Email: "john.smith@example.com"
- Phone: "5551234567"

**Test Steps:**
1. Enter search criteria in Aura component
2. Observe results and timing
3. Enter same criteria in LWC component
4. Observe results and timing
5. Compare

**Expected Results:**
| Aspect | Aura | LWC | Match? |
|--------|------|-----|--------|
| Result Count | ___ | ___ | [ ] |
| Result Order | ___ | ___ | [ ] |
| Response Time | ___ ms | ___ ms | [ ] |
| Fields Displayed | ___ | ___ | [ ] |
| Behavior | ___ | ___ | [ ] |

**Parity Items:**
- [ ] Same search results
- [ ] Same result order
- [ ] Same field display
- [ ] Similar or better performance
- [ ] Same error handling

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-004: Search Result Selection

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-004 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactSearchResults |

**Objective:** Verify contact selection from results

**Test Steps:**
1. Perform search in both components
2. Select contact from results
3. Compare behavior

**Expected Results:**
- Single row selection (maxRowSelection=1)
- Selected contact displayed in details panel
- Contact information shown correctly
- "Select Contact" button enabled
- Row highlighting identical
- BR Association highlighting identical

**Comparison:**
- [ ] Selection behavior identical
- [ ] Details display identical
- [ ] Button states identical
- [ ] Visual highlighting identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-005: New Contact Button Visibility

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-005 |
| **Priority** | P1 - High |
| **Test Type** | Functional Parity |
| **Component** | contactSearchResults |

**Objective:** Verify "New Contact" button appears at correct times

**Test Scenarios:**

| Scenario | Results Count | Case Type | Show Button? |
|----------|---------------|-----------|--------------|
| 1 | 0 | Any | Yes |
| 2 | 1-4 | Activate | Yes |
| 3 | 1-4 | Deactivate | Yes |
| 4 | 1-4 | Modify | Yes |
| 5 | 1-4 | Other | No |
| 6 | 5+ | Any | No |

**Test Steps:**
For each scenario:
1. Set up test conditions
2. Perform search in Aura
3. Observe button visibility
4. Perform search in LWC
5. Compare button visibility

**Expected Results:**
- Button visibility rules identical
- Button placement identical
- Button styling identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-006: Contact Creation Form - Customer

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-006 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactCreationForm |

**Objective:** Verify customer contact creation form

**Test Steps:**
1. Click "New Contact" in both components
2. Compare form fields and layout

**Form Fields Checklist:**
- [ ] First Name field (required)
- [ ] Last Name field (required)
- [ ] Email Address field
- [ ] Preferred Phone Number field
- [ ] Phone Extension field (6 char max)
- [ ] Preferred Contact Method dropdown (required)
- [ ] Account Title dropdown (required)
- [ ] "Add New Title" button
- [ ] Department dropdown
- [ ] "Save Contact" button

**Expected Results:**
- All fields present in same order
- Same validation rules
- Same required field indicators
- Same field labels and placeholders
- Same dropdown options
- Button placement identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-007: Contact Creation Form - Vendor

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-007 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactCreationForm |

**Objective:** Verify vendor contact creation form

**Form Fields Checklist:**
- [ ] First Name field
- [ ] Last Name field
- [ ] Email Address field
- [ ] Phone Number field
- [ ] Extension field
- [ ] Preferred Contact Method
- [ ] Vendor Role selection

**Expected Results:**
- Vendor-specific fields only
- No Account Title field (customer only)
- No Department field (customer only)
- Same validation rules

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-008: Duplicate Detection Modal

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-008 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | duplicateDetectionModal |

**Objective:** Verify duplicate detection modal appears and functions

**Test Steps:**
1. Attempt to create duplicate contact in Aura
2. Observe modal display
3. Attempt to create duplicate contact in LWC
4. Observe modal display
5. Compare

**Expected Results:**
- Modal appears automatically on duplicate detection
- "Potential Duplicate Contacts" title displayed
- Datatable with duplicates shown
- Same columns displayed:
  - Name
  - Title
  - Phone
  - Email
  - BR Association
  - Last Activity
- "Continue" button available
- Row selection works
- Modal closeable
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-009: Account Title Selection

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-009 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | contactCreationForm |

**Objective:** Verify account title dropdown works

**Test Steps:**
1. Open new contact form in both components
2. Click Account Title dropdown
3. Compare options

**Expected Results:**
- Dropdown populated from same Apex method
- Only Active titles shown
- Sorted alphabetically
- Same title list in both components
- Selection works identically

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-010: Add New Title Functionality

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-010 |
| **Priority** | P1 - High |
| **Test Type** | Functional Parity |
| **Component** | contactCreationForm |

**Objective:** Verify "Add New Title" button works

**Test Steps:**
1. Click "Add New Title" in both components
2. Enter new title name
3. Save
4. Verify new title appears in dropdown
5. Compare behavior

**Expected Results:**
- Modal/component opens for title entry
- Title name field available
- Save functionality works
- New title immediately available in dropdown
- Toast message shown: "Your new title is now available..."
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-011: Contact Save - Success

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-011 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | Full workflow |

**Objective:** Verify contact save success workflow

**Test Steps:**
1. Fill out new contact form with valid data
2. Click "Save Contact"
3. Observe behavior in both components

**Expected Results:**
- Contact created in database
- Contact associated to case
- Toast message: "Contact created successfully" (or similar)
- Modal/component closes
- Case page refreshes
- New contact visible on case
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-012: Inactive Account Title Validation

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-012 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | Contact association |

**Objective:** Verify inactive title validation

**Pre-conditions:**
- Contact with inactive account title exists

**Test Steps:**
1. Search for and select contact with inactive title
2. Attempt to associate to case
3. Observe error in both components

**Expected Results:**
- Error toast displayed
- Error message: "Contact's Account Title is inactive. Please update..."
- Contact NOT associated
- User remains on component
- Mode is "sticky" (doesn't auto-close)
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-013: Internal User Search

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-013 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | Internal user search |

**Objective:** Verify internal user search works

**Test Steps:**
1. Select "Internal" contact type
2. Enter user search term
3. Compare results

**Expected Results:**
- Single search field displayed
- User search works on Name, Email
- Account Team Members shown
- User selection works
- User details displayed
- "Select User" button works
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-014: Modal Minimize/Maximize

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-014 |
| **Priority** | P2 - Medium |
| **Test Type** | Functional Parity |
| **Component** | Main modal |

**Objective:** Verify minimize/maximize functionality

**Test Steps:**
1. Click minimize button (dash icon)
2. Observe minimized state
3. Click maximize button
4. Observe restored state

**Expected Results:**
- Modal minimizes to bottom of screen or similar
- Modal content hidden when minimized
- Maximize button available when minimized
- Modal restores to previous state
- No data loss during minimize/maximize
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-015: Modal Close

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-015 |
| **Priority** | P0 - Critical |
| **Test Type** | Functional Parity |
| **Component** | Main modal |

**Objective:** Verify modal close functionality

**Test Steps:**
1. Open component
2. Click close button (X icon)
3. Observe behavior

**Expected Results:**
- Modal closes immediately
- Component removed from DOM
- No unsaved data warning (current behavior)
- Parent page not refreshed (unless save occurred)
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-016: Search Debouncing

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-016 |
| **Priority** | P1 - High |
| **Test Type** | Functional Parity |
| **Component** | contactSearchForm |

**Objective:** Verify search triggers appropriately

**Test Steps:**
1. Type in search field quickly
2. Observe when search fires
3. Compare timing

**Expected Results:**
- Search does NOT fire on every keystroke
- Search fires after brief pause (debounce)
- Search fires on blur from field
- Search fires on Enter key
- Behavior similar (LWC should be better with proper debounce)

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-017: Business Rule Association Highlighting

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-017 |
| **Priority** | P1 - High |
| **Test Type** | Functional Parity |
| **Component** | contactSearchResults |

**Objective:** Verify BR Association highlighting

**Test Steps:**
1. Perform search returning contacts with and without BR Association
2. Observe row highlighting

**Expected Results:**
- Contacts with BR Association = "Yes" highlighted differently
- CSS class "bgHighlight" applied (or equivalent)
- Visual distinction clear
- Highlighting identical in both components

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-018: Location Contact Auto-Load

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-018 |
| **Priority** | P1 - High |
| **Test Type** | Functional Parity |
| **Component** | Auto-search on load |

**Objective:** Verify contacts auto-load for location cases

**Pre-conditions:**
- Case with Location set
- Location has associated contacts

**Test Steps:**
1. Open component on case with location
2. Observe auto-loading

**Expected Results:**
- Contacts auto-loaded without user action
- Customer type pre-selected
- Location contacts displayed
- "Unspecified" contacts excluded
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-019: Field Validation - Required Fields

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-019 |
| **Priority** | P1 - High |
| **Test Type** | Functional Parity |
| **Component** | contactCreationForm |

**Objective:** Verify required field validation

**Test Steps:**
1. Leave required fields blank
2. Attempt to save
3. Observe validation

**Required Fields:**
- First Name
- Last Name
- Preferred Contact Method
- Account Title (customer only)

**Expected Results:**
- Validation prevents save
- Required field indicators shown (red asterisk)
- Error messages displayed
- Form does not submit
- User remains on form
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### FP-020: Phone Number Format Validation

| Field | Value |
|-------|-------|
| **Test Case ID** | FP-020 |
| **Priority** | P2 - Medium |
| **Test Type** | Functional Parity |
| **Component** | contactCreationForm |

**Objective:** Verify phone format validation

**Test Data:**
- Valid: "5551234567" (10 digits)
- Invalid: "555" (too short)
- Invalid: "abcd" (non-numeric)

**Test Steps:**
1. Enter invalid phone in both components
2. Observe validation
3. Enter valid phone
4. Observe acceptance

**Expected Results:**
- Pattern validation applied (10 digits)
- Invalid formats rejected
- Validation message shown
- Behavior identical

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## UI/UX Consistency Test Cases

### UI-001: Visual Layout Comparison

| Field | Value |
|-------|-------|
| **Test Case ID** | UI-001 |
| **Priority** | P0 - Critical |
| **Test Type** | UI/UX |
| **Component** | All |

**Objective:** Verify visual layout matches Aura component

**Test Method:** Side-by-side screenshot comparison

**Areas to Compare:**
1. Modal size and positioning
2. Button placement and styling
3. Form field layout
4. Datatable appearance
5. Color scheme
6. Font sizes and weights
7. Spacing and padding
8. Icons

**Expected Results:**
- 95%+ visual similarity
- Any differences must be improvements (SLDS compliance)
- Layout responsive and functional
- No broken layouts

**Comparison Screenshots:**
- [ ] Contact type selector
- [ ] Customer search form
- [ ] Vendor search interface
- [ ] Search results datatable
- [ ] Contact details panel
- [ ] New contact form
- [ ] Duplicate modal

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### UI-002: SLDS Component Usage

| Field | Value |
|-------|-------|
| **Test Case ID** | UI-002 |
| **Priority** | P1 - High |
| **Test Type** | UI/UX |
| **Component** | All |

**Objective:** Verify proper SLDS component usage

**Checklist:**
- [ ] lightning-button-stateful used correctly
- [ ] lightning-datatable configured properly
- [ ] lightning-input types correct
- [ ] lightning-layout structure valid
- [ ] lightning-record-form (if used) configured
- [ ] Proper SLDS classes applied
- [ ] No deprecated SLDS patterns

**Expected Results:**
- All Lightning base components used correctly
- SLDS markup valid
- Components render properly
- No console errors

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### UI-003: Button States and Interactions

| Field | Value |
|-------|-------|
| **Test Case ID** | UI-003 |
| **Priority** | P1 - High |
| **Test Type** | UI/UX |
| **Component** | All buttons |

**Objective:** Verify button states work correctly

**Buttons to Test:**
1. Contact type selector buttons (stateful)
2. New Contact button
3. Save Contact button
4. Select Contact button
5. Close button (X)
6. Minimize button (dash)
7. Add New Title button

**States to Verify:**
- Default state
- Hover state
- Active/pressed state
- Disabled state (if applicable)
- Loading state (if applicable)

**Expected Results:**
- All states render correctly
- Visual feedback on interaction
- Disabled states prevent action
- Loading states show spinner
- Behavior matches Aura

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### UI-004: Loading Indicators

| Field | Value |
|-------|-------|
| **Test Case ID** | UI-004 |
| **Priority** | P1 - High |
| **Test Type** | UI/UX |
| **Component** | All async operations |

**Objective:** Verify loading indicators appear

**Operations to Test:**
- Search execution
- Contact creation
- Contact association
- Account title retrieval
- Initial component load

**Expected Results:**
- lightning-spinner shown during async operations
- User cannot interact during loading
- Spinner dismissed after operation
- No indefinite loading states
- Behavior matches or improves on Aura

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### UI-005: Toast Messages

| Field | Value |
|-------|-------|
| **Test Case ID** | UI-005 |
| **Priority** | P1 - High |
| **Test Type** | UI/UX |
| **Component** | Toast notifications |

**Objective:** Verify toast messages displayed correctly

**Toast Scenarios:**
- Contact created successfully
- Contact associated successfully
- Account title inactive error
- Generic error messages
- New title created

**Expected Results:**
- Toast appears at top of screen
- Correct variant (success/error/warning)
- Message text clear and helpful
- Toast auto-dismisses (success)
- Error toasts persist until dismissed
- Behavior identical to Aura

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Browser Compatibility Test Cases

### BC-001: Chrome - Latest Version

| Field | Value |
|-------|-------|
| **Test Case ID** | BC-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Browser Compatibility |
| **Browser** | Chrome Latest |

**Test Scope:** Execute core functional tests (FP-001 through FP-020)

**Expected Results:**
- All functionality works
- No console errors
- No visual rendering issues
- Performance acceptable

**Test Results:**
| Test | Status | Notes |
|------|--------|-------|
| FP-001 | [ ] Pass [ ] Fail | |
| FP-003 | [ ] Pass [ ] Fail | |
| FP-006 | [ ] Pass [ ] Fail | |
| FP-011 | [ ] Pass [ ] Fail | |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### BC-002: Firefox - Latest Version

| Field | Value |
|-------|-------|
| **Test Case ID** | BC-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Browser Compatibility |
| **Browser** | Firefox Latest |

**Test Scope:** Execute core functional tests

**Expected Results:**
- All functionality works
- No Firefox-specific issues
- Event handling works correctly
- CSS renders properly

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### BC-003: Safari - Latest Version

| Field | Value |
|-------|-------|
| **Test Case ID** | BC-003 |
| **Priority** | P0 - Critical |
| **Test Type** | Browser Compatibility |
| **Browser** | Safari Latest (Mac) |

**Test Scope:** Execute core functional tests

**Expected Results:**
- All functionality works
- No Safari-specific rendering issues
- Date/time handling correct
- Form validation works

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### BC-004: Edge - Latest Version

| Field | Value |
|-------|-------|
| **Test Case ID** | BC-004 |
| **Priority** | P1 - High |
| **Test Type** | Browser Compatibility |
| **Browser** | Edge Latest |

**Test Scope:** Execute core functional tests

**Expected Results:**
- All functionality works
- Chromium-based Edge compatible
- No Edge-specific issues

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Mobile Responsiveness Test Cases

### MR-001: iPhone - Portrait Mode

| Field | Value |
|-------|-------|
| **Test Case ID** | MR-001 |
| **Priority** | P1 - High |
| **Test Type** | Mobile Responsiveness |
| **Device** | iPhone 13 (iOS 15+) |

**Objective:** Verify component works on iPhone in portrait

**Test Areas:**
1. Modal fits screen (no horizontal scroll)
2. Buttons touch-friendly (44x44px minimum)
3. Text readable without zooming
4. Form fields accessible
5. Datatable scrollable
6. All functions accessible

**Expected Results:**
- Component fully functional on mobile
- No layout breaking
- Touch interactions work
- Virtual keyboard doesn't break layout
- Performance acceptable

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### MR-002: iPhone - Landscape Mode

| Field | Value |
|-------|-------|
| **Test Case ID** | MR-002 |
| **Priority** | P2 - Medium |
| **Test Type** | Mobile Responsiveness |
| **Device** | iPhone 13 (iOS 15+) |

**Objective:** Verify component works in landscape

**Expected Results:**
- Layout adjusts to landscape
- All content visible
- Functions work correctly

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### MR-003: Android - Portrait Mode

| Field | Value |
|-------|-------|
| **Test Case ID** | MR-003 |
| **Priority** | P1 - High |
| **Test Type** | Mobile Responsiveness |
| **Device** | Samsung Galaxy S21 |

**Objective:** Verify component works on Android

**Expected Results:**
- Same functionality as iPhone
- No Android-specific issues
- Performance comparable

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### MR-004: Tablet - iPad

| Field | Value |
|-------|-------|
| **Test Case ID** | MR-004 |
| **Priority** | P1 - High |
| **Test Type** | Mobile Responsiveness |
| **Device** | iPad Pro 12.9" |

**Objective:** Verify component works on tablet

**Expected Results:**
- Larger screen utilized effectively
- Layout scales appropriately
- Desktop-like experience where appropriate
- Touch still works (not just mouse)

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Component Communication Test Cases

### CC-001: Parent to Child Event Flow

| Field | Value |
|-------|-------|
| **Test Case ID** | CC-001 |
| **Priority** | P1 - High |
| **Test Type** | Component Communication |
| **Component** | Event flow |

**Objective:** Verify parent passes data to child components

**Test Cases:**
1. searchExistingContact passes recordId to children
2. searchExistingContact passes caseData to children
3. searchExistingContact passes searchResults to results component
4. searchExistingContact passes accountTitles to form component

**Expected Results:**
- @api properties work correctly
- Data flows one-way (parent to child)
- Child components receive updates
- Re-rendering occurs appropriately

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### CC-002: Child to Parent Event Flow

| Field | Value |
|-------|-------|
| **Test Case ID** | CC-002 |
| **Priority** | P1 - High |
| **Test Type** | Component Communication |
| **Component** | Event flow |

**Objective:** Verify child components dispatch events to parent

**Test Cases:**
1. contactTypeSelector dispatches 'contacttypechange'
2. contactSearchForm dispatches 'search'
3. contactSearchResults dispatches 'contactselect'
4. contactCreationForm dispatches 'save'

**Expected Results:**
- CustomEvent dispatched correctly
- Event detail contains correct data
- Parent receives and handles event
- State updates appropriately

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### CC-003: Component Isolation

| Field | Value |
|-------|-------|
| **Test Case ID** | CC-003 |
| **Priority** | P1 - High |
| **Test Type** | Component Communication |
| **Component** | All |

**Objective:** Verify components are properly isolated

**Test Cases:**
1. Child component cannot directly modify parent state
2. Siblings cannot directly communicate
3. Shadow DOM isolation works
4. No global variable pollution

**Expected Results:**
- Proper encapsulation maintained
- Communication only via events and @api
- No unexpected side effects
- Clean component boundaries

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Jest Unit Test Verification

### JEST-001: Test Coverage Verification

| Field | Value |
|-------|-------|
| **Test Case ID** | JEST-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Unit Test Verification |
| **Component** | All LWC components |

**Objective:** Verify Jest test coverage meets target

**Command:**
```bash
npm run test:unit:coverage
```

**Expected Results:**
- Overall coverage ≥85%
- Per-component coverage:
  - searchExistingContact: ≥85%
  - contactTypeSelector: ≥85%
  - contactSearchForm: ≥85%
  - contactSearchResults: ≥85%
  - contactCreationForm: ≥85%

**Coverage Report:**
| Component | Statements | Branches | Functions | Lines | Status |
|-----------|------------|----------|-----------|-------|--------|
| searchExistingContact | ___% | ___% | ___% | ___% | [ ] |
| contactTypeSelector | ___% | ___% | ___% | ___% | [ ] |
| contactSearchForm | ___% | ___% | ___% | ___% | [ ] |
| contactSearchResults | ___% | ___% | ___% | ___% | [ ] |
| contactCreationForm | ___% | ___% | ___% | ___% | [ ] |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### JEST-002: Test Execution Verification

| Field | Value |
|-------|-------|
| **Test Case ID** | JEST-002 |
| **Priority** | P0 - Critical |
| **Test Type** | Unit Test Verification |
| **Component** | All Jest tests |

**Objective:** Verify all Jest tests pass

**Command:**
```bash
npm run test:unit
```

**Expected Results:**
- All tests pass
- No failing tests
- No skipped tests
- Execution time reasonable (<5 minutes)

**Test Results:**
- Total Tests: ___
- Passing: ___
- Failing: ___
- Skipped: ___
- Execution Time: ___ seconds

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Performance Test Cases

### PERF-001: Initial Load Time Comparison

| Field | Value |
|-------|-------|
| **Test Case ID** | PERF-001 |
| **Priority** | P0 - Critical |
| **Test Type** | Performance |
| **Component** | Full component |

**Objective:** Verify LWC loads faster than Aura

**Test Method:**
1. Clear browser cache
2. Open Aura component
3. Measure load time (Chrome DevTools)
4. Clear browser cache
5. Open LWC component
6. Measure load time
7. Repeat 10 times, average results

**Performance Targets:**
- Aura baseline: 3,000-4,000ms
- LWC target: <2,500ms (30-40% improvement)

**Test Results:**
| Run | Aura (ms) | LWC (ms) | Improvement |
|-----|-----------|----------|-------------|
| 1 | ___ | ___ | ___% |
| 2 | ___ | ___ | ___% |
| 3 | ___ | ___ | ___% |
| Avg | ___ | ___ | ___% |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PERF-002: Re-render Performance

| Field | Value |
|-------|-------|
| **Test Case ID** | PERF-002 |
| **Priority** | P1 - High |
| **Test Type** | Performance |
| **Component** | State updates |

**Objective:** Verify re-render performance improved

**Test Method:**
1. Perform search (trigger re-render)
2. Measure render time
3. Compare Aura vs LWC

**Performance Targets:**
- Aura baseline: 500-800ms
- LWC target: <300ms (50% improvement)

**Test Results:**
| Operation | Aura (ms) | LWC (ms) | Improvement |
|-----------|-----------|----------|-------------|
| Search Results Render | ___ | ___ | ___% |
| Form Field Update | ___ | ___ | ___% |
| Contact Selection | ___ | ___ | ___% |

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### PERF-003: Bundle Size

| Field | Value |
|-------|-------|
| **Test Case ID** | PERF-003 |
| **Priority** | P1 - High |
| **Test Type** | Performance |
| **Component** | Bundle |

**Objective:** Verify bundle size acceptable

**Test Method:**
1. Check deployed LWC bundle size
2. Compare to target

**Performance Target:**
- Bundle size: <150kb

**Test Results:**
- Total Bundle Size: ___ kb
- Largest Component: ___ kb
- Status: [ ] Pass [ ] Fail

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Accessibility Test Cases

### ACC-001: Keyboard Navigation

| Field | Value |
|-------|-------|
| **Test Case ID** | ACC-001 |
| **Priority** | P1 - High |
| **Test Type** | Accessibility |
| **Component** | All |

**Objective:** Verify keyboard-only navigation works

**Test Steps:**
1. Use Tab to navigate through all interactive elements
2. Use Enter/Space to activate buttons
3. Use Arrow keys in dropdowns
4. Use Escape to close modals

**Expected Results:**
- All interactive elements reachable via keyboard
- Tab order logical
- Focus indicators visible
- No keyboard traps
- Shortcuts work (if implemented)

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### ACC-002: Screen Reader Compatibility

| Field | Value |
|-------|-------|
| **Test Case ID** | ACC-002 |
| **Priority** | P1 - High |
| **Test Type** | Accessibility |
| **Component** | All |

**Objective:** Verify screen reader announces correctly

**Test Method:** Use NVDA or JAWS

**Expected Results:**
- All labels read correctly
- Button states announced
- Form fields have associated labels
- Error messages announced
- Loading states announced
- Modal roles correct

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

## Test Execution Schedule

### Week 1: Functional Parity & UI/UX
| Day | Test Cases | Owner | Status |
|-----|------------|-------|--------|
| Mon | FP-001 to FP-006 | QA Eng 1 | [ ] |
| Tue | FP-007 to FP-012 | QA Eng 1 | [ ] |
| Wed | FP-013 to FP-020 | QA Eng 2 | [ ] |
| Thu | UI-001 to UI-005 | QA Eng 2 | [ ] |
| Fri | Review & Report | QA Lead | [ ] |

### Week 2: Browser, Mobile & Performance
| Day | Test Cases | Owner | Status |
|-----|------------|-------|--------|
| Mon | BC-001 to BC-004 | QA Eng 1 | [ ] |
| Tue | MR-001 to MR-004 | QA Eng 2 | [ ] |
| Wed | PERF-001 to PERF-003 | QA Eng 1 | [ ] |
| Thu | ACC-001 to ACC-002 | QA Eng 2 | [ ] |
| Fri | Component Comm Tests | QA Lead | [ ] |

### Week 3: Regression & UAT
| Day | Activities | Owner | Status |
|-----|------------|-------|--------|
| Mon | Regression Testing | All QA | [ ] |
| Tue-Thu | UAT Support | All QA | [ ] |
| Fri | Final Report | QA Lead | [ ] |

---

## Defect Management

### Exit Criteria

Testing complete when:
- ✓ All P0 functional parity tests pass (100%)
- ✓ 95%+ P1 tests pass
- ✓ Jest coverage ≥85%
- ✓ All supported browsers pass
- ✓ Mobile devices functional
- ✓ Performance targets met
- ✓ Zero critical defects
- ✓ UAT sign-off obtained

---

**Document Status:** Ready for Test Execution
**Next Steps:** Execute tests per schedule, track results, report defects

---

**End of QA Test Case Scenarios Document**
