# scubro-homepage

The Brotherhood of SCU（四川大学开源社区）官方网站，基于 [Astro](https://astro.build) + Tailwind CSS v4 构建。

**线上地址**：https://scubro.dev

## 开发

```bash
npm install
npm run dev        # 本地开发 http://localhost:4321
npm run build      # 构建到 dist/
npm run preview    # 本地预览构建产物
```

## 写文章

在 `src/content/blog/` 下新建 Markdown 文件即可，文件名即 URL slug：

```markdown
---
title: 文章标题
description: 摘要（可选，用于列表和 SEO）
date: 2026-09-06 12:00:00
author: 你的名字
tags:
  - dev
---

正文……
```

图片放在 `public/images/posts/<slug>/` 下，正文里用 `/images/posts/<slug>/xxx.avif` 引用。

## 更新成员名录

成员数据来自 GitHub 组织 API（含角色与 bio），存储在 `src/data/members.json`，由 GitHub Actions（`.github/workflows/sync-members.yml`）每天自动同步，有变化时自动提交并触发部署，无需手动维护。

提交推送用的是 `MEMBERS_SYNC_TOKEN` secret，不是内置 `GITHUB_TOKEN`——后者的 push 按 GitHub 设计不会触发 `deploy.yml`。因此该 token 除 `read:org`（读组织成员）外还需仓库写权限：classic PAT 用 `repo` + `read:org`，fine-grained PAT 用 Repository → Contents: Read and write 加 Organization → Members: Read-only。

## 部署

推送到 `main` 分支后，GitHub Actions（`.github/workflows/deploy.yml`）自动构建并发布到 GitHub Pages。
自定义域名 `scubro.dev` 通过 `public/CNAME` 保持绑定。

## 目录结构

```
src/
  content/blog/     # 博客文章（Markdown）
  data/site.ts      # 站点数据：项目、成员、理念、联系方式
  components/       # 页头、页脚、项目卡等组件
  layouts/          # 基础布局
  pages/            # 路由：首页 / 博客 / 项目 / 成员 / 关于
  styles/           # 设计系统（Tailwind v4 @theme 令牌 + 长文排版）
public/
  images/           # 项目封面、文章配图
  CNAME             # 自定义域名
```
