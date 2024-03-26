import Vue from 'vue'
import Vuex from 'vuex'
//持久化

import api from "../fetch/api"
Vue.use(Vuex);

const actions={
    //拿取数据
    async fetchMineBaseMsg({ commit },url) {
        try {
          console.log(url)
          const data = await api.mineBaseMsgApi(url);
          //将用户数据传入
          commit("add_data",data.data)
        } catch (error) {
          console.error(error);
        }
      },
    //写入数据
    async addMineBaseMsg({commit},data){
      try{
        const send_data= await api.mineBaseMsgApiSend(data)
        if(data.question==" "&&data.answer==" "){
          commit("updataall_id")
        }
        else{commit("updatauser_id")}
      }catch (error) {
        console.error(error);
      }
    },
    //按talk_id删除数据
    async deleteMineBaseMsg({commit},url){
      try{
        console.log("已调用")
        const deletdata= await api.mineBaseMsgApidelete(url)
        commit("deletetalk_id_all",deletdata)
      }catch(error){
        console.error(error)
      }
    },
    //按question精准删除数据
    async deleteMineBaseMsgQue({commit},url){
      try{
        console.log("已调用!!!!")
        const deletdata_que=await api.mineBaseMsgApidelete(url)
        commit("deletequestion",deletdata_que)
      }catch(error){
        console.error(error)
      }
    }
}
const mutations={
  add_data(state,data){
    state.all_data=data
    //直接拿取数据库传来数据的id,保持最新的user_id和talk_id
    state.user_id=data[data.length-1].userid
    state.talk_id=data[data.length-1].talk_id
   
  },
  //分类更新user_id和talk_id
  updataall_id(state){
    state.user_id=state.user_id+1
    state.talk_id=state.talk_id+1
  },
  updatauser_id(state){
    state.user_id=state.user_id+1
    // state.talk_id=state.talk_id+1
  },
  //按talk_id删除
  deletetalk_id_all(state,deletdata){
    state.talk_id=state.talk_id-1
    state.all_data=state.all_data.filter(item=>{
      return !deletdata.find(deletdata=>deletdata.talk_id===item.talk_id && deletdata.userid===item.userid)
    })
  },
  //按question删除
  deletequestion(state,deletdata_que){
    state.all_data=state.all_data.filter(item=>{
      return !deletdata_que.find(deletdata_que=>deletdata_que.talk_id===item.talk_id && deletdata_que.question===item.question)
    })
  }
}
const state={
   all_data:[],
   user_id:0,
   //每个用户的talk_id也要从最新的开始
   talk_id:0
}


export default new Vuex.Store({
actions,
mutations,
state,
// vuexLocal
});