# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkecs.v2 import *
from huaweicloudsdkims.v2.region.ims_region import ImsRegion
from huaweicloudsdkims.v2 import *
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2 import *
from huaweicloudsdkevs.v2.region.evs_region import *
from huaweicloudsdkevs.v2 import *
import time

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
    client_evs = EvsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(EvsRegion.value_of("la-north-2")) \
        .build()

    try:
        request = CreateVolumeRequest()
        volumebody = CreateVolumeOption(
            availability_zone="la-north-2b",
            name="test-python-evs",
            size=101,
            volume_type="SSD"
        )
        request.body = CreateVolumeRequestBody(
            volume=volumebody
        )
        res_evs = client_evs.create_volume(request)
        print("Disk")
        print(res_evs)

        request = ListImagesRequest()
        request.imagetype = "gold"
        res_ecstype = client_ims.list_images(request)
#        print(res_ecstype.images[0])

        request = ListVpcsRequest()
        res_vpc = client_vpc.list_vpcs(request)
#        print(res_vpc.vpcs[0])

        request = ListSubnetsRequest()
        request.vpc_id = res_vpc.vpcs[0].id
        res_sub = client_vpc.list_subnets(request)
#        print(res_sub.subnets[0])

        print()
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
        res_ecs = client_ecs.create_servers(request)
        print("Server")
        print(res_ecs)

        status= ''
        while(status!='ACTIVE'):
            request = ShowServerRequest()
            request.server_id = res_ecs.server_ids[0]
            response = client_ecs.show_server(request)
            print('VM status ')
            print(response.server.status)
            time.sleep(1)
            status= response.server.status

        print()
        print("Attach disk to ECS")
        request = AttachServerVolumeRequest()
        request.server_id= res_ecs.server_ids[0]
        volumeAttachmentbody = AttachServerVolumeOption(
            volume_id=res_evs.volume_ids[0],
            count=2
        )
        request.body = AttachServerVolumeRequestBody(
            volume_attachment=volumeAttachmentbody
        )
        response = client_ecs.attach_server_volume(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)