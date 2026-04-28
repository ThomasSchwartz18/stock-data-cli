# Final Project Course Requirements

## Minimum Requirements
Your project must meet all of the following requirements to receive full credit.

### 1. GitHub Repository
Your project must live in a public GitHub repository that you created for this project (not a fork of a course repo). The repo must show a meaningful commit history — commit early and often throughout development.

### 2. README
Your `README.md` must be thorough and written for someone who has never seen your project. At minimum it must include:
- **What it does** — a clear, one- to two-paragraph description of your tool and the problem it solves
- **Installation** — step-by-step instructions for installing dependencies and/or building the project
- **Usage** — how to run the program, with concrete command examples and expected output
- **Examples** — at least two or three realistic usage examples showing different features or flags
- **Known limitations or future ideas** (optional but encouraged)

### 3. Tests
Your project must include a meaningful test suite:
- **Python**: use `pytest` with at least five tests covering core logic
- Tests should cover real behavior — not just that the program runs, but that it produces correct output for known inputs. Edge cases and error handling are fair game.

### 4. CI/CD Pipeline
Your repository must include a GitHub Actions workflow (`.github/workflows/`) that automatically runs your test suite on every push to `main`. The workflow should:
- Install dependencies
- Run all tests
- Pass cleanly on your final submission

### 5. AGENTS.md
Include an `AGENTS.md` file in the root of your repository documenting how you used AI tools during development. This is not a formality — write honestly about where AI helped, where it steered you wrong, and what you learned from the collaboration.

---

## Grading Rubric
Your project is worth 35 points (20% of your course grade).

| Component | Points | What we’re looking for |
| :--- | :--- | :--- |
| **Functionality** | 10 | The program runs without errors, solves the stated problem, and handles bad input gracefully |
| **Code quality** | 8 | Code is readable, well-organized, and idiomatic for the chosen language |
| **Tests** | 7 | Test suite is meaningful, covers core logic and edge cases, and all tests pass |
| **README** | 5 | Clear, complete, and accurate — a stranger could install and use the tool from the README alone |
| **CI/CD pipeline** | 5 | Workflow runs and passes on every push; no manual steps required to verify tests |
| **Total** | **35** | |

*Note on Partial Credit*: Partial credit is available within each component. A project that is mostly complete but missing one piece (e.g., tests exist but CI is broken) will not lose full points for that category. Show your work and explain anything incomplete in your README.

---

## Key Dates & Submission
- **Final submission**: Sunday, May 3, 2026 at 11:59 PM
- Submit a link to your public GitHub repository via Canvas by the deadline.

### Submission Checklist
- [ ] Repository is public and accessible
- [ ] `README.md` covers installation, usage, and examples
- [ ] All tests pass locally
- [ ] GitHub Actions workflow passes on the main branch
- [ ] `AGENTS.md` is present and honest
- [ ] Commit history reflects ongoing work (not one giant commit at the end)