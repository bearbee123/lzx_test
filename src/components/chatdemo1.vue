<template>
	<div class="chat-container">
		<!-- 聊天标题栏 -->
		<div class="chat-header">
			<h3>New chat</h3>
		</div>

		<!-- 聊天消息窗口 -->
		<div class="chat-messages">
			<!-- 模拟的消息 -->
			<div class="message received">
				<span class="message-content">hello</span>
				<span class="message-timestamp">2023/3/20 23:30:19</span>
			</div>
			<div class="message sent">
				<span class="message-content">你好</span>
				<span class="message-timestamp">2023/3/20 23:30:24</span>
			</div>
			<!-- 可能需要根据实际情况动态渲染消息 -->
		</div>

		<!-- 消息输入区 -->
		<div class="chat-input">
			<input type="text" placeholder="Type a message..." />
			<button>Send</button>
		</div>
	</div>
</template>

<script>
export default {
	name: "ChatWindow",
	data() {
		return {
			// 组件的数据
		};
	},
};
</script>

<style scoped>
.chat-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	border: 1px solid #e0e0e0;
	background-color: #f9f9f9;
}

.chat-header {
	background-color: #f0f0f0;
	padding: 10px;
	border-bottom: 1px solid #e0e0e0;
}

.chat-messages {
	flex-grow: 1;
	padding: 10px;
	overflow-y: auto;
}

.message {
	margin-bottom: 10px;
	padding: 5px;
	background-color: white;
	border-radius: 5px;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}

.message.sent {
	align-self: flex-end;
	background-color: #dcf8c6;
}

.message.received {
	align-self: flex-start;
}

.message-content {
	margin: 0;
}

.message-timestamp {
	display: block;
	font-size: 0.75rem;
	color: #999;
	margin-top: 5px;
}

.chat-input {
	display: flex;
	padding: 10px;
	border-top: 1px solid #e0e0e0;
}

.chat-input input {
	flex-grow: 1;
	padding: 10px;
	border: 1px solid #e0e0e0;
	border-radius: 5px;
	margin-right: 10px;
}

.chat-input button {
	padding: 10px 15px;
	background-color: #0b93f6;
	border: none;
	border-radius: 5px;
	color: white;
	cursor: pointer;
}

.chat-input button:hover {
	background-color: #0a83d6;
}
</style>
