<template>
  <div v-loading="loading">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else >

        <el-col :span="16" :offset="4">
            <div class="NewsContainer">
                <h1>{{ news.title }}</h1>
                <el-text size="large" style="color:white">
                    {{ news.pub_date }}
                    {{ news.sources.name }}
                    <template v-if="news.sources.author"> / {{ news.sources.author }}</template>
                    / {{ news.sources.category }}
                </el-text>
                <el-image :src="news.covers_cover_image" fit="scale-down" />
                <el-text size="large" style="color:gray" tag="i">{{news.covers.caption}}</el-text>
                <p/>
                <el-text size="large" style="color:white;">{{news.content}}</el-text>
                <el-row  v-if="news.tags[0].name!=''" style="margin-top:10px" :gutter="20">
                    <div v-for="tag_obj in news.tags" :key="tag_obj">
                        <el-col :span="2">
                            <!-- color="hsla(160, 100%, 37%, 0.2)" -->
                            <el-tag @click="TagClickHandler(tag_obj.name)" class="tags" type="info" effect="plain" size="large"  >{{tag_obj.name}}</el-tag>
                        </el-col>
                    </div>
                </el-row>



            </div>
        </el-col>
    </div>
   

  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import {fetchNews} from '@/api/request_backend.js'
// import NewsPreview from '@/components/NewsPreview.vue';


export default {
  name: 'News',
  props:['news_id'],
  components: {

  },
  methods:{
    TagClickHandler(tag_name) {
        window.open("https://tw-nba.udn.com/search/tag/"+tag_name)
    }
  },
  setup(props) {
    const loading = ref(true);
    const error = ref(null);
    let news = ref(null)

    const fetchData = async (news_id) => {
      try {
        loading.value = true;
        // 调用 API 方法获取新闻详情
        let news_lst = await fetchNews(news_id);
        news.value = news_lst[0]
        console.log(news)
      } catch (err) {
        error.value = 'Error fetching news detail';
        console.error('Error fetching news detail:', err);
      } finally {
        loading.value = false;
      }
    };
    
    onMounted(() => {
        fetchData(props.news_id)
    });

    return {
        loading,
        error,
        news
    }
  }
    
};


</script>

<style scoped>

.NewsContainer{
  margin-top:20px;
  margin-bottom:20px;
  border: 1px solid white;
  border-radius: 2px;
  padding: 5px;
}

.tags {
    cursor: pointer;
    color: black;
}

.tags:hover {
  background-color: rgba(0, 0, 0, 0.3);
  color:white
}
</style>

