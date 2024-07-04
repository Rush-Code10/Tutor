css = '''

<style>
.chat-message {
    padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #262730
}
.chat-message.bot {
    background-color: #262730
}
.chat-message .avatar {
  width: 5%;
}
.chat-message .avatar img {
  max-width: 45px;
  max-height: 45px;
  border-radius: 20%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.imgur.com/ZyDFqUX.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.imgur.com/TphPURw.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''