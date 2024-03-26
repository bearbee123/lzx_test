<template>
	<div id="chat-container">
		<div id="chat-messages" ref="chatMessages">
			<div v-for="(item, index) in messages" :key="index">
				<div class="userChat">
					<img src="@/imgs/人头像.jpg" class="chatImg" />
					<span>{{ item.question }}</span>
					<div class="userChat_box">
					</div>
				</div>
				<br />
				<br />
				<div class="botChat">
					<img src="@/imgs/机器人.png" class="chatImg" />
					<div class="botMessagebox">
					<span class="botMessage"> {{ item.answer }}</span>
					</div>
					<div class="botChatimg_box">
						<img src="@/imgs/删除.png" class="botChat_del"@click="handleBotChatDel(index)">
						<img src="@/imgs/复制.png" class="botChat_cop"@click="handleCopy(item.answer)">
					</div>
				</div>
				<br />
			</div>
		</div>
		<div id="user-input">
			<input
				type="text"
				v-model="newMessage"
				id="message-input"
				placeholder="Type your message..."
			/>
			<button id="send-button" @click="sendMessage">Send</button>
		</div>
		<div id="timer">{{ timer }}</div> <!-- 计时器元素 -->
	</div>
</template>

<script>
import{EventBus} from"./main.vue"
export default {
	
	data() {
		return {
			messages: [],
			newMessage: "",
			timer: 0, // 计时器变量
			talk_id:0,
			usr_url:this.$route.path,
			talk_time:""
		};
	},
	created(){
		console.log(this.talk_id)
		EventBus.$on('clearMessagesEvent',()=>{
			this.clearMessages();
			this.timer=3
		}),

		EventBus.$on('gettalktime', (talk_time) => {
		// 处理接收到的 talk_time
		console.log(`Received talk_id: ${talk_time}`);
		this.talk_time= talk_time;
		});
		//同步数据,展示最近的聊天记录根据talk_id
		this.presentMessage()
		//接收left组件传递过来的信息
		EventBus.$on("leftMessageClicked",(talk_id)=>{
			this.presentMessage(talk_id)
			this.talk_id=talk_id
			console.log(this.talk_id)
		})
		
	},
	mounted(){
	},
	methods: {
		//构建现存message
		presentMessage(talk_id){
		this.$store.dispatch("fetchMineBaseMsg","http://localhost:8000/user/by_username"+this.usr_url).then(() => {
		const get_data = this.$store.state.all_data;
		//如果有talk_id传入则表明需要切换了，如果没有则表示初始化
		// const latestTalkId=get_data[get_data.length-1].talk_id
		//每次可以去访问最新一次的对话因为talk_id我们会去那最新的，有种保持继续聊天的感觉
		const latestTalkId = talk_id ? talk_id : get_data[get_data.length - 1].talk_id;
		// 根据latestTalkId获取相同talk_id的数据，并去除question和answer的值为空格的数据
			const latestTalkData = get_data.filter(item => {
				const isQuestionEmpty = !item.question || item.question.trim() === '';
				const isAnswerEmpty = !item.answer || item.answer.trim() === '';
				return item.talk_id === latestTalkId && !isQuestionEmpty && !isAnswerEmpty;
			});

			this.messages = latestTalkData.map(item => {
					return {
						question: item.question,
						answer: item.answer
					};
					});
		})
		},
		async sendMessage() {
		//先建立对话聊天
		if(typeof this.$store.state.all_data ==='undefined'){
			// this.$store.state.all_data=new_chat_data
			alert("请先建立聊天对话")
			return
		}

		this.timer=0
		this.id=this.id+1
    	const questionText = "asdjklzxcjkl";
    	const answerText = "This is the response message.This is the response message.This is the response message.";
    	let newItem = {
    		question: questionText,
    		answer: "",
    		};
    	EventBus.$emit("timerValue",this.timer)
		// console.log(this.talk_id)
    	this.messages.push(newItem);
		this.timer=1
    	const typeText = async (text, index, target) => {
       		if (index < text.length) {
				//用来判断是否打断对话和动作，timer==3即有动作打断
				if(this.timer!=3){
					target += text[index];
					newItem.answer = target; // 更新回答消息
					await new Promise(resolve => setTimeout(resolve, 10)); // 等待100毫秒
					await typeText(text, index + 1, target);}
			else if(this.timer==3){return;}
        	}
    	};
    	await typeText(answerText, 0, "");

		// 拿取messages的长度，取最后一个创建新数据
		const len_messages=this.messages.length
		console.log(this.messages[len_messages-1])
		this.sendDatatoMysql(this.messages[len_messages-1].question,this.messages[len_messages-1].answer)
		this.timer = 2;
		EventBus.$emit("timerValue", this.timer);
      	this.$nextTick(() => {
        this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
      	});
      
    	this.newMessage = "";
    	},

		//以下是清除的操作

   		clearMessages() {
			// 清除消息所呈现的 <div> 元素
			this.$refs.chatMessages.innerHTML = '';
			// 清空消息数组
			this.messages = [];
			this.$store.state.talk_id=this.$store.state.talk_id-1
    	},
		handleBotChatDel(index) {
      	// this.timer = 3;
		  const deletedata=this.messages[index]
		  const del_question=deletedata.question
		  this.messages.splice(index, 1);
		  console.log(this.$store.state.talk_id)
		  let realtalk_id=0
		  if(this.talk_id==0){
				realtalk_id=this.$store.state.talk_id
			}
			else{
				realtalk_id=this.talk_id
			}
		  console.log(realtalk_id)
		  console.log("http://localhost:8000/user/delete_by_username_talk_id_question"+this.usr_url+"/"+realtalk_id+"/"+del_question)
		  this.$store.dispatch("deleteMineBaseMsgQue","http://localhost:8000/user/delete_by_username_talk_id_question"+this.usr_url+"/"+realtalk_id+"/"+del_question)
		  console.log(del_question)
    	},
		//以下是复制的操作
		handleCopy(text) {
		navigator.clipboard.writeText(text)
			.then(() => {
			console.log('成功复制: ' + text);
			})
			.catch(err => {
			console.error('复制失败: ', err);
			});
		},
			// 传递数据
		async sendDatatoMysql(question,answer){
			const user_name=this.usr_url.replace("/","")
			let realtalk_id=0
			//这个判断是为了页面刚开始设计的，能让新建对话继续按照最新的来
			if(this.talk_id==0){
				realtalk_id=this.$store.state.talk_id
			}
			else{
				realtalk_id=this.talk_id
			}
			
			const new_chat_data={
				"user_id": this.$store.state.user_id+1,
				"user_name": user_name,
				"talk_id": realtalk_id,
				"talk_time":this.talk_time,
				"question": question,
				"answer": answer,
				"message":" "
			}
			
			//聊天记录存入store并且同步数据

			this.$store.state.all_data.push(new_chat_data)
			//向后端发送数据
			try{
				this.$store.dispatch("addMineBaseMsg",new_chat_data)
			}catch(error){
				console.error('Error sending data to backend:', error);
			}
		}
			
	},

};
</script>

<style scoped>
.userChat {
	display: flex;
	width: 100%;
	height: 40px;
}

.userChat span {
	background-color: rgb(210, 249, 209);
	height: 100%;
	line-height: 30px;
	border-radius: 0.375rem;
	padding: 5px;
}

.botChat {
	position: relative;
	display: flex;
	height: auto; 
    width: 100%; /* 设置消息框的宽度 */
    transition: height 0.3s; /* 添加过渡效果 */
	
    
}
.botChat.expanded {
    height: auto; /* 当内容超出高度时展开 */
}
.botMessagebox{
	width: 90%;
	background-color: rgb(244, 246, 248);
	padding: 20px; 
}
.botChat span {
	display: inline-block;
    background-color: rgb(244, 246, 248);
	width: 90%;
    line-height: 1.5; /* 设置行高，可根据需要调整 */
    border-radius: 0.375rem;
    padding: 35px;
    word-wrap: break-word; /* 当单词长度超过容器宽度时自动换行 */
    overflow-wrap: break-word; /* 支持非IE浏览器的自动换行 */
}
.botChatimg_box{
	position: absolute;
	width: 100px;
	bottom: 10px;
    right: 20px;
}

.botChat_del{
  width: 20px; 
  height: 20px; /* 设置容器高度 */
  padding-left: 10px;
  padding-right: 20px;
  cursor: pointer; /* 鼠标移上去显示手型 */
  
}

.botChat_cop{
width: 20px; /* 设置容器宽度 */
height: 20px; /* 设置容器高度 */
cursor: pointer; 
}
.chatImg {
	width: 30px;
	height: 30px;
	padding-right: 10px;
}
#chat-container {
	max-width: 100%;
	height: 100vh;
	margin: 0px auto;
	border: 1px solid #ccc;
	border-radius: 5px;
	overflow: hidden;
}

#chat-messages {
	height: 90%; /* Set a fixed height */
	padding: 10px;
	overflow-y: scroll;
}

.user-message {
	text-align: right;
}

#user-input {
	padding: 10px;
	border-top: 1px solid #ccc;
	display: flex;
}

#message-input {
	flex: 1;
	padding: 20px;
}

#send-button {
	padding: 5px 10px;
	background-color: #4caf50;
	color: white;
	border: none;
	border-radius: 3px;
	cursor: pointer;
}
#timer {
    display: none;
}
</style>
