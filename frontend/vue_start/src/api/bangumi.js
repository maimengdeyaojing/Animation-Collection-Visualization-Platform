import axios from 'axios'

// 创建 Bangumi API 实例
const bangumiApi = axios.create({
  baseURL: 'https://api.bgm.tv',
  timeout: 10000
})

// 获取每周放送
export function getCalendar() {
  return bangumiApi.get('/calendar')
}

// 获取条目详情
export function getSubject(id) {
  return bangumiApi.get(`/v0/subjects/${id}`)
}

// 搜索动画
export function searchAnime(keyword) {
  return bangumiApi.post('/v0/search/subjects', {
    keyword,
    sort: 'rank',
    filter: {
      type: [2] // 2表示动画
    }
  })
}

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/bangumi"
});

export function getToken(code) {
  return api.post("/token", null, {
    params: { code }
  });
}

export function getMe(token) {
  return api.get("/me", {
    params: { token }
  });
}

export function getCollections(
  username,
  token
) {
  return api.get(
    `/collections/${username}`,
    {
      params: { token }
    }
  );
}

export const syncBangumi = (
  username,
  token
) => {

  return api.post(
    "/sync",
    null,
    {
      params: {
        username,
        token
      }
    }
  )
}

export const getStats = () => {

  return api.get(
    "/stats"
  )

}
