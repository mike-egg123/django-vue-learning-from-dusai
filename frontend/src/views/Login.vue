<template>
  <BlogHeader />

  <div id="grid">
    <div id="signup">
      <h3>注册账号</h3>
      <form>
        <div class="form-elem">
          <span>账&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号：</span>
          <input v-model="signupName" type="text" placeholder="输入用户名">
        </div>
        <div class="form-elem">
          <span>密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码：</span>
          <input v-model="signupPwd1" type="password" placeholder="输入密码">
        </div>
        <div class="form-elem">
          <span>确认密码：</span>
          <input v-model="signupPwd2" type="password" placeholder="请再次输入密码">
        </div>
        <div class="form-elem">
          <button v-on:click.prevent="signup">提交</button>
        </div>
      </form>
    </div>

    <div id="signin">
      <h3>登录账号</h3>
      <form>
        <div class="form-elem">
          <span>账&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号：</span>
          <input v-model="signinName" type="text" placeholder="输入用户名">
        </div>
        <div class="form-elem">
          <span>密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码：</span>
          <input v-model="signinPwd" type="password" placeholder="输入密码">
        </div>
        <div class="form-elem">
          <button v-on:click.prevent="signin">登录</button>
        </div>
      </form>
    </div>
  </div>

  <BlogFooter />

</template>

<script>
import axios from 'axios';
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';

export default {
  name: 'Login',
  components: { BlogHeader, BlogFooter },
  data: function () {
    return {
      signupName: '',
      signupPwd1: '',
      signupPwd2: '',
      signinName: '',
      signinPwd: '',
      signupResponse: null,
    }
  },
  methods: {
    signup () {
      const that = this;
      if (this.signupPwd1 !== this.signupPwd2) {
        alert("两次密码不一致，请重新输入！")
        return
      }
      axios.post('/api/user/', {
        username: this.signupName,
        password: this.signupPwd1
      })
        .then(function (response) {
          that.signupResponse = response.data; // 这里如果是this，则会找不到实例，原因是这是一个普通的函数，获取的实例是axios，而之前ArticleList.vue中的this则位于箭头函数中，可以自动获取外层的Vue对象
          alert('注册成功，快去登录吧！');
        })
        .catch(function () {
          alert("用户名已存在，请更换用户名并重试！");
        });
    },
    signin () {
      const that = this;
      axios.post('/api/token/', {
        username: this.signinName,
        password: this.signinPwd
      })
        .then(function (response) {
          const storage = localStorage;
          // Date.parse返回1970年1月1日UTC以来的毫秒数
          // Token被设置为1分钟，因此这里加上60000毫秒
          const expiredTime = Date.parse(response.headers.date) + 60000;
          // 设置localStorage
          storage.setItem('access.myblog', response.data.access);
          storage.setItem('refresh.myblog', response.data.refresh);
          storage.setItem('expiredTime.myblog', expiredTime);
          storage.setItem('username.myblog', that.signinName);
          // 登录成功后跳转到博客首页
          that.$router.push({name: 'Home'});
        })
        .catch(function () {
          alert("登录失败，请重试！");
        });
    }
  }
}
</script>

<style scoped>
#grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

#signup {
  text-align: center;
}

#signin {
  text-align: center;
}

.form-elem {
  padding: 10px;
}

input {
  height: 25px;
  padding-left: 10px;
}

button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: gray;
  color: whitesmoke;
  border-radius: 5px;
  width: 60px;
}
</style>