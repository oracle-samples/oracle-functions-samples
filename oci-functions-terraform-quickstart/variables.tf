# Copyright (c) 2020 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.

variable "tenancy_id" {}
variable "user_id" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "region" {}
variable "default_compartment_id" {}
variable "function_image" {
  default = "syd.ocir.io/ociateam/helloworld:0.0.1" #Please change this if you have built a docker image with different tags, see README.
}