# Exercice 3

## Création des buckets.

```bash
mc mb local/admin-bucket
mc mb local/manager-bucket
mc mb local/client-bucket
mc ls local
```

Buckets |
-|
admin-bucket/ |
client-bucket/ |
manager-bucket/ |

## Création des policies.

```bash
mc admin policy create local admin-policy "./minio/exos/exo3/admin-policy.json"
mc admin policy create local manager-policy "./minio/exos/exo3/manager-policy.json"
mc admin policy create local client-policy "./minio/exos/exo3/client-policy.json"
mc admin policy list local
```

## Création des comptes admin, manager et user

```bash
mc admin user add local minio-admin "minioadmin"
mc admin user add local minio-manager "miniomanager"
mc admin user add local minio-client "minioclient"
mc admin user list local
```
## Attache des policies.

```bash
mc admin policy attach local admin-policy --user minio-admin
mc admin policy attach local manager-policy --user minio-manager
mc admin policy attach local client-policy --user minio-client
mc admin user list local
```

? | User | Policy
-|-|-
enabled | minio-admin | admin-policy
enabled | minio-client | client-policy
enabled | minio-manager | manager-policy

## Création des alias

```bash
mc alias set minio-admin http://localhost:9000 minio-admin "minioadmin"
mc alias set minio-manager http://localhost:9000 minio-manager "miniomanager"
mc alias set minio-client http://localhost:9000 minio-client "minioclient"
```