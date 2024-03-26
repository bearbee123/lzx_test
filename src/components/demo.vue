<template>
    <div id="chat-container">
      <div id="chat-messages" ref="chatMessages">
        <div v-for="message in messages" :key="message.id" :class="{ 'user-message': message.isUser, 'bot-message': !message.isUser }">
          <strong v-if="!message.isUser">{{ message.sender }}:</strong> {{ message.text }}
        </div>
      </div>
      <div id="user-input">
        <input type="text" v-model="newMessage" id="message-input" placeholder="Type your message...">
        <button id="send-button" @click="sendMessage">Send</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        messages: [],
        newMessage: ''
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim() === '') {
          return;
        }
  
        this.messages.push({
          id: Date.now(),
          sender: 'You',
          isUser: true,
          text: this.newMessage
        });
  
        // Simulate Bot's async reply with flowing messages
        this.simulateBotReply();
  
        this.newMessage = ''; // Clear the input field
      },
      simulateBotReply() {
        // Simulate Bot's async reply with flowing messages using setInterval
        const originalMessage = 'I got your message! Thank you.'; // Bot's reply
        let index = 0;
  
        const intervalId = setInterval(() => {
          if (index < originalMessage.length) {
            this.messages.push({
              id: Date.now(),
              sender: 'Bot',
              isUser: false,
              text: originalMessage.charAt(index)
            });
            index++;
  
            // Use $nextTick to ensure that the DOM has been updated
            this.$nextTick(() => {
              let chatMessages = this.$refs.chatMessages;
              chatMessages.scrollTop = chatMessages.scrollHeight;
            });
          } else {
            clearInterval(intervalId);
            // Use $nextTick to ensure that the DOM has been updated
            this.$nextTick(() => {
              let chatMessages = this.$refs.chatMessages;
              chatMessages.scrollTop = chatMessages.scrollHeight;
            });
          }
        }, 200);
      }
    }
  };
  </script>
  
  <style scoped>
  #chat-container {
    max-width: 400px;
    margin: 50px auto;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
  }
  
  #chat-messages {
    height: 200px; /* Set a fixed height */
    padding: 10px;
    overflow-y: scroll;
  }
  
  .user-message {
    text-align: right;
    background-color: #e0f7fa;
    margin-right: 10px;
  }
  
  .bot-message {
    text-align: left;
    background-color: #c8e6c9;
    margin-left: 10px;
  }
  
  #user-input {
    padding: 10px;
    border-top: 1px solid #ccc;
    display: flex;
  }
  
  #message-input {
    flex: 1;
    padding: 5px;
  }
  
  #send-button {
    padding: 5px 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  </style>
  