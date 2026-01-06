from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class UspeedoEmailProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            access_key_id = credentials.get("access_key_id")
            access_key_secret = credentials.get("access_key_secret")
            
            if not access_key_id:
                raise ToolProviderCredentialValidationError("ACCESSKEY_ID is required")
            
            if not access_key_secret:
                raise ToolProviderCredentialValidationError("ACCESSKEY_SECRET is required")
            
            # 确保凭证是字符串类型
            if not isinstance(access_key_id, str):
                raise ToolProviderCredentialValidationError("ACCESSKEY_ID must be a string")
            
            if not isinstance(access_key_secret, str):
                raise ToolProviderCredentialValidationError("ACCESSKEY_SECRET must be a string")
            
            # 基本验证：确保凭证不为空（去除首尾空格后）
            if not access_key_id.strip():
                raise ToolProviderCredentialValidationError("ACCESSKEY_ID cannot be empty")
            
            if not access_key_secret.strip():
                raise ToolProviderCredentialValidationError("ACCESSKEY_SECRET cannot be empty")
                
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"Invalid credentials: {str(e)}")

    #########################################################################################
    # If OAuth is supported, uncomment the following functions.
    # Warning: please make sure that the sdk version is 0.4.2 or higher.
    #########################################################################################
    # def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    #     """
    #     Generate the authorization URL for uspeedo-email OAuth.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return ""
        
    # def _oauth_get_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    # ) -> Mapping[str, Any]:
    #     """
    #     Exchange code for access_token.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return dict()

    # def _oauth_refresh_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    # ) -> OAuthCredentials:
    #     """
    #     Refresh the credentials
    #     """
    #     return OAuthCredentials(credentials=credentials, expires_at=-1)
