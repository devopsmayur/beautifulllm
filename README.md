beautifulllm
A secure, Python-based toolset for fetching secrets from HashiCorp Vault, parsing website content, and leveraging Anthropic's Claude LLM for intelligent website summarization.

Features
Secure Secret Management: Integrates with HashiCorp Vault using AppRole authentication to safely retrieve secrets (like API keys).
AI-powered Summarization: Uses Anthropic's Claude (via the anthropic Python library) to generate concise summaries of website content.
Website Parsing: Fetches and parses website HTML, stripping away irrelevant content for clean analysis.
Jupyter Notebook Integration: Outputs summaries directly as Markdown for interactive use in notebooks.
Requirements
Python 3.7+
hvac
requests
beautifulsoup4
anthropic
IPython
Install dependencies:

bash
pip install hvac requests beautifulsoup4 anthropic ipython
Getting Started
Configure HashiCorp Vault Credentials

Set these environment variables (or provide them in code):

VAULT_ADDR (e.g., http://localhost:8200)
VAULT_ROLE_ID
VAULT_SECRET_ID
(Optional) ANTHROPIC_API_KEY as a fallback
Usage Example

Python
from secure_analyzer import summarize, display_summary

# Summarize a website and print result
summary = summarize("https://devopsmayur.github.io/mgblogs")
print(summary)

# Or display summary in a Jupyter notebook
display_summary("https://devopsmayur.github.io/mgblogs")
How It Works
VaultSecretManager: Handles AppRole authentication and secret retrieval from Vault.
Anthropic Client: Authenticates using securely fetched API Key for Claude LLM access.
Website Class: Downloads and parses web pages, cleans up unwanted tags, and extracts readable text.
Summarization Functions: Sends the cleaned text to Claude with clear instructions to generate a succinct markdown summary.
Security Notes
Production Use: Always use Vault for secret management. The environment variable fallback is for development only.
Token Renewal: Vault tokens are automatically renewed when possible.
Example Output
Code
✓ Successfully authenticated with Vault using AppRole
✓ Successfully retrieved API key from HashiCorp Vault using AppRole
✓ Anthropic API connection successful
Website title: My Blog
Content preview: Welcome to my blog...
✓ Claude test response:
11
License
MIT

Note:
Update the description and usage sections as your project evolves! If your project grows, consider breaking the codebase into modules and providing more extensive documentation.

Let me know if you want a more detailed section, contribution guidelines, or any project badges!

