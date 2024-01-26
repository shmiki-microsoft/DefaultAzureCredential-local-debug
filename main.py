import os
import logging
import sys
from azure.core import exceptions
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient

#ロガーを取得
# azure. で始まるモジュールのログすべてを取得
logger = logging.getLogger('azure') 
# blob ストレージのログのみに絞るとき
# logger = logging.getLogger("azure.storage.blob")
# DefaultAzureCredentialのログのみに絞るとき
# logger = logging.getLogger('azure.identity')
#ログレベルを設定
logger.setLevel(logging.DEBUG)
# ログメッセージのフォーマットを設定
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ログメッセージをコンソールに出力するハンドラーを作成
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
# ロガーにハンドラーを追加
logger.addHandler(handler)

# ログレベルの確認
print(
    f"Logger enabled for ERROR={logger.isEnabledFor(logging.ERROR)}, "
    f"WARNING={logger.isEnabledFor(logging.WARNING)}, "
    f"INFO={logger.isEnabledFor(logging.INFO)}, "
    f"DEBUG={logger.isEnabledFor(logging.DEBUG)}"
)

try:
    #環境変数の設定内容の確認
    print("環境変数の設定内容")
    print(os.getenv("AZURE_CLIENT_ID"))
    print(os.getenv("AZURE_CLIENT_SECRET"))
    print(os.getenv("AZURE_TENANT_ID"))

    # 認証オブジェクトを取得
    # logging_enable=True で HTTTP のログも出力デバックログを出力
    #token_credential = DefaultAzureCredential(logging_enable=True)
    # 取得するトークンのチェック
    # 明示的にトークンを取得 実行しなくてもblob_service_client.list_containers() など
    # 各 Azure リソース側のメソッドが自動的にトークンを呼び出し取得してくれる
    #access_token_raw = token_credential.get_token("https://management.azure.com//.default").token
    #print(jwt.decode(access_token_raw,options={"verify_signature": False}))

    #key vault からシークレットを取得
    KVUri = f"https://{os.getenv("key_vault_name")}.vault.azure.net"
    credential = DefaultAzureCredential(logging_enable=True)
    client = SecretClient(vault_url=KVUri, credential=credential,logging_enable=True,logging_body=True)
    private_key = client.get_secret(os.getenv("key_vault_secret_name")).value
    print(private_key)

    # # BlobServiceClient オブジェクトを作成
    # #logging_enable=Trueでデバックログも  logging_body=True で HTTP のログも出力
    # blob_service_client = BlobServiceClient(
    #     account_url="https://shmikimgdc.blob.core.windows.net",
    #     credential=token_credential,
    #     logging_body=True,
    #     logging_enable=True)
    # # 全てのコンテナをリストし、それらをコンソールに出力
    # container_list = blob_service_client.list_containers()
    # #print("\nList of containers in the storage account:")
    # for container in container_list:
    #     print(container.name)
except (
    exceptions.ClientAuthenticationError,
    exceptions.HttpResponseError
) as e:
    print(e.message)