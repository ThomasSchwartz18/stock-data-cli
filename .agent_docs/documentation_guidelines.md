# Documentation Guidelines

## Purpose
Ensure the `README.md` remains professional, accurate, and meets all course requirements as the project evolves. Documentation must be updated alongside code changes, not as an afterthought.

## README.md Required Structure
The `README.md` must follow this professional format:
1. **Title & Badges**: Project name and dynamic CI/CD GitHub Actions status badges.
2. **What it does**: A clear, 1-2 paragraph description of the tool and the problem it solves.
3. **Screenshots / GIFs**: Visual proof of the CLI and TUI in action. (Agents should use image placeholders like `!CLI Output` and instruct the user to capture the real screenshot).
4. **Installation**: Step-by-step instructions for cloning the repo, setting up a virtual environment, and installing dependencies.
5. **Usage & Examples**: Concrete command examples (`e.g., python src/cli/app.py quote AAPL`) alongside expected outputs or feature descriptions.
6. **Project Structure**: A brief tree of the codebase so evaluators understand the architecture.
7. **Known Limitations & Future Ideas**: Document any API rate limits, missing features, or planned enhancements (as encouraged by the course rubric).

## Agent Documentation Workflow
- **Continuous Updates**: Whenever a new CLI command, flag, or feature is successfully implemented and tested, the agent MUST automatically propose an update to the `Usage & Examples` section of the `README.md`.
- **Asset Management**: If a visual change is made (like adding a new Rich table or Textual dashboard), instruct the user to take a screenshot and place it in the `docs/assets/` directory.
- **Completeness Check**: Ensure that a stranger could install and use the tool relying purely on the `README.md` instructions.

## Code Comments and Docstrings
- Ensure all public functions, classes, and modules have accurate Python docstrings.
- Keep inline comments focused on *why* the code is doing something, not *what* it is doing.