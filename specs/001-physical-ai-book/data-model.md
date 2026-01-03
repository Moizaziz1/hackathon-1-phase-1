# Data Model: Physical AI & Humanoid Robotics Book

## Book Module
- **name**: string (required) - Module name (e.g., "ROS 2 Fundamentals")
- **title**: string (required) - Display title for the module
- **description**: string (required) - Brief overview of the module content
- **learningObjectives**: array of strings (required) - Specific skills/knowledge learners will gain
- **prerequisites**: array of strings (optional) - Knowledge/skills required before starting
- **duration**: string (optional) - Estimated time to complete the module
- **contentPath**: string (required) - File path to the module's content
- **labs**: array of Lab objects (optional) - Associated hands-on labs

## Content Page
- **id**: string (required) - Unique identifier for the page
- **title**: string (required) - Page title
- **content**: string (required) - Markdown content of the page
- **module**: string (required) - Reference to the parent module
- **order**: integer (required) - Order within the module
- **type**: enum (required) - Type of content (concept, tutorial, lab, resource)
- **relatedPages**: array of strings (optional) - Links to related content

## Hands-on Lab
- **id**: string (required) - Unique identifier for the lab
- **title**: string (required) - Lab title
- **description**: string (required) - Brief overview of the lab
- **objectives**: array of strings (required) - What learners will achieve
- **requirements**: array of strings (required) - Software/hardware needed
- **steps**: array of objects (required) - Sequential instructions
  - **stepNumber**: integer (required)
  - **description**: string (required)
  - **expectedOutcome**: string (optional)
- **validation**: string (required) - How to verify successful completion
- **module**: string (required) - Reference to the parent module

## Capstone Project
- **id**: string (required) - Unique identifier for the project
- **title**: string (required) - Project title
- **description**: string (required) - Overview of the project
- **objectives**: array of strings (required) - Learning outcomes
- **requirements**: array of strings (required) - Prerequisites and resources
- **phases**: array of objects (required) - Project development stages
  - **phaseName**: string (required)
  - **description**: string (required)
  - **tasks**: array of strings (required)
  - **deliverables**: array of strings (required)
- **integrationPoints**: array of strings (required) - How it connects to modules
- **validationCriteria**: array of strings (required) - How success is measured

## Architecture Diagram
- **id**: string (required) - Unique identifier for the diagram
- **title**: string (required) - Diagram title
- **description**: string (required) - What the diagram illustrates
- **filePath**: string (required) - Path to the diagram file
- **module**: string (optional) - Module this diagram belongs to
- **type**: enum (required) - Type of diagram (system, flow, component, etc.)

## Code Example
- **id**: string (required) - Unique identifier for the example
- **title**: string (required) - Example title
- **description**: string (required) - What the example demonstrates
- **code**: string (required) - The actual code content
- **language**: string (required) - Programming language
- **module**: string (required) - Module this example belongs to
- **relatedConcepts**: array of strings (optional) - Concepts illustrated
- **usageNotes**: string (optional) - Additional guidance for use