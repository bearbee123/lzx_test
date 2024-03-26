<template>
	<div class="main">
		<Left />
		<div class="chat">
			<Chat />
		</div>
		<div class="case">
			<Case />
			<div class="fbx"><Fbx /></div>
		</div>
	</div>
</template>

<script>
import Left from"./left.vue"
import Chat from "./chat.vue";
import Case from "./case.vue";
import Fbx from "./fbxDemo.vue";
//创建全局总事件
import Vue from 'vue';

export const EventBus = new Vue();
export default {
	name: "Main",

	components: {
		Chat,
		Case,
		Fbx,
		Left,
	},
	
};

</script>

<style scoped>
.main {
	padding: 0px;
	margin: 0px;
	display: flex;
}

.chat {
	height: 100vh;
	margin-left: 10px;
	width: 1250px;
	background-color: #ffffff;
}
.case {
	margin-left: 20px;
	/* 修改一下 */
	height: 100vh;
	/* width: 400px; */
	flex-direction: column;
	display: flex;

}
.content {
	height: 90vh;
}
.chatBox {
	resize: none;
	width: 100%;
	height: 100px;
	display: flex;
}
.fbx{
	flex: 1;
}
</style>
