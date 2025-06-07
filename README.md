# Claude Web Scraper & Content Analyzer

A Python tool that scrapes websites and uses Claude AI to generate intelligent summaries of web content. Perfect for content research, competitive analysis, and automated content summarization.

## Features

- 🌐 **Web Scraping**: Extracts clean text content from any website
- 🤖 **AI-Powered Analysis**: Uses Claude Sonnet 4 to generate intelligent summaries
- 🧹 **Content Cleaning**: Removes scripts, styles, and irrelevant HTML elements
- 📝 **Markdown Output**: Generates well-formatted markdown summaries
- 🔍 **Navigation Filtering**: Ignores navigation elements to focus on main content
- 📊 **Jupyter Integration**: Displays formatted results in notebooks

## Installation

### 1. Clone or Download
Save the code as `claude_web_scraper.py` (avoid naming it `claude.py` or `anthropic.py`)

### 2. Install Dependencies
```bash
pip install requests beautifulsoup4 python-dotenv anthropic ipython
```

### 3. Set Up API Key
Create a `.env` file in the same directory:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
```

### 4. Get Claude API Key
1. Sign up at [Anthropic Console](https://console.anthropic.com)
2. Create an API key
3. Add it to your `.env` file

## Usage

### Basic Usage
```python
from claude_web_scraper import summarize, display_summary

# Get text summary
summary = summarize("https://example.com")
print(summary)

# Display formatted markdown (in Jupyter)
display_summary("https://example.com")
```

### Manual Website Analysis
```python
from claude_web_scraper import Website

# Create website object
site = Website("https://example.com")
print(f"Title: {site.title}")
print(f"Content: {site.text[:500]}...")  # First 500 chars
```

### Run Complete Analysis
```bash
python claude_web_scraper.py
```

## Code Structure

### Classes
- **`Website`**: Handles web scraping and content extraction
  - `__init__(url)`: Fetches and processes webpage
  - `title`: Extracted page title
  - `text`: Clean text content

### Functions
- **`summarize(url)`**: Complete analysis pipeline - returns AI summary
- **`display_summary(url)`**: Shows formatted markdown in Jupyter
- **`user_prompt_for(website)`**: Formats content for AI analysis

## Example Output

```markdown
# Website Summary

## Main Content
This is a DevOps blog focusing on containerization and CI/CD practices.

## Key Topics
- Docker containerization fundamentals
- Kubernetes orchestration
- CI/CD pipeline automation
- Cloud deployment strategies

## Recent Posts
- Understanding Docker Containers
- Kubernetes Best Practices
- Automated Deployment Workflows
```

## Configuration

### Supported Models
- `claude-sonnet-4-20250514` (default)
- `claude-opus-4` (for more complex analysis)

### Customization Options

**Adjust Max Tokens:**
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,  # Increase for longer summaries
    # ...
)
```

**Custom System Prompt:**
```python
system_prompt = "You are a technical content analyzer specializing in developer blogs. Provide detailed technical summaries."
```

**Custom Headers:**
```python
headers = {
    "User-Agent": "Your Custom User Agent",
    "Accept": "text/html,application/xhtml+xml"
}
```

## Requirements

- Python 3.7+
- Active internet connection
- Claude API key with available credits
- Target websites must be publicly accessible

## Dependencies

```txt
requests>=2.25.1
beautifulsoup4>=4.9.3
python-dotenv>=0.19.0
anthropic>=0.3.0
ipython>=7.0.0
```

## Limitations

- **Rate Limits**: Claude API has usage limits
- **Content Size**: Very large websites may exceed token limits
- **Dynamic Content**: JavaScript-rendered content not captured
- **Authentication**: Cannot access login-protected pages
- **Robots.txt**: Respects website scraping policies

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'anthropic'"**
```bash
pip install anthropic
```

**"API key not found"**
- Check `.env` file exists
- Verify `ANTHROPIC_API_KEY` is set correctly
- Ensure no extra spaces in the key

**"Website not accessible"**
- Check URL is correct and accessible
- Some sites block automated requests
- Try different User-Agent headers

**"Token limit exceeded"**
- Reduce `max_tokens` parameter
- Target smaller websites
- Split large content into chunks

### Debug Mode
Add print statements to see what's happening:
```python
print(f"Fetching: {url}")
print(f"Title: {website.title}")
print(f"Content length: {len(website.text)}")
```

## Best Practices

1. **Respect Rate Limits**: Don't make too many requests quickly
2. **Check Robots.txt**: Respect website scraping policies
3. **Use Appropriate Headers**: Identify your bot properly
4. **Handle Errors**: Add try-catch blocks for production use
5. **Cache Results**: Store summaries to avoid re-processing

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

---

**Note**: This tool is for educational and research purposes. Always respect website terms of service and robots.txt files when scraping content.
