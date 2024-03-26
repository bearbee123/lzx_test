<template>
	<div id="app">
		<nav>
		<router-link to="/lzx">asdsadsa</router-link>
		</nav>
		<router-view/>
	
	</div>
</template>

<script>

export default {
	name: "APP",
	mounted() {
    console.log(this.$route); // 在mounted钩子函数中访问路由参数
  },
};
</script>

<style>
* {
	margin: 0;
	padding: 0;
}
</style>
