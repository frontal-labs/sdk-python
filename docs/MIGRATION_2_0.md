# Migrating to Frontal Python SDK 2.0

Version 2.0 gives inventory-backed methods resource-oriented names and semantic
path argument names. The HTTP method, route, request/response behavior, and
service namespace remain governed by `contracts/sdk-endpoints.json` and the
committed OpenAPI snapshots. Existing names are not retained as aliases in 2.0;
use this table to update call sites.

The transport also distinguishes omitted bodies from JSON values: omit `body`
to send no body, pass `body=None` for JSON `null`, and pass `body={}` for an
empty object. `FrontalError.transient` indicates a temporary failure;
`safe_to_retry` indicates that replay is safe for the operation. `retryable`
remains a compatibility alias for `transient` in 2.0.

## Method and argument mapping

| Service | 1.x method | 2.0 method | Path argument changes |
| --- | --- | --- | --- |
| `agents` | `delete_agents_by_param_1` | `delete` | param_1 → id |
| `agents` | `get_agents` | `list` | — |
| `agents` | `get_agents_by_param_1` | `get` | param_1 → id |
| `agents` | `get_agents_by_param_1_runs` | `runs.list` | param_1 → agent_id |
| `agents` | `get_agents_by_param_1_versions` | `versions.list` | param_1 → agent_id |
| `agents` | `get_agents_runs_by_param_1` | `runs.get` | param_1 → id |
| `agents` | `get_agents_runs_by_param_1_conversation` | `runs.conversation` | param_1 → id |
| `agents` | `post_agents` | `create` | — |
| `agents` | `post_agents_by_param_1_rollback` | `rollback` | param_1 → id |
| `agents` | `post_agents_by_param_1_runs` | `runs.create` | param_1 → agent_id |
| `agents` | `put_agents_by_param_1` | `update` | param_1 → id |
| `agents` | `stream_agents_runs_by_param_1_stream` | `runs.stream` | param_1 → id |
| `ai` | `get_internal_models` | `list_model_records` | — |
| `ai` | `get_internal_models_defaults` | `list_defaults` | — |
| `ai` | `post_ai_chat_completions` | `create_completion` | — |
| `ai` | `post_internal_embeddings` | `create_embedding` | — |
| `ai` | `post_internal_predictions` | `create_prediction` | — |
| `audit` | `get_audit_events` | `list_events` | — |
| `audit` | `get_audit_events_by_param_1` | `get_event` | param_1 → event_id |
| `audit` | `post_audit_events` | `create_event` | — |
| `auth` | `delete_auth_account_mfa_by_param_1` | `delete_mfa` | param_1 → mfa_id |
| `auth` | `delete_auth_account_security_api_keys_by_param_1` | `delete_api_key` | param_1 → api_key_id |
| `auth` | `delete_auth_account_security_devices_by_param_1` | `delete_device` | param_1 → device_id |
| `auth` | `delete_auth_account_sessions_by_param_1` | `delete_session` | param_1 → session_id |
| `auth` | `delete_auth_admin_users_by_param_1` | `delete_user` | param_1 → user_id |
| `auth` | `delete_auth_admin_users_by_param_1_factors_by_param_2` | `delete_factor_for_user` | param_1 → user_id, param_2 → factor_id |
| `auth` | `delete_auth_factors_by_param_1` | `delete_factor` | param_1 → factor_id |
| `auth` | `delete_auth_user_identities_by_param_1` | `delete_identity` | param_1 → identity_id |
| `auth` | `get_auth_account_mfa_by_param_1` | `get_mfa` | param_1 → mfa_id |
| `auth` | `get_auth_account_security_api_keys` | `list_api_keys` | — |
| `auth` | `get_auth_account_security_api_keys_by_param_1` | `get_api_key` | param_1 → api_key_id |
| `auth` | `get_auth_account_security_devices` | `list_devices` | — |
| `auth` | `get_auth_account_security_devices_by_param_1` | `get_device` | param_1 → device_id |
| `auth` | `get_auth_account_sessions` | `list_sessions` | — |
| `auth` | `get_auth_admin_users` | `list_users` | — |
| `auth` | `get_auth_admin_users_by_param_1` | `get_user` | param_1 → user_id |
| `auth` | `get_auth_admin_users_by_param_1_factors` | `list_user_factors` | param_1 → user_id |
| `auth` | `get_auth_factors` | `list_factors` | — |
| `auth` | `get_auth_user_identities` | `list_identities` | — |
| `auth` | `post_auth_account_mfa_by_param_1_challenge` | `challenge_mfa` | param_1 → mfa_id |
| `auth` | `post_auth_account_mfa_by_param_1_verify` | `verify_mfa` | param_1 → mfa_id |
| `auth` | `post_auth_account_security_api_keys` | `create_api_key` | — |
| `auth` | `post_auth_account_security_devices` | `create_device` | — |
| `auth` | `post_auth_account_security_devices_by_param_1_trust` | `trust_device` | param_1 → device_id |
| `auth` | `post_auth_account_sessions_by_param_1_extend` | `extend_session` | param_1 → session_id |
| `auth` | `post_auth_admin_users` | `create_user` | — |
| `auth` | `post_auth_factors` | `create_factor` | — |
| `auth` | `post_auth_factors_by_param_1_challenge` | `challenge_factor` | param_1 → factor_id |
| `auth` | `post_auth_factors_by_param_1_verify` | `verify_factor` | param_1 → factor_id |
| `auth` | `post_auth_user_identities` | `create_identity` | — |
| `auth` | `put_auth_account_security_api_keys_by_param_1` | `update_api_key` | param_1 → api_key_id |
| `auth` | `put_auth_admin_users_by_param_1` | `update_user` | param_1 → user_id |
| `billing` | `download_billing_invoices_by_param_1_pdf` | `download_invoice_pdf` | param_1 → invoice_id |
| `billing` | `get_billing_addons_by_param_1_entitlements` | `list_addon_entitlements` | param_1 → addon_id |
| `billing` | `get_billing_customers_by_param_1_entitlements` | `list_customer_entitlements` | param_1 → customer_id |
| `billing` | `get_billing_customers_by_param_1_invoices_summary` | `get_customer_invoices_summary` | param_1 → customer_id |
| `billing` | `get_billing_customers_by_param_1_usage` | `get_customer_usage` | param_1 → customer_id |
| `billing` | `get_billing_customers_by_param_1_wallets` | `list_customer_wallets` | param_1 → customer_id |
| `billing` | `get_billing_customers_portal_by_param_1` | `get_portal` | param_1 → portal_id |
| `billing` | `get_billing_plans_by_param_1_entitlements` | `list_plan_entitlements` | param_1 → plan_id |
| `billing` | `get_billing_prices_lookup_by_param_1` | `get_lookup` | param_1 → lookup_id |
| `billing` | `get_billing_subscriptions_by_param_1_entitlements` | `list_subscription_entitlements` | param_1 → subscription_id |
| `billing` | `get_billing_wallets_by_param_1_balance_real_time` | `get_wallet_balance_real_time` | param_1 → wallet_id |
| `billing` | `get_billing_wallets_by_param_1_transactions` | `list_wallet_transactions` | param_1 → wallet_id |
| `billing` | `post_billing_invoices_by_param_1_finalize` | `finalize_invoice` | param_1 → invoice_id |
| `billing` | `post_billing_invoices_by_param_1_void` | `void_invoice` | param_1 → invoice_id |
| `billing` | `post_billing_meters_by_param_1_disable` | `disable_meter` | param_1 → meter_id |
| `billing` | `post_billing_plans_by_param_1_clone` | `clone_plan` | param_1 → plan_id |
| `billing` | `post_billing_subscriptions_by_param_1_activate` | `activate_subscription` | param_1 → subscription_id |
| `billing` | `post_billing_subscriptions_by_param_1_cancel` | `cancel_subscription` | param_1 → subscription_id |
| `billing` | `post_billing_subscriptions_by_param_1_pause` | `pause_subscription` | param_1 → subscription_id |
| `billing` | `post_billing_subscriptions_by_param_1_resume` | `resume_subscription` | param_1 → subscription_id |
| `billing` | `post_billing_wallets_by_param_1_terminate` | `terminate_wallet` | param_1 → wallet_id |
| `billing` | `post_billing_wallets_by_param_1_top_up` | `top_up_wallet` | param_1 → wallet_id |
| `blob` | `delete_blob_object_by_param_1_by_param_2` | `delete_object` | param_1 → container, param_2 → object_key |
| `blob` | `get_blob_object_by_param_1_by_param_2` | `get_object` | param_1 → container, param_2 → object_key |
| `blob` | `get_blob_object_info_by_param_1_by_param_2` | `get_object_info` | param_1 → container, param_2 → object_key |
| `blob` | `post_blob_object_list_by_param_1` | `post_blob_object_list_by_list_id` | param_1 → list_id |
| `blob` | `post_blob_object_sign_by_param_1_by_param_2` | `sign_object` | param_1 → container, param_2 → object_key |
| `blob` | `upload_blob_object_by_param_1_by_param_2` | `upload_object` | param_1 → container, param_2 → object_key |
| `connectors` | `delete_connectors_installations_by_param_1` | `delete_installation` | param_1 → installation_id |
| `connectors` | `get_connectors_catalog_by_param_1` | `get_catalog` | param_1 → catalog_id |
| `connectors` | `get_connectors_connection_tests_by_param_1` | `get_connection_test` | param_1 → connection_test_id |
| `connectors` | `get_connectors_installations` | `list_installations` | — |
| `connectors` | `get_connectors_installations_by_param_1` | `get_installation` | param_1 → installation_id |
| `connectors` | `get_diagnostics` | `list_diagnostics` | — |
| `connectors` | `patch_connectors_installations_by_param_1` | `update_installation` | param_1 → installation_id |
| `connectors` | `post_connectors_installations` | `create_installation` | — |
| `connectors` | `post_connectors_installations_by_param_1_pause` | `pause_installation` | param_1 → installation_id |
| `connectors` | `post_connectors_installations_by_param_1_resume` | `resume_installation` | param_1 → installation_id |
| `connectors` | `post_connectors_sync_runs_by_param_1_replay` | `replay_sync_run` | param_1 → sync_run_id |
| `data` | `get_data_aggregations_aggregations` | `list_aggregations` | — |
| `data` | `get_data_aggregations_aggregations_by_param_1` | `get_aggregation` | param_1 → aggregation_id |
| `data` | `get_data_archival_archival_policies` | `list_policies` | — |
| `data` | `get_data_archival_archival_policies_by_param_1` | `get_policy` | param_1 → policy_id |
| `data` | `get_data_enrichment_enrichment_profiles` | `list_enrichment_profiles` | — |
| `data` | `get_data_enrichment_enrichment_profiles_by_param_1` | `get_enrichment_profile` | param_1 → profile_id |
| `data` | `get_data_exports_exports` | `list_exports` | — |
| `data` | `get_data_exports_exports_by_param_1` | `get_export` | param_1 → export_id |
| `data` | `get_data_normalization_normalization_profiles` | `list_normalization_profiles` | — |
| `data` | `get_data_normalization_normalization_profiles_by_param_1` | `get_normalization_profile` | param_1 → profile_id |
| `data` | `get_data_quality_quality_rulesets` | `list_rulesets` | — |
| `data` | `get_data_quality_quality_rulesets_by_param_1` | `get_ruleset` | param_1 → ruleset_id |
| `data` | `get_data_schemas_schemas` | `list_schemas` | — |
| `data` | `get_data_schemas_schemas_by_param_1` | `get_schema_ref` | param_1 → schema_ref |
| `data` | `get_data_serving_serving_products` | `list_products` | — |
| `data` | `get_data_serving_serving_products_by_param_1` | `get_product` | param_1 → product_id |
| `data` | `get_data_streams_streams` | `list_streams` | — |
| `data` | `get_data_streams_streams_by_param_1` | `get_stream` | param_1 → stream_id |
| `data` | `get_data_sync_sync_jobs` | `list_jobs` | — |
| `data` | `get_data_sync_sync_jobs_by_param_1` | `get_job` | param_1 → job_id |
| `data` | `get_data_transformations_transformations` | `list_transformations` | — |
| `data` | `get_data_transformations_transformations_by_param_1` | `get_transformation` | param_1 → transformation_id |
| `data` | `post_data_aggregations_aggregations` | `create_aggregation` | — |
| `data` | `post_data_aggregations_aggregations_by_param_1_executions` | `create_execution_for_aggregation` | param_1 → aggregation_id |
| `data` | `post_data_archival_archival_policies` | `create_policy` | — |
| `data` | `post_data_archival_archival_policies_by_param_1_executions` | `create_execution_for_policy` | param_1 → policy_id |
| `data` | `post_data_enrichment_enrichment_profiles` | `create_enrichment_profile` | — |
| `data` | `post_data_enrichment_enrichment_profiles_by_param_1_executions` | `create_execution_for_enrichment_profile` | param_1 → profile_id |
| `data` | `post_data_exports_exports` | `create_export` | — |
| `data` | `post_data_exports_exports_by_param_1_executions` | `create_execution_for_export` | param_1 → export_id |
| `data` | `post_data_normalization_normalization_profiles` | `create_normalization_profile` | — |
| `data` | `post_data_normalization_normalization_profiles_by_param_1_executions` | `create_execution_for_normalization_profile` | param_1 → profile_id |
| `data` | `post_data_quality_quality_rulesets` | `create_ruleset` | — |
| `data` | `post_data_quality_quality_rulesets_by_param_1_evaluations` | `create_evaluation_for_ruleset` | param_1 → ruleset_id |
| `data` | `post_data_schemas_schemas` | `create_schema` | — |
| `data` | `post_data_serving_serving_products` | `create_product` | — |
| `data` | `post_data_serving_serving_products_by_param_1_refreshes` | `create_refresh_for_product` | param_1 → product_id |
| `data` | `post_data_streams_streams` | `create_stream` | — |
| `data` | `post_data_streams_streams_by_param_1_deliveries` | `create_delivery_for_stream` | param_1 → stream_id |
| `data` | `post_data_sync_sync_jobs` | `create_job` | — |
| `data` | `post_data_sync_sync_jobs_by_param_1_executions` | `create_execution_for_job` | param_1 → job_id |
| `data` | `post_data_transformations_transformations` | `create_transformation` | — |
| `data` | `post_data_transformations_transformations_by_param_1_executions` | `create_execution_for_transformation` | param_1 → transformation_id |
| `governance` | `delete_policies_by_param_1` | `delete_policy` | param_1 → policy_id |
| `governance` | `delete_roles_by_param_1` | `delete_role` | param_1 → role_id |
| `governance` | `get_compliance_assessments` | `list_assessments` | — |
| `governance` | `get_compliance_assessments_by_param_1` | `get_assessment` | param_1 → assessment_id |
| `governance` | `get_compliance_frameworks` | `list_frameworks` | — |
| `governance` | `get_compliance_violations` | `list_violations` | — |
| `governance` | `get_permissions` | `list_permissions` | — |
| `governance` | `get_permissions_by_param_1` | `get_permission` | param_1 → permission_id |
| `governance` | `get_policies` | `list_policies` | — |
| `governance` | `get_policies_by_param_1` | `get_policy` | param_1 → policy_id |
| `governance` | `get_policies_by_param_1_versions` | `list_policy_versions` | param_1 → policy_id |
| `governance` | `get_policies_templates` | `list_templates` | — |
| `governance` | `get_roles` | `list_roles` | — |
| `governance` | `get_roles_by_param_1` | `get_role` | param_1 → role_id |
| `governance` | `post_compliance_assessments` | `create_assessment` | — |
| `governance` | `post_compliance_violations_by_param_1_resolve` | `resolve_violation` | param_1 → violation_id |
| `governance` | `post_permissions` | `create_permission` | — |
| `governance` | `post_policies` | `create_policy` | — |
| `governance` | `post_roles` | `create_role` | — |
| `governance` | `put_policies_by_param_1` | `update_policy` | param_1 → policy_id |
| `lineage` | `get_lineage_edges` | `list_edges` | — |
| `lineage` | `get_lineage_edges_by_param_1` | `get_edge` | param_1 → edge_id |
| `lineage` | `get_lineage_nodes` | `list_nodes` | — |
| `lineage` | `get_lineage_nodes_by_param_1` | `get_node` | param_1 → node_id |
| `lineage` | `get_lineage_nodes_by_param_1_trace` | `get_node_trace` | param_1 → node_id |
| `observability` | `delete_observability_alerts_by_param_1` | `delete_alert` | param_1 → alert_id |
| `observability` | `delete_observability_dashboards_by_param_1` | `delete_dashboard` | param_1 → dashboard_id |
| `observability` | `get_observability_alerts` | `list_alerts` | — |
| `observability` | `get_observability_alerts_incidents` | `list_incidents` | — |
| `observability` | `get_observability_dashboards` | `list_dashboards` | — |
| `observability` | `get_observability_dashboards_by_param_1` | `get_dashboard` | param_1 → dashboard_id |
| `observability` | `get_observability_events_stats` | `list_stats` | — |
| `observability` | `get_observability_metrics` | `list_metrics` | — |
| `observability` | `get_observability_traces` | `list_traces` | — |
| `observability` | `get_observability_traces_by_param_1` | `get_trace` | param_1 → trace_id |
| `observability` | `post_observability_alerts` | `create_alert` | — |
| `observability` | `post_observability_alerts_by_param_1_disable` | `disable_alert` | param_1 → alert_id |
| `observability` | `post_observability_alerts_by_param_1_enable` | `enable_alert` | param_1 → alert_id |
| `observability` | `post_observability_dashboards` | `create_dashboard` | — |
| `observability` | `post_observability_dashboards_by_param_1_share` | `share_dashboard` | param_1 → dashboard_id |
| `observability` | `post_observability_events` | `create_event` | — |
| `observability` | `put_observability_alerts_by_param_1` | `update_alert` | param_1 → alert_id |
| `observability` | `put_observability_dashboards_by_param_1` | `update_dashboard` | param_1 → dashboard_id |
| `ontology` | `delete_ontology_objects_object_types_by_param_1` | `delete_object_type` | param_1 → object_type_id |
| `ontology` | `delete_ontology_objects_objects_by_param_1` | `delete_object` | param_1 → object_id |
| `ontology` | `delete_ontology_reasoning_rules_by_param_1` | `delete_reasoning_rule` | param_1 → rule_id |
| `ontology` | `delete_ontology_relationships_relationship_types_by_param_1` | `delete_relationship_type` | param_1 → relationship_type_id |
| `ontology` | `delete_ontology_relationships_relationships_by_param_1` | `delete_relationship` | param_1 → relationship_id |
| `ontology` | `delete_ontology_rollouts_rollouts_by_param_1` | `delete_rollout` | param_1 → rollout_id |
| `ontology` | `delete_ontology_rollups_rollups_by_param_1` | `delete_rollup` | param_1 → rollup_id |
| `ontology` | `delete_ontology_schemas_schemas_by_param_1` | `delete_schema` | param_1 → schema_id |
| `ontology` | `delete_ontology_validation_rules_by_param_1` | `delete_validation_rule` | param_1 → rule_id |
| `ontology` | `delete_ontology_versions_versions_by_param_1` | `delete_version` | param_1 → version_id |
| `ontology` | `get_ontology_events_events` | `list_events` | — |
| `ontology` | `get_ontology_events_events_by_param_1` | `get_event` | param_1 → event_id |
| `ontology` | `get_ontology_events_events_checkpoints_by_param_1` | `get_consumer` | param_1 → consumer |
| `ontology` | `get_ontology_objects_object_types` | `list_object_types` | — |
| `ontology` | `get_ontology_objects_object_types_by_param_1` | `get_object_type` | param_1 → object_type_id |
| `ontology` | `get_ontology_objects_objects` | `list_objects` | — |
| `ontology` | `get_ontology_objects_objects_by_param_1` | `get_object` | param_1 → object_id |
| `ontology` | `get_ontology_reasoning_rules` | `list_reasoning_rules` | — |
| `ontology` | `get_ontology_relationships_relationship_types` | `list_relationship_types` | — |
| `ontology` | `get_ontology_relationships_relationships` | `list_relationships` | — |
| `ontology` | `get_ontology_relationships_relationships_by_param_1` | `get_relationship` | param_1 → relationship_id |
| `ontology` | `get_ontology_rollouts_rollouts` | `list_rollouts` | — |
| `ontology` | `get_ontology_rollouts_rollouts_by_param_1` | `get_rollout` | param_1 → rollout_id |
| `ontology` | `get_ontology_rollouts_rollouts_by_param_1_status` | `list_rollout_status` | param_1 → rollout_id |
| `ontology` | `get_ontology_rollups_rollup_results_by_param_1` | `get_execution` | param_1 → execution_id |
| `ontology` | `get_ontology_rollups_rollups` | `list_rollups` | — |
| `ontology` | `get_ontology_rollups_rollups_by_param_1` | `get_rollup` | param_1 → rollup_id |
| `ontology` | `get_ontology_rollups_rollups_by_param_1_result` | `get_rollup_result` | param_1 → rollup_id |
| `ontology` | `get_ontology_schemas_schemas` | `list_schemas` | — |
| `ontology` | `get_ontology_schemas_schemas_by_param_1` | `get_schema` | param_1 → schema_id |
| `ontology` | `get_ontology_validation_rules` | `list_validation_rules` | — |
| `ontology` | `get_ontology_validation_rules_by_param_1` | `get_rule` | param_1 → rule_id |
| `ontology` | `get_ontology_versions_release_bundles` | `list_release_bundles` | — |
| `ontology` | `get_ontology_versions_release_bundles_by_param_1` | `get_bundle` | param_1 → bundle_id |
| `ontology` | `get_ontology_versions_versions_by_param_1` | `get_version` | param_1 → version_id |
| `ontology` | `post_ontology_engine_ontologies_compare_versions` | `create_compare_version` | — |
| `ontology` | `post_ontology_engine_ontologies_infer_classes` | `create_infer_class` | — |
| `ontology` | `post_ontology_engine_ontologies_infer_properties` | `create_infer_property` | — |
| `ontology` | `post_ontology_events_events` | `create_event` | — |
| `ontology` | `post_ontology_events_events_checkpoints` | `create_checkpoint` | — |
| `ontology` | `post_ontology_extract_extract_coreferences` | `create_coreference` | — |
| `ontology` | `post_ontology_extract_extract_entities` | `create_entity` | — |
| `ontology` | `post_ontology_extract_extract_events` | `create_extract_event` | — |
| `ontology` | `post_ontology_extract_extract_relations` | `create_relation` | — |
| `ontology` | `post_ontology_extract_extract_triplets` | `create_triplet` | — |
| `ontology` | `post_ontology_reasoning_facts` | `create_fact` | — |
| `ontology` | `post_ontology_reasoning_rules` | `create_reasoning_rule` | — |
| `ontology` | `post_ontology_rollouts_rollouts` | `create_rollout` | — |
| `ontology` | `post_ontology_rollouts_rollouts_by_param_1_pause` | `pause_rollout` | param_1 → rollout_id |
| `ontology` | `post_ontology_rollouts_rollouts_by_param_1_resume` | `resume_rollout` | param_1 → rollout_id |
| `ontology` | `post_ontology_rollouts_rollouts_by_param_1_rollback` | `rollback_rollout` | param_1 → rollout_id |
| `ontology` | `post_ontology_rollouts_rollouts_by_param_1_start` | `start_rollout` | param_1 → rollout_id |
| `ontology` | `post_ontology_rollups_rollups` | `create_rollup` | — |
| `ontology` | `post_ontology_rollups_rollups_by_param_1_execute` | `execute_rollup` | param_1 → rollup_id |
| `ontology` | `post_ontology_rollups_rollups_by_param_1_preview` | `preview_rollup` | param_1 → rollup_id |
| `ontology` | `post_ontology_schemas_schemas` | `create_schema` | — |
| `ontology` | `post_ontology_transformations_transformations` | `create_transformation` | — |
| `ontology` | `post_ontology_validation_rules` | `create_validation_rule` | — |
| `ontology` | `post_ontology_versions_release_bundles` | `create_release_bundle` | — |
| `ontology` | `post_ontology_versions_versions` | `create_version` | — |
| `ontology` | `put_ontology_objects_object_types_by_param_1` | `update_object_type` | param_1 → object_type_id |
| `ontology` | `put_ontology_objects_objects_by_param_1` | `update_object` | param_1 → object_id |
| `ontology` | `put_ontology_reasoning_rules_by_param_1` | `update_rule` | param_1 → rule_id |
| `ontology` | `put_ontology_relationships_relationships_by_param_1` | `update_relationship` | param_1 → relationship_id |
| `ontology` | `put_ontology_rollouts_rollouts_by_param_1` | `update_rollout` | param_1 → rollout_id |
| `ontology` | `put_ontology_rollups_rollups_by_param_1` | `update_rollup` | param_1 → rollup_id |
| `pipelines` | `get_data_pipelines_capabilities` | `list_capabilities` | — |
| `pipelines` | `get_data_pipelines_pipeline_runs` | `list_pipeline_runs` | — |
| `pipelines` | `get_data_pipelines_pipeline_runs_by_param_1` | `get_run` | param_1 → run_id |
| `pipelines` | `get_data_pipelines_pipelines` | `list_pipelines` | — |
| `pipelines` | `get_data_pipelines_pipelines_by_param_1` | `get_definition` | param_1 → definition_id |
| `pipelines` | `get_data_pipelines_runs` | `list_runs` | — |
| `pipelines` | `post_data_pipelines_pipelines` | `create_pipeline` | — |
| `pipelines` | `post_data_pipelines_runs` | `create_run` | — |
| `pipelines` | `stream_data_pipelines_pipeline_runs_by_param_1` | `stream_data_pipelines_pipeline_runs_by_run_id` | param_1 → run_id |
| `sandbox` | `get_sandbox_languages` | `list_languages` | — |
| `schedules` | `delete_workflows_schedules_by_param_1` | `delete_schedule` | param_1 → schedule_id |
| `schedules` | `get_workflows_schedules` | `list_schedules` | — |
| `schedules` | `get_workflows_schedules_by_param_1` | `get_schedule` | param_1 → schedule_id |
| `schedules` | `patch_workflows_schedules_by_param_1` | `update_schedule` | param_1 → schedule_id |
| `schedules` | `post_workflows_schedules` | `create_schedule` | — |
| `schedules` | `post_workflows_schedules_by_param_1_pause` | `pause_schedule` | param_1 → schedule_id |
| `schedules` | `post_workflows_schedules_by_param_1_resume` | `resume_schedule` | param_1 → schedule_id |
| `schedules` | `post_workflows_schedules_by_param_1_trigger` | `trigger_schedule` | param_1 → schedule_id |
| `webhooks` | `delete_webhooks_by_param_1` | `delete_webhook` | param_1 → webhook_id |
| `webhooks` | `get_webhooks` | `list_webhooks` | — |
| `webhooks` | `get_webhooks_by_param_1` | `get_webhook` | param_1 → webhook_id |
| `webhooks` | `get_webhooks_deliveries` | `list_deliveries` | — |
| `webhooks` | `get_webhooks_deliveries_by_param_1` | `get_delivery` | param_1 → delivery_id |
| `webhooks` | `get_webhooks_stats` | `list_stats` | — |
| `webhooks` | `post_webhooks` | `create_webhook` | — |
| `webhooks` | `post_webhooks_by_param_1_rotate_secret` | `rotate_secret_webhook` | param_1 → webhook_id |
| `webhooks` | `post_webhooks_deliveries_by_param_1_retry` | `retry_delivery` | param_1 → delivery_id |
| `webhooks` | `put_webhooks_by_param_1` | `update_webhook` | param_1 → webhook_id |
| `workflows` | `delete_workflows_by_param_1` | `delete_workflow` | param_1 → workflow_id |
| `workflows` | `get_workflows` | `list_workflows` | — |
| `workflows` | `get_workflows_approvals` | `list_approvals` | — |
| `workflows` | `get_workflows_approvals_by_param_1` | `get_approval` | param_1 → approval_id |
| `workflows` | `get_workflows_by_param_1` | `get_workflow` | param_1 → workflow_id |
| `workflows` | `get_workflows_executions` | `list_executions` | — |
| `workflows` | `get_workflows_executions_by_param_1` | `get_execution` | param_1 → execution_id |
| `workflows` | `get_workflows_executions_by_param_1_tasks` | `list_execution_tasks` | param_1 → execution_id |
| `workflows` | `get_workflows_runs_by_param_1_steps` | `list_run_steps` | param_1 → run_id |
| `workflows` | `get_workflows_tasks_by_param_1` | `get_task` | param_1 → task_id |
| `workflows` | `get_workflows_templates` | `list_templates` | — |
| `workflows` | `get_workflows_templates_by_param_1` | `get_template` | param_1 → template_id |
| `workflows` | `patch_workflows_by_param_1` | `update_workflow` | param_1 → workflow_id |
| `workflows` | `post_workflows` | `create_workflow` | — |
| `workflows` | `post_workflows_approvals_by_param_1_approve` | `approve_approval` | param_1 → approval_id |
| `workflows` | `post_workflows_approvals_by_param_1_reject` | `reject_approval` | param_1 → approval_id |
| `workflows` | `post_workflows_by_param_1_archive` | `archive_workflow` | param_1 → workflow_id |
| `workflows` | `post_workflows_by_param_1_publish` | `publish_workflow` | param_1 → workflow_id |
| `workflows` | `post_workflows_by_param_1_restore` | `restore_workflow` | param_1 → workflow_id |
| `workflows` | `post_workflows_by_param_1_versions` | `create_version_for_workflow` | param_1 → workflow_id |
| `workflows` | `post_workflows_executions` | `create_execution` | — |
| `workflows` | `post_workflows_tasks_by_param_1_cancel` | `cancel_task` | param_1 → task_id |
| `workflows` | `post_workflows_tasks_by_param_1_retry` | `retry_task` | param_1 → task_id |
| `workflows` | `post_workflows_templates` | `create_template` | — |
| `workflows` | `post_workflows_templates_by_param_1_instantiate` | `instantiate_template` | param_1 → template_id |
