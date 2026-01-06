# USpeedo 邮件插件测试指南

## 前置要求

1. Python 3.11 或更高版本
2. 已安装 Dify 平台（本地或云端）
3. 从 uspeedo.com 获取的 ACCESSKEY_ID 和 ACCESSKEY_SECRET

## 方式一：本地调试模式（推荐用于开发测试）

### 步骤 1: 安装依赖

```bash
cd /Users/user/Desktop/demo/dify-plugin/uspeedo-email
pip install -r requirements.txt
```

### 步骤 2: 配置调试环境（可选）

如果需要使用远程调试模式，创建 `.env` 文件：

```bash
# 创建 .env 文件
cat > .env << EOF
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug.dify.ai:5003
REMOTE_INSTALL_KEY=your-debug-key
EOF
```

**注意**：如果您的 Dify 实例在本地运行，可能不需要这些配置。

### 步骤 3: 运行插件

```bash
python -m main
```

插件将在本地运行，默认监听端口（通常是 5003）。

### 步骤 4: 在 Dify 中配置插件

1. **登录 Dify 平台**
2. **进入插件管理页面**：
   - 导航到 "设置" → "插件" 或 "Settings" → "Plugins"
3. **添加插件**：
   - 如果使用远程调试模式，插件会显示为 "debugging" 状态
   - 如果使用本地模式，可能需要通过 URL 或文件安装
4. **配置凭证**：
   - 点击插件进入配置页面
   - 输入您的 `ACCESSKEY_ID`（访问密钥ID）
   - 输入您的 `ACCESSKEY_SECRET`（访问密钥）
   - 保存配置

### 步骤 5: 测试插件

1. **创建工作流或对话**：
   - 在 Dify 中创建一个新的工作流或对话
2. **添加工具节点**：
   - 在工作流中添加 "uspeedo-email" 工具节点
3. **配置工具参数**：
   - `send_email`: 发送邮箱地址（例如：sender@example.com）
   - `target_email_address`: 收件人邮箱列表（例如：["recipient@example.com"]）
   - `subject`: 邮件主题（例如：测试邮件）
   - `content`: 邮件内容，HTML 格式（例如：<html><body><h1>测试</h1></body></html>）
   - `from_name`: 发件人名称（可选，例如：USpeedo）
4. **运行测试**：
   - 执行工作流，检查邮件是否成功发送
   - 查看返回结果，确认发送状态

## 方式二：打包安装模式（用于生产环境）

### 步骤 1: 安装 Dify CLI 工具

**重要说明**：`dify-plugin-cli` **不在 Homebrew 官方仓库中**，因此 `brew install dify-plugin-cli` 会失败。需要手动从 GitHub Releases 下载二进制文件。

**方法一：使用 curl 下载（推荐）**

```bash
# macOS (Apple Silicon/M1/M2/M3) - 您的系统使用此版本
cd /tmp
curl -L -o dify-plugin https://github.com/langgenius/dify-plugin-daemon/releases/download/0.5.2/dify-plugin-darwin-arm64
chmod +x dify-plugin
sudo mv dify-plugin /usr/local/bin/

# macOS (Intel 芯片)
cd /tmp
curl -L -o dify-plugin https://github.com/langgenius/dify-plugin-daemon/releases/download/0.5.2/dify-plugin-darwin-amd64
chmod +x dify-plugin
sudo mv dify-plugin /usr/local/bin/

# 验证安装
dify-plugin --version
```

**方法二：手动下载**

1. 访问 https://github.com/langgenius/dify-plugin-daemon/releases
2. 找到最新版本（当前为 0.5.2）
3. 下载对应平台的二进制文件：
   - macOS Intel: `dify-plugin-darwin-amd64`
   - macOS Apple Silicon: `dify-plugin-darwin-arm64`
4. 将文件重命名为 `dify-plugin` 并移动到 `/usr/local/bin/` 目录
5. 添加执行权限：`chmod +x /usr/local/bin/dify-plugin`
6. 验证安装：`dify-plugin --version`

### 步骤 2: 打包插件

```bash
cd /Users/user/Desktop/demo/dify-plugin/uspeedo-email
dify-plugin plugin package . -o uspeedo-email-0.0.1.difypkg
```

### 步骤 3: 在 Dify 中安装插件

1. **登录 Dify 平台**
2. **进入插件管理页面**
3. **上传插件包**：
   - 点击 "安装插件" 或 "Install Plugin"
   - 选择打包好的 `.difypkg` 文件
   - 等待安装完成
4. **配置凭证**（同方式一的步骤 4）
5. **测试插件**（同方式一的步骤 5）

## 常见问题排查

### 0. brew install dify-plugin-cli 失败

**问题**：执行 `brew install dify-plugin-cli` 时提示 "No available formula with the name 'dify-plugin-cli'"

**原因**：`dify-plugin-cli` 不在 Homebrew 官方仓库中，因此无法通过 `brew install` 安装。

**解决方案**：
- 按照"方式二：打包安装模式"中的"步骤 1"手动下载二进制文件
- 使用 `curl` 命令下载（推荐）：
  ```bash
  # Apple Silicon (M1/M2/M3)
  curl -L -o /tmp/dify-plugin https://github.com/langgenius/dify-plugin-daemon/releases/download/0.5.2/dify-plugin-darwin-arm64
  chmod +x /tmp/dify-plugin
  sudo mv /tmp/dify-plugin /usr/local/bin/
  ```

### 1. 插件无法启动

**问题**：运行 `python -m main` 时出错

**解决方案**：
- 检查 Python 版本：`python --version`（需要 3.11+）
- 检查依赖是否安装：`pip list | grep dify-plugin`
- 检查依赖是否安装：`pip list | grep requests`
- 重新安装依赖：`pip install -r requirements.txt --upgrade`

### 2. 插件在 Dify 中不可见

**解决方案**：
- 确认插件服务正在运行（`python -m main`）
- 检查 Dify 配置中的插件服务地址
- 刷新 Dify 页面
- 检查浏览器控制台是否有错误

### 3. 凭证验证失败

**问题**：配置凭证时提示验证失败

**解决方案**：
- 确认 ACCESSKEY_ID 和 ACCESSKEY_SECRET 正确
- 确认凭证不为空且没有多余空格
- 检查凭证是否从 uspeedo.com 正确获取

### 4. 邮件发送失败

**问题**：工具执行后返回错误

**解决方案**：
- 检查所有必需参数是否已填写
- 确认收件人邮箱地址格式正确
- 检查邮件内容是否为有效的 HTML
- 查看错误消息，根据提示调整参数
- 确认 USpeedo 账户有足够的发送配额

### 5. 网络连接问题

**问题**：无法连接到 USpeedo API

**解决方案**：
- 检查网络连接
- 确认防火墙设置
- 检查 USpeedo API 服务状态
- 验证 API 地址是否正确：`https://api.uspeedo.com/api/v1/email/SendEmail`

## 测试用例示例

### 测试用例 1: 基本邮件发送

```yaml
send_email: "sender@example.com"
target_email_address: ["recipient@example.com"]
subject: "测试邮件"
content: "<html><body><h1>这是测试邮件</h1><p>如果您收到此邮件，说明插件工作正常。</p></body></html>"
from_name: "USpeedo 测试"
```

### 测试用例 2: 多个收件人

```yaml
send_email: "sender@example.com"
target_email_address: ["recipient1@example.com", "recipient2@example.com"]
subject: "群发测试"
content: "<html><body><p>这是一封群发测试邮件。</p></body></html>"
from_name: "USpeedo"
```

### 测试用例 3: 最小参数（无 from_name）

```yaml
send_email: "sender@example.com"
target_email_address: ["recipient@example.com"]
subject: "简单测试"
content: "<html><body><p>测试内容</p></body></html>"
```

## 调试技巧

1. **查看日志**：
   - 运行插件时，终端会显示请求日志
   - 注意观察错误信息和状态码

2. **测试 API 直接调用**：
   ```bash
   curl -X POST "https://api.uspeedo.com/api/v1/email/SendEmail" \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic $(echo -n 'YOUR_ACCESSKEY_ID:YOUR_ACCESSKEY_SECRET' | base64)" \
     -d '{
       "SendEmail": "sender@example.com",
       "TargetEmailAddress": ["recipient@example.com"],
       "Subject": "测试",
       "Content": "<html><body><p>测试</p></body></html>",
       "FromName": "USpeedo"
     }'
   ```

3. **检查返回结果**：
   - 成功时返回 JSON 格式的成功消息
   - 失败时返回详细的错误信息

## 下一步

测试成功后，您可以：
1. 在工作流中集成邮件发送功能
2. 结合 AI 模型生成邮件内容
3. 设置自动化邮件通知
4. 打包发布到 Dify 插件市场

