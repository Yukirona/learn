resource "flexibleengine_vpc_v1" "example_vpc" {
  name        = "example-vpc"
  cidr        = "192.168.24.0/24"
  description = "Example VPC"
}

resource "flexibleengine_vpc_subnet_v1" "example_subnet" {
  name       = "example-subnet"
  cidr       = "192.168.24.0/24"
  gateway_ip = "192.168.24.1"
  vpc_id     = flexibleengine_vpc_v1.example_vpc.id
}

resource "flexibleengine_compute_instance_v2" "example_ecs" {
  name            = "example-ecs"
  image_name      = "OBS Ubuntu 20.04"
  flavor_id       = "s6.small.1"
  key_pair        = "KeyPair-ericbonnet1"
  security_groups = ["sg-eric.bonnet-2"]

  network {
    uuid = flexibleengine_vpc_subnet_v1.example_subnet.id
  }
}

resource "flexibleengine_vpc_eip" "eip_example" {
  publicip {
    type = "5_bgp"
  }
  bandwidth {
    name       = "test"
    size       = 10
    share_type = "PER"
  }
}


resource "flexibleengine_compute_floatingip_associate_v2" "myip" {
  floating_ip = flexibleengine_vpc_eip.eip_example.publicip.0.ip_address
  instance_id = flexibleengine_compute_instance_v2.example_ecs.id
}

output "eip" {
 value = flexibleengine_compute_instance_v2.example_ecs.floating_ip
}
