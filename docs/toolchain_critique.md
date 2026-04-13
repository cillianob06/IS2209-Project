# **Toolchain Critique - IS2209 Group 43**

## **What Worked**

GitHub was the backbone of the project and worked well as a central collaboration point. The pull request model gave the team a clear process for contributing code and the Actions CI pipeline provided automated feedback on every change. Once configured correctly, the pipeline reliably caught issues such as missing dependencies before they were merged.

Supabase provided a straightforward PostgreSQL solution that required minimal setup. Connecting via a DATABASE_URL string meant the application code stayed clean. The free tier was sufficient for the project's needs.

Render proved to be a reliable hosting platform and was simpler to configure than Railway, which the team initially used. Automatic deploys on push to master meant the live application stayed in sync with the codebase without any manual intervention.

The Dog API provided a rich source of data including breed images, temperament, and lifespan information. The free tier was sufficient for development and testing purposes.

## **What We Would Change**

Project board: The team would introduce a project board such as GitHub Projects from the start of the project. Working without formal task tracking meant it was sometimes unclear who was working on what, which led to occasional merge conflicts and duplicated effort. A Kanban board with To Do, In Progress, and Done columns would have improved clarity across the team.

.idea/ in .gitignore: The PyCharm .idea/ folder should have been added to .gitignore from the beginning. This caused recurring merge conflicts on workspace.xml that slowed down the team's ability to pull changes from the remote repository.

## **Risks and Mitigations**

Dog API limitations: The Dog API's free tier does not reliably return breed metadata with image results, which limited the functionality of the breed info card and leaderboard features. This was mitigated by making a separate API call to the /breeds/{id} endpoint and passing breed names from the frontend where the API response lacked metadata. A paid API key or alternative data source would resolve this more cleanly.

Branch protection: The team experienced a case where a pull request with failing CI checks was merged into master. Enabling branch protection rules on GitHub to require all status checks to pass before merging would prevent this in future.