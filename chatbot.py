import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f2f5')
        
        # Custom fonts
        self.title_font = ('Helvetica', 18, 'bold')
        self.chat_font = ('Helvetica', 12)
        self.button_font = ('Helvetica', 10, 'bold')
        
        # Title frame
        title_frame = tk.Frame(self.root, bg='#4a6fa5')
        title_frame.pack(fill=tk.X)
        
        # Title label
        title_label = tk.Label(
            title_frame,
            text="AI Assistant",
            font=self.title_font,
            bg='#4a6fa5',
            fg='white',
            pady=15
        )
        title_label.pack()
        
        # Chat history frame
        chat_frame = tk.Frame(self.root, bg='#f0f2f5')
        chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Chat history
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            state='disabled',
            font=self.chat_font,
            bg='white',
            fg='#333333',
            padx=10,
            pady=10,
            bd=0,
            highlightthickness=1,
            highlightbackground='#cccccc',
            highlightcolor='#cccccc'
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f2f5')
        input_frame.pack(pady=(0, 10), padx=10, fill=tk.X)
        
        # Input area
        self.user_input = tk.Entry(
            input_frame,
            width=5,
            font=self.chat_font,
            bg='white',
            fg='#333333',
            bd=0,
            highlightthickness=1,
            highlightbackground='#cccccc',
            highlightcolor='#4a6fa5',
            insertbackground='#4a6fa5'
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # Send button
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            font=self.button_font,
            bg='#4a6fa5',
            fg='white',
            activebackground='#3a5a8f',
            activeforeground='white',
            bd=0,
            padx=15,
            pady=5,
            highlightthickness=0
        )
        send_button.pack(side=tk.RIGHT)
        
        # Configure tag colors for different senders
        self.chat_history.tag_config('user', foreground='#4a6fa5')
        self.chat_history.tag_config('bot', foreground='#2e7d32')

    def send_message(self):
        user_message = self.user_input.get().strip()
        if not user_message:
            return
            
        self.update_chat("You", user_message, 'user')
        self.user_input.delete(0, tk.END)
        
        try:
            bot_response = self.get_completion(user_message)
            self.update_chat("Bot", bot_response, 'bot')
        except Exception as e:
            messagebox.showerror("Error", f"API Error: {str(e)}")

    def update_chat(self, sender, message, tag):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: ", tag)
        self.chat_history.insert(tk.END, f"{message}\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state='disabled')

    def get_completion(self, prompt):
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()