<template>
    <div @click="NewsPreviewClickHandler(news_data.news_id)">
    <el-row>
        <el-col :span="7">
            <el-image :src="news_data.covers_thumbnail" fit="contain" />
        </el-col>
        <el-col :offset="1" :span="16">
            <div>
                <el-text size="large" style="color:white">{{ news_data.title }}</el-text>
            </div>
            <div>
                <el-text size="small" style="color:white">{{ news_data.pub_date }}</el-text>
            </div>
            <div>
                <el-text line-clamp="3" size="default" style="color:white">{{ news_data.content }}</el-text>
            </div>
        </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
// import {fetchImage} from '@/api/request_backend.js'

export default {
  name: 'NewsPreview',
  props:[
    'news_data',
  ],
  methods: {
    NewsPreviewClickHandler(news_id) {
        this.$router.push({ name: 'news', params: { news_id: news_id } });
    }
  },
  setup(props) {
    const news_data=props.news_data
    // const loading = ref(true);
    // const error = ref(null);
    // const fetchImageData = async () => {
    //     try {
    //         loading.value = true;
    //         const data = await fetchImage(news_data.covers_thumbnail);
    //         news_data.covers_thumbnail = data;
    //     } catch (err) {
    //         error.value = 'Error fetching data';
    //         console.error(err);
    //     } finally {
    //         loading.value = false;
    //     }
    // };

    // onMounted(() => {
    //     fetchImageData()
    // })


    return {
        news_data
    };
  },
};







</script>

<style scoped>


</style>
