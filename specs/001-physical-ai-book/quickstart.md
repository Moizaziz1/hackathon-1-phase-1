# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager
- Git for version control
- Text editor or IDE of your choice

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm start
   # or
   yarn start
   ```

   This will start the Docusaurus development server and open the book in your browser at `http://localhost:3000`.

4. **Build for production**
   ```bash
   npm run build
   # or
   yarn build
   ```

## Project Structure Overview

```
docs/
├── intro.md                    # Introduction to Physical AI
├── modules/                    # Learning modules
│   ├── ros2-fundamentals/      # ROS 2 fundamentals module
│   ├── simulation-digital-twins/ # Simulation & Digital Twins module
│   ├── ai-perception-navigation/ # AI Perception & Navigation module
│   └── vision-language-action/   # Vision-Language-Action Systems module
├── capstone-project/           # Capstone project guide
└── tutorials/                  # Additional tutorials
```

## Adding New Content

### Adding a New Module
1. Create a new directory in `docs/modules/`
2. Add an `index.md` file as the entry point
3. Add additional content pages as needed
4. Update the sidebar configuration in `docusaurus.config.js`

### Adding a Hands-on Lab
1. Create a new directory within the appropriate module's `hands-on-labs/` folder
2. Write the lab instructions in Markdown format
3. Include setup requirements, step-by-step instructions, and expected outcomes
4. Add links to related resources or code examples

### Adding Code Examples
1. Place code files in the `static/files/code-examples/` directory
2. Reference them in your content using Docusaurus code block syntax
3. Include language-specific syntax highlighting

## Content Guidelines

### Writing Style
- Follow the "Accuracy First" principle: ensure all technical information is correct
- Write in an "Open & Accessible" manner: explain concepts clearly for different skill levels
- Structure content to support "Modular Knowledge": each section should stand alone when possible
- Include practical examples that support "Learning by Building"

### Technical Accuracy
- Test all code examples before publishing
- Verify that all simulation examples work with specified tools
- Include notes about sim-to-real transfer where applicable
- Maintain "Technical Excellence" in all examples and explanations

## Deployment

The book is designed to be deployed to GitHub Pages:
1. The `npm run deploy` command builds and deploys to GitHub Pages
2. Ensure your GitHub repository is configured for GitHub Pages
3. The site will be available at `https://<username>.github.io/<repository>`