# Phase 5: Final Course Audit & Documentation

## Objective
Perform a full submission-quality audit against course requirements and grading rubric. This phase ensures the project is not only functional but also documented, tested, and packaged in a way that maximizes points and reduces last-minute risk before submission.

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/course_requirements.md`
- `.agent_docs/documentation_guidelines.md`
- `.agent_docs/testing_and_changes.md`
- `.agent_docs/python_standards.md`

## Implementation Scope
In scope:
- README quality pass, usage examples, and visuals checklist.
- Test suite depth check (minimum 5 meaningful tests; target beyond minimum).
- CI workflow verification and fixes if needed.
- Final AGENTS reflection reminder for student-authored section.

Out of scope:
- Large new features unrelated to rubric closure.
- Risky refactors that could destabilize already passing behavior.

## Tasks
1. README completion audit
   - Verify all required sections are complete and accurate:
     - what the tool does
     - installation
     - usage and examples
     - project structure
     - known limitations/future ideas
   - Ensure commands and outputs in README match actual application behavior.
   - Acceptance criteria: a new user can clone, install, and run features using only README.
2. Test suite and coverage confidence pass
   - Verify at least 5 meaningful tests exist across core logic and edge cases.
   - Add missing tests for highest-risk untested paths (invalid input, retries, rate limits, formatting).
   - Acceptance criteria: tests are deterministic and validate behavior, not just execution.
3. CI/CD verification and stabilization
   - Confirm `.github/workflows/test.yml` runs on push to `main` and pull requests.
   - Address flaky assumptions or environment mismatches.
   - Acceptance criteria: pipeline passes without manual intervention.
4. Repository readiness and change hygiene
   - Verify `.gitignore` and secret handling are intact.
   - Ensure commit history reflects logical incremental work.
   - Acceptance criteria: no sensitive files committed; repo is cleanly reviewable.
5. Final reflection handoff
   - Confirm `AGENTS.md` contains a protected student reflection section.
   - Do not modify the reflection content on behalf of the student.
   - Acceptance criteria: student has clear prompt to complete final reflection before submission.

## Testing Requirements
- Run `pytest -v` locally as final gate.
- Re-run tests after any audit fixes.
- Confirm CI behavior matches local command and dependency setup.

## Documentation Requirements
- Finalize README examples and screenshot references.
- Ensure limitations and future ideas are explicit and honest.
- Ensure all documented commands are currently valid.

## AI Agent Audit Checklist
Before marking this phase as complete, an AI agent must verify the following:
- [ ] Code changes align with `.agent_docs/` guidelines.
- [ ] Tests have been written/updated and pass locally.
- [ ] The `README.md` has been updated to reflect any new features, flags, or usage commands.
- [ ] No secrets or sensitive information have been hardcoded.
- [ ] The commit history reflects logical, incremental steps.
- [ ] The CI/CD pipeline on the `main` branch is passing.

## Exit Criteria
- README is submission-ready and consistent with real behavior.
- Test suite is meaningful and meets/exceeds course minimum requirement.
- CI workflow is green and reproducible.
- Repository contains no exposed secrets and maintains clean project hygiene.
- Student reflection section in `AGENTS.md` is present and ready for final manual completion.

## Notes & AI Collaboration Learnings
*Document any challenges, course corrections, or AI collaboration notes here.*
