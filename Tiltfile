docker_build(
  'wdoyle123/search-api',      
  '.',                        
  live_update=[
    sync('app', '/search-api/app'),
    run('pip install -r search-api/requirements.txt', trigger=['requirements.txt']),
  ]
)

k8s_yaml(kustomize('manifests/base'))

k8s_resource(
  'search-api-deployment',
  port_forwards=8000
)

k8s_resource(
  'search-db',
  port_forwards=5432
)

