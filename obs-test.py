# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkobs.v1.region.obs_region import ObsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkobs.v1 import *
from huaweicloudsdkobs.v1.obs_credentials import *

if __name__ == "__main__":
    ak = "IH093VXMHKQIJQZ8VWST"
    sk = "RGZUsapjLBqqKB1aqKUPTqgfBmklMJdlskWDnegC"

    credentials = ObsCredentials(ak, sk)

    client = ObsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(ObsRegion.value_of("la-north-2")) \
        .build()

    try:
        request = ListBucketsRequest()
        response = client.list_buckets(request)
        print('Buckets:')
        print(response)

#        request = CreateBucketRequest()
#        request.bucket_name = "bankchain1"
#        response = client.create_bucket(request)
#        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)