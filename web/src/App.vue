<template>
  <div id="app">
    <v-app
        style="background-image: linear-gradient(to right top, #d16ba5, #c777b9, #ba83ca, #aa8fd8, #9a9ae1, #8aa7ec, #79b3f4, #69bff8, #52cffe, #41dfff, #46eefa, #5ffbf1);"
    >
      <v-app-bar elevation="0" class="g-glossy">
        <v-app-bar-nav-icon>
          <v-img :src="logo" width="36"></v-img>
        </v-app-bar-nav-icon>
        <div class="ml-4">
          <div class="text-body-1 font-weight-black">
            VATECH E-GAME
          </div>
          <div class="text-caption mt-n1">
            Build Your Team(BYT)
          </div>
        </div>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-magnify"></v-btn>
        <v-btn icon="mdi-theme-light-dark"></v-btn>
      </v-app-bar>
      <v-main>
        <router-view></router-view> <!-- 显示路由组件 -->
      </v-main>
    </v-app>

  </div>
</template>

<script setup>
import logo from './assets/role-model.png'
</script>

<style>
/* 设置全局样式，包括暗色调的背景 */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url('assets/background/app-egame.png') no-repeat center center fixed;
  background-size: cover; /* 确保背景图片覆盖整个视窗 */
}

.g-glossy {
  background-color: rgba(255, 255, 255, 0.5) !important;
  backdrop-filter: blur(10px);
}

</style>
