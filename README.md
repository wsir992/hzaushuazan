# 华中农业大学教师主页刷赞脚本
## 原理

点赞功能通过 POST 请求 `/system/resource/tsites/praise.jsp` 实现，发送 `ac=updatePraise` 参数即可增加点赞数。服务端无 IP/频率限制，可并发刷赞。

## 环境准备

```bash
pip install requests
```

## 使用方法

```bash
# 刷 100 次（默认）
python like.py -n 100

# 刷 500 次，10 线程并发
python like.py -n 500 -t 10

# 刷 1000 次，20 线程并发
python like.py -n 1000 -t 20
```

## 给其他老师使用
1. 打开该老师的教师主页（如 `https://faculty.hzau.edu.cn/xxx/zh_CN/index.htm`）
2. 按 F12 打开开发者工具，在页面源码中搜索 `TsitesPraiseUtil`，找到类似以下代码：

```html
<script>
_TsitesPraiseUtil_u10.setParam({
    'uid': '5199',          # ← 记下这个值
    'homepageid': 9357,     # ← 记下这个值
    ...
});
</script>
```

3. 运行脚本：
```bash
python like.py --uid 5199 --homepageid 9357 -n 100
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n` | 点赞次数 | 100 |
| `-t` / `--threads` | 并发线程数 | 5 |
| `--uid` | 教师 UID | 0 |
| `--homepageid` | 主页 ID | 0 |

## 验证

运行后脚本会输出刷赞前后的点赞数，对比净增量即可确认是否成功。
