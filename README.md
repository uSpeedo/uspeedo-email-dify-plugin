# USpeedo Email Plugin

**Author:** uspeedo  
**Version:** 0.0.1  
**Type:** tool

## 简介

USpeedo Email 是一个 Dify 插件，允许您在工作流中通过 USpeedo 邮件服务发送邮件。该插件支持发送 HTML 格式的邮件，支持多个收件人，并提供了灵活的配置选项。

## 功能特性

- ✅ 支持发送 HTML 格式邮件
- ✅ 支持多个收件人（逗号分隔）
- ✅ 支持自定义发件人显示名称
- ✅ 完整的错误处理和验证
- ✅ 安全的凭证管理

## 安装

### 方式一：从 Dify 插件市场安装

1. 在 Dify 平台中打开插件市场
2. 搜索 "uspeedo-email"
3. 点击安装

### 方式二：手动安装

1. 下载插件包（`.difypkg` 文件）
2. 在 Dify 平台的插件管理页面中上传安装

## 配置

安装插件后，需要配置以下凭证：

- **ACCESSKEY_ID**: 从 [uspeedo.com](https://uspeedo.com) 获取的访问密钥 ID
- **ACCESSKEY_SECRET**: 从 [uspeedo.com](https://uspeedo.com) 获取的访问密钥

### 获取凭证步骤

1. 访问 [uspeedo.com](https://uspeedo.com)
2. 登录您的账户
3. 进入 API 密钥管理页面
4. 创建或查看您的 ACCESSKEY_ID 和 ACCESSKEY_SECRET

## 使用方法

### 在工作流中使用

1. 在 Dify 工作流编辑器中添加 "uspeedo-email" 工具节点
2. 配置以下参数：
   - **发送邮箱** (`send_email`): 发件人邮箱地址（必填）
   - **收件人邮箱地址** (`target_email_address`): 收件人邮箱，多个地址用逗号分隔，例如：`user1@example.com,user2@example.com`（必填）
   - **邮件主题** (`subject`): 邮件主题（必填）
   - **邮件内容** (`content`): 邮件的 HTML 内容（必填）
   - **发件人显示名称** (`from_name`): 发件人的显示名称（可选）

3. 运行工作流即可发送邮件

### 示例

```json
{
  "send_email": "sender@example.com",
  "target_email_address": "recipient1@example.com,recipient2@example.com",
  "subject": "测试邮件",
  "content": "<h1>这是一封测试邮件</h1><p>邮件内容...</p>",
  "from_name": "USpeedo Team"
}
```

## 支持的语言

- 中文（简体）
- English
- 日本語
- Português (Brasil)

## 版本历史

### 0.0.1
- 初始版本
- 支持基本的邮件发送功能
- 支持多收件人
- 支持 HTML 内容

## 技术支持

如有问题或建议，请访问：
- [USpeedo 官网](https://uspeedo.com)
- [Dify 文档](https://docs.dify.ai)

## 许可证

请查看插件的许可证文件以了解使用条款。


