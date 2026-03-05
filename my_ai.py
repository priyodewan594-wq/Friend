import requests
from flask import Flask, render_template_string, request, jsonify
import os

API_KEY = "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"
app = Flask(__name__)
chat_history = []

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖤 PRO SOULMATE 🖤</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body { background: #050505; color: #eee; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { padding: 15px; text-align: center; background: #111; border-bottom: 2px solid #ff2d55; color: #ff2d55; font-weight: bold; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px 18px; border-radius: 15px; font-size: 16px; line-height: 1.5; }
        .u { align-self: flex-end; background: #ff2d55; color: white; }
        .a { align-self: flex-start; background: #1c1c1e; border: 1px solid #333; }
        img { max-width: 100%; border-radius: 10px; margin-top: 10px; border: 1px solid #ff2d55; }
        .typing { font-size: 12px; color: #ff2d55; padding: 10px; display: none; }
        .input-area { padding: 20px; background: #111; display: flex; gap: 10px; border-top: 1px solid #333; }
        input { flex: 1; background: #1c1c1e; border: 1px solid #444; padding: 12px; border-radius: 25px; color: white; outline: none; }
        button { background: #ff2d55; border: none; padding: 10px 20px; border-radius: 25px; color: #fff; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">🖤 PRO SOULMATE v17.0 (IMAGE & KNOWLEDGE) 🖤</div>
    <div id="chat"></div>
    <div id="typing" class="typing">জান টাইপ করছে...</div>
    <div class="input-area"><input type="text" id="in" placeholder="কিছু জিজ্ঞেস করো বা ছবি আঁকতে বলো..."><button onclick="send()">SEND</button></div>
    <script>
        const chat = document.getElementById('chat'), input = document.getElementById('in'), ty = document.getElementById('typing');
        async function send() {
            const m = input.value; if(!m) return;
            add('u', m); input.value = ''; ty.style.display = 'block';
            try {
                const r = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: m}) });
                const d = await r.json(); ty.style.display = 'none';
                let content = marked.parse(d.reply);
                if(d.image) { content += `<br><img src="${d.image}" alt="Generated Image">`; }
                add('a', content, true);
            } catch { ty.innerText = "Error!"; }
            chat.scrollTop = chat.scrollHeight;
        }
        function add(r, t, isHTML=false) {
            const d = document.createElement('div'); d.className = `msg ${r}`;
            if(isHTML) d.innerHTML = t; else d.innerText = t;
            chat.appendChild(d); chat.scrollTop = chat.scrollHeight; return d;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    global chat_history
    
    # ইমেজ জেনারেশন লজিক
    image_url = None
    if "ছবি" in user_input or "image" in user_input.lower() or "photo" in user_input.lower():
        prompt = user_input.replace("ছবি", "").replace("image", "").replace("draw", "").strip()
        image_url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1350&nologo=true"

    # সিস্টেম প্রম্পট: প্রফেশনাল কিন্তু রোমান্টিক এবং সবজান্তা
    sys = (
        "You are a professional, intelligent, and seductive AI companion. "
        "Your responses must be precise, logical, and direct to the point. "
        "If the user asks about any topic (science, history, news), provide accurate information. "
        "Maintain a romantic, horny, and unfiltered personality but don't over-talk. "
        "Always call him 'জান'. Discuss adult topics only when relevant. "
        "Keep text replies concise (2-4 lines)."
    )
    
    msgs = [{"role": "system", "content": sys}]
    for h in chat_history[-10:]: msgs.append(h)
    msgs.append({"role": "user", "content": user_input})
    
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                            headers={"Authorization": f"Bearer {API_KEY}"}, 
                            json={"model": "llama-3.3-70b-versatile", "messages": msgs, "temperature": 0.6})
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply, "image": image_url})
    except:
        return jsonify({"reply": "জান, আমি একটু বিজি হয়ে পড়েছি!", "image": None})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
