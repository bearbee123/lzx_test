<template>
	<div id="example-box">
		<h3 class="caseTitle">示例</h3>
		<div
			v-for="(text, index) in exampleTexts"
			:key="index"
			class="example-text"
			@mouseover="changeColor(index)"
			@mouseout="resetColor(index)"
		>
			{{ text.text }}
		</div>
	</div>
</template>

<script>
export default {
	name: "CASE",
	data() {
		return {
			exampleTexts: [
				{ text: "1.图书馆如何上网" },
				{ text: "2.如何向图书馆捐赠图书" },
				{ text: "3.图书最多借多长时间" },
				{ text: "4.怎么申请活动场地" },
				{ text: "5.学校治安情况怎么样" },
				{ text: "6.如何查询教室监控" },
				{ text: "7.我们学校的食堂怎么样" },
				{ text: "8.学生缴费流程" },
			],
		};
	},
	components: {},
	methods: {
		changeColor(index) {
			this.$set(this.exampleTexts, index, {
				text: this.exampleTexts[index].text,
				backgroundColor: "#f00",
				color: "#fff",
			});
		},
		resetColor(index) {
			this.$set(this.exampleTexts, index, {
				text: this.exampleTexts[index].text,
				backgroundColor: "",
				color: "#333",
			});
		},
	},
};
</script>

<style scoped>
.caseTitle {
	padding-top: 10px;
	text-align: center;
}
#example-box {
	width: 300px;
	background-color: #d5dbdb;
}

.example-text {
	padding: 10px;
	color: black;
	cursor: pointer;
}

.example-text:hover {
	background-color: rgb(219, 234, 254);
	color: skyblue;
}
</style>
