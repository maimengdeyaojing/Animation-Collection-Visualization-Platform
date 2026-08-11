<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

import { getToken } from "@/api/bangumi";
import { getMe } from "@/api/bangumi";
import { syncBangumi } from "@/api/bangumi";

const route = useRoute();
const router = useRouter();

onMounted(async () => {

  console.log("OAuthCallback执行")
  console.log("当前URL:", window.location.href)
  
  try {

    const code = route.query.code;

    console.log("授权码:", code);

    // 获取 access_token
    const tokenRes = await getToken(code);

    const accessToken =
      tokenRes.data.access_token;

    console.log("Token获取成功");

    localStorage.setItem(
      "bgm_token",
      accessToken
    );

    // 获取用户资料
    const meRes =
      await getMe(accessToken);

    const user =
      meRes.data;

    console.log("用户信息", user);

    console.log("用户名", user.username);

    localStorage.setItem(
      "bgm_user",
      JSON.stringify(user)
    );

    // 同步到数据库
    console.log("开始同步收藏...");

    const syncRes =
      await syncBangumi(
        user.username,
        accessToken
      );

    console.log(syncRes.data);

    console.log("同步完成");

    router.push("/home");

  } catch (err) {

    console.error(err);

  }

});
</script>