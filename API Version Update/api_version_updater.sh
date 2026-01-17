#!/bin/bash
################################################################################
# API Version Updater Script
#
# Purpose: Automates bulk updating of Salesforce metadata API versions
# Author: George Martin, Salesforce Technical Architect
# Date: January 17, 2026
# Version: 1.0
#
# Usage: ./api_version_updater.sh [phase] [target-api-version]
# Example: ./api_version_updater.sh phase1 63.0
################################################################################

set -e  # Exit on error

# Configuration
TARGET_API_VERSION="${2:-65.0}"
PHASE="${1:-all}"
BACKUP_DIR="api_upgrade_backup_$(date +%Y%m%d_%H%M%S)"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
METADATA_DIR="$REPO_ROOT/force-app/main/default"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_UPDATED=0
ERRORS=0

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          Salesforce API Version Updater v1.0              ║${NC}"
    echo -e "${BLUE}║              by George Martin                              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

create_backup() {
    print_info "Creating backup of metadata..."
    mkdir -p "$BACKUP_DIR"

    if cp -r "$METADATA_DIR" "$BACKUP_DIR/"; then
        print_success "Backup created: $BACKUP_DIR"
    else
        print_error "Failed to create backup!"
        exit 1
    fi
}

update_api_version() {
    local file_pattern=$1
    local old_version=$2
    local metadata_type=$3
    local search_dir=$4

    print_info "Updating $metadata_type from API $old_version to $TARGET_API_VERSION..."

    local count=0
    local files=$(find "$search_dir" -name "$file_pattern" -exec grep -l "<apiVersion>$old_version</apiVersion>" {} \; 2>/dev/null)

    if [ -z "$files" ]; then
        print_warning "No files found with API $old_version for $metadata_type"
        return 0
    fi

    while IFS= read -r file; do
        if [ -f "$file" ]; then
            # Create temporary file
            local temp_file="${file}.tmp"

            # Perform replacement
            if sed "s/<apiVersion>$old_version<\/apiVersion>/<apiVersion>$TARGET_API_VERSION<\/apiVersion>/g" "$file" > "$temp_file"; then
                mv "$temp_file" "$file"
                echo "  ✓ Updated: $(basename $file)"
                ((count++))
                ((TOTAL_UPDATED++))
            else
                print_error "Failed to update: $file"
                ((ERRORS++))
                rm -f "$temp_file"
            fi
        fi
    done <<< "$files"

    if [ $count -gt 0 ]; then
        print_success "Updated $count $metadata_type files"
    fi
}

phase1_critical() {
    print_header
    print_info "PHASE 1: Critical Priority (API 38.0)"
    print_info "Target API Version: $TARGET_API_VERSION"
    echo ""

    # Apex Classes using API 38.0
    update_api_version "*.cls-meta.xml" "38.0" "Apex Classes (API 38.0)" "$METADATA_DIR/classes"

    # Apex Triggers using API 38.0
    update_api_version "*.trigger-meta.xml" "38.0" "Apex Triggers (API 38.0)" "$METADATA_DIR/triggers"
}

phase2_high_volume() {
    print_header
    print_info "PHASE 2: High Volume (API 45.0 - 46.0)"
    print_info "Target API Version: $TARGET_API_VERSION"
    echo ""

    # Apex Classes using API 45.0
    update_api_version "*.cls-meta.xml" "45.0" "Apex Classes (API 45.0)" "$METADATA_DIR/classes"

    # Apex Classes using API 46.0
    update_api_version "*.cls-meta.xml" "46.0" "Apex Classes (API 46.0)" "$METADATA_DIR/classes"

    # Apex Triggers using API 45.0
    update_api_version "*.trigger-meta.xml" "45.0" "Apex Triggers (API 45.0)" "$METADATA_DIR/triggers"

    # Apex Triggers using API 46.0
    update_api_version "*.trigger-meta.xml" "46.0" "Apex Triggers (API 46.0)" "$METADATA_DIR/triggers"

    # Aura Components using API 45.0
    update_api_version "*.cmp-meta.xml" "45.0" "Aura Components (API 45.0)" "$METADATA_DIR/aura"
    update_api_version "*.app-meta.xml" "45.0" "Aura Apps (API 45.0)" "$METADATA_DIR/aura"
    update_api_version "*.evt-meta.xml" "45.0" "Aura Events (API 45.0)" "$METADATA_DIR/aura"

    # Aura Components using API 46.0
    update_api_version "*.cmp-meta.xml" "46.0" "Aura Components (API 46.0)" "$METADATA_DIR/aura"

    # Visualforce Pages using API 45.0
    update_api_version "*.page-meta.xml" "45.0" "Visualforce Pages (API 45.0)" "$METADATA_DIR/pages"
}

phase3_medium() {
    print_header
    print_info "PHASE 3: Medium Priority (API 47.0 - 52.0)"
    print_info "Target API Version: $TARGET_API_VERSION"
    echo ""

    for version in 47.0 48.0 49.0 50.0 51.0 52.0; do
        update_api_version "*.cls-meta.xml" "$version" "Apex Classes (API $version)" "$METADATA_DIR/classes"
        update_api_version "*.trigger-meta.xml" "$version" "Apex Triggers (API $version)" "$METADATA_DIR/triggers"
        update_api_version "*.cmp-meta.xml" "$version" "Aura Components (API $version)" "$METADATA_DIR/aura"
        update_api_version "*-meta.xml" "$version" "LWC Components (API $version)" "$METADATA_DIR/lwc"
        update_api_version "*.page-meta.xml" "$version" "Visualforce Pages (API $version)" "$METADATA_DIR/pages"
        update_api_version "*.component-meta.xml" "$version" "VF Components (API $version)" "$METADATA_DIR/components"
    done
}

phase4_low() {
    print_header
    print_info "PHASE 4: Low Priority (API 53.0 - 59.0)"
    print_info "Target API Version: $TARGET_API_VERSION"
    echo ""

    for version in 53.0 54.0 55.0 56.0 57.0 58.0 59.0; do
        update_api_version "*.cls-meta.xml" "$version" "Apex Classes (API $version)" "$METADATA_DIR/classes"
        update_api_version "*.trigger-meta.xml" "$version" "Apex Triggers (API $version)" "$METADATA_DIR/triggers"
        update_api_version "*.cmp-meta.xml" "$version" "Aura Components (API $version)" "$METADATA_DIR/aura"
        update_api_version "*-meta.xml" "$version" "LWC Components (API $version)" "$METADATA_DIR/lwc"
        update_api_version "*.page-meta.xml" "$version" "Visualforce Pages (API $version)" "$METADATA_DIR/pages"
        update_api_version "*.component-meta.xml" "$version" "VF Components (API $version)" "$METADATA_DIR/components"
        update_api_version "*.flow-meta.xml" "$version" "Flows (API $version)" "$METADATA_DIR/flows"
    done
}

phase5_final() {
    print_header
    print_info "PHASE 5: Final Updates (API 60.0 - 64.0)"
    print_info "Target API Version: $TARGET_API_VERSION"
    echo ""

    for version in 60.0 61.0 62.0 63.0 64.0; do
        update_api_version "*.cls-meta.xml" "$version" "Apex Classes (API $version)" "$METADATA_DIR/classes"
        update_api_version "*.trigger-meta.xml" "$version" "Apex Triggers (API $version)" "$METADATA_DIR/triggers"
        update_api_version "*.cmp-meta.xml" "$version" "Aura Components (API $version)" "$METADATA_DIR/aura"
        update_api_version "*-meta.xml" "$version" "LWC Components (API $version)" "$METADATA_DIR/lwc"
        update_api_version "*.page-meta.xml" "$version" "Visualforce Pages (API $version)" "$METADATA_DIR/pages"
        update_api_version "*.component-meta.xml" "$version" "VF Components (API $version)" "$METADATA_DIR/components"
        update_api_version "*.flow-meta.xml" "$version" "Flows (API $version)" "$METADATA_DIR/flows"
    done
}

run_all_phases() {
    print_header
    print_info "Running ALL PHASES"
    print_info "Target API Version: $TARGET_API_VERSION"
    echo ""

    create_backup

    phase1_critical
    phase2_high_volume
    phase3_medium
    phase4_low
    phase5_final
}

print_summary() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                   UPDATE SUMMARY                           ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Target API Version:    ${GREEN}$TARGET_API_VERSION${NC}"
    echo -e "Total Files Updated:   ${GREEN}$TOTAL_UPDATED${NC}"
    echo -e "Errors:                ${RED}$ERRORS${NC}"
    echo -e "Backup Location:       ${BLUE}$BACKUP_DIR${NC}"
    echo ""

    if [ $ERRORS -eq 0 ]; then
        print_success "API version update completed successfully!"
    else
        print_warning "Update completed with $ERRORS errors. Please review."
    fi

    echo ""
    echo -e "${YELLOW}NEXT STEPS:${NC}"
    echo "1. Review changes: git diff"
    echo "2. Stage changes:  git add force-app/main/default"
    echo "3. Commit:         git commit -m 'Update API versions to $TARGET_API_VERSION'"
    echo "4. Deploy to sandbox:"
    echo "   sfdx project deploy start --target-org <sandbox-name>"
    echo "5. Run tests:"
    echo "   sfdx apex run test --target-org <sandbox-name> --code-coverage --wait 60"
    echo ""
}

################################################################################
# Main Script Execution
################################################################################

# Check if we're in the right directory
if [ ! -d "$METADATA_DIR" ]; then
    print_error "Metadata directory not found: $METADATA_DIR"
    print_error "Please run this script from the repository root or API Version Update folder"
    exit 1
fi

# Parse command line arguments
case "$PHASE" in
    phase1)
        create_backup
        phase1_critical
        ;;
    phase2)
        create_backup
        phase2_high_volume
        ;;
    phase3)
        create_backup
        phase3_medium
        ;;
    phase4)
        create_backup
        phase4_low
        ;;
    phase5)
        create_backup
        phase5_final
        ;;
    all)
        run_all_phases
        ;;
    *)
        print_error "Invalid phase: $PHASE"
        echo ""
        echo "Usage: $0 [phase] [target-api-version]"
        echo ""
        echo "Phases:"
        echo "  phase1  - Critical Priority (API 38.0)"
        echo "  phase2  - High Volume (API 45.0-46.0)"
        echo "  phase3  - Medium Priority (API 47.0-52.0)"
        echo "  phase4  - Low Priority (API 53.0-59.0)"
        echo "  phase5  - Final Updates (API 60.0-64.0)"
        echo "  all     - Run all phases (default)"
        echo ""
        echo "Example: $0 phase1 63.0"
        echo "Example: $0 all 65.0"
        exit 1
        ;;
esac

# Print summary
print_summary

# Exit with appropriate code
exit $ERRORS
