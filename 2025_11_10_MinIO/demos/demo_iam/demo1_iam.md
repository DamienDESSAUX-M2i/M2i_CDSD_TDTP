# IAM

Set user_key and secret_key to an alias.
```bash
mc alias set local http://localhost:9000 minioadmin minioadmin
```

Add a user to an alias.
```bash
mc admin user add local etl_user "etl_user"
```

List users of an alias.
```bash
mc admin user list local
```

Create an alias for a user.
```bash
mc alias etl http://localhost:9000 etl_user "etl_user"
```

Create a policy.
```bash
mc admin policy create local etl-bronze "./2025_11_10_MinIO/demos/demo_iam/etl_policy.json"
```

Attach a policy to a user.
```bash
mc admin policy attach local etl-bronze --user etl_user
```