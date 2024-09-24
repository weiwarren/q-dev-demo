# Overview
Q Dev in the Console
- [ ] Dashboard
- [ ] Customizations

Q Dev in IDE    
- [ ] Q Dev Chat
- [ ] Q Dev Inline Suggestions

Q Dev in cli
- [ ] Q dev app, terminal integration
- [ ] Q chat

# Extensions
- [ ] v1.25.0
- [ ] fast release cycle (3-4 release / months)
- [ ] Connected with product team for feedback and continous improvements

# Q Dev Settings in VSCode
- [ ] Beta feature
- [ ] Short Key (Opt + C, Tab, -> , <-, ESC) https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/actions-and-shortcuts.html
- [ ] Telemetry metrics - Amazon Q Developer uses telemetry metrics to provide data for which code suggestions are suggested or rejected. These telemetry metrics do

# Q Chat
- [ ] Insert / Copy
- [ ] Workspace - only index code. This indexing takes approximately 5–20 minutes for workspace sizes up to 200 MB. Auto refreshed index on 24hours cycle. Incremental updates which memory aware.
 not store any user data.

# Amazon Q App
- [ ] Terminal integration - for git commit messages / cli autocompletion
- [ ] other features

# What is not suppoerted in Q Dev inline suggestion
- .Dockerfile
- .xml
- .env, .properties ...
- .css, .scss, .less ...
- html, .ejs ...

# Tips and tricks
- Generate the plan (analysis) => generate the architecture (design) => generate the api (documentations) => generate folder and files (boilerplate) => generate skeleton code => inline completion => generate unit tests => generate deployment code => generate e2e / integration tests for benchmarking
- Separate ideation from code generation
- Generate skeleton with comments using chat, use inline suggestions later on
- Use it to create test case scenarios for the code instead of generating valid test cases at once
- Provide example of test case including mock and dependencies instead of let it magically figure out all the mocks required in the function chain.
- Use Cmd+C to force generation if you are not getting anything or send it to chat directly
- Insert comments if you are not getting inline suggestions.
- Escape all the triple ticks, all the hash and empty line break to remove automatic styling in chat

# Problem Statement
- [ ] A simple data lake platform to upload CSV, preview a subset of data / (maybe transform), then trigger glue to crawl so I can query using athena from the app.
- [ ] Iterative fast locally and can be deployed to prod easily
