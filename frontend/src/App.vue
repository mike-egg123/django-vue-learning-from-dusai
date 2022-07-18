<!-- 真正写前端页面跳转逻辑以及接口调用的地方 -->
<template>
  <!-- 各路径所代表的页面的实际渲染位置 -->
  <router-view />
</template>

<script>
export default {
  name: "App",
}
</script>

<style>
#app {
  font-family: Georgia, Arial, sans-serif;
  margin-left: 40px;
  margin-right: 40px;
}
</style>
