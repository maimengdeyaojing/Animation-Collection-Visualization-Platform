<template>
  <div class="home">

    <!-- 欢迎栏 -->
    <el-card class="welcome-card">
      <h2>欢迎来到 Anime Project</h2>
      <p>发现优秀动画，记录追番日常</p>
    </el-card>

    <!-- Bangumi同步 -->
    <el-card class="bangumi-card" shadow="hover">

      <div class="bangumi-sync">

        <div class="left">
          <div class="title">
            导入 Bangumi 账号数据
          </div>

          <div class="desc">
            一键同步在看、看过和想看列表
          </div>
        </div>

        <div class="right">
          <el-button
            type="success"
            size="large"
            @click="handleBangumiLogin"
          >
            连接 Bangumi
          </el-button>
        </div>

      </div>

    </el-card>

    <!-- 数据统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="number">{{ stats.doing }}</div>
            <div class="label">在看番剧</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="number"> {{ stats.completed }}</div>
            <div class="label">看过作品</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="number"> {{ stats.wish }}</div>
            <div class="label">想看作品</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="number"> {{ totalAnime }}</div>
            <div class="label">本季新番</div>
          </div>
        </el-card>
      </el-col>
      

    </el-row>

    <el-card class="section-card">
      <template #header>
        <span>📺 本周放送</span>
      </template>

      <el-row :gutter="20">
        <el-col
          v-for="day in weekData"
          :key="day.weekday.id"
          :span="8"
          style="margin-bottom:20px"
        >
          <el-card shadow="hover">

            <h3>{{ day.weekday.cn }}</h3>

            <el-divider />

            <div
              v-for="anime in day.items"
              :key="anime.id"
              class="anime-item"
            >
              {{ anime.name_cn || anime.name }}
            </div>

          </el-card>
        </el-col>
      </el-row>
    </el-card>

  </div>
</template>

<script setup>

import { ref, onMounted, computed } from 'vue'
import { getCalendar } from '@/api/bangumi'
import { ElMessage } from 'element-plus'
import { getStats } from '@/api/bangumi'

const weekData = ref([])

const loadCalendar = async () => {
  try {
    const res = await getCalendar()
    weekData.value = res.data
  } catch (error) {
    console.error('获取番剧日历失败', error)
  }
}

const stats = ref({
  doing: 0,
  completed: 0,
  wish: 0
})

const loadStats = async () => {

  try {

    const res = await getStats()

    stats.value = res.data

  } catch (err) {

    console.error(err)

  }

}


onMounted(() => {

  loadCalendar()

  loadStats()

})

const handleBangumiLogin = () => {

  const clientId = 'bgm63556a30fef6e8765'

  const redirectUri =
    encodeURIComponent(
      'http://localhost:5173/oauth/callback'
    )

  window.location.href =
    `https://bgm.tv/oauth/authorize?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}`
}

const totalAnime = computed(() => {
  return weekData.value.reduce(
    (sum, day) => sum + day.items.length,
    0
  )
})

</script>


<style scoped>
.home {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.label {
  margin-top: 10px;
  color: #666;
}

.section-card {
  margin-bottom: 20px;
}

.anime-cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.anime-info {
  margin-top: 10px;
  text-align: center;
}
.anime-item {
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.anime-item:last-child {
  border-bottom: none;
}

.bangumi-card {
  margin-bottom: 20px;
}

.bangumi-sync {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.desc {
  margin-top: 6px;
  color: #909399;
}

</style>