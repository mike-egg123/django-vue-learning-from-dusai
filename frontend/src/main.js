// 把后续的Vue组件挂载到index.html中
// 也可以将前端的初始化配置写到这里来
import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 导入路由router文件夹

// 通过原型链将自定义的appendIfExists方法加入到原生对象URLSearchParams中
URLSearchParams.prototype.appendIfExists = function (key, value) {
  if (value !== null && value !== undefined) {
    this.append(key, value)
  }
}
router.beforeEach((to, from, next) => {
  console.log(to.path)
  console.log(from.path)
  if (to.meta.requireAuth) {
    console.log(to.params.username)
    console.log(localStorage.getItem('username.myblog'))
    if (localStorage.getItem('access.myblog') && to.params.username === localStorage.getItem('username.myblog')) {
      next();
    } else if (to.params.username !== localStorage.getItem('username.myblog')) {
      alert('请不要尝试使用url访问其他用户资料！')
      next({
        path: from.path
      })
    }
    else {
      if (to.path === '/login') {
        next();
      }
      else {
        alert('请先登录！')
        next({
          path: '/login'
        })
      }
    }
  } else {
    next();
  }
})
createApp(App).use(router).mount('#app')
