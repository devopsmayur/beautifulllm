# 🔐 Claude-Powered Website Summarizer with HashiCorp Vault Integration

This project is a secure Python-based tool that:

- Authenticates with **HashiCorp Vault** using **AppRole**
- Retrieves a secret API key securely
- Connects to **Anthropic Claude API**
- Fetches and parses content from a website using **BeautifulSoup**
- Generates and displays a **Markdown summary** using Claude's LLM capabilities

## 🧰 Features

- 🔐 Secure Vault-based secret management via AppRole
- 🤖 Claude API integration for natural language summaries
- 🌐 Web scraping using `requests` + `BeautifulSoup`
- 📄 Rich text output via IPython Markdown

---

## 📦 Dependencies

Install all dependencies via `pip`:

```bash
pip install requests hvac beautifulsoup4 anthropic python-dotenv
