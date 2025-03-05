# ==================================================================
# 🚀 INDUSTRY-LEADING AUTO-SCALING FOR AI EXECUTION IN CLOUD
# ✅ Fully Automated, Self-Healing, Secure, and Scalable AI Model Deployment
# ==================================================================

# 🔹 **AWS Auto Scaling for AI Execution**
resource "aws_autoscaling_group" "ai_execution_auto_scaling" {
  desired_capacity     = 2  # Start with 2 instances
  max_size             = 10  # Maximum number of instances
  min_size             = 1   # Minimum number of instances
  vpc_zone_identifier  = ["subnet-0abcde1234567890"]  # Update with your subnet
  launch_configuration = aws_launch_configuration.ai_launch_config.id

  health_check_type          = "EC2"
  health_check_grace_period = 300
  force_delete              = true

  tags = [
    {
      key                 = "Name"
      value               = "AI Execution Instance"
      propagate_at_launch = true
    }
  ]

  # Auto-scaling policies based on CPU utilization
  scaling_policies {
    name                  = "scale-up"
    adjustment_type       = "ChangeInCapacity"
    scaling_adjustment    = 1
    cooldown              = 300
    metric_aggregation_type = "Average"
    estimated_instance_warmup = 60
    target_tracking_scaling {
      target_value        = 70
      predefined_metric_specification {
        predefined_metric_type = "ASGAverageCPUUtilization"
      }
    }
  }

  scaling_policies {
    name                  = "scale-down"
    adjustment_type       = "ChangeInCapacity"
    scaling_adjustment    = -1
    cooldown              = 300
    metric_aggregation_type = "Average"
    estimated_instance_warmup = 60
    target_tracking_scaling {
      target_value        = 30
      predefined_metric_specification {
        predefined_metric_type = "ASGAverageCPUUtilization"
      }
    }
  }
}

resource "aws_launch_configuration" "ai_launch_config" {
  name          = "ai_launch_configuration"
  image_id      = "ami-0abcdef1234567890"  # Replace with the latest AI-optimized AMI
  instance_type = "g5.4xlarge"  # Instance type optimized for AI with NVIDIA GPUs
  key_name      = "ai_execution_key"
  security_groups = [aws_security_group.ai_security_group.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update && sudo apt install -y docker docker-compose python3 python3-pip
              sudo systemctl start docker
              sudo systemctl enable docker
              git clone https://github.com/YourOrg/UnifiedModelAI.git /app
              cd /app/deploy
              docker-compose up --build -d
              EOF
}

# 🔹 **GCP Auto Scaling for AI Execution**
resource "google_compute_instance_group_manager" "ai_execution_gcp_auto_scaling" {
  name = "ai-execution-gcp-autoscale"
  zone = "us-central1-a"
  instance_template = google_compute_instance_template.ai_execution_gcp_template.id
  target_pools = [google_compute_target_pool.ai_execution_target_pool.id]

  # Set Auto-scaling parameters based on CPU usage
  auto_healing {
    initial_delay_sec = 300
  }

  scaling_policy {
    target_utilization = 0.7
    min_num_instances  = 1
    max_num_instances  = 10
  }
}

resource "google_compute_instance_template" "ai_execution_gcp_template" {
  name = "ai-execution-gcp-template"

  instance_description = "AI Execution Template"
  machine_type         = "n1-standard-8"
  disks {
    auto_delete  = true
    boot         = true
    initialize_params {
      image = "projects/deeplearning-platform-release/global/images/family/tf-latest-gpu"
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Include an external IP address
    }
  }

  metadata_startup_script = <<-EOF
              #!/bin/bash
              sudo apt update && sudo apt install -y docker docker-compose python3 python3-pip
              sudo systemctl start docker
              sudo systemctl enable docker
              git clone https://github.com/YourOrg/UnifiedModelAI.git /app
              cd /app/deploy
              docker-compose up --build -d
              EOF
}

# 🔹 **Azure Virtual Machine Auto-Scaling for AI Execution**
resource "azurerm_virtual_machine_scale_set" "ai_execution_azure_autoscale" {
  name                = "ai-execution-azure-scale-set"
  location            = azurerm_resource_group.ai_execution_rg.location
  resource_group_name = azurerm_resource_group.ai_execution_rg.name
  upgrade_mode        = "Manual"

  sku {
    name     = "Standard_NC6"
    capacity = 2  # Minimum number of instances
  }

  # Scaling based on CPU utilization
  autoscale {
    min_instance_count = 1
    max_instance_count = 10
    target_cpu_utilization = 75
  }

  vm_profile {
    name                = "ai-execution-vm"
    os_profile {
      computer_name  = "AIExecution"
      admin_username = "adminuser"
      admin_password = "SecurePassword123!"
    }

    storage_profile {
      os_disk {
        caching              = "ReadWrite"
        managed_disk_type    = "Premium_LRS"
        create_option        = "FromImage"
        disk_size_gb         = 100
      }
    }

    network_profile {
      network_interface {
        name                      = "network-interface"
        primary                   = true
        enable_ip_forwarding      = true
        subnet_id                = azurerm_subnet.ai_subnet.id
      }
    }
  }

  tags = {
    environment = "production"
  }
}

# 🔹 **AI Execution Security Group in Azure**
resource "azurerm_network_security_group" "ai_execution_sg" {
  name                = "ai_execution_security_group"
  location            = azurerm_resource_group.ai_execution_rg.location
  resource_group_name = azurerm_resource_group.ai_execution_rg.name

  security_rule {
    name                       = "allow_ssh"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                  = "Tcp"
    source_port_range         = "*"
    destination_port_range    = "22"
    source_address_prefix     = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow_http"
    priority                   = 101
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                  = "Tcp"
    source_port_range         = "*"
    destination_port_range    = "80"
    source_address_prefix     = "*"
    destination_address_prefix = "*"
  }
}

# 🔹 **Azure Monitoring & Auto-Healing**
resource "azurerm_monitor_diagnostic_setting" "ai_execution_monitoring" {
  name                         = "ai-execution-monitoring"
  target_resource_id           = azurerm_virtual_machine_scale_set.ai_execution_azure_autoscale.id
  log_analytics_destination_type = "Dedicated"
  log_analytics_workspace_id   = azurerm_log_analytics_workspace.ai_workspace.id

  metrics {
    category = "AllMetrics"
    enabled  = true
  }

  logs {
    category = "AuditLogs"
    enabled  = true
  }
}

resource "azurerm_log_analytics_workspace" "ai_workspace" {
  name                = "ai-execution-logs"
  location            = azurerm_resource_group.ai_execution_rg.location
  resource_group_name = azurerm_resource_group.ai_execution_rg.name
  sku                 = "PerGB2018"
}
