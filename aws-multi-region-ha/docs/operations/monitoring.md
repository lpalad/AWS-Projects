# Infrastructure Monitoring Guide
Location: /docs/operations/monitoring.md

## Overview
This document outlines the comprehensive monitoring setup across both regions (Sydney and Oregon) for infrastructure, applications, and databases.

## File Location
This document is part of the following structure:
- /docs/operations/monitoring.md
- Part of aws-multi-region-ha repository
- Operations documentation section

## CloudWatch Implementation
### Metrics Configuration
- EC2 Instances:
  - CPU Utilization
  - Memory Usage
  - Network I/O
  - Disk Operations
  - Status Checks

- Application Load Balancer:
  - Request Count
  - Target Response Time
  - HTTP Error Codes
  - Healthy Host Count
  - Rejected Connection Count

- Aurora Database:
  - CPU Utilization
  - FreeableMemory
  - DatabaseConnections
  - ReadIOPS/WriteIOPS
  - ReplicationLag
  - BackupRetentionPeriod

### Alarm Setup
- EC2 Alarms:
  - High CPU (>80%, 5 minutes)
  - Memory Usage (>85%, 5 minutes)
  - Status Check Failures
  - Instance Health

- ALB Alarms:
  - High Latency (>2 seconds)
  - 5XX Error Rate (>1%)
  - Unhealthy Host Count
  - Rejected Connections

- Aurora Alarms:
  - High CPU (>75%, 5 minutes)
  - Low Memory (<2GB)
  - Replication Lag (>1 minute)
  - Connection Count (>85% max)

## Log Management
### CloudWatch Logs
- Application Logs:
  - Web Server Access Logs
  - API Server Logs
  - Application Error Logs
  - Security Logs

- System Logs:
  - EC2 System Logs
  - CloudWatch Agent Logs
  - SSM Agent Logs

- Database Logs:
  - Aurora Error Logs
  - Slow Query Logs
  - Audit Logs
  - General Logs

### Log Retention
- Critical Logs: 1 year
- Operation Logs: 3 months
- System Logs: 1 month
- Access Logs: 6 months

## Performance Monitoring
### Enhanced Monitoring
- Aurora Performance:
  - Query Performance
  - Lock Waits
  - Transaction Logs
  - Table Statistics

- API Performance:
  - Response Times
  - Error Rates
  - Token Usage
  - Endpoint Statistics

### Resource Utilization
- Network Traffic:
  - Inbound/Outbound
  - Protocol Distribution
  - Peak Usage Times
  - Bandwidth Consumption

- Storage Metrics:
  - EBS Volume Usage
  - IOPS Consumption
  - Throughput
  - Latency

## Alerting Configuration
### SNS Topics
- Critical Alerts:
  - Service Outages
  - Security Incidents
  - Database Issues
  - High Priority Alarms

- Operation Alerts:
  - Performance Degradation
  - Capacity Warnings
  - Backup Status
  - Maintenance Events

### Alert Routing
- Emergency Contacts:
  - Service Down
  - Security Breach
  - Data Loss Risk

- Operations Team:
  - Performance Issues
  - Capacity Planning
  - Maintenance Tasks

## Dashboard Setup
### Global Dashboard
- Service Health:
  - Regional Status
  - Critical Metrics
  - Active Alerts
  - Recent Events

- Performance Overview:
  - Response Times
  - Error Rates
  - Resource Usage
  - Cost Metrics

### Regional Dashboards
- Sydney Region:
  - Web Servers Status
  - ALB Metrics
  - Primary Database
  - Network Health

- Oregon Region:
  - API Server Status
  - Read Replica Stats
  - Application Metrics
  - Resource Usage

## Cost Monitoring
### Resource Costs
- Compute Resources:
  - EC2 Instances
  - Load Balancers
  - Data Transfer

- Database Costs:
  - Aurora Instances
  - Storage Usage
  - Backup Storage
  - Replication Costs

### Budget Alerts
- Monthly Thresholds:
  - 80% Budget Warning
  - 90% Budget Alert
  - Service-specific Alerts
  - Unusual Usage Detection

## Maintenance Windows
### Scheduled Maintenance
- Database Maintenance:
  - Patch Updates
  - Parameter Changes
  - Backup Verification

- System Updates:
  - Security Patches
  - OS Updates
  - Application Updates

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://aws.leonardspalad.com/  
LinkedIn: https://www.linkedin.com/in/leonardspalad/
