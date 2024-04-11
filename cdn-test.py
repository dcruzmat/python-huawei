# coding: utf-8

from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcdn.v2.region.cdn_region import CdnRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcdn.v2 import *

from huaweicloudsdkscm.v3.region.scm_region import ScmRegion
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkscm.v3 import *
import json

if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
    #ak = __import__('os').getenv("CLOUD_SDK_AK")
    #sk = __import__('os').getenv("CLOUD_SDK_SK")
    ak = "IH093VXMHKQIJQZ8VWST"
    sk = "RGZUsapjLBqqKB1aqKUPTqgfBmklMJdlskWDnegC"

    try:
        credentials = GlobalCredentials(ak, sk)
        client = ScmClient.new_builder() \
			.with_credentials(credentials) \
			.with_region(ScmRegion.value_of("ap-southeast-1")) \
			.build()
        print("SCM connected")

        request = ListCertificatesRequest()
        response = client.list_certificates(request)
        print(response)

        client = CdnClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(CdnRegion.value_of("ap-southeast-1")) \
            .build()
        print("CDN connected")

#        domain_body = json.loads('{"domain":{"domain_name":"subdominio1.davidcm.org","business_type":"web","service_area":"outside_mainland_china","sources":[{"ip_or_domain":"cra-test.obs-website.la-north-2.myhuaweicloud.com","origin_type":"obs_bucket","active_standby":"1","enable_obs_web_hosting":"1"}]}}')
        sources1 = [Sources(ip_or_domain='cra-test.obs-website.la-north-2.myhuaweicloud.com', origin_type='obs_bucket', active_standby=1, enable_obs_web_hosting=1)]
        domain_body = DomainBody(domain_name='subdominio1.davidcm.org', business_type='web', sources=sources1, service_area='outside_mainland_china')
        request = CreateDomainRequest()
        request.body = CreateDomainRequestBody(domain=domain_body)
        response = client.create_domain(request)
        print(response)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)