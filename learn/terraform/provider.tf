terraform {
required_providers {
  flexibleengine = {
    source = "FlexibleEngineCloud/flexibleengine"
    version = "1.38.0"
   }
 }
}

# Configure the FlexibleEngine Provider
provider "flexibleengine" {
  access_key  = "ENPQT4R7YDI6INOVUGG8"
  secret_key  = "RtyTkxkwlplpu9UriBUlzswPHAnkcMX9G3Rlv2aW"
  domain_name = "OCB0002982"
  region      = "eu-west-0"
}
