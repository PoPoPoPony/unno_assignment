import axiosInstance from '@/axios.js';

export const fetchNewsList = async (limit, offset) => {
    try {
        const response = await axiosInstance.get('/newslist', {
            params:{
                limit: limit,
                offset: offset
            }
        });
        return response.data;
    } catch (err) {
        throw new Error('Error fetching data');
    }
};

export const fetchNews = async (news_id) => {
    try {
        const response = await axiosInstance.get(`/news/${news_id}`);
        return response.data;
    } catch (err) {
        throw new Error('Error fetching data');
    }
};


export const fetchImage = async (image_url) => {
    try {
        const response = await axiosInstance.get(image_url);
        return response.data;
    } catch (err) {
        throw new Error('Error fetching data');
    }
};
