"""
Google Blogger Auto-Posting System
100% FREE - Simple & Working!
Google Gemini FREE API ব্যবহার করে (No Credit Card!)
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import time
import requests
import json

# ===============================
# Configuration
# ===============================

class Config:
    """System configuration"""
    
    # Google services
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    
    # Gemini FREE API (no credit card needed!)
    GEMINI_API_KEY = None  # Will ask at runtime or get from user
    
    # Fixed prompts
    BLOG_PROMPTS = [
        "Write about artificial intelligence and its impact on society",
        "Write about healthy eating habits and nutrition tips",
        "Write about digital marketing strategies for small businesses",
        "Write about learning programming and coding basics",
        "Write about travel tips and destination recommendations"
    ]


# ===============================
# FREE Content Generator (Google Gemini)
# ===============================

class GeminiFreeGenerator:
    """Google Gemini - Completely FREE (No credit card required!)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def generate_blog(self, prompt):
        """Generate blog using Gemini FREE API"""
        
        if not self.api_key:
            print("❌ Gemini API key not set!")
            return None
        
        print(f"\n📝 Generating blog...")
        print(f"   Topic: {prompt[:60]}...")
        
        # Prepare request
        full_prompt = f"""Create a complete blog post about: {prompt}

Format your response EXACTLY like this:

TITLE: [Write an engaging, SEO-friendly title]

CONTENT:
<p>Write an engaging introduction paragraph here.</p>

<h2>First Main Section</h2>
<p>Write detailed content for this section. Make it informative and interesting.</p>

<h2>Second Main Section</h2>
<p>Continue with more valuable information. Include practical examples.</p>

<h2>Third Main Section</h2>
<p>Add more relevant content. Keep it engaging and useful for readers.</p>

<p>Write a strong conclusion paragraph that summarizes the key points.</p>

TAGS: technology, blogging, guide, tips, tutorial

Requirements:
- Write 500-700 words
- Use proper HTML formatting (<p>, <h2>, <ul>, <li>, <strong>)
- Make it informative and engaging
- Include practical tips or examples
- Professional and reader-friendly tone"""

        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }]
        }
        
        try:
            # Make API request
            url = f"{self.api_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract generated text
                if 'candidates' in result and len(result['candidates']) > 0:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    print("✅ Blog generated successfully!")
                    return self._parse_response(text)
                else:
                    print("❌ No content generated")
                    return None
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def _parse_response(self, text):
        """Parse AI response into blog components"""
        
        title = "Blog Post"
        content = "<p>Content not available</p>"
        tags = ["blog", "article"]
        
        lines = text.split('\n')
        
        # Extract title
        for i, line in enumerate(lines):
            if 'TITLE:' in line.upper():
                title = line.split(':', 1)[1].strip()
                if not title and i + 1 < len(lines):
                    title = lines[i + 1].strip()
                break
        
        # Extract tags
        for line in lines:
            if 'TAGS:' in line.upper() or 'TAG:' in line.upper():
                tags_str = line.split(':', 1)[1].strip()
                tags = [t.strip() for t in tags_str.split(',') if t.strip()]
                break
        
        # Extract content
        content_start = -1
        content_end = len(text)
        
        for i, line in enumerate(lines):
            if 'CONTENT:' in line.upper():
                content_start = i + 1
            if content_start != -1 and ('TAGS:' in line.upper() or 'TAG:' in line.upper()):
                content_end = i
                break
        
        if content_start != -1:
            content_lines = lines[content_start:content_end]
            content = '\n'.join(content_lines).strip()
        
        # Basic HTML check
        if '<p>' not in content and '<h' not in content:
            # Add basic formatting
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            content = '\n'.join([f'<p>{p}</p>' for p in paragraphs])
        
        return {
            'title': title,
            'content': content,
            'tags': tags[:5] if tags else ['blog', 'article']
        }


# ===============================
# Simple Template Generator (Backup)
# ===============================

class SimpleTemplateGenerator:
    """Simple template-based content (works without any AI!)"""
    
    @staticmethod
    def generate(prompt):
        """Generate basic blog from template"""
        
        # Extract topic from prompt
        topic = prompt.replace("Write about", "").strip()
        
        title = f"A Complete Guide to {topic.title()}"
        
        content = f"""
<p>Welcome to our comprehensive guide about {topic}. In this article, we'll explore the key aspects and provide you with valuable insights.</p>

<h2>Understanding the Basics</h2>
<p>{topic.capitalize()} is an important topic that affects many aspects of our daily lives. Whether you're a beginner or looking to expand your knowledge, this guide will help you understand the fundamentals.</p>

<h2>Key Points to Consider</h2>
<p>When exploring {topic}, there are several important factors to keep in mind:</p>
<ul>
<li><strong>Research and Learning:</strong> Take time to understand the core concepts</li>
<li><strong>Practical Application:</strong> Apply what you learn in real-world situations</li>
<li><strong>Continuous Improvement:</strong> Keep updating your knowledge regularly</li>
</ul>

<h2>Best Practices and Tips</h2>
<p>To get the most out of {topic}, consider these proven strategies:</p>
<p>Start with the basics and gradually build your understanding. Don't rush the learning process. Take time to practice and apply what you learn. Seek feedback from others and stay updated with the latest developments.</p>

<h2>Common Mistakes to Avoid</h2>
<p>Many people make these common mistakes when dealing with {topic}. Being aware of them will help you avoid unnecessary setbacks and progress more smoothly.</p>

<h2>Conclusion</h2>
<p>Understanding {topic} is a journey that requires patience and dedication. By following the guidelines in this article, you'll be well on your way to mastering the subject. Remember to practice regularly and stay curious.</p>

<p>We hope this guide has been helpful. Feel free to explore more resources and continue your learning journey!</p>
"""
        
        tags = ["guide", "tips", "tutorial", "learning", "blog"]
        
        return {
            'title': title,
            'content': content.strip(),
            'tags': tags
        }


# ===============================
# Google Blogger Manager
# ===============================

class BloggerManager:
    """Google Blogger API handler"""
    
    def __init__(self):
        self.service = None
        self.blog_id = None
        print("\n📝 Initializing Blogger Manager...")
    
    def authenticate(self):
        """Authenticate with Google"""
        creds = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                print("✅ Found existing credentials")
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing credentials...")
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("\n❌ credentials.json not found!")
                    print("\n📝 How to get credentials.json:")
                    print("1. Go to: https://console.cloud.google.com")
                    print("2. Create project → Enable Blogger API v3")
                    print("3. Create OAuth 2.0 Client ID (Desktop app)")
                    print("4. Download as credentials.json")
                    return False
                
                print("🔐 Starting authentication...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', Config.SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ Authentication successful!")
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('blogger', 'v3', credentials=creds)
        print("✅ Blogger API connected!")
        return True
    
    def select_blog(self):
        """Select blog"""
        try:
            print("\n🔍 Fetching your blogs...")
            blogs = self.service.blogs().listByUser(userId='self').execute()
            
            if not blogs.get('items'):
                print("❌ No blogs found!")
                print("   Create a blog at: https://www.blogger.com")
                return False
            
            print("\n📚 Your blogs:")
            for idx, blog in enumerate(blogs['items'], 1):
                print(f"  {idx}. {blog['name']}")
                print(f"     {blog['url']}")
            
            if len(blogs['items']) == 1:
                self.blog_id = blogs['items'][0]['id']
                print(f"\n✅ Selected: {blogs['items'][0]['name']}")
            else:
                choice = int(input("\nSelect blog number: ")) - 1
                self.blog_id = blogs['items'][choice]['id']
                print(f"✅ Selected: {blogs['items'][choice]['name']}")
            
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def create_post(self, title, content, labels=None, draft=False):
        """Create post"""
        try:
            post_body = {
                'kind': 'blogger#post',
                'title': title,
                'content': content
            }
            
            if labels:
                post_body['labels'] = labels
            
            print(f"\n📤 Posting: {title[:50]}...")
            
            if draft:
                post = self.service.posts().insert(
                    blogId=self.blog_id, body=post_body, isDraft=True
                ).execute()
                print("✅ Draft created!")
            else:
                post = self.service.posts().insert(
                    blogId=self.blog_id, body=post_body
                ).execute()
                print("✅ Published!")
            
            print(f"🔗 {post['url']}")
            return post
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


# ===============================
# Main System
# ===============================

class BloggerAutoPost:
    """Main auto-posting system"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("🚀 Blogger Auto-Posting System")
        print("   100% FREE - Google Gemini")
        print("="*60)
        
        self.blogger = BloggerManager()
        self.generator = None
        self.is_setup = False
    
    def setup(self):
        """Setup system"""
        print("\n🔧 Setting up...")
        
        # Get Gemini API key
        print("\n🤖 Setting up AI Generator...")
        print("\n💡 Google Gemini is 100% FREE!")
        print("   No credit card needed, just a Google account")
        
        api_key = Config.GEMINI_API_KEY
        
        if not api_key:
            print("\n📝 Get your FREE Gemini API key:")
            print("   1. Visit: https://makersuite.google.com/app/apikey")
            print("   2. Sign in with Google account")
            print("   3. Click 'Create API Key'")
            print("   4. Copy the key")
            
            api_key = input("\n🔑 Paste your Gemini API key (or press Enter to use templates): ").strip()
        
        if api_key:
            self.generator = GeminiFreeGenerator(api_key)
            self.use_ai = True
            print("✅ Gemini AI ready!")
        else:
            print("⚠️  No API key - using template generator")
            self.generator = SimpleTemplateGenerator()
            self.use_ai = False
        
        # Setup Blogger
        if not self.blogger.authenticate():
            return False
        
        if not self.blogger.select_blog():
            return False
        
        self.is_setup = True
        print("\n✅ Setup complete!")
        return True
    
    def create_and_post(self, prompt, draft=False):
        """Generate and post blog"""
        if not self.is_setup:
            print("❌ Run setup first!")
            return False
        
        print(f"\n{'='*60}")
        print("📝 Creating blog post...")
        print(f"{'='*60}")
        
        # Generate content
        if self.use_ai:
            blog_data = self.generator.generate_blog(prompt)
        else:
            blog_data = self.generator.generate(prompt)
        
        if not blog_data:
            print("❌ Failed to generate")
            return False
        
        print(f"\n📋 Title: {blog_data['title']}")
        print(f"   Tags: {', '.join(blog_data['tags'])}")
        print(f"   Length: {len(blog_data['content'])} chars")
        
        # Post to Blogger
        post = self.blogger.create_post(
            title=blog_data['title'],
            content=blog_data['content'],
            labels=blog_data['tags'],
            draft=draft
        )
        
        return post is not None
    
    def auto_post_all(self, draft=False):
        """Post all prompts"""
        print(f"\n🎯 Auto-posting {len(Config.BLOG_PROMPTS)} blogs...")
        
        success = 0
        for idx, prompt in enumerate(Config.BLOG_PROMPTS, 1):
            print(f"\n{'='*60}")
            print(f"Post {idx}/{len(Config.BLOG_PROMPTS)}")
            print(f"{'='*60}")
            
            if self.create_and_post(prompt, draft):
                success += 1
            
            if idx < len(Config.BLOG_PROMPTS):
                print("\n⏳ Waiting 10 seconds...")
                time.sleep(10)
        
        print(f"\n✅ Done! {success}/{len(Config.BLOG_PROMPTS)} successful")


# ===============================
# Main
# ===============================

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║  🚀 Blogger Auto-Poster - Simple & FREE                  ║
║                                                           ║
║  ✓ Google Gemini FREE API (No credit card!)             ║
║  ✓ Template fallback (works without AI)                 ║
║  ✓ Easy setup & use                                      ║
╚═══════════════════════════════════════════════════════════╝

📦 Install:
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib requests

🔑 Required:
- credentials.json (from Google Cloud Console)
- Gemini API key (FREE from makersuite.google.com)
    """)
    
    # Check credentials
    if not os.path.exists('credentials.json'):
        print("\n⚠️  Need credentials.json!")
        print("Get from: https://console.cloud.google.com")
        input("Press ENTER after adding it...")
        
        if not os.path.exists('credentials.json'):
            print("❌ Still not found!")
            return
    
    # Initialize
    system = BloggerAutoPost()
    
    if not system.setup():
        print("\n❌ Setup failed!")
        return
    
    # Menu
    while True:
        print("\n" + "="*60)
        print("📋 MENU")
        print("="*60)
        print("1. Post single blog (custom)")
        print("2. Post ALL fixed prompts")
        print("3. Test (draft mode)")
        print("4. View prompts")
        print("5. Exit")
        
        choice = input("\nChoice (1-5): ").strip()
        
        if choice == '1':
            prompt = input("\n📝 Blog topic: ").strip()
            if prompt:
                draft = input("Draft? (y/n): ").lower() == 'y'
                system.create_and_post(prompt, draft)
        
        elif choice == '2':
            draft = input("\nDrafts? (y/n): ").lower() == 'y'
            confirm = input(f"Post {len(Config.BLOG_PROMPTS)} blogs? (y/n): ")
            if confirm.lower() == 'y':
                system.auto_post_all(draft)
        
        elif choice == '3':
            print("\n🧪 Test mode")
            system.create_and_post(Config.BLOG_PROMPTS[0], draft=True)
        
        elif choice == '4':
            print("\n📚 Fixed Prompts:")
            for i, p in enumerate(Config.BLOG_PROMPTS, 1):
                print(f"  {i}. {p}")
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")