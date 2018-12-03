variable "region" {
  type = "string"

  default = "us-west-2"
}

provider "aws" {
  region = "${var.region}"
}

resource "aws_key_pair" "terraform-packer-auto" {
    key_name = "terraform-packer-auto"
    public_key = "${file("../../private/id_terra.pub")}"
}

variable "simple-identity-service-ami" {}

resource "aws_default_vpc" "default" {}

resource "aws_security_group" "simple-identity-sg" {
  name   = "simple-identity-group"
  vpc_id = "${aws_default_vpc.default.id}"

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "simple-identity" {
  ami                         = "${var.simple-identity-service-ami}"
  instance_type               = "t2.micro"
  security_groups             = ["${aws_security_group.simple-identity-sg.name}"]
  associate_public_ip_address = true
}

output "instance_ips" {
  value = ["${aws_instance.simple-identity.public_ip}"]
}
