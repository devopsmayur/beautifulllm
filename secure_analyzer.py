# imports
import os
import requests
import hvac
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import anthropic

class VaultSecretManager:
    """
    HashiCorp Vault integration for secure secret management using AppRole authentication
    """
    def __init__(self, vault_url=None, role_id=None, secret_id=None, vault_path="secret/data/anthropic"):
        """
        Initialize Vault client with AppRole authentication
        Args:
            vault_url: Vault server URL (defaults to VAULT_ADDR env var)
            role_id: AppRole Role ID (defaults to VAULT_ROLE_ID env var)
            secret_id: AppRole Secret ID (defaults to VAULT_SECRET_ID env var)
            vault_path: Path to secrets in Vault
        """
        self.vault_url = vault_url or os.getenv('VAULT_ADDR', 'http://localhost:8200')
        self.role_id = role_id or os.getenv('VAULT_ROLE_ID')
        self.secret_id = secret_id or os.getenv('VAULT_SECRET_ID')
        self.vault_path = vault_path
        
        if not self.role_id:
            raise ValueError("Role ID must be provided via VAULT_ROLE_ID environment variable or constructor")
        if not self.secret_id:
            raise ValueError("Secret ID must be provided via VAULT_SECRET_ID environment variable or constructor")
        
        # Initialize Vault client
        self.client = hvac.Client(url=self.vault_url)
        
        # Authenticate using AppRole
        self._authenticate_with_approle()
    
    def _authenticate_with_approle(self):
        """
        Authenticate with Vault using AppRole method
        """
        try:
            # Authenticate using AppRole
            auth_response = self.client.auth.approle.login(
                role_id=self.role_id,
                secret_id=self.secret_id
            )
            
            # Set the client token from the auth response
            self.client.token = auth_response['auth']['client_token']
            
            # Verify authentication was successful
            if not self.client.is_authenticated():
                raise ValueError("AppRole authentication failed - client not authenticated")
            
            print(f"✓ Successfully authenticated with Vault using AppRole")
            print(f"  - Token TTL: {auth_response['auth']['lease_duration']} seconds")
            print(f"  - Renewable: {auth_response['auth']['renewable']}")
            
            # Store auth info for potential token renewal
            self.auth_info = auth_response['auth']
            
        except Exception as e:
            raise Exception(f"Failed to authenticate with Vault using AppRole: {str(e)}")
    
    def renew_token(self):
        """
        Renew the Vault token if it's renewable
        """
        try:
            if hasattr(self, 'auth_info') and self.auth_info.get('renewable', False):
                renewal_response = self.client.auth.token.renew_self()
                print(f"✓ Token renewed successfully. New TTL: {renewal_response['auth']['lease_duration']} seconds")
                return True
            else:
                print("⚠ Token is not renewable")
                return False
        except Exception as e:
            print(f"✗ Failed to renew token: {str(e)}")
            return False
    
    def get_secret(self, key):
        """
        Retrieve a secret from Vault
        Args:
            key: The key name for the secret
        Returns:
            The secret value
        """
        try:
            # Read secret from Vault (KV v2 engine)
            response = self.client.secrets.kv.v2.read_secret_version(path=self.vault_path.split('/')[-1])
            secrets = response['data']['data']
            
            if key not in secrets:
                raise KeyError(f"Secret '{key}' not found in Vault path '{self.vault_path}'")
            
            return secrets[key]
        except Exception as e:
            raise Exception(f"Failed to retrieve secret from Vault: {str(e)}")

# Initialize Vault secret manager with AppRole authentication
try:
    vault_manager = VaultSecretManager()
    api_key = vault_manager.get_secret('ANTHROPIC_API_KEY')
    print("✓ Successfully retrieved API key from HashiCorp Vault using AppRole")
except Exception as e:
    print(f"✗ Vault AppRole authentication failed: {e}")
    print("Falling back to environment variable (NOT RECOMMENDED for production)")
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("No API key found in Vault or environment variables")

# Initialize Anthropic client with securely retrieved API key
client = anthropic.Anthropic(api_key=api_key)

# Test connection
message = "Hello, Claude! How are you doing today?"
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": message}]
)
print("✓ Anthropic API connection successful")
print(response.content[0].text)

# Some websites need you to use proper headers when fetching them:
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            soup = BeautifulSoup(response.content, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            
            # Check if body exists before trying to access it
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = soup.get_text(separator="\n", strip=True)
        except requests.RequestException as e:
            print(f"Error fetching website {url}: {e}")
            self.title = "Error loading website"
            self.text = f"Failed to load content from {url}"

# Test website parsing
mg = Website("https://devopsmayur.github.io/mgblogs")
print(f"Website title: {mg.title}")
print(f"Content preview: {mg.text[:200]}...")

# System prompt for Claude
system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

# Test Claude with a simple question
test_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant with a sense of humor.",
    messages=[{"role": "user", "content": "What is 2 + 2?"}]
)
print("✓ Claude test response:")
print(test_response.content[0].text)

def summarize(url):
    """
    Summarize a website using Claude
    Args:
        url: The URL to analyze
    Returns:
        Summary text from Claude
    """
    try:
        website = Website(url)
        user_content = user_prompt_for(website)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error summarizing website: {str(e)}"

def display_summary(url):
    """
    Display a formatted summary of a website
    Args:
        url: The URL to analyze and display
    """
    summary = summarize(url)
    display(Markdown(summary))
