# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkecs.v2 import *
from huaweicloudsdkims.v2.region.ims_region import ImsRegion
from huaweicloudsdkims.v2 import *
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2 import *

if __name__ == "__main__":
    ak = "IH093VXMHKQIJQZ8VWST"
    sk = "RGZUsapjLBqqKB1aqKUPTqgfBmklMJdlskWDnegC"

    credentials = BasicCredentials(ak, sk) \

    client_ecs = EcsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(EcsRegion.value_of("la-north-2")) \
        .build()
    client_ims = ImsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(ImsRegion.value_of("la-north-2")) \
        .build()
    client_vpc = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("la-north-2")) \
        .build()

    try:
        request = ListImagesRequest()
        request.imagetype = "gold"
        res_ecstype = client_ims.list_images(request)
        print(res_ecstype.images[0])

        print()
        request = ListVpcsRequest()
        res_vpc = client_vpc.list_vpcs(request)
        print(res_vpc.vpcs[0])

        print()
        request = ListSubnetsRequest()
        request.vpc_id = res_vpc.vpcs[0].id
        res_sub = client_vpc.list_subnets(request)
        print(res_sub.subnets[0])

        rootVolumeServer = PrePaidServerRootVolume(volumetype="SSD")
        listNicsServer = [ PrePaidServerNic(subnet_id=res_sub.subnets[0].id) ]
        prepaidServer = PrePaidServer(
            image_ref=res_ecstype.images[0].id, 
            flavor_ref="s6.xlarge.2", 
            name="test_ecs_python_1", 
            vpcid=res_vpc.vpcs[0].id, 
            nics=listNicsServer,
            root_volume=rootVolumeServer)
        create_server_body = CreateServersRequestBody(dry_run=True, server=prepaidServer)
        request = CreateServersRequest()
        request.body = CreateServersRequestBody(dry_run= False, server=prepaidServer)
        response = client_ecs.create_servers(request)
        print(response)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)