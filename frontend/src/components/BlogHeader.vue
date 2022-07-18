<template>
  <div id="header">
    <div class="grid">
      <div></div>
      <h1>My Drf-Vue Blog</h1>
      <SearchButton />
    </div>
    <hr>
    <div class="login">
      <div v-if="hasLogin">
        <div class="dropdown">
          <button class="dropbtn">欢迎，{{ username }}！</button>
          <div class="dropdown-content">
            <router-link :to="{ name: 'UserCenter', params: { username: username } }">用户中心</router-link>
            <router-link :to="{ name: 'Home' }" v-on:click.prevent="logout()">注销登录</router-link>
          </div>
        </div>

      </div>
      <div v-else>
        <router-link :to="{ name: 'Login' }" class="login-link">登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>

import SearchButton from '@/components/SearchButton.vue';
import authorization from '@/utils/authorization';

export default {
  name: 'BlogHeader',
  components: { SearchButton },
  // props: ['welcomeName'], // 由于HTML对大小写不敏感，所以Vue规定camelCase的prop名需要使用其等价的kebab-case命名
  // props: {
  //   wname: String
  // },
  // computed属性是基于它们的响应式依赖进行缓存的，只在相关参数发生变化时才重新计算，并且默认不接受参数，并且不能产生副作用，即不能改变任何Vue所管理的数据。
  // computed: {
  //   name () {
  //     console.log(this.welcomeName)
  //     return (this.welcomeName !== undefined) ? this.welcomeName : this.username
  //   }
  // },
  data: function () {
    return {
      username: '',
      hasLogin: false
    }
  },
  // mounted中干了三件事：检查localStorage中保存的令牌是否过期，如果未过期则保持登录状态，如果已经过期，
  // 则检查是否有刷新令牌，如果有，则保持登录状态，同时更新令牌和过期时间
  // 其他任何情况均认为用户未登录，并清空localStorage
  mounted () {
    // 将身份验证模块抽出变成一个authorization函数了
    authorization().then((data) => [this.hasLogin, this.username] = data)
  },
  methods: {
    logout: function () {
      this.hasLogin = false;
      localStorage.clear();
      if (this.$route.name == "Home") { // 如果当前页面是首页，才要刷新，否则不用刷新，因为router-link已经跳转到首页去了，如果再刷新则又回到了前一级页面
        window.location.reload(false)
      }
    },
    refresh () {
      this.username = localStorage.getItem('username.myblog')
    }
  }
}
</script>

<style scoped>
/* 样式来源: https://www.runoob.com/css/css-dropdowns.html* /
    /* 下拉按钮样式 */
.dropbtn {
  background-color: mediumslateblue;
  color: white;
  padding: 8px 8px 30px 8px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  height: 16px;
  border-radius: 5px;
}

/* 容器 <div> - 需要定位下拉内容 */
.dropdown {
  position: relative;
  display: inline-block;
}

/* 下拉内容 (默认隐藏) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 120px;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* 下拉菜单的链接 */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* 鼠标移上去后修改下拉菜单链接颜色 */
.dropdown-content a:hover {
  background-color: #f1f1f1
}

/* 在鼠标移上去后显示下拉菜单 */
.dropdown:hover .dropdown-content {
  display: block;
}

/* 当下拉内容显示后修改下拉按钮的背景颜色 */
.dropdown:hover .dropbtn {
  background-color: darkslateblue;
}
</style>

<style scoped>
.login-link {
  color: black;
}

.login {
  text-align: right;
  padding-right: 5px;
}

#header {
  text-align: center;
  margin-top: 20px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
}
</style>
