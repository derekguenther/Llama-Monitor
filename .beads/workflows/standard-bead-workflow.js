/**
 * Standard Bead Workflow Template
 *
 * This workflow follows the beads issue tracker process:
 * 1. Validate beads exist
 * 2. Claim work and set status:in-worktree label
 * 3. Implement fixes in parallel worktrees
 * 4. Set status:needs-review label
 * 5. Review agent evaluates and merges
 * 6. Close beads after merge
 *
 * Usage: Copy this file, customize the beads array and implementation prompts.
 */

export const meta = {
  name: 'standard-bead-workflow',
  description: 'Work on multiple beads following proper beads workflow process',
  phases: [
    { title: 'Validate', detail: 'Verify all beads exist in tracker' },
    { title: 'Claim', detail: 'Claim work and set in-worktree label' },
    { title: 'Implement', detail: 'Implement fixes in parallel worktrees' },
    { title: 'Review', detail: 'Evaluate and merge each bead' },
  ],
};

// List of bead IDs to work on - must exist in .beads/issues.jsonl
const BEADS_TO_WORK = [
  // Add bead IDs here after creating them
  // Example: 'llama-monitor-abc', 'llama-monitor-xyz'
];

// Implementation configuration for each bead
const BEAD_IMPLEMENTATION = {
  // Example structure - customize for your beads
  // 'llama-monitor-abc': {
  //   prompt: 'Fix the Active Slots 0/0 display issue...',
  //   filesToModify: ['web_server.py', 'templates/index.html'],
  // },
};

/**
 * Main workflow - works on beads in parallel with worktree isolation
 */
export async function main(args, workflow) {
  const { agent, parallel, pipeline, phase, log } = workflow;

  // Phase 1: Validate beads exist
  phase('Validate');
  log(`Validating ${BEADS_TO_WORK.length} beads exist in tracker...`);

  const beadsExist = await agent(
    `Verify all beads in ${JSON.stringify(BEADS_TO_WORK)} exist in .beads/issues.jsonl.
     Report any missing beads that need to be created first.`,
    { phase: 'Validate' }
  );

  // Phase 2: Claim work
  phase('Claim');
  log(`Claiming work for ${BEADS_TO_WORK.length} beads...`);

  await parallel(BEADS_TO_WORK.map(beadId => () =>
    agent(
      `Claim the bead ${beadId} by:
       1. Running: bd update ${beadId} --claim
       2. Running: bd update ${beadId} --add-label status:in-worktree
       3. Creating a worktree: git worktree add .worktrees/${beadId} -b ${beadId}
       4. Confirming the worktree was created successfully`,
      { label: `claim:${beadId}`, phase: 'Claim' }
    )
  ));

  // Phase 3: Implement fixes
  phase('Implement');
  log(`Implementing fixes for ${BEADS_TO_WORK.length} beads...`);

  const implementations = await parallel(BEADS_TO_WORK.map(beadId => () => {
    const config = BEAD_IMPLEMENTATION[beadId];
    const prompt = config?.prompt || `Fix the issue described in bead ${beadId}.`;

    return agent(
      `Work on bead ${beadId} in the worktree at .worktrees/${beadId}:

      ${prompt}

      Instructions:
      1. Navigate to .worktrees/${beadId}
      2. Make the necessary code changes
      3. Create tests to verify the fix
      4. Run tests to confirm they pass
      5. Commit changes with descriptive message
      6. Set review label: bd update ${beadId} --add-label status:needs-review`,
      { label: `impl:${beadId}`, phase: 'Implement', isolation: 'worktree' }
    );
  }));

  // Phase 4: Review and merge
  phase('Review');
  log(`Reviewing ${BEADS_TO_WORK.length} implementations...`);

  const reviews = await parallel(BEADS_TO_WORK.map(beadId => () =>
    agent(
      `Review the implementation for bead ${beadId}:

      - Check that the fix is correct
      - Verify tests pass (run: python3 -m pytest)
      - If approved: merge the branch and push to remote
      - Then: bd update ${beadId} --remove-label status:needs-review --add-label status:ready-to-merge
      - Finally: bd close ${beadId} --reason "Merged to main"

      If issues are found, request changes.`,
      { label: `review:${beadId}`, phase: 'Review' }
    )
  ));

  // Summary
  log('Workflow complete!');
  return {
    beadsValidated: beadsExist,
    implementations,
    reviews,
  };
}
