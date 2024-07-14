import axios from 'axios';

axios.defaults.retry = 3
axios.defaults.retryDelay = 2000;

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 2000,
    headers: {
        'Content-Type': 'application/json',
    }
});

axiosInstance.interceptors.response.use((res)=>{
    return res
}, (error)=>{
    var config = error.config
    config.retry=3
    config.retryDelay=2000;

    if(!config || !config.retry) return Promise.reject(error)
    config.__retryCount = config.__retryCount || 0
    if(config.__retryCount>=config.retry) {
        return Promise.reject(error)
    }
    config.__retryCount +=1
    var backoff = new Promise(function (resolve) {
        setTimeout(function() {
            resolve()
        }, config.retryDelay || 1)
    })
    return backoff.then(function() {
        return axios(config)
    })
})

export default axiosInstance;