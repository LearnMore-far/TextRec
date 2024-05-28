import oss2
import hashlib
import requests


def md5_hash(string):
    """
    根据给定的字符串生成MD5散列值
    """
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


def upload_file(file_path, file_name):
    seg = file_name
    ext = seg.split('.')[-1]
    object_name = f"knowledge/{md5_hash(seg)}.{ext}"
    response = requests.get("https://v2.mputao.com/v2/sts/token")
    data = response.json()
    credentials = (data['data']['Credentials'])
    sts_access_key_id = credentials['AccessKeyId']
    sts_access_key_secret = credentials['AccessKeySecret']
    security_token = credentials['SecurityToken']

    endpoint = 'https://oss-cn-shenzhen.aliyuncs.com'
    bucket_name = "test-mp-cx"
    # 使用临时访问凭证中的认证信息初始化StsAuth实例。
    auth = oss2.StsAuth(sts_access_key_id,
                        sts_access_key_secret,
                        security_token)
    # 使用StsAuth实例初始化存储空间。
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # 上传Object。
    with open(file_path, 'rb') as f:
        result = bucket.put_object(object_name, f)
    return f'https://test-mp-cx.oss-cn-shenzhen.aliyuncs.com/{object_name}'


if __name__ == '__main__':
    print(upload_file("../data/picture/pdf.png", "pdf.png"))
