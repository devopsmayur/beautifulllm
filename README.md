
# 🔐 Claude-Powered Website Summarizer with HashiCorp Vault Integration

This project is a secure Python-based tool that:

- Authenticates with **HashiCorp Vault** using **AppRole**
- Retrieves a secret API key securely
- Connects to **Anthropic Claude API**
- Fetches and parses content from a website using **BeautifulSoup**
- Generates and displays a **Markdown summary** using Claude's LLM capabilities

---

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
```

You’ll also need:

- A running [HashiCorp Vault](https://www.vaultproject.io/)  
- A valid [Anthropic Claude API Key](https://www.anthropic.com/)

---

## 🔧 Environment Configuration

Set the following environment variables (manually or via `.env` file):

```env
VAULT_ADDR=http://localhost:8200
VAULT_ROLE_ID=your_approle_role_id
VAULT_SECRET_ID=your_approle_secret_id
```

The Vault path where your Claude API key is stored should default to:

```
secret/data/anthropic
```

Under this path, you should store the key as:

```json
{
  "ANTHROPIC_API_KEY": "your-actual-api-key"
}
```

---

## 🚀 How It Works

1. **Vault AppRole Authentication**: Securely logs into Vault using Role ID and Secret ID.  
2. **Secret Retrieval**: Fetches the `ANTHROPIC_API_KEY` from Vault.  
3. **Claude API Client**: Initializes the Claude client with the retrieved key.  
4. **Website Scraping**: Fetches a web page and parses the title + content.  
5. **Content Summarization**: Uses Claude to generate a natural language summary.  
6. **Output**: Displays the summary in a Markdown-rendered cell (Jupyter-friendly).  

---

## 🧪 Example Usage

```python
display_summary("https://devopsmayur.github.io/mgblogs")
```

### Sample Output:

```markdown
### Website Summary: mgblogs

This site is a personal tech blog covering DevOps, cloud infrastructure, and engineering insights. It includes recent updates, tutorials, and learning resources for professionals.
```

---

## 📁 Project Structure

```plaintext
.
├── main.py              # Main script with Vault + Claude + Web summarization logic
├── .env                 # Optional - for storing secrets locally (not for production)
├── README.md            # You're reading it!
```

---

## ⚠️ Warnings

- **Never** hardcode secrets. Use Vault or secure environment variables.  
- Avoid using `.env` files in production environments.  
- Claude API key is sensitive. Ensure Vault access is tightly controlled.  

---

## 📚 References

- [HashiCorp Vault Docs](https://developer.hashicorp.com/vault/docs)  
- [Anthropic Claude API](https://docs.anthropic.com/)  
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  

---

## 🧠 Author

**Mayur Gandhi**  
Senior Enterprise Technologist | Cloud & AI Architect  
[https://devopsmayur.github.io/mgblogs](https://devopsmayur.github.io/mgblogs)

---

## 📝 License

MIT License
