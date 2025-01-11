# Default values for kaj-dev-argo-testing-srvc.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

deployment:
  name: {{APP_NAME}}
  namespace: {{NAMESPACE}}
  autoPromote: {{AUTO_PROMOTE}}
  delayPromote: {{DELAY_PROMOTE}}
  serviceAccount: service-account-credentials
  isInternal: {{IS_INTERNAL}}
  
replicaCount: {{REPLICA_COUNT}}

image:
  repository: {{ARTIFACT_REGISTRY}}
  pullPolicy: IfNotPresent
  tag: "{{TAGS}}"

service:
  type: ClusterIP
  port: {{APP_PORT}}
  targetPort: {{TARGET_PORT}}

ingress:
  enabled: true
  priority: 10
  domain: {{DOMAIN}}
  greenDomain: {{GREEN_DOMAIN}}
  internalDomain: prd-kaj-gpt-chat-srvc-intl.kiriminaja.io
  className: {{INGRESS}}
  ssl: {{SSL}}
  ssl_redirect: {{SSL_REDIRECT}}
  force_ssl_redirect: {{FORCE_SSL_REDIRECT}}

tls: 
  secretName: bakso-my-id-cert

resources:
  requests:
    cpu: {{RESOURCE_CPU}}
    memory: {{RESOURCE_MEMORY}}
  limits:
    cpu: {{RESOURCE_LIMIT_CPU}}
    memory: {{RESOURCE_LIMIT_MEMORY}}

hpa:
  enabled: true
  spec:
    minReplicas: {{MIN_REPLICAS}}
    maxReplicas: {{MAX_REPLICAS}}
    memory:
      averageUtilization: {{CPU_AVERAGE}}
    cpu:
      averageUtilization: {{MEMORY_AVERAGE}}