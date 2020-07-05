#
# oci-functions-terraform-quickstart version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

locals {
  application_display_name             = "test_app"
  application_config                   = { "name" : "Oracle" }
  function_display_name                = "hello_world"
  function_memory_in_mbs               = 128
  function_timeout_in_seconds          = 120
  function_config                      = { "name" : "Oracle" }
  invoke_function_invoke_function_body = "{\"name\":\"Oracle\"}"
  invoke_function_fn_invoke_type       = "sync"
}

resource "oci_functions_application" "this" {
  #Required
  compartment_id = var.default_compartment_id
  display_name   = local.application_display_name
  subnet_ids     = [module.oci_subnets.subnets.public.id]

  #Optional
  config = local.application_config
}

resource "oci_functions_function" "this" {
  #Required
  application_id = oci_functions_application.this.id
  display_name   = local.function_display_name
  image          = var.function_image
  memory_in_mbs  = local.function_memory_in_mbs

  #Optional
  config             = local.function_config
  timeout_in_seconds = local.function_timeout_in_seconds
}

resource "oci_functions_invoke_function" "this" {
  #Required
  function_id = oci_functions_function.this.id

  #Optional
  invoke_function_body = local.invoke_function_invoke_function_body
  #fn_intent = "${var.invoke_function_fn_intent}"
  fn_invoke_type        = local.invoke_function_fn_invoke_type
  base64_encode_content = false
}

