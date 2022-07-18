import axios from 'axios';

async function authorization () {
  const storage = localStorage;

  let hasLogin = false;
  let username = storage.getItem('username.myblog');

  // 过期时间
  const expiredTime = Number(storage.getItem('expiredTime.myblog'));
  // 当前时间
  const current = (new Date()).getTime();
  // 刷新令牌
  const refreshToken = storage.getItem('refresh.myblog');

  // token未过期
  if (expiredTime > current) {
    hasLogin = true;
    console.log('authorization access')
  }
  // token过期
  else if (refreshToken !== null) {
    try {
      // async/await: async 表示函数里含有异步操作，await 表示紧跟其后的表达式需要等待结果
      let response = await axios.post('/api/token/refresh/', { refresh: refreshToken });

      const nextExpiredTime = Date.parse(response.headers.date) + 60000;
      storage.setItem('access.myblog', response.data.access);
      storage.setItem('expiredTime.myblog', nextExpiredTime);
      storage.removeItem('refresh.myblog');
      hasLogin = true;
      console.log('authorization refresh')
    }
    catch (err) {
      storage.clear();
      hasLogin = false;
      console.log('authorization err')
    }
  }
  else {
    storage.clear();
    hasLogin = false;
    console.log('authorization exp')
  }
  console.log('authorization done')
  // async函数返回的并不是return后面的数据，而是包含数据的Promise对象，因此调用它的位置需要改为Promise.then().catch()
  return [hasLogin, username]
}

export default authorization;