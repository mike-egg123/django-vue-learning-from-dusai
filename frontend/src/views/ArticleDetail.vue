<!-- 文章详情页面 -->
<template>
  <BlogHeader />
  <!-- 在渲染文章前，用v-if先确认数据是否存在，避免出现潜在的调用数据不存在的bug -->
  <div v-if="article !== null" class="grid-container">
    <div>
      <h1 id="title">{{ article.title }}</h1>
      <p id="subtitle">
        本文由 {{ article.author.username }} 发布于 {{ formatted_time(article.created) }}

      </p>
      <!-- 由于body_html和toc_html都是后端渲染好的markdown文本，因此用v-html直接转换成html -->
      <div v-html="article.body_html" class="article-body"></div>
    </div>
    <div>
      <h3>目录</h3>
      <div v-html="article.toc_html" class="toc"></div>
    </div>
  </div>
  <BlogFooter />
</template>

<script>
import BlogHeader from '@/components/BlogHeader.vue'
import BlogFooter from '@/components/BlogFooter.vue'
import axios from 'axios'


export default {
  name: "ArticleDetail",
  components: { BlogHeader, BlogFooter },
  data: function () {
    return {
      article: null
    }
  },
  mounted () {
    // 通过$route.params.id可以获得路由中的动态参数，以此拼接为接口向后端请求数据
    axios
      .get('/api/article/' + this.$route.params.id)
      .then(response => (this.article = response.data))
  },
  methods: {
    formatted_time: function (iso_date_string) {
      const date = new Date(iso_date_string);
      return date.toLocaleDateString();
    }
  }
}
</script>

<style scoped>
/* 网格样式，grid-template-columns属性规定了有几列，宽度分别是多少 */
.grid-container {
  display: grid;
  grid-template-columns: 3fr 1fr;
}

#title {
  text-align: center;
  font-size: x-large;
}

#subtitle {
  text-align: center;
  color: gray;
  font-size: small;
}
</style>

<style>
.article-body p img {
  max-width: 100%;
  border-radius: 50px;
  box-shadow: gray 0 0 20px;
}

.toc ul {
  list-style-type: none;
}

.toc a {
  color: gray;
}
</style>

