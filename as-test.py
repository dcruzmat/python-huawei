# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkas.v1.region.as_region import AsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkas.v1 import *
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2 import *

if __name__ == "__main__":
    ak = "IH093VXMHKQIJQZ8VWST"
    sk = "RGZUsapjLBqqKB1aqKUPTqgfBmklMJdlskWDnegC"
    credentials = BasicCredentials(ak, sk)

    client_vpc = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(VpcRegion.value_of("la-north-2")) \
        .build()
    print("VPC Connected")

    client = AsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(AsRegion.value_of("la-north-2")) \
        .build()
    print("AS Connected")

    try:
        print()
        print("VPCs:")
        request = ListVpcsRequest()
        res_vpc = client_vpc.list_vpcs(request)
        print(res_vpc.vpcs[0])

        print()
        print("Subnets:")
        request = ListSubnetsRequest()
        request.vpc_id = res_vpc.vpcs[0].id
        res_sub = client_vpc.list_subnets(request)
        print(res_sub.subnets[0])

        print()
        print("Creating AS Configuration")
        request = CreateScalingConfigRequest()
        listSecurityGroupsInstanceConfig = [
            SecurityGroups(
                id="a4718d57-538b-41ed-ab7b-27f9892a7498"
            )
        ]
        listDiskInstanceConfig = [
            DiskInfo(
                size=40,
                volume_type="SSD",
                disk_type="SYS"
            )
        ]
        instanceConfigbody = InstanceConfig(
            flavor_ref="s6.xlarge.2",
            image_ref="eafbe389-5898-48c7-a2e4-91a3948de4a0",
            disk=listDiskInstanceConfig,
            user_data="QW5kcmVhMTk4MCQ=",
            security_groups=listSecurityGroupsInstanceConfig
        )
        request.body = CreateScalingConfigOption(
            instance_config=instanceConfigbody,
            scaling_configuration_name="scaling_conf_python"
        )
        response = client.create_scaling_config(request)
        print(response)

        print()
        print("Creating AS Group")
        request = CreateScalingGroupRequest()
        listNetworksbody = [
            Networks(
                id=res_sub.subnets[0].id,
            )
        ]
        request.body = CreateScalingGroupOption(
            vpc_id=res_vpc.vpcs[0].id,
            networks=listNetworksbody,
            max_instance_number=5,
            min_instance_number=1,
            desire_instance_number=1,
            scaling_configuration_id=response.scaling_configuration_id,
            scaling_group_name="scaling_group_python"
        )
        response = client.create_scaling_group(request)
        print(response)

        print()
        print("Enabling AS Group")
        request = ResumeScalingGroupRequest()
        request.scaling_group_id = response.scaling_group_id
        request.body = ResumeScalingGroupOption(
            action="resume"
        )
        response = client.resume_scaling_group(request)
        print(response)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)