// 存放路由相关的文件
import { createWebHistory, createRouter } from "vue-router";
import Home from "@/views/Home.vue";
import ArticleDetail from "@/views/ArticleDetail.vue";
import Login from "@/views/Login.vue";
import UserCenter from "@/views/UserCenter.vue";

// 列表routes定义了所有需要挂载到路由中的路径，成员为路径url、路径名河路径的vue对象
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/article/:id", // 动态路由
    name: "ArticleDetail",
    component: ArticleDetail
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/user/:username",
    name: "UserCenter",
    component: UserCenter,
    meta: { requireAuth: true }
  }
];

// 用createRouter函数创建路由
const router = createRouter({
  history: createWebHistory(), // HTML5模式，路径中没有丑陋的#符号
  routes
});

export default router;
