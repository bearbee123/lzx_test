import axios from "axios";
//获取数据
export function fetch(url) {
    return new Promise((resolve, reject) => {
        axios.get(url)
            .then(response => {
                //  alert('Api--ok');
                resolve(response.data);
            })
            .catch((error) => {
              console.log(error)
               reject(error)
            })
    })
}
//传递数据
export function sendData(data,url) {
  return new Promise((resolve, reject) => {
      axios.post(url,data)
          .then(response => {
              //  alert('Api--ok');
              resolve(response.data);
          })
          .catch((error) => {
            console.log(error)
             reject(error)
          })
  })
}
//删除数据
export function deleteData(url){
  return new Promise((resolve,reject)=>{
    axios.delete(url)
      .then(response=>{
        if (response.code === "0000") {
          resolve("成功删除所有匹配用户");
      } else if (response.code === "0001") {
          resolve("未找到匹配的用户");
      } else if(response.code==="0002") {
          reject("删除用户时出现异常");
      }
      })
      .catch(error => {
        reject(error);
         });
  })
}
export default {
    // 获取我的页面的后台数据
    mineBaseMsgApi(url) {
      return fetch(url);
    },
    //传递我页面的数据向后端
    mineBaseMsgApiSend(data,url="http://localhost:8000/user/addUser"){
      return sendData(data,url)
    },
    //删除数据
    mineBaseMsgApidelete(url){
      return deleteData(url)
    }
  }