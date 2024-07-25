<template>
  <div>
    <vue-danmaku
      ref="danmaku"
      v-model="danmus"
      :channels="20"
      :speeds="110"
      :randomChannel="false"
      use-slot
      :loop="false"
      style="height: 90vh; width: 90vw"
    >
      <!-- 弹幕插槽 -->
      <template v-slot:dm="{ index, danmu }">
        <div :style="{ color: '#FFFFFF', textShadow: '2px 2px 4px #000', fontSize: '24px' }">
          <span :style="{ color: danmu.color, fontWeight: 'bold' }">{{ danmu.character }}</span>
          : {{ danmu.text }}
        </div>
      </template>
      <video
        ref="video"
        width="100%"
        controls
        @play="onPlay"
        @pause="onPause"
        @timeupdate="onTimeUpdate"
      >
        <source src="./videos/8.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </vue-danmaku>
    <!-- 添加滑块 -->
    <input
      type="range"
      min="0.1"
      max="2.0"
      step="0.1"
      v-model="playbackRate"
      @input="onPlaybackRateChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import vueDanmaku from 'vue3-danmaku'

// 定义 ref 变量
const allDanmus = ref([])
const danmus = ref([])
let currentDanmuIndex = 0
let rafId = null
const video = ref(null)
const danmaku = ref(null)
const characterColors = ref({})
const playbackRate = ref(1.0) // 定义播放速度
const danmuScrollTime = 6 // 弹幕滚动时间，假设是5秒

// 颜色列表
const colorList = [
  '#a3dba0',
  '#a1f509',
  '#cb15d4',
  '#b80d9a',
  '#4fa513',
  '#73026c',
  '#28fa79',
  '#e920e7',
  '#ab83dd',
  '#c2d8a6'
]

// 辅助函数：将 HH:MM:SS 格式转换为秒数
const timeStringToSeconds = (timeString) => {
  const [hours, minutes, seconds] = timeString.split(':').map(Number)
  return hours * 3600 + minutes * 60 + seconds
}

// 定义颜色生成函数为颜色列表的索引
const generateColor = (index) => colorList[index % colorList.length]

// 获取弹幕数据并转换时间格式
const fetchDanmusFromJson = async () => {
  try {
    const response = await fetch('danmu_20240718133419.json') // 替换为实际的 JSON 文件路径
    const data = await response.json()
    const characters = new Set(data.map((item) => item.character))
    let index = 0
    characters.forEach((character) => {
      if (!characterColors.value[character]) {
        characterColors.value[character] = generateColor(index++)
      }
    })
    allDanmus.value = data.map((item) => ({
      time: timeStringToSeconds(item.time), // 转换时间格式
      content: item.content,
      character: item.character,
      color: characterColors.value[item.character]
    }))
  } catch (error) {
    console.error('加载弹幕失败:', error)
  }
}

// 根据当前时间推送弹幕
const pushDanmusByTime = (currentTime) => {
  while (
    currentDanmuIndex < allDanmus.value.length &&
    allDanmus.value[currentDanmuIndex].time <= currentTime
  ) {
    const { content, character, color } = allDanmus.value[currentDanmuIndex]
    danmaku.value.push({ text: content, character, color }) // 使用 ref 推送弹幕
    currentDanmuIndex++
  }
}

// 视频事件处理函数
const onPlay = () => {
  const updateDanmus = () => {
    pushDanmusByTime(Math.floor(video.value.currentTime))
    adjustPlaybackRate(Math.floor(video.value.currentTime))
    rafId = requestAnimationFrame(updateDanmus)
  }
  if (!rafId) {
    rafId = requestAnimationFrame(updateDanmus)
  }
}

const onPause = () => {
  if (rafId) {
    cancelAnimationFrame(rafId)
    rafId = null
  }
}

const onTimeUpdate = () => {
  pushDanmusByTime(Math.floor(video.value.currentTime))
  adjustPlaybackRate(Math.floor(video.value.currentTime))
}

// 播放速度变化处理函数
const onPlaybackRateChange = () => {
  video.value.playbackRate = playbackRate.value
}

// 调整播放速度
const adjustPlaybackRate = (currentTime) => {
  const windowSize = 10 // 10秒窗口
  const startTime = currentTime
  const endTime = currentTime + windowSize

  const danmuInWindow = allDanmus.value.filter(
    (danmu) => danmu.time >= startTime && danmu.time <= endTime
  )

  const density = danmuInWindow.length / windowSize
  playbackRate.value = Math.min(Math.max(1 - density * 0.1, 0.1), 2.0)
}

// 组件挂载和卸载时处理
onMounted(async () => {
  await fetchDanmusFromJson()
  watch(playbackRate, (newRate) => {
    video.value.playbackRate = newRate
  })
})

onUnmounted(() => {
  if (rafId) {
    cancelAnimationFrame(rafId)
  }
})
</script>

<style>
video {
  display: block;
  margin: 0 auto;
}
input[type='range'] {
  width: 100%;
  margin: 10px 0;
}
</style>
