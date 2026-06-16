/**
 * Bead Workflow Validator Agent
 *
 * This agent validates that all bead IDs referenced in a workflow exist
 * in the beads tracker before allowing the workflow to proceed.
 *
 * Usage: Run this agent before starting any bead workflow.
 */

export const meta = {
  name: 'validate-bead-workflow',
  description: 'Validate that all beads exist before workflow execution',
};

export async function main(args, workflow) {
  const { agent, log, phase } = workflow;

  phase('Validate');
  log('Checking bead tracker for referenced beads...');

  const validation = await agent(
    `Validate that all bead IDs referenced in the workflow exist in the beads tracker.

    Instructions:
    1. Read .beads/issues.jsonl to get all existing beads
    2. Find all bead IDs referenced in the workflow script
    3. Report which beads exist and which are missing
    4. For missing beads, provide the bd create command to make them

    Return a summary of:
    - Total beads referenced
    - How many exist
    - How many are missing
    - Commands to create missing beads (if any)`,
    { schema: {
      type: 'object',
      properties: {
        totalBeads: { type: 'number' },
        existingBeads: { type: 'number' },
        missingBeads: { type: 'number' },
        beadDetails: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              id: { type: 'string' },
              exists: { type: 'boolean' },
              status: { type: 'string' },
              createCommand: { type: 'string' },
            },
          },
        },
      },
    }}
  );

  log(`Validation complete: ${validation.existingBeads} exist, ${validation.missingBeads} missing`);

  if (validation.missingBeads > 0) {
    log('WARNING: Some beads do not exist! Create them first:');
    validation.beadDetails
      .filter(b => !b.exists)
      .forEach(b => log(`  ${b.id}: ${b.CreateCommand}`));
  }

  return validation;
}
