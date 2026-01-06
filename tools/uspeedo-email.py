import base64
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class UspeedoEmailTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 获取邮件参数
            send_email = tool_parameters.get("send_email")
            target_email_address = tool_parameters.get("target_email_address")
            subject = tool_parameters.get("subject")
            content = tool_parameters.get("content")
            from_name = tool_parameters.get("from_name")
            
            # 验证必需参数
            if not send_email:
                yield self.create_text_message("错误：发送邮箱地址不能为空")
                return
            
            if not target_email_address:
                yield self.create_text_message("错误：收件人邮箱地址不能为空")
                return
            
            # 检查是否为字符串类型
            if not isinstance(target_email_address, str):
                yield self.create_text_message("错误：收件人邮箱地址必须是字符串类型")
                return
            
            # 去除首尾空格
            target_email_address = target_email_address.strip()
            
            if not target_email_address:
                yield self.create_text_message("错误：收件人邮箱地址不能为空")
                return
            
            # 将逗号分隔的字符串转换为数组
            email_list = [email.strip() for email in target_email_address.split(',')]
            # 过滤空字符串
            email_list = [email for email in email_list if email]
            
            # 验证至少有一个有效的邮箱地址
            if len(email_list) == 0:
                yield self.create_text_message("错误：收件人邮箱地址不能为空")
                return
            
            # 基本验证：检查每个邮箱地址是否包含 @ 符号
            for email in email_list:
                if '@' not in email:
                    yield self.create_text_message(f"错误：邮箱地址格式无效：{email}")
                    return
            
            # 使用解析后的数组
            target_email_address = email_list
            
            if not subject:
                yield self.create_text_message("错误：邮件主题不能为空")
                return
            
            if not content:
                yield self.create_text_message("错误：邮件内容不能为空")
                return
            
            # 从凭证中获取 ACCESSKEY_ID 和 ACCESSKEY_SECRET
            credentials = self.runtime.credentials
            access_key_id = credentials.get("access_key_id")
            access_key_secret = credentials.get("access_key_secret")
            
            if not access_key_id or not access_key_secret:
                yield self.create_text_message("错误：缺少访问凭证，请配置 ACCESSKEY_ID 和 ACCESSKEY_SECRET")
                return
            
            # 构建 Basic Auth 头部
            auth_string = f"{access_key_id}:{access_key_secret}"
            auth_bytes = auth_string.encode("utf-8")
            auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
            
            # 构建请求体
            payload = {
                "SendEmail": send_email,
                "TargetEmailAddress": target_email_address,
                "Subject": subject,
                "Content": content,
            }
            
            # 如果提供了发件人名称，添加到请求体中
            if from_name:
                payload["FromName"] = from_name
            
            # 调用 USpeedo API
            url = "https://api.uspeedo.com/api/v1/email/SendEmail"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth_base64}",
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                yield self.create_json_message({
                    "success": True,
                    "message": "邮件发送成功",
                    "data": result,
                })
            else:
                error_message = f"邮件发送失败：HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_message = f"邮件发送失败：{error_data['message']}"
                    elif "error" in error_data:
                        error_message = f"邮件发送失败：{error_data['error']}"
                except Exception:
                    error_message = f"邮件发送失败：{response.text}"
                
                yield self.create_text_message(error_message)
                
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"网络请求错误：{str(e)}")
        except Exception as e:
            yield self.create_text_message(f"发送邮件时发生错误：{str(e)}")
