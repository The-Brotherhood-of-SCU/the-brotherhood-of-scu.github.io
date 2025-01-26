此文件夹用于存放项目图片文件

# 命名
全部使用小写英文，使用减号`-`来连接单词，例如：`my-image-name.avif`

# 预处理

注意存放时，先利用`bat`文件将其压缩为`avif`格式

- `convert2avif_height_500px-small-size-extreme`:极限压缩
- `convert2avif_height_500px-small-size`:小尺寸压缩
- `convert2avif_height_500px`:一般压缩

使用方式很简单，将要压缩的文件夹拖入即可

Note：需要环境变量中配置了`ffmpeg`