/**
 * Workflow Validation Script for Beads Issue Tracker
 *
 * This script validates that all bead IDs referenced in a workflow exist
 * in the beads tracker before work begins.
 *
 * Usage: node .beads/workflow-validation.js <workflow-script-path>
 */

const fs = require('fs');
const path = require('path');

const BEADS_DIR = path.join(__dirname, '..');
const ISSUES_FILE = path.join(BEADS_DIR, 'issues.jsonl');

/**
 * Load all beads from the issues.jsonl file
 */
function loadBeads() {
    const beads = new Map();
    try {
        const content = fs.readFileSync(ISSUES_FILE, 'utf8');
        const lines = content.trim().split('\n').filter(line => line.trim());

        for (const line of lines) {
            try {
                const issue = JSON.parse(line);
                if (issue.id) {
                    beads.set(issue.id, issue);
                }
            } catch (e) {
                console.warn(`Warning: Could not parse line in issues.jsonl`);
            }
        }
    } catch (err) {
        console.error(`Error reading issues.jsonl: ${err.message}`);
    }

    return beads;
}

/**
 * Extract bead IDs from a workflow script
 * Looks for patterns like:
 * - bead: 'llama-monitor-xxx'
 * - beads: ['llama-monitor-xxx', ...]
 * - llama-monitor-xxx in strings
 */
function extractBeadIdsFromWorkflow(workflowContent) {
    const beadIds = new Set();

    // Pattern 1: bead: 'llama-monitor-xxx'
    const singleBeadPattern = /bead:\s*['"]([^'"]+)['"]/gi;
    let match;
    while ((match = singleBeadPattern.exec(workflowContent)) !== null) {
        beadIds.add(match[1]);
    }

    // Pattern 2: beads: ['llama-monitor-xxx', ...]
    const beadsArrayPattern = /beads:\s*\[([^\]]+)\]/gi;
    while ((match = beadsArrayPattern.exec(workflowContent)) !== null) {
        const arrayContent = match[1];
        const ids = arrayContent.match(/['"]([^'"]+)['"]/gi);
        if (ids) {
            ids.forEach(id => beadIds.add(id.replace(/['"]/g, '')));
        }
    }

    // Pattern 3: Direct references like llama-monitor-xxx (generic pattern)
    const genericPattern = /\b(llama-monitor-[a-z0-9]+)\b/gi;
    while ((match = genericPattern.exec(workflowContent)) !== null) {
        beadIds.add(match[1]);
    }

    return Array.from(beadIds);
}

/**
 * Validate workflow bead IDs against the beads tracker
 */
function validateWorkflowBeads(workflowPath) {
    console.log(`\n=== Beads Workflow Validation ===\n`);

    // Load beads from tracker
    const beads = loadBeads();
    console.log(`Found ${beads.size} beads in tracker\n`);

    // Read workflow script
    let workflowContent;
    try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
    } catch (err) {
        console.error(`Error reading workflow file: ${err.message}`);
        process.exit(1);
    }

    // Extract bead IDs from workflow
    const workflowBeadIds = extractBeadIdsFromWorkflow(workflowContent);
    console.log(`Found ${workflowBeadIds.length} bead references in workflow:\n`);
    workflowBeadIds.forEach(id => console.log(`  - ${id}`));

    // Validate each bead
    console.log('\n--- Validation Results ---\n');

    const missingBeads = [];
    const foundBeads = [];

    for (const beadId of workflowBeadIds) {
        const bead = beads.get(beadId);
        if (bead) {
            foundBeads.push({ id: beadId, status: bead.status, title: bead.title });
            console.log(`✓ ${beadId}`);
            console.log(`  Status: ${bead.status}`);
            console.log(`  Title: ${bead.title}\n`);
        } else {
            missingBeads.push(beadId);
            console.log(`✗ ${beadId} - NOT FOUND IN TRACKER`);
            console.log(`  This bead does not exist in .beads/issues.jsonl\n`);
        }
    }

    // Summary
    console.log('--- Summary ---\n');
    console.log(`Found: ${foundBeads.length} beads`);
    console.log(`Missing: ${missingBeads.length} beads\n`);

    if (missingBeads.length > 0) {
        console.log('⚠️  WARNING: Some bead IDs do not exist in the tracker!\n');
        console.log('Before running this workflow, create the missing beads:');
        missingBeads.forEach(id => {
            console.log(`  bd create --title="..." --description="..." --type=bug|task|feature --priority=2`);
        });
        return false;
    }

    console.log('✓ All bead IDs validated successfully!');
    return true;
}

// Main execution
const workflowPath = process.argv[2];

if (!workflowPath) {
    console.error('Usage: node .beads/workflow-validation.js <workflow-script-path>');
    console.error('\nExample:');
    console.error('  node .beads/workflow-validation.js workflows/fix-webpage-issues.js');
    process.exit(1);
}

const isValid = validateWorkflowBeads(workflowPath);
process.exit(isValid ? 0 : 1);
