# **Team Collaboration Log - IS2209 Group 43**

## **Roles**

The team consisted of four members.

### **Cillian**

Took the lead role, responsible for the core application development including the Flask backend, database integration, API routes, the CI pipeline, deployment to Render, and overall project coordination.

### **Jack**

Contributed the CI pipeline setup, adding the lint and test steps to the GitHub Actions workflow.

### **Ronan and Donagh**

Contributed frontend improvements to the user interface, including features such as breed filtering.

## **Ceremonies**

The team collaborated informally, coordinating work through GitHub pull requests and commits rather than formal ceremonies such as standups or sprint planning. Using the issue feature on github to identify and fix problems within the application allowed for seamless iterative design. This approach suited the scale of the project, with team members working at their own pace and reviewing each other's pull requests before merging, although the use of a project board may have more positively increased workflow effectiveness.

## **Version Control**

The team followed a feature branching model with all work developed on short-lived feature branches and merged into master via pull requests. Branch naming followed the feat/&lt;description&gt; format throughout the project.

Each team member created pull requests, with CI checks required to pass before merging. Where checks failed, fixes were committed and the pipeline re-run before proceeding.

## **PR Evidence**

The team's collaboration is evidenced through the GitHub pull request history. Key PRs include:

- Addition of lint and test steps to the CI pipeline (Jack)
- UI improvement work (Donagh)
- CI configuration and requirements fixes (Cillian)
- Database integration and API routes (Cillian)

In total the team merged over a dozen workflow runs on the master branch, with pull requests used as the primary mechanism for code review.

Repository: <https://github.com/cillianob06/IS2209-Project>

## **Note on Task Tracking**

The team did not use a formal project board. Task allocation was managed informally through GitHub commits and pull requests, with each team member working on clearly scoped features or fixes. Issues were created on GitHub in situations where a particular part of code needed fixing.