import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

# Load API credentials from environment variables
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")

# Initialize OpenAI client with custom API endpoint
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

class ChatbotApp:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f2f5')  # Light gray background
        
        # Define custom fonts for different UI elements
        self.title_font = ('Helvetica', 18, 'bold')
        self.chat_font = ('Helvetica', 12)
        self.button_font = ('Helvetica', 10, 'bold')
        
        # Create title frame with blue background
        title_frame = tk.Frame(self.root, bg='#4a6fa5')
        title_frame.pack(fill=tk.X)
        
        # Add title label to the title frame
        title_label = tk.Label(
            title_frame,
            text="AI Assistant",
            font=self.title_font,
            bg='#4a6fa5',
            fg='white',
            pady=15
        )
        title_label.pack()
        
        # Create frame for chat history area
        chat_frame = tk.Frame(self.root, bg='#f0f2f5')
        chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Create scrollable text widget for chat history
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,              # Word wrapping
            width=50,
            height=20,
            state='disabled',          # Read-only by default
            font=self.chat_font,
            bg='white',                # White background for chat area
            fg='#333333',              # Dark gray text
            padx=10,
            pady=10,
            bd=0,                      # No border
            highlightthickness=1,      # Thin highlight border
            highlightbackground='#cccccc',
            highlightcolor='#cccccc'
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        
        # Create frame for input controls
        input_frame = tk.Frame(self.root, bg='#f0f2f5')
        input_frame.pack(pady=(0, 10), padx=10, fill=tk.X)
        
        # Create text input field for user messages
        self.user_input = tk.Entry(
            input_frame,
            width=5,
            font=self.chat_font,
            bg='white',
            fg='#333333',
            bd=0,                      # No border
            highlightthickness=1,
            highlightbackground='#cccccc',
            highlightcolor='#4a6fa5',  # Blue highlight when focused
            insertbackground='#4a6fa5' # Blue cursor
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # Create send button
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            font=self.button_font,
            bg='#4a6fa5',              # Blue background
            fg='white',                # White text
            activebackground='#3a5a8f', # Darker blue when clicked
            activeforeground='white',
            bd=0,                      # No border
            padx=15,
            pady=5,
            highlightthickness=0
        )
        send_button.pack(side=tk.RIGHT)
        
        # Configure text tags for different message senders
        self.chat_history.tag_config('user', foreground='#4a6fa5')  # Blue for user
        self.chat_history.tag_config('bot', foreground='#2e7d32')   # Green for bot

    def send_message(self):
        """Handle sending user message and getting AI response"""
        # Get user input and remove whitespace
        user_message = self.user_input.get().strip()
        if not user_message:
            return  # Don't send empty messages
            
        # Add user message to chat history
        self.update_chat("You", user_message)
        # Clear input field
        self.user_input.delete(0, tk.END)
        
        # Show typing indicator while waiting for response
        self.show_typing_indicator()
        
        try:
            # Get AI response
            bot_response = self.get_completion(user_message)
            # Remove typing indicator
            self.remove_typing_indicator()
            # Add bot response to chat history
            self.update_chat("Bot", bot_response, 'bot')
        except Exception as e:
            # Handle API errors
            self.remove_typing_indicator()
            messagebox.showerror("Error", f"API Error: {str(e)}")

    def show_typing_indicator(self):
        """Display typing indicator while AI is processing"""
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, "AI is typing...\n", "typing")
        self.chat_history.see(tk.END)  # Scroll to bottom
        self.chat_history.configure(state='disabled')
        self.root.update()  # Force UI update
        
    def remove_typing_indicator(self):
        """Remove the typing indicator from chat"""
        self.chat_history.configure(state='normal')
        # Delete the last line (typing indicator)
        self.chat_history.delete("end-2l", "end-1l")
        self.chat_history.configure(state='disabled')

    def update_chat(self, sender, message, tag=None):
        """Add a new message to the chat history"""
        self.chat_history.configure(state='normal')  # Enable editing
        
        if sender == "You":
            # Add user message with blue color
            self.chat_history.insert(tk.END, f"You: ", "user")
            self.chat_history.insert(tk.END, f"{message}\n\n")
        else:
            # Add bot message with green color
            self.chat_history.insert(tk.END, f" AI: ", "bot")
            self.chat_history.insert(tk.END, f"{message}\n\n")
            
        self.chat_history.see(tk.END)  # Auto-scroll to bottom
        self.chat_history.configure(state='disabled')  # Make read-only again

    def get_completion(self, prompt):
        """Get AI response from the API"""
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",  # Free model
            messages=[{"role": "user", "content": prompt}],
            temperature=0  # Deterministic responses
        )
        return response.choices[0].message.content

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()