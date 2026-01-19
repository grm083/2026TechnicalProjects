# Technical Design Document: As-Is Aura to LWC Migration

**Project Code:** CSC-LWC-ASIS-2026-002
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
| Senior LWC Developer | [Name] | _________________ | ______ |
| UX Lead | [Name] | _________________ | ______ |
| QA Lead | [Name] | _________________ | ______ |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Aura Architecture](#current-aura-architecture)
3. [Proposed LWC Architecture](#proposed-lwc-architecture)
4. [Component Design](#component-design)
5. [State Management](#state-management)
6. [Event Handling](#event-handling)
7. [API Integration](#api-integration)
8. [Migration Mapping](#migration-mapping)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Plan](#deployment-plan)
11. [Rollback Strategy](#rollback-strategy)
12. [Dependencies](#dependencies)
13. [Appendices](#appendices)

---

## Executive Summary

This document provides the technical design for migrating the SearchExistingContact Aura component to Lightning Web Components (LWC) while maintaining 100% functional parity. The migration will transform a 685-line monolithic Aura component into 3-4 focused LWC components using modern web standards.

### Key Changes
- Convert Aura component to LWC component structure
- Migrate 70+ Aura attributes to LWC tracked properties
- Replace Aura events with LWC custom events
- Modernize JavaScript from ES5 to ES6+
- Maintain exact UI layout and user workflows

### Performance Targets
- Initial load time: <2,500ms (30-40% improvement)
- Time to interactive: <3,000ms (40% improvement)
- Re-render time: <300ms (50% improvement)
- Bundle size: <150kb

### Non-Goals
- UI/UX redesign (see Project CSC-LWC-REDESIGN-2026-003)
- Additional features
- Workflow changes

---

## Current Aura Architecture

### Component Structure

**SearchExistingContact.cmp** (685 lines)
- **Controller:** SearchExistingContactController.js (270+ lines)
- **Helper:** SearchExistingContactHelper.js (500+ lines)
- **Style:** SearchExistingContact.css
- **Dependencies:**
  - ContactSearchandCreate Apex class
  - lightning:workspaceAPI
  - lightning:datatable (3 instances)
  - lightning:recordForm (5 instances)
  - c:SingleTabComponentRefresh event

### Component Responsibilities

1. **Contact Type Selection**
   - Three stateful buttons (Customer, Vendor, Internal)
   - Mutually exclusive selection logic
   - Context-based filtering

2. **Search Functionality**
   - Customer: Multi-field search (firstName, lastName, email, phone, mobile)
   - Vendor: Single search field + vendor selection
   - Internal: User search

3. **Results Display**
   - lightning:datatable with selection
   - Row highlighting for business rule association
   - Contact preview on selection

4. **Contact Creation**
   - Dynamic form based on contact type
   - Account title/department selection
   - Duplicate detection modal
   - Field validation

5. **Contact Association**
   - Link contact to case
   - Create account relationships
   - Update case contact field
   - Validation rules

### Current Attribute Map (70+ attributes)

| Category | Count | Examples |
|----------|-------|----------|
| Boolean State | 15 | boolCustomer, boolVendor, boolNewContact |
| String Data | 20+ | firstName, lastName, email, phone |
| Object Collections | 10 | soslContacts, dupContacts, vendorAccts |
| Display Control | 8 | showForm, showSearch, boolSOSL |
| Case Data | 7 | caseAccount, locAccount, caseContact |
| Configuration | 5+ | soslFields, dupFields, displayContFields |

---

## Proposed LWC Architecture

### Component Hierarchy

```
searchExistingContact (Main Container)
├── contactTypeSelector
│   └── Handles Customer/Vendor/Internal selection
├── searchExistingContactForm
│   ├── customerContactSearch
│   ├── vendorContactSearch
│   └── internalUserSearch
├── contactSearchResults
│   └── Datatable with selection
├── contactDetailsPanel
│   └── Selected contact display
└── contactCreationForm
    ├── customerContactForm
    ├── vendorContactForm
    └── duplicateDetectionModal
```

### Component Files Structure

```
force-app/main/default/lwc/
├── searchExistingContact/
│   ├── searchExistingContact.html (Main template)
│   ├── searchExistingContact.js (Container logic)
│   ├── searchExistingContact.css
│   └── searchExistingContact.js-meta.xml
├── contactTypeSelector/
│   ├── contactTypeSelector.html
│   ├── contactTypeSelector.js
│   └── contactTypeSelector.js-meta.xml
├── contactSearchForm/
│   ├── contactSearchForm.html
│   ├── contactSearchForm.js
│   └── contactSearchForm.js-meta.xml
└── contactCreationForm/
    ├── contactCreationForm.html
    ├── contactCreationForm.js
    └── contactCreationForm.js-meta.xml
```

---

## Component Design

### 1. Main Container Component

**File:** `searchExistingContact.js`

```javascript
import { LightningElement, api, track, wire } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { NavigationMixin } from 'lightning/navigation';
import { refreshApex } from '@salesforce/apex';

// Apex imports (refactored controller)
import searchContacts from '@salesforce/apex/ContactSearchController.searchContacts';
import createContactForCase from '@salesforce/apex/ContactSearchController.createContactForCase';
import associateContactToCase from '@salesforce/apex/ContactSearchController.associateContactToCase';
import getAccountTitles from '@salesforce/apex/ContactSearchController.getAccountTitles';
import getAccountDepts from '@salesforce/apex/ContactSearchController.getAccountDepts';

export default class SearchExistingContact extends NavigationMixin(LightningElement) {
    // Public API properties
    @api recordId; // Case record ID

    // Component state
    @track state = {
        // Contact type selection
        contactType: 'Customer', // Customer, Vendor, Internal

        // UI state
        isModalOpen: true,
        isMinimized: false,
        showNewContactForm: false,
        showDuplicateModal: false,
        isLoading: false,

        // Search state
        searchCriteria: {},
        searchResults: [],
        selectedContactId: null,

        // Form state
        newContact: {},
        duplicateContacts: [],

        // Case context
        caseData: null,
        existingContact: null,

        // Configuration
        accountTitles: [],
        accountDepts: [],
        vendorRoles: []
    };

    // Lifecycle hooks
    connectedCallback() {
        this.initializeComponent();
    }

    renderedCallback() {
        // Handle any post-render logic
    }

    // Initialization
    async initializeComponent() {
        try {
            this.state.isLoading = true;

            // Load case data
            await this.loadCaseData();

            // Load configuration data
            await this.loadConfigurationData();

            // Perform initial search if context available
            if (this.shouldAutoSearch()) {
                await this.performInitialSearch();
            }

        } catch (error) {
            this.handleError(error);
        } finally {
            this.state.isLoading = false;
        }
    }

    // Computed properties
    get isCustomer() {
        return this.state.contactType === 'Customer';
    }

    get isVendor() {
        return this.state.contactType === 'Vendor';
    }

    get isInternal() {
        return this.state.contactType === 'Internal';
    }

    get hasSearchResults() {
        return this.state.searchResults && this.state.searchResults.length > 0;
    }

    get hasSelectedContact() {
        return this.state.selectedContactId != null;
    }

    get showNewButton() {
        // Match Aura logic: show if no results or results < threshold
        return !this.hasSearchResults ||
               (this.state.searchResults.length < 5 &&
                this.isSpecialCaseType());
    }

    get modalClass() {
        return this.state.isMinimized ?
               'slds-modal slds-fade-in-open slds-modal_minimized' :
               'slds-modal slds-fade-in-open slds-modal_medium';
    }

    // Event handlers
    handleContactTypeChange(event) {
        const newType = event.detail.contactType;

        // Clear previous state
        this.state.contactType = newType;
        this.state.searchResults = [];
        this.state.selectedContactId = null;
        this.state.showNewContactForm = false;

        // Load type-specific data
        this.loadContactTypeData(newType);

        // Auto-search if criteria available
        if (this.shouldAutoSearch()) {
            this.performInitialSearch();
        }
    }

    handleSearch(event) {
        const criteria = event.detail.criteria;
        this.performSearch(criteria);
    }

    handleContactSelect(event) {
        this.state.selectedContactId = event.detail.contactId;
    }

    handleNewContact(event) {
        this.state.showNewContactForm = true;
        this.state.selectedContactId = null;
    }

    handleContactSave(event) {
        const contactData = event.detail.contactData;
        this.saveNewContact(contactData);
    }

    handleAssociateContact(event) {
        this.associateSelectedContact();
    }

    handleModalClose() {
        this.state.isModalOpen = false;

        // Dispatch event to parent
        this.dispatchEvent(new CustomEvent('modalclose'));
    }

    handleModalMinimize() {
        this.state.isMinimized = !this.state.isMinimized;
    }

    // Business logic methods
    async loadCaseData() {
        // Load case and related data
        const caseData = await this.getCaseContext();
        this.state.caseData = caseData;

        // Determine contact type based on case
        this.determineContactType(caseData);

        // Check if case already has contact
        if (caseData.contactId) {
            this.state.existingContact = caseData.contact;
        }
    }

    async loadConfigurationData() {
        try {
            // Load account titles
            if (this.state.caseData?.accountId) {
                this.state.accountTitles = await getAccountTitles({
                    accountId: this.state.caseData.accountId
                });
            }

            // Load account departments
            if (this.state.caseData?.accountId) {
                this.state.accountDepts = await getAccountDepts({
                    accountId: this.state.caseData.accountId
                });
            }

        } catch (error) {
            console.error('Error loading configuration:', error);
        }
    }

    async performSearch(criteria) {
        try {
            this.state.isLoading = true;
            this.state.searchCriteria = criteria;

            // Build search request
            const searchRequest = {
                ...criteria,
                accountId: this.state.caseData.accountId,
                contactType: this.state.contactType
            };

            // Call Apex
            const result = await searchContacts({
                criteria: JSON.stringify(searchRequest),
                caseId: this.recordId
            });

            // Update state
            this.state.searchResults = result.contacts || [];

        } catch (error) {
            this.handleError(error);
        } finally {
            this.state.isLoading = false;
        }
    }

    async saveNewContact(contactData) {
        try {
            this.state.isLoading = true;

            // Build contact request
            const request = {
                ...contactData,
                accountId: this.state.caseData.accountId,
                caseId: this.recordId,
                contactType: this.state.contactType
            };

            // Call Apex
            const result = await createContactForCase({
                request: JSON.stringify(request),
                caseId: this.recordId
            });

            // Handle result
            if (result.success) {
                if (result.duplicatesFound) {
                    // Show duplicate modal
                    this.state.duplicateContacts = result.duplicates;
                    this.state.showDuplicateModal = true;
                } else {
                    // Success - close modal and refresh
                    this.showToast('Success', 'Contact created successfully', 'success');
                    this.handleModalClose();
                    this.refreshParent();
                }
            } else {
                this.showToast('Error', result.message, 'error');
            }

        } catch (error) {
            this.handleError(error);
        } finally {
            this.state.isLoading = false;
        }
    }

    async associateSelectedContact() {
        try {
            this.state.isLoading = true;

            // Call Apex
            const result = await associateContactToCase({
                caseId: this.recordId,
                contactId: this.state.selectedContactId,
                contactType: this.state.contactType
            });

            // Handle result
            if (result.success) {
                this.showToast('Success', 'Contact associated successfully', 'success');
                this.handleModalClose();
                this.refreshParent();
            } else {
                this.showToast('Error', result.message, 'error');
            }

        } catch (error) {
            this.handleError(error);
        } finally {
            this.state.isLoading = false;
        }
    }

    // Utility methods
    determineContactType(caseData) {
        // Match Aura logic for contact type determination
        if (caseData.locationId && !caseData.vendorId) {
            this.state.contactType = 'Customer';
        } else if (caseData.vendorId) {
            this.state.contactType = 'Vendor';
        }
    }

    shouldAutoSearch() {
        const { caseData, contactType } = this.state;

        if (contactType === 'Customer' && caseData?.locationId) {
            return true;
        }
        if (contactType === 'Vendor' && caseData?.vendorId) {
            return true;
        }
        return false;
    }

    isSpecialCaseType() {
        const specialTypes = ['Activate', 'Deactivate', 'Modify'];
        return specialTypes.includes(this.state.caseData?.caseType);
    }

    async getCaseContext() {
        // Implement case data retrieval
        // This would call the refactored Apex controller
        return {}; // Placeholder
    }

    refreshParent() {
        // Refresh the parent page
        eval("$A.get('e.force:refreshView').fire();");
    }

    showToast(title, message, variant) {
        const event = new ShowToastEvent({
            title: title,
            message: message,
            variant: variant
        });
        this.dispatchEvent(event);
    }

    handleError(error) {
        console.error('Component error:', error);
        const message = error.body?.message || error.message || 'An error occurred';
        this.showToast('Error', message, 'error');
    }
}
```

**File:** `searchExistingContact.html`

```html
<template>
    <!-- Modal Container -->
    <template if:true={state.isModalOpen}>
        <section
            role="dialog"
            tabindex="-1"
            aria-modal="true"
            class={modalClass}
            style="position:fixed !important; padding-top:10rem;">

            <div class="slds-modal__container">
                <!-- Modal Header -->
                <header class="slds-modal__header">
                    <lightning-button-icon
                        icon-name="utility:dash"
                        variant="bare-inverse"
                        alternative-text="Minimize"
                        title="Minimize"
                        onclick={handleModalMinimize}
                        class="minimizeIcon">
                    </lightning-button-icon>

                    <lightning-button-icon
                        icon-name="utility:close"
                        variant="bare"
                        alternative-text="Close"
                        title="Close"
                        onclick={handleModalClose}
                        class="slds-modal__close">
                    </lightning-button-icon>

                    <h2 class="slds-text-heading_medium">Contact</h2>
                </header>

                <!-- Modal Content -->
                <div class="slds-modal__content slds-p-around_medium">
                    <!-- Loading Spinner -->
                    <template if:true={state.isLoading}>
                        <lightning-spinner
                            alternative-text="Loading..."
                            size="medium">
                        </lightning-spinner>
                    </template>

                    <!-- Contact Type Selector -->
                    <c-contact-type-selector
                        selected-type={state.contactType}
                        case-data={state.caseData}
                        oncontacttypechange={handleContactTypeChange}>
                    </c-contact-type-selector>

                    <!-- Main Content Area -->
                    <div class="slds-grid slds-wrap slds-p-around_small">
                        <!-- Left Panel: Search & Results -->
                        <div class="slds-col slds-size_1-of-2">
                            <c-contact-search-form
                                contact-type={state.contactType}
                                case-data={state.caseData}
                                onsearch={handleSearch}
                                onnewcontact={handleNewContact}>
                            </c-contact-search-form>

                            <!-- Search Results -->
                            <template if:true={hasSearchResults}>
                                <c-contact-search-results
                                    contacts={state.searchResults}
                                    selected-contact-id={state.selectedContactId}
                                    show-new-button={showNewButton}
                                    oncontactselect={handleContactSelect}
                                    onnewcontact={handleNewContact}>
                                </c-contact-search-results>
                            </template>
                        </div>

                        <!-- Right Panel: Details or Form -->
                        <div class="slds-col slds-size_1-of-2">
                            <!-- Selected Contact Details -->
                            <template if:true={hasSelectedContact}>
                                <c-contact-details-panel
                                    contact-id={state.selectedContactId}
                                    onassociate={handleAssociateContact}>
                                </c-contact-details-panel>
                            </template>

                            <!-- New Contact Form -->
                            <template if:true={state.showNewContactForm}>
                                <c-contact-creation-form
                                    contact-type={state.contactType}
                                    account-titles={state.accountTitles}
                                    account-depts={state.accountDepts}
                                    vendor-roles={state.vendorRoles}
                                    onsave={handleContactSave}
                                    oncancel={handleNewContactCancel}>
                                </c-contact-creation-form>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Backdrop -->
        <div class="slds-backdrop slds-backdrop_open"
             style="position:fixed !important;">
        </div>
    </template>

    <!-- Duplicate Detection Modal -->
    <template if:true={state.showDuplicateModal}>
        <c-duplicate-detection-modal
            duplicates={state.duplicateContacts}
            onclose={handleDuplicateModalClose}
            onselect={handleDuplicateSelect}>
        </c-duplicate-detection-modal>
    </template>
</template>
```

### 2. Contact Type Selector Component

**File:** `contactTypeSelector.js`

```javascript
import { LightningElement, api } from 'lwc';

export default class ContactTypeSelector extends LightningElement {
    @api selectedType = 'Customer';
    @api caseData;

    get isCustomer() {
        return this.selectedType === 'Customer';
    }

    get isVendor() {
        return this.selectedType === 'Vendor';
    }

    get isInternal() {
        return this.selectedType === 'Internal';
    }

    get showTypeSelector() {
        // Show selector if no contact yet or in edit mode
        return !this.caseData?.contactId || this.caseData?.isEditMode;
    }

    handleCustomerClick() {
        if (!this.isCustomer) {
            this.selectType('Customer');
        }
    }

    handleVendorClick() {
        if (!this.isVendor) {
            this.selectType('Vendor');
        }
    }

    handleInternalClick() {
        if (!this.isInternal) {
            this.selectType('Internal');
        }
    }

    selectType(newType) {
        this.dispatchEvent(new CustomEvent('contacttypechange', {
            detail: {
                contactType: newType,
                previousType: this.selectedType
            }
        }));
    }
}
```

**File:** `contactTypeSelector.html`

```html
<template>
    <template if:true={showTypeSelector}>
        <lightning-layout multiple-rows class="ridgedBorder">
            <lightning-layout-item size="3" padding="around-medium">
                <div class="slds-align_absolute-center">
                    <strong>Contact type:</strong><br/>
                </div>
            </lightning-layout-item>

            <lightning-layout-item size="3" padding="around-medium"
                                   class="slds-align_absolute-center">
                <lightning-button-stateful
                    label-when-off="Customer"
                    label-when-on="Customer"
                    label-when-hover="Customer"
                    variant="brand"
                    icon-name-when-off="utility:add"
                    icon-name-when-on="utility:check"
                    icon-name-when-hover="utility:close"
                    state={isCustomer}
                    onclick={handleCustomerClick}>
                </lightning-button-stateful>
            </lightning-layout-item>

            <lightning-layout-item size="3" padding="around-medium"
                                   class="slds-align_absolute-center">
                <lightning-button-stateful
                    label-when-off="Vendor"
                    label-when-on="Vendor"
                    label-when-hover="Vendor"
                    variant="brand"
                    icon-name-when-off="utility:add"
                    icon-name-when-on="utility:check"
                    icon-name-when-hover="utility:close"
                    state={isVendor}
                    onclick={handleVendorClick}>
                </lightning-button-stateful>
            </lightning-layout-item>

            <lightning-layout-item size="3" padding="around-medium"
                                   class="slds-align_absolute-center">
                <lightning-button-stateful
                    label-when-off="Internal"
                    label-when-on="Internal"
                    label-when-hover="Internal"
                    variant="brand"
                    icon-name-when-off="utility:add"
                    icon-name-when-on="utility:check"
                    icon-name-when-hover="utility:close"
                    state={isInternal}
                    onclick={handleInternalClick}>
                </lightning-button-stateful>
            </lightning-layout-item>
        </lightning-layout>
    </template>
</template>
```

### 3. Contact Search Form Component

**File:** `contactSearchForm.js`

```javascript
import { LightningElement, api, track } from 'lwc';

export default class ContactSearchForm extends LightningElement {
    @api contactType;
    @api caseData;

    @track searchCriteria = {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        mobile: '',
        searchTerm: ''
    };

    // Debounce timer
    searchTimeout;

    get isCustomer() {
        return this.contactType === 'Customer';
    }

    get isVendor() {
        return this.contactType === 'Vendor';
    }

    get isInternal() {
        return this.contactType === 'Internal';
    }

    get searchLabel() {
        if (this.isCustomer) {
            return 'Search contacts by name, email, or phone';
        } else if (this.isVendor) {
            return 'Search vendor contacts';
        } else {
            return 'Search internal users';
        }
    }

    handleFieldChange(event) {
        const field = event.target.name;
        const value = event.target.value;

        this.searchCriteria[field] = value;

        // Debounce search
        this.debouncedSearch();
    }

    handleSearchKeyUp(event) {
        // Trigger search on Enter key
        if (event.keyCode === 13) {
            this.performSearch();
        } else {
            this.debouncedSearch();
        }
    }

    handleFocusOut() {
        // Trigger search on field blur
        this.performSearch();
    }

    debouncedSearch() {
        // Clear previous timeout
        clearTimeout(this.searchTimeout);

        // Set new timeout
        this.searchTimeout = setTimeout(() => {
            this.performSearch();
        }, 500); // 500ms debounce
    }

    performSearch() {
        // Validate search criteria
        if (!this.hasValidSearchCriteria()) {
            return;
        }

        // Dispatch search event
        this.dispatchEvent(new CustomEvent('search', {
            detail: {
                criteria: {...this.searchCriteria}
            }
        }));
    }

    hasValidSearchCriteria() {
        const { firstName, lastName, email, phone, mobile, searchTerm } = this.searchCriteria;

        // At least one field must have 2+ characters
        return (firstName && firstName.length > 1) ||
               (lastName && lastName.length > 1) ||
               (email && email.length > 1) ||
               (phone && phone.length > 1) ||
               (mobile && mobile.length > 1) ||
               (searchTerm && searchTerm.length > 1);
    }

    clearSearch() {
        this.searchCriteria = {
            firstName: '',
            lastName: '',
            email: '',
            phone: '',
            mobile: '',
            searchTerm: ''
        };
    }
}
```

**File:** `contactSearchForm.html`

```html
<template>
    <div class="slds-box slds-m-bottom_small">
        <p class="slds-m-bottom_small">{searchLabel}</p>

        <!-- Customer Search Form -->
        <template if:true={isCustomer}>
            <lightning-layout multiple-rows>
                <lightning-layout-item size="6" padding="around-small">
                    <lightning-input
                        name="firstName"
                        label="First Name"
                        value={searchCriteria.firstName}
                        onchange={handleFieldChange}
                        onkeyup={handleSearchKeyUp}>
                    </lightning-input>
                </lightning-layout-item>

                <lightning-layout-item size="6" padding="around-small">
                    <lightning-input
                        name="lastName"
                        label="Last Name"
                        value={searchCriteria.lastName}
                        onchange={handleFieldChange}
                        onkeyup={handleSearchKeyUp}>
                    </lightning-input>
                </lightning-layout-item>

                <lightning-layout-item size="4" padding="around-small">
                    <lightning-input
                        type="email"
                        name="email"
                        label="Email Address"
                        value={searchCriteria.email}
                        placeholder="address@example.com"
                        onchange={handleFieldChange}
                        onfocusout={handleFocusOut}>
                    </lightning-input>
                </lightning-layout-item>

                <lightning-layout-item size="4" padding="around-small">
                    <lightning-input
                        type="tel"
                        name="phone"
                        label="Phone Number"
                        value={searchCriteria.phone}
                        placeholder="Enter number with no spaces"
                        pattern="[0-9]{10}"
                        onchange={handleFieldChange}
                        onfocusout={handleFocusOut}>
                    </lightning-input>
                </lightning-layout-item>

                <lightning-layout-item size="4" padding="around-small">
                    <lightning-input
                        type="tel"
                        name="mobile"
                        label="Mobile Number"
                        value={searchCriteria.mobile}
                        placeholder="Enter number with no spaces"
                        pattern="[0-9]{10}"
                        onchange={handleFieldChange}
                        onfocusout={handleFocusOut}>
                    </lightning-input>
                </lightning-layout-item>
            </lightning-layout>
        </template>

        <!-- Vendor Search Form -->
        <template if:true={isVendor}>
            <lightning-input
                type="search"
                name="searchTerm"
                label="Search Vendor Contacts"
                value={searchCriteria.searchTerm}
                placeholder="Search all vendor contacts..."
                onchange={handleFieldChange}
                onkeyup={handleSearchKeyUp}>
            </lightning-input>
        </template>

        <!-- Internal User Search Form -->
        <template if:true={isInternal}>
            <lightning-input
                type="search"
                name="searchTerm"
                label="Search Internal Users"
                value={searchCriteria.searchTerm}
                placeholder="Search all users..."
                onchange={handleFieldChange}
                onkeyup={handleSearchKeyUp}>
            </lightning-input>
        </template>
    </div>
</template>
```

### 4. Contact Search Results Component

**File:** `contactSearchResults.js`

```javascript
import { LightningElement, api } from 'lwc';

export default class ContactSearchResults extends LightningElement {
    @api contacts = [];
    @api selectedContactId;
    @api showNewButton = false;

    // Column definitions matching Aura
    columns = [
        { label: 'Name', fieldName: 'name', type: 'text', cellAttributes: { class: { fieldName: 'rowClass' } } },
        { label: 'Title', fieldName: 'title', type: 'text' },
        { label: 'Phone', fieldName: 'phone', type: 'phone' },
        { label: 'Email', fieldName: 'email', type: 'email' },
        { label: 'BR Association', fieldName: 'businessRuleAssociation', type: 'text' },
        { label: 'Last Activity', fieldName: 'lastActivityDate', type: 'date' }
    ];

    get hasContacts() {
        return this.contacts && this.contacts.length > 0;
    }

    get selectedRows() {
        return this.selectedContactId ? [this.selectedContactId] : [];
    }

    handleRowSelection(event) {
        const selectedRows = event.detail.selectedRows;

        if (selectedRows && selectedRows.length > 0) {
            const selectedContact = selectedRows[0];

            this.dispatchEvent(new CustomEvent('contactselect', {
                detail: {
                    contactId: selectedContact.contactId,
                    contact: selectedContact
                }
            }));
        }
    }

    handleNewContact() {
        this.dispatchEvent(new CustomEvent('newcontact'));
    }
}
```

**File:** `contactSearchResults.html`

```html
<template>
    <div class="slds-box slds-m-top_small">
        <template if:true={hasContacts}>
            <lightning-datatable
                key-field="contactId"
                data={contacts}
                columns={columns}
                max-row-selection="1"
                selected-rows={selectedRows}
                onrowselection={handleRowSelection}
                resize-column-disabled>
            </lightning-datatable>

            <template if:true={showNewButton}>
                <div class="slds-m-top_small">
                    <lightning-button
                        variant="brand"
                        label="New"
                        title="New Contact"
                        icon-name="utility:new"
                        onclick={handleNewContact}>
                    </lightning-button>
                </div>
            </template>
        </template>

        <template if:false={hasContacts}>
            <div class="slds-text-align_center slds-p-vertical_large">
                <p class="slds-text-color_weak">
                    No contacts found. Try adjusting your search criteria.
                </p>
                <lightning-button
                    variant="brand"
                    label="Create New Contact"
                    icon-name="utility:new"
                    onclick={handleNewContact}
                    class="slds-m-top_small">
                </lightning-button>
            </div>
        </template>
    </div>
</template>
```

---

## State Management

### State Object Structure

```javascript
// Main component state
state = {
    // Contact type selection
    contactType: 'Customer', // 'Customer' | 'Vendor' | 'Internal'

    // UI state
    isModalOpen: true,
    isMinimized: false,
    showNewContactForm: false,
    showDuplicateModal: false,
    isLoading: false,

    // Search state
    searchCriteria: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        mobile: '',
        searchTerm: ''
    },
    searchResults: [],
    selectedContactId: null,

    // Form state
    newContact: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        extension: '',
        preferredMethod: '',
        accountTitleId: '',
        department: ''
    },
    duplicateContacts: [],

    // Case context
    caseData: {
        id: null,
        accountId: null,
        locationId: null,
        vendorId: null,
        contactId: null,
        caseType: null,
        caseSubType: null,
        status: null
    },
    existingContact: null,

    // Configuration
    accountTitles: [],
    accountDepts: [],
    vendorRoles: []
};
```

### State Update Patterns

```javascript
// Reactive updates using @track
this.state.isLoading = true; // Triggers re-render

// Nested property updates
this.state = {
    ...this.state,
    searchCriteria: {
        ...this.state.searchCriteria,
        firstName: 'John'
    }
};

// Array updates
this.state.searchResults = [...newResults];

// Object updates with spread
this.state.newContact = {
    ...this.state.newContact,
    email: 'new@email.com'
};
```

---

## Event Handling

### Custom Events

#### 1. contacttypechange
```javascript
// Dispatched by: contactTypeSelector
// Consumed by: searchExistingContact

this.dispatchEvent(new CustomEvent('contacttypechange', {
    detail: {
        contactType: 'Customer',
        previousType: 'Vendor'
    }
}));
```

#### 2. search
```javascript
// Dispatched by: contactSearchForm
// Consumed by: searchExistingContact

this.dispatchEvent(new CustomEvent('search', {
    detail: {
        criteria: {
            firstName: 'John',
            lastName: 'Smith',
            email: 'john@example.com'
        }
    }
}));
```

#### 3. contactselect
```javascript
// Dispatched by: contactSearchResults
// Consumed by: searchExistingContact

this.dispatchEvent(new CustomEvent('contactselect', {
    detail: {
        contactId: '003xxxxxxxxxxxxxxx',
        contact: {...}
    }
}));
```

#### 4. newcontact
```javascript
// Dispatched by: contactSearchResults, contactSearchForm
// Consumed by: searchExistingContact

this.dispatchEvent(new CustomEvent('newcontact'));
```

#### 5. save
```javascript
// Dispatched by: contactCreationForm
// Consumed by: searchExistingContact

this.dispatchEvent(new CustomEvent('save', {
    detail: {
        contactData: {
            firstName: 'Jane',
            lastName: 'Doe',
            email: 'jane@example.com',
            // ... more fields
        }
    }
}));
```

#### 6. associate
```javascript
// Dispatched by: contactDetailsPanel
// Consumed by: searchExistingContact

this.dispatchEvent(new CustomEvent('associate', {
    detail: {
        contactId: '003xxxxxxxxxxxxxxx'
    }
}));
```

### Event Flow Diagram

```
┌──────────────────────────────────────────────────────┐
│          searchExistingContact (Parent)              │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │     contactTypeSelector                     │   │
│  │                                             │   │
│  │  ───[contacttypechange]──>                 │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │     contactSearchForm                       │   │
│  │                                             │   │
│  │  ───[search]──>                            │   │
│  │  ───[newcontact]──>                        │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │     contactSearchResults                    │   │
│  │                                             │   │
│  │  ───[contactselect]──>                     │   │
│  │  ───[newcontact]──>                        │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │     contactCreationForm                     │   │
│  │                                             │   │
│  │  ───[save]──>                              │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## API Integration

### Apex Method Mapping

| Aura Method | LWC Import | Usage |
|-------------|------------|-------|
| `c.returnCase` | `getCaseContext` | Load case data on init |
| `c.searchContacts` | `searchContacts` | Multi-field contact search |
| `c.searchLocCont` | `searchContacts` | Location-based search |
| `c.createNewContact` | `createContactForCase` | Create customer contact |
| `c.createNewVenContact` | `createContactForCase` | Create vendor contact |
| `c.existingContact` | `associateContactToCase` | Associate contact to case |
| `c.checkDuplicateContacts` | `createContactForCase` | Duplicate detection |
| `c.getAccountTitles` | `getAccountTitles` | Load title picklist |
| `c.getAccountDepts` | `getAccountDepts` | Load dept picklist |
| `c.getVendorRoles` | `getVendorRoles` | Load vendor roles |
| `c.getAccountTeam` | `searchContacts` | Load account team |
| `c.getUsers` | `searchContacts` | Internal user search |
| `c.internalContact` | `internalContact` | Get internal contact |
| `c.saveUserToCase` | `saveUserToCase` | Associate user to case |

### Wire Services

```javascript
// Use wire for cacheable data
@wire(getAccountTitles, { accountId: '$caseData.accountId' })
wiredTitles({ error, data }) {
    if (data) {
        this.state.accountTitles = data;
    } else if (error) {
        this.handleError(error);
    }
}

// Use imperative for non-cacheable operations
async performSearch() {
    try {
        const result = await searchContacts({
            criteria: JSON.stringify(this.searchCriteria),
            caseId: this.recordId
        });
        this.state.searchResults = result.contacts;
    } catch (error) {
        this.handleError(error);
    }
}
```

---

## Migration Mapping

### Complete Attribute Mapping

| Aura Attribute | LWC Property | Type | Notes |
|----------------|--------------|------|-------|
| `boolCustomer` | `state.contactType === 'Customer'` | Computed | Consolidate 3 bools into single enum |
| `boolVendor` | `state.contactType === 'Vendor'` | Computed | |
| `boolInternal` | `state.contactType === 'Internal'` | Computed | |
| `boolNewContact` | `state.showNewContactForm` | Boolean | Renamed for clarity |
| `boolSOSL` | (removed) | - | No longer needed with new architecture |
| `showSearch` | `state.hasSearchResults` | Computed | |
| `boolShowNew` | `showNewButton` | Computed | |
| `boolEdit` | `state.caseData.isEditMode` | Boolean | |
| `boolShowUser` | `state.contactType === 'Internal'` | Computed | |
| `boolReadOnly` | `contact.isReadOnly` | Boolean | |
| `caseAccount` | `state.caseData.accountId` | Id | |
| `locAccount` | `state.caseData.locationId` | Id | |
| `caseContact` | `state.caseData.contactId` | Id | |
| `caseUser` | `state.caseData.userId` | Id | |
| `caseStatus` | `state.caseData.status` | String | |
| `recordId` | `recordId` | @api Id | |
| `vendorAcc` | `state.caseData.vendorId` | Id | |
| `vendorAccount` | `state.selectedVendorId` | Id | |
| `vendorName` | `state.selectedVendorName` | String | |
| `searchString` | `state.searchCriteria.searchTerm` | String | |
| `userString` | `state.searchCriteria.searchTerm` | String | |
| `soslRows` | `selectedRows` | Computed | |
| `soslContacts` | `state.searchResults` | Array | |
| `dupContacts` | `state.duplicateContacts` | Array | |
| `vendorAccts` | `state.vendorAccounts` | Array | |
| `soslFields` | `columns` | Array | |
| `dupFields` | `duplicateColumns` | Array | |
| `vendorFields` | `vendorColumns` | Array | |
| `accountTitles` | `state.accountTitles` | Array | |
| `selTitle` | `state.newContact.accountTitleId` | Id | |
| `accountDepts` | `state.accountDepts` | Array | |
| `selDept` | `state.newContact.department` | String | |
| `vendorRoles` | `state.vendorRoles` | Array | |
| `selVendorRoles` | `state.newContact.vendorRoles` | Array | |
| `searchPlaceholder` | (hardcoded) | String | |
| `searchLabel` | `searchLabel` | Computed | |
| `searchFirstName` | `state.searchCriteria.firstName` | String | |
| `searchLastName` | `state.searchCriteria.lastName` | String | |
| `searchEmail` | `state.searchCriteria.email` | String | |
| `searchPhone` | `state.searchCriteria.phone` | String | |
| `searchMobile` | `state.searchCriteria.mobile` | String | |
| `contactId` | `state.selectedContactId` | Id | |
| `userId` | `state.selectedUserId` | Id | |
| `firstName` | `state.newContact.firstName` | String | |
| `lastName` | `state.newContact.lastName` | String | |
| `phone` | `state.newContact.phone` | String | |
| `email` | `state.newContact.email` | String | |
| `title` | `state.newContact.accountTitleId` | Id | |
| `preferred` | `state.newContact.preferredMethod` | String | |
| `conType` | `state.contactType` | String | |
| `extension` | `state.newContact.extension` | String | |
| `displayContFields` | `contactFields` | Array | |
| `displayUserFields` | `userFields` | Array | |
| `showForm` | `state.isModalOpen` | Boolean | |
| `showPriorSearchResult` | (removed) | - | No longer needed |
| `isModalOpenContact` | `state.isModalOpen` | Boolean | |
| `isVendor` | `state.caseData.hasVendor` | Boolean | |
| `isClient` | `state.caseData.hasClient` | Boolean | |
| `isLocation` | `state.caseData.hasLocation` | Boolean | |
| `isOpen` | `state.showDuplicateModal` | Boolean | |

### Method Mapping

| Aura Method | LWC Method | Location |
|-------------|------------|----------|
| `init` | `connectedCallback()` | Main component |
| `handleCusClick` | `handleCustomerClick()` | contactTypeSelector |
| `handleVenClick` | `handleVendorClick()` | contactTypeSelector |
| `handleIntClick` | `handleInternalClick()` | contactTypeSelector |
| `searchAllContact` | `handleFieldChange()` + debounce | contactSearchForm |
| `searchAll` | `handleFieldChange()` + debounce | contactSearchForm |
| `selectContact` | `handleRowSelection()` | contactSearchResults |
| `newContact` | `handleNewContact()` | Main component |
| `saveNewContact` | `handleContactSave()` | Main component |
| `saveExistingContact` | `handleAssociateContact()` | Main component |
| `closeModel` | `handleModalClose()` | Main component |
| `minimizeModal` | `handleModalMinimize()` | Main component |
| `changeContact` | `handleChangeContact()` | Main component |

---

## Testing Strategy

### Jest Unit Tests

**Test Coverage Target:** 85%+

```javascript
// searchExistingContact.test.js
import { createElement } from 'lwc';
import SearchExistingContact from 'c/searchExistingContact';

// Mock Apex
import searchContacts from '@salesforce/apex/ContactSearchController.searchContacts';
jest.mock('@salesforce/apex/ContactSearchController.searchContacts', () => ({
    default: jest.fn()
}), { virtual: true });

describe('c-search-existing-contact', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('renders modal on component load', () => {
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        document.body.appendChild(element);

        const modal = element.shadowRoot.querySelector('.slds-modal');
        expect(modal).not.toBeNull();
    });

    it('initializes with customer contact type', () => {
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        element.recordId = '500xxxxxxxxxxxxxxx';
        document.body.appendChild(element);

        expect(element.state.contactType).toBe('Customer');
    });

    it('changes contact type when button clicked', () => {
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        document.body.appendChild(element);

        const typeSelector = element.shadowRoot.querySelector('c-contact-type-selector');
        typeSelector.dispatchEvent(new CustomEvent('contacttypechange', {
            detail: { contactType: 'Vendor' }
        }));

        return Promise.resolve().then(() => {
            expect(element.state.contactType).toBe('Vendor');
        });
    });

    it('performs search when criteria entered', async () => {
        const mockResults = {
            contacts: [
                { contactId: '003xxx1', name: 'John Smith' },
                { contactId: '003xxx2', name: 'Jane Doe' }
            ]
        };
        searchContacts.mockResolvedValue(mockResults);

        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        element.recordId = '500xxxxxxxxxxxxxxx';
        document.body.appendChild(element);

        const searchForm = element.shadowRoot.querySelector('c-contact-search-form');
        searchForm.dispatchEvent(new CustomEvent('search', {
            detail: {
                criteria: { firstName: 'John' }
            }
        }));

        await Promise.resolve();

        expect(searchContacts).toHaveBeenCalled();
        expect(element.state.searchResults.length).toBe(2);
    });

    it('displays search results', async () => {
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        element.recordId = '500xxxxxxxxxxxxxxx';
        document.body.appendChild(element);

        element.state.searchResults = [
            { contactId: '003xxx1', name: 'John Smith' }
        ];

        await Promise.resolve();

        const results = element.shadowRoot.querySelector('c-contact-search-results');
        expect(results).not.toBeNull();
        expect(results.contacts.length).toBe(1);
    });

    it('shows new contact form when new button clicked', () => {
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        document.body.appendChild(element);

        const results = element.shadowRoot.querySelector('c-contact-search-results');
        results.dispatchEvent(new CustomEvent('newcontact'));

        return Promise.resolve().then(() => {
            expect(element.state.showNewContactForm).toBe(true);
        });
    });

    it('closes modal when close button clicked', () => {
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        document.body.appendChild(element);

        const closeButton = element.shadowRoot.querySelector('lightning-button-icon[title="Close"]');
        closeButton.click();

        return Promise.resolve().then(() => {
            expect(element.state.isModalOpen).toBe(false);
        });
    });

    it('handles error when search fails', async () => {
        searchContacts.mockRejectedValue(new Error('Search failed'));

        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        element.recordId = '500xxxxxxxxxxxxxxx';
        document.body.appendChild(element);

        const searchForm = element.shadowRoot.querySelector('c-contact-search-form');
        searchForm.dispatchEvent(new CustomEvent('search', {
            detail: {
                criteria: { firstName: 'John' }
            }
        }));

        await Promise.resolve();

        expect(element.state.isLoading).toBe(false);
        // Toast event should be dispatched
    });
});
```

### Integration Tests

```javascript
// Integration test with multiple components
describe('Contact Search Integration', () => {
    it('completes full search and selection workflow', async () => {
        // 1. Create component
        const element = createElement('c-search-existing-contact', {
            is: SearchExistingContact
        });
        element.recordId = '500xxxxxxxxxxxxxxx';
        document.body.appendChild(element);

        // 2. Change contact type
        const typeSelector = element.shadowRoot.querySelector('c-contact-type-selector');
        typeSelector.dispatchEvent(new CustomEvent('contacttypechange', {
            detail: { contactType: 'Customer' }
        }));

        await Promise.resolve();

        // 3. Enter search criteria
        const searchForm = element.shadowRoot.querySelector('c-contact-search-form');
        searchForm.dispatchEvent(new CustomEvent('search', {
            detail: {
                criteria: { firstName: 'John', lastName: 'Smith' }
            }
        }));

        await Promise.resolve();

        // 4. Select contact from results
        const results = element.shadowRoot.querySelector('c-contact-search-results');
        results.dispatchEvent(new CustomEvent('contactselect', {
            detail: { contactId: '003xxxxxxxxxxxxxxx' }
        }));

        await Promise.resolve();

        // 5. Verify contact selected
        expect(element.state.selectedContactId).toBe('003xxxxxxxxxxxxxxx');
    });
});
```

---

## Deployment Plan

### Pre-Deployment Checklist

- [ ] All Jest tests passing (85%+ coverage)
- [ ] Code review completed
- [ ] Accessibility audit completed
- [ ] Performance tests meeting targets
- [ ] Lightning Locker compliance verified
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Deployment runbook validated

### Deployment Steps

#### Step 1: Deploy LWC Components (Parallel Deployment)

```bash
# Deploy LWC components WITHOUT updating Aura component reference
sfdx force:source:deploy -p force-app/main/default/lwc/searchExistingContact
sfdx force:source:deploy -p force-app/main/default/lwc/contactTypeSelector
sfdx force:source:deploy -p force-app/main/default/lwc/contactSearchForm
sfdx force:source:deploy -p force-app/main/default/lwc/contactSearchResults
sfdx force:source:deploy -p force-app/main/default/lwc/contactCreationForm
sfdx force:source:deploy -p force-app/main/default/lwc/contactDetailsPanel
```

#### Step 2: Smoke Testing in Production

- Test LWC components in sandbox-like environment
- Verify no conflicts with existing Aura component
- Validate API integration

#### Step 3: Update Lightning Pages

```bash
# Deploy updated Lightning page layouts
# Replace Aura component with LWC component
sfdx force:source:deploy -p force-app/main/default/flexipages
```

#### Step 4: Monitor

- Watch error logs for 48 hours
- Monitor performance metrics
- Collect user feedback

#### Step 5: Cleanup (After 30 days)

```bash
# Remove old Aura component
sfdx force:source:delete -p force-app/main/default/aura/SearchExistingContact
```

### Deployment Timeline

| Day | Activity | Duration |
|-----|----------|----------|
| Day 1 | Deploy LWC components | 2 hours |
| Day 1-2 | Smoke testing | 2 days |
| Day 3 | Update Lightning pages | 2 hours |
| Day 3-5 | Monitor and address issues | 3 days |
| Day 30 | Remove Aura component | 1 hour |

---

## Rollback Strategy

### Rollback Triggers

- Critical functional regression
- Performance significantly worse than Aura
- >5% error rate
- Data integrity issues

### Rollback Steps

#### Immediate Rollback (0-15 minutes)

1. **Revert Lightning Page Layouts**
   ```bash
   # Deploy previous version from git
   git checkout HEAD~1 -- force-app/main/default/flexipages
   sfdx force:source:deploy -p force-app/main/default/flexipages
   ```

2. **Verify Aura Component Active**
   - Check Lightning pages in UI
   - Verify functionality restored

#### Full Rollback (if needed)

1. Remove LWC components
2. Restore Aura component from backup
3. Clear browser caches
4. Communicate to users

### Rollback Testing

- Test rollback procedure in sandbox
- Document rollback time: <30 minutes
- Assign rollback team roles

---

## Dependencies

### Platform Dependencies

1. **Salesforce Version:** Winter '25 or later (API v59.0+)
2. **LWC Framework:** Enabled (default for all orgs)
3. **Lightning Experience:** Required
4. **Refactored Apex Controller:** CSC-APEX-2026-001 must be deployed first

### Component Dependencies

1. **Lightning Base Components:**
   - lightning-button
   - lightning-button-icon
   - lightning-button-stateful
   - lightning-datatable
   - lightning-input
   - lightning-layout
   - lightning-record-form
   - lightning-spinner

2. **Custom Events:**
   - Migrated from Aura events to LWC custom events

3. **Workspace API:**
   - Page refresh functionality
   - Tab management

### Permission Dependencies

- Same as current Aura component
- No additional permissions required

---

## Appendices

### Appendix A: Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | Latest 2 | Full |
| Firefox | Latest 2 | Full |
| Safari | Latest 2 | Full |
| Edge | Latest 2 | Full |
| IE 11 | N/A | Not Supported (LWC requirement) |

### Appendix B: Performance Benchmarks

**Target Performance:**
```
Initial Load: <2,500ms (current: 3,000-4,000ms)
Time to Interactive: <3,000ms (current: 4,000-5,000ms)
Re-render: <300ms (current: 500-800ms)
Bundle Size: <150kb
```

### Appendix C: Functional Parity Checklist

- [ ] Contact type selection (Customer, Vendor, Internal)
- [ ] Multi-field customer contact search
- [ ] Single-field vendor search
- [ ] User search for internal contacts
- [ ] Location-based contact filtering
- [ ] Vendor account selection
- [ ] Contact selection from results
- [ ] New contact creation forms
- [ ] Account title selection
- [ ] Account department selection
- [ ] "Add New Title" functionality
- [ ] Duplicate contact detection
- [ ] Duplicate contact modal
- [ ] Contact-to-case association
- [ ] Account relationship creation
- [ ] Account title validation
- [ ] Contact display (read-only)
- [ ] User display (for internal contacts)
- [ ] "Change Contact" functionality
- [ ] Modal minimize/maximize
- [ ] Modal close
- [ ] Toast messages (success/error)
- [ ] Tab refresh after save
- [ ] Business rule association highlighting
- [ ] Conditional field display
- [ ] Form validation
- [ ] Error handling

### Appendix D: Component Size Comparison

| Metric | Aura | LWC | Change |
|--------|------|-----|--------|
| Main Component Lines | 685 | ~400 | -42% |
| JavaScript Lines | 770 | ~600 | -22% |
| Total Components | 1 | 4 | +300% |
| Avg Component Size | 685 | ~150 | -78% |
| Bundle Size | N/A | <150kb | New |

### Appendix E: Code Review Checklist

- [ ] Follows LWC best practices
- [ ] Lightning Locker compliant
- [ ] Proper use of @api, @track, @wire
- [ ] Event naming conventions followed
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] Accessibility (ARIA) attributes
- [ ] Performance optimizations applied
- [ ] Security considerations addressed
- [ ] Jest tests written (85%+ coverage)
- [ ] No console.log in production code
- [ ] Comments for complex logic
- [ ] Proper indentation and formatting

---

**Document Status:** Ready for Review
**Next Steps:**
1. Technical Lead review and approval
2. Begin LWC component development
3. Jest test development in parallel
4. Integration testing in sandbox

**Review Comments:**
_[Space for reviewer comments]_

---

**End of Technical Design Document**
