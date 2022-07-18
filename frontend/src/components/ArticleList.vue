<template>
  <div v-for="article in info.results" v-bind:key="article.url" id="articles">
    <div>
      <span v-for="tag in article.tags" v-bind:key="tag" class="tag">
        {{ tag }}
      </span>
    </div>
    <!-- <div class="article-title">
      {{ article.title }}
    </div> -->
    <!-- 不再使用常规的<a>标签，而是<router-link>标签 -->
    <!-- :to属性指定了跳转位置，跳转到了/article/:id处，其中的id由params指出，如果是query，则是url参数，用?拼接到url之后 -->
    <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }" class="article-title">
      {{ article.title }}
    </router-link>
    <div>{{ formatted_time(article.created) }}</div>
  </div>
  <div id="paginator">
    <span v-if="is_page_exist('previous')">
      <router-link :to="get_path('previous')">
        Prev
      </router-link>
    </span>
    <span class="current-page">
      {{ get_page_param('current') }}
    </span>
    <span v-if="is_page_exist('next')">
      <router-link :to="get_path('next')">
        Next
      </router-link>
    </span>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ArticleList',
  data: function () {
    return {
      info: ''
    }
  },
  mounted () {
    this.get_article_data();
  },
  methods: {
    formatted_time: function (iso_date_string) {
      const date = new Date(iso_date_string);
      return date.toLocaleDateString();
    },
    // 判断页面是否存在
    is_page_exist (direction) {
      if (direction === 'next') {
        return this.info.next !== null;
      }
      return this.info.previous !== null;
    },
    // 获取页码
    get_page_param: function (direction) {
      try {
        let url_string;
        switch (direction) {
          case 'next':
            url_string = this.info.next;
            break;
          case 'previous':
            url_string = this.info.previous;
            break;
          default:
            if (!('page' in this.$route.query)) return 1;
            if (this.$route.query.page === null) return 1;
            return this.$route.query.page;
        }
        const url = new URL(url_string);
        return url.searchParams.get('page')
      }
      catch (err) {
        return;
      }
    },
    // 获取文章列表数据
    get_article_data: function () {
      let url = '/api/article';

      let params = new URLSearchParams(); // 专门处理路径参数的类
      params.appendIfExists('page', this.$route.query.page); // 本身的append方法无法判断值是否存在，因此在main.js中扩展这个类的方法
      params.appendIfExists('search', this.$route.query.search);
      const paramString = params.toString();
      if (paramString.charAt(0) !== '') {
        url += '/?' + paramString;
      }
      axios.get(url).then(response => (this.info = response.data))
    },
    // 获取路径
    get_path: function (direction) {
      let url = '';

      try {
        switch (direction) {
          case 'next':
            if (this.info.next !== undefined) {
              url += (new URL(this.info.next)).search // 这个search表示获取URL中?及以后的内容，即查询参数
            }
            break;
          case 'previous':
            if (this.info.previous !== undefined) {
              url += (new URL(this.info.previous)).search
            }
            break;
        }
      }
      catch { return url }

      return url
    }
  },
  watch: {
    // 监听路由变化
    $route () {
      this.get_article_data();
    }
  },
}
</script>

<style scoped>
#articles {
  padding: 10px;
}

.article-title {
  font-size: large;
  font-weight: bolder;
  color: black;
  text-decoration: none;
  padding: 5px 0 5px 0;
}

.tag {
  padding: 2px 5px 2px 5px;
  margin: 5px 5px 5px 0;
  font-family: Georgia, Arial, sans-serif;
  font-size: small;
  background-color: #4e4e4e;
  color: whitesmoke;
  border-radius: 5px;
}

#paginator {
  text-align: center;
  padding-top: 50px;
}

a {
  color: black;
}

.current-page {
  font-size: x-large;
  font-weight: bold;
  padding-left: 10px;
  padding-right: 10px;
}
</style>
