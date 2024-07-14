<template>
  <div>
    <el-row>
      <el-col :span="16" :offset="4">
        <div class="NewsListContainer">
          <div v-for="news_data in all_news_data" :key="news_data.news_id">
            <NewsPreview class="NewsPreviewItem" :news_data="news_data"></NewsPreview>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import {fetchNewsList} from '@/api/request_backend.js'
import NewsPreview from '@/components/NewsPreview.vue';


export default {
  name: 'NewsList',
  components: {
    NewsPreview,
  },
  methods:{

  },
  setup() {
    const all_news_data = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const fetchData = async (limit, offset) => {
      try {
        loading.value = true;
        const data = await fetchNewsList(limit, offset);
        all_news_data.value = data;
      } catch (err) {
        error.value = 'Error fetching data';
        console.error(err);
      } finally {
        loading.value = false;
      }
    };



    onMounted(() => {
      fetchData(null, 0);
      
    });

    return {
      all_news_data,
      loading,
      error,
    };
  },
};


</script>

<style scoped>
.NewsListContainer{
  margin-top:20px;
  margin-bottom:20px;
  border: 1px solid white;
  border-radius: 2px;
  padding: 5px;
}

.NewsPreviewItem {
  margin: 10px;
  cursor: pointer;
}

.NewsPreviewItem:hover {
  background-color: rgba(0, 0, 0, 0.3);
}



</style>

