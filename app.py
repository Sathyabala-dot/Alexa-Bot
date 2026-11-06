from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
user_name = ""

def reply_to(message):
    global user_name

    # Make the message lowercase so capital letters do not matter.
    message = message.lower().strip()
    words = message.split()

    # Reply to the user's name before checking for a greeting.
    if "my name is" in message:
        user_name = message.split("my name is")[-1].strip(" .!?").title()
        return "Hello, " + user_name + "! Nice to meet you. I will remember your name while the app is running."
    elif "what is my name" in message or "what's my name" in message:
        if user_name:
            return "Your name is " + user_name + "!"
        return "I do not know yet. Tell me by typing: my name is Sam."
    elif "nice to meet you" in message:
        return "Nice to meet you too!"
    elif "good morning" in message:
        return "Good morning" + (", " + user_name if user_name else "") + "! I hope you have a wonderful day!"
    elif "good afternoon" in message:
        return "Good afternoon" + (", " + user_name if user_name else "") + "! How is your day going?"
    elif "good evening" in message:
        return "Good evening" + (", " + user_name if user_name else "") + "! It is nice to talk with you."
    elif "good night" in message:
        return "Good night" + (", " + user_name if user_name else "") + "! Sleep well."
    elif "hello" in words or "hi" in words or "hey" in words or "hiya" in words:
        return "Hello" + (", " + user_name if user_name else "") + "! How are you today?"
    elif "what's up" in message or "whats up" in message or "how's it going" in message:
        return "I am here and ready to chat! How are you?"
    elif "how are you" in message:
        return "I am doing well, thank you! How are you?"
    elif "i am good" in message or "i am fine" in message or "i am great" in message:
        return "I am glad to hear that" + (", " + user_name if user_name else "") + "!"
    elif "not good" in message or "feeling sad" in message:
        return "I am sorry to hear that. I hope your day gets better!"
    elif "your name" in message or "who are you" in message:
        return "I am Alexa, a simple greeting bot made for a school project."
    elif "thank" in message or "thanks" in message:
        return "You are welcome!"
    elif "bye" in message or "goodbye" in message:
        return "Goodbye! Have a nice day!"
    else:
        return "I am Alexa, your greeting bot. Try saying hello or good morning!"


PAGE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#5546d7">
  <title>Alexa Greeting Bot</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; padding: 18px; background: #f2f3fb; color: #20223a; font-family: Arial, sans-serif; }
    main { width: min(100%, 620px); margin: 0 auto; }
    header { text-align: center; padding: 18px 10px; }
    header h1 { margin: 0 0 7px; color: #4235b5; font-size: 30px; }
    header p { margin: 0; color: #62647a; }
    .chat { height: min(58vh, 520px); min-height: 300px; overflow-y: auto; padding: 16px; border-radius: 18px; background: white; box-shadow: 0 8px 28px #24205b12; }
    .bubble { max-width: 86%; padding: 11px 14px; margin: 8px 0; border-radius: 16px; line-height: 1.45; overflow-wrap: anywhere; }
    .bot { background: #eeedff; border-bottom-left-radius: 4px; }
    .user { margin-left: auto; background: #5546d7; color: white; border-bottom-right-radius: 4px; }
    .controls { display: flex; gap: 8px; margin-top: 12px; }
    input { flex: 1; min-width: 0; padding: 13px; border: 1px solid #d5d5e4; border-radius: 12px; font-size: 16px; }
    button { border: 0; border-radius: 12px; padding: 12px 15px; font-size: 15px; font-weight: 700; color: white; background: #5546d7; cursor: pointer; }
    button:active { transform: scale(.98); }
    button.secondary { background: #77798d; }
    .hint { margin: 13px 4px; color: #65677b; font-size: 14px; line-height: 1.5; }
    @media (max-width: 420px) { body { padding: 10px; } header h1 { font-size: 26px; } .controls { flex-wrap: wrap; } #message { flex-basis: 100%; } }
  </style>
</head>
<body>
<main>
  <header><h1>Alexa Greeting Bot</h1><p>A friendly bot that greets you and speaks its replies</p></header>
  <section class="chat" id="chat" aria-live="polite">
    <div class="bubble bot">Hello! I am Alexa. Say good morning, ask how I am, or tell me your name!</div>
  </section>
  <form class="controls" id="form">
    <input id="message" type="text" placeholder="Type a message…" autocomplete="off" aria-label="Your message">
    <button type="submit">Send</button>
    <button class="secondary" id="mic" type="button" title="Speak">🎙️</button>
  </form>
  <p class="hint" id="hint">Try: “hello”, “good night”, “my name is Sam”, or “what is my name?”</p>
</main>
<script>
  const chat = document.getElementById('chat');
  const input = document.getElementById('message');
  const micButton = document.getElementById('mic');
  const hint = document.getElementById('hint');
  function addBubble(text, who) {
    const bubble = document.createElement('div');
    bubble.className = 'bubble ' + who;
    bubble.textContent = text;
    chat.appendChild(bubble);
    chat.scrollTop = chat.scrollHeight;
  }
  function speak(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'en-IN';
    speech.rate = 0.95;
    window.speechSynthesis.speak(speech);
  }
  document.getElementById('form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) { input.focus(); return; }
    addBubble(message, 'user');
    input.value = '';
    try {
      const response = await fetch('/reply', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message})
      });
      const data = await response.json();
      addBubble(data.reply, 'bot');
      speak(data.reply);
    } catch (error) {
      addBubble('Sorry, I could not connect. Please try again.', 'bot');
    }
  });
  micButton.addEventListener('click', () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      hint.textContent = 'Voice typing is not available in this browser. Please type your message instead.';
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    micButton.disabled = true;
    let recognitionFailed = false;
    hint.textContent = 'Starting microphone…';
    recognition.onstart = () => {
      hint.textContent = 'Listening now — speak a short phrase.';
    };
    recognition.onend = () => {
      micButton.disabled = false;
      if (!recognitionFailed) {
        hint.textContent = 'Try: “hello”, “good night”, “my name is Sam”, or “what is my name?”';
      }
    };
    recognition.onresult = (event) => {
      input.value = event.results[0][0].transcript;
      document.getElementById('form').requestSubmit();
    };
    recognition.onerror = (event) => {
      recognitionFailed = true;
      const messages = {
        'not-allowed': 'Please allow microphone access in your browser settings, then try again.',
        'service-not-allowed': 'This browser is blocking speech recognition. Please type your message.',
        'no-speech': 'I did not hear speech. Tap the microphone and speak clearly, or type your message.',
        'network': 'This browser cannot reach its speech service. Use your keyboard microphone: tap the message box, tap the keyboard mic, speak, then tap Send.',
        'language-not-supported': 'This browser does not support English (India) speech recognition. I will try English (US).'
      };
      hint.textContent = messages[event.error] || 'I could not use the microphone. Please try again or type your message.';
      if (event.error === 'network') input.focus();
      if (event.error === 'language-not-supported') {
        recognition.lang = 'en-US';
        recognitionFailed = false;
        setTimeout(() => {
          try { recognition.start(); }
          catch (error) { hint.textContent = 'Speech recognition could not restart. Please type your message.'; }
        }, 300);
      }
    };
    try {
      recognition.start();
    } catch (error) {
      micButton.disabled = false;
      hint.textContent = 'The microphone could not start. Please try again or type your message.';
    }
  });
</script>
</body>
</html>'''


@app.get("/")
def home():
    return render_template_string(PAGE)


@app.post("/reply")
def get_reply():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify(reply="Please type a message first."), 400
    return jsonify(reply=reply_to(message))


if __name__ == "__main__":
    # This lets another device on the same Wi-Fi open the app.
    app.run(host="0.0.0.0", port=5000, debug=False)
