# 发布实现与验证

2026-10-25：为指定仓库YZYExp/Learn-Music加入独立主页、分章阅读、全文搜索、主题筛选、浏览器本地阅读进度、原生音频实验与第一版EPUB直接下载。

主稿由book.json单一清单消费。网页Markdown依赖独立锁定，导出另设工作流。已核查官方Actions版本：checkout v7、setup-python v7、configure-pages v6、upload-pages-artifact v5、deploy-pages v5、upload-artifact v7。

网页输出通过全量本地href/src目标检查；书稿本地引用、SVG XML、EPUB XML与资源链接独立检查。浏览器截图为临时验证产物，不进入源库。

仓库已存在初始化提交，沿用该历史，不为恢复旧工程而改写远端。首次启用Pages为管理设置；工作流使用Pages部署权限与OIDC，不尝试用普通GITHUB_TOKEN代替有权账户的首次管理操作。
