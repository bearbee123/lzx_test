<template>
  <div class="leftHistory">
    <div class="leftTitle">HQU智能问答</div>
    <div class="addNewChat"@click="addnewchat_all">
      <span class="addNewChat_w">新 的 聊 天</span>
      <img class="addIcon"src="@/imgs/增加.png" alt="Add New">
    </div>
    <hr></hr>
      <div class="leftMain">
        <div v-if="showLeftTitle" class="leftTitleText">这是左边的聊天记录</div>
        <div v-for="(item, index) in mesList" :key="index" class="leftmessage"@mouseover="handleMouseOver" @mouseleave="handleMouseLeave"@click="clickMessage(item)">
          <span class="messageText">{{ item.message }}</span>
          <div>
          <img class="closeIcon" src="@/imgs/关闭.png" @click="allclearAllMessages(index,item)"  alt="Close Icon">
        </div>
          <div>
            <span class="timestamp">{{ item.talk_time }}</span> <!-- 显示时间戳 -->
          </div>
        </div>
      </div>
  </div>
</template>
  <script>
  import { EventBus } from "./main.vue"
  export default {
  data() {
    return {
      mesList: [], // 聊天记录列表
      clickCount: 0, // 点击次数
      showLeftTitle: true, // 是否显示左边的聊天记录标题
      usr_url:this.$route.path,
      is_newchat:false,//用于判断是否是只有一个的新对话
      talk_id:0//用于接收点击
    };
  },
  //获取传过来的数据
  props:{
    type:Array,
    default:function(){
    }
  },
  async created() {
    //获取页面url
    //用来加载页面是获取数据库内容，同步数据展示，其中包含对相同talk_id只取其中第一个的原则
    this.$store.dispatch("fetchMineBaseMsg","http://localhost:8000/user/by_username"+this.usr_url).then(() => {
    const get_data = this.$store.state.all_data;
    const talkIdSet = new Set(); // 存储已存在的talk_id
    const melist = get_data.reduce((acc, item) => {
      const talkId = item.talk_id;
      if (!talkIdSet.has(talkId)) {
        talkIdSet.add(talkId);
        acc.push({
          talk_id: talkId,
          talk_time: item.talk_time,
          message: item.message
        });
      }
      return acc;
    }, []);
    this.mesList=melist
      }
    )
  },
 
  methods: {
    //对于新的历史聊天记录使用两个方法累加
    addnewchat_all(){
      this.addNewChat()
      // this.addNewchat_chat()
    },

    addNewChat() {
      //先进行新会话查询功能
      //如果stroe中state为空
      if(typeof this.$store.state.all_data ==='undefined')
      {this.is_newchat=true} else {
        const latestData = this.$store.state.all_data[this.$store.state.all_data.length - 1];
        console.log(latestData)
        if (latestData.question=== " " && latestData.answer=== " ") {
            // 如果最新数据中的questions或answer为空白，则直接结束addnewchat
            alert("请在该对话中询问");
            this.is_newchat=false
            return;
      } else  {
        this.is_newchat=true
        }
     }
      console.log(this.$store.state.all_data)
      this.clickCount++;
      if (this.clickCount === 1) {
        this.showLeftTitle = false; // 第一次点击后隐藏左边的聊天记录标题
      }
      const currentTime = new Date().toLocaleTimeString(); // 获取当前时间
      const currentyear=new Date().toLocaleDateString()
      const currentalltime=currentyear+" "+currentTime
      
      // 将 talk_id 赋值给一个变量,都从数据仓库里面拿取保持数据的统一
      const talkId = this.$store.state.talk_id+1;
      console.log(this.mesList)
      this.mesList.push({ message: `这是第${this.clickCount}次点击`,talk_time: currentalltime,talk_id:talkId});
      //将改点击传入后端，同时涉及刷新页面和传入数据
      //获取id
      const user_name=this.usr_url.replace("/","")
      console.log(this.$store.state.user_id)
      const new_chat_data={
        "user_id": this.$store.state.user_id+1,
				"user_name": user_name,
        "talk_id":this.$store.state.talk_id+1,
				"talk_time":currentalltime,
				"question": " ",
				"answer": " ",
        "message":" "
      }

      //同步store数据和传入后端的数据
      if(typeof this.$store.state.all_data ==='undefined'){
        this.$store.state.all_data=new_chat_data
      }else{
        this.$store.state.all_data.push(new_chat_data)
      }

      this.$store.dispatch("addMineBaseMsg",new_chat_data)
      console.log(this.$store.state.all_data)
      //每次创建会传递talk_id,和时间
      EventBus.$emit("leftMessageClicked",talkId)
      EventBus.$emit("gettalktime",currentalltime)
    },

    //以下是一些对leftmessage的一些方法
    //单击leftmessage获取talk_id，传递它，然后在chat组件中重新获取数据
    clickMessage(item) {
      // 从点击的项中获取talk_id
      const talkId = item.talk_id;
      this.talk_id=talkId
      console.log(this.talk_id)
      // 使用EventBus传递talk_id
      EventBus.$emit('leftMessageClicked', talkId);

    },

     // 点击聊天记录按钮关闭，清除消息用于单个删除页面聊天记录（设计后端的一个接口问题）,需要两个方法同时使用，为的是拿到talk_id且
     //同时清除消息
     allclearAllMessages(index,item){
      this.clickMessage(item)
      this.clearAllMessages(index)
     },
     clearAllMessages(index) { 
      EventBus.$emit('clearMessagesEvent');
      this.removeChat(index)
      //向后端接口传递数据
      this.$store.dispatch("deleteMineBaseMsg","http://localhost:8000/user/delete_by_username_talk_id"+this.usr_url+"/"+this.talk_id)
    // console.log("http://localhost:8000/user/delete_by_username_talk_id"+this.usr_url+"/"+this.talk_id)
    },
    removeChat(index) {
      // 检查是否所有 leftmessage 都被删除
      this.mesList.splice(index, 1);

      if (this.mesList.length === 0) {
          this.resetChat();
      }
    },
    resetChat() {
    const currentTime = new Date().toLocaleTimeString();
    const currentyear = new Date().toLocaleDateString();
    const currentalltime = currentyear + " " + currentTime;
    this.mesList.push({ message: `这是一个新的聊天`, timestamp: currentalltime });
      },
    
    //对于新聊天的一个只需要传递消息删除信息即可
    // addNewchat_chat(){
    //   EventBus.$emit('clearMessagesEvent');
    // }, 
    
    //leftmessage的动态效果
    handleMouseOver(event) {
      event.currentTarget.classList.add('hoverEffect');
    },

    handleMouseLeave(event) {
      event.currentTarget.classList.remove('hoverEffect');
    },

    
  },
};

  </script>
  
  <style scoped>
  @font-face {
    font-family: "阿里妈妈方圆体 VF Regular";
    src: url("//at.alicdn.com/wf/webfont/XchthrKyhDcE/rU1PHcs8g9xN.woff2") format("woff2"),
    url("//at.alicdn.com/wf/webfont/XchthrKyhDcE/OGx74Wkm7Qxx.woff") format("woff");
    font-display: swap;
    }
    @font-face {
  font-family: "阿里妈妈东方大楷 Regular";src: url("//at.alicdn.com/wf/webfont/XchthrKyhDcE/So7MvjL2GPDI.woff2") format("woff2"),
  url("//at.alicdn.com/wf/webfont/XchthrKyhDcE/BPZV9lL8T5zm.woff") format("woff");
  font-display: swap;
}
  .leftHistory {
    background-color: rgb(26, 34, 70);
    height: 100vh;
    width: 260px;
    color: white;
  }
  
  .leftTitle {
    height: 40px;
    line-height: 40px;
    text-align: center;
    font-family: "阿里妈妈东方大楷 Regular", Arial, sans-serif;
    font-weight: 500;
    font-size: 30px;
    margin-bottom: 20px;
  }
  .addNewChat{
    width: 80%;
    height: 50px;
    margin-left:9% ;
    margin-bottom: 20px;
    border-radius: 10px;
    background-color: rgb(47, 62, 126);
    border: 3px solid transparent;
    border-color: white;
    cursor: pointer;
    position: relative;
  }
  .addNewChat_w{
    margin-left: 28%;
    margin-top: 50px;
    font-family: "阿里妈妈方圆体 VF Regular", Arial, sans-serif;
    font-weight: 800;
  }
  .addNewChat:hover{
    background-color: rgb(57, 74, 151);
  }
  .addIcon{
    width: 20px; /* 设置容器宽度 */
  height: 20px; /* 设置容器高度 */
  position: absolute;
  top:50%;
  left: 45%;
  }
  .leftMain {
    margin: 10px;
    font-family: "阿里妈妈方圆体 VF Regular", Arial, sans-serif;
  }
  .leftmessage {
    height: 50px;
    margin-bottom: 10px;
    /* 调整字体 */
    padding-left: 20px;
    padding-top: 20px;
    font-weight: 540;
    background-color: rgb(47, 62, 126);
    border-radius: 10px; /* 圆润的边框 */
    border: 3px solid transparent; 
    transition: transform 0.3s,border-color 0.3s; /* 添加过渡效果 */
    position: relative;
}
.leftmessage:hover {
  border-color: white; /* 鼠标悬停时边框颜色变为白色 */
  background-color: rgb(57, 74, 151);
}

.hoverEffect {
  transform: translateY(5px); /* 下沉效果 */
}
.closeIcon {
  width: 17px; /* 设置容器宽度 */
  height: 17px; /* 设置容器高度 */
  position: absolute;
  top: 4px;
  right: 4px;
  cursor: pointer; /* 鼠标移上去显示手型 */
  opacity: 0; /* 初始状态下隐藏 */
  transition: opacity 0.3s; /* 添加过渡效果 */
}
.leftmessage:hover .closeIcon {
  opacity: 1; /* 鼠标悬停时显示关闭图标 */
}
.closeIcon:hover {
  filter: brightness(0.8); /* 鼠标悬停时降低亮度 */
}
/* 时间设置 */
.timestamp{
  position: absolute;
  top: 70%;
  right: 2px;
}
  </style>
  