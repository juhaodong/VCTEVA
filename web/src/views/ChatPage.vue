<template>

  <v-container height="100%" fluid>

    <div>
      <div class="text-h1 font-weight-black mt-4">
        🚢 Chooooose your superhero
      </div>
      <div class="text-h5 font-weight-black mt-12">
        to build an awesome team 💪
      </div>
      <div class="mt-8">
        <div></div>
      </div>
    </div>
    <div style="display: grid;grid-template-columns: repeat(5,minmax(0,1fr));grid-gap: 12px">
      <template v-for="i in 5" :key="i">
        <v-card variant="flat" class="pa-4 g-glossy" width="100%" color="">
          <v-responsive :aspect-ratio="9/12">
            <div style="height: 100%;" class="d-flex flex-column justify-center text-center">
              <v-spacer></v-spacer>
              <div class="text-body-1">Waiting your summon...</div>
            </div>
          </v-responsive>
        </v-card>
      </template>
    </div>
    <div class="text-h4 mt-8 ">
      Write your <span class="font-weight-black">MAGIC</span> spell here!
    </div>
    <v-text-field
        color="black"
        density="default"
        style="border-bottom: 3px solid black" hide-details variant="plain" placeholder="I need an absolute dominator on the field"
        append-inner-icon="mdi-arrow-right"
    ></v-text-field>
    <!-- Chat Section -->
    <div style="position: fixed;bottom: 0;left: 0;right: 0;" class="rounded-t  elevation-4">
      <template v-if="!toolbarExpand">
        <div style="display: grid;grid-template-columns: repeat(2,minmax(0,1fr))">
          <div @click="showToolbar(0)" class="pa-6 bg-green-lighten-2 text-h4 font-weight-black d-flex align-center">
            🤖 AI Assistant
            <v-spacer></v-spacer>
            <v-icon>mdi-arrow-right</v-icon>
          </div>
          <div @click="showToolbar(1)" class="pa-6 bg-grey-lighten-5 text-h4 font-weight-black d-flex align-center">
            ⛹️ Player Base
            <v-spacer></v-spacer>
            <v-icon>mdi-arrow-right</v-icon>
          </div>
        </div>
      </template>
      <template v-else>
        <div
            :class="toolbarTab===0?'bg-green-lighten-5':'bg-grey-lighten-5'"
            class="d-flex flex-column"
            style="height: 60vh"
        >
          <template v-if="toolbarTab===0">
            <div class="pa-4 bg-green-lighten-2 text-h4 font-weight-black d-flex align-center">
              🤖 AI Assistant
              <v-spacer></v-spacer>
              <v-btn @click.stop="toolbarExpand=false" icon="mdi-close" variant="text"></v-btn>
            </div>
            <div>
              <div class="chat-history">
                <div v-for="(message, index) in messages" :key="index" :class="['message', messageClass(message.type)]">
                  <!-- Bot Avatar -->
                  <div class="message-avatar" v-if="message.type === 'bot'" style="margin-right: 10px;">
                    <img
                        src="./components/llama.png" alt="Bot Avatar" class="avatar" style="width: 35px; height: 35px;"
                    />
                  </div>

                  <!-- Message Bubble -->
                  <div class="message-bubble">
                    <!-- If the message contains markdown, render it with v-html -->
                    <p v-if="message.isMarkdown" v-html="message.text" class="bot-message"></p>
                    <!-- Otherwise, render it as plain text -->
                    <p v-else class="user-message">{{ message.text }}</p>
                  </div>

                  <!-- User Avatar -->
                  <div class="message-avatar" v-if="message.type === 'user'" style="margin-left: 10px;">
                    <v-icon size="35" color="black">mdi-account-circle</v-icon>
                  </div>

                </div>
                <!-- Loading Indicator -->
                <div v-if="isLoading" class="loading-indicator">
                  <div class="message-avatar" style="margin-right: 10px;">
                    <img
                        src="./components/llama.png" alt="Bot Avatar" class="avatar" style="width: 35px; height: 35px;"
                    />
                  </div>
                  <span>Loading</span><span class="loading-dots"></span>
                  <!--          <div class="spinner"></div>-->
                </div>
              </div>
            </div>
            <v-spacer></v-spacer>
            <div class="d-flex bg-green-lighten-2 pa-4">
              <v-text-field
                  hide-details
                  variant="outlined" rounded="xl" bg-color="white" @keydown.enter="sendMessage"
                  placeholder="Type your message..."
                  v-model="inputMessage"
                  class="mr-2"
                  append-inner-icon="mdi-send"
                  density="comfortable"
              ></v-text-field>
            </div>

          </template>
          <template v-else>
            <div @click="showToolbar(1)" class="pa-4 bg-grey-lighten-5 text-h4 font-weight-black d-flex align-center">
              ⛹️ Player Base
              <v-spacer></v-spacer>
              <v-btn @click.stop="toolbarExpand=false" icon="mdi-close" variant="text"></v-btn>
            </div>
            <v-card width="30%" class="px-6 py-4" :rounded="'xl'" elevation="4">
              <div class="player-list-header">
                <span>Players</span>
              </div>
              <!-- 搜索框：根据选手名字筛选 -->
              <v-text-field
                  v-model="searchQuery"
                  variant="outlined" prepend-inner-icon="mdi-magnify" density="comfortable"
                  placeholder="Search Players..."
              ></v-text-field>

              <select v-model="selectedRegion" class="custom-select">
                <option value="">All Regions</option>
                <option v-for="region in regions" :key="region" :value="region">
                  {{ region }}
                </option>
              </select>
              <!-- 这里添加VueVirtualScroller -->
              <RecycleScroller
                  class="scroller"
                  :items="filteredPlayers"
                  :item-size="120"
                  key-field="player_id"
                  v-slot="{ item }"
              >
                <div class="player-card">
                  <div class="player-info">
                    <div class="player-avatar" :style="{ backgroundColor: item.bgColor }">
                      {{ item.avatarInitials }}
                    </div>
                    <div>
                      <h3 class="player-name">{{ item.handle }} </h3>
                      <p class="player-score">{{ item.name }}</p>
                      <p class="player-score"> {{ item.region }}</p>
                    </div>
                  </div>
                  <v-bottom-sheet inset>
                    <template v-slot:activator="{ props }">
                      <div class="text-center">
                        <v-btn
                            class="select-button"
                            v-bind="props"
                            text="Select"
                            @click="addPlayerToTeam(item)"
                        ></v-btn>
                      </div>
                    </template>

                    <v-sheet>
                      <team-display
                          :average="average"
                          :team="selectedTeam"
                          @deletePlayer="deletePlayerFromTeam"
                          @show-champion="showModal"
                      />
                    </v-sheet>
                  </v-bottom-sheet>
                </div>
              </RecycleScroller>
            </v-card>
          </template>
        </div>

      </template>

    </div>


    <!-- Player List Section -->


    <TrophyModal
        v-if="championModal"
        :isVisible="championModal"
        @close="closeModal"
    />
  </v-container>
</template>
<script>
import TeamDisplay from "@/views/components/TeamDisplay.vue";
import {client} from "@gradio/client";
import global from "..//global.js";
import axios from 'axios';
import TrophyModal from "@/views/components/TrophyModal.vue";
import {marked} from 'marked';
import {RecycleScroller} from "vue3-virtual-scroller";

export default {
  components: {
    TrophyModal,
    TeamDisplay,
    RecycleScroller
  },
  computed: {
    filteredPlayers() {
      return this.availablePlayers.filter((player) => {
        const matchesName = player.name
            ? player.name.toLowerCase().includes(this.searchQuery.toLowerCase())
            : false;

        const matchesRegion =
            !this.selectedRegion || player.region === this.selectedRegion;

        return matchesName && matchesRegion;
      });
    },
  },
  async mounted() {
    try {
      const response = await axios.get(global.DATABASE_LINK + '/players');
      this.availablePlayers = response.data.map(player => {
        // 获取玩家名字的前两个字母，并将其转换为大写
        const initials = player.name
            ? player.name.split(' ').map(word => word.charAt(0).toUpperCase()).join('').slice(0, 2)
            : player.handle.charAt(0).toUpperCase();

        // 随机生成一个背景颜色
        const colors = ['#e57373', '#81c784', '#64b5f6', '#ffb74d', '#ba68c8'];
        const bgColor = colors[Math.floor(Math.random() * colors.length)];

        return {
          ...player,
          avatarInitials: initials,
          bgColor,
        };
      });

      console.log(this.availablePlayers); // 检查输出的内容是否正确
      const regionResponse = await axios.get(global.DATABASE_LINK + '/regions');
      const averageResponse = await axios.get(global.DATABASE_LINK + '/average');
      this.regions = regionResponse.data;
      this.average = averageResponse.data[0];
    } catch (error) {
      console.error('Error fetching data:', error);
    }


  },
  data() {
    return {
      toolbarExpand: false,
      toolbarTab: 0,
      isLoading: false,
      championModal: false,
      searchQuery: '',
      average: {},
      selectedRegion: '',
      regions: [],
      llmService: global.LLM_SERVICE_TPYE,
      selectedTeam: [],
      inputMessage: '',
      messages: [
        {type: 'bot', text: 'Yeah, it would help in forming a team!'},
      ],
      availablePlayers: [],
    };
  },
  methods: {
    showToolbar(tab) {
      this.toolbarExpand = true
      this.toolbarTab = tab
    },
    showModal() {
      this.championModal = true;
    },
    closeModal() {
      this.championModal = false;
    },
    addPlayerToTeam(player) {
      if (this.selectedTeam.length < 5 && !this.selectedTeam.includes(player)) {
        this.selectedTeam.push(player);
      }
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) return;
      this.messages.push({type: 'user', text: this.inputMessage});
      const message = this.inputMessage;
      this.inputMessage = '';
      this.isLoading = true;
      try {
        const app = await client(global.GRADIO_LOCAL_LINK);
        console.log('client config ok');
        const result = await app.predict("/chat", [message]);
        const botResponse = result.data[0];
        // Convert botResponse to markdown format using 'marked'
        const markdownResponse = marked(botResponse);

        this.messages.push({type: 'bot', text: markdownResponse, isMarkdown: true});
      } catch (error) {
        this.messages.push({type: 'bot', text: 'Sorry, I could not process your question at the moment.'});
        console.log(error);
      } finally {
        this.isLoading = false; // Reset loading state
      }
    },
    messageClass(type) {
      return type === 'user' ? 'user-message justify-end' : 'bot-message justify-start';
    },
    deletePlayerFromTeam(player) {
      const index = this.selectedTeam.indexOf(player);
      if (index > -1) { // 如果找到了该元素
        this.selectedTeam.splice(index, 1); // 删除元素
      }
    }
  }
};
</script>

<style scoped>
/* 全局背景设置 */
.app-container {
  display: flex;
  justify-content: space-between;
  padding: 30px; /* 增加整体容器的内边距 */
  background-color: #f5f7fa;
  height: 100%;
  width: 100vw;
}

/* 聊天区域样式 */
.chat-section {
  background-color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px; /* 增加底部间距 */
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px; /* 增加消息间距 */
}

.user-message .message-bubble {
  background-color: white;
  border-radius: 15px 15px 0 15px;
  align-self: flex-end;
}

.bot-message .message-bubble {
  background-color: #ffffff;
  border-radius: 15px 15px 15px 0;
  color: black;
  align-self: flex-start;
}

.message-avatar {
  padding-left: 10px;
  padding-right: 10px;
}

.message-bubble {
  padding: 10px;
  max-width: 70%; /* 调整气泡的最大宽度 */
  font-size: 14px;
  line-height: 1.4;
}

.avatar {
  width: 35px; /* 调整头像大小 */
  height: 35px;
  border-radius: 50%;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input-box {
  flex-grow: 1;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ddd;
  outline: none;
}

.send-button {
  background-color: #6c63ff;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover {
  background-color: #4c47d8;
}


.player-info {
  text-align: left;
  display: flex;
  gap: 10px;
  align-items: center; /* 垂直居中 */
  height: 100%; /* 需要的高度 */
}

.player-list-header {
  color: black;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px; /* 增加底部间距 */
}

.player-card {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: space-between;
  padding: 10px;
  border-radius: 15px;
  background-color: #f0f0f0;
}


.player-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
}

.player-name {
  font-family: 'Bebas Neue', Impact, sans-serif; /* 选择一个粗体且霸气的字体 */
  font-size: 35px;
  color: #070602;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.player-score {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 14px;
  color: #d4ac0d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.select-button {
  background-color: #6c63ff;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 5px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.select-button:hover {
  background-color: #4c47d8;
}

/* 右边选手名字输入框 */
.custom-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
}

.custom-input:focus {
  border-color: #007bff;
}

/* 右边选手赛区选择框 */
.custom-select {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
  background-color: #fff;
}

.custom-select:focus {
  border-color: #007bff;
}

/* 加载回答时候的加载特效 */
.loading-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #a09dcf;
  font-weight: bold;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Animated loading dots */
.loading-dots::after {
  content: '';
  display: inline-block;
  animation: ellipsis 1.2s infinite steps(4, end);
  vertical-align: bottom;
  font-weight: bold;
}

@keyframes ellipsis {
  0% {
    content: '';
  }
  25% {
    content: '.';
  }
  50% {
    content: '..';
  }
  75% {
    content: '...';
  }
  100% {
    content: '';
  }
}

.g-glossy {
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
}

</style>
