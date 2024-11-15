<h1 align="center">🌟 Cognipath 🌟</h1>

<p align="center">
  Cognipath is an AI-powered educational platform designed to help children develop essential skills through interactive and engaging tools. Leveraging Google Cloud’s Gemini API, Vertex AI, Imagen3, and Text-to-Speech, Cognipath provides personalized, inclusive learning experiences that empower children of all abilities, including those with Autism Spectrum Disorder (ASD).
</p>

<img src="https://github.com/user-attachments/assets/72fb1a64-7bbd-4da4-89dc-29f63b92a13e" alt="project-screenshot" width=auto height="auto">

<h2>📑 Table of Contents</h2>
<ul>
  <li><a href="#inspiration">✨ Inspiration</a></li>
  <li><a href="#what-it-does">💡 What It Does</a></li>
  <li><a href="#how-we-built-it">🔧 How We Built It</a></li>
  <li><a href="#challenges-we-ran-into">🚧 Challenges We Ran Into</a></li>
  <li><a href="#accomplishments-that-were-proud-of">🏆 Accomplishments That We're Proud Of</a></li>
  <li><a href="#what-we-learned">📚 What We Learned</a></li>
  <li><a href="#whats-next-for-cognipath">🔮 What's Next for Cognipath</a></li>
  <li><a href="#installation">⚙️ Installation</a></li>
  <li><a href="#usage">🚀 Usage</a></li>
  <li><a href="#team">👥 Team</a></li>
  <li><a href="#acknowledgments">📣 Acknowledgments</a></li>
</ul>

<h2 id="inspiration">✨ Inspiration</h2>
<p>
  The inspiration for <strong>Cognipath</strong> comes from a personal experience. My younger brother, who is on the Autism Spectrum, often struggled with traditional learning tools. This project was born out of a desire to create a supportive, engaging, and inclusive educational platform to help children like him and others feel empowered in their learning journey.
</p>

<h2 id="what-it-does">💡 What It Does</h2>
<p>
  Cognipath includes several innovative features to support children’s learning:
</p>
<ul>
  <li><strong>Storyfy</strong>: Converts user drawings, text, and audio into engaging stories, followed by a comprehension quiz.</li>
  <li><strong>Expressify</strong>: Facilitates conversations with an AI avatar that responds to real-time video inputs, enhancing communication skills.</li>
  <li><strong>Writing Wizard</strong>: Use the power of gemini flash 1.5 to understand the handwritten paragraphs please correct</li>
  <li><strong>Emotion Recognition</strong>: Presents emotion-related images and prompts children to identify the corresponding emotion, fostering emotional awareness.</li>
</ul>
<img src="https://github.com/user-attachments/assets/fc107b36-e14a-4781-8e98-4dfe8c078a9d" alt="project-screenshot" width=auto height="auto">
<p>
  The platform also includes a parental dashboard that tracks daily, weekly, and monthly progress, recent activities, and provides insights on writing, communication, emotion understanding, and expressive proficiency.
</p>

<h2 id="how-we-built-it">🔧 How We Built It</h2>
<ul>
  <li><strong>Backend</strong>: Built with Flask and <strong>Firebase</strong> for secure data management.</li>
  <li><strong>Frontend</strong>: Implemented with HTML, CSS, and JavaScript for an interactive user experience.</li>
  <li><strong>AI and Cloud Services</strong>:
    <ul>
      <li><strong>Gemini API</strong>: For interpreting text, images, and video inputs.</li>
      <li><strong>Vertex AI</strong>: Used for deploying machine learning models.</li>
      <li><strong>Imagen3</strong>: Converts text inputs into engaging images for storytelling.</li>
      <li><strong>Text-to-Speech</strong>: Provides narration for stories and responses.</li>
    </ul>
  </li>
</ul>
<h2>🧐 Structure</h2>

```
|-- .venv/                                 # Virtual environment folder
|-- requirements.txt                      # App Dependencies
|-- run.py                                # Start the app - WSGI gateway
|-- run.py
|-- credentials.json
|-- Dockerfile
|-- README.md
|-- LICENSE
|-- .gitignore

|-- app/
|    |
|    |    |
|    |    |-- static/
|    |    |    |
|    |    |    |-- images/
|    |    |    |
|    |    |    |-- static/
|    |    |    |    |-- auth/
|    |    |    |    |-- back/
|    |    |    |    |-- front/
|    |    |    |-- templates/            # Templates used to render pages
|    |    |    |    |-- *.html/          # All HTML files

|    |-- templates/                      
|    |    |
|    |    |-- *.html                   
|    |
|    |-- views.py                       # App views and routes

```

<h2 id="challenges-we-ran-into">🚧 Challenges We Ran Into</h2>
<ul>
  <li><strong>Integrating AI Services</strong>: Ensuring compatibility and real-time performance with tools like Gemini API and Vertex AI.</li>
  <li><strong>User Experience Design</strong>: Creating an intuitive interface for children and informative insights for parents.</li>
  <li><strong>Data Security</strong>: Protecting user data, especially for young users, using Firebase.</li>
  <li><strong>Accessibility</strong>: Customizing features to support children with ASD for an inclusive learning experience.</li>
</ul>

<h2 id="accomplishments-that-were-proud-of">🏆 Accomplishments That We're Proud Of</h2>
<ul>
  <li>Developing an inclusive educational platform that supports children with diverse learning needs, including those with ASD.</li>
  <li>Creating interactive learning experiences that engage children while providing valuable progress insights for parents.</li>
</ul>

<h2 id="what-we-learned">📚 What We Learned</h2>
<ul>
  <li>The importance of integrating multiple AI services into a cohesive solution.</li>
  <li>The value of user-centric design and accessibility in educational tools.</li>
  <li>How to manage user data securely in compliance with best practices.</li>
</ul>

<h2 id="whats-next-for-cognipath">🔮 What's Next for Cognipath</h2>
<ul>
  <li>Expanding <strong>Expressify</strong> with enhanced interaction capabilities.</li>
  <li>Adding more creative learning tools and emotional well-being activities.</li>
  <li>Supporting multiple languages and accessibility features.</li>
  <li>Enhancing the parental dashboard with deeper insights.</li>
</ul>

<h2 id="installation">⚙️ Installation</h2>
<ol>
  <li>Clone this repository:
    <pre><code>git clone https://github.com/Ghada-ui/CogniPath.git</code></pre>
  </li>
  <li>Navigate to the project directory:
    <pre><code>cd cognipath</code></pre>
  </li>
  <li>Create a virtual environment:
    <pre><code>python -m venv .venv</code></pre>
  </li>
  <li>Activate the virtual environment:
    <pre><code>.venv/Scripts/Activate</code></pre>
    (On macOS/Linux, use: <code>source .venv/bin/activate</code>)
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Create a `.env` file in the project directory with the following contents:
    <pre><code>
GEMINI_API_KEY=""   
FIREBASE_WEB_API_KEY=""
FIREBASE_AUTH_DOMAIN=""
FIREBASE_DATABASE_URL=""
FIREBASE_PROJECT_ID=""
FIREBASE_STORAGE_BUCKET=""
FIREBASE_MESSAGING_SENDER_ID=""
FIREBASE_APP_ID=""
FIREBASE_MEASUREMENT_ID=""
APP_SECRET=""
GCP_PROJECT=""
GCP_REGION=""
API_URL_3D=""
Image_Bearer=""
    </code></pre>
  </li>
  <li>Download the `credentials.json` file for your Google Cloud project and place it in the root directory (`./`):
    <pre><code>./credentials.json</code></pre>
  </li>
  <li>Ensure the `firebase.json` file is placed in the `app/` directory:
    <pre><code>app/firebase.json</code></pre>
  </li>
  <li>Run the application:
    <pre><code>python run.py</code></pre>
  </li>
</ol>



<h2 id="usage">🚀 Usage</h2>
<ol>
  <li><strong>Create an Account</strong>: Sign up with your email or Google account.</li>
  <li><strong>Explore Features</strong>: Click "Learn" to access the main features. For Google signups, complete your profile in the Profile section.</li>
  <li><strong>Feature Guide</strong>: Use the help button on each feature page to learn more.</li>
  <li><strong>Permissions</strong>: Enable mic and camera for <strong>Expressify</strong>.</li>
  <li><strong>Track Progress</strong>: Add the child’s name and age in the Profile section to start tracking progress on the dashboard.</li>
</ol>

<h2 id="team">👥 Team</h2>
<img src="https://github.com/user-attachments/assets/4553b6a1-55f8-484a-a256-c020724a62a6" alt="project-screenshot" width=auto height="auto">

<h2 id="acknowledgments">📣 Acknowledgments</h2>
<p>
  This project was developed for the <strong>Google Cloud Gemini Hackathon</strong>. We are grateful for the opportunity to contribute to innovative, data-driven educational tools and look forward to future developments.
</p>

---


